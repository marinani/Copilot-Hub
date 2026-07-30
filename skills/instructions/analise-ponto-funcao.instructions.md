---
applyTo: '**'
description: 'Análise de Pontos de Função (ou Function Point Analysis) para medição do tamanho funcional de um software a partir da visão do usuário'
---

## 🖥️ Análise de Pontos de Função (APF) em TI

A Análise de Pontos de Função (APF) é um método padronizado para **medir o tamanho funcional de um software** a partir da perspectiva do **usuário**.

Sua principal meta é medir **o que** o software faz (as funcionalidades), e não **como** ele foi construído (linhas de código, linguagem de programação). A unidade de medida resultante é o **Ponto de Função (PF)**.

### 🎯 Objetivos Principais da APF

1. **Estimativa:** Fornecer uma base objetiva para estimar o **esforço**, o **custo** e o **tempo** necessários para desenvolver ou manter um software.
2. **Produtividade:** Medir a produtividade de equipes de desenvolvimento comparando a quantidade de Pontos de Função entregues com o esforço investido (horas/pessoa).
3. **Contrato:** Ser a métrica para precificação e gerenciamento de contratos de desenvolvimento e manutenção de software.
4. **Comparação:** Permitir a comparação entre diferentes projetos, tecnologias e organizações de forma consistente.

---

### ⚙️ Como Funciona o Processo de APF

O processo de contagem de Pontos de Função é detalhado e segue regras estritas estabelecidas por organizações como o **IFPUG** (*International Function Point Users Group*). Ele se baseia na identificação e classificação dos **Requisitos Funcionais do Usuário** em cinco tipos principais de funções.

#### 1. Classificação das Funções

As funcionalidades são divididas em dois grupos principais: **Funções de Dados** e **Funções Transacionais**.

| Grupo                     | Tipo de Função                         | Descrição                                                                                                                                                                                                      |
|:--------------------------|:---------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Funções de Dados**      | **Arquivo Lógico Interno (ALI)**       | Arquivos de dados mantidos **dentro** da aplicação (ex: as tabelas de dados que a aplicação grava/lê, como Clientes, Produtos, etc.).                                                                          |
|                           | **Arquivo de Interface Externa (AIE)** | Arquivos de dados mantidos **por outra** aplicação, mas que são referenciados/lidos pela aplicação que está sendo medida (ex: dados de um sistema de RH que são lidos pelo seu sistema de Folha de Pagamento). |
| **Funções Transacionais** | **Entrada Externa (EE)**               | Processos que recebem dados ou informações de controle de fora da aplicação e **atualizam** um Arquivo Lógico Interno (ex: tela de "Cadastro de Novo Cliente").                                                |
|                           | **Saída Externa (SE)**                 | Processos que enviam dados ou informações de controle para fora da aplicação, geralmente com lógica de processamento ou cálculo (ex: um relatório complexo com cálculo de impostos).                           |
|                           | **Consulta Externa (CE)**              | Processos que recuperam e enviam dados para fora, **sem** lógica de cálculo ou atualização de dados internos (ex: tela de "Consulta de Clientes" simples).                                                     |

#### 2. Determinação da Complexidade

Para cada uma das cinco funções identificadas, o analista atribui um grau de complexidade: **Simples**, **Média** ou **Complexa**. Essa classificação é feita com base:

* No número de **Tipos de Dados (TDs)**: Campos únicos reconhecidos pelo usuário.
* No número de **Tipos de Registro (TRs)**: Subgrupos de dados reconhecidos pelo usuário.

#### 3. Cálculo dos Pontos de Função Não-Ajustados (PFNA)

A complexidade de cada função é então multiplicada por um peso pré-definido pelo IFPUG para gerar os Pontos de Função Não-Ajustados (PFNA).

$$PFNA = \sum (\text{Número de Funções de um Tipo} \times \text{Peso de Complexidade})$$

#### 4. Cálculo do Fator de Ajuste (FA)

O resultado PFNA é então ajustado por um fator de ajuste (FA) para levar em conta características gerais do sistema, como desempenho, reusabilidade e facilidade de operação. O FA é baseado na avaliação de 14 **Características Gerais do Sistema (CGS)**.

#### 5. Cálculo Final dos Pontos de Função (PF)

O resultado final, que representa o tamanho funcional do software, é obtido pela fórmula:

$$PF = PFNA \times \text{Fator de Ajuste (FA)}$$

O valor final em **Pontos de Função (PF)** é o que será usado para planejar, estimar e gerenciar o projeto de software.

---

### 📊 Tabela de Pesos (Pontos de Função Não-Ajustados - PFNA)

O peso atribuído a cada função (em Pontos de Função) é definido conforme a metodologia do **IFPUG** (*International Function Point Users Group*):

#### 1. Pesos para Funções de Dados

| Tipo de Função                         | Complexidade Baixa | Complexidade Média | Complexidade Alta |
|:---------------------------------------|:-------------------|:-------------------|:------------------|
| **Arquivo Lógico Interno (ALI)**       | 7 PF               | 10 PF              | 15 PF             |
| **Arquivo de Interface Externa (AIE)** | 5 PF               | 7 PF               | 10 PF             |

