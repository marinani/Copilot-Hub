# Guide 2: Execution Investigation and Deep Dive

## 1. Execution Trigger

Started only after the user approves the plan. Focused on extracting the "absolute truth" from code, database, and interfaces.

## 2. Feature and Use Case Investigation

When analyzing code to document system flows, the agent must document each Use Case with technical rigor:

* **Preconditions:** The mandatory system state before the feature begins.
* **Main Flow:** The exact and normal sequence of steps (happy path).
* **Sub-flows:** Repetition logic or embedded auxiliary processes (`<<include>>`).
* **Alternative Flows and Exceptions:** Optional paths (`<<extend>>`) and system error handling.

## 3. Database and Dictionary Investigation (Skill `database-mcp`)

Mandatory (blocking) use of the `database-mcp` skill for relational persistence:

* **Routine Extraction (BLOCKING):** It is mandatory to extract the complete SQL body of Procedures, Functions, Triggers, and Views and record them in `tec-req-XXXX`.
* **Execution Summary:** Provide an explanation of which tables undergo mutation in the extracted SQL.
* **ETL Mapping:** If the system performs integrations or transfers, identify: Source, Destination, Transformation Rules, Data Types, and Masks.
* **Data Dictionary (`did-`):** Record tables, columns, types, PK/FK, nullability. **LGPD (BLOCKING):** It is mandatory to add the tag `LGPD: sensitive data` or `LGPD: non-sensitive data` in the comment of each column.

## 4. Integrations and External Components

* **Integration Documentation:** Each distinct operation with an external system (e.g., Query Citizen at SERPRO) generates an independent technical requirement. The agent must map the payload (request/response), authentication, timeouts, and generate a Mermaid Sequence Diagram.
* **Field and Mask Dictionary:** For forms and APIs, detail field name, type, required status, format, and expected masks (e.g., `CPF: 000.000.000-00`), indicating the regex or method that applies it in the code.

## 5. Recording in the Master RF and RN Documents (Blocking)

During the deep dive, when identifying functional requirements (FR) and business rules (BR) of the system, the agent must:

1. **Consult** the master documents before assigning an identifier:
   - `documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/regras/requisitos-funcionais.md`
   - `documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/regras/regras-negocios.md`
2. **Verify** whether the FR or BR already exists (avoid duplicates) or obtain the next available number.
3. **Insert** the new entry in the master document with: identifier, title, description, and "Documents that use it" field.
4. **Only then** reference the identifier in the `tec-req-XXXX` being produced.
5. **Never** create FR or BR directly in `tec-req-XXXX` without first recording it in the master.

## 6. Final Traceability

All extracted SQLs, DTOs, generated Mermaid diagrams, and investigated business rules form the base content that the agent will use to fill in the `tec-req-XXXX` (Technical Document) and calculate the `apf-req-XXXX` (Function Point Analysis) in a mathematical and irrefutable manner.
