# Skill: Estimativa de Software Bottom-Up — Sigesguarda Pro

> **Geração automatizada de estimativas de esforço técnico com decomposição progressiva de trabalho.**

## Visão Geral

A **Skill de Estimativa Bottom-Up** é uma ferramenta que realiza estimativas de software do tipo **Bottom-Up**, baseada na decomposição progressiva do trabalho em unidades pequenas e mensuráveis. Ela analisa requisições, decompõe o escopo em funcionalidades, estima o esforço em horas para cada atividade técnica e gera documentos formatados (Markdown, XLSX, PDF) prontos para aprovação e execução.

### Características Principais

- ✅ Decomposição automática de requisições em funcionalidades
- ✅ Estimativa calibrada em horas (Engenharia de Requisitos, Implementação, Teste, etc.)
- ✅ Geração de documentação formal em Markdown
- ✅ Exportação para planilha XLSX (compatível com Excel)
- ✅ Geração de PDF formatado para aprovação
- ✅ Base de conhecimento histórica para calibração de estimativas futuras
- ✅ Plano de implementação detalhado (to-do list técnico)
- ✅ Integração com Redmine/Service Desk para rastreabilidade

---

## 📋 Quando Usar Esta Skill

Use a skill de estimativa Bottom-Up quando:

- Um usuário solicita estimativa de esforço para uma demanda (ex: "Quanto tempo leva para implementar X?")
- É necessário gerar uma proposta formal com breakdown de horas
- Uma requisição do Redmine/Service Desk precisa de estimativa técnica
- É necessário documentar o escopo, funcionalidades e plano de execução
- Um cliente solicita aprovação de cronograma e alocação de horas

### Exemplos de Acionamento

Procure por palavras-chave do usuário como:
- "estimar..." | "estimativa..." | "quanto tempo leva..."
- "quantas horas..." | "esforço necessário..."
- "bottom-up" | "calcular horas..."
- "redmine [numero]" | "chamado [numero]"
- "prazo de entrega" | "dimensionar esforço"

---

## 🛠️ Configuração na Máquina do Usuário

### Pré-requisitos Obrigatórios

Antes de usar a skill, certifique-se de que sua máquina atende aos seguintes requisitos:

#### 1. **Python 3.7+** com pip instalado

Verificar versão:
```powershell
python --version
```

Se Python não estiver instalado:
1. Baixe de: https://www.python.org/downloads/
2. Durante a instalação, **marque a opção "Add Python to PATH"**
3. Reinicie seu terminal/PowerShell

#### 2. **Biblioteca openpyxl** (para geração de XLSX)

Instalar:
```powershell
python -m pip install openpyxl
```

Verificar instalação:
```powershell
python -c "import openpyxl; print(openpyxl.__version__)"
```

#### 3. **Google Chrome** (para geração de PDF)

