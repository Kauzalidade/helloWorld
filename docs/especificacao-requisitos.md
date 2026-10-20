# Especificação de Requisitos — Sistema de RH e Folha de Pagamento

**Cliente:** Correspondente bancário (15 colaboradores, matriz + 2 filiais)  
**Elaborado por:** GTI 4º período · **Destino:** GTI 2º período (desenvolvimento)  
**Versão:** 1.0 consolidada · 14/10/2026  

---

## Como ler este documento
Este documento reúne, em um só lugar, tudo que foi definido com o cliente (grupo de RH) e as regras adotadas pelo grupo.
- **[CONFIRMADO]** = Informado pelo cliente.
- **[ADOTADO]** = Padrão recomendado pelo grupo, configurável.
- **[HIPÓTESE]** = Ainda precisa de confirmação.

> **Regra de ouro:** Se faltar informação, **não inventem a regra**; anotem a dúvida e perguntem ao GTI 4º período.

---

## Equipe e Responsáveis

| Nome | Grupo | Função |
| :--- | :--- | :--- |
| **Severino Felipe** | GTI 4º período | Líder e ponte com o 2º período |
| **Antônio Fabrício** | GTI 4º período | Regras de negócio e folha |
| **José Roberto** | GTI 4º período | Contato com o cliente (RH) e ata |
| **Wesley Antônio** | GTI 4º período | Testes e qualidade |
| **Kauã** | GTI 2º período (desenvolvimento) | Representante da turma; função a definir |
| **Jeremias** | GTI 2º período (desenvolvimento) | A definir pela equipe após receber o documento |
| **Valdir** | GTI 2º período (desenvolvimento) | A definir pela equipe após receber o documento |
| **Vitor** | Grupo de RH (cliente) | Diretor de Recursos Humanos: coordena a equipe, acompanha resultados e supervisiona as atividades |
| **Deyse** | Grupo de RH (cliente) | Analista de Departamento Pessoal: folha, férias, 13º, benefícios e documentos |
| **Alana Catiany de Morais** | Grupo de RH (cliente) | Analista de Recrutamento e Seleção. Passou as informações ao GTI |
| **Marília** | Grupo de RH (cliente) | Analista de Treinamento e Desenvolvimento |
| **Thayane** | Grupo de RH (cliente) | Analista de Gestão e Relatórios: organiza dados, controla planilhas e elabora relatórios |

---

## 1. Objetivo e Decisões do Cliente

O cliente quer organizar e calcular a folha de pagamento (férias, 13º, horas extras e demais verbas), com acesso restrito a RH e diretoria, backup diário e primeira entrega em 15 dias. O sistema calcula a folha (decisão do grupo).

| Tema | Decisão | Status |
| :--- | :--- | :--- |
| **Colaboradores** | 15, todos CLT. Sem estagiários, PJ ou aprendizes na 1ª versão | **CONFIRMADO** |
| **Estrutura** | 1 matriz + 2 filiais (filial é cadastro, não fixa no código) | **CONFIRMADO** |
| **Jornada** | 44 horas semanais (divisor 220 horas/mês) | **CONFIRMADO** |
| **Horas extras** | 50% em dia útil; 100% em domingo e feriado, conforme legislação e convenção | **CONFIRMADO** |
| **Banco de horas** | Não será usado. Horas extras sempre pagas | **CONFIRMADO** |
| **Ponto** | Sem registro eletrônico. O RH lança horas extras e faltas por mês | **CONFIRMADO** |
| **Pagamento** | Transferência bancária, até o 5º dia útil do mês seguinte. Arquivo bancário fica para depois; a 1ª versão gera dados e relatórios de pagamento | **CONFIRMADO** |
| **Fechamento** | O RH confere, fecha e aprova a folha. A diretoria acompanha e consulta relatórios | **CONFIRMADO** |
| **Benefícios** | Vale-transporte e vale-alimentação; outros no futuro | **CONFIRMADO** |
| **Férias e 13º** | 30 dias com 1/3; 13º em duas parcelas (até 30/11 e 20/12) | **CONFIRMADO** |
| **Rescisão** | Segunda etapa | **CONFIRMADO** |
| **Documentos** | CPF, documento de identificação, contrato, comprovante de residência, dados bancários, documentos admissionais e atestados | **CONFIRMADO** |
| **Alertas** | Documentos com validade, exames ocupacionais periódicos e outros prazos administrativos | **CONFIRMADO** |
| **Acesso** | Só RH e diretoria, com permissões por função | **CONFIRMADO** |
| **Dados sensíveis** | NÃO armazenar religião, sexualidade, raça, dados genéticos ou biomédicos sem finalidade legítima e específica. O sistema não terá esses campos | **CONFIRMADO** |
| **Convenção coletiva** | Existe uma convenção aplicável; nome e valores ainda não informados. Valem os padrões da CLT até lá | **PENDENTE** |

