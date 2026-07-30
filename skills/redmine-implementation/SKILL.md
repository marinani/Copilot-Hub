---
name: redmine-implementation
description: Executes the complete workflow for analyzing and implementing a Redmine ticket. Fetches the issue via MCP, validates project/assignee/status, analyzes the current codebase, asks the developer questions, generates an implementation plan and test plan (Dev + QA), implements, and updates the status in Redmine. Use when the user writes "redmine: #<number>" or "ticket: #<number>".
---

# RedmineImplementation

## Expected Input

```
redmine: #168856
ticket: #168856
```

## Output Formatting (Chat)

- **Ticket/card list** must be displayed as a **Markdown table** (columns such as ID, title, status, assignee, priority, update date).
- **Ticket detail** must be displayed as a **chat-integrated card** (structured markdown with clear fields and sections).

---

## Non-Negotiable Rules

- Mandatory architecture: as defined in `config.arquitetura` — respect the project's layer pattern.
- Target platforms: as defined in `config.plataformas` — consider all when implementing and testing.
- UI texts and comments in pt-BR.
- No hardcoded tokens or credentials.
- Do not introduce new libraries without explicit decision.
- The `planning-and-task-breakdown` skill must be used obligatorily and non-negotiably to create/maintain all artifacts in `planning/`.
- All user interaction during execution in VS Code must happen in the integrated chat using **handoff** (never in `input()` of a script, never in a terminal prompt).
- Any question, confirmation, or choice (free text or closed options) must be made exclusively via **handoff**.
- To interact with Redmine during this workflow, only this skill (`redmine-implementation`) must be used. Mandatory item.
- A ticket is only **completed** when all items in the plan are checked AND all tests pass.
- If there is a blockage: status changes to **Blockers** + note in Redmine — never close with pending items.
- Analysis must always result in a mandatory plan: **resolution plan** (when the problem is clear) or **investigation plan** (when the problem is unclear).
- When the request is for **analysis**, the agent must jointly analyze the Redmine card, the related code, and **always consider attached images** as mandatory evidence.
- In **analysis** requests, the agent must first understand the current behavior before proposing a solution or plan.
- In **analysis** requests, the agent must add the "Ia" tag to the card.
- During analysis, the agent must execute sufficient tests, reproductions, and triangulations to eliminate ambiguities; if there is still material doubt, it must ask the user in the chat before proceeding.
- Update the plan in real time as discoveries, decisions, test results, blockers, and changes in understanding emerge.
- When plan execution begins, change the issue status in Redmine to **In Progress** before starting the first implementation phase.
- When completing each phase of the plan, the agent must objectively report what was done and **wait for explicit developer authorization** before proceeding to the next phase.
- Plan execution can only begin after **explicit user approval** via handoff (e.g., "yes", "approved", "you can start"). Without explicit approval, implementation is prohibited.
- These rules apply to any analysis requested by the user, even if the card already seems clear or the solution seems obvious.
- **Redmine comments**: by default, all comments must be sent as **private** (`private_notes: true`). Public comments should only be sent when: (a) it is the "implementation completed" comment, or (b) the user explicitly requests it.
- **Public "implementation completed" comment**: must contain the title **"Fix applied"**, plain non-technical text (no class names, functions, methods, files, or jargon), and must be **approved by the user** before sending.
- **Public comments in general**: always in plain text, no technical jargon, and always approved by the user before sending.

## Interactive Gates — NEVER Skip

There are 3 moments where execution **must stop** and wait for the developer's response.
In this skill, the word **GATE** means obligatorily: **interactive integration with the VS Code chat**.

Each gate must:

1. Display the question in the chat (single, objective message);
2. Use **handoff** to wait for the developer's response;
3. Wait for the developer's response in the next message;
4. Not advance in the same response.

| Gate          | When                                 | What to Wait For                                          |
| ------------- | ------------------------------------ | --------------------------------------------------------- |
| **STEP 4**    | After codebase analysis              | Developer confirms understanding or adds context          |
| **STEP 7**    | After generating the plan            | Developer confirms "you can start" (yes/no + observations)|
| **STEP 9a**   | After automated checks               | Developer confirms they tested manually (yes/no/issues)   |
| **STEP 9b**   | Before sending public comment        | Developer approves the non-technical public comment text  |

