# Technical Writing Principles

---

## Clarity and Scannability

> **Scope of these principles:** The conciseness guidelines below apply to **technical** artifacts (`tec-req-XXXX`, `api-`, `apf-`, `did-`, `dcl-`, `der-`, `min-`). The business document `req-XXXX` follows its own **deliberate verbosity** rules defined in section 5 of `SKILL.md`: narrative paragraphs, maximum detail, and concrete examples are mandatory to ensure comprehension by non-technical audiences.

- **Use active voice** and short sentences.
- **Be direct:** if the reader needs to re-read to understand, simplify.
- **Organize with Markdown:** headings, subheadings, lists, and code blocks make information navigable.
- **Prefer concrete examples** over abstract descriptions.
- **Avoid unnecessary jargon:** if a technical term is needed, add it to the document's glossary.

---

## Empathy for Target Audience

Define who will use the document and adapt the tone and level of detail:

| Audience              | Focus                                                                                   |
| --------------------- | --------------------------------------------------------------------------------------- |
| **Developers**        | APIs, code examples, implementation details, method and file references                 |
| **QA / Testers**      | Acceptance criteria, negative scenarios, expected input and output data                 |
| **Stakeholders / PMs**| Objectives, business impact, scope, metrics, and risks                                 |
| **End Users**         | Step-by-step tutorials, FAQs, and troubleshooting                                      |

---

## Docs-as-Code

- **Version documentation alongside code:** keep artifacts in the repository.
- **Use Git** for history, pull request review, and asynchronous collaboration.
- **Prefer Markdown** as the base format for all artifacts.
- Consider site generation tools from Markdown (**Docusaurus**, **MkDocs**, **Hugo**) for projects with large public or internal documentation.

---

## Standard Documentation Production Process

1. **Brainstorming with stakeholders:** identify actors, flows, and edge cases.
2. **Project reading:** understand context, structure, and stack through `README.md` and base documents.
3. **Deep investigation:** traverse code, sub-functions, frontend, validations, database, integrations, and design.
4. **Impact mapping:** list impacting/impacted documentation/requirements.
5. **Initial draft:** create a draft with minimum structure.
6. **Update mode (blocking):** when updating an existing document, fully preserve the format/structure of the already-applied template (sections, tables, columns, order, and checklists), changing only the necessary content.
7. **Wireframe production:** for interface requirements, invoke the `design-lead` agent to generate wireframe images. **Rule for req-XXXX:** PNG image only (ASCII wireframe as fallback if PNG is not possible). **Rule for tec-req-XXXX:** both ASCII wireframe (embedded) and PNG image (referenced) are mandatory. If `design-lead` is not available, use available design skills and the `capture-mockup.cjs` script as a fallback. Always validate that the PNG file exists after generation.
8. **Technical review:** validate with engineers and QA.
9. **Cross-document review:** adjust related documents when necessary.
10. **Approval:** record formal approval (`apr_req-`) before implementation.
11. **Maintenance:** update when the requirement changes and record change history.

---

## Recommended Tools

| Tool                            | Usage                                                           |
| ------------------------------- | --------------------------------------------------------------- |
| **Markdown**                    | Base for all artifacts                                          |
| **Mermaid.js**                  | Diagrams embedded in Markdown                                  |
| **Git / GitHub / GitLab**       | Versioning and collaborative review                             |
| **Docusaurus / MkDocs**         | Documentation site generation                                  |
| **Swagger / OpenAPI / Postman** | Interactive API documentation                                  |
| **database-mcp**                | Inspect procedures, views, functions, and database schema       |
| **MCP libraries**               | Validate integrations and external framework behavior           |
| **Figma / Sketch / Adobe XD**   | Prototypes and design system (reference in `padrao-visual.md`)  |
