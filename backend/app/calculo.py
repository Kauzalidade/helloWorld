"""Motor de cálculo da folha (funções puras, sem banco e sem Flask).

Regras da especificação v1.0: RN-02, RN-03, RN-20 a RN-24, RN-30 a RN-33, RN-41, RN-50, RN-51.
Dinheiro SEMPRE em Decimal. Nenhum valor legal fica fixo aqui: tudo vem do objeto Parametros.
"""
import decimal
from decimal import Decimal as D, InvalidOperation


class ErroCalculo(ValueError):
    pass


class Parametros:
    """Parâmetros vigentes numa competência (nome -> valor) e a versão (início da vigência) de cada um."""

    def __init__(self, valores, versoes=None):
        self.valores = valores
        self.versoes = versoes or {}

    def __getitem__(self, nome):
        if nome not in self.valores:
            raise ErroCalculo(f"Parâmetro '{nome}' sem vigência para a competência informada.")
        return self.valores[nome]

    def versao(self, *nomes):
        return {n: self.versoes.get(n) for n in nomes}


def dec(valor, nome):
    if isinstance(valor, bool) or valor is None:
        raise ErroCalculo(f"Valor inválido para '{nome}'.")
    try:
        v = D(str(valor))
    except (InvalidOperation, ValueError):
        raise ErroCalculo(f"Valor inválido para '{nome}'.")
    if not v.is_finite():
        raise ErroCalculo(f"Valor inválido para '{nome}'.")
    return v


def arred(valor, p):
    """RN-03: arredondamento configurável (padrão: 2 casas, meio para cima), aplicado em cada verba."""
    casas = int(p["arredondamento_casas"])
    modo = getattr(decimal, p["arredondamento_modo"])
    return valor.quantize(D(1).scaleb(-casas), rounding=modo)


class Memoria:
    """RN-02: registra base, regra, parâmetros (com versão) e arredondamento de cada valor."""

    def __init__(self, p):
        self.p = p
        self.itens = []

    def reg(self, verba, base, regra, nomes_param, bruto, valor):
        self.itens.append({
            "verba": verba,
            "base": {k: (str(v) if isinstance(v, D) else v) for k, v in base.items()},
            "regra": regra,
            "parametros": self.p.versao(*nomes_param),
            "valor_calculado": str(bruto),
            "valor": str(valor),
            "arredondamento": f"{self.p['arredondamento_casas']} casas, {self.p['arredondamento_modo']}",
        })


# ---------------------------------------------------------------- INSS (RN-22)
def calcular_inss(base, p, mem=None):
    teto = p["teto_inss"]
    base_limitada = min(base, teto)
    anterior, total, detalhe = D(0), D(0), []
    for faixa in p["inss_faixas"]:
        if base_limitada <= anterior:
            break
        parte = min(base_limitada, faixa["ate"]) - anterior
        parcela = parte * faixa["aliquota"]
        detalhe.append(f"{parte} x {faixa['aliquota']} = {parcela}")
        total += parcela
        anterior = faixa["ate"]
    valor = arred(total, p)
    if mem:
        mem.reg("INSS", {"base_informada": base, "base_limitada_ao_teto": base_limitada},
                "Cálculo progressivo por faixa, limitado ao teto: " + "; ".join(detalhe),
                ("inss_faixas", "teto_inss"), total, valor)
    return valor


# ---------------------------------------------------------------- IRRF (RN-23)
def _imposto_faixa(base, p):
    for f in p["irrf_faixas"]:
        if f["ate"] is None or base <= f["ate"]:
            return arred(max(base * f["aliquota"] - f["deduzir"], D(0)), p)
    raise ErroCalculo("Tabela do IRRF sem faixa final.")


def calcular_irrf(rendimento, inss, dependentes, p, mem=None):
    ded_dep = p["deducao_dependente"] * dependentes
    base_trad = max(rendimento - inss - ded_dep, D(0))
    base_simp = max(rendimento - p["desconto_simplificado"], D(0))
    imp_trad = _imposto_faixa(base_trad, p)
    imp_simp = _imposto_faixa(base_simp, p)
    if imp_simp < imp_trad:
        usada, base_usada, imposto = "SIMPLIFICADA", base_simp, imp_simp
    else:
        usada, base_usada, imposto = "TRADICIONAL", base_trad, imp_trad

    r = p["irrf_reducao"]
    if rendimento <= r["limite_isencao"]:
        reducao = min(r["reducao_max"], imposto)
    elif rendimento <= r["limite_superior"]:
        reducao = arred(max(r["fator_a"] - r["fator_b"] * rendimento, D(0)), p)
        reducao = min(reducao, imposto)
    else:
        reducao = D(0)
    reducao = arred(reducao, p)
    final = arred(max(imposto - reducao, D(0)), p)

    if mem:
        mem.reg("IRRF - base tradicional",
                {"rendimento_tributavel": rendimento, "inss": inss, "dependentes": dependentes,
                 "deducao_dependentes": ded_dep, "base": base_trad},
                "Rendimento - INSS - (dependentes x dedução); imposto = base x alíquota - parcela a deduzir.",
                ("irrf_faixas", "deducao_dependente"), imp_trad, imp_trad)
        mem.reg("IRRF - base simplificada",
                {"rendimento_tributavel": rendimento, "base": base_simp},
                "Rendimento - desconto simplificado; imposto = base x alíquota - parcela a deduzir.",
                ("irrf_faixas", "desconto_simplificado"), imp_simp, imp_simp)
        mem.reg("IRRF - redução Lei 15.270/2025", {"rendimento_tributavel": rendimento, "imposto": imposto},
                "Até o limite de isenção a redução zera o imposto; na faixa intermediária, fator_a - fator_b x rendimento; "
                "nunca negativa nem maior que o imposto.",
                ("irrf_reducao",), reducao, reducao)
        mem.reg("IRRF", {"base_usada": usada, "imposto_antes_da_reducao": imposto, "reducao": reducao},
                "Usa a base que gera menor imposto; imposto final = imposto - redução (mínimo 0).",
                ("irrf_faixas", "irrf_reducao"), final, final)
    return final, usada, base_usada


