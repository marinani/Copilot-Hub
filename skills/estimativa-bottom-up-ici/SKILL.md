---
name: estimativa-bottom-up
description: >
  Realiza estimativas de software do tipo Bottom-Up para o sistema Sigesguarda Pro.
  Analisa o codebase, a documentação de discovery e o histórico de estimativas anteriores
  para gerar estimativas detalhadas em horas por funcionalidade. Use quando o usuário
  pedir para "estimar", "estimativa", "quanto tempo leva", "calcular horas",
  "bottom-up", "estimativa bottom-up", "estimar demanda", "estimar requisição",
  "estimar chamado", "estimar redmine", "quantas horas", "esforço necessário",
  "prazo de entrega", "dimensionar esforço".
license: Complete terms in LICENSE.txt
---

# Estimativa de Software Bottom-Up — Sigesguarda Pro

Skill para realizar estimativas de software do tipo Bottom-Up, baseada na decomposição progressiva do trabalho em unidades pequenas e mensuráveis. Cada item é estimado individualmente e depois agregado em uma estimativa consolidada.

Para detalhes teóricos completos sobre a metodologia, consulte a [documentação de referência](./estimativa_bottom_up_software.md).

## Quando Usar Esta Skill

- O usuário solicita uma estimativa de esforço para uma demanda/requisição
- O usuário quer saber quantas horas uma funcionalidade levará
- É necessário gerar uma planilha de estimativa Bottom-Up formal
- O usuário menciona um número de requisição/chamado do Redmine
- O usuário descreve uma melhoria ou nova funcionalidade e quer saber o prazo

## Pré-requisitos

Antes de estimar, você DEVE ter acesso a:

1. **Descrição clara da solicitação** — obtida do usuário, de um chamado Redmine, ou de um documento de escopo
2. **Documentação do sistema** — pasta `/documentacao/discovery` na raiz do repositório
3. **Histórico de estimativas** — pasta `.github/skills/estimativa-bottom-up-ici/base-conhecimento/` (arquivos `.md`)
4. **Código-fonte** — pasta `/Fontes` para análise de impacto técnico

## Workflow de Estimativa

Siga rigorosamente estas etapas, na ordem apresentada.

### Etapa 1: Entender a Solicitação

1. Leia atentamente a descrição fornecida pelo usuário
2. Identifique os requisitos funcionais e não-funcionais implícitos
3. Faça perguntas de esclarecimento se a solicitação for ambígua
4. Documente premissas adotadas
5. **🔴 PERGUNTA OBRIGATÓRIA — Número do Chamado**: Caso o usuário ainda não tenha informado, pergunte:

   > *"Qual é o **número do chamado no service desk** (ex: Redmine, GLPI) referente a esta solicitação?"*

   Registre o número antes de prosseguir. **Esta pergunta é obrigatória e não deve ser omitida.**
   - Se o usuário fornecer o número: os arquivos gerados seguirão o padrão `ESTIMATIVA-[numero].md` / `Estimativa_[numero].md`
   - Se o usuário informar que **não há número** ou se recusar a fornecer: os arquivos serão gerados com nome baseado em descrição curta (`ESTIMATIVA-<descricao-curta>.md`), fora do padrão de rastreabilidade. Registre esta situação no Resumo da Estimativa como observação.

6. **🔴 PERGUNTA OBRIGATÓRIA — Homologação Assistida**: Pergunte ao usuário:

   > *"Esta estimativa incluirá **homologação assistida**? (acompanhamento presencial ou remoto do analista durante a validação pelo cliente em ambiente de homologação)"*

   Registre a resposta (SIM ou NÃO) antes de prosseguir. **Esta pergunta é obrigatória e não deve ser omitida.** Se a resposta for SIM, será acrescido **15% do subtotal** de horas ao final da estimativa como item de Homologação/Implantação.

### Etapa 2: Analisar o Sistema Atual

1. Consulte a documentação de discovery relevante em `/documentacao/discovery`:
   - **Catálogo de telas**: `TELA-CATALOGO.md` e arquivos `TELA-T0XX-*.md`
   - **Fluxos de negócio**: `FLUXO-F0XX-*.md`
   - **Mapa de dados**: `DADOS-05-MAPA-DADOS.md`, `DADOS-06-STATUS-E-TRANSICOES.md`
   - **Catálogo de serviços**: `EJB-CATALOGO.md` e `EJB-S0XX-*.md`
   - **Integrações**: `FLUXO-F005-Integracoes.md`
   - **Consolidação**: `consolidacao.md` e `consolidacao.json`