---

## 2. Escopo e Etapas de Construção

| Etapa | O que construir | Pronto quando |
| :---: | :--- | :--- |
| **1** | Login, perfis (RH e diretoria), cadastro de filiais e colaboradores | Cadastra, edita, consulta e inativa; CPF duplicado é rejeitado |
| **2** | Lançamento de eventos: horas extras, faltas, atestados, VT e VA | Cenários de horas extras e descontos passam |
| **3** | Cálculo da folha, memória de cálculo e fechamento | Folha calculada com memória; fechamento bloqueado nos casos da tabela 7.1 |
| **4** | Férias, 13º, documentos com alerta, contracheque e relatórios | Cenários de férias passam; relatórios exportam em PDF e Excel |

- **Fora da 1ª versão:** Ponto eletrônico, banco de horas, rescisão, arquivo bancário, recrutamento, desempenho e treinamentos, portal do colaborador, integrações (eSocial, Microsoft 365, Google).
- **Sugestão técnica:** Sistema web com banco relacional (PostgreSQL ou MySQL). Dinheiro sempre em tipo decimal, nunca ponto flutuante. Parâmetros legais em tabela do banco, com data de início e fim de vigência.

---

## 3. Glossário

| Termo | Definição |
| :--- | :--- |
| **Competência** | Mês/ano de referência da folha (ex.: 10/2026) |
| **Evento** | Lançamento que gera provento ou desconto (hora extra, falta, VT, VA) |
| **Provento / Desconto** | Valor recebido / valor retirado do colaborador |
| **Base de cálculo** | Conjunto de valores usados para calcular um provento ou desconto |
| **Memória de cálculo** | Registro passo a passo de como cada valor foi calculado |
| **Fechamento** | Trava da competência após conferência do RH; depois disso não se altera sem reabertura justificada |
| **Período aquisitivo / concessivo** | 12 meses que dão direito às férias / 12 meses seguintes para concedê-las |
| **Abono pecuniário** | Venda de até 1/3 das férias |
| **DSR** | Descanso semanal remunerado |
| **Parâmetro** | Valor que muda com o tempo (tabelas, percentuais) e não pode ficar fixo no código |

---

## 4. Perfis e Permissões

| Ação | RH | Diretoria | Admin do sistema |
| :--- | :---: | :---: | :---: |
| Cadastrar/editar colaborador e filial | Sim | Não | Não |
| Consultar dados cadastrais | Sim | Sim | Não |
| Lançar eventos e calcular folha | Sim | Não | Não |
| Conferir, fechar e aprovar folha | Sim | Não | Não |
| Reabrir competência fechada | Solicita, com justificativa | Aprova **[HIPÓTESE]** | Não |
| Consultar folha e relatórios | Sim | Sim | Não |
| Ver dados de saúde (atestados, exames) | Sim | Não **[HIPÓTESE]** | Não |
| Ver log de acessos e alterações | Não | Sim | Sim |
| Gerenciar usuários | Não | Não | Sim |

---

## 5. Regras de Negócio

