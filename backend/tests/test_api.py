import os
import sqlite3
import tempfile
import unittest

from werkzeug.security import generate_password_hash

from app import create_app
from app.cpf import gerar_cpf
from app.db import agora, get_db


class ApiBase(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        self.app = create_app({"TESTING": True, "DATABASE": self.path,
                               "SECRET_KEY": "chave-de-teste-com-mais-de-32-bytes-ok-123"})
        self.c = self.app.test_client()
        with self.app.app_context():
            db = get_db()
            for nome, email, perfil in (("RH", "rh@t.com", "RH"), ("Dir", "dir@t.com", "DIRETORIA"),
                                        ("Adm", "adm@t.com", "ADMIN")):
                db.execute("INSERT INTO usuarios (nome,email,senha_hash,perfil,criado_em) VALUES (?,?,?,?,?)",
                           (nome, email, generate_password_hash("senha-12345"), perfil, agora()))
            db.commit()
        self.rh, self.dir, self.adm = (self.token(e) for e in ("rh@t.com", "dir@t.com", "adm@t.com"))
        self.filial = self.c.post("/api/filiais", json={"nome": "Matriz", "tipo": "MATRIZ"}, headers=self.rh).json["id"]

    def tearDown(self):
        os.unlink(self.path)

    def token(self, email):
        r = self.c.post("/api/auth/login", json={"email": email, "senha": "senha-12345"})
        return {"Authorization": "Bearer " + r.json["token"]}

    def novo(self, **extra):
        d = {"nome": "Ana Souza", "cpf": gerar_cpf("123456789"), "data_admissao": "2023-03-10",
             "salario_base": "2200.00", "filial_id": self.filial}
        d.update(extra)
        return self.c.post("/api/colaboradores", json=d, headers=self.rh)


class TestLoginEPerfis(ApiBase):
    def test_login_invalido(self):
        r = self.c.post("/api/auth/login", json={"email": "rh@t.com", "senha": "errada"})
        self.assertEqual(r.status_code, 401)

    def test_sem_token(self):
        self.assertEqual(self.c.get("/api/colaboradores").status_code, 401)

    def test_diretoria_nao_cadastra(self):
        r = self.c.post("/api/colaboradores", json={}, headers=self.dir)
        self.assertEqual(r.status_code, 403)

    def test_admin_nao_ve_dados_cadastrais(self):
        self.assertEqual(self.c.get("/api/colaboradores", headers=self.adm).status_code, 403)

    def test_rh_nao_ve_log(self):
        self.assertEqual(self.c.get("/api/logs", headers=self.rh).status_code, 403)

    def test_so_admin_gerencia_usuarios(self):
        self.assertEqual(self.c.get("/api/usuarios", headers=self.rh).status_code, 403)
        self.assertEqual(self.c.get("/api/usuarios", headers=self.adm).status_code, 200)


class TestCadastro(ApiBase):
    def test_cria_e_consulta(self):
        r = self.novo()
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json["situacao"], "ATIVO")
        self.assertEqual(r.json["jornada_semanal"], 44)
        self.assertEqual(self.c.get(f"/api/colaboradores/{r.json['id']}", headers=self.dir).status_code, 200)

    def test_cpf_duplicado_rejeitado(self):
        self.assertEqual(self.novo().status_code, 201)
        self.assertEqual(self.novo(nome="Fabio Nunes").status_code, 409)

    def test_cpf_invalido(self):
        self.assertEqual(self.novo(cpf="111.111.111-11").status_code, 400)

    def test_salario_zero_ou_negativo(self):
        self.assertEqual(self.novo(salario_base="0").status_code, 400)
        self.assertEqual(self.novo(salario_base="-10").status_code, 400)

    def test_dados_proibidos(self):
        r = self.novo(religiao="x")
        self.assertEqual(r.status_code, 400)
        self.assertIn("religiao", r.json["detalhes"])

    def test_inativar_em_vez_de_excluir(self):
        cid = self.novo().json["id"]
        r = self.c.delete(f"/api/colaboradores/{cid}", headers=self.rh)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json["colaborador"]["situacao"], "INATIVO")
        self.assertEqual(self.c.get(f"/api/colaboradores/{cid}", headers=self.rh).status_code, 200)

    def test_historico_de_salario_e_filial(self):
        cid = self.novo().json["id"]
        f2 = self.c.post("/api/filiais", json={"nome": "Filial 1", "tipo": "FILIAL"}, headers=self.rh).json["id"]
        self.c.put(f"/api/colaboradores/{cid}", json={"salario_base": "2500.00", "filial_id": f2}, headers=self.rh)
        h = self.c.get(f"/api/colaboradores/{cid}/historico", headers=self.rh).json
        campos = {x["campo"]: x for x in h}
        self.assertEqual(campos["salario_base"]["valor_anterior"], "2200.00")
        self.assertEqual(campos["salario_base"]["valor_novo"], "2500.00")
        self.assertIn("filial_id", campos)

    def test_pendencia_dados_bancarios(self):
        cid = self.novo().json["id"]
        p = self.c.get(f"/api/colaboradores/{cid}/pendencias", headers=self.rh).json["pendencias"]
        self.assertIn("dados bancários", p)
        self.c.put(f"/api/colaboradores/{cid}", json={"banco": "001", "agencia": "1", "conta": "2"}, headers=self.rh)
        p = self.c.get(f"/api/colaboradores/{cid}/pendencias", headers=self.rh).json["pendencias"]
        self.assertNotIn("dados bancários", p)

    def test_busca_por_cpf_e_nome(self):
        self.novo()
        self.assertEqual(len(self.c.get("/api/colaboradores?busca=Ana", headers=self.rh).json), 1)
        self.assertEqual(len(self.c.get("/api/colaboradores?busca=" + gerar_cpf("123456789")[:6], headers=self.rh).json), 1)
        self.assertEqual(len(self.c.get("/api/colaboradores?busca=Zzz", headers=self.rh).json), 0)


class TestLog(ApiBase):
    def test_log_registra_antes_e_depois(self):
        cid = self.novo().json["id"]
        self.c.put(f"/api/colaboradores/{cid}", json={"cargo": "Atendente"}, headers=self.rh)
        logs = self.c.get("/api/logs?entidade=colaborador&acao=ALTERAR", headers=self.dir).json
        self.assertEqual(logs[0]["depois"], {"cargo": "Atendente"})
        self.assertEqual(logs[0]["usuario_email"], "rh@t.com")

    def test_consulta_gera_log(self):
        cid = self.novo().json["id"]
        self.c.get(f"/api/colaboradores/{cid}", headers=self.dir)
        logs = self.c.get("/api/logs?acao=CONSULTA", headers=self.adm).json
        self.assertEqual(logs[0]["usuario_email"], "dir@t.com")

    def test_log_nao_pode_ser_editado_nem_apagado(self):
        self.novo()
        with self.app.app_context():
            db = get_db()
            with self.assertRaises(sqlite3.DatabaseError):
                db.execute("UPDATE audit_log SET acao='X'")
            with self.assertRaises(sqlite3.DatabaseError):
                db.execute("DELETE FROM audit_log")


class TestSimulacao(ApiBase):
    def test_simulacao_folha_via_api(self):
        r = self.c.post("/api/simulacao/folha", json={"competencia": "2026-10", "salario_base": "3000.00"}, headers=self.rh)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json["liquido"], "2751.40")

    def test_competencia_ruim(self):
        r = self.c.post("/api/simulacao/folha", json={"competencia": "x", "salario_base": "3000"}, headers=self.rh)
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main()