# ---------------------------------------------------------------- Horas extras e DSR (RN-30, RN-31)
def horas_extras(salario, h_util, h_dom, p, mem=None):
    if h_util < 0 or h_dom < 0:
        raise ErroCalculo("Hora extra negativa não é permitida.")
    valor_hora = salario / p["divisor_horas"]
    res = {}
    for chave, horas, adicional, rotulo in (
        ("dia_util", h_util, p["adicional_he_dia_util"], "Hora extra dia útil"),
        ("domingo_feriado", h_dom, p["adicional_he_domingo_feriado"], "Hora extra domingo/feriado"),
    ):
        bruto = valor_hora * horas * (1 + adicional)
        valor = arred(bruto, p)
        res[chave] = valor
        if horas > 0 and mem:
            nome_adic = "adicional_he_dia_util" if chave == "dia_util" else "adicional_he_domingo_feriado"
            mem.reg(rotulo, {"salario_base": salario, "valor_hora": valor_hora, "horas": horas, "adicional": adicional},
                    "Valor da hora (salário / divisor) x horas x (1 + adicional).",
                    ("divisor_horas", nome_adic), bruto, valor)
    return res


def dsr_horas_extras(total_he, dias_uteis, domingos_feriados, p, mem=None):
    if total_he == 0:
        return arred(D(0), p)
    if dias_uteis <= 0:
        raise ErroCalculo("Informe os dias úteis do mês para calcular o DSR das horas extras.")
    bruto = total_he / dias_uteis * domingos_feriados
    valor = arred(bruto, p)
    if mem:
        mem.reg("DSR sobre horas extras",
                {"total_horas_extras": total_he, "dias_uteis": dias_uteis, "domingos_feriados": domingos_feriados},
                "(valor das horas extras / dias úteis) x domingos e feriados.", (), bruto, valor)
    return valor


# ---------------------------------------------------------------- Faltas, VT, VA (RN-33, RN-50, RN-51)
def desconto_faltas(salario, dias_falta, p, mem=None):
    bruto = salario / p["dias_base_falta"] * dias_falta
    valor = arred(bruto, p)
    if mem and dias_falta > 0:
        mem.reg("Faltas injustificadas", {"salario_base": salario, "dias_falta": dias_falta},
                "(salário-base / dias base) x dias de falta injustificada.", ("dias_base_falta",), bruto, valor)
    return valor


def desconto_vt(salario, custo_mensal, p, mem=None):
    seis = salario * p["vt_percentual"]
    bruto = min(seis, custo_mensal)
    valor = arred(bruto, p)
    if mem:
        mem.reg("Vale-transporte", {"salario_base": salario, "custo_mensal_vt": custo_mensal, "percentual_do_salario": seis},
                "Menor valor entre o percentual do salário-base e o custo mensal do VT.", ("vt_percentual",), bruto, valor)
    return valor


def desconto_va(valor_va, p, mem=None):
    bruto = valor_va * p["va_coparticipacao"]
    valor = arred(bruto, p)
    if mem and valor > 0:
        mem.reg("Vale-alimentação (coparticipação)", {"valor_va": valor_va},
                "Valor mensal do VA x coparticipação.", ("va_coparticipacao",), bruto, valor)
    return valor


# ---------------------------------------------------------------- Férias (RN-41)
def calcular_ferias(salario, media_variaveis, dias, p):
    if not (1 <= dias <= 30):
        raise ErroCalculo("Dias de férias devem estar entre 1 e 30.")
    mem = Memoria(p)
    remuneracao = salario + media_variaveis
    bruto = remuneracao / p["dias_base_ferias"] * dias
    ferias = arred(bruto, p)
    terco_bruto = ferias / p["ferias_adicional_divisor"]
    terco = arred(terco_bruto, p)
    mem.reg("Férias", {"remuneracao": remuneracao, "dias": dias},
            "(salário-base + média de variáveis) / dias base x dias de férias.", ("dias_base_ferias",), bruto, ferias)
    mem.reg("1/3 constitucional", {"ferias": ferias}, "Férias / divisor do adicional (3).",
            ("ferias_adicional_divisor",), terco_bruto, terco)
    return {"ferias": str(ferias), "adicional_terco": str(terco), "total_bruto": str(arred(ferias + terco, p)),
            "memoria_calculo": mem.itens}