### 5.1 Regras gerais
- **RN-01 Parametrização:** Nenhum valor legal ou percentual fixo no código. Cada parâmetro tem nome, valor, início e fim de vigência. O cálculo usa o parâmetro vigente na competência.
- **RN-02 Memória de cálculo:** Cada valor registra base, regra aplicada, parâmetro (e versão) e arredondamento.
- **RN-03 Arredondamento [ADOTADO]:** 2 casas decimais, meio para cima, aplicado em cada verba antes de somar. Regra configurável.
- **RN-04 Fechamento:** Competência fechada não aceita alteração. Reabrir exige justificativa, usuário, data e aprovação da diretoria **[HIPÓTESE]**.
- **RN-05 Dado obrigatório ausente:** Bloqueia o fechamento e indica o campo pendente.
- **RN-06 Líquido negativo:** Bloqueia o fechamento e exige justificativa.
- **RN-07 Histórico:** Mudanças de salário, cargo, setor, filial e situação geram registro com data, valor anterior e novo valor.

### 5.2 Cadastro
- **RN-10 Dados mínimos [HIPÓTESE]:** Nome, CPF, nascimento, admissão, cargo, setor, filial, salário-base, jornada, dados bancários, dependentes (para IRRF).
- **RN-11 CPF único e válido:** Duplicado é rejeitado.
- **RN-12 Inativação:** Colaborador não é excluído, apenas inativado.
- **RN-13 Filial única:** Um colaborador pertence a uma filial por vez; transferência registra data e histórico.
- **RN-14 Dados proibidos:** O cadastro não terá campos de religião, orientação sexual, raça/etnia, dados genéticos ou biomédicos. Qualquer inclusão futura exige finalidade e base legal registradas.

### 5.3 Cálculo mensal
- **RN-20 Proporcionalidade [HIPÓTESE]:** A folha considera colaboradores ativos no período; admitidos ou desligados no mês recebem proporcional aos dias trabalhados.
- **RN-21 Ordem de cálculo:**
  1. Salário e proventos
  2. Base do INSS
  3. INSS
  4. Base do IRRF
  5. IRRF
  6. Demais descontos
  7. Líquido (Líquido = Proventos − Descontos)
- **RN-22 INSS:** Base = Salário-base + horas extras + DSR + demais proventos que incidem. Cálculo progressivo por faixa (seção 6.2), limitado ao teto.
- **RN-23 IRRF:** O sistema calcula duas bases e usa a que gerar menor imposto:
  - *(a) Tradicional:* Proventos tributáveis − INSS − (dependentes × R$ 189,59)
  - *(b) Simplificada:* Proventos tributáveis − R$ 607,20
  - Imposto = Base × Alíquota − Parcela a deduzir; depois aplica a redução da seção 6.3; mínimo 0,00. Registrar na memória qual base foi usada.
- **RN-24 FGTS:** 8% sobre a remuneração, mostrado como encargo da empresa, não como desconto do colaborador.

### 5.4 Horas extras, DSR e faltas
- **RN-30 Valor da hora:** Salário-base / 220.
  - Dia útil: Hora × 1,5.
  - Domingo e feriado: Hora × 2,0.
  - Adicionais são parâmetros (convenção pode alterar).
- **RN-31 DSR sobre horas extras:**
  $$\text{DSR} = \left(\frac{\text{Total de horas extras do mês}}{\text{Dias úteis do mês}}\right) \times \text{Domingos e feriados do mês}$$
  Integra a base de INSS e IRRF.
- **RN-32 Reflexos:** A média das horas extras do período reflete em férias e 13º.
- **RN-33 Faltas:** Desconto = $(\text{salário-base} / 30) \times \text{dias de falta injustificada}$, mais perda do DSR da semana. Atestado médico válido não desconta. Atestados exigem anexo e período.
- **RN-34 Afastamentos [HIPÓTESE]:** (INSS, maternidade, paternidade, acidente): data de início, fim previsto e tipo; alerta ao RH perto do término. Tratamento na folha a detalhar com o contador.