> **Additional interactions (not formal gates, but also stop and wait for developer response):**
>
> - **STEP 2.2**: when the description is vague — handoff for clarification or confirmation of understanding.
> - **STEP 3.2**: after listing files found in the codebase — waits for developer confirmation/additions.
> - **STEP 9b**: before sending the public completion comment — developer approves the non-technical text.

**At each gate: emit the question message and end the response. Do not advance in the same response.**

---

## STEP 0 — Load Configuration and Fetch Issue

Before any operation, the script must ensure:

- **Python is installed in the environment** (available in PATH). If not, the agent must warn that it needs to be installed and, if the user agrees, install automatically (including adding to the system PATH).
  - **The Redmine API key is available** (`REDMINE_API_KEY`). If not:
    1. The agent must check if the key is present in the operating system environment with the PowerShell command: `echo $env:REDMINE_API_KEY` (Windows) or `echo $REDMINE_API_KEY` (Linux/Mac). If the result is empty, the key is not defined.
    2. **The agent must ask directly in the chat via handoff** and collect the response. **NEVER use `input()` or terminal prompt.**
    3. The `index.py` script emits a JSON error (`REDMINE_API_KEY_MISSING`) to stderr and exits with code 2 when the key is missing — the agent must intercept this error and ask the question in the chat.
    4. Upon receiving the key via chat, the agent must: (a) **set it permanently in the operating system with `setx REDMINE_API_KEY "..."` on Windows**, so it is available in any terminal/project; (b) also set it as an environment variable for the current session (`$env:REDMINE_API_KEY = "..."`) before re-running the script; (c) **NOT store the key in `.github/config.yaml`** (it is sensitive).
- **The project name (`project_name`) is defined**. If not, ask the user via **handoff** and store in `.github/config.yaml` (section `redmine`).
- **The `status_ids` are updated automatically** from the Redmine API.
- **The custom field mapping for tags in Redmine is configured** to allow including the value `IA` in the card.

1. Read `.github/config.yaml` (if it does not exist, it will be created) and verify the `redmine` section with project information:

- `project_name` (if absent, the agent must ask via handoff and record the response).
- `project_id` and `project_id_numeric` will be populated automatically from the project name.
- `status_ids` will be updated with data returned by `/issue_statuses.json`.
- `usuario_id` — numeric ID of the developer in Redmine (required for Gate 2 of STEP 1; ask the user via handoff if absent).
- `tag_custom_field_id` — ID of the custom tag field in Redmine (required for writing the `IA` tag; ask via handoff if absent).
- `ia_tag_value` — value of the AI tag to be applied to the card (default: `IA`).

The `projeto` section defines codebase settings (referenced in STEPs 8 and 9 as `config.*`):

```yaml
redmine:
  project_name: "project-name"
  project_id: "project-slug" # populated automatically
  project_id_numeric: 42 # populated automatically
  usuario_id: 123 # developer ID in Redmine
  tag_custom_field_id: 15 # custom "tag" field ID in Redmine
  ia_tag_value: "IA" # value to include in the custom tag field
  status_ids: # updated automatically via API
    a_fazer: 1
    fazendo: 2
    feito: 3
    impedimentos: 6
    backlog: 7

projeto:
  arquitetura: "Clean Architecture" # layer pattern (config.arquitetura)
  plataformas: # target platforms (config.plataformas)
    - Android
    - iOS
  cmd_testes: "dotnet test" # command to run tests (null if not applicable)
  cmd_typecheck: "dotnet build" # type/build check (null if not applicable)
  cmd_lint: null # lint (null if not configured)
  pasta_testes: # test folders (config.pasta_testes)
    - "tests/"
  estrutura_src: # main source folders (config.estrutura_src)
    - "src/"
```

**Important note:** `.github/config.yaml` stores **ONLY project information** (project_name, project_id, status_ids, etc). Sensitive credentials like `REDMINE_API_KEY` **must be in the OS environment** (via `setx`), **never** in the configuration file.