2. Identifique os Controllers, Services, Repositórios, Views e entidades que serão impactados
3. Analise o código-fonte existente quando necessário para entender a complexidade real
4. Mapeie dependências e integrações afetadas

### Etapa 3: Consultar o Histórico de Estimativas

1. Consulte a base de conhecimento em `.github/skills/estimativa-bottom-up-ici/base-conhecimento/` (arquivos `.md`)
2. Busque estimativas anteriores com escopo semelhante para usar como referência
3. Identifique padrões de horas para tipos de tarefa similares (CRUDs, integrações, relatórios, etc.)
4. Use o histórico para calibrar suas estimativas — evitando sub ou superestimação
5. Documente quais estimativas anteriores foram usadas como referência

### Etapa 4: Decompor em Funcionalidades

1. Quebre a solicitação em funcionalidades individuais e mensuráveis
2. Cada funcionalidade deve ser:
   - **Pequena**: entre 2h e 40h (se maior, decompor novamente)
   - **Verificável**: tem critério de aceite claro
   - **Implementável**: escopo técnico definido
   - **Testável**: pode ser validada independentemente
3. Classifique cada funcionalidade como:
   - **Novo**: funcionalidade inédita no sistema
   - **Melhoria**: alteração/ajuste em funcionalidade existente

### Etapa 5: Estimar Horas por Funcionalidade

Para cada funcionalidade, distribua as horas nos seguintes tipos de atividade, respeitando os percentuais máximos contratuais:

| Tipo de Atividade | Percentual Máximo | Descrição |
|---|---|---|
| **Engenharia de Requisitos** | 40% | Levantamento, negociação, prototipação, documentação, verificação e validação |
| **Implementação** | 75% | Estudo técnico e codificação |
| **Teste** | 20% | Casos de teste, testes manuais/automatizados, regressivos, relatório |
| **Homologação/Implantação** | 15% | **Condicional** — Incluir **somente se** o usuário confirmou homologação assistida na Etapa 1. Neste caso, calcular `Subtotal × 15%` e adicionar como linha separada ao final da tabela, abaixo do subtotal. |
| **Cientista de Dados** | 10% | BI, IA, IoT (quando aplicável) |

**Regras de estimativa:**
- Os percentuais são referência máxima por item, não totais fixos
- Nem todos os tipos de atividade são obrigatórios — use conforme a demanda
- Se um tipo exceder o percentual, justifique o motivo
- **Homologação assistida**: se confirmada na Etapa 1, adicione uma linha de Homologação/Implantação ao final da tabela com valor = `Subtotal × 15%` (arredondado para cima para múltiplo de 0,5h). O **Total Geral** deve refletir Subtotal + Homologação
- Use a técnica PERT quando houver incerteza: `E = (O + 4M + P) / 6`
- Considere fatores de complexidade: integrações externas (+20%), ambiente legado (+40%), requisitos instáveis (+30%)

### Etapa 6: Gerar o Resultado

A estimativa gera **dois arquivos**:

**Arquivo 1 — Estimativa formal** (para o solicitante):
- Salvar em `estimativas-bottom-up/` na raiz do repositório
- **Nomenclatura (depende do número do chamado informado na Etapa 1):**
  - ✅ Com número: `ESTIMATIVA-[numero].md` (ex: `ESTIMATIVA-1234.md`) — padrão de rastreabilidade
  - ⚠️ Sem número: `ESTIMATIVA-<descricao-curta>.md` (ex: `ESTIMATIVA-ajuste-botao-156.md`) — fora do padrão, registrar como observação no Resumo
- Conteúdo segue o formato de saída detalhado abaixo

**Arquivo 2 — Retroalimentação da base de conhecimento**:
- Salvar em `.github/skills/estimativa-bottom-up-ici/base-conhecimento/`
- **Nomenclatura (depende do número do chamado informado na Etapa 1):**
  - ✅ Com número: `Estimativa_[numero].md` (ex: `Estimativa_1234.md`) — padrão de rastreabilidade
  - ⚠️ Sem número: `Estimativa_<descricao-curta>.md` (ex: `Estimativa_ajuste-botao-156.md`) — fora do padrão, registrar como observação no arquivo
