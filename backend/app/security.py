from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request

from .db import get_db

PERFIS = ("RH", "DIRETORIA", "ADMIN")


def erro(msg, status=400, **extra):
    return jsonify({"erro": msg, **extra}), status


def gerar_token(usuario):
    agora = datetime.now(timezone.utc)
    payload = {
        "sub": str(usuario["id"]),
        "perfil": usuario["perfil"],
        "iat": agora,
        "exp": agora + timedelta(hours=current_app.config["TOKEN_HORAS"]),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def exigir(*perfis):
    """Exige login e, se informado, um dos perfis (seção 4 da especificação)."""

    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return erro("Não autenticado.", 401)
            try:
                dados = jwt.decode(auth[7:], current_app.config["SECRET_KEY"], algorithms=["HS256"])
                uid = int(dados["sub"])
            except jwt.ExpiredSignatureError:
                return erro("Sessão expirada. Faça login novamente.", 401)
            except (jwt.InvalidTokenError, KeyError, ValueError):
                return erro("Token inválido.", 401)
            u = get_db().execute("SELECT id, nome, email, perfil, ativo FROM usuarios WHERE id=?", (uid,)).fetchone()
            if not u or not u["ativo"]:
                return erro("Usuário inexistente ou inativo.", 401)
            if perfis and u["perfil"] not in perfis:
                return erro("Sem permissão para esta ação.", 403)
            g.usuario = dict(u)
            return f(*args, **kwargs)

        return wrapper

    return decorador
