# Especificação de Requisitos

**Sistema de RH e Folha de Pagamento**

Cliente: correspondente bancário (15 colaboradores, matriz + 2 filiais)

Elaborado pelo GTI 4º período · Destino: GTI 2º período (desenvolvimento)

Atividade da disciplina: Spec-Driven Development com IA · Prof. Dr. Juan Apolinario

Versão 1.3 · 21/10/2026 (histórico na seção 19)

Repositório do desenvolvimento (GTI 2º período): github.com/Kauzalidade/helloWorld

> **Resumo:** especificação de um sistema web de RH e folha de pagamento para uma empresa correspondente bancária (15 colaboradores, matriz + 2 filiais). O sistema calcula INSS e IRRF de 2026, explica cada valor (memória de cálculo) e controla férias, 13º, documentos e alertas. É verificável: regras numeradas, requisitos não funcionais com números, cenários Gherkin com situações de erro e exemplos de cálculo. Orienta a implementação por agentes de IA (seções 15.1 e 15.3) e registra a revisão feita com IA (seção 15.2).

> **Como ler:** este documento reune, em um só lugar, tudo que foi definido com o cliente (grupo de RH) e as regras adotadas pelo grupo. **[CONFIRMADO]** = informado pelo cliente. **[ADOTADO]** = melhor opção escolhida pelo grupo onde o cliente não respondeu; é configurável e vale até o RH ou o contador pedir mudança. Nenhum item deste documento está bloqueado esperando resposta do cliente. Regra de ouro: se faltar informação, **não inventem a regra**; anotem a dúvida e perguntem ao GTI 4º período.

### Equipe e responsáveis

| Nome | Grupo | Função |
|---|---|---|
| Severino Felipe | GTI 4º período | Líder e ponte com o 2º período |
| Antônio Fabrício | GTI 4º período | Regras de negócio e folha |
| José Roberto | GTI 4º período | Contato com o cliente (RH) e ata |
| Wesley Antônio | GTI 4º período | Testes e qualidade |
| Jonas Kauã | GTI 2º período (desenvolvimento) | Representante da turma e desenvolvedor |
| Carlos Pietro | GTI 2º período (desenvolvimento) | Desenvolvedor |
| José Geremias | GTI 2º período (desenvolvimento) | Desenvolvedor |
| Valdir Fonséca | GTI 2º período (desenvolvimento) | Desenvolvedor |
| Vitor | Grupo de RH (cliente) | Diretor de Recursos Humanos: coordena a equipe, acompanha resultados e supervisiona as atividades |
| Deyse | Grupo de RH (cliente) | Analista de Departamento Pessoal: folha, férias, 13º, benefícios e documentos |
| Alana Catiany de Morais | Grupo de RH (cliente) | Analista de Recrutamento e Seleção. Passou as informações ao GTI |
| Marília | Grupo de RH (cliente) | Analista de Treinamento e Desenvolvimento |
| Thayane | Grupo de RH (cliente) | Analista de Gestão e Relatórios: organiza dados, controla planilhas e elabora relatórios |

## 1. Problema, objetivos, público-alvo e decisões do cliente

### 1.1 Problema

Uma empresa correspondente bancária, com **15 colaboradores** em **1 matriz e 2 filiais**, precisa organizar e calcular a folha de pagamento (salário, horas extras, férias, 13º, benefícios e descontos), com acesso restrito a **RH e diretoria**, backup diário e primeira entrega em 15 dias. Hoje o trabalho depende de planilhas e conferência manual. Em folha, **um centavo errado** vira reclamação e retrabalho, e é preciso **explicar de onde saiu cada valor**. O sistema **calcula** a folha (decisão do grupo).

### 1.2 Objetivos

| ID | Objetivo | Como medir |
|---|---|---|
| OB-01 | Calcular a folha mensal de todos os colaboradores com INSS e IRRF corretos | Resultados iguais aos exemplos da seção 8 (tolerância de R$ 0,01) |
| OB-02 | Tornar cada valor explicável (memória de cálculo) | 100% dos valores com base, regra e parâmetro registrados |
| OB-03 | Controlar férias e 13º sem perder prazos | Alertas de férias a vencer; cálculo conforme RN-40 a RN-46 |
| OB-04 | Guardar documentos com alertas de vencimento | Alerta gerado 30 dias antes (configurável) |
| OB-05 | Proteger dados pessoais conforme a LGPD | Acesso restrito, log de acessos e nenhum dado sensível desnecessário |
| OB-06 | Permitir que a regra mude sem reprogramar | Parâmetros legais com vigência, cadastráveis |

### 1.3 Público-alvo e limites

| Perfil | Quem é | Uso principal |
|---|---|---|
| RH | Analistas de Departamento Pessoal e equipe de RH | Cadastrar, lançar eventos, calcular, conferir, fechar e aprovar a folha |
| Diretoria | Diretor de RH e demais diretores | Acompanhar resultados e consultar relatórios |
| Admin do sistema | Responsável técnico | Gerenciar usuários e consultar logs |

Colaboradores e gestores **não** acessam o sistema nesta versão. O que entra e o que fica de fora da 1ª versão está na seção 2.

> **Diretriz para o desenvolvimento:** o grupo do GTI 2º período deve atualizar o README.md do repositório (github.com/Kauzalidade/helloWorld) para referenciar e seguir esta versão 1.3, implementando as regras oficiais de DSR (RN-31), reflexos de horas extras (RN-32 e RN-48) e 13º salário (RN-46 e RN-48).

### 1.4 Decisões do cliente

| Tema | Decisão | Status |
|---|---|---|
| Colaboradores | 15, todos CLT. Sem estagiários, PJ ou aprendizes na 1ª versão | CONFIRMADO |
| Estrutura | 1 matriz + 2 filiais (filial é cadastro, não fixa no código) | CONFIRMADO |
| Jornada | 44 horas semanais (divisor 220 horas/mês) | CONFIRMADO |
| Horas extras | 50% em dia útil; 100% em domingo e feriado, conforme legislação e convenção | CONFIRMADO |
| Banco de horas | Não será usado. Horas extras sempre pagas | CONFIRMADO |
| Ponto | Sem registro eletrônico. O RH lança horas extras e faltas por mês | CONFIRMADO |
| Pagamento | Transferência bancária, até o 5º dia útil do mês seguinte. Arquivo bancário fica para depois; a 1ª versão gera dados e relatórios de pagamento | CONFIRMADO |
| Fechamento | O RH confere, fecha e aprova a folha. A diretoria acompanha e consulta relatórios | CONFIRMADO |
| Benefícios | Vale-transporte e vale-alimentação; outros no futuro | CONFIRMADO |
| Férias e 13º | 30 dias com 1/3; 13º em duas parcelas (até 30/11 e 20/12) | CONFIRMADO |
| Rescisão | Segunda etapa | CONFIRMADO |
| Documentos | CPF, documento de identificação, contrato, comprovante de residência, dados bancários, documentos admissionais e atestados | CONFIRMADO |
| Alertas | Documentos com validade, exames ocupacionais periódicos e outros prazos administrativos | CONFIRMADO |
| Acesso | Só RH e diretoria, com permissões por função | CONFIRMADO |
| Dados sensíveis | NÃO armazenar religião, sexualidade, raça, dados genéticos ou biomédicos sem finalidade legítima e específica. O sistema não terá esses campos | CONFIRMADO |
| Convenção coletiva | Existe uma convenção aplicável; nome e valores não informados. Premissa: valem os padrões da CLT e a convenção entra como parâmetro cadastrável (cenários na seção 10) | ADOTADO |

## 2. Limites, escopo e etapas de construção

| Etapa | O que construir | Pronto quando |
|---|---|---|
| 1 | Login, perfis (RH e diretoria), cadastro de filiais e colaboradores, parâmetros legais e feriados | Cadastra, edita, consulta e inativa; CPF duplicado é rejeitado |
| 2 | Lançamento de eventos: horas extras, faltas, atestados, VT, VA e verbas avulsas | Cenários de horas extras e descontos passam. A tela de lançamentos, com o campo de verbas avulsas (RN-25), precisa estar pronta antes do cálculo da Etapa 3 |
| 3 | Cálculo da folha, memória de cálculo e fechamento (só começa com a Etapa 2 completa, incluindo verbas avulsas) | Folha calculada com memória; fechamento bloqueado nos casos da tabela 7.1 |
| 4 | Férias, 13º, documentos com alerta, contracheque e relatórios | Cenários de férias passam; relatórios exportam em PDF e Excel |

**Fora da 1ª versão:** ponto eletrônico, banco de horas, rescisão, arquivo bancário, recrutamento, desempenho e treinamentos, portal do colaborador, integrações (eSocial, Microsoft 365, Google). Também ficam de fora, como cálculo automático: adicional noturno, insalubridade, periculosidade, comissões, salário-família, pensão alimentícia, consignado e assistência médica. O RH registra esses casos como **verbas avulsas** (RN-25).

**Sugestão técnica:** sistema web com banco relacional (PostgreSQL ou MySQL). Dinheiro sempre em tipo decimal, nunca ponto flutuante. Parâmetros legais em tabela do banco, com data de início e fim de vigência.