- Conteúdo inclui **todas as seções do Arquivo 1** (Escopo, Tabela de Estimativa e Resumo) **mais** uma seção adicional de **Plano de Implementação** em formato to-do list detalhado (ver formato abaixo)
- Este arquivo alimenta o histórico consultado na Etapa 3 de estimativas futuras **e serve como guia de execução** quando a requisição for assumida por um desenvolvedor

**Formato do Arquivo 2 — Seção adicional: Plano de Implementação**

Após o Resumo da Estimativa, adicione a seguinte seção ao final do arquivo da base de conhecimento:

```markdown
## Plano de Implementação

> Este plano detalha as tarefas técnicas de implementação na ordem recomendada de execução.
> Ao assumir esta requisição, marque cada item como concluído à medida que avançar.

### [Nome da Funcionalidade 1]

- [ ] Levantar e validar requisitos com o solicitante
- [ ] Identificar os arquivos/componentes impactados
- [ ] [Tarefa técnica específica A — descrita em linguagem clara]
- [ ] [Tarefa técnica específica B]
- [ ] Escrever e executar testes para esta funcionalidade
- [ ] Validar resultado com o solicitante

### [Nome da Funcionalidade 2]

- [ ] [Tarefa técnica específica A]
- [ ] [Tarefa técnica específica B]
- [ ] Escrever e executar testes para esta funcionalidade
- [ ] Validar resultado com o solicitante

### Encerramento

- [ ] Executar testes regressivos nas funcionalidades adjacentes
- [ ] Atualizar documentação interna (se aplicável)
- [ ] Preparar ambiente para homologação (se homologação assistida confirmada)
- [ ] Registrar conclusão no chamado/Redmine
```

**Regras para o Plano de Implementação:**
- Cada `###` agrupa as tarefas de **um item** da tabela de estimativa — use o mesmo nome da coluna **Funcionalidade**
- As tarefas devem ser **acionáveis e granulares**: cada item deve poder ser concluído em uma única sessão de trabalho
- Inclua tarefas de análise, implementação, teste e validação para cada funcionalidade, conforme as horas estimadas
- Tarefas técnicas podem usar linguagem técnica (nomes de arquivos, classes, métodos) pois este arquivo é lido pelo desenvolvedor, não pelo cliente
- A seção **Encerramento** é obrigatória e sempre aparece ao final

Após salvar ambos os arquivos, informe os caminhos completos gerados e prossiga OBRIGATORIAMENTE para a **Etapa 6.5**.

### Etapa 6.5: Gerar Planilha XLSX (Obrigatório Perguntar)

⚠️ **OBRIGATÓRIO**: Ao concluir a Etapa 6, você DEVE SEMPRE fazer a pergunta abaixo. **Nunca omita esta pergunta.**

> **"Deseja gerar a planilha XLSX de estimativa Bottom-Up (formato .xlsx compatível com Excel)?"**

**Se a resposta for SIM**, execute o seguinte processo:

#### 6.5.1 — Montar o JSON de dados

Construa um objeto JSON com todos os dados da estimativa gerada, seguindo o schema abaixo:

```json
{
  "cliente":           "<nome do cliente, ex: PMC>",
  "orgao":             "<órgão, ex: SMDT>",
  "sistema":           "<nome do sistema, ex: Sigesguarda Pro>",
  "requisicao":        "<número do chamado ou descrição curta>",
  "sgc":               "<identificador SGC ou string vazia>",
  "analista":          "<nome do analista responsável>",
  "tecnologia":        "<tecnologia, ex: DotNet>",
  "data_estimativa":   "<data no formato DD/MM/AAAA>",
  "escopo":            "<texto do escopo da estimativa>",
  "material_apoio":    "<documentos utilizados, ex: RDM 1234>",
  "homologacao_horas": <horas de homologação como número, ex: 4.5 (0 se não aplicável)>,
  "implantacao_horas": <horas de implantação como número, ex: 0>,
  "itens": [
    {
      "item_rdm":       "<número do item, ex: 1>",
      "funcionalidade": "<nome da funcionalidade>",
      "requisito":      "<identificador do requisito, ex: REQ001 - Nome>",
      "tipo":           "<Melhoria ou Novo>",
      "descricao":      "<descrição da funcionalidade>",
      "eng_req":        <horas de engenharia de requisitos, número>,
      "impl":           <horas de implementação, número>,
      "teste":          <horas de teste, número>,
      "ds":             <horas de cientista de dados, número>
    }
  ]
}
```