### 5.5 Férias e 13º
- **RN-40 Períodos:** Período aquisitivo de 12 meses a partir da admissão; depois, concessivo de 12 meses.
- **RN-41 Remuneração de férias:** 30 dias corridos mais 1/3 constitucional sobre a remuneração (salário-base + média de variáveis).
- **RN-42 Fracionamento [HIPÓTESE]:** Em até 3 períodos: um com no mínimo 14 dias e os demais com no mínimo 5 dias.
- **RN-43 Abono pecuniário:** Até 1/3 dos dias pode virar dinheiro, sem incidência de INSS e IRRF sobre o abono. INSS e IRRF incidem sobre as férias gozadas.
- **RN-44 Impacto de faltas nas férias [HIPÓTESE]:** Faltas injustificadas no aquisitivo reduzem dias de direito conforme tabela (parâmetro).
- **RN-45 Alertas e validação de férias:** Alerta ao RH quando o concessivo estiver perto do fim (sugestão: 60 dias). Pedido de férias antes de completar o aquisitivo é rejeitado.
- **RN-46 13º salário:** 1/12 por mês com 15 dias ou mais trabalhados.
  - 1ª parcela = 50% do salário (mais média proporcional), sem descontos, até 30/11.
  - 2ª parcela (até 20/12) = 13º integral menos 1ª parcela, com INSS e IRRF calculados sobre o 13º à parte.

### 5.6 Benefícios, documentos e dados
- **RN-50 Vale-transporte [ADOTADO]:** Só para quem optar. Desconto = menor valor entre 6% do salário-base e o custo mensal do VT informado pelo RH.
- **RN-51 Vale-alimentação [ADOTADO]:** Valor mensal fixo por colaborador (parâmetro). Coparticipação padrão 0%, configurável.
- **RN-52 Documentos:** Anexos por colaborador com tipo, validade (quando houver) e quem anexou. Alerta de vencimento com antecedência configurável (sugestão 30 dias). Documento sem validade não gera alerta.
- **RN-53 Exames ocupacionais:** Cadastrar data do último exame e periodicidade; alertar o RH antes do vencimento.
- **RN-54 Saúde:** Atestados e exames são dados de saúde, com acesso restrito e log de cada consulta.
- **RN-55 Contracheque [ADOTADO]:** PDF gerado pelo RH por colaborador e competência, com proventos, descontos, líquido e memória resumida. Não há portal para o colaborador.
- **RN-56 Retenção e LGPD [ADOTADO]:** Dados e documentos guardados durante o vínculo e por 5 anos após o desligamento; depois, eliminar ou anonimizar (LGPD). O sistema sinaliza os dados vencidos; a eliminação exige confirmação do RH e fica em log.
- **RN-57 Dados de pagamento:** Relatório com colaborador, líquido, dados bancários e competência.

---

## 6. Parâmetros Legais de 2026

Valores conferidos em 13/10/2026 em fontes públicas (Portaria Interministerial MPS/MF 13/2026 para o INSS; Lei 15.270/2025 e tabela da Receita Federal para o IRRF). Todos entram no sistema como parâmetros com vigência. O contador do cliente deve confirmar antes do uso real.

### 6.1 Parâmetros gerais

| Parâmetro | Valor |
| :--- | :--- |
| **Salário mínimo** | R$ 1.621,00 |
| **Teto do INSS** | R$ 8.475,55 (contribuição máxima R$ 988,09) |
| **Dedução por dependente (IRRF)** | R$ 189,59 por mês |
| **Desconto simplificado (IRRF)** | R$ 607,20 por mês |
| **FGTS (encargo da empresa)** | 8% |
| **Divisor de horas mensais** | 220 |

### 6.2 INSS 2026 (empregado, cálculo progressivo por faixa)

| Faixa | Salário de contribuição | Alíquota |
| :---: | :--- | :---: |
| 1 | Até R$ 1.621,00 | 7,5% |
| 2 | De R$ 1.621,01 a R$ 2.902,84 | 9% |
| 3 | De R$ 2.902,85 a R$ 4.354,27 | 12% |
| 4 | De R$ 4.354,28 até R$ 8.475,55 | 14% |

