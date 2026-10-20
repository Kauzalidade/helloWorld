import sqlite3
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from flask import Blueprint, g, jsonify, request

from .cpf import cpf_valido, normalizar_cpf
from .db import agora, get_db, registrar_log
from .security import erro, exigir

bp = Blueprint("cadastro", __name__, url_prefix="/api")

CAMPOS = ("nome", "cpf", "data_nascimento", "data_admissao", "cargo", "setor", "filial_id",
          "salario_base", "jornada_semanal", "banco", "agencia", "conta", "dependentes")
OBRIGATORIOS = ("nome", "cpf", "data_admissao", "salario_base", "filial_id")
# RN-14: o cadastro NÃO tem estes campos e rejeita se alguém tentar enviar
PROIBIDOS = {"religiao", "religião", "orientacao_sexual", "sexualidade", "raca", "raça", "etnia",
             "raca_etnia", "cor", "dados_geneticos", "dados_biomedicos", "genetica"}
CAMPOS_HISTORICO = ("salario_base", "cargo", "setor", "filial_id", "situacao")  # RN-07


# ------------------------------------------------------------------ validação
def _data(v):
    try:
        return date.fromisoformat(str(v))
    except ValueError:
        return None


def _inteiro(v):
    if isinstance(v, bool):
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return int(f) if f == int(f) else None


def validar_colaborador(dados, completo):
    erros, limpo = {}, {}
    for k in dados:
        if str(k).lower() in PROIBIDOS:
            erros[k] = "Campo proibido: o sistema não armazena este tipo de dado (RN-14)."
        elif k not in CAMPOS:
            erros[k] = "Campo desconhecido ou não editável por aqui."
    if erros:
        return limpo, erros
    if completo:
        for c in OBRIGATORIOS:
            if dados.get(c) in (None, ""):
                erros[c] = "Obrigatório."
    for c, v in dados.items():
        vazio = v is None or (isinstance(v, str) and not v.strip())
        if vazio:
            if c in OBRIGATORIOS:
                erros[c] = "Obrigatório."
            else:
                limpo[c] = None if c != "dependentes" else 0
            continue
        if c == "nome":
            limpo[c] = str(v).strip()
            if len(limpo[c]) < 2:
                erros[c] = "Nome muito curto."
        elif c == "cpf":
            if not cpf_valido(v):
                erros[c] = "CPF inválido."
            else:
                limpo[c] = normalizar_cpf(v)
        elif c in ("data_nascimento", "data_admissao"):
            d = _data(v)
            if d is None:
                erros[c] = "Data inválida (use AAAA-MM-DD)."
            elif c == "data_nascimento" and d >= date.today():
                erros[c] = "Data de nascimento deve estar no passado."
            else:
                limpo[c] = d.isoformat()
        elif c in ("cargo", "setor", "banco", "agencia", "conta"):
            limpo[c] = str(v).strip()[:100]
        elif c == "filial_id":
            n = _inteiro(v)
            if n is None or n <= 0:
                erros[c] = "Filial inválida."
            else:
                limpo[c] = n
        elif c == "salario_base":
            try:
                s = Decimal(str(v))
            except InvalidOperation:
                s = None
            if isinstance(v, bool) or s is None or not s.is_finite():
                erros[c] = "Salário inválido."
            elif s <= 0:
                erros[c] = "Salário deve ser maior que zero."
            elif s != s.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP):
                erros[c] = "Use no máximo 2 casas decimais."
            else:
                limpo[c] = str(s.quantize(Decimal("0.01")))
        elif c == "jornada_semanal":
            n = _inteiro(v)
            if n is None or not (1 <= n <= 44):
                erros[c] = "Jornada semanal deve estar entre 1 e 44 horas."
            else:
                limpo[c] = n
        elif c == "dependentes":
            n = _inteiro(v)
            if n is None or n < 0:
                erros[c] = "Número de dependentes inválido."
            else:
                limpo[c] = n
    return limpo, erros


def pendencias(c):
    """RN-05 / RN-10: campos obrigatórios ausentes (bloqueiam o fechamento da folha)."""
    falta = []
    for campo, rotulo in (("data_nascimento", "data de nascimento"), ("cargo", "cargo"), ("setor", "setor")):
        if not c[campo]:
            falta.append(rotulo)
    if not (c["banco"] and c["agencia"] and c["conta"]):
        falta.append("dados bancários")
    return falta


# ------------------------------------------------------------------ filiais
def _filial(row):
    return {"id": row["id"], "nome": row["nome"], "tipo": row["tipo"], "ativo": bool(row["ativo"])}


@bp.get("/filiais")
@exigir("RH", "DIRETORIA")
def listar_filiais():
    return jsonify([_filial(r) for r in get_db().execute("SELECT * FROM filiais ORDER BY tipo, nome")])


