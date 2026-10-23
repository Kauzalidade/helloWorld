# Guia de Uso de Inteligência Artificial no Projeto

Este documento orienta a equipe de desenvolvimento do **GTI 2º período** sobre como utilizar ferramentas e agentes de Inteligência Artificial de forma produtiva, segura e alinhada à especificação elaborada pelo **GTI 4º período**.

---

## 🎯 Regra de Ouro com IA

> **"Não crie regra de negócio. Se faltar informação, marque como hipótese e liste como pergunta pendente."**

Ao interagir com qualquer modelo ou agente de IA, certifique-se de que a IA **não invente regras tributárias, trabalhistas ou comportamentais** para preencher lacunas. Toda dúvida deve ser registrada como `[HIPÓTESE]` e encaminhada para o arquivo [docs/perguntas-pendentes.md](perguntas-pendentes.md).

---

## 📋 Como Preparar o Contexto para a IA

Antes de enviar qualquer solicitação de código ou modelagem para a IA:
1. Forneça o arquivo [docs/spec.md](spec.md) como contexto ou anexo.
2. Reforce a instrução de respeitar as diretrizes de [AGENTS.md](../AGENTS.md).
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



---

# Registro de uso de IA do grupo

## 20/10/2026 - Organização inicial do repositório
- Ferramenta: Antigravity (Gemini)
- Prompt: colei o PDF da especificação no chat e pedi para colocar
  na pasta docs e criar README, AGENTS.md e .gitignore
- Resultado: converteu a spec para Markdown e criou os arquivos
- O que conferi: números das tabelas de INSS/IRRF e exemplos da seção 8
- O que corrigi: o README trouxe um nome (Pietro) que não está no PDF;
  nada, estava correto


  # Registro de uso de IA do grupo

## 20/10/2026 - prompts utilizados no projetos
- Ferramenta: Antigravity (Gemini)
1- Cálculos Trabalhistas & Tabela de Retenção (RH + TI)
Prompt:
"Atuo em um projeto interdisciplinar entre Tecnologia e Recursos Humanos. Preciso criar a lógica/tabela para os cálculos das alíquotas progressivas do INSS e do Imposto de Renda (IRRF). Por favor, apresente o cálculo detalhado de cada faixa salarial e forneça um exemplo em pseudocódigo ou estrutura de dados (JSON/Array) para implementação em código."

2. Uso de Repositórios GitHub no ChatGPT
Prompt:
"Quais são as melhores formas de integrar ou consultar um repositório do GitHub dentro do ChatGPT? Explique como funciona a leitura de código via links públicos, uso de extensões/plugins ou upload direto de arquivos e repositórios na ferramenta."

3. Integração de Repositório Existente com IDEs / Ferramentas de I.A. (Ex: Anti-Gravity)
Prompt:
"Tenho um repositório existente no GitHub ([https://github.com/Kauzalidade/helloWorld](https://github.com/Kauzalidade/helloWorld)). Como faço para clonar esse projeto, sincronizar as alterações e trabalhar nele utilizando o ecossistema/IDE Anti-Gravity? Forneça o passo a passo pelos comandos de terminal do Git e pela interface visual."

4. Gerenciamento de Branches no Anti-Gravity / Git
Prompt:
"Como criar e alternar para uma nova branch (new branch) utilizando a interface do Anti-Gravity e via terminal Git? Explique o comando correto para criar a branch localmente e enviá-la para o repositório remoto no GitHub (git push -u origin <nome-da-branch>)."

5. Gestão de Colaboradores e Permissões no GitHub
Prompt:
"Como adicionar membros de uma equipe como colaboradores em um repositório no GitHub? Forneça o passo a passo nas configurações de acesso (Manage access / Collaborators) do repositório no site do GitHub e explique como os convidados devem aceitar o convite."
  