*Cada alíquota incide apenas sobre a parte do salário dentro da faixa; somam-se os valores. Acima do teto usa-se o teto. O cálculo por faixa pode diferir em até R$ 0,01 de calculadoras que usam parcela a deduzir; os testes aceitam essa tolerância.*

### 6.3 IRRF 2026 (mensal)

| Base de cálculo mensal | Alíquota | Parcela a deduzir |
| :--- | :---: | :---: |
| Até R$ 2.428,80 | Isento | — |
| De R$ 2.428,81 a R$ 2.826,65 | 7,5% | R$ 182,16 |
| De R$ 2.826,66 a R$ 3.751,05 | 15% | R$ 394,16 |
| De R$ 3.751,06 a R$ 4.664,68 | 22,5% | R$ 675,49 |
| Acima de R$ 4.664,68 | 27,5% | R$ 908,73 |

**Redução da Lei 15.270/2025:**
- Rendimento tributável mensal até R$ 5.000,00: tem redução de até R$ 312,89, que zera o imposto.
- De R$ 5.000,01 a R$ 7.350,00: $\text{Redução} = 978,62 - (0,133145 \times \text{rendimento mensal})$, nunca negativa nem maior que o imposto apurado.
- Acima de R$ 7.350,00: sem redução.

---

## 7. Tabelas de Decisão

### 7.1 Fechamento da folha

| Situação | Dado obrigatório | Líquido | Ação do sistema |
| :--- | :--- | :--- | :--- |
| **Normal** | Completo | Maior ou igual a 0 | Permite fechar e exibe memória de cálculo |
| **Dado ausente** | Faltando | — | Bloqueia e mostra o campo pendente |
| **Líquido negativo** | Completo | Menor que 0 | Bloqueia e exige justificativa |
| **Líquido negativo justificado** | Completo | Menor que 0 | Permite fechar e registra a justificativa |

### 7.2 Pedido de férias

| Aquisitivo completo | Dentro do concessivo | Fracionamento válido | Ação |
| :---: | :---: | :---: | :--- |
| Sim | Sim | Sim | Enviar para aprovação |
| Não | — | — | Rejeitar: ainda sem direito |
| Sim | Não (vencido) | — | Alertar RH; aprovar só com justificativa |
| Sim | Sim | Não | Rejeitar informando o motivo |

### 7.3 Horas extras

| Dia | Adicional | Observação |
| :--- | :--- | :--- |
| **Dia útil** | 50% (parâmetro) | Mínimo legal |
| **Domingo ou feriado** | 100% (parâmetro) | Conforme cliente e convenção |

---

## 8. Exemplos Numéricos para os Testes

- **A. Salário R$ 3.000,00, sem dependentes:**
  - INSS: $121,575 + 115,3656 + (97,16 \times 12\% = 11,6592) = \text{R\$} 248,60$.
  - IRRF: Base simplificada $2.392,80$ cai na faixa isenta = $\text{R\$} 0,00$.
  - Líquido: $\text{R\$} 2.751,40$.
- **B. Salário R$ 6.000,00, sem dependentes:**
  - INSS: $121,575 + 115,3656 + 174,1716 + (1.645,73 \times 14\% = 230,4022) = \text{R\$} 641,51$ (tolerância R$ 0,01).
  - IRRF tradicional: base $5.358,49 \times 27,5\% - 908,73 = 564,85$;
  - IRRF simplificado: $574,29$; usa o menor ($564,85$).
  - Redução Lei 15.270/2025: $978,62 - (0,133145 \times 6.000) = 179,75$.
  - IRRF final: $564,85 - 179,75 = \text{R\$} 385,10$.
  - Líquido: $\text{R\$} 4.973,39$.
- **C. Acima do teto (R$ 10.000,00):**
  - INSS limitado ao teto: $\text{R\$} 988,09$.
- **D. Horas extras:**
  - Salário R$ 2.200,00 / 220 = R$ 10,00 por hora.
  - 2 horas em dia útil = $\text{R\$} 30,00$.
  - 2 horas em domingo = $\text{R\$} 40,00$.