@bp.post("/filiais")
@exigir("RH")
def criar_filial():
    d = request.get_json(silent=True) or {}
    nome, tipo = str(d.get("nome", "")).strip(), str(d.get("tipo", "FILIAL")).upper()
    if len(nome) < 2 or tipo not in ("MATRIZ", "FILIAL"):
        return erro("Dados inválidos.", 400, detalhes={"nome": "Obrigatório.", "tipo": "MATRIZ ou FILIAL."})
    db = get_db()
    try:
        cur = db.execute("INSERT INTO filiais (nome, tipo) VALUES (?,?)", (nome, tipo))
    except sqlite3.IntegrityError:
        return erro("Já existe filial com este nome.", 409)
    registrar_log("CRIAR", "filial", cur.lastrowid, depois={"nome": nome, "tipo": tipo})
    db.commit()
    return jsonify(_filial(db.execute("SELECT * FROM filiais WHERE id=?", (cur.lastrowid,)).fetchone())), 201


@bp.put("/filiais/<int:fid>")
@exigir("RH")
def alterar_filial(fid):
    d = request.get_json(silent=True) or {}
    db = get_db()
    f = db.execute("SELECT * FROM filiais WHERE id=?", (fid,)).fetchone()
    if not f:
        return erro("Filial não encontrada.", 404)
    novo = {}
    if "nome" in d:
        novo["nome"] = str(d["nome"]).strip()
        if len(novo["nome"]) < 2:
            return erro("Nome inválido.")
    if "tipo" in d:
        if str(d["tipo"]).upper() not in ("MATRIZ", "FILIAL"):
            return erro("Tipo deve ser MATRIZ ou FILIAL.")
        novo["tipo"] = str(d["tipo"]).upper()
    if "ativo" in d:
        novo["ativo"] = 1 if d["ativo"] else 0
    if not novo:
        return erro("Nada para alterar.")
    try:
        db.execute(f"UPDATE filiais SET {', '.join(c + '=?' for c in novo)} WHERE id=?", [*novo.values(), fid])
    except sqlite3.IntegrityError:
        return erro("Já existe filial com este nome.", 409)
    registrar_log("ALTERAR", "filial", fid, antes={c: f[c] for c in novo}, depois=novo)
    db.commit()
    return jsonify(_filial(db.execute("SELECT * FROM filiais WHERE id=?", (fid,)).fetchone()))


# ------------------------------------------------------------------ colaboradores
def _buscar(cid):
    return get_db().execute(
        "SELECT c.*, f.nome AS filial_nome FROM colaboradores c JOIN filiais f ON f.id=c.filial_id WHERE c.id=?",
        (cid,)).fetchone()


def _historico(db, cid, campo, anterior, novo):
    db.execute("INSERT INTO historico_colaborador (colaborador_id, campo, valor_anterior, valor_novo, data_hora, usuario_id) "
               "VALUES (?,?,?,?,?,?)", (cid, campo, None if anterior is None else str(anterior),
                                        None if novo is None else str(novo), agora(), g.usuario["id"]))


@bp.get("/colaboradores")
@exigir("RH", "DIRETORIA")
def listar_colaboradores():
    sql = "SELECT c.*, f.nome AS filial_nome FROM colaboradores c JOIN filiais f ON f.id=c.filial_id WHERE 1=1"
    args = []
    busca = request.args.get("busca", "").strip()
    if busca:
        digitos = normalizar_cpf(busca)
        if digitos:
            sql += " AND (c.nome LIKE ? OR c.cpf LIKE ?)"
            args += [f"%{busca}%", f"%{digitos}%"]
        else:
            sql += " AND c.nome LIKE ?"
            args.append(f"%{busca}%")
    if request.args.get("filial_id"):
        sql += " AND c.filial_id=?"
        args.append(request.args["filial_id"])
    if request.args.get("situacao"):
        sql += " AND c.situacao=?"
        args.append(request.args["situacao"].upper())
    sql += " ORDER BY c.nome"
    return jsonify([dict(r) for r in get_db().execute(sql, args)])


@bp.post("/colaboradores")
@exigir("RH")
def criar_colaborador():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return erro("Envie um JSON com os dados do colaborador.")
    limpo, erros = validar_colaborador(dados, completo=True)
    if erros:
        return erro("Dados inválidos.", 400, detalhes=erros)
    db = get_db()
    filial = db.execute("SELECT ativo FROM filiais WHERE id=?", (limpo["filial_id"],)).fetchone()
    if not filial or not filial["ativo"]:
        return erro("Dados inválidos.", 400, detalhes={"filial_id": "Filial inexistente ou inativa."})
    if db.execute("SELECT 1 FROM colaboradores WHERE cpf=?", (limpo["cpf"],)).fetchone():
        return erro("CPF já cadastrado.", 409, detalhes={"cpf": "Duplicado."})
    limpo.setdefault("jornada_semanal", 44)
    limpo.setdefault("dependentes", 0)
    cols = list(limpo)
    try:
        cur = db.execute(
            f"INSERT INTO colaboradores ({', '.join(cols)}, criado_em, atualizado_em) "
            f"VALUES ({', '.join('?' * len(cols))}, ?, ?)", [*limpo.values(), agora(), agora()])
    except sqlite3.IntegrityError:
        return erro("CPF já cadastrado.", 409, detalhes={"cpf": "Duplicado."})
    registrar_log("CRIAR", "colaborador", cur.lastrowid, depois=limpo)
    db.commit()
    return jsonify(dict(_buscar(cur.lastrowid))), 201