# ---------------------------------------------------------------- Folha mensal (RN-21)
def _nao_negativo(entrada, chave, padrao="0"):
    v = dec(entrada.get(chave, padrao), chave)
    if v < 0:
        raise ErroCalculo(f"'{chave}' não pode ser negativo.")
    return v


def calcular_folha(entrada, p):
    mem = Memoria(p)
    salario = dec(entrada.get("salario_base"), "salario_base")
    if salario <= 0:
        raise ErroCalculo("Salário-base deve ser maior que zero.")
    salario = arred(salario, p)
    dependentes = _nao_negativo(entrada, "dependentes")
    h_util = _nao_negativo(entrada, "horas_extras_dia_util")
    h_dom = _nao_negativo(entrada, "horas_extras_domingo_feriado")
    dias_uteis = _nao_negativo(entrada, "dias_uteis_mes")
    dom_fer = _nao_negativo(entrada, "domingos_feriados_mes")
    dias_falta = _nao_negativo(entrada, "dias_falta")
    vt_optante = bool(entrada.get("vt_optante", False))
    vt_custo = _nao_negativo(entrada, "vt_custo_mensal")
    va_valor = _nao_negativo(entrada, "va_valor_mensal")

    # (1) salário e proventos
    mem.reg("Salário-base", {"salario_base": salario}, "Informado no cadastro do colaborador.", (), salario, salario)
    he = horas_extras(salario, h_util, h_dom, p, mem)
    total_he = he["dia_util"] + he["domingo_feriado"]
    dsr = dsr_horas_extras(total_he, dias_uteis, dom_fer, p, mem)
    proventos = [("SALARIO", "Salário-base", salario)]
    if he["dia_util"] > 0:
        proventos.append(("HE_DIA_UTIL", "Horas extras dia útil", he["dia_util"]))
    if he["domingo_feriado"] > 0:
        proventos.append(("HE_DOM_FER", "Horas extras domingo/feriado", he["domingo_feriado"]))
    if dsr > 0:
        proventos.append(("DSR_HE", "DSR sobre horas extras", dsr))
    total_proventos = sum((v for _, _, v in proventos), D(0))

    # (2) base INSS, (3) INSS, (4)-(5) IRRF
    base_inss = total_proventos
    inss = calcular_inss(base_inss, p, mem)
    irrf, base_irrf, _ = calcular_irrf(total_proventos, inss, dependentes, p, mem)

    # (6) demais descontos
    descontos = [("INSS", "INSS", inss), ("IRRF", "IRRF", irrf)]
    faltas = desconto_faltas(salario, dias_falta, p, mem)
    if faltas > 0:
        descontos.append(("FALTAS", "Faltas injustificadas", faltas))
    if vt_optante:
        descontos.append(("VT", "Vale-transporte", desconto_vt(salario, vt_custo, p, mem)))
    va = desconto_va(va_valor, p, mem)
    if va > 0:
        descontos.append(("VA", "Vale-alimentação (coparticipação)", va))
    total_descontos = sum((v for _, _, v in descontos), D(0))

    # (7) líquido (RN-06) e FGTS (RN-24, encargo da empresa)
    liquido = arred(total_proventos - total_descontos, p)
    fgts_bruto = total_proventos * p["fgts_aliquota"]
    fgts = arred(fgts_bruto, p)
    mem.reg("FGTS (encargo da empresa)", {"remuneracao": total_proventos},
            "Remuneração x alíquota do FGTS. Não é desconto do colaborador.", ("fgts_aliquota",), fgts_bruto, fgts)

    alertas = []
    if liquido < 0:
        alertas.append("Líquido negativo: o fechamento fica bloqueado até haver justificativa (RN-06).")

    def linha(c, d, v):
        return {"codigo": c, "descricao": d, "valor": str(arred(v, p))}

    return {
        "proventos": [linha(*x) for x in proventos],
        "descontos": [linha(*x) for x in descontos],
        "bases": {"inss": str(arred(base_inss, p)), "irrf_rendimento_tributavel": str(arred(total_proventos, p)),
                  "irrf_base_usada": base_irrf},
        "encargos_empresa": {"fgts": str(fgts)},
        "total_proventos": str(arred(total_proventos, p)),
        "total_descontos": str(arred(total_descontos, p)),
        "liquido": str(liquido),
        "bloqueia_fechamento": liquido < 0,
        "alertas": alertas,
        "memoria_calculo": mem.itens,
    }
