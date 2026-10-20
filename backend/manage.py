"""Comandos de apoio.

    python manage.py init-db
    python manage.py criar-usuario --nome "Maria" --email maria@empresa.com --perfil RH
    python manage.py seed-demo      # filiais e colaboradores fictícios da seção 11 da especificação
"""
import argparse
import getpass
import sys

from werkzeug.security import generate_password_hash

from app import create_app
from app.cpf import gerar_cpf
from app.db import agora, get_db, init_db
from app.security import PERFIS


def criar_usuario(args):
    senha = getpass.getpass("Senha (mín. 8 caracteres): ")
    if len(senha) < 8:
        sys.exit("Senha muito curta.")
    db = get_db()
    db.execute("INSERT INTO usuarios (nome, email, senha_hash, perfil, criado_em) VALUES (?,?,?,?,?)",
               (args.nome, args.email.lower(), generate_password_hash(senha), args.perfil, agora()))
    db.commit()
    print("Usuário criado.")


def seed_demo(_args):
    db = get_db()
    for nome, tipo in (("Matriz", "MATRIZ"), ("Filial 1", "FILIAL"), ("Filial 2", "FILIAL")):
        db.execute("INSERT OR IGNORE INTO filiais (nome, tipo) VALUES (?,?)", (nome, tipo))
    fid = {r["nome"]: r["id"] for r in db.execute("SELECT id, nome FROM filiais")}
    demo = [  # nome, filial, cargo, salário, admissão (seção 11; CPFs fictícios, mas válidos)
        ("Ana Souza", "Matriz", "Atendente", "2200.00", "2023-03-10"),
        ("Bruno Lima", "Filial 1", "Gerente", "5000.00", "2021-01-02"),
        ("Carla Dias", "Filial 2", "Atendente", "1900.00", "2026-09-15"),
        ("Diego Alves", "Matriz", "Operador", "2000.00", "2022-06-05"),
        ("Elisa Rocha", "Filial 1", "Analista", "3000.00", "2024-08-20"),
    ]
    for i, (nome, filial, cargo, sal, adm) in enumerate(demo, start=1):
        db.execute(
            "INSERT OR IGNORE INTO colaboradores (nome, cpf, data_admissao, cargo, filial_id, salario_base, criado_em, atualizado_em) "
            "VALUES (?,?,?,?,?,?,?,?)", (nome, gerar_cpf(f"{i}2345678"), adm, cargo, fid[filial], sal, agora(), agora()))
    db.commit()
    print("Dados de exemplo inseridos.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init-db")
    u = sub.add_parser("criar-usuario")
    u.add_argument("--nome", required=True)
    u.add_argument("--email", required=True)
    u.add_argument("--perfil", required=True, choices=PERFIS)
    sub.add_parser("seed-demo")
    a = ap.parse_args()
    with create_app().app_context():
        if a.cmd == "init-db":
            init_db()
            print("Banco pronto.")
        elif a.cmd == "criar-usuario":
            criar_usuario(a)
        else:
            seed_demo(a)