Verificar caminho padrão:
```powershell
Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

Se não encontrado:
1. Baixe Chrome de: https://www.google.com/intl/pt-BR/chrome/
2. Instale no local padrão
3. Verifique o caminho novamente

**Se Chrome está em local diferente**, você precisará ajustar o caminho no comando de geração de PDF (veja seção [Geração de PDF](#geração-de-pdf) abaixo).

#### 4. **Git** (para versionamento de estimativas)

Verificar instalação:
```powershell
git --version
```

Se não instalado, baixe de: https://git-scm.com/download/win

#### 5. **Editor de Markdown** (recomendado: VS Code)

Qualquer editor funciona, mas VS Code oferece preview de Markdown nativo:
- Download: https://code.visualstudio.com/
- Extensão recomendada: "Markdown Preview Enhanced"

### Estrutura de Diretórios Necessária

Após clonar o repositório, verifique se a seguinte estrutura está presente:

```
workspace-root/
├── .github/
│   └── skills/
│       └── estimativa-bottom-up-ici/              ← SkillFolder
│           ├── SKILL.md                            (arquivo de configuração da skill)
│           ├── README.md                           (este arquivo)
│           ├── estimativa_bottom_up_software.md    (documentação teórica)
│           ├── gerar_planilha_estimativa.py        (script Python para XLSX)
│           ├── template-estimativa.html            (template para PDF)
│           ├── base-conhecimento/                  (histórico de estimativas)
│           │   ├── Estimativa_XXXXX.md
│           │   ├── Estimativa_XXXXX.md
│           │   └── ... (mais arquivos)
│           └── logo_ici.png                        (logo para PDF)
├── documentacao/
│   └── discovery/                                  (documentação do sistema)
│       ├── TELA-CATALOGO.md
│       ├── FLUXO-F0XX-*.md
│       ├── DADOS-*.md
│       └── ... (mais arquivos)
├── Fontes/                                         (código-fonte do sistema)
│   └── ... (estrutura do projeto)
└── estimativas-bottom-up/                          (output: estimativas geradas)
    ├── ESTIMATIVA-XXXXX.md                        (arquivo formal em Markdown)
    ├── ESTIMATIVA-XXXXX.json                      (dados estruturados)
    ├── Estimativa_XXXXX.xlsx                      (planilha Excel)
    ├── ESTIMATIVA-XXXXX.html                      (versão HTML para PDF)
    └── ESTIMATIVA-XXXXX.pdf                       (documento PDF)