Salve o JSON em `estimativas-bottom-up/` com nome `ESTIMATIVA-<identificador>.json`.

#### 6.5.2 — Executar o script Python

Execute o script de geração da planilha:

```powershell
$json  = "C:\<caminho-raiz>\estimativas-bottom-up\ESTIMATIVA-<identificador>.json"
$xlsx  = "C:\<caminho-raiz>\estimativas-bottom-up\Estimativa_<identificador>.xlsx"
$skill = "C:\<caminho-raiz>\.github\skills\estimativa-bottom-up-ici\gerar_planilha_estimativa.py"
py $skill --dados $json --saida $xlsx
```

> **Importante:** Substitua `<caminho-raiz>` pelo caminho absoluto real da raiz do workspace.

> **Dependência:** O script requer `openpyxl`. Caso não esteja instalado, execute antes: `py -m pip install openpyxl`

#### 6.5.3 — Confirmar a geração

Após executar o script:
1. Verifique se o arquivo foi criado com `Test-Path "$xlsx"`
2. Informe ao usuário o caminho completo do XLSX gerado
3. Mencione que a planilha está pronta para ser usada como anexo formal da estimativa

**Se a resposta for NÃO**, registre que o usuário optou por não gerar o XLSX e prossiga para a Etapa 7.

---

**🔴 REGRA OBRIGATÓRIA: Ao concluir a Etapa 6.5, você DEVE SEMPRE perguntar ao usuário se deseja gerar o PDF. Esta pergunta é obrigatória e não deve ser omitida.**

O conteúdo do arquivo formal DEVE seguir EXATAMENTE o formato abaixo.

---

## Formato de Saída Obrigatório

### 1. Escopo da Estimativa

Texto narrativo que explica:
- O que foi solicitado
- O que será implementado
- O comportamento atual vs. o novo comportamento esperado
- Premissas adotadas
- Restrições identificadas

> **🔵 LINGUAGEM OBRIGATÓRIA — Escopo e Funcionalidades:** O texto do escopo e os nomes/descrições das funcionalidades na tabela devem ser escritos em **linguagem simples e não técnica**, acessível ao cliente/gestor que aprovará a estimativa. Evite termos de código, nomes de classes, métodos, endpoints, tabelas de banco de dados ou arquivos internos do sistema. Descreva o que o usuário vê e faz, não o que o código executa.
>
> Exemplos:
> - ❌ Técnico: *"Ajustar o método `SalvarAtendimento()` no `AtendimentoService` para persistir o campo `DataFechamento` na tabela `Atendimentos`"*
> - ✅ Simples: *"Registrar automaticamente a data e hora em que o atendimento foi encerrado"*
>
> - ❌ Técnico: *"Corrigir a query no repositório que faz JOIN com `ProtocolosLidos` retornando registros duplicados"*
> - ✅ Simples: *"Corrigir a exibição da lista de protocolos que mostrava itens repetidos"*

**Exemplo de escopo:**

> Esta solicitação tem como objetivo alterar o comportamento do botão "Marcar como lido e tramitar via 156", presente no modal de detalhes de protocolo da tela de Monitoramento (_ModalProtocolo156.cshtml). Atualmente, ao clicar nesse botão, o sistema registra o protocolo como lido na base de dados local (tabela ProtocolosLidos) e o move para a aba "Protocolos lidos", sem nenhuma interação com a API externa do SIAC 156.
>
> O novo comportamento exige que, ao clicar no botão, seja aberta a modal de Devolução 156 (_ModalDevolucao156.cshtml) para que o operador informe o motivo e a observação — e o protocolo seja efetivamente devolvido à central 156 via API externa, sem que o operador precise antes "assumir" o chamado e criar um atendimento formal.

### 2. Tabela de Estimativa

> **Instrução de formatação:** Ao escrever a tabela no arquivo `.md`, alinhe as colunas com espaços para que fiquem visualmente legíveis mesmo em editores de texto simples. Use o formato abaixo como referência, ajustando a largura de cada coluna ao conteúdo real.