### 2.1 Modelo de dados conceitual

Entidades que o desenvolvimento deve criar (campos mínimos; detalhes nas seções 5 a 7).

| Entidade | Campos principais | Relações |
|---|---|---|
| Usuário | e-mail, senha (hash), perfil (RH, Diretoria, Admin), ativo | Gera Logs |
| Filial | nome, tipo (matriz ou filial), ativa | 1 Filial tem N Colaboradores |
| Colaborador | nome, CPF, nascimento, admissão, desligamento, cargo, setor, salário-base, jornada, dados bancários, dependentes, situação | Pertence a 1 Filial; tem N Eventos, Documentos, Férias e Históricos |
| Competência | mês/ano, situação (aberta ou fechada) | Tem N Folhas |
| Evento | tipo (hora extra, falta, atestado, VT, VA, verba avulsa), quantidade, data, observação, anexo | Pertence a 1 Colaborador e 1 Competência |
| Parâmetro | nome, valor, início e fim da vigência | Usado pelo cálculo |
| Folha e Verba | Folha: colaborador, competência, proventos, descontos, líquido, FGTS. Verba: tipo, valor, base, regra, parâmetro (e versão), arredondamento | Folha tem N Verbas; a Verba é a memória de cálculo |
| Férias | período aquisitivo e concessivo, dias, abono, situação (pendente, aprovada, recusada) | Pertence a 1 Colaborador |
| Documento e Alerta | Documento: tipo, arquivo, validade, anexado por. Alerta: tipo, referência, data prevista, situação | Alerta nasce de Documento, Férias ou Afastamento |
| Saldo a descontar | colaborador, competência de origem, valor original, valor restante, situação | Pertence a 1 Colaborador; vira desconto na competência seguinte |
| Histórico e Log | campo alterado, valor anterior e novo, data, usuário. Log é imutável | Histórico pertence a 1 Colaborador |

## 3. Glossário

| Termo | Definição |
|---|---|
| Competência | Mês/ano de referência da folha (ex.: 10/2026) |
| Evento | Lançamento que gera provento ou desconto (hora extra, falta, VT, VA) |
| Provento / Desconto | Valor recebido / valor retirado do colaborador |
| Base de cálculo | Conjunto de valores usados para calcular um provento ou desconto |
| Memória de cálculo | Registro passo a passo de como cada valor foi calculado |
| Fechamento | Trava da competência após conferência do RH; depois disso não se altera sem reabertura justificada |
| Período aquisitivo / concessivo | 12 meses que dão direito às férias / 12 meses seguintes para concedê-las |
| Abono pecuniário | Venda de até 1/3 das férias |
| DSR | Descanso semanal remunerado |
| Saldo a descontar | Parte dos descontos que não coube no líquido e é descontada nos meses seguintes, dentro do limite |
| Reflexo | Efeito de uma verba variável (como a média das horas extras) no cálculo de férias e 13º |
| Verba avulsa | Provento ou desconto lançado manualmente pelo RH, com marcação de incidência em INSS, IRRF e FGTS |
| Dia útil para o DSR | Dias do mês menos domingos e feriados (o sábado conta como dia útil) |
| Situação da competência | Aberta, calculada ou fechada (tabela 7.5) |
| Parâmetro | Valor que muda com o tempo (tabelas, percentuais) e não pode ficar fixo no código |

## 4. Perfis e permissões

| Ação | RH | Diretoria | Admin do sistema |
|---|---|---|---|
| Cadastrar/editar colaborador e filial | Sim | Não | Não |
| Consultar dados cadastrais | Sim | Sim | Não |
| Lançar eventos e calcular folha | Sim | Não | Não |
| Conferir, fechar e aprovar folha | Sim | Não | Não |
| Reabrir competência fechada | Sim, com justificativa obrigatória [ADOTADO] | Não (é notificada e consulta o log) | Não |
| Consultar folha e relatórios | Sim | Sim | Não |
| Cadastrar parâmetros, feriados e verbas avulsas | Sim | Não | Não |
| Ver dados de saúde (atestados, exames) | Sim | Não [ADOTADO] | Não |
| Ver log de acessos e alterações | Não | Sim | Sim |
| Gerenciar usuários | Não | Não | Sim |

## 5. Regras de negócio

### 5.1 Regras gerais

- **RN-01 Parametrização:** nenhum valor legal ou percentual fixo no código. Cada parâmetro tem nome, valor, início e fim de vigência. O cálculo usa o parâmetro vigente na competência.
- **RN-02 Memória de cálculo:** cada valor registra base, regra aplicada, parâmetro (e versão) e arredondamento.
- **RN-03 Arredondamento [ADOTADO]:** 2 casas decimais, meio para cima, aplicado em cada verba antes de somar. Regra configurável.
- **RN-04 Fechamento:** competência fechada não aceita alteração. Reabrir exige justificativa obrigatória; o RH reabre por conta própria, sem aguardar a Diretoria. O sistema homologa na hora, grava um evento destacado no Log de Auditoria imutável (justificativa, usuário, data e hora) e notifica a Diretoria para fiscalização [ADOTADO].
- **RN-05 Dado obrigatório ausente:** bloqueia o fechamento e indica o campo pendente.
- **RN-06 Descontos acima dos proventos [ADOTADO]:** o líquido nunca fica negativo e o sistema não cria provento artificial. INSS e IRRF nunca são limitados; os demais descontos (VT, avulsos e saldo anterior, nessa ordem) são limitados ao que sobrar dos proventos, deixando o líquido em 0,00. O excedente vira **saldo a descontar** do colaborador. O fechamento exige justificativa do RH. Na competência seguinte, o saldo entra como desconto "Saldo a descontar - mês anterior", limitado a 30% do bruto (parâmetro, RN-01); o que sobrar segue para o mês seguinte até quitar.
- **RN-07 Histórico:** mudanças de salário, cargo, setor, filial e situação geram registro com data, valor anterior e novo valor.
- **RN-08 Ciclo da competência [ADOTADO]:** aberta, calculada e fechada (tabela 7.5). Pode recalcular enquanto não estiver fechada; só fecha se estiver calculada e sem pendência.

### 5.2 Cadastro

- **RN-10** Dados mínimos [ADOTADO]: nome, CPF, nascimento, admissão, cargo, setor, filial, salário-base, jornada, dados bancários, dependentes (para IRRF).
- **RN-11** CPF único e válido. Duplicado é rejeitado.
- **RN-12** Colaborador não é excluído, apenas inativado.
- **RN-13** Um colaborador pertence a uma filial por vez; transferência registra data e histórico.
- **RN-14 Dados proibidos:** o cadastro não terá campos de religião, orientação sexual, raça/etnia, dados genéticos ou biomédicos. Qualquer inclusão futura exige finalidade e base legal registradas.
- **RN-15 Validações [ADOTADO]:** CPF com 11 dígitos e dígitos verificadores corretos; nome com pelo menos 3 caracteres; salário-base maior que zero; data de desligamento não anterior à admissão; e-mail em formato válido; agência e conta só com números. Campo obrigatório vazio rejeita o cadastro e indica o campo.
- **RN-16 Dependentes [ADOTADO]:** cada dependente informado (nome, nascimento, parentesco) gera a dedução mensal do parâmetro (R$ 189,59) no IRRF. O sistema não confere os requisitos legais do dependente; a responsabilidade é do RH.

### 5.3 Cálculo mensal

- **RN-20** A folha considera colaboradores ativos no período; admitidos ou desligados no mês recebem proporcional aos dias trabalhados (salário-base / 30 x dias) [ADOTADO].
- **RN-21 Ordem:** (1) salário e proventos, (2) base do INSS, (3) INSS, (4) base do IRRF, (5) IRRF, (6) demais descontos, (7) líquido. Líquido = proventos menos descontos.
- **RN-22 INSS:** base = salário-base + horas extras + DSR + demais proventos que incidem. Cálculo progressivo por faixa (seção 6.2), limitado ao teto.
- **RN-23 IRRF:** o sistema calcula duas bases e usa a que gerar menor imposto: (a) tradicional = proventos tributáveis menos INSS menos (dependentes x 189,59); (b) simplificada = proventos tributáveis menos 607,20. Imposto = base x alíquota menos parcela a deduzir; depois aplica a redução da seção 6.3; mínimo 0,00. Registrar na memória qual base foi usada.
- **RN-24 FGTS:** 8% sobre a remuneração, mostrado como encargo da empresa, não como desconto do colaborador.
- **RN-25 Verbas avulsas [ADOTADO]:** o RH lança provento ou desconto avulso com descrição, valor e três marcações (incide em INSS, IRRF e FGTS). Só entra em competência aberta e aparece na memória de cálculo.
- **RN-26 Incidências:** INSS, IRRF e FGTS seguem a tabela 7.4.
- **RN-27 Aviso nos parâmetros:** a tela de parâmetros legais exibe, em destaque e sempre visível, o aviso de que alterar alíquotas e bases legais sem validação do contador pode gerar cálculos incorretos e passivos jurídicos. Alterações de parâmetro entram no Log de Auditoria.

### 5.4 Horas extras, DSR e faltas