- **E. Férias:**
  - Salário R$ 3.000,00 com 30 dias: férias $3.000,00 + 1/3 (1.000,00) = \text{R\$} 4.000,00$ brutos.
- **F. Vale-transporte:**
  - Salário R$ 2.000,00:
    - Custo R$ 180,00 gera desconto de $\text{R\$} 120,00$ (6%).
    - Custo R$ 90,00 gera desconto de $\text{R\$} 90,00$ (limitado ao custo).

---

## 9. User Stories

| ID | História | Critérios de aceite |
| :--- | :--- | :--- |
| **US-01** | Como analista de RH, quero cadastrar e inativar colaboradores para manter a base atualizada. | CPF novo e válido cria o colaborador. CPF repetido é rejeitado. Desligado é inativado, nunca excluído. |
| **US-02** | Como analista de RH, quero lançar horas extras, faltas, atestados, VT e VA para entrarem na folha. | Evento fica salvo com usuário e data. Competência fechada rejeita lançamento. |
| **US-03** | Como analista de RH, quero ver a memória de cálculo para explicar o pagamento. | Mostra base, regra, valor e arredondamento; registra usuário, data e versão dos parâmetros. |
| **US-04** | Como analista de RH, quero fechar a folha só com dados completos. | Dado ausente bloqueia e indica o campo. Líquido negativo exige justificativa. |
| **US-05** | Como analista de RH, quero controlar saldo e pedidos de férias. | Aquisitivo incompleto rejeita. Concessivo perto do fim gera alerta. |
| **US-06** | Como analista de RH, quero anexar documentos com validade e receber alertas. | Documento com validade em 30 dias gera alerta. Exame ocupacional próximo gera alerta. |
| **US-07** | Como diretor, quero saber quem acessou ou alterou cada informação. | Registra usuário, data, hora e valores antes e depois. |
| **US-08** | Como diretor, quero relatórios em PDF ou Excel. | Arquivo gerado com os mesmos valores da tela. |
| **US-09** | Como analista de RH, quero gerar o contracheque em PDF. | PDF com proventos, descontos e líquido por competência. |

---

## 10. Cenários de Aceite (Gherkin)

```gherkin
Funcionalidade: Folha de pagamento

  Cenario: Calculo normal com memoria de calculo
    Dado um colaborador ativo com salario-base 3.000,00 na competencia 10/2026
    Quando o RH calcular a folha
    Entao o INSS deve ser 248,60 e o IRRF deve ser 0,00
    E a memoria de calculo deve mostrar base, regra, valor e arredondamento

  Cenario: INSS limitado ao teto
    Dado um colaborador com salario-base 10.000,00
    Quando a folha for calculada
    Entao o INSS deve ser 988,09

  Cenario: IRRF com reducao entre 5.000,01 e 7.350,00
    Dado um colaborador com salario-base 6.000,00 e sem dependentes
    Quando a folha for calculada
    Entao o IRRF deve ser 385,10

  Cenario: Dado obrigatorio ausente bloqueia fechamento
    Dado um colaborador ativo sem dados bancarios
    Quando o RH tentar fechar a competencia
    Entao o sistema bloqueia e indica "dados bancarios" como pendente

  Cenario: Liquido negativo
    Dado um colaborador cujos descontos superam os proventos
    Quando a folha for calculada
    Entao o sistema bloqueia o fechamento e exige justificativa

  Cenario: Competencia fechada nao e alterada
    Dado uma competencia fechada
    Quando o RH tentar lancar um evento
    Entao o sistema rejeita e informa que a competencia esta fechada

  Cenario: Hora extra em dia util e em domingo
    Dado um colaborador com salario-base 2.200,00 e divisor 220
    Quando o RH lancar 2 horas extras em dia util
    Entao o valor pago deve ser 30,00
    Quando o RH lancar 2 horas extras em domingo
    Entao o valor pago deve ser 40,00

  Cenario: Ferias com 1/3 constitucional
    Dado um colaborador com salario-base 3.000,00 e 30 dias de ferias aprovados
    Entao o valor das ferias e 3.000,00 e o adicional de 1/3 e 1.000,00

  Cenario: Pedido de ferias antes do periodo aquisitivo
    Dado um colaborador admitido ha 8 meses
    Quando solicitar ferias
    Entao o sistema rejeita informando que o periodo aquisitivo nao foi completado

  Cenario: Desconto do vale-transporte
    Dado um colaborador optante com salario-base 2.000,00 e custo mensal de 180,00
    Entao o desconto deve ser 120,00
    Dado custo mensal de 90,00
    Entao o desconto deve ser 90,00

  Cenario: Arredondamento por verba
    Dado uma verba calculada em 12,345
    Entao a verba deve ser registrada como 12,35

  Cenario: Parametro com vigencia
    Dado uma nova tabela do INSS com inicio em 01/01/2027
    Quando a folha de 12/2026 for recalculada
    Entao o sistema deve usar a tabela de 2026

  Cenario: Log de acesso a dado de saude
    Dado um usuario autorizado
    Quando ele consultar um atestado
    Entao o sistema registra usuario, data, hora e dado consultado

  Cenario: Inativar em vez de excluir
    Dado um colaborador desligado
    Quando o RH tentar exclui-lo
    Entao o sistema apenas o inativa e mantem o historico
```

