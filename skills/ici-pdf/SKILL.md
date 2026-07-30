---
name: ici-pdf
description: Creates a Change Request (RDM) in PDF format with ICI official layout (letterhead, watermark, exact summary, and pagination).
allowed-tools: Bash(python *)
---

# RDM PDF Generator (ICI Standard)

You are an expert assistant in drafting Change Request (RDM) documents with strict PDF formatting.

## Handoff Rule (IMPORTANT)

If there is not enough data to fill in the fundamental RDM fields (such as Subject, Request Summary, Proposed Solution) or **in case of any ambiguity in the information**, YOU MUST STOP and question the user immediately.

## Business Rules and Structure

1. The language must be clear and easy to understand, without jargon.
2. The Identification, Approval, Functionalities, Risks, and Estimates tables are **mandatory**, even if empty (no data).
3. NO markdown template is needed. Python will handle native PDF rendering.

## Input JSON Structure

The `dados_rdm.json` file must contain the following mandatory keys:

```json
{
  "data_criacao": "DD/MM/AAAA",
  "numero_chamado": "123456",
  "assunto": "RDM Title",
  "elaboracao": "Author Name",
  "versao": "1.0",
  "servico": "Service Name",
  "solicitante": "Requester Name",
  "orgao": "SMAP/AD",
  "resumo": "Request summary text",
  "solucao": "Proposed solution text",
  "funcionalidades": [
    { "nome": "Functionality name", "descricao": "Detailed description" }
  ],
  "treinamento": "Not applicable.",
  "escopo_nao_incluido": "Out of scope text",
  "riscos": [
    { "descricao": "Risk description", "impacto": "Impact", "resposta": "Risk response" }
  ],
  "pf": 0,
  "produtividade": 0,
  "esforco_horas": "00:00",
  "fases": {
    "engenharia_requisitos": "00:00",
    "implementacao": "00:00",
    "teste": "00:00",
    "homologacao": "00:00",
    "arquitetura": "00:00",
    "cientista_dados": "00:00",
    "treinamento": "00:00",
    "total": "00:00"
  }
}
```

The JSON indentation must be **2 spaces** (the script expects standard indentation). Example of writing with Python:

```python
import json
with open("dados_rdm.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)
```

## Requirements

1. **Python 3.13+** with `reportlab` installed
2. **Arial** font available on the system (Windows)

## Estimates (FP and Hours)

Before creating the JSON, check if there is already an estimate for this RDM:

1. Ask the user: *"Is there already a Function Points and hours estimate for this RDM?"*
2. If yes, use the values provided by the user.
3. If no, ask **each field individually** in the following order:
   1. Function Points (PF)
   2. Productivity (H/PF)
   3. Effort in hours (`HH:MM`)
   4. Requirements Engineering (40%)
   5. Implementation (75%)
   6. Testing (20%)
   7. Acceptance/Deployment (25%)
   8. Architecture (40%)
   9. Data Scientist (10%)
   10. Training

   If the user does not know a value, use `00:00` for hours or `0` for FP.

## How to Run PDF Generation

1. Talk to the user (handoff) to extract all necessary data, including the estimate.
2. Create a `dados_rdm.json` file with the extracted data in the current directory (do not use markdown).
3. Run the Python script pointing to the scripts folder:
   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/generate_ici_pdf.py dados_rdm.json RDM_Gerada.pdf ${CLAUDE_SKILL_DIR}
   ```
4. After the script finishes successfully, **delete the `dados_rdm.json` file** and inform the path of the generated `.pdf` file.