```

**Caso a pasta `estimativas-bottom-up/` não exista, crie-a manualmente:**

```powershell
New-Item -ItemType Directory -Path "C:\caminho\do\workspace\estimativas-bottom-up" -Force
```

---

## 🚀 Como Usar a Skill

### Fluxo Geral

A skill segue um workflow estruturado em **8 etapas obrigatórias**. Você não precisa executar nada manualmente — o agente IA guia todo o processo. Seu papel é:

1. **Descrever a requisição** ao agente IA
2. **Responder às perguntas obrigatórias** (número do chamado, homologação assistida, etc.)
3. **Validar o resultado** (revisar arquivos gerados)
4. **Aprovar** a estimativa para o cliente

### Etapa por Etapa

#### **Etapa 1: Entender a Solicitação**

O agente IA:
- Lê atentamente sua descrição
- Faz perguntas de esclarecimento (se necessário)

**Você DEVE responder a duas perguntas obrigatórias:**

1. **"Qual é o número do chamado no service desk?"**
   - Exemplo: `1234` (Redmine)
   - Se não existir número: responda `não há número` ou `sem número`

2. **"Esta estimativa incluirá homologação assistida?"**
   - Respostas aceitas: `SIM` ou `NÃO`
   - Homologação assistida = acompanhamento presencial/remoto do analista durante validação em ambiente de homologação

#### **Etapa 2: Análise do Sistema Atual**

O agente IA analisa automaticamente:
- Documentação de discovery em `/documentacao/discovery/`
- Catálogo de telas, fluxos, dados, serviços
- Mapa de integrações

Você não precisa fazer nada nesta etapa.

#### **Etapa 3: Histórico de Estimativas**

O agente IA consulta estimativas anteriores em `.github/skills/estimativa-bottom-up-ici/base-conhecimento/` para calibrar horas com base em padrões históricos.

Você não precisa fazer nada nesta etapa.

#### **Etapa 4: Decomposição em Funcionalidades**

O agente IA quebra a requisição em funcionalidades menores e mensuráveis.

Você pode revisar e sugerir ajustes no escopo se necessário.

#### **Etapa 5: Estimativa em Horas**

O agente IA estima horas para cada funcionalidade, distribuindo entre:
- **Engenharia de Requisitos** (máximo 40% do total)
- **Implementação** (máximo 75% do total)
- **Teste** (máximo 20% do total)
- **Homologação/Implantação** (15% do subtotal — condicional)
- **Cientista de Dados** (10% — se aplicável)

**Fórmula PERT (quando houver incerteza):**
```
E = (O + 4M + P) / 6
Onde: O = otimista, M = mais provável, P = pessimista
```

#### **Etapa 6: Gerar Resultado (Markdown)**

O agente IA gera **dois arquivos** automaticamente:

1. **Arquivo formal** (`ESTIMATIVA-[numero].md`)
   - Escopo em linguagem simples
   - Tabela de estimativa
   - Resumo com premissas e riscos

2. **Arquivo base de conhecimento** (`Estimativa_[numero].md`)
   - Mesmo conteúdo do arquivo 1
   - PLUS: Plano de Implementação (to-do list detalhado para o desenvolvedor)

#### **Etapa 6.5: Gerar Planilha XLSX (Opcional)**

O agente IA pergunta:
> **"Deseja gerar a planilha XLSX de estimativa?"**

**Se você responder SIM:**

1. O agente monta um JSON estruturado com os dados
2. Executa automaticamente o script Python:
   ```powershell
   python "C:\...\gerar_planilha_estimativa.py" --dados JSON_FILE --saida XLSX_FILE
   ```
3. Verifica se o arquivo foi criado
4. Informa o caminho completo do arquivo XLSX

**Se você responder NÃO:** O processo prossegue para a próxima etapa.

#### **Etapa 7: Gerar PDF para Aprovação (Opcional)**

O agente IA pergunta:
> **"Deseja gerar um arquivo PDF formatado da estimativa para envio de aprovação?"**

**Se você responder SIM:**

1. O agente preenche o template HTML (`.github/skills/estimativa-bottom-up-ici/template-estimativa.html`) com os dados
2. Executa o comando Chrome headless:
   ```powershell
   & "C:\Program Files\Google\Chrome\Application\chrome.exe" `
     --headless `
     --disable-gpu `
     --print-to-pdf="C:\...\ESTIMATIVA-XXXXX.pdf" `
     --print-to-pdf-no-header `
     --no-margins `
     "file:///C:/caminho/ESTIMATIVA-XXXXX.html"
   ```
3. Verifica se o PDF foi criado
4. Informa o caminho completo do PDF

**Se você responder NÃO:** O processo prossegue para a próxima etapa.

#### **Etapa 8: Gerar Texto para Service Desk**

O agente IA coleta as seguintes informações (se ainda não fornecidas):

1. **Data Início**: Data prevista para começar (ex: `01/07/2026`)
2. **Data Prazo Homologação**: Data limite para validação (ex: `15/07/2026`)
3. **Dias para Produção**: Dias corridos após homologação (ex: `2`)

O agente calcula automaticamente:
- **Data Fim Prevista** = Data Prazo Homologação + Dias para Produção
- **Distribuição de horas por mês** = proporcional aos dias corridos de cada mês

Gera um texto formatado pronto para copiar e colar no Redmine/Service Desk:

```
+---------------------------------------------------------------------------+
| Total de Horas: 36h                                                       |
|        Jul/2026: 20h                                                      |
|        Ago/2026: 16h                                                      |
+---------------------------------------------------------------------------+
| Datas Previstas:                                                          |
|       Data Início: 01/07/2026                                             |
|       Data Prazo Homologação: 15/07/2026                                  |
|       Data Fim Prevista: 17/07/2026                                       |
+---------------------------------------------------------------------------+
| Quantidade de Entregas Parciais: 0                                        |
| Dias Para Disponibilizar em PRODUÇÃO: 2                                   |
+---------------------------------------------------------------------------+
| Estimativa Pontua: [a preencher com o link do Pontua]                    |
+---------------------------------------------------------------------------+
```

---

## 📂 Estrutura de Arquivos Gerados

Depois que a skill executa, você encontrará os seguintes arquivos no diretório `estimativas-bottom-up/`:

### 1. Arquivo Markdown Formal

**Nome:** `ESTIMATIVA-[numero].md` (ex: `ESTIMATIVA-1234.md`)

**Conteúdo:**
- Escopo da estimativa (em linguagem simples)
- Tabela de horas por funcionalidade
- Resumo com totais, premissas, riscos, observações

**Uso:** Enviar para cliente/gestor para aprovação.

**Exemplo:**
```markdown
# Estimativa de Esforço — Requisição 1234

## Escopo da Estimativa

Esta solicitação tem como objetivo [...descrição do que será implementado...]