---

## 11. Dados de Exemplo (Fictícios)

| Colaborador | Filial | Cargo | Salário-base | Admissão | Caso |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ana Souza** | Matriz | Atendente | R$ 2.200,00 | 10/03/2023 | Normal, com 2 h extras |
| **Bruno Lima** | Filial 1 | Gerente | R$ 5.000,00 | 02/01/2021 | Férias com abono |
| **Carla Dias** | Filial 2 | Atendente | R$ 1.900,00 | 15/09/2026 | Admissão no meio do mês |
| **Diego Alves** | Matriz | Operador | R$ 2.000,00 | 05/06/2022 | Atestado de 3 dias |
| **Elisa Rocha** | Filial 1 | Analista | R$ 3.000,00 | 20/08/2024 | Desligada em 10/2026 (borda) |
| **Fabio Nunes** | Matriz | Atendente | R$ 2.200,00 | 01/02/2025 | ERRO: CPF duplicado |
| **Gabi Melo** | Matriz | Atendente | R$ 0,00 | 01/04/2025 | ERRO: Salário zero |

**Casos de borda a cobrir nos testes:** CPF duplicado, salário zero ou negativo, hora extra negativa, líquido negativo, competência fechada, admissão e desligamento no mesmo mês, férias cruzando dois meses, salário acima do teto do INSS.

---

## 12. Telas da 1ª Versão

| Tela | Conteúdo |
| :--- | :--- |
| **Login** | E-mail, senha e controle de sessão |
| **Lista de colaboradores** | Busca por nome ou CPF, filtro por filial e situação, botão Novo |
| **Ficha do colaborador** | Abas: Dados, Contrato, Documentos, Férias, Histórico. Botões Editar e Inativar |
| **Lançamento de eventos** | Competência, colaborador, tipo (hora extra, falta, atestado, VT, VA), quantidade e observação |
| **Folha do mês** | Status da competência, botões Calcular e Fechar, lista com proventos, descontos, líquido e pendências; clicar na linha abre a memória de cálculo |
| **Férias** | Período aquisitivo e concessivo, saldo, solicitação, status e aprovação, alerta de vencimento |
| **Contracheque** | Geração em PDF por colaborador e competência |
| **Relatórios** | Seleção do relatório e competência, exportação em PDF e Excel |
| **Alertas** | Documentos, exames ocupacionais, férias a vencer e afastamentos |

---

## 13. Relatórios [ADOTADO]

Todos com exportação em PDF e Excel e com competência, filial, data de geração e usuário. O relatório de log só aparece para diretoria e admin.
- Folha do mês por filial e total
- Contracheque individual
- Férias (saldo e vencimentos)
- Horas extras do mês
- Colaboradores ativos por filial
- Documentos e exames a vencer
- Dados de pagamento (colaborador, líquido, dados bancários)
- Log de acessos e alterações