- **RN-30** Valor da hora = salário-base dividido por 220. Dia útil: hora x 1,5. Domingo e feriado: hora x 2,0. Adicionais são parâmetros (convenção pode alterar).
- **RN-31 DSR sobre horas extras:** (total de horas extras do mês / dias úteis do mês) x domingos e feriados do mês. Integra a base de INSS e IRRF.
- **RN-32 Reflexos:** a média das horas extras do período reflete em férias e 13º.
- **RN-33 Faltas:** desconto = (salário-base / 30) x dias de falta injustificada, mais perda do DSR da semana. Atestado médico válido não desconta. Atestados exigem anexo e período.
- **RN-34 Afastamentos** (INSS, maternidade, paternidade, acidente): data de início, fim previsto e tipo; alerta ao RH perto do término. Tratamento na folha [ADOTADO]: doença e acidente, os 15 primeiros dias são pagos normalmente pela empresa e a partir do 16º dia o salário fica suspenso na folha (benefício pago pelo INSS); maternidade e paternidade mantêm o salário integral. A compensação junto ao INSS fica fora da 1ª versão.
- **RN-35 Calendário de feriados [ADOTADO]:** tabela cadastrável pelo RH, usada no DSR e nas horas extras de 100%. Carga inicial com os 10 feriados nacionais de 2026 (Portaria MGI 11.460/2025): 01/01, 03/04, 21/04, 01/05, 07/09, 12/10, 02/11, 15/11, 20/11 e 25/12. Pontos facultativos não são feriados, salvo se o RH cadastrar. Feriados estaduais e municipais são cadastrados pelo RH. Dia útil para o DSR = dias do mês menos domingos e feriados.

### 5.5 Férias e 13º

- **RN-40** Período aquisitivo de 12 meses a partir da admissão; depois, concessivo de 12 meses.
- **RN-41** 30 dias corridos mais 1/3 constitucional sobre a remuneração (salário-base + média de variáveis).
- **RN-42** Fracionamento em até 3 períodos: um com no mínimo 14 dias e os demais com no mínimo 5 dias [ADOTADO, conforme CLT].
- **RN-43** Abono pecuniário: até 1/3 dos dias pode virar dinheiro, sem incidência de INSS e IRRF sobre o abono. INSS e IRRF incidem sobre as férias gozadas.
- **RN-44** Faltas injustificadas no aquisitivo reduzem os dias de direito [ADOTADO, parâmetro]: até 5 faltas, 30 dias; de 6 a 14, 24 dias; de 15 a 23, 18 dias; de 24 a 32, 12 dias; acima de 32, perde o direito.
- **RN-45** Alerta ao RH quando o concessivo estiver perto do fim (sugestão: 60 dias). Pedido de férias antes de completar o aquisitivo é rejeitado.
- **RN-46 13º:** 1/12 por mês com 15 dias ou mais trabalhados. 1ª parcela = 50% do salário (mais média proporcional), sem descontos, até 30/11. 2ª parcela (até 20/12) = 13º integral menos 1ª parcela, INSS e IRRF calculados sobre o 13º à parte.
- **RN-47 Início e pagamento das férias:** o gozo não pode começar nos 2 dias que antecedem feriado ou dia de descanso semanal (CLT, art. 134). O pagamento das férias é feito até 2 dias antes do início (CLT, art. 145); o sistema mostra a data limite.
- **RN-48 Média de variáveis [ADOTADO]:** a média mensal das horas extras (e do DSR delas) é a soma paga no período aquisitivo (férias) ou no ano (13º) dividida por 12. Entra na base de férias, do 1/3 e do 13º.
- **RN-49 Férias que cruzam dois meses [ADOTADO]:** as férias (valor e 1/3) são calculadas na competência do início do gozo, com INSS e IRRF somados ao salário daquele mês (RN-26). Em cada mês, o salário paga só os dias não gozados. Confirmar a regra com o contador.

### 5.6 Benefícios, documentos e dados

- **RN-50 Vale-transporte [ADOTADO]:** só para quem optar. Desconto = menor valor entre 6% do salário-base e o custo mensal do VT informado pelo RH.
- **RN-51 Vale-alimentação [ADOTADO]:** valor mensal fixo por colaborador (parâmetro). Coparticipação padrão 0%, configurável.
- **RN-52 Documentos:** anexos por colaborador com tipo, validade (quando houver) e quem anexou. Alerta de vencimento com antecedência configurável (sugestão 30 dias). Documento sem validade não gera alerta.
- **RN-53 Exames ocupacionais:** cadastrar data do último exame e periodicidade; alertar o RH antes do vencimento.
- **RN-54 Saúde:** atestados e exames são dados de saúde, com acesso restrito e log de cada consulta.
- **RN-55 Contracheque [ADOTADO]:** PDF gerado pelo RH por colaborador e competência, com proventos, descontos, líquido e memória resumida. Não há portal para o colaborador.
- **RN-56 Retenção [ADOTADO]:** dados e documentos guardados durante o vínculo e por 5 anos após o desligamento; depois, eliminar ou anonimizar (LGPD). O sistema sinaliza os dados vencidos; a eliminação exige confirmação do RH e fica em log.
- **RN-57 Dados de pagamento:** relatório com colaborador, líquido, dados bancários e competência.
- **RN-58 Prazo de pagamento [CONFIRMADO]:** a folha é paga até o 5º dia útil do mês seguinte. O sistema alerta o RH no 3º dia útil se a competência ainda não estiver fechada [ADOTADO].

## 6. Parâmetros legais de 2026

> Valores conferidos em 13/10/2026 em fontes públicas (Portaria Interministerial MPS/MF 13/2026 para o INSS; Lei 15.270/2025 e tabela da Receita Federal para o IRRF). Todos entram no sistema como **parâmetros com vigência**. O contador do cliente deve confirmar antes do uso real.

### 6.1 Parâmetros gerais

| Parâmetro | Valor |
|---|---|
| Salário mínimo | R$ 1.621,00 |
| Teto do INSS | R$ 8.475,55 (contribuição máxima R$ 988,09) |
| Dedução por dependente (IRRF) | R$ 189,59 por mês |
| Desconto simplificado (IRRF) | R$ 607,20 por mês |
| FGTS (encargo da empresa) | 8% |
| Divisor de horas mensais | 220 |

### 6.2 INSS 2026 (empregado, cálculo progressivo por faixa)

| Faixa | Salário de contribuição | Alíquota |
|---|---|---|
| 1 | Até R$ 1.621,00 | 7,5% |
| 2 | De R$ 1.621,01 a R$ 2.902,84 | 9% |
| 3 | De R$ 2.902,85 a R$ 4.354,27 | 12% |
| 4 | De R$ 4.354,28 até R$ 8.475,55 | 14% |

Cada alíquota incide apenas sobre a parte do salário dentro da faixa; somam-se os valores. Acima do teto usa-se o teto. O cálculo por faixa pode diferir em até R$ 0,01 de calculadoras que usam parcela a deduzir; os testes aceitam essa tolerância.

### 6.3 IRRF 2026 (mensal)

| Base de cálculo mensal | Alíquota | Parcela a deduzir |
|---|---|---|
| Até R$ 2.428,80 | Isento | - |
| De R$ 2.428,81 a R$ 2.826,65 | 7,5% | R$ 182,16 |
| De R$ 2.826,66 a R$ 3.751,05 | 15% | R$ 394,16 |
| De R$ 3.751,06 a R$ 4.664,68 | 22,5% | R$ 675,49 |
| Acima de R$ 4.664,68 | 27,5% | R$ 908,73 |

**Redução da Lei 15.270/2025:** rendimento tributável mensal até R$ 5.000,00 tem redução de até R$ 312,89, que zera o imposto. De R$ 5.000,01 a R$ 7.350,00: redução = R$ 978,62 menos (0,133145 x rendimento mensal), nunca negativa nem maior que o imposto apurado. Acima de R$ 7.350,00: sem redução.

## 7. Tabelas de decisão

### 7.1 Fechamento da folha

| Situação | Dado obrigatório | Líquido | Ação do sistema |
|---|---|---|---|
| Normal | Completo | Maior ou igual a 0 | Permite fechar e exibe memória de cálculo |
| Dado ausente | Faltando | - | Bloqueia e mostra o campo pendente |
| Descontos acima dos proventos | Completo | Líquido calculado menor que 0 | Limita os descontos (líquido 0,00), cria saldo a descontar e exige justificativa para fechar |
| Saldo a descontar justificado | Completo | Saldo maior que 0 | Permite fechar, registra a justificativa e lança o saldo como desconto na competência seguinte (limite de 30% do bruto) |

### 7.2 Pedido de férias

| Aquisitivo completo | Dentro do concessivo | Fracionamento válido | Ação |
|---|---|---|---|
| Sim | Sim | Sim | Enviar para aprovação |
| Não | - | - | Rejeitar: ainda sem direito |
| Sim | Não (vencido) | - | Alertar RH; aprovar só com justificativa |
| Sim | Sim | Não | Rejeitar informando o motivo |

### 7.3 Horas extras

| Dia | Adicional | Observação |
|---|---|---|
| Dia útil | 50% (parâmetro) | Mínimo legal |
| Domingo ou feriado | 100% (parâmetro) | Conforme cliente e convenção |