**O que determina a Complexidade (Baixa, Média, Alta) de um ALI ou AIE?**

A complexidade é determinada cruzando-se:

* **DERs (Dados Elementares Referenciados):** o número de campos (atributos) únicos reconhecidos pelo usuário no arquivo.
* **RLRs (Registros Lógicos Referenciados):** o número de subgrupos de dados (sub-registros ou relacionamentos) reconhecidos pelo usuário.

#### 2. Pesos para Funções Transacionais

| Tipo de Função            | Complexidade Baixa | Complexidade Média | Complexidade Alta |
|:--------------------------|:-------------------|:-------------------|:------------------|
| **Entrada Externa (EE)**  | 3 PF               | 4 PF               | 6 PF              |
| **Saída Externa (SE)**    | 4 PF               | 5 PF               | 7 PF              |
| **Consulta Externa (CE)** | 3 PF               | 4 PF               | 6 PF              |

**O que determina a Complexidade (Baixa, Média, Alta) de uma EE, SE ou CE?**

A complexidade é determinada cruzando-se:

* **DERs (Dados Elementares Referenciados):** o número de campos únicos que entram, saem ou são validados.
* **ALRs (Arquivos Lógicos Referenciados):** o número de ALIs e AIEs referenciados/lidos pela transação.

---

### 🔄 Fluxo de Cálculo Simplificado

1. **Identificar as Funções:** Listar todos os ALIs, AIEs, EEs, SEs e CEs com base nos requisitos.
2. **Determinar a Complexidade:** Para cada função, classificar a complexidade (Baixa, Média ou Alta) usando as regras de DERs e RLRs/ALRs.
3. **Aplicar os Pesos:** Multiplicar o número de funções de um determinado tipo e complexidade pelo seu peso correspondente na tabela (ex: 5 EEs Médias x 4 PF = 20 PF).
4. **Somar para PFNA:** Somar todos os resultados para obter o **Total de Pontos de Função Não-Ajustados (PFNA)**.
5. **Aplicar o Ajuste:** O PFNA é então ajustado pelo **Fator de Ajuste (FA)** para chegar ao número final de Pontos de Função (PF).

O uso dessas tabelas garante que a medição do tamanho do software seja padronizada e objetiva.

---

### 📈 Exemplos de Estimativa

Estimar o tamanho funcional de um software usando a Análise de Pontos de Função (APF) envolve a análise dos seus componentes (Funções de Dados e Funções Transacionais) e a atribuição de complexidade para determinar os Pontos de Função Não-Ajustados (PFNA).

#### Premissas Adotadas

| Tipo de Contagem                               | Detalhe                                                        |
|:-----------------------------------------------|:---------------------------------------------------------------|
| **DERs** (*Data Element Types*)                | Número de campos (atributos) únicos reconhecidos pelo usuário. |
| **RLRs/ALRs** (*Record/File Types Referenced*) | Número de relacionamentos ou arquivos referenciados.           |
| **Peso do PFNA**                               | Utiliza-se a tabela de pesos padrão do IFPUG.                  |

#### 1. Exemplo: Criação de um Cadastro Básico de Cliente

**Cenário:** Uma tela simples para cadastrar, consultar e visualizar informações básicas de um cliente, sem relacionamentos complexos com outros módulos ou cálculos.

##### Análise Funcional

| Tipo de Função          | Descrição                                   | DERs                                       | RLRs/ALRs               | Complexidade | Peso PF | Contagem (PF)             |
|:------------------------|:--------------------------------------------|:-------------------------------------------|:------------------------|:-------------|:--------|:--------------------------|
| **Função de Dado**      | **ALI** - Cadastro de Clientes              | 10 (Nome, CPF, Endereço, Telefone, E-mail) | 1 (Registro de Cliente) | Baixa        | 7       | $1 \times 7 = \mathbf{7}$ |
| **Função Transacional** | **EE** - Inclusão de Cliente                | 5 (Campos para cadastro)                   | 1 (ALI - Clientes)      | Baixa        | 3       | $1 \times 3 = \mathbf{3}$ |
| **Função Transacional** | **CE** - Consulta de Cliente (Visualização) | 5 (Campos exibidos)                        | 1 (ALI - Clientes)      | Baixa        | 3       | $1 \times 3 = \mathbf{3}$ |
| **Função Transacional** | **EE** - Alteração de Cliente               | 5 (Campos alterados)                       | 1 (ALI - Clientes)      | Baixa        | 3       | $1 \times 3 = \mathbf{3}$ |
| **Função Transacional** | **EE** - Exclusão de Cliente                | 1 (CPF/ID)                                 | 1 (ALI - Clientes)      | Baixa        | 3       | $1 \times 3 = \mathbf{3}$ |
| **PFNA Total**          | **(Soma de todos os componentes)**          |                                            |                         |              |         | **19 PFNA**               |