@bp.get("/colaboradores/<int:cid>")
@exigir("RH", "DIRETORIA")
def obter_colaborador(cid):
    c = _buscar(cid)
    if not c:
        return erro("Colaborador não encontrado.", 404)
    registrar_log("CONSULTA", "colaborador", cid)
    get_db().commit()
    return jsonify(dict(c))


@bp.put("/colaboradores/<int:cid>")
@exigir("RH")
def alterar_colaborador(cid):
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict) or not dados:
        return erro("Envie os campos que deseja alterar.")
    db = get_db()
    atual = _buscar(cid)
    if not atual:
        return erro("Colaborador não encontrado.", 404)
    limpo, erros = validar_colaborador(dados, completo=False)
    if erros:
        return erro("Dados inválidos.", 400, detalhes=erros)
    if "filial_id" in limpo:
        filial = db.execute("SELECT ativo FROM filiais WHERE id=?", (limpo["filial_id"],)).fetchone()
        if not filial or not filial["ativo"]:
            return erro("Dados inválidos.", 400, detalhes={"filial_id": "Filial inexistente ou inativa."})
    if "cpf" in limpo and db.execute("SELECT 1 FROM colaboradores WHERE cpf=? AND id<>?", (limpo["cpf"], cid)).fetchone():
        return erro("CPF já cadastrado.", 409, detalhes={"cpf": "Duplicado."})
    mudou = {c: v for c, v in limpo.items() if str(v) != str(atual[c])}
    if mudou:
        try:
            db.execute(f"UPDATE colaboradores SET {', '.join(c + '=?' for c in mudou)}, atualizado_em=? WHERE id=?",
                       [*mudou.values(), agora(), cid])
        except sqlite3.IntegrityError:
            return erro("CPF já cadastrado.", 409, detalhes={"cpf": "Duplicado."})
        for campo in CAMPOS_HISTORICO:
            if campo in mudou:
                _historico(db, cid, campo, atual[campo], mudou[campo])
        registrar_log("ALTERAR", "colaborador", cid, antes={c: atual[c] for c in mudou}, depois=mudou)
        db.commit()
    return jsonify(dict(_buscar(cid)))


@bp.delete("/colaboradores/<int:cid>")
@exigir("RH")
def inativar_colaborador(cid):
    """RN-12: colaborador não é excluído, só inativado."""
    db = get_db()
    atual = _buscar(cid)
    if not atual:
        return erro("Colaborador não encontrado.", 404)
    corpo = request.get_json(silent=True) or {}
    deslig = _data(corpo["data_desligamento"]) if corpo.get("data_desligamento") else date.today()
    if deslig is None:
        return erro("Data de desligamento inválida (use AAAA-MM-DD).")
    if atual["situacao"] != "INATIVO":
        db.execute("UPDATE colaboradores SET situacao='INATIVO', data_desligamento=?, atualizado_em=? WHERE id=?",
                   (deslig.isoformat(), agora(), cid))
        _historico(db, cid, "situacao", "ATIVO", "INATIVO")
        registrar_log("INATIVAR", "colaborador", cid, antes={"situacao": "ATIVO"},
                      depois={"situacao": "INATIVO", "data_desligamento": deslig.isoformat()})
        db.commit()
    return jsonify({"mensagem": "Colaborador inativado. Ele não é excluído; o histórico foi mantido.",
                    "colaborador": dict(_buscar(cid))})


@bp.post("/colaboradores/<int:cid>/reativar")
@exigir("RH")
def reativar_colaborador(cid):
    db = get_db()
    atual = _buscar(cid)
    if not atual:
        return erro("Colaborador não encontrado.", 404)
    if atual["situacao"] != "ATIVO":
        db.execute("UPDATE colaboradores SET situacao='ATIVO', data_desligamento=NULL, atualizado_em=? WHERE id=?",
                   (agora(), cid))
        _historico(db, cid, "situacao", "INATIVO", "ATIVO")
        registrar_log("REATIVAR", "colaborador", cid, antes={"situacao": "INATIVO"}, depois={"situacao": "ATIVO"})
        db.commit()
    return jsonify(dict(_buscar(cid)))


@bp.get("/colaboradores/<int:cid>/historico")
@exigir("RH", "DIRETORIA")
def historico_colaborador(cid):
    if not _buscar(cid):
        return erro("Colaborador não encontrado.", 404)
    linhas = get_db().execute("SELECT * FROM historico_colaborador WHERE colaborador_id=? ORDER BY id", (cid,))
    return jsonify([dict(r) for r in linhas])


@bp.get("/colaboradores/<int:cid>/pendencias")
@exigir("RH", "DIRETORIA")
def pendencias_colaborador(cid):
    c = _buscar(cid)
    if not c:
        return erro("Colaborador não encontrado.", 404)
    return jsonify({"colaborador_id": cid, "pendencias": pendencias(c)})