2. Fetch the issue via MCP `get_issue` with the provided ID.

### 0.1 — Mandatory Operations with Custom Fields (Specific Issue)

When it is necessary to query or modify custom fields of a specific card/issue, use these commands from `mcp/index.py`:

- **Get custom fields of the issue**:
  - `python mcp/index.py get_issue_custom_fields <issue_id>`
- **Get a specific custom field**:
  - `python mcp/index.py get_issue_custom_fields <issue_id> --field_id <custom_field_id>`
- **Add value to custom field**:
  - `python mcp/index.py add_issue_custom_field_value <issue_id> --field_id <custom_field_id> --value "<value>"`
- **Remove value from custom field**:
  - `python mcp/index.py remove_issue_custom_field_value <issue_id> --field_id <custom_field_id> --value "<value>"`

Rules:

- Always operate on the **specific issue** provided in the ticket.
- For the AI tag, use `tag_custom_field_id` + `ia_tag_value` from the config.
- Before adding/removing a value, query the current field to avoid duplicates and record evidence in the plan.

### 0.2 — Mandatory Operations for Native Card Tags (`tag_list` / `tags`)

When the Redmine instance supports native tags on the card, inclusion must be done via payload in `update_issue` (API `/issues/{id}.json`) using **`tag_list`** as the standard.

Recommended command from the skill itself (`mcp/index.py`):

- **Add native tag to card with automatic fallback**:
  - `python mcp/index.py add_issue_tag <issue_id> --tag "<tag_value>"`

Mandatory attempt order for tag inclusion (idempotent):

1. `{"issue":{"tag_list":["<tag>"]}}`
2. If the instance rejects array format, try `{"issue":{"tag_list":"<tag>"}}`
3. If `tag_list` is not accepted, fallback to `tags`:
   - `{"issue":{"tags":["<tag>"]}}`
   - `{"issue":{"tags":"<tag>"}}`

Rules:

- Always avoid duplicates (do not resend the same tag when already applied).
- If `GET /issues/{id}.json` does not expose `tag_list`/`tags`, validate via evidence in `GET /issues/{id}.json?include=journals`.
- Consider success only with HTTP `204` response on `PUT` **and** evidence in the journal (`details` containing changes to `tag_list`/`tags`).
- If no payload variation is accepted, record a blocker in the plan and follow the blocking flow.

API update example (reference):

```bash
PUT /issues/177099.json
{
  "issue": {
    "tag_list": ["test"]
  }
}
```

Journal validation example (when default GET does not show tags):

- `details.property = attr`
- `details.name = tag_list`
- `old_value = ""`
- `new_value = "test"`

Skill command example:

```bash
python mcp/index.py add_issue_tag 177099 --tag "test"
```

### 0.3 — Comment Visibility Control

The `update_issue` command now supports the `--public` flag to control comment visibility.

**Usage rules:**

- **Private comment (default)**: send WITHOUT the `--public` flag:
  ```bash
  python mcp/index.py update_issue <issue_id> --notes "private note" --status_id <id>
  ```
- **Public comment**: send WITH the `--public` flag:
  ```bash
  python mcp/index.py update_issue <issue_id> --notes "public note" --status_id <id> --public
  ```

> Omitting the `--public` flag results in `private_notes: true` (private comment).
> With `--public`, the `private_notes` field is set to `false`.

---

## STEP 1 — Validation Gates (Execute in Order, Stop at First Failure)

### Gate 1 — Correct Project

- The issue's `project.id` field must equal the config's `project_id_numerico`.
- If different:
  > "⛔ Issue #X belongs to project '[name]', not the configured project ('[config.projeto_nome]'). Check the ticket number."
  > → **ENDS**

### Gate 2 — Assigned to Developer

- The issue's `assigned_to.id` field must equal the config's `usuario_id`.
- If `assigned_to` is null/absent:
  > "⛔ Issue #X is not assigned to anyone. Assign it to yourself in Redmine before continuing."
  > → **ENDS**
- If assigned to someone else:
  > "⛔ Issue #X is assigned to [name]. It is not yours to implement."
  > → **ENDS**