```markdown
| Item | Funcionalidade                     | Tipo     | Descrição da Funcionalidade                                                                         | Eng. Req. | Impl. | Teste | Total |
|------|------------------------------------|----------|-----------------------------------------------------------------------------------------------------|-----------|-------|-------|-------|
| 1    | Análise e planejamento             | Melhoria | Levantamento dos requisitos, análise de impacto no código existente e documentação do escopo técnico |     4     |   0   |   0   |   4   |
| 2    | Alteração do endpoint X            | Melhoria | Ajustar o serviço para incluir a nova regra de negócio Y                                            |     0     |   8   |   2   |  10   |
| 3    | Nova tela de cadastro Z            | Novo     | Criar tela de cadastro com campos A, B, C e validações                                              |     2     |  12   |   3   |  17   |
| **Subtotal** |                           |          |                                                                                                     |   **6**   | **20**| **5** | **31**|
| *Homologação Assistida* |            |          | *Condicional — incluir somente se confirmado na Etapa 1 (15% do Subtotal = 31 × 15% ≈ 5h)*          |           |       |       |  *5*  |
| **Total Geral** |                     |          |                                                                                                     |           |       |       | **36**|
```

> **Nota sobre a linha de Homologação Assistida:** Inclua-a somente se o usuário respondeu SIM na Etapa 1. Quando NÃO houver homologação assistida, omita essa linha e o **Total Geral** será igual ao **Subtotal**.

**Regras de formatação da tabela:**
- Cabeçalho com separadores `---` alinhados à largura de cada coluna
- Coluna **Descrição** pode ser longa — mantenha-a descritiva, mas objetiva (máx. ~120 caracteres por célula)
- Coluna **Descrição** e coluna **Funcionalidade** devem usar **linguagem simples e não técnica** — descreva o que o usuário percebe ou realiza, não implementações internas (sem nomes de classes, métodos, tabelas ou arquivos)
- Colunas numéricas (Eng. Req., Impl., Teste, Total) centralizadas com espaços
- Linha de **Subtotal** com valores em negrito `**valor**`
- Linha de *Homologação Assistida* em itálico, condicional (ver Etapa 1)
- Linha de **Total Geral** com valor final em negrito
- Linha de separação `---` após o cabeçalho deve cobrir toda a largura da célula

### 3. Resumo da Estimativa

Ao final, apresente:

- **Subtotal de horas**: soma de todos os itens funcionais
- **Homologação assistida**: informar se foi confirmada pelo usuário (SIM/NÃO) e o valor em horas acrescentado (se SIM: Subtotal × 15%)
- **Total Geral de horas**: Subtotal + Homologação (quando aplicável)
- **Estimativas de referência utilizadas**: listar requisições do histórico consultadas
- **Premissas**: listar premissas adotadas
- **Riscos identificados**: fatores que podem impactar a estimativa
- **Observações**: considerações adicionais relevantes

### Etapa 7: Gerar PDF para Aprovação (Obrigatório Perguntar)

⚠️ **OBRIGATÓRIO**: Ao concluir a Etapa 6, você DEVE SEMPRE fazer a pergunta abaixo. **Nunca omita esta pergunta.**

**Pergunta que DEVE ser feita:**

> **"Deseja gerar um arquivo PDF formatado da estimativa para enviar para aprovação?"**

**Se a resposta for SIM**, execute o seguinte processo:

#### 7.1 — Preparar o HTML a partir do template

1. Leia o template em `.github/skills/estimativa-bottom-up-ici/template-estimativa.html`
2. Substitua **todos** os marcadores `{{PLACEHOLDER}}` pelos dados da estimativa gerada:

| Marcador | Valor a usar |
|----------|--------------|
| `{{TITULO}}` | Título curto da estimativa |
| `{{VERSAO}}` | `1.3` |
| `{{CLIENTE}}` | Cliente (ex: `PMC`) |
| `{{ORGAO}}` | Órgão (ex: `SMDT`) |
| `{{SISTEMA}}` | Sistema (ex: `Sigesguarda Pro`) |
| `{{REQUISICAO}}` | Número da requisição ou `—` |
| `{{SGC}}` | Identificador SGC ou `—` |
| `{{ANALISTA}}` | Nome do analista responsável |
| `{{TECNOLOGIA}}` | Tecnologia (ex: `DotNet`) |
| `{{DATA_ESTIMATIVA}}` | Data atual no formato `DD/MM/AAAA` |
| `{{ESCOPO_HTML}}` | Texto do escopo com formatação HTML (`<strong>`, `<em>`, `<br>`) |
| `{{ITEM_N}}`, `{{ITEM_FUNC}}`, etc. | Dados de cada item — repita o bloco `<tr>` de item do template para cada linha |
| `{{TOTAL_ENG}}`, `{{TOTAL_IMPL}}`, `{{TOTAL_TESTE}}`, `{{TOTAL_DS}}`, `{{TOTAL_HORAS}}` | Totais de horas por tipo de atividade |
| `{{DISTRIB_ENG}}`, `{{DISTRIB_IMPL}}`, `{{DISTRIB_TESTE}}`, `{{DISTRIB_DS}}` | Percentuais de distribuição (ex: `11,76%`) |
| `{{HOMO_HORAS}}` | Horas de homologação ou `0:00` |
| `{{IMPL_HORAS}}` | Horas de implantação ou `0:00` |
| `{{GRAND_TOTAL}}` | Total geral da estimativa |
| `{{RODAPE_ANALISTA}}` | Nome do analista para o rodapé |
| `{{RODAPE_DATA}}` | Data atual para o rodapé |
| `{{RODAPE_SISTEMA}}` | Sistema para o rodapé |

