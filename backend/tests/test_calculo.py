"""Testes do motor de cálculo: exemplos da seção 8 e cenários Gherkin da seção 10."""
import sqlite3
import unittest
from decimal import Decimal as D

from app.calculo import ErroCalculo, Memoria, arred, calcular_folha, calcular_ferias, calcular_inss, \
    desconto_vt, horas_extras
from app.db import SCHEMA
from app.parametros import carregar_parametros, semear_parametros_2026


def parametros(competencia="2026-10"):
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    semear_parametros_2026(db)
    return carregar_parametros(db, competencia), db


class TestCalculo(unittest.TestCase):
    def setUp(self):
        self.p, self.db = parametros()

    def test_a_salario_3000(self):
        r = calcular_folha({"salario_base": "3000.00"}, self.p)
        self.assertEqual(r["descontos"][0]["valor"], "248.60")   # INSS
        self.assertEqual(r["descontos"][1]["valor"], "0.00")     # IRRF
        self.assertEqual(r["liquido"], "2751.40")
        self.assertTrue(r["memoria_calculo"])

    def test_b_salario_6000_com_reducao(self):
        r = calcular_folha({"salario_base": "6000.00"}, self.p)
        inss = D(r["descontos"][0]["valor"])
        self.assertLessEqual(abs(inss - D("641.51")), D("0.01"))
        self.assertEqual(r["descontos"][1]["valor"], "385.10")
        self.assertEqual(r["liquido"], "4973.39")
        self.assertEqual(r["bases"]["irrf_base_usada"], "TRADICIONAL")

    def test_c_inss_limitado_ao_teto(self):
        self.assertEqual(calcular_inss(D("10000.00"), self.p), D("988.09"))

    def test_d_horas_extras(self):
        he = horas_extras(D("2200.00"), D(2), D(0), self.p)
        self.assertEqual(he["dia_util"], D("30.00"))
        he = horas_extras(D("2200.00"), D(0), D(2), self.p)
        self.assertEqual(he["domingo_feriado"], D("40.00"))

    def test_hora_extra_negativa_rejeitada(self):
        with self.assertRaises(ErroCalculo):
            horas_extras(D("2200.00"), D(-1), D(0), self.p)

    def test_e_ferias_com_terco(self):
        r = calcular_ferias(D("3000.00"), D(0), 30, self.p)
        self.assertEqual(r["ferias"], "3000.00")
        self.assertEqual(r["adicional_terco"], "1000.00")
        self.assertEqual(r["total_bruto"], "4000.00")

    def test_f_vale_transporte(self):
        self.assertEqual(desconto_vt(D("2000.00"), D("180.00"), self.p), D("120.00"))
        self.assertEqual(desconto_vt(D("2000.00"), D("90.00"), self.p), D("90.00"))

    def test_arredondamento_meio_para_cima(self):
        self.assertEqual(arred(D("12.345"), self.p), D("12.35"))

    def test_salario_zero_rejeitado(self):
        with self.assertRaises(ErroCalculo):
            calcular_folha({"salario_base": "0"}, self.p)

    def test_liquido_negativo_bloqueia_fechamento(self):
        r = calcular_folha({"salario_base": "1500.00", "vt_optante": True, "vt_custo_mensal": "50.00",
                            "dias_falta": 0, "va_valor_mensal": "0"}, self.p)
        self.assertFalse(r["bloqueia_fechamento"])
        # força desconto maior que o provento: coparticipação de VA altíssima não existe, então usa faltas
        r = calcular_folha({"salario_base": "1500.00", "dias_falta": 40}, self.p)
        self.assertTrue(r["bloqueia_fechamento"])
        self.assertTrue(r["alertas"])

    def test_memoria_registra_parametro_e_versao(self):
        r = calcular_folha({"salario_base": "3000.00"}, self.p)
        inss = next(i for i in r["memoria_calculo"] if i["verba"] == "INSS")
        self.assertEqual(inss["parametros"]["inss_faixas"], "2026-01-01")
        self.assertIn("ROUND_HALF_UP", inss["arredondamento"])

    def test_parametro_com_vigencia(self):
        """Nova tabela do INSS começando em 01/01/2027 não afeta a folha de 12/2026."""
        self.db.execute("INSERT INTO parametros (nome, valor, inicio, fim) VALUES (?,?,?,NULL)",
                        ("teto_inss", "9999.99", "2027-01-01"))
        p_2026 = carregar_parametros(self.db, "2026-12")
        p_2027 = carregar_parametros(self.db, "2027-01")
        self.assertEqual(p_2026["teto_inss"], D("8475.55"))
        self.assertEqual(p_2027["teto_inss"], D("9999.99"))

    def test_competencia_sem_tabela_legal_da_erro(self):
        p, _ = parametros("2027-03")
        with self.assertRaises(ErroCalculo):
            calcular_inss(D("3000.00"), p)

    def test_competencia_invalida(self):
        with self.assertRaises(ErroCalculo):
            carregar_parametros(self.db, "10/2026")


if __name__ == "__main__":
    unittest.main()