### 7.4 Incidência por verba (INSS, IRRF e FGTS)

| Verba | INSS | IRRF | FGTS (8%) |
|---|---|---|---|
| Salário-base e proporcional | Sim | Sim | Sim |
| Horas extras e DSR sobre horas extras | Sim | Sim | Sim |
| Falta injustificada e DSR perdido | Reduzem a base | Reduzem a base | Reduzem a base |
| Atestado médico válido | Não reduz | Não reduz | Não reduz |
| Férias gozadas e 1/3 | Sim | Sim | Sim |
| Abono pecuniário (venda de férias) e 1/3 | Não | Não | Não |
| 13º salário | Só na 2ª parcela, sobre o total | Só na 2ª parcela, à parte | Sim, sobre cada parcela |
| VT e VA fornecidos pela empresa [ADOTADO] | Não | Não | Não |
| Verba avulsa | Conforme marcação do RH | Conforme marcação do RH | Conforme marcação do RH |

### 7.5 Ciclo de vida da competência

| Situação | Como entra | O que pode fazer | Como sai |
|---|---|---|---|
| Aberta | RH cria a competência ou ao fechar a anterior | Lançar eventos e verbas avulsas, calcular e recalcular | Calcular leva a Calculada |
| Calculada | Depois de Calcular | Ver memória de cálculo, recalcular, fechar se não houver pendência | Fechar leva a Fechada; alterar evento volta a Aberta |
| Fechada | RH fecha a folha | Consultar, gerar contracheque e relatórios; nada se altera | Reabertura pelo RH, com justificativa obrigatória, leva a Aberta; a Diretoria é notificada |

## 8. Exemplos numéricos para os testes

- **A. Salário R$ 3.000,00, sem dependentes.** INSS: 121,575 + 115,3656 + (97,16 x 12% = 11,6592) = **R$ 248,60**. IRRF: base simplificada 2.392,80 cai na faixa isenta = **R$ 0,00**. Líquido: **R$ 2.751,40**.
- **B. Salário R$ 6.000,00, sem dependentes.** INSS: 121,575 + 115,3656 + 174,1716 + (1.645,73 x 14% = 230,4022) = **R$ 641,51** (tolerância R$ 0,01). IRRF tradicional: base 5.358,49 x 27,5% menos 908,73 = 564,85; simplificado: 574,29; usa o menor. Redução: 978,62 menos (0,133145 x 6.000) = 179,75. IRRF final: **R$ 385,10**. Líquido: **R$ 4.973,39**.
- **C. Acima do teto (R$ 10.000,00).** INSS limitado ao teto: **R$ 988,09**.
- **D. Horas extras.** Salário 2.200,00 / 220 = 10,00 por hora. 2 horas em dia útil = **R$ 30,00**. 2 horas em domingo = **R$ 40,00**.
- **E. Férias.** Salário 3.000,00 com 30 dias: férias 3.000,00 + 1/3 de 1.000,00 = **R$ 4.000,00** brutos.
- **F. Vale-transporte.** Salário 2.000,00: custo 180,00 gera desconto de **R$ 120,00** (6%); custo 90,00 gera desconto de **R$ 90,00** (limitado ao custo).
- **G. DSR e folha completa (competência 10/2026).** Calendário: 31 dias, 4 domingos e 1 feriado (12/10), logo 26 dias úteis e 5 domingos e feriados. Salário 2.200,00 (hora 10,00); 10 horas extras em dia útil = 10 x 15,00 = **R$ 150,00**. DSR = 150,00 / 26 x 5 = **R$ 28,85**. Bruto: 2.378,85. INSS: 121,575 + (757,85 x 9% = 68,2065) = **R$ 189,78**. IRRF: **R$ 0,00** (base abaixo de 2.428,80). Líquido: **R$ 2.189,07**.
- **H. IRRF com dependentes.** Salário 5.500,00 com 2 dependentes. INSS: **R$ 571,51**. Base tradicional: 5.500,00 menos 571,51 menos 379,18 = 4.549,31 (imposto 348,10); simplificada: 4.892,80 (imposto 436,79); usa o menor. Redução: 978,62 menos (0,133145 x 5.500) = 246,32. IRRF final: **R$ 101,78**. Líquido: **R$ 4.826,71**.
- **I. IRRF isento e FGTS.** Salário 2.000,00: INSS **R$ 155,69**, IRRF **R$ 0,00**, líquido **R$ 1.844,31**. FGTS sobre 3.000,00 = **R$ 240,00** (encargo da empresa, não reduz o líquido).
- **J. Férias com INSS e IRRF.** Salário 3.000,00, 30 dias gozados: base 4.000,00. INSS: 121,575 + 115,3656 + 131,6592 = **R$ 368,60**. IRRF: tradicional 150,55; simplificado 114,76; usa 114,76; a redução (até 312,89) zera: **R$ 0,00**. Líquido das férias: **R$ 3.631,40**.
- **K. Reflexo das horas extras.** Salário 2.200,00 e horas extras (com DSR) de 1.800,00 no período: média mensal = 1.800,00 / 12 = 150,00. Base de férias e 13º = **R$ 2.350,00**. Férias: 1/3 = 783,33; total **R$ 3.133,33**. 13º: 1ª parcela = **R$ 1.175,00** (sem descontos). 2ª parcela: INSS sobre 2.350,00 = 187,19; IRRF 0,00; **2.350,00 menos 1.175,00 menos 187,19 = R$ 987,81**.
- **L. 13º proporcional, admissão, desligamento e afastamento.** Admitido em 20/08/2026 com salário 3.000,00: agosto tem 12 dias e não conta; setembro a dezembro dão 4/12, logo 13º de **R$ 1.000,00**. Admissão no dia 16 de mês de 30 dias: **R$ 1.500,00**. Desligamento no dia 10: **R$ 1.000,00**. Afastamento pelo INSS a partir do dia 10: 9 dias trabalhados mais 15 pagos pela empresa = 24 dias = **R$ 2.400,00**.
- **M. Feriado municipal.** No exemplo G, se o RH cadastrar mais um feriado municipal em 10/2026: 25 dias úteis e 6 domingos e feriados; DSR = 150,00 / 25 x 6 = **R$ 36,00**.
- **N. Datas de férias.** Início em 05/09/2026 (sábado, 2 dias antes do feriado de 07/09): rejeitado. Início em 10/11/2026: pagamento até **08/11/2026**.

## 9. User stories

| ID | História | Critérios de aceite |
|---|---|---|
| US-01 | Como analista de RH, quero cadastrar e inativar colaboradores para manter a base atualizada. | CPF novo e válido cria o colaborador. CPF repetido é rejeitado. Desligado é inativado, nunca excluído. |
| US-02 | Como analista de RH, quero lançar horas extras, faltas, atestados, VT e VA para entrarem na folha. | Evento fica salvo com usuário e data. Competência fechada rejeita lançamento. |
| US-03 | Como analista de RH, quero ver a memória de cálculo para explicar o pagamento. | Mostra base, regra, valor e arredondamento; registra usuário, data e versão dos parâmetros. |
| US-04 | Como analista de RH, quero fechar a folha só com dados completos. | Dado ausente bloqueia e indica o campo. Desconto acima dos proventos gera saldo a descontar e exige justificativa. |
| US-05 | Como analista de RH, quero controlar saldo e pedidos de férias. | Aquisitivo incompleto rejeita. Concessivo perto do fim gera alerta. |
| US-06 | Como analista de RH, quero anexar documentos com validade e receber alertas. | Documento com validade em 30 dias gera alerta. Exame ocupacional próximo gera alerta. |
| US-07 | Como diretor, quero saber quem acessou ou alterou cada informação. | Registra usuário, data, hora e valores antes e depois. |
| US-08 | Como diretor, quero relatórios em PDF ou Excel. | Arquivo gerado com os mesmos valores da tela. |
| US-09 | Como analista de RH, quero gerar o contracheque em PDF. | PDF com proventos, descontos e líquido por competência. |
| US-10 | Como analista de RH, quero lançar verbas avulsas para tratar casos que o sistema não calcula. | Exige descrição, valor e marcações de INSS, IRRF e FGTS; só entra em competência aberta; aparece na memória de cálculo. |
| US-11 | Como analista de RH, quero cadastrar feriados e parâmetros com vigência para a folha seguir o calendário e a lei. | Parâmetro sem vigência é rejeitado; feriado cadastrado muda o DSR. |
| US-12 | Como Admin, quero gerenciar usuários e perfis. | Cria, inativa e redefine senha com log; o Admin não vê dados da folha. |

