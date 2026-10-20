import json
import sqlite3
from datetime import datetime, timezone

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    perfil TEXT NOT NULL CHECK (perfil IN ('RH','DIRETORIA','ADMIN')),
    ativo INTEGER NOT NULL DEFAULT 1,
    criado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS filiais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    tipo TEXT NOT NULL CHECK (tipo IN ('MATRIZ','FILIAL')),
    ativo INTEGER NOT NULL DEFAULT 1
);

-- Dinheiro guardado como TEXT (ex.: '3000.00') e lido como Decimal. Nunca float.
CREATE TABLE IF NOT EXISTS colaboradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    data_nascimento TEXT,
    data_admissao TEXT NOT NULL,
    data_desligamento TEXT,
    cargo TEXT,
    setor TEXT,
    filial_id INTEGER NOT NULL REFERENCES filiais(id),
    salario_base TEXT NOT NULL,
    jornada_semanal INTEGER NOT NULL DEFAULT 44,
    banco TEXT,
    agencia TEXT,
    conta TEXT,
    dependentes INTEGER NOT NULL DEFAULT 0,
    situacao TEXT NOT NULL DEFAULT 'ATIVO' CHECK (situacao IN ('ATIVO','INATIVO')),
    criado_em TEXT NOT NULL,
    atualizado_em TEXT NOT NULL
);

-- RN-07: histórico de salário, cargo, setor, filial e situação
CREATE TABLE IF NOT EXISTS historico_colaborador (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    colaborador_id INTEGER NOT NULL REFERENCES colaboradores(id),
    campo TEXT NOT NULL,
    valor_anterior TEXT,
    valor_novo TEXT,
    data_hora TEXT NOT NULL,
    usuario_id INTEGER
);

-- RNF-03 / US-07: log de acesso e alteração (quem, quando, o quê, antes e depois)
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora TEXT NOT NULL,
    usuario_id INTEGER,
    usuario_email TEXT,
    acao TEXT NOT NULL,
    entidade TEXT NOT NULL,
    entidade_id TEXT,
    antes TEXT,
    depois TEXT
);

-- RN-01: parâmetros legais com início e fim de vigência (valor em JSON)
CREATE TABLE IF NOT EXISTS parametros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    valor TEXT NOT NULL,
    inicio TEXT NOT NULL,
    fim TEXT,
    UNIQUE (nome, inicio)
);

-- Logs e histórico não podem ser editados nem apagados
CREATE TRIGGER IF NOT EXISTS audit_log_sem_update BEFORE UPDATE ON audit_log
BEGIN SELECT RAISE(ABORT, 'audit_log e imutavel'); END;
CREATE TRIGGER IF NOT EXISTS audit_log_sem_delete BEFORE DELETE ON audit_log
BEGIN SELECT RAISE(ABORT, 'audit_log e imutavel'); END;
CREATE TRIGGER IF NOT EXISTS historico_sem_update BEFORE UPDATE ON historico_colaborador
BEGIN SELECT RAISE(ABORT, 'historico e imutavel'); END;
CREATE TRIGGER IF NOT EXISTS historico_sem_delete BEFORE DELETE ON historico_colaborador
BEGIN SELECT RAISE(ABORT, 'historico e imutavel'); END;
"""


def agora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    from .parametros import semear_parametros_2026

    db = get_db()
    db.executescript(SCHEMA)
    semear_parametros_2026(db)
    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()


def registrar_log(acao, entidade, entidade_id=None, antes=None, depois=None, usuario=None):
    """Grava no log. Quem chama é responsável pelo commit (assim log e alteração ficam na mesma transação)."""
    u = usuario or g.get("usuario") or {}

    def js(x):
        return None if x is None else json.dumps(x, ensure_ascii=False, default=str)

    get_db().execute(
        "INSERT INTO audit_log (data_hora, usuario_id, usuario_email, acao, entidade, entidade_id, antes, depois) "
        "VALUES (?,?,?,?,?,?,?,?)",
        (agora(), u.get("id"), u.get("email"), acao, entidade,
         None if entidade_id is None else str(entidade_id), js(antes), js(depois)),
    )