## Tabela de Estimativa

| Item | Funcionalidade | Tipo | Descrição | Eng. Req. | Impl. | Teste | Total |
|------|---|---|---|---|---|---|---|
| 1 | Análise e planejamento | Melhoria | [...] | 4 | 0 | 0 | 4 |
| 2 | Implementação de nova funcionalidade | Novo | [...] | 2 | 8 | 2 | 12 |
| **Subtotal** | | | | **6** | **8** | **2** | **16** |
| **Total Geral** | | | | | | | **16** |

## Resumo da Estimativa

- **Total de horas:** 16h
- **Homologação assistida:** Não
- **Premissas:** [...]
- **Riscos:** [...]
```

### 2. Arquivo Base de Conhecimento

**Nome:** `Estimativa_[numero].md` (ex: `Estimativa_1234.md`)

**Localização:** `.github/skills/estimativa-bottom-up-ici/base-conhecimento/`

**Conteúdo:**
- Mesmo conteúdo do arquivo 1
- PLUS: **Plano de Implementação** (to-do list técnico com tarefas granulares)

**Uso:** Arquivo de referência para estimativas futuras + guia de execução para o desenvolvedor.

### 3. Arquivo JSON (dados estruturados)

**Nome:** `ESTIMATIVA-[numero].json` (ex: `ESTIMATIVA-1234.json`)

**Conteúdo:** Dados estruturados da estimativa (cliente, órgão, itens, horas, etc.)

**Uso:** Entrada para o script Python de geração XLSX.

**Exemplo:**
```json
{
  "cliente": "PMC",
  "orgao": "SMDT",
  "sistema": "Sigesguarda Pro",
  "requisicao": "1234",
  "analista": "João Silva",
  "tecnologia": "DotNet",
  "data_estimativa": "01/07/2026",
  "homologacao_horas": 0,
  "implantacao_horas": 0,
  "itens": [
    {
      "item_rdm": "1",
      "funcionalidade": "Análise e planejamento",
      "tipo": "Melhoria",
      "descricao": "Levantamento dos requisitos...",
      "eng_req": 4,
      "impl": 0,
      "teste": 0,
      "ds": 0
    }
  ]
}
```

### 4. Planilha Excel (XLSX)

**Nome:** `Estimativa_[numero].xlsx` (ex: `Estimativa_1234.xlsx`)

**Conteúdo:**
- Headers com informações do projeto (cliente, órgão, sistema, analista, data)
- Tabela de estimativa com cores e formatação
- Cálculos de totais e distribuição percentual

**Uso:** Enviar para cliente como anexo formal + usar para acompanhamento de execução.

### 5. Arquivo HTML (intermediário para PDF)

**Nome:** `ESTIMATIVA-[numero].html` (ex: `ESTIMATIVA-1234.html`)

**Conteúdo:** Versão HTML do template preenchido com os dados.

**Uso:** Intermediário — gerado automaticamente e convertido para PDF. Pode ser aberto no navegador para visualizar.

### 6. PDF Formatado

**Nome:** `ESTIMATIVA-[numero].pdf` (ex: `ESTIMATIVA-1234.pdf`)

**Conteúdo:** Documento PDF formatado, pronto para envio ao cliente.

**Características:**
- Cabeçalho com logo e dados do projeto
- Tabela de estimativa com cores
- Cálculos de percentual e distribuição
- Rodapé com assinatura do analista

**Uso:** Documento oficial para aprovação do cliente.

---

## 🔧 Troubleshooting

### Problema: "Python não encontrado"

**Solução:**
1. Verifique instalação: `python --version`
2. Se não aparecer, adicione Python ao PATH do sistema
3. Reinicie o PowerShell após ajuste

### Problema: "openpyxl não está instalado"

**Solução:**
```powershell
python -m pip install --upgrade pip
python -m pip install openpyxl
```

### Problema: "Chrome não encontrado"

**Solução:**
1. Verifique caminho: `Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"`
2. Se não encontrado, instale Chrome de https://www.google.com/chrome
3. Se Chrome está em local diferente, ajuste o caminho no comando de geração de PDF