### Gate 3 — Valid Status for Implementation

- The statuses below indicate the ticket has already been implemented, is in validation/QA, or has been closed — none allow new implementation.
- If `status.id` is in `status_encerrados` (Done, Testing, Approval, Build, Ready, Cancelled):
  > "⛔ Issue #X has status '[status]'. Nothing to implement."
  > → **ENDS**
- If status is **Backlog** (id: 7):
  > "⚠️ Issue #X is in Backlog. Do you confirm it should be implemented now? (answer yes/no)"
  > → **Wait for confirmation. If no: ENDS.**
- If status is **To Do** (id: 1) or **In Progress** (id: 2):
  → Continues normally.

---

## STEP 2 — Issue Analysis

### 2.0 — Mandatory Rule for Analysis Mode

If the developer's request is for **analysis** (without starting immediate implementation) and the issue is in **To Do** (id: 1), the following must be executed before the analysis:

1. Assign the issue to the config's `usuario_id` (via update in Redmine through the skill itself);
2. Add the AI tag to the custom tag field (`tag_custom_field_id`) with the value `ia_tag_value` (default `IA`);
3. Record in `planning/onda-{number}/0-issue.md` that the assignment and `IA` tag were applied.

If `tag_custom_field_id` is not configured, open a **handoff** to collect the ID and only then proceed.

### 2.1 — Classify Type

Based on `tracker.name` and description content, classify:

- `bug` — incorrect behavior in existing functionality
- `issue` — reported problem/incident (operational equivalent of bug)
- `melhoria` — enhancement of existing functionality
- `feature` — new functionality

### 2.2 — Evaluate Description Quality

**Rich description** (has: what, where, expected vs actual behavior) → proceed to STEP 3.

**Poor description** (vague, short, or absent):

- Display interpretation based on the title and open a **handoff** for the developer's response:
  > "⚠️ The description is vague. Based on the title, I understood that: _[interpretation]_. Is that correct? Can you add more details?"
- Wait for the developer's response via handoff:
  - Developer adds details → use the addition as the effective description → proceed.
  - Developer doesn't know → use MCP `update_issue` to add a note to the issue:
    > _"Insufficient description for implementation. Please add: expected behavior, usage scenario, and acceptance criteria."_
    > → **ENDS** with a warning to the developer.

### 2.3 — Create `planning/onda-{number}/0-issue.md`

