# Directory Structure and File Naming

## Directory Structure

```
/documentacao
|-- README.md  (mandatory root TOC)
|-- matriz-risco-sistema.md (mandatory global risk matrix)
|-- mapeamento-investigacao-sistema.md (continuous mapping, structure, dependencies, and evidence record)
|-- arquitetura-tech-stack.md (architecture, tech stack, integrations, and observations record)
|-- design.md (root copy of the visual design document; must be kept in sync with `documentacao/padrao_visual/design.md`)
|-- tamanho-aplicacao.md (Document synchronized with the sum of function points of requirements, updated with each requirement inclusion/change)
|-- /padrao_visual
  |-- padrao-visual.md
  |-- layout.md
  |-- design.md
  |-- /wireframes
    |-- req-XXXX.png
|-- /legado                                      (Documentation of the previous system intended only as support, cannot be modified)
|-- /processo_unificado
  |-- /artefatos_aprovados
    |-- /documentacao_api
      |-- api-nome_da_api.md
    |-- /visao
      |-- vis-nome_da_visao.md
    |-- /detalhamento_requisitos
      |-- req-XXXX-nome_do_requisito.md          (stakeholder document — business language, no technical details)
      |-- /tec
        |-- tec-req-XXXX-nome_do_requisito.md    (technical document — for the developer, with all implementation details)
      |-- /apf
        |-- apf-req-XXXX.md
      |-- /estimativas
        |-- estimativa-req-XXXX-{YYYY-MM-DD-HHmmSS}.md
      |-- /criterios
        |-- cri-req-XXXX-nome_do_requisito.md    (all possible Gherkin scenarios for the requirement)
      |-- /regras
        |-- requisitos-funcionais.md             (single source of truth — all FR of the project with continuous numbering)
        |-- regras-negocios.md                   (single source of truth — all BR of the project with continuous numbering)
      |-- apr_req-nome_do_requisito_de_aprovacao.md
    |-- /diagrama_de_classes
      |-- dcl-nome_do_diagrama_de_classes.md
    |-- /diagrama_de_integracao_de_sistemas
      |-- min-nome_do_diagrama_de_integracao_de_sistemas.md
    |-- /diagrama_de_entidades_e_relacionamento
      |-- der-nome_do_diagrama_de_entidades_e_relacionamentos.md
    |-- /dicionario_de_dados
      |-- did-nome_do_dicionario_de_dados.md
    |-- /documentos_de_apoio
      |-- <additional_artifact>.md

```

**Critical rule:** Requirements (`req-XXXX`) always at the root; technical (`tec-req-XXXX`) always in `tec/`; APF (`apf-req-XXXX`) always in `apf/`.

---

## Document Types and Prefixes

| Document Type                     | Prefix                   | Purpose                                                                                                                                                                                                                                                                                                                                     |
| --------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| API Documentation                 | api-                     | Describe endpoints, payloads, and responses                                                                                                                                                                                                                                                                                                 |
| Vision Document                   | vis-                     | Objectives, scope, stakeholders, and benefits                                                                                                                                                                                                                                                                                               |
| Requirement (stakeholder)         | req-                     | Business language document for non-technical stakeholders: functional flows, business rules, acceptance criteria, and impacts. **Strictly prohibited: code, routes, files, method names, classes, endpoints, tables, columns, English terms, or any IT jargon.**                                                                            |
| Technical Requirement (developer) | tec-req-                 | Technical document for the developer, created in `detalhamento_requisitos/tec/` using the template `documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/tec-req-template.md`: routes, files, code, endpoints, DTOs, database, procedures, technical diagrams, measurable NFRs, and all code investigation evidence. |
| FPA per Requirement               | apf-req-                 | Function point calculation linked to the requirement                                                                                                                                                                                                                                                                                        |
| Complete Acceptance Criteria      | cri-req-                 | All possible Gherkin scenarios for the requirement (happy path, exceptions, edge cases). Maximum of 5 criteria in `req-` and `tec-req-` documents; the full set resides in this artifact.                                                                                                                                                   |
| Functional Requirements (Master)  | requisitos-funcionais.md | Single source of truth for all FR of the project, with continuous global numbering. Location: `detalhamento_requisitos/regras/`.                                                                                                                                                                                                            |
| Business Rules (Master)           | regras-negocios.md       | Single source of truth for all BR of the project, with continuous global numbering. Location: `detalhamento_requisitos/regras/`.                                                                                                                                                                                                            |
| Requirement Approval              | apr_req-                 | Formal confirmation that the requirement is approved                                                                                                                                                                                                                                                                                        |
| Class Diagram                     | dcl-                     | Code structure and relationships between classes                                                                                                                                                                                                                                                                                            |
| System Integration Diagram        | min-                     | Communication between services and external systems                                                                                                                                                                                                                                                                                         |
| Entity Relationship Diagram (DER) | der-                     | Data model and cardinalities                                                                                                                                                                                                                                                                                                                |
| Data Dictionary                   | did-                     | Field and table metadata                                                                                                                                                                                                                                                                                                                    |
| Visual Pattern Document           | padrao-visual.md         | Reproduce design, navigation, components, and visual tokens                                                                                                                                                                                                                                                                                 |
| Layout Document                   | layout.md                | Describe layout pattern, positioning, and visual structure                                                                                                                                                                                                                                                                                  |
| Support Document                  | -                        | Additional documents not directly described by the skill, stored in `documentacao/processo_unificado/artefatos_aprovados/documentos_de_apoio/`                                                                                                                                                                                              |

---

## Mandatory TOC at Documentation Root

Within `/documentacao`, there must be a `README.md` containing:

1. Documentation context and objective;
2. Navigable index for all areas of the structure;
3. Prefix convention;
4. Artifact status (draft, in review, approved);
5. Last global documentation update.
6. When applicable, index of links between requirements and related artifacts.

Without this root TOC, the documentation is considered incomplete.

---

## FR and BR Numbering Rule

- **Functional Requirements (FR):** continuous and global `RF-XXXX` numbering throughout the project. Never restarts per requirement.
- **Business Rules (BR):** continuous and global `RN-XXXX` numbering throughout the project. Never restarts per requirement.
- Before creating a new FR or BR, consult `detalhamento_requisitos/regras/requisitos-funcionais.md` or `regras-negocios.md` to obtain the next available number.
- See complete governance in section 15 of `SKILL.md`.
