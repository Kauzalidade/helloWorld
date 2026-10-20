# Guia de Uso de Inteligência Artificial no Projeto

Este documento orienta a equipe de desenvolvimento do **GTI 2º período** sobre como utilizar ferramentas e agentes de Inteligência Artificial de forma produtiva, segura e alinhada à especificação elaborada pelo **GTI 4º período**.

---

## 🎯 Regra de Ouro com IA

> **"Não crie regra de negócio. Se faltar informação, marque como hipótese e liste como pergunta pendente."**

Ao interagir com qualquer modelo ou agente de IA, certifique-se de que a IA **não invente regras tributárias, trabalhistas ou comportamentais** para preencher lacunas. Toda dúvida deve ser registrada como `[HIPÓTESE]` e encaminhada para o arquivo [docs/perguntas-pendentes.md](file:///c:/Users/Kauã/OneDrive/Documentos/GitHub/helloWorld/docs/perguntas-pendentes.md).

---

## 📋 Como Preparar o Contexto para a IA

Antes de enviar qualquer solicitação de código ou modelagem para a IA:
1. Forneça o arquivo [docs/especificacao-requisitos.md](file:///c:/Users/Kauã/OneDrive/Documentos/GitHub/helloWorld/docs/especificacao-requisitos.md) como contexto ou anexo.
2. Reforce a instrução de respeitar as diretrizes de [AGENTS.md](file:///c:/Users/Kauã/OneDrive/Documentos/GitHub/helloWorld/AGENTS.md).
3. Especifique claramente qual das **4 etapas** está sendo trabalhada. Não permita que a IA implemente recursos de etapas futuras.

---

## 🛠️ Prompts Padronizados da Especificação (Seção 15)

Utilize os prompts abaixo para manter a consistência e a rastreabilidade do projeto:

### 1. Revisar a Especificação
*Use quando quiser identificar pontos cegos, ambiguidades ou casos de borda antes de codificar.*

```text
Você é analista de requisitos. 
Com base na especificação em anexo, liste ambiguidades, regras sem exemplo, casos de borda faltando e contradições, em formato de tabela. 
Não crie regra nova. Se houver lacuna, identifique-a como hipótese ou dúvida a ser esclarecida com o GTI 4º período.
```

---

### 2. Gerar Testes Automatizados
*Use antes de começar a implementação de um cálculo ou funcionalidade (TDD).*

```text
A partir das regras RN-30 a RN-33 e dos cenários Gherkin da especificação, gere testes automatizados de horas extras, DSR e faltas cobrindo todos os casos de borda. 
Atenção: Use tipo decimal para dinheiro (nunca ponto flutuante). 
Informe claramente quais testes dependem de pendências em aberto.
```

---

### 3. Modelar o Banco de Dados
*Use para propor schemas, migrations e relacionamentos relacionais.*

```text
Proponha tabelas, campos, chaves primárias/estrangeiras e índices para colaboradores, filiais, eventos, folha, memória de cálculo, parâmetros com vigência, férias, documentos e logs. 
Atenção às regras arquiteturais:
- Valores monetários em DECIMAL(12,2).
- Valores e alíquotas legais (INSS, IRRF, FGTS, salário mínimo) devem ficar em tabelas de parâmetros com data de início e fim de vigência.
- Nenhum campo para religião, sexualidade, raça/etnia ou biometria (LGPD - RN-14).
```

---

### 4. Implementar uma Etapa
*Use para gerar a implementação incremental de uma etapa específica do projeto.*

```text
Implemente apenas a Etapa 1 (login, perfis, filiais e cadastro de colaboradores), seguindo estritamente as regras RN-10 a RN-14 e as user stories US-01 e US-07. 
Escreva os testes automatizados primeiro. 
Não implemente nenhuma funcionalidade fora do escopo desta etapa.
```

---

### 5. Conferir e Auditar o Código Gerado
*Use para validar o código gerado pela IA ou por outro desenvolvedor contra a especificação.*

```text
Compare o código implementado com a especificação de requisitos. 
Liste em detalhes:
1. Comportamentos implementados que não estão na especificação.
2. Valores fixos (hardcoded) no código que deveriam ser parâmetros parametrizáveis por vigência.
3. Regras de negócio que ainda não possuem testes automatizados associados.
4. Possíveis violações de precisão decimal ou da LGPD.
```

---

## 🔍 Checklist de Aceite do Código Gerado por IA

Antes de aceitar ou realizar *commit* de código gerado por IA, valide os seguintes pontos:

- [ ] **Precisão Monetária:** Foi usado tipo decimal ou biblioteca de precisão arbitrária? (Nenhum `float`/`double` para dinheiro).
- [ ] **Parametrização:** Existem alíquotas ou faixas legais fixadas no código (*hardcoded*)? (Devem vir do banco com vigência).
- [ ] **Arredondamento:** O arredondamento é de 2 casas, "meio para cima", aplicado por verba antes da soma?
- [ ] **LGPD:** O cadastro respeitou a ausência de dados proibidos (religião, sexualidade, raça, biometria)?
- [ ] **Inativação:** Foi implementada inativação lógica em vez de exclusão física para colaboradores?
- [ ] **Logs de Auditoria:** Operações críticas registram usuário, data, hora, ação e valores anterior/novo?
- [ ] **Testes Passando:** Os testes baseados nos cenários Gherkin (Seção 10) e exemplos numéricos (Seção 8) foram executados e passaram?
