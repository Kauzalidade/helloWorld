# Diretrizes para Agentes de IA — projetoFolha (Sistema de RH e Folha de Pagamento)

Este arquivo define as regras operacionais, comportamentais e técnicas obrigatórias para qualquer agente de inteligência artificial (ou desenvolvedor assistido por IA) atuando neste repositório.

---

## ⚠️ 1. Regra de Ouro: Proibição de Inventar Regras de Negócio

> **Se faltar informação ou houver qualquer ambiguidade, NÃO invente a regra de negócio.**

- Marque qualquer suposição não confirmada explicitamente como **`[HIPÓTESE]`**.
- Adicione a dúvida imediatamente no arquivo [docs/perguntas-pendentes.md](docs/perguntas-pendentes.md).
- Consulte e respeite o documento base: [docs/spec.md](docs/spec.md).
- Toda comunicação de dúvidas de negócio deve ser direcionada à liderança do **GTI 4º período** (Severino Felipe / Antônio Fabrício).

---

## 💰 2. Tratamento Numérico e Financeiro

- **Dinheiro é SEMPRE tipo Decimal de precisão arbitrária:**
  - Em bancos de dados SQL: use `DECIMAL(12, 2)` ou `NUMERIC(12, 2)`.
  - No código (Node.js/TypeScript/Python/Java): **NUNCA use `float` ou o tipo `number` binário padrão** para operações monetárias. Utilize bibliotecas como `decimal.js`, `bignumber.js` ou inteiros em centavos.
  - Ponto flutuante binário causa erros cumulativos de arredondamento e é terminantemente proibido.
- **Arredondamento por Verba (RN-03):**
  - Duas casas decimais, padrão "metade para cima" (*half-up*), aplicado individualmente em cada provento ou desconto antes da soma final.
  - Tolerância de até R$ 0,01 em cálculos de INSS progressivo em relação a calculadoras com parcela a deduzir.

---

## 🏛️ 3. Parametrização e Vigência Legal (RN-01)

- **Zero *hardcoding* de regras legais:**
  - Valores de salário mínimo, teto do INSS, alíquotas por faixa (7,5%, 9%, 12%, 14%), dedução por dependente (R$ 189,59), desconto simplificado (R$ 607,20), percentual do FGTS (8%) e faixas de IRRF **NUNCA** devem ser constantes fixas no código-fonte.
  - Devem ser armazenados em tabelas de parâmetros com colunas de vigência (`data_inicio`, `data_fim`).
  - O cálculo da folha deve consultar exclusivamente os parâmetros com vigência ativa na competência de referência.

---

## 🔒 4. LGPD, Privacidade e Dados Proibidos (RN-14, RNF-04, RNF-07)

- **Campos Proibidos:** O sistema **NÃO DEVE** ter campos cadastrais para religião, orientação sexual, raça/etnia, biometria ou dados genéticos. Qualquer adição necessita de respaldo formal e finalidade legal comprovada.
- **Dados de Saúde:** Atestados médicos, afastamentos e exames ocupacionais são dados sensíveis. O acesso é restrito ao perfil de RH e cada consulta deve ser registrada em log (RN-54).
- **Inativação Obrigatória (RN-12):** Colaboradores desligados **nunca são excluídos fisicamente do banco de dados**, apenas inativados, preservando o histórico legal e auditoria.
- **Logs Imutáveis (RNF-03):** Registros de log de auditoria não podem ser editados nem apagados via aplicação.

---

## 📦 5. Escopo por Etapas e Limitações

Respeite estritamente a fase atual solicitada pelo usuário. Não implemente adiantado módulos pertencentes a etapas posteriores:

1. **Etapa 1:** Login, perfis (RH, Diretoria, Admin), filiais e colaboradores (RN-10 a RN-14, US-01, US-07).
2. **Etapa 2:** Lançamento de eventos (horas extras, faltas, atestados, VT, VA) (RN-30 a RN-34, US-02).
3. **Etapa 3:** Cálculo da folha, memória de cálculo e fechamento (RN-20 a RN-24, US-03, US-04).
4. **Etapa 4:** Férias, 13º, contracheques e relatórios PDF/Excel (RN-40 a RN-57, US-05, US-06, US-08, US-09).

### Itens Fora do Escopo da Versão 1:
- Ponto eletrônico
- Banco de horas (horas extras são sempre pagas)
- Rescisão contratual
- Arquivo bancário CNAB
- Recrutamento, seleção e portal do colaborador
- Integrações automáticas externas (eSocial, Microsoft, Google)

---

## 🧪 6. Testes Automatizados e Cenários de Aceite

- **Escreva os testes primeiro:** Ao implementar qualquer etapa ou cálculo, crie os testes unitários/integração baseados nos cenários Gherkin (Seção 10 da especificação).
- **Casos de Teste Mínimos Obrigatórios:**
  - Salário R$ 3.000,00 (sem dependentes) -> INSS R$ 248,60 | IRRF R$ 0,00 | Líquido R$ 2.751,40
  - Salário R$ 6.000,00 (sem dependentes) -> INSS R$ 641,51 | IRRF R$ 385,10 | Líquido R$ 4.973,39
  - Salário R$ 10.000,00 -> INSS limitado ao teto (R$ 988,09)
  - Casos de borda: CPF duplicado, salário zero ou negativo, horas extras negativas, líquido negativo, fechamento com dados pendentes.

---

## 🤖 7. Utilização de Prompts

Quando o usuário solicitar uma tarefa com IA, use como referência os templates pré-aprovados disponíveis em [docs/uso-de-ia.md](docs/uso-de-ia.md).