> `{number}` is the numeric ID of the issue in Redmine (e.g., issue #168856 → folder `planning/onda-168856/`). The same number is used in all planning files generated by this execution.

```markdown
# Issue #{number} — {title}

- **Project:** {project}
- **Tracker:** {tracker}
- **Status:** {status}
- **Priority:** {priority}
- **Assignee:** {assignee}
- **Author:** {author}
- **Created on:** {creation_date}
- **Updated:** {update_date}

## Original Description

{description}

## Developer Addition (if applicable)

{developer_addition}

## Classification

Type: bug | issue | melhoria | feature
```

---

## STEP 3 — Codebase Analysis

1. Search the codebase for files related to the issue's topic in the folders defined in the root **README.md** of the workspace.

2. Display what was found:

   > "I found the following related files: [list]. Are there others I should consider?"
   → Collect the response via **handoff** and wait. Incorporate if there are additions.

3. Check if there is documentation for the requirement/problem being evaluated (project README, functional docs, ADRs, specifications, etc.).
   - If documentation is found: record the path(s), evaluate the content, and cross-reference with the problem described in the card.
   - If **not** found: open a **handoff** asking the user if this documentation exists and where it is.
     - If the user provides the location: read/evaluate the documentation and continue the analysis.
     - If the user confirms it does not exist: record in the plan the need to create the requirement documentation.

4. Generate a preview of what can be done based on what exists (code + documentation).

5. Create `planning/onda-{number}/1-analise.md`:

```markdown
# Analysis — Issue #{number}

## Related Files Found

- {config.estrutura_src[x]}/...

## Files Added by Developer

- (if applicable)

## Requirement Documentation

- Found at: {documentation_paths} | Not found
- Evidence used in analysis: {documentation_summary}
- Action when absent: add requirement documentation creation to the plan

## Preview of What Can Be Done

{preliminary_technical_description}
```

---

## STEP 4 — Present Understanding and Wait for Input

⛔ **MANDATORY GATE — DO NOT PROCEED WITHOUT DEVELOPER RESPONSE**

Based on the codebase analysis (STEP 3), display in a single message:

1. **What was understood** — describe the problem or functionality in your own words,
   citing the files found and the identified cause (if bug/issue) or expected behavior.

2. **What will be done** — describe the solution approach clearly and directly:
   which files will be modified, what logic will be applied, what the expected impact is.

3. **Follow-up question** — end with:
   > "This is my understanding. Do you want to add anything before I generate the plan?
   > (e.g., screenshot, additional context, technical constraint, solution preference)"

> Use **handoff** to wait for the developer's response (free text).

**End the response here.** Do not generate a plan, do not implement, do not create files beyond those already created.

→ **STOP HERE. Wait for the developer's response before moving to STEP 5.**
→ Developer responds "no" / "go ahead" / "no additions" → proceed normally.
→ Developer adds context → incorporate and proceed.

---

## STEP 5 — Implementation Plan

Generate a 100% closed checklist (no open questions) incorporating the responses from STEP 4.

⛔ **MANDATORY:** plan creation and maintenance must be done using the **`planning-and-task-breakdown`** skill (non-negotiable).

Plan type criteria:

- If the problem is clear: create a **resolution plan** with implementation tasks.
- If the problem is unclear: create an **investigation plan** with hypotheses, experiments, expected evidence, and exit criteria to convert into a resolution plan.

In both cases, plan creation is mandatory.

1. Create (if it does not exist) the wave folder in `planning/onda-{number}/`.
2. Create **2-plano.md** with the problem view, proposed solution, impacted files, risks, and acceptance criteria.
3. Create **3-checklist.md** with actionable items and verification criteria.

### Minimum Example of `planning/onda-{number}/2-plano.md`

```markdown
# Implementation Plan — Issue #{number}

## Type

bug | issue | melhoria | feature

## Problem / Motivation

{summary_of_what_will_be_done}

## Files to Create

- [ ] {config.estrutura_src[x]}/...

## Files to Modify

- [ ] {config.estrutura_src[x]}/...

## API Endpoints Involved

- GET /...
- POST /...

## Execution Order

1. ...
2. ...

## Attention Points / Risks

- ...

## Acceptance Criteria

- [ ] ...
- [ ] ...

## Requirement Documentation

- [ ] Validate that the requirement/problem documentation exists and was considered in the analysis
- [ ] If it does not exist, include a task for creating/updating the documentation
```

### Minimum Example of `planning/onda-{number}/3-checklist.md`

```markdown
# Checklist — Issue #{number}

## Implementation Validations

- [ ] Code compiling / build passing
- [ ] Unit or integration tests created/updated
- [ ] Minimum coverage achieved (if applicable)

## Functional Tests (QA)

- [ ] Main scenario validated manually
- [ ] Edge scenarios tested

## Error Reproduction (mandatory for bug/issue)

- [ ] Step-by-step to reproduce the current error documented
- [ ] Evidence of reproduction before the fix (message, log, screenshot, behavior)
- [ ] Post-fix validation steps executed

## Other

- [ ] Documentation updated / created (mandatory)
- [ ] Release notes / changelog updated (if necessary)
```

---

## STEP 6 — Test Plan (Integrated into Checklist)

The test plan is part of `3-checklist.md` and must contain:

- Technical tests: commands using `config.cmd_testes`, `config.cmd_typecheck`, and `config.cmd_lint`.
- Functional tests: reproduction steps, expected results, and edge cases.
- When the type is **bug** or **issue**, mandatory inclusion of a step-by-step reproduction of the error described in the ticket (before the fix) and validation steps after the fix.
- Regression checks (unaffected flows).

> The goal is to keep everything traceable in `planning/onda-{number}/` following the `planning-and-task-breakdown` skill pattern.

---

## STEP 7 — Confirmation to Implement

⛔ **MANDATORY GATE — DO NOT IMPLEMENT WITHOUT DEVELOPER RESPONSE**

⛔ **EXPLICIT APPROVAL MANDATORY:** after creating the plan (`2-plano.md` + `3-checklist.md`), the agent must present the plan to the user in the chat and wait for explicit approval to begin execution.

The questions must be presented **in the chat itself via handoff**, interactively, waiting for the developer to respond in a new message (without advancing in the same text).

Example question to send in a single message:

> "Plan generated. Before starting implementation:
>
> 1. Do you have any observations, technical decisions, or constraints I should record in the plan?
> 2. Can I start now?
>
> Please respond with your observations (if any) + yes/no to proceed."

> Use **handoff** to wait for the developer's response.

### Approval Normalization (Mandatory)

To remove ambiguity, the decision to start execution must follow only these responses:

- **APPROVED**: `yes`, `approved`, `you can start`, `ok to start`.
- **NOT APPROVED**: `no`, `wait`, `not yet`.
- **AMBIGUOUS**: any other response.

Action rules:

- Developer responds with observations → incorporate into `planning/onda-{number}/2-plano.md`.
- Only start STEP 8 when the response is **APPROVED**.
- If the response is **NOT APPROVED** or **AMBIGUOUS**, **do not implement**; update the plan and open a new handoff requesting objective confirmation until **APPROVED**.

---

## STEP 8 — Implementation

### 8.1 — Snapshot Before

Before any code changes, capture the current state and record in `planning/onda-{number}/4-execucao-testes.md` (section "Before"):

```bash
# Use the commands defined in config.json (adapt to the project's shell):
{config.cmd_typecheck}   # type/build check — if cmd_typecheck is not null
{config.cmd_lint}        # lint — if cmd_lint is not null
{config.cmd_testes}      # automated tests
```

> Record the result in `planning/onda-{number}/4-execucao-testes.md` (section "Before").

### 8.2 — Change Status in Redmine

If status was **To Do** (id: 1) → change to **In Progress** (id: 2) via MCP `update_issue`.

### 8.3 — Implement

Follow `planning/onda-{number}/3-checklist.md` item by item, marking each checkbox upon completion.

Mandatory architecture: as defined in `config.arquitetura`.
Platforms to consider: as defined in `config.plataformas`.

### 8.4 — Create Automated Tests

Create tests in the folders defined in `config.pasta_testes`, following the naming pattern
already existing in the project (e.g., `*.test.ts`, `*.spec.cs`, `*_test.py`).

| What to Create                         | Minimum Criteria                                                   |
| --------------------------------------- | ------------------------------------------------------------------ |
| Logic/service/repository test           | Happy path, network error/exception, empty data                    |
| Screen/component/controller test        | Render/response OK, loading state, error, main interaction         |

### 8.5 — Post-Implementation Verification

```bash
# Use the commands defined in config.json (skip if the field is null):
{config.cmd_typecheck}
{config.cmd_lint}
{config.cmd_testes}
```

**Mandatory criteria:**

- Typecheck / build: 0 new errors
- Lint: 0 new warnings (if cmd_lint configured)
- Tests: 0 failing
- Scope coverage: no regression vs before snapshot

---

## STEP 9 — Closure

### If implementation OK:

1. Fill in `planning/onda-{number}/4-execucao-testes.md` with the final result (before vs after).

2. ⛔ **MANDATORY GATE — DO NOT MARK AS DONE WITHOUT DEVELOPER RESPONSE**

   Display the question below in a single message and **end the response there**.
   Do not change the status in Redmine, do not add a note, do not emit a final report.
   Wait for the developer's response in the next message.

   > "The automated checks passed. Have you tested manually on the device/emulator as per `planning/onda-{number}/3-checklist.md` — test section?
   > Are the tests OK to mark as Done?"
   >
   > Please respond: yes / no / or list the issues found (if any)."

> Use **handoff** to wait for the developer's response.

- **No / issues found** → record the issues, fix them and run the checks again. Do not proceed until the developer confirms OK.
- **Yes** → proceed to the next items in STEP 9.

→ **STOP HERE. Wait for the developer's response before marking as Done.**

3. Change the status in Redmine to **Done** (id: 3) via MCP `update_issue`.

   > QA is responsible for moving to **Testing** when they begin validation.

4. ⛔ **MANDATORY GATE — DO NOT SEND PUBLIC COMMENT WITHOUT APPROVAL**

   Generate the public "implementation completed" comment text following these rules:

   - **Mandatory title:** "Fix applied"
   - **Plain, non-technical text:** no class names, functions, methods, files, or technical jargon
   - **Accessible language:** aimed at non-technical stakeholders
   - **Content:** what was fixed/implemented in natural language and the expected result

   Example format:

   ```
   Fix applied

   The issue in the fee calculation was fixed where the displayed value
   did not consider the usage time discount. Now the discount is
   applied correctly, and the final value presented to the user
   reflects the total with the benefit.
   ```

   After generating the text, present it to the user via **handoff** for approval:

   > "The public completion comment will be sent with the title 'Fix applied'.
   >
   > Proposed text:
   > ```
   > {non_technical_text}
   > ```
   >
   > Can I send this public comment to Redmine? (yes/no)"
   >
   > Use **handoff** to wait for the developer's response.

   - **No / changes** → adjust the text as requested by the developer and re-present until approval.
   - **Yes** → send the command:

     ```bash
     python mcp/index.py update_issue {issue_id} --notes "{approved_text}" --public
     ```

5. Emit the final report in the chat (see format below).

### If blocked during implementation:

1. Change status to **Blockers** (id: 6) via MCP `update_issue`.

2. Add a note to the issue explaining the blockage.

3. Record in `planning/onda-{number}/4-execucao-testes.md` as **BLOCKED** with the reason.

4. End without marking as completed.

---

## Generated File Structure

```
planning/
└── onda-{number}/
    ├── 0-issue.md                 ← Redmine issue data
    ├── 1-analise.md               ← files found + codebase preview
    ├── 2-plano.md                 ← implementation plan + context
    ├── 3-checklist.md             ← implementation checklist + test guide
    └── 4-execucao-testes.md       ← automated check results (OK or BLOCKED)
```

---

## Final Report (Mandatory Format)

Emit in the chat upon closing:

```
════════════════════════════════════════════════════════
  TICKET #XXXXX — {title}
  Type: bug | issue | melhoria | feature
════════════════════════════════════════════════════════

STATUS: ✅ COMPLETED — status Done, awaiting QA | 🔴 BLOCKED | 📋 PLAN GENERATED — awaiting developer

────────────────────────────────────────────────────────
 PROBLEM / MOTIVATION
────────────────────────────────────────────────────────
{summary in 2-3 lines}

────────────────────────────────────────────────────────
 IMPLEMENTED SCOPE
────────────────────────────────────────────────────────
✅ Item 1
✅ Item 2
❌ Item not implemented — reason

────────────────────────────────────────────────────────
 AUTOMATED CHECKS
────────────────────────────────────────────────────────
Typecheck/Build : ✅ 0 errors | ❌ N errors | — (not configured)
Lint            : ✅ 0 warnings | ❌ N warnings | — (not configured)
Tests before    : N passing / M failing
Tests after     : N passing / M failing  → ✅ no regression | ❌ regression
New tests       : N files
  - {config.pasta_testes[x]}/....test.*

────────────────────────────────────────────────────────
 FILES CREATED / MODIFIED
────────────────────────────────────────────────────────
CREATE     src/screens/...
MODIFY     src/services/...
DOCS       planning/onda-{number}/
PLAN       planning/onda-{number}/

────────────────────────────────────────────────────────
 REDMINE UPDATED
────────────────────────────────────────────────────────
✅ Status: In Progress → Done (QA moves to Testing on start)
✅ Public completion note added ("Fix applied")

────────────────────────────────────────────────────────
 MANUAL TEST (QA)
────────────────────────────────────────────────────────
See: planning/onda-{number}/3-checklist.md — Test Section
════════════════════════════════════════════════════════
```
