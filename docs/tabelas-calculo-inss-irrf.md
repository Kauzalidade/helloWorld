# Tabelas de cálculo: INSS e IRRF (2026)

> Derivado de `docs/spec.md` (seções 5.3, 6.2, 6.3 e 8). Em caso de divergência, vale a especificação.
> Valores conferidos em 13/10/2026. O contador do cliente deve confirmar antes do uso real (pendência **P-02**).
> **RN-01:** estes valores NÃO podem ficar fixos no código. Devem ser carregados de uma tabela de parâmetros com início e fim de vigência.

## 1. Parâmetros gerais

| Parâmetro | Valor |
|---|---|
| Salário mínimo | R$ 1.621,00 |
| Teto do INSS | R$ 8.475,55 (contribuição máxima R$ 988,09) |
| Dedução por dependente (IRRF) | R$ 189,59 por mês |
| Desconto simplificado (IRRF) | R$ 607,20 por mês |
| FGTS (encargo da empresa) | 8% |
| Divisor de horas mensais | 220 |

## 2. INSS (empregado, progressivo por faixa)

| Faixa | Salário de contribuição | Alíquota | Largura da faixa | Contribuição máxima da faixa |
|---|---|---|---|---|
| 1 | até R$ 1.621,00 | 7,5% | 1.621,00 | R$ 121,575 |
| 2 | R$ 1.621,01 a R$ 2.902,84 | 9% | 1.281,84 | R$ 115,3656 |
| 3 | R$ 2.902,85 a R$ 4.354,27 | 12% | 1.451,43 | R$ 174,1716 |
| 4 | R$ 4.354,28 a R$ 8.475,55 | 14% | 4.121,28 | R$ 576,9792 |

**Fórmula:** `INSS = Σ (parte do salário dentro da faixa × alíquota)`. Acima do teto, usa-se o teto (R$ 988,09).

**Base do INSS (RN-22):** salário-base + horas extras + DSR + demais proventos que incidem.

Alternativa com parcela a deduzir (diferença de até R$ 0,01; os testes aceitam essa tolerância):

| Faixa | Alíquota | Parcela a deduzir |
|---|---|---|
| 1 | 7,5% | 0,00 |
| 2 | 9% | 24,315 |
| 3 | 12% | 111,4002 |
| 4 | 14% | 198,4856 |

## 3. IRRF (mensal)

| Base de cálculo mensal | Alíquota | Parcela a deduzir |
|---|---|---|
| até R$ 2.428,80 | isento | n/a |
| R$ 2.428,81 a R$ 2.826,65 | 7,5% | R$ 182,16 |
| R$ 2.826,66 a R$ 3.751,05 | 15% | R$ 394,16 |
| R$ 3.751,06 a R$ 4.664,68 | 22,5% | R$ 675,49 |
| acima de R$ 4.664,68 | 27,5% | R$ 908,73 |

### Redução da Lei 15.270/2025 (sobre o rendimento tributável mensal)

| Rendimento tributável | Redução |
|---|---|
| até R$ 5.000,00 | até R$ 312,89 (zera o imposto) |
| R$ 5.000,01 a R$ 7.350,00 | R$ 978,62 − (0,133145 × rendimento mensal) |
| acima de R$ 7.350,00 | sem redução |

A redução nunca é negativa nem maior que o imposto apurado.

### Passo a passo (RN-21 e RN-23)

1. Calcular o INSS e arredondar (2 casas, meio para cima, por verba: RN-03).
2. Base **tradicional** = proventos tributáveis − INSS − (dependentes × 189,59).
3. Base **simplificada** = proventos tributáveis − 607,20.
4. Para cada base: `base × alíquota − parcela a deduzir` (base na faixa isenta = 0,00).
5. Usar o **menor** imposto e registrar na memória de cálculo qual base foi usada.
6. Aplicar a redução da Lei 15.270/2025.
7. IRRF final = imposto − redução, mínimo 0,00.

O abono pecuniário de férias não entra na base de INSS e IRRF (RN-43).

## 4. Exemplos para os testes (seção 8 da especificação)

| Caso | INSS | IRRF | Líquido |
|---|---|---|---|
| A: salário 3.000,00, sem dependentes | 121,575 + 115,3656 + 11,6592 = **248,60** | simplificada 2.392,80 (isenta) = **0,00** | **2.751,40** |
| B: salário 6.000,00, sem dependentes | **641,51** (tolerância 0,01) | tradicional 564,85; simplificada 574,29; usa 564,85. Redução 978,62 − 798,87 = 179,75. Final **385,10** | **4.973,39** |
| C: salário 10.000,00 | **988,09** (teto) | n/a | n/a |

## 5. Implementação (para quem for programar)

- Dinheiro sempre em tipo decimal, nunca `float`/`double`.
- Faixas, alíquotas, parcelas, teto, dedução por dependente e desconto simplificado ficam em tabela de parâmetros (nome, valor, início, fim de vigência).
- O cálculo usa o parâmetro vigente na **competência** (cenário "Parâmetro com vigência" do Gherkin).
- Cada valor gera memória de cálculo: base, regra, parâmetro (e versão), arredondamento (RN-02).
