import json
import re
from decimal import Decimal

from .calculo import ErroCalculo, Parametros

INICIO_2026 = "2026-01-01"
FIM_2026 = "2026-12-31"

# (nome, valor em JSON, fim da vigência). fim=None: vale até ser substituído por outra vigência.
# Fonte: seção 6 da especificação v1.0 (conferir com o contador antes do uso real - P-02).
PARAMETROS_2026 = [
    ("salario_minimo", "1621.00", FIM_2026),
    ("teto_inss", "8475.55", FIM_2026),
    ("deducao_dependente", "189.59", FIM_2026),
    ("desconto_simplificado", "607.20", FIM_2026),
    ("inss_faixas", '[{"ate": 1621.00, "aliquota": 0.075},'
                    ' {"ate": 2902.84, "aliquota": 0.09},'
                    ' {"ate": 4354.27, "aliquota": 0.12},'
                    ' {"ate": 8475.55, "aliquota": 0.14}]', FIM_2026),
    ("irrf_faixas", '[{"ate": 2428.80, "aliquota": 0, "deduzir": 0},'
                    ' {"ate": 2826.65, "aliquota": 0.075, "deduzir": 182.16},'
                    ' {"ate": 3751.05, "aliquota": 0.15, "deduzir": 394.16},'
                    ' {"ate": 4664.68, "aliquota": 0.225, "deduzir": 675.49},'
                    ' {"ate": null, "aliquota": 0.275, "deduzir": 908.73}]', FIM_2026),
    ("irrf_reducao", '{"limite_isencao": 5000.00, "reducao_max": 312.89, "limite_superior": 7350.00,'
                     ' "fator_a": 978.62, "fator_b": 0.133145}', FIM_2026),
    ("fgts_aliquota", "0.08", None),
    ("divisor_horas", "220", None),
    ("adicional_he_dia_util", "0.5", None),
    ("adicional_he_domingo_feriado", "1.0", None),
    ("dias_base_falta", "30", None),
    ("dias_base_ferias", "30", None),
    ("ferias_adicional_divisor", "3", None),
    ("vt_percentual", "0.06", None),
    ("va_coparticipacao", "0", None),
    ("arredondamento_casas", "2", None),
    ("arredondamento_modo", '"ROUND_HALF_UP"', None),
]


def semear_parametros_2026(db):
    if db.execute("SELECT COUNT(*) FROM parametros").fetchone()[0] > 0:
        return
    for nome, valor, fim in PARAMETROS_2026:
        db.execute("INSERT INTO parametros (nome, valor, inicio, fim) VALUES (?,?,?,?)",
                   (nome, valor, INICIO_2026, fim))


def carregar_parametros(db, competencia):
    """Parâmetros vigentes na competência 'AAAA-MM' (RN-01). Vigência avaliada no 1º dia do mês."""
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", str(competencia or "")):
        raise ErroCalculo("Competência deve estar no formato AAAA-MM.")
    ref = competencia + "-01"
    valores, versoes = {}, {}
    for (nome,) in db.execute("SELECT DISTINCT nome FROM parametros").fetchall():
        linha = db.execute(
            "SELECT valor, inicio FROM parametros WHERE nome=? AND inicio<=? AND (fim IS NULL OR fim>=?) "
            "ORDER BY inicio DESC LIMIT 1", (nome, ref, ref)).fetchone()
        if linha:
            valores[nome] = json.loads(linha["valor"], parse_float=Decimal, parse_int=Decimal)
            versoes[nome] = linha["inicio"]
    return Parametros(valores, versoes)
