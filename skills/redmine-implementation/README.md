# Skill: RedmineImplementation

This skill implements a complete workflow for responding to Redmine tickets directly within the repository, using MCP to fetch/update issues and maintaining planning history in `planning/wave-<number>/`.

## When to use

Use this skill when you need to:

- Analyze a Redmine ticket (issue) and validate whether it belongs to the correct project.
- Verify whether the ticket is assigned to the correct developer.
- Define an implementation and test plan based on the issue description.
- Implement code changes and follow up on Redmine (update status, notes, etc.).

It can be triggered by sending something like:

```text
redmine: #168856
chamado: #168856
```

## What it does

Executing this skill performs a structured flow that includes:

1. Initial validations (project, assignee, issue status).
2. Description analysis and type classification (bug, improvement, feature).
3. Automatic artifact creation in `planning/wave-<number>/` (issue, analysis, plan, etc.).
4. Codebase inspection to identify files and potential points of change.
5. **Developer interaction via handoff at critical decision points (validation gates)**.
6. Status and notes updates on Redmine as progress is made.

## Generated file structure

The skill creates and maintains a set of artifacts in:

- `planning/wave-<number>/0-issue.md` (issue data and classification)
- `planning/wave-<number>/1-analysis.md` (codebase analysis)
- `planning/wave-<number>/1-plan.md` (implementation plan)
- `planning/wave-<number>/2-checklist.md` (checklist and test plan)
- `planning/wave-<number>/5-test-execution.md` (test results and validation)

## Prerequisites

### Python

- **Python installed and available in PATH**. If Python is not available, the skill will warn and offer to install it automatically (after user confirmation).

### REDMINE_API_KEY

- **Permanently configured on Windows** via `setx REDMINE_API_KEY "..."` command to be available in any terminal/project.
- Will be requested via **handoff** in the chat if not configured.
- **Never** store it in `.github/config.yaml` (it is a sensitive credential).

### Configuration file

- The `.github/config.yaml` file stores **only Redmine project information**:
  - `project_name` (project name, required)
  - `project_id` (project identifier, auto-filled)
  - `project_id_numeric` (numeric ID, auto-filled)
  - `status_ids` (status mapping, auto-updated from API)
- Will be created automatically on first execution if it does not exist.

### Permissions

- Appropriate permissions to read/update issues in Redmine.

## Configuration behavior

- **REDMINE_API_KEY**: requested via **handoff** when missing → stored in OS with `setx` → set in current session with `$env:REDMINE_API_KEY = "..."`
- **project_name**: requested via **handoff** when missing → stored in `.github/config.yaml` (`redmine` section)
- **project_id and status_ids**: auto-populated from the Redmine API
- **user_login**: determined at each execution from the OS logged-in user, but **never** saved to config

## Interactive Gates (Handoff)

The skill implements 3 mandatory gates where the agent **waits for developer response via handoff**:

1. **STEP 4** — After codebase analysis: developer supplements the understanding of the issue
2. **STEP 7** — After generating the plan: developer confirms readiness to begin implementation
3. **STEP 9** — After automated checks: developer confirms the code has been manually tested

At each gate, the agent emits the question and ends the message, waiting for the developer's next response without advancing in the same message.

## Chat output

The agent formats responses in a structured way for better readability:

- **Ticket/card list**: displayed as a **Markdown table** (columns: ID, title, status, assignee, priority, update date).
- **Ticket detail**: displayed as a **chat-embedded card**, with fields and sections clearly separated.

## Important notes

- UI messages and generated documentation are in **English**.
- The skill must not introduce external dependencies without explicit decision.
- If the `planning-and-task-breakdown` skill is available, it is mandatory for generating/maintaining artifacts in `planning/`.
- The issue is only marked as **Done** when all checklist tasks are complete AND all tests pass.
- If there is a blocker during implementation, the status changes to **Impediments** and the issue is not closed.
- Sensitive credentials (**REDMINE_API_KEY**) always remain **in the OS environment**, never in versioned configuration files.