## 10. Cenários de aceite (Gherkin)

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

  Cenario: Descontos acima dos proventos
    Dado um colaborador com salario-base 2.000,00, INSS 155,69 e IRRF 0,00
    E um desconto avulso de 2.500,00
    Quando o RH calcular a folha
    Entao o desconto avulso aplicado deve ser 1.844,31 e o liquido 0,00
    E o sistema nao cria provento artificial
    E registra saldo a descontar de 655,69

  Cenario: Fechar com saldo a descontar sem justificativa
    Dado uma folha com saldo a descontar de 655,69
    Quando o RH tentar fechar a competencia sem justificativa
    Entao o sistema bloqueia e pede a justificativa

  Cenario: Saldo a descontar na competencia seguinte
    Dado um saldo a descontar de 655,69 e bruto de 2.000,00 com limite de 30%
    Quando a folha da competencia seguinte for calculada
    Entao o desconto "Saldo a descontar - mes anterior" deve ser 600,00
    E o saldo restante de 55,69 segue para a competencia seguinte

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

  Cenario: Login valido
    Dado um usuario RH cadastrado e ativo
    Quando ele informar e-mail e senha corretos
    Entao o sistema abre a tela inicial

  Cenario: Senha incorreta
    Dado um usuario RH cadastrado
    Quando ele informar uma senha incorreta
    Entao o sistema recusa o acesso
    E exibe "E-mail ou senha invalidos" sem dizer qual dos dois errou

  Cenario: Acesso sem login
    Dado um visitante sem sessao ativa
    Quando ele tentar abrir a folha do mes
    Entao o sistema redireciona para a tela de login

  Cenario: Sessao expirada
    Dado um usuario logado sem atividade por mais de 30 minutos
    Quando ele tentar qualquer acao
    Entao o sistema exige novo login

  Cenario: Diretoria nao fecha a folha
    Dado um usuario com perfil Diretoria
    Quando ele tentar fechar uma competencia
    Entao o sistema nega a acao e registra a tentativa no log

  Cenario: Diretoria nao ve dados de saude
    Dado um usuario com perfil Diretoria
    Quando ele tentar abrir o atestado de um colaborador
    Entao o sistema nega o acesso e registra a tentativa no log

  Cenario: CPF duplicado
    Dado um colaborador cadastrado com um CPF
    Quando o RH cadastrar outro colaborador com o mesmo CPF
    Entao o sistema rejeita e informa que o CPF ja existe

  Cenario: Salario zero ou negativo
    Quando o RH cadastrar um colaborador com salario-base 0,00
    Entao o sistema rejeita e indica o campo salario-base

  Cenario: Cadastro sem dados sensiveis
    Quando o RH abrir o cadastro de um colaborador
    Entao nao deve existir campo de religiao, orientacao sexual, raca, dados geneticos ou biomedicos

  Cenario: Admissao no meio do mes
    Dado um colaborador com salario-base 3.000,00 admitido no dia 16 de um mes de 30 dias
    Quando a folha desse mes for calculada
    Entao o salario proporcional deve ser 1.500,00 (15 dias)

  Cenario: Falta injustificada com perda do DSR
    Dado um colaborador com salario-base 3.000,00 e 1 falta injustificada no mes
    Quando a folha for calculada
    Entao o desconto da falta deve ser 100,00 e o desconto do DSR deve ser 100,00

  Cenario: Reabertura de competencia pelo RH
    Dado uma competencia fechada e a diretoria sem acesso ao sistema
    Quando o RH reabrir a competencia informando a justificativa
    Entao a competencia fica aberta na hora, sem aguardar aprovacao
    E o Log de Auditoria registra um evento destacado com justificativa, usuario, data e hora
    E a Diretoria recebe uma notificacao da reabertura

  Cenario: Diretoria nao reabre competencia
    Dado um usuario com perfil Diretoria
    Quando ele tentar reabrir uma competencia fechada
    Entao o sistema nega a acao e registra a tentativa no log

  Cenario: Reabertura sem justificativa
    Dado uma competencia fechada
    Quando o RH solicitar a reabertura sem justificativa
    Entao o sistema rejeita e pede a justificativa

  Cenario: Ferias que cruzam dois meses
    Dado um colaborador com salario-base 3.000,00 e 30 dias de ferias
    E as ferias iniciando no dia 20 de um mes de 30 dias
    Quando a folha desse mes e a do mes seguinte forem calculadas
    Entao o salario do mes do inicio deve ser 1.900,00 (19 dias trabalhados)
    E o salario do mes seguinte deve ser 1.100,00 (11 dias trabalhados)
    E as ferias de 4.000,00 sao calculadas na competencia do inicio do gozo

  Cenario: Admissao e desligamento no mesmo mes
    Dado um colaborador com salario-base 3.000,00 admitido no dia 5
    E desligado no dia 20 de um mes de 30 dias
    Quando a folha desse mes for calculada
    Entao o salario proporcional deve ser 1.600,00 (16 dias)

  Cenario: Aviso na tela de parametros
    Quando o RH abrir a tela de parametros e feriados
    Entao o sistema exibe em destaque o aviso sobre validacao do contador
    E o aviso diz que alterar aliquotas e bases legais sem validacao gera risco
    E cada alteracao de parametro fica registrada no Log de Auditoria

  Cenario: Parametro sem vigencia
    Quando o RH cadastrar um parametro sem data de inicio
    Entao o sistema rejeita e indica o campo de vigencia

  Cenario: Fracionamento de ferias invalido
    Dado um colaborador com direito a 30 dias
    Quando pedir 3 periodos de 10 dias
    Entao o sistema rejeita informando que um periodo deve ter no minimo 14 dias

  Cenario: Fracionamento de ferias valido
    Dado um colaborador com direito a 30 dias
    Quando pedir periodos de 14, 8 e 8 dias
    Entao o sistema envia o pedido para aprovacao

  Cenario: Abono pecuniario
    Dado um colaborador com salario-base 3.000,00 e 30 dias de direito
    Quando vender 10 dias de ferias
    Entao o abono deve ser 1.000,00 mais 1/3 de 333,33, total 1.333,33
    E nao deve haver INSS nem IRRF sobre o abono

  Cenario: Primeira parcela do 13o
    Dado um colaborador com 12 meses trabalhados e salario-base 3.000,00
    Quando o RH gerar a 1a parcela do 13o
    Entao o valor deve ser 1.500,00 sem INSS nem IRRF

  Cenario: Alerta de documento a vencer
    Dado um documento com validade em 25 dias
    Quando o RH abrir os alertas
    Entao o sistema exibe o alerta de vencimento do documento

  Cenario: Convencao coletiva altera o adicional de domingo
    Dado um colaborador com salario-base 2.200,00 e divisor 220
    E a convencao cadastrada como parametro com adicional de 120% em domingo e feriado
    Quando o RH lancar 2 horas extras em domingo
    Entao o valor pago deve ser 44,00 (10,00 x 2,2 x 2 horas)
    E a memoria de calculo cita o parametro da convencao usado

  Cenario: Sem convencao cadastrada valem os padroes da CLT
    Dado que nenhuma convencao foi cadastrada
    Quando o RH lancar 2 horas extras em domingo para salario-base 2.200,00
    Entao o valor pago deve ser 40,00 (adicional padrao de 100%)

  Cenario: Contracheque em PDF
    Dado uma folha calculada de um colaborador
    Quando o RH gerar o contracheque
    Entao o PDF mostra proventos, descontos, liquido e memoria resumida

  Cenario: Exportar relatorio
    Dado o relatorio da folha do mes na tela
    Quando o diretor exportar em Excel
    Entao os valores do arquivo devem ser iguais aos da tela

  Cenario: Mensagem de erro indica o campo
    Quando o RH salvar um colaborador sem data de admissao
    Entao o sistema exibe "Informe a data de admissao" ao lado do campo

  Cenario: Desempenho do calculo
    Dado 50 colaboradores ativos com eventos lancados
    Quando o RH calcular a folha
    Entao o calculo termina em ate 5 segundos

  Cenario: Desempenho de consulta
    Dado a lista de colaboradores com 50 registros
    Quando o RH abrir a lista
    Entao a tela carrega em ate 2 segundos

  Cenario: Restauracao de backup
    Dado um backup diario valido
    Quando o Admin restaurar o backup em ambiente de teste
    Entao os dados voltam integros em ate 4 horas
    E a perda maxima e de 24 horas

  Cenario: Dados fora do prazo de guarda
    Dado um colaborador desligado ha mais de 5 anos
    Quando o RH abrir a lista de dados vencidos
    Entao o sistema sinaliza o colaborador
    E a eliminacao so ocorre com confirmacao do RH e registro em log

  Cenario: Ferias reduzidas por faltas
    Dado um colaborador com 7 faltas injustificadas no periodo aquisitivo
    Quando as ferias forem solicitadas
    Entao o direito deve ser de 24 dias

  Cenario: Afastamento por doenca apos 15 dias
    Dado um colaborador com salario-base 3.000,00
    E afastado pelo INSS a partir do dia 10 de um mes de 30 dias
    Quando a folha desse mes for calculada
    Entao o salario pago deve ser 2.400,00
    E esses 24 dias sao 9 trabalhados mais 15 de afastamento pagos pela empresa
    E os dias do 16o dia de afastamento em diante ficam com salario suspenso

  Cenario: DSR sobre horas extras
    Dado a competencia 10/2026 com 26 dias uteis e 5 domingos e feriados
    E um colaborador com salario-base 2.200,00 e 10 horas extras em dia util
    Quando a folha for calculada
    Entao as horas extras devem ser 150,00
    E o DSR sobre as horas extras deve ser 28,85

  Cenario: Folha completa com horas extras e DSR
    Dado o colaborador do cenario anterior sem dependentes
    Quando a folha for calculada
    Entao o bruto deve ser 2.378,85 e o INSS 189,78
    E o IRRF deve ser 0,00 e o liquido 2.189,07

  Cenario: Feriado cadastrado altera o DSR
    Dado a competencia 10/2026 e um feriado municipal cadastrado pelo RH
    E 10 horas extras em dia util com salario-base 2.200,00
    Quando a folha for calculada
    Entao o DSR deve ser 36,00 (150,00 / 25 x 6)

  Cenario: Calendario inicial de feriados
    Dado o sistema recem instalado
    Quando o RH abrir o calendario de feriados
    Entao devem existir os 10 feriados nacionais de 2026, incluindo 12/10/2026

  Cenario: IRRF com dependentes
    Dado um colaborador com salario-base 5.500,00 e 2 dependentes
    Quando a folha for calculada
    Entao o INSS deve ser 571,51 e o IRRF 101,78
    E o liquido deve ser 4.826,71

  Cenario: IRRF isento
    Dado um colaborador com salario-base 2.000,00 e sem dependentes
    Quando a folha for calculada
    Entao o INSS deve ser 155,69 e o IRRF 0,00
    E o liquido deve ser 1.844,31

  Cenario: FGTS como encargo da empresa
    Dado um colaborador com salario-base 3.000,00
    Quando a folha for calculada
    Entao o FGTS deve ser 240,00 como encargo da empresa
    E o liquido do colaborador nao deve ser reduzido pelo FGTS

  Cenario: Ferias com INSS e IRRF
    Dado um colaborador com salario-base 3.000,00 e 30 dias de ferias gozados
    Quando o RH calcular as ferias
    Entao a base deve ser 4.000,00 e o INSS 368,60
    E o IRRF deve ser 0,00 e o liquido 3.631,40

  Cenario: Reflexo das horas extras nas ferias
    Dado um colaborador com salario-base 2.200,00 e media mensal de horas extras de 150,00
    Quando o RH calcular as ferias de 30 dias
    Entao a base deve ser 2.350,00, o adicional de 1/3 deve ser 783,33
    E o total deve ser 3.133,33

  Cenario: Reflexo das horas extras no 13o
    Dado um colaborador com 12 meses, salario-base 2.200,00 e media mensal de horas extras de 150,00
    Quando o RH gerar a 1a parcela do 13o
    Entao o valor deve ser 1.175,00 sem descontos

  Cenario: Segunda parcela do 13o
    Dado o colaborador do cenario anterior com 1a parcela paga de 1.175,00
    Quando o RH gerar a 2a parcela do 13o
    Entao o INSS sobre 2.350,00 deve ser 187,19 e o IRRF 0,00
    E a 2a parcela deve ser 987,81

  Cenario: 13o proporcional
    Dado um colaborador admitido em 20/08/2026 com salario-base 3.000,00
    Quando o RH calcular o 13o de 2026
    Entao devem contar 4 meses (setembro a dezembro)
    E o 13o deve ser 1.000,00

  Cenario: Desligamento no meio do mes
    Dado um colaborador com salario-base 3.000,00 desligado no dia 10 de um mes de 30 dias
    Quando a folha desse mes for calculada
    Entao o salario proporcional deve ser 1.000,00

  Cenario: Atestado valido nao desconta
    Dado um colaborador com atestado medico valido de 3 dias anexado
    Quando a folha for calculada
    Entao nao deve haver desconto de falta nem de DSR

  Cenario: Atestado sem anexo
    Quando o RH registrar um atestado sem anexo ou sem periodo
    Entao o sistema rejeita e indica o campo pendente

  Cenario: Hora extra negativa
    Quando o RH lancar -2 horas extras
    Entao o sistema rejeita e informa que a quantidade deve ser maior que zero

  Cenario: Colaborador sem vale-transporte
    Dado um colaborador que nao optou pelo vale-transporte
    Quando a folha for calculada
    Entao nao deve haver desconto de vale-transporte

  Cenario: Verba avulsa com incidencia
    Dado um provento avulso de 100,00 marcado com incidencia em INSS e IRRF
    Quando a folha for calculada
    Entao os 100,00 devem entrar nas bases de INSS e IRRF
    E a verba deve aparecer na memoria de calculo

  Cenario: Verba avulsa sem incidencia
    Dado um provento avulso de 100,00 sem marcacao de incidencia
    Quando a folha for calculada
    Entao os 100,00 nao devem entrar nas bases de INSS e IRRF

  Cenario: Inicio das ferias antes de feriado
    Dado o feriado nacional de 07/09/2026 (segunda-feira)
    Quando o RH pedir ferias com inicio em 05/09/2026
    Entao o sistema rejeita informando que o gozo nao pode comecar
    E explica que e vedado nos 2 dias antes de feriado ou descanso semanal

  Cenario: Data limite de pagamento das ferias
    Dado ferias aprovadas com inicio em 10/11/2026
    Quando o RH abrir o pedido
    Entao o sistema mostra a data limite de pagamento 08/11/2026

  Cenario: Recalcular enquanto a competencia nao esta fechada
    Dado uma competencia calculada e ainda nao fechada
    Quando o RH alterar um evento e calcular de novo
    Entao a folha deve ser recalculada com os novos valores

  Cenario: Alerta de prazo de pagamento
    Dado uma competencia ainda nao fechada no 3o dia util do mes seguinte
    Quando o RH abrir os alertas
    Entao o sistema exibe o alerta de prazo de pagamento da folha

  Cenario: CPF invalido
    Quando o RH cadastrar um colaborador com CPF de digitos verificadores incorretos
    Entao o sistema rejeita e informa que o CPF e invalido

  Cenario: Desligamento anterior a admissao
    Quando o RH informar desligamento em data anterior a admissao
    Entao o sistema rejeita e indica o campo data de desligamento

  Cenario: Anexo invalido
    Quando o RH anexar um arquivo de 12 MB ou em formato nao permitido
    Entao o sistema rejeita e informa os formatos e o tamanho aceitos

  Cenario: Bloqueio por tentativas de senha
    Dado um usuario cadastrado
    Quando ele errar a senha 5 vezes seguidas
    Entao o sistema bloqueia o acesso por 15 minutos

  Cenario: Admin gerencia usuarios
    Dado um usuario com perfil Admin
    Quando ele criar um usuario com perfil RH
    Entao o sistema registra a criacao no log

  Cenario: Admin nao ve dados da folha
    Dado um usuario com perfil Admin
    Quando ele tentar abrir a folha do mes
    Entao o sistema nega o acesso e registra a tentativa no log