3. Para cada item da estimativa, copie o bloco `<tr>` de item do template e preencha os marcadores correspondentes. Remova o bloco de exemplo original.
4. Salve o HTML preenchido em `estimativas-bottom-up/` com o mesmo nome base da estimativa, extensão `.html`:
   - Exemplo: `estimativas-bottom-up/ESTIMATIVA-RDM-1234.html`

#### 7.2 — Gerar o PDF via Chrome headless

Execute o seguinte comando PowerShell para converter o HTML em PDF:

```powershell
$html = "file:///C:/caminho/completo/estimativas-bottom-up/ESTIMATIVA-<identificador>.html"
$pdf  = "C:\caminho\completo\estimativas-bottom-up\ESTIMATIVA-<identificador>.pdf"
$chr  = "C:\Program Files\Google\Chrome\Application\chrome.exe"
& $chr --headless --disable-gpu --print-to-pdf="$pdf" --print-to-pdf-no-header --no-margins $html
```

> **Importante:** Substitua `/C:/caminho/completo/` pelo caminho absoluto real da raiz do workspace. O arquivo HTML deve existir antes de executar o comando.

> **⚠️ Cabeçalho e rodapé do navegador:** O flag `--print-to-pdf-no-header` é **obrigatório** e suprime todos os elementos inseridos automaticamente pelo Chrome ao imprimir uma página: data, horário, URL do arquivo, título da página e números de página. O flag `--no-margins` remove as margens extras que o Chrome adiciona ao redor do conteúdo. **Nunca remova esses flags** — sem eles, essas informações aparecem no PDF gerado e comprometem a apresentação formal do documento.
>
> **⚠️ Versão do Chrome:** O flag `--headless=old` foi **removido no Chrome 132** (janeiro de 2025). Use apenas `--headless` (modo padrão atual). Se o Chrome não estiver em `C:\Program Files\Google\Chrome\Application\chrome.exe`, ajuste o caminho em `$chr`.

#### 7.3 — Confirmar a geração

Após executar o comando:
1. Verifique se o PDF foi criado com `Test-Path "$pdf"`
2. Informe ao usuário o caminho completo do PDF gerado
3. Mencione que o arquivo está pronto para ser enviado para aprovação

**Se a resposta for NÃO**, registre que o usuário optou por NÃO gerar o PDF, mas confirme que a opção estava disponível.

### Etapa 8: Gerar Texto para Preenchimento no Service Desk

⚠️ **OBRIGATÓRIO**: Execute sempre após a Etapa 7, independentemente de o PDF ter sido gerado ou não.

Colete as seguintes informações do usuário (as que ainda não foram fornecidas durante a conversa):

1. **Data Início**: data prevista para início da implementação (formato `DD/MM/AAAA`)
2. **Data Fim**: data prevista para conclusão do desenvolvimento (formato `DD/MM/AAAA`)
3. **Data Prazo Homologação**: data limite para o cliente validar em ambiente de homologação (formato `DD/MM/AAAA`)
4. **Dias para Disponibilizar em Produção**: número de dias corridos após a homologação para publicar em produção (ex: `2`)

**Cálculos automáticos antes de gerar o texto:**

| Campo calculado | Fórmula |
|---|---|
| **Data Fim Prevista** | Data Prazo Homologação + Dias para Disponibilizar em Produção (dias corridos) |
| **Distribuição de horas por mês** | Distribua o Total Geral de horas proporcionalmente entre os meses cobertos pelo período Data Início → Data Fim, usando dias corridos de cada mês como critério de rateio. Se o período for integralmente dentro de um único mês calendário, inclua apenas uma linha de mês. |