**Resultado:** A criação de um cadastro básico de cliente é estimada em **19 Pontos de Função Não-Ajustados**.

#### 2. Exemplo: Ordem de Serviço (Cadastro Complexo)

**Cenário:** Criação de uma Ordem de Serviço (OS) que requer várias validações, consulta a múltiplos arquivos de dados (Clientes e Produtos) e gera um registro financeiro. A tela tem processamento e regra de negócio complexa.

##### Análise Funcional

| Tipo de Função          | Descrição                                                      | DERs                                  | ALRs                                       | Complexidade | Peso PF | Contagem (PF)               |
|:------------------------|:---------------------------------------------------------------|:--------------------------------------|:-------------------------------------------|:-------------|:--------|:----------------------------|
| **Função de Dado**      | **ALI** - Ordem de Serviço                                     | 35 (Itens da OS, datas, status, etc.) | 3 (Cabeçalho, Itens de Serviço, Histórico) | Média        | 10      | $1 \times 10 = \mathbf{10}$ |
| **Função de Dado**      | **ALI** - Movimentação Financeira (criado pela OS)             | 15 (Valor, data, conta, etc.)         | 2 (Registro principal, parcela)            | Baixa        | 7       | $1 \times 7 = \mathbf{7}$   |
| **Função de Dado**      | **AIE** - Cadastro de Produtos (lido)                          | 10 (Nome, preço, estoque)             | 1 (Tabela Produtos externa)                | Média        | 7       | $1 \times 7 = \mathbf{7}$   |
| **Função Transacional** | **EE** - Inclusão da OS (com validação)                        | 15 (Campos de entrada)                | 3 (ALI-OS, ALI-Mov. Fin., AIE-Produtos)    | Alta         | 6       | $1 \times 6 = \mathbf{6}$   |
| **Função Transacional** | **SE** - Geração de Relatório de OS (com cálculos de impostos) | 25 (Campos + impostos)                | 3 (ALI-OS, ALI-Mov. Fin., AIE-Produtos)    | Alta         | 7       | $1 \times 7 = \mathbf{7}$   |
| **PFNA Total**          | **(Soma de todos os componentes)**                             |                                       |                                            |              |         | **37 PFNA**                 |

**Resultado:** A funcionalidade de Ordem de Serviço (que envolve dados e transações complexas) é estimada em **37 Pontos de Função Não-Ajustados**.

#### 3. Exemplo: Atualização de Cadastro

**Cenário:** O projeto exige a modificação de uma funcionalidade existente (a tela de "Alteração de Cliente" do Exemplo 1) para adicionar o campo "Preferências de Contato" (Telefone, E-mail, Ambos) e a lógica de validação.

##### Análise Funcional (Contagem de Melhoria)

Em projetos de melhoria, o foco é contar apenas o que foi adicionado, alterado ou excluído.

| Tipo de Função                 | Descrição                                             | Ação da Contagem                       |
|:-------------------------------|:------------------------------------------------------|:---------------------------------------|
| **ALI** - Cadastro de Clientes | Adição do campo "Preferências de Contato".            | A função **ALI** é **Alterada (CHG)**. |
| **EE** - Alteração de Cliente  | Adição de um campo na tela e nova regra de validação. | A função **EE** é **Alterada (CHG)**.  |

| Tipo de Função                | Contagem                           | Peso do PF (Complexidade)                                                                                                                                                                                                                 | Contagem (PF) |
|:------------------------------|:-----------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------|
| **ALI** - Clientes            | Alterado (CHG)                     | O peso do ALI original era Baixa (7 PF). A mudança é menor. Conta-se apenas a **funcionalidade afetada** pelo tamanho da mudança (normalmente 1/3, 1/2 ou o peso total dependendo da metodologia). Vamos contar 1 PF para o ALI alterado. | $\mathbf{1}$  |
| **EE** - Alteração de Cliente | Alterado (CHG)                     | O peso da EE original era Baixa (3 PF). A adição de um campo e uma validação simples mantém a complexidade Baixa. Conta-se 2 PF para a EE alterada.                                                                                       | $\mathbf{2}$  |
| **PFNA Total**                | **(Soma de todos os componentes)** |                                                                                                                                                                                                                                           | **3 PFNA**    |

**Resultado:** A **melhoria/atualização** da funcionalidade de Alteração de Cliente é estimada em **3 Pontos de Função Não-Ajustados** (EFP - *Enhancement Function Points*), refletindo apenas o esforço de mudança.

---

### 💡 Exemplo de Uso Simples

Se um sistema de cadastro simples for medido, ele pode ter:

* **1 ALI** (Tabela de Clientes)
* **1 EE** (Tela de Inclusão de Clientes)
* **1 CE** (Tela de Consulta de Clientes)

Cada uma é analisada, recebe uma complexidade (Simples, Média ou Complexa), e a pontuação de PF é calculada. Se o resultado for 35 PF, isso indica o tamanho funcional do projeto.