```

### Rastreabilidade: requisito e cenários que o verificam

| Requisito | Cenários (nomes) |
|---|---|
| US-01, RN-11 a RN-14 | CPF duplicado; Salário zero; Inativar em vez de excluir; Cadastro sem dados sensíveis |
| US-02, RN-30 a RN-33, RN-50 | Hora extra; Falta com DSR; Vale-transporte; Competência fechada; Convenção coletiva (2 cenários) |
| US-03, RN-01 a RN-03, RN-21 a RN-23 | Cálculo normal; INSS no teto; IRRF com redução; Arredondamento; Parâmetro com e sem vigência; Admissão no meio do mês; Afastamento após 15 dias |
| US-04, RN-04 a RN-06 | Dado ausente; Descontos acima dos proventos; Fechar com saldo sem justificativa; Saldo na competência seguinte; Reabertura pelo RH com e sem justificativa; Diretoria não reabre |
| US-05, RN-40 a RN-46 | Férias com 1/3; Pedido antes do aquisitivo; Fracionamento (2); Abono; Férias reduzidas por faltas; 1ª parcela do 13º |
| US-06, RN-52, RN-53, RN-56 | Alerta de documento a vencer; Dados fora do prazo de guarda |
| US-07, RNF-01 a RNF-04 | Login, senha incorreta, sem login, sessão expirada; Diretoria sem permissão (2); Log de dado de saúde |
| US-08, US-09, RN-55 | Contracheque em PDF; Exportar relatório |
| RN-31, RN-32, RN-46, RN-47, RN-48 | DSR; Folha completa; Reflexo nas férias e no 13º; 2ª parcela; 13º proporcional; Início das férias antes de feriado; Data limite de pagamento |
| RN-16, RN-20, RN-22 a RN-24, RN-49 | IRRF com dependentes; IRRF isento; FGTS; Férias com INSS e IRRF; Desligamento no mês; Admissão e desligamento no mesmo mês; Férias que cruzam dois meses |
| US-10, US-11, RN-25 a RN-27, RN-35 | Verba avulsa (2); Calendário inicial de feriados; Feriado altera o DSR; Aviso na tela de parâmetros |
| US-12, RN-08, RN-15, RN-58 | Admin gerencia usuários e não vê a folha; Recalcular enquanto aberta; Alerta de prazo; CPF inválido; Desligamento antes da admissão; Atestado sem anexo; Hora extra negativa |
| RNF-19, RNF-21 | Bloqueio por tentativas de senha; Anexo inválido |
| RNF-08 a RNF-13, RNF-15 | Desempenho (2); Restauração de backup; Mensagem de erro indica o campo |

## 11. Dados de exemplo (fictícios)

| Colaborador | Filial | Cargo | Salário-base | Admissão | Caso |
|---|---|---|---|---|---|
| Ana Souza | Matriz | Atendente | 2.200,00 | 10/03/2023 | Normal, com 2 h extras |
| Bruno Lima | Filial 1 | Gerente | 5.000,00 | 02/01/2021 | Férias com abono |
| Carla Dias | Filial 2 | Atendente | 1.900,00 | 15/09/2026 | Admissão no meio do mês |
| Diego Alves | Matriz | Operador | 2.000,00 | 05/06/2022 | Atestado de 3 dias |
| Elisa Rocha | Filial 1 | Analista | 3.000,00 | 20/08/2024 | Desligada em 10/2026 (borda) |
| Fabio Nunes | Matriz | Atendente | 2.200,00 | 01/02/2025 | ERRO: CPF duplicado |
| Gabi Melo | Matriz | Atendente | 0,00 | 01/04/2025 | ERRO: salário zero |
| Hugo Pires | Filial 2 | Gerente | 5.500,00 | 12/05/2020 | IRRF com 2 dependentes |
| Iara Costa | Filial 1 | Atendente | 3.000,00 | 20/08/2026 | 13º proporcional (4/12) |

**Casos de borda a cobrir nos testes:** CPF duplicado, salário zero ou negativo, hora extra negativa, descontos acima dos proventos, competência fechada, admissão e desligamento no mesmo mês, férias cruzando dois meses, salário acima do teto do INSS.

## 12. Telas da 1ª versão

| Tela | Conteúdo |
|---|---|
| Login | E-mail, senha e controle de sessão |
| Lista de colaboradores | Busca por nome ou CPF, filtro por filial e situação, botão Novo |
| Ficha do colaborador | Abas: Dados, Contrato, Documentos, Férias, Histórico. Botões Editar e Inativar |
| Lançamento de eventos | Competência, colaborador, tipo (hora extra, falta, atestado, VT, VA, verba avulsa), quantidade e observação |
| Folha do mês | Status da competência, botões Calcular e Fechar, lista com proventos, descontos, líquido e pendências; clicar na linha abre a memória de cálculo |
| Férias | Período aquisitivo e concessivo, saldo, solicitação, status e aprovação, alerta de vencimento |
| Contracheque | Geração em PDF por colaborador e competência |
| Relatórios | Seleção do relatório e competência, exportação em PDF e Excel |
| Parâmetros e feriados | Lista de parâmetros legais com início e fim de vigência; calendário de feriados (nacionais, estaduais e municipais); só o RH altera. A tela exibe, em destaque, uma trava visual com o aviso: "Atenção: a alteração de alíquotas e bases legais sem validação do contador pode gerar cálculos incorretos e passivos jurídicos para a empresa." (RN-27) |
| Alertas | Documentos, exames ocupacionais, férias a vencer, afastamentos e prazo de pagamento da folha |

## 13. Relatórios [ADOTADO]

Todos com exportação em PDF e Excel e com competência, filial, data de geração e usuário. O relatório de log só aparece para diretoria e admin.

| Relatório | Campos | Filtros |
|---|---|---|
| Folha do mês | Colaborador, filial, proventos, descontos, líquido, FGTS; totais por filial e geral | Competência, filial |
| Contracheque | Empresa, filial, competência, colaborador (nome, CPF, cargo, admissão), verbas (descrição, referência, provento, desconto), totais, líquido, bases de INSS, IRRF e FGTS, memória resumida | Competência, colaborador |
| Férias | Colaborador, início do aquisitivo, fim do concessivo, dias de saldo, situação, vencimento | Filial, situação |
| Horas extras do mês | Colaborador, horas em dia útil, horas em domingo e feriado, valor, DSR | Competência, filial |
| Colaboradores ativos | Nome, CPF, cargo, setor, filial, admissão, salário-base | Filial, situação |
| Documentos e exames a vencer | Colaborador, documento ou exame, validade, dias para vencer | Prazo (30 dias padrão) |
| Dados de pagamento | Colaborador, líquido, banco, agência, conta, competência | Competência, filial |
| Log de acessos e alterações | Usuário, data e hora, ação, dado, valor antes e depois | Período, usuário (só diretoria e admin) |

## 14. Requisitos não funcionais

### 14.1 Segurança, LGPD e backup

- **RNF-01** Login com e-mail e senha; senhas com hash; sessão expira após 30 minutos sem atividade [ADOTADO].
- **RNF-02** Permissões por perfil (seção 4).
- **RNF-03** Log de acesso e alteração (quem, quando, o quê, valor antes e depois). Logs não podem ser editados nem apagados.
- **RNF-04** Dados sensíveis e dados de saúde cifrados em repouso; comunicação por HTTPS.
- **RNF-05** Backup diário, com teste periódico de restauração [CONFIRMADO].
- **RNF-06** Acesso por computador; versão para celular fica para a 2ª versão [ADOTADO].
- **RNF-07** Atender à LGPD: finalidade clara para cada dado, acesso mínimo necessário e retenção de 5 anos após o desligamento.
- **RNF-19** Senha com pelo menos 10 caracteres, com letras e números; bloqueio de 15 minutos após 5 tentativas erradas [ADOTADO].
- **RNF-20** Datas e horas no fuso de Brasília; logs guardados por 5 anos [ADOTADO].
- **RNF-21** Anexos em PDF, JPG ou PNG de até 10 MB [ADOTADO].

### 14.2 Desempenho [ADOTADO]

- **RNF-08** Cálculo da folha de 15 a 50 colaboradores em até **5 segundos**.
- **RNF-09** Telas de consulta respondem em até **2 segundos** em uso normal.
- **RNF-10** Contracheque e relatórios gerados em até **10 segundos**.
- **RNF-11** Suporta até **10 usuários simultâneos** e **50 colaboradores** sem mudar a estrutura.

### 14.3 Disponibilidade e recuperação [ADOTADO]

- **RNF-12** Disponibilidade de 99% em horário comercial.
- **RNF-13** Perda máxima de dados de 24 horas (RPO) e restauração em até 4 horas (RTO).

### 14.4 Usabilidade

- **RNF-14** Interface em português do Brasil, valores em reais (R$) e datas em dd/mm/aaaa.
- **RNF-15** Mensagens de erro dizem **qual campo** está errado e **o que fazer**.
- **RNF-16** Qualquer valor da folha se explica com no máximo 2 cliques (memória de cálculo).

### 14.5 Manutenibilidade e qualidade

- **RNF-17** Toda regra de cálculo tem teste automatizado derivado dos cenários da seção 10.
- **RNF-18** Mudanças nesta especificação são versionadas (seção 19).

### 14.6 Mensagens padrão de erro

| Situação | Mensagem |
|---|---|
| CPF repetido | Já existe um colaborador com este CPF. |
| CPF inválido | CPF inválido. Confira os 11 dígitos. |
| Campo obrigatório vazio | Informe [nome do campo]. |
| Competência fechada | Esta competência está fechada. Para alterar, reabra informando a justificativa. |
| Aquisitivo incompleto | O período aquisitivo ainda não foi completado. |
| Líquido negativo | Os descontos superam os proventos. O excedente virou saldo a descontar; informe a justificativa para fechar. |
| Sem permissão | Você não tem permissão para esta ação. |
| Login inválido | E-mail ou senha inválidos. |
| Bloqueio por tentativas | Acesso bloqueado por 15 minutos após 5 tentativas incorretas. |
| Anexo inválido | Arquivo inválido. Use PDF, JPG ou PNG de até 10 MB. |

## 15. Uso de IA

### 15.1 Prompts para o desenvolvimento (GTI 2º período)

Cole este documento antes de cada prompt. Regra comum: *"Não crie regra de negócio. Se faltar informação, marque como hipótese e liste como pergunta pendente."*

| Prompt | Texto |
|---|---|
| 1. Revisar a spec | Você é analista de requisitos. Liste ambiguidades, regras sem exemplo, casos de borda faltando e contradições, em tabela. Não crie regra nova. |
| 2. Gerar testes | A partir das regras RN-30 a RN-33 e dos cenários Gherkin, gere testes automatizados de horas extras com casos de borda. Use tipo decimal para dinheiro. Informe quais testes dependem de pendências. |
| 3. Modelar o banco | Proponha tabelas, campos e chaves para colaboradores, filiais, eventos, folha, memória de cálculo, parâmetros com vigência, férias, documentos e logs. Valores legais ficam em tabela de parâmetros. |
| 4. Implementar uma etapa | Implemente apenas a Etapa 1 (login, perfis, cadastro), seguindo RN-10 a RN-14 e as user stories US-01 e US-07. Escreva os testes primeiro. Não implemente nada fora da etapa. |
| 5. Conferir o gerado | Compare o código com a especificação. Liste comportamento que não está na spec, valores fixos no código e regras sem teste. |

### 15.2 Revisão desta especificação com IA

**Ferramenta:** Claude Sonnet 5.5 (Anthropic), usado pela equipe durante todo o levantamento e a escrita, para apontar ambiguidades, inconsistências e requisitos ausentes e para gerar cenários e exemplos. **As decisões foram da equipe**; a parte legal ainda precisa de conferência de um contador. Principais ajustes:

| # | Tipo | O que a IA apontou | Ajuste feito |
|---|---|---|---|
| 1 | Inconsistência | Cliente informou 20 colaboradores e 4 filiais, depois 15 e matriz + 2 filiais; a folha aparecia como etapa futura | RH confirmou 15 e matriz + 2 filiais; folha virou o núcleo da 1ª versão (seção 1) |
| 2 | Ambiguidade | Não estava claro se o sistema calcula ou só organiza a folha, quais perfis existem e quem fecha | Decidido: o sistema calcula; perfis RH, Diretoria e Admin; RH fecha e aprova (seções 1 e 4) |
| 3 | Risco LGPD | Cliente pediu religião, sexualidade, raça, dados genéticos e biomédicos, sem necessidade para a folha | RH confirmou não armazenar; criada a RN-14 e um cenário de teste |
| 4 | Requisito ausente | Faltavam memória de cálculo, fechamento, bloqueios, arredondamento, DSR, retenção, logs e metas de desempenho | Incluídos RN-02 a RN-06, RN-31, RN-32, RN-56, tabela 7.1 e seção 14 |
| 5 | Verificação | INSS e IRRF vinham da memória da IA; cenário de falta ignorava o DSR da RN-33 | Tabelas conferidas em fontes públicas (13/10/2026); exemplos recalculados; cenário de falta corrigido |
| 6 | Sem teste | Regras só em texto ou como [HIPÓTESE] deixavam margem para o agente interpretar | Cenários Gherkin com erros, matriz de rastreabilidade e modelo de dados; hipóteses viraram [ADOTADO] com valores |
| 7 | Pendência | Convenção coletiva sem nome nem valores bloqueava a decisão | Virou premissa: padrões da CLT, com a convenção como parâmetro cadastrável e dois cenários de teste |
| 8 | Lacuna | DSR, reflexos, 13º, incidências por verba, feriados e validações de campo sem regra completa ou sem teste | Incluídas RN-08, RN-15, RN-16, RN-25, RN-26, RN-35, RN-47 a RN-49 e RN-58, tabelas 7.4 e 7.5, exemplos G a N e mais de 30 cenários; dados de 2026 conferidos em fontes oficiais |

**Limites da revisão:** valores legais e adicionais da convenção precisam de confirmação por contador ou RH; itens [ADOTADO] são decisões provisórias; a IA pode errar em detalhes de legislação, por isso cada número tem exemplo de cálculo e tolerância de R$ 0,01.

**Prompts usados na elaboração (resumo):** (1) montar os requisitos a partir do questionário, marcando o que for suposição; (2) transformar perguntas em propostas que o cliente só confirma; (3) pesquisar e conferir as tabelas de INSS e IRRF de 2026; (4) revisar a especificação contra o enunciado e os slides da aula; (5) escrever cenários Gherkin com erros e ligar cada requisito ao seu teste.

### 15.3 Antes de começar: decisões técnicas e modo de uso com agente de IA

Esta especificação define **o que** o sistema faz. As decisões abaixo **não** estão nela e o GTI 2º período precisa tomá-las e informá-las à IA em todo prompt; se ninguém decidir, a IA escolhe sozinha.

| Decisão | Como tratar | Quem decide |
|---|---|---|
| Linguagem e framework | A equipe escolhe uma combinação e a informa em todo prompt | GTI 2º período |
| Banco de dados | PostgreSQL ou MySQL (seção 2); dinheiro em tipo decimal | GTI 2º período |
| Estrutura técnica (camadas, API, tabelas) | A IA propõe (prompt 3 da seção 15.1) e a equipe aprova antes de gerar código | GTI 2º período |
| Visual das telas | Livre, respeitando a seção 12 | GTI 2º período |
| Testes automatizados | Usar o framework da linguagem escolhida; os cenários da seção 10 e os exemplos da seção 8 viram testes | GTI 2º período |

- **Uma etapa por vez**, na ordem da seção 2. A Etapa 3 (cálculo) só começa com a Etapa 2 completa, incluindo verbas avulsas.
- **Testes primeiro:** uma etapa só é considerada pronta quando todos os testes dela passam.
- **Nada fixo no código:** valores legais ficam na tabela de parâmetros (RN-01).
- **Conferir tudo contra o documento** (prompt 5): regra que não está aqui não entra no sistema.
- **Dúvida ou conflito:** registrar e perguntar ao GTI 4º período; a IA não decide regra de negócio.
- **Cálculos da folha:** revisão humana, de preferência com apoio contábil, antes de qualquer uso real.

## 16. Pendências e decisões adotadas

> Nenhum item abaixo impede o desenvolvimento. Onde o RH não respondeu, o grupo adotou a melhor opção. Se o RH ou o contador pedir mudança, altera-se o parâmetro e gera-se uma nova versão deste documento.

| ID | Assunto | Decisão adotada | Revisão futura |
|---|---|---|---|
| P-01 | Convenção coletiva (nome, adicionais, piso, regras de VA e VT) | Valem os padrões da CLT; a convenção entra como parâmetro cadastrável, sem mudar código | Cadastrar os valores quando o RH informar |
| P-02 | Conferência das tabelas e regras por contador | Tabelas oficiais de 2026 já conferidas em fontes públicas; exemplos recalculados | Recomendada antes do uso real |
| P-03 | Afastados na folha (INSS, maternidade etc.) | Regra definida na RN-34 | Compensação junto ao INSS na 2ª versão |
| P-04 | Itens [ADOTADO] (retenção, relatórios, arredondamento, VT, VA, contracheque, reabertura, fracionamento) | Valem como descritos; todos são parâmetros configuráveis | Ajustar se o RH pedir |

## 17. Registro do levantamento (ata resumida)

- **Fatos (informados pelo cliente):** todas as decisões marcadas CONFIRMADO na seção 1. As informações foram passadas por Alana Catiany de Morais, do grupo de RH, em 08/10, e o questionário de confirmação foi respondido pelo grupo em 14/10. Um integrante do GTI 4º período também enviou mensagens para ajudar no levantamento.
- **Conflito resolvido:** o cliente havia informado 20 e 15 colaboradores, e 4 filiais ou matriz + 2 filiais; o RH confirmou 15 colaboradores e matriz + 2 filiais.
- **Decisões do grupo (GTI 4º período):** o sistema calcula a folha; valores legais parametrizados; sem campos de dados sensíveis desnecessários; padrões [ADOTADO] onde o cliente não respondeu.
- **Decisões sem resposta do cliente:** todas marcadas [ADOTADO] neste documento, com a melhor opção escolhida pelo grupo. Nenhuma bloqueia o desenvolvimento.
- **Fontes dos parâmetros legais:** tabelas públicas de INSS e IRRF de 2026, consultadas em 13/10/2026.

## 18. Checklist de qualidade (slide 22 da aula)

| Critério | Como o documento atende | Onde |
|---|---|---|
| Clareza | Linguagem de negócio, glossário e regras numeradas | Seções 3 e 5 |
| Testabilidade | Cenários Gherkin com erros e matriz de rastreabilidade | Seção 10 |
| Exemplos | Casos normais, de borda e de erro com valores calculados | Seções 8, 10 e 11 |
| Parametrização | Nenhum valor legal fixo; parâmetros com vigência | RN-01 e seção 6 |
| Rastreabilidade | Decisões com status e origem; ata de fatos, decisões e hipóteses | Seções 1.4 e 17 |
| Auditabilidade | Memória de cálculo e logs de acesso e alteração | RN-02 e RNF-03 |
| Ambiguidades explícitas | Pendências, hipóteses e ajustes da revisão com IA | Seções 15.2 e 16 |
| Versionamento | Histórico de versões e regra de mudança | Seção 19 |
| Tabelas de decisão | Fechamento da folha, pedido de férias e horas extras, com exceções | Seção 7 |
| Prompt pack | Prompts para o desenvolvimento e prompts usados na elaboração | Seção 15 |

## 19. Histórico de versões

| Versão (toda mudança de regra gera uma nova) | Data | Mudança |
|---|---|---|
| 0.1 | 13/10/2026 | Rascunho a partir do levantamento inicial, com regras como hipótese |
| 0.5 | 14/10/2026 | Respostas do grupo de RH incorporadas; conflitos de porte e filiais resolvidos |
| 1.0 | 14/10/2026 | Versão consolidada enviada ao GTI 2º período |
| 1.1 | 20/10/2026 | Atualizada de acordo com o que o professor Juan abordou em sala de aula e alinhada com o restante dos requisitos que foram solicitados no Classroom pelo professor Juan; equipe do 2º período atualizada. |
| 1.2 | 20/10/2026 | Documento completado para o desenvolvimento (inclui reabertura pelo RH com log destacado e aviso na tela de parâmetros): regras de DSR, reflexos, 13º, feriados, verbas avulsas, validações, incidências e ciclo da competência; cenários e exemplos novos; campos dos relatórios e mensagens padrão |
| 1.3 | 21/10/2026 | Incluída a seção 15.3: decisões técnicas que o GTI 2º período deve tomar e modo de uso do documento com agente de IA |
