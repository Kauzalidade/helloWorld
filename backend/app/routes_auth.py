import sqlite3

from flask import Blueprint, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from .db import agora, get_db, registrar_log
from .security import PERFIS, erro, exigir, gerar_token

bp = Blueprint("auth", __name__, url_prefix="/api")


def _usuario_publico(u):
    return {"id": u["id"], "nome": u["nome"], "email": u["email"], "perfil": u["perfil"], "ativo": bool(u["ativo"])}


@bp.post("/auth/login")
def login():
    d = request.get_json(silent=True) or {}
    email = str(d.get("email", "")).strip().lower()
    senha = str(d.get("senha", ""))
    db = get_db()
    u = db.execute("SELECT * FROM usuarios WHERE email=?", (email,)).fetchone()
    if not u or not u["ativo"] or not check_password_hash(u["senha_hash"], senha):
        registrar_log("LOGIN_FALHA", "usuario", None, depois={"email": email}, usuario={"email": email})
        db.commit()
        return erro("E-mail ou senha inválidos.", 401)
    registrar_log("LOGIN", "usuario", u["id"], usuario={"id": u["id"], "email": u["email"]})
    db.commit()
    return jsonify({"token": gerar_token(u), "usuario": _usuario_publico(u)})


@bp.get("/auth/me")
@exigir()
def me():
    return jsonify(_usuario_publico(g.usuario))


# ---- Gerenciar usuários: só ADMIN (seção 4)
@bp.get("/usuarios")
@exigir("ADMIN")
def listar_usuarios():
    linhas = get_db().execute("SELECT * FROM usuarios ORDER BY nome").fetchall()
    return jsonify([_usuario_publico(u) for u in linhas])


@bp.post("/usuarios")
@exigir("ADMIN")
def criar_usuario():
    d = request.get_json(silent=True) or {}
    nome, email = str(d.get("nome", "")).strip(), str(d.get("email", "")).strip().lower()
    senha, perfil = str(d.get("senha", "")), d.get("perfil")
    erros = {}
    if len(nome) < 2:
        erros["nome"] = "Obrigatório."
    if "@" not in email:
        erros["email"] = "E-mail inválido."
    if len(senha) < 8:
        erros["senha"] = "Mínimo de 8 caracteres."
    if perfil not in PERFIS:
        erros["perfil"] = f"Use um de: {', '.join(PERFIS)}."
    if erros:
        return erro("Dados inválidos.", 400, detalhes=erros)
    db = get_db()
    try:
        cur = db.execute("INSERT INTO usuarios (nome, email, senha_hash, perfil, criado_em) VALUES (?,?,?,?,?)",
                         (nome, email, generate_password_hash(senha), perfil, agora()))
    except sqlite3.IntegrityError:
        return erro("Já existe usuário com este e-mail.", 409)
    registrar_log("CRIAR", "usuario", cur.lastrowid, depois={"nome": nome, "email": email, "perfil": perfil})
    db.commit()
    return jsonify(_usuario_publico(db.execute("SELECT * FROM usuarios WHERE id=?", (cur.lastrowid,)).fetchone())), 201


@bp.patch("/usuarios/<int:uid>")
@exigir("ADMIN")
def alterar_usuario(uid):
    d = request.get_json(silent=True) or {}
    db = get_db()
    u = db.execute("SELECT * FROM usuarios WHERE id=?", (uid,)).fetchone()
    if not u:
        return erro("Usuário não encontrado.", 404)
    campos, antes, depois = {}, {}, {}
    if "perfil" in d:
        if d["perfil"] not in PERFIS:
            return erro(f"Perfil inválido. Use um de: {', '.join(PERFIS)}.")
        campos["perfil"] = d["perfil"]
    if "ativo" in d:
        if uid == g.usuario["id"] and not d["ativo"]:
            return erro("Você não pode desativar o próprio usuário.", 409)
        campos["ativo"] = 1 if d["ativo"] else 0
    if "senha" in d:
        if len(str(d["senha"])) < 8:
            return erro("Senha com no mínimo 8 caracteres.")
        campos["senha_hash"] = generate_password_hash(str(d["senha"]))
    if not campos:
        return erro("Nada para alterar.")
    for c, v in campos.items():
        if c != "senha_hash":
            antes[c], depois[c] = u[c], v
    db.execute(f"UPDATE usuarios SET {', '.join(c + '=?' for c in campos)} WHERE id=?", [*campos.values(), uid])
    registrar_log("ALTERAR", "usuario", uid, antes=antes, depois={**depois, **({"senha": "(alterada)"} if "senha_hash" in campos else {})})
    db.commit()
    return jsonify(_usuario_publico(db.execute("SELECT * FROM usuarios WHERE id=?", (uid,)).fetchone()))