### Problema: "Erro ao gerar planilha XLSX"

**Solução:**
1. Verifique se o arquivo JSON foi criado corretamente
2. Teste manualmente: `python "C:\...\gerar_planilha_estimativa.py" --dados "C:\...\ESTIMATIVA-1234.json" --saida "C:\...\Estimativa_1234.xlsx"`
3. Verifique permissões de escrita no diretório `estimativas-bottom-up/`

### Problema: "Erro ao gerar PDF"

**Solução:**
1. Verifique se o arquivo HTML foi criado
2. Teste Chrome manualmente: `& "C:\Program Files\Google\Chrome\Application\chrome.exe" --version`
3. Verifique se há espaços no caminho do arquivo (use aspas duplas)
4. Se receber erro de headless, atualize Chrome para versão 132+

### Problema: "Diretório estimativas-bottom-up/ não existe"

**Solução:**
Crie manualmente:
```powershell
New-Item -ItemType Directory -Path "C:\caminho\workspace\estimativas-bottom-up" -Force
```

### Problema: "Base de conhecimento não encontrada"

**Solução:**
Verifique se o diretório `.github/skills/estimativa-bottom-up-ici/base-conhecimento/` existe. Se não existir, crie-o:
```powershell
New-Item -ItemType Directory -Path ".github/skills/estimativa-bottom-up-ici/base-conhecimento" -Force
```

---

## 📊 Exemplo Prático Completo

### Cenário: Requisição do Redmine para Novo Relatório

**Você solicita:**
> "Preciso estimar a requisição 1234 do Redmine. Preciso criar um novo relatório de monitoramento que mostre protocolo recebido, data, hora, status e órgão de origem."

**O agente IA pergunta obrigatoriamente:**

1. *"Qual é o número do chamado no service desk?"*
   - Você responde: `1234`

2. *"Esta estimativa incluirá homologação assistida?"*
   - Você responde: `Sim`

**O agente IA então:**
- Analisa a documentação de discovery do Sigesguarda Pro
- Consulta estimativas históricas de relatórios
- Decompõe em funcionalidades: Análise, Design, Implementação, Testes
- Estima horas: 4h (Análise) + 12h (Dev) + 3h (Testes) = 19h
- Adiciona 15% de Homologação = 19 × 0.15 = 3h
- **Total: 22h**

**Gera:**
1. ✅ `ESTIMATIVA-1234.md` (arquivo formal)
2. ✅ `Estimativa_1234.md` (base de conhecimento + plano de implementação)
3. ✅ `ESTIMATIVA-1234.json` (dados estruturados)
4. (Opcionalmente) ✅ `Estimativa_1234.xlsx` (planilha)
5. (Opcionalmente) ✅ `ESTIMATIVA-1234.pdf` (documento PDF)
6. ✅ Texto formatado para Redmine/Service Desk

**Você então:**
- Revisa os arquivos gerados
- Aprova a estimativa
- Copia o texto formatado para o Redmine
- Envia o PDF para o cliente

---

## 📖 Documentação Adicional

Para entender a teoria completa da metodologia Bottom-Up, consulte:

- [`estimativa_bottom_up_software.md`](./estimativa_bottom_up_software.md) — Conceitos, estrutura técnica, fluxo completo
- [`SKILL.md`](./SKILL.md) — Especificação técnica detalhada (8 etapas, regras, formatos)
- Pasta `base-conhecimento/` — 85+ estimativas históricas para consulta e referência

---

## 🤝 Suporte e Feedback

Se encontrar problemas:

1. **Verifique os pré-requisitos** (Python 3.7+, openpyxl, Chrome)
2. **Consulte a seção de Troubleshooting** acima
3. **Reporte problemas** em: https://github.com/anomalyco/opencode/issues

---

## 📝 Licença

Consulte `LICENSE.txt` neste diretório.

---

**Versão:** 1.0  
**Última atualização:** Junho de 2026  
**Mantido por:** Equipe de Arquitetura (ICI)