**Texto gerado (copiar e colar no service desk):**

```
+---------------------------------------------------------------------------+
| Total de Horas: [TOTAL_GERAL]h                                            |
|        [Mês 1/Ano]: [HORAS_MES_1]h                                       |
|        [Mês 2/Ano]: [HORAS_MES_2]h  ← incluir somente se houver >1 mês  |
+---------------------------------------------------------------------------+
| Datas Previstas:                                                          |
|       Data Início: [DATA_INICIO]                                          |
|       Data Prazo Homologação: [DATA_PRAZO_HOMO]                           |
|       Data Fim Prevista: [DATA_FIM_PREVISTA]                              |
+---------------------------------------------------------------------------+
| Quantidade de Entregas Parciais: 0                                        |
| Dias Para Disponibilizar em PRODUÇÃO: [DIAS_PRODUCAO]                     |
+---------------------------------------------------------------------------+
| Estimativa Pontua: [a preencher com o link do Pontua]                     |
+---------------------------------------------------------------------------+
```

**Regras de preenchimento dos marcadores:**

| Marcador | Valor |
|---|---|
| `[TOTAL_GERAL]` | Total Geral de horas da estimativa |
| `[Mês N/Ano]` / `[HORAS_MES_N]` | Para cada mês calendário entre Data Início e Data Fim, inclua uma linha `Mês N/Ano: Xh`. Ex: `Jun/2026: 8h`, `Jul/2026: 2h` |
| `[DATA_INICIO]` | Data informada pelo usuário (`DD/MM/AAAA`) |
| `[DATA_PRAZO_HOMO]` | Data informada pelo usuário (`DD/MM/AAAA`) |
| `[DATA_FIM_PREVISTA]` | Data Prazo Homologação + Dias para Disponibilizar em Produção (`DD/MM/AAAA`) |
| `[DIAS_PRODUCAO]` | Número informado pelo usuário |
| `[a preencher com o link do Pontua]` | Deixar como placeholder — o usuário preencherá após registrar no Pontua |

---

✅ **Resumo das Etapas Obrigatórias:**
1. ✅ Etapa 1: Entender a solicitação + **OBRIGATÓRIO perguntar sobre número do chamado** (registrar número ou indicar ausência) + **OBRIGATÓRIO perguntar sobre homologação assistida** (registrar SIM/NÃO antes de prosseguir)
2. ✅ Etapa 2: Analisar o sistema
3. ✅ Etapa 3: Consultar histórico
4. ✅ Etapa 4: Decompor funcionalidades
5. ✅ Etapa 5: Estimar horas (acrescentar 15% de Homologação ao Subtotal se resposta da Etapa 1 foi SIM)
6. ✅ Etapa 6: Gerar resultado (gerar arquivos .md)
7. ✅ **Etapa 6.5 (OBRIGATÓRIO): SEMPRE perguntar sobre planilha XLSX — se SIM, montar JSON e executar script Python; se NÃO, confirmar recusa**
8. ✅ **Etapa 7 (OBRIGATÓRIO): SEMPRE perguntar sobre PDF — se SIM, gerar PDF; se NÃO, confirmar recusa**
9. ✅ **Etapa 8 (OBRIGATÓRIO): Coletar datas, calcular campos automáticos e gerar texto formatado para o service desk**

---

## Diretrizes de Qualidade

- **Precisão**: Decomponha até o nível mais granular possível. Tasks entre 2h e 16h são ideais.
- **Rastreabilidade**: Cada item da tabela deve ser verificável e independente.
- **Consistência**: Use o histórico de estimativas para manter coerência com estimativas anteriores.
- **Transparência**: Documente todas as premissas e incertezas.
- **Conservadorismo**: Na dúvida, estime para cima. Melhor sobrar tempo do que faltar.

## Referências

- [Documentação de referência Bottom-Up](./estimativa_bottom_up_software.md) — teoria completa da metodologia
- [Template HTML da estimativa](./template-estimativa.html) — base para geração do PDF na Etapa 7
- `/documentacao/discovery/` — documentação de discovery do Sigesguarda Pro
- `.github/skills/estimativa-bottom-up-ici/base-conhecimento/` — base de conhecimento com estimativas históricas (arquivos `.md`)
- `/Fontes/` — código-fonte do sistema para análise de impacto