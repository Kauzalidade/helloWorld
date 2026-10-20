import re


def normalizar_cpf(valor):
    """Deixa só os dígitos do CPF."""
    return re.sub(r"\D", "", str(valor or ""))


def _digito(cpf, n):
    soma = sum(int(cpf[i]) * (n + 1 - i) for i in range(n))
    return ((soma * 10) % 11) % 10


def cpf_valido(valor):
    cpf = normalizar_cpf(valor)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    return _digito(cpf, 9) == int(cpf[9]) and _digito(cpf, 10) == int(cpf[10])


def gerar_cpf(base9):
    """Gera um CPF válido a partir de 9 dígitos (usado só em testes e dados de exemplo)."""
    base = normalizar_cpf(base9)[:9].ljust(9, "0")
    base += str(_digito(base, 9))
    base += str(_digito(base, 10))
    return base
