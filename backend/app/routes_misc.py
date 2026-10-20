import json
import re

from flask import Blueprint, jsonify, request

from .calculo import ErroCalculo, calcular_ferias, calcular_folha, dec
from .db import get_db
from .parametros import carregar_parametros
from .security import erro, exigir

bp = Blueprint("misc", __name__, url_prefix="/api")


@bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@bp.get("/logs")
@exigir("DIRETORIA", "ADMIN")
def listar_logs():
    """US-07: quem acessou ou alterou o quê. Só diretoria e admin (seção 4)."""
    sql, args = "SELECT * FROM audit_log WHERE 1=1", []
    for param, coluna in (("usuario_email", "usuario_email"), ("entidade", "entidade"),
                          ("entidade_id", "entidade_id"), ("acao", "acao")):
        if request.args.get(param):
            sql += f" AND {coluna}=?"
            args.append(request.args[param])
    if request.args.get("de"):
        sql += " AND data_hora>=?"
        args.append(request.args["de"])
    if request.args.get("ate"):
        sql += " AND data_hora<=?"
        args.append(request.args["ate"] + "T23:59:59" if len(request.args["ate"]) == 10 else request.args["ate"])
    try:
        limite = max(1, min(int(request.args.get("limit", 100)), 1000))
    except ValueError:
        limite = 100
    sql += " ORDER BY id DESC LIMIT ?"
    args.append(limite)
    saida = []
    for r in get_db().execute(sql, args):
        d = dict(r)
        d["antes"] = json.loads(d["antes"]) if d["antes"] else None
        d["depois"] = json.loads(d["depois"]) if d["depois"] else None
        saida.append(d)
    return jsonify(saida)


@bp.get("/parametros")
@exigir("RH", "DIRETORIA")
def ver_parametros():
    try:
        p = carregar_parametros(get_db(), request.args.get("competencia"))
    except ErroCalculo as e:
        return erro(str(e))
    return jsonify({"competencia": request.args.get("competencia"), "valores": p.valores, "vigencias": p.versoes})


@bp.post("/simulacao/folha")
@exigir("RH")
def simular_folha():
    """Calcula a folha de UM colaborador com os dados enviados (sem gravar). Base para a Etapa 3."""
    d = request.get_json(silent=True) or {}
    try:
        p = carregar_parametros(get_db(), d.get("competencia"))
        return jsonify({"competencia": d["competencia"], **calcular_folha(d, p)})
    except ErroCalculo as e:
        return erro(str(e))


@bp.post("/simulacao/ferias")
@exigir("RH")
def simular_ferias():
    d = request.get_json(silent=True) or {}
    try:
        p = carregar_parametros(get_db(), d.get("competencia"))
        salario = dec(d.get("salario_base"), "salario_base")
        media = dec(d.get("media_variaveis", 0), "media_variaveis")
        dias = int(dec(d.get("dias", 30), "dias"))
        return jsonify(calcular_ferias(salario, media, dias, p))
    except ErroCalculo as e:
        return erro(str(e))
