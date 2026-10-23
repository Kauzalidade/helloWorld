# Perguntas Pendentes e Hipóteses de Negócio

Este documento registra todas as pendências formais, hipóteses não confirmadas e dúvidas de negócio do **projetoFolha** (Sistema de RH e Folha de Pagamento).

> **Regra de ouro:** Se faltar informação, **não inventem a regra**; anotem a dúvida neste arquivo e perguntem ao **GTI 4º período** ou ao cliente.

---

## 📌 1. Pendências Oficiais da Especificação (Seção 16)

| ID | Pendência | Responsável | Impede Início? | Status Atual | Detalhamento / Pergunta |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **P-01** | **Convenção Coletiva de Trabalho (CCT)** | Grupo de RH | Não (usar padrões CLT) | Aberto | Qual o sindicato/CCT da categoria? Existem pisos salariais específicos, adicionais de horas extras diferenciados ou regras próprias para VT/VA? |
| **P-02** | **Conferência das tabelas e regras por contador** | Cliente / Contador | Não (necessária antes de produção) | Aberto | O contador do cliente validou os cálculos de 2026 (Portaria MPS/MF 13/2026 e Lei 15.270/2025 para IRRF com redução progressiva)? |
| **P-03** | **Tratamento de afastados na folha** | Grupo de RH | Não na 1ª versão | Aberto | Como tratar afastamento por INSS (>15 dias), licença maternidade e paternidade no cálculo do salário e nos encargos? |
| **P-04** | **Confirmação dos itens adotados [ADOTADO]** | Grupo de RH | Não (parâmetros configuráveis) | Aberto | Confirmar os padrões definidos pelo GTI 4º período (arredondamento, prazos de retenção LGPD, relatórios e layout de contracheque). |

---

## 🔍 2. Hipóteses Mapeadas que Precisam de Confirmação

| Ref. | Tema | Hipótese Assumida | Impacto no Código | Pergunta para o GTI 4º Período / Cliente |
| :--- | :--- | :--- | :--- | :--- |
| **H-01** (Seção 4 / RN-04) | Reabertura de Competência | O RH solicita a reabertura justificando o motivo, e a **Diretoria aprova** formalmente. | Fluxo de aprovação com mudança de estado da folha (`FECHADA` -> `SOLICITADA_REABERTURA` -> `ABERTA`). | Apenas a diretoria pode aprovar a reabertura ou o próprio gestor de RH pode fazê-lo diretamente em caso de urgência? |
| **H-02** (Seção 4 / RN-54) | Acesso a Dados de Saúde | A Diretoria **NÃO** tem acesso a atestados e exames; apenas o RH tem permissão. | Regra de autorização (RBAC) e ocultação de anexos médicos para perfil Diretoria. | A diretoria pode visualizar o motivo/CID do atestado ou apenas o total de dias de ausência para fins de planejamento? |
| **H-03** (RN-10) | Campos Mínimos de Cadastro | Nome, CPF, nascimento, admissão, cargo, setor, filial, salário-base, jornada, dados bancários e dependentes IRRF. | Definição dos campos obrigatórios (`NOT NULL`) na tabela de colaboradores. | Há necessidade de telefone, e-mail pessoal ou endereço completo obrigatório já na Etapa 1? |
| **H-04** (RN-20) | Proporcionalidade de Admissão/Demissão | Admitidos ou desligados no mês recebem proporcional aos dias corridos trabalhados (fração de 30 avos). | Fórmula do cálculo do salário no mês de admissão/desligamento. | O divisor de proporcionalidade de mês incompleto é sempre 30 ou considera o número exato de dias do mês (ex.: 28, 31)? |
| **H-05** (RN-42) | Fracionamento de Férias | Permitido em até 3 períodos: um de no mínimo 14 dias e os demais com no mínimo 5 dias. | Validação das datas no formulário de agendamento de férias. | O cliente adota a regra padrão da CLT de fracionamento ou há política interna de período mínimo único? |
| **H-06** (RN-44) | Redução de Férias por Faltas | Faltas injustificadas no período aquisitivo reduzem o saldo de dias conforme tabela CLT (art. 130). | Tabela progressiva de abatimento de dias de férias por número de faltas. | O RH deseja que o sistema reduza os dias automaticamente com base nas faltas lançadas no período aquisitivo? |
| **H-07** (RNF-06) | Responsividade Mobile | Foco prioritário é acesso via desktop/computador; celular responsivo apenas se houver tempo hábil. | Complexidade do layout CSS da interface web. | O uso do sistema em tablets ou celulares por gestores é crítico para a 1ª versão? |

---

## ⚙️ 3. Padrões Adotados pelo GTI 4º Período ([ADOTADO])

Os itens abaixo foram configurados com base nas melhores práticas pelo grupo de requisitos, mas podem ser ajustados via parâmetros pelo cliente:

1. **Arredondamento (RN-03):** 2 casas decimais, arredondamento "metade para cima" (*half-up*), aplicado em cada verba antes de totalizar a folha.
2. **Vale-transporte (RN-50):** Opcional ao colaborador; desconto do menor valor entre 6% do salário-base e o custo informado pelo RH.
3. **Vale-alimentação (RN-51):** Valor mensal fixo por colaborador parametrizável, com coparticipação padrão de 0%.
4. **Contracheque (RN-55):** Emitido em PDF pelo RH (não haverá portal de autoatendimento para o colaborador na v1).
5. **Retenção LGPD (RN-56):** Preservação dos dados durante a vigência do contrato e por 5 anos após a rescisão; após isso, o sistema sugere anonimização com confirmação do RH.
6. **Relatórios (Seção 13):** Exportação disponível nos formatos PDF e Excel com carimbo de competência, filial, data e usuário responsável.

---

## 📝 4. Registro de Novas Dúvidas e Decisões

Ao encontrar uma nova dúvida durante o desenvolvimento, utilize a tabela abaixo para registrá-la:

| Data | Questão Encontrada | Responsável | Resposta / Decisão | Data da Resolução |
| :---: | :--- | :---: | :--- | :---: |
| 14/10/2026 | Divergência no número de colaboradores e filiais | GTI 4º | Confirmado pelo cliente: 15 colaboradores, 1 matriz + 2 filiais | 14/10/2026 |
| — | *(Adicione novas dúvidas aqui)* | — | — | — |