---

## 14. Segurança, LGPD e Backup

- **RNF-01 Autenticação:** Login com senha e controle de sessão; senhas com hash.
- **RNF-02 Autorização:** Permissões por perfil (seção 4).
- **RNF-03 Trilha de auditoria:** Log de acesso e alteração (quem, quando, o quê, valor antes e depois). Logs não podem ser editados nem apagados.
- **RNF-04 Criptografia:** Dados sensíveis e dados de saúde cifrados em repouso.
- **RNF-05 Backup diário:** Com teste periódico de restauração **[CONFIRMADO]**.
- **RNF-06 Plataforma:** Acesso por computador; celular responsivo se der tempo **[HIPÓTESE]**.
- **RNF-07 LGPD:** Finalidade clara para cada dado, acesso mínimo necessário e retenção de 5 anos após o desligamento.

---

## 15. Prompts para usar com IA

Cole este documento antes de cada prompt. Regra comum: *"Não crie regra de negócio. Se faltar informação, marque como hipótese e liste como pergunta pendente."*

| Prompt | Texto |
| :--- | :--- |
| **1. Revisar a spec** | Você é analista de requisitos. Liste ambiguidades, regras sem exemplo, casos de borda faltando e contradições, em tabela. Não crie regra nova. |
| **2. Gerar testes** | A partir das regras RN-30 a RN-33 e dos cenários Gherkin, gere testes automatizados de horas extras com casos de borda. Use tipo decimal para dinheiro. Informe quais testes dependem de pendências. |
| **3. Modelar o banco** | Proponha tabelas, campos e chaves para colaboradores, filiais, eventos, folha, memória de cálculo, parâmetros com vigência, férias, documentos e logs. Valores legais ficam em tabela de parâmetros. |
| **4. Implementar uma etapa** | Implemente apenas a Etapa 1 (login, perfis, cadastro), seguindo RN-10 a RN-14 e as user stories US-01 e US-07. Escreva os testes primeiro. Não implemente nada fora da etapa. |
| **5. Conferir o gerado** | Compare o código com a especificação. Liste comportamento que não está na spec, valores fixos no código e regras sem teste. |

---

## 16. Pendências Abertas

| ID | Pendência | Responsável | Impede de começar? |
| :---: | :--- | :--- | :---: |
| **P-01** | Nome da convenção coletiva e seus valores (adicionais, piso, regras de VA e VT) | Grupo de RH | Não. Valem os padrões da CLT até lá |
| **P-02** | Conferência final das tabelas e regras por contador ou especialista | Cliente | Não, mas é necessária antes do uso real |
| **P-03** | Tratamento de afastados na folha (INSS, maternidade etc.) | Grupo de RH | Não na 1ª versão |
| **P-04** | Confirmação dos itens [ADOTADO] (retenção, relatórios, arredondamento, VT, VA, contracheque) | Grupo de RH | Não. São parâmetros configuráveis |

---

## 17. Registro do Levantamento (Ata Resumida)

- **Fatos (informados pelo cliente):** Todas as decisões marcadas `CONFIRMADO` na seção 1. As informações foram passadas por Alana Catiany de Morais, do grupo de RH, em 08/10, e o questionário de confirmação foi respondido pelo grupo em 14/10. Um integrante do GTI 4º período também enviou mensagens para ajudar no levantamento.
- **Conflito resolvido:** O cliente havia informado 20 e 15 colaboradores, e 4 filiais ou matriz + 2 filiais; o RH confirmou 15 colaboradores e matriz + 2 filiais.
- **Decisões do grupo (GTI 4º período):** O sistema calcula a folha; valores legais parametrizados; sem campos de dados sensíveis desnecessários; padrões `[ADOTADO]` onde o cliente não respondeu.
- **Hipóteses:** Tudo marcado `[HIPÓTESE]` neste documento.
- **Fontes dos parâmetros legais:** Tabelas públicas de INSS e IRRF de 2026, consultadas em 13/10/2026.
