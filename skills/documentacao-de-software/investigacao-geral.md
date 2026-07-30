# Guide 1: General Investigation and Planning (Discovery Phase)

## 1. Initialization Principles

The investigation must not be based on assumptions. The agent must map the ecosystem (backend, frontend, infrastructure, database) to understand the context before writing any line of functional requirements.

## 2. Ecosystem Scanning and Atomic Requirement Identification

The agent must scan the folder structure, technologies (tech stack), and architectural patterns (e.g., MVC, REST APIs, Workers, Messaging). During this superficial investigation, the agent must mandatorily identify systemic requirements following the atomic criterion:

* **APIs:** Each detected endpoint is listed as a requirement.
* **Frontend (MVC/Pages):** Each triggered route is a requirement (separating `GET` routes from `POST/PUT` routes).
* **Integrations:** Each communication operation with external systems is a requirement.
* **Queues/Messaging:** Each consumed or published queue is listed separately as a requirement.
* **Background Services/Jobs:** Each mapped worker, daemon, or cron job is an autonomous requirement.

## 3. Target File Generation (`investigacao-alvos.yaml`)

Based on the granular scanning above, the agent must generate the targets document (`investigacao-alvos.yaml`) which will serve as a structured backlog. The YAML structure must contain:

* **File List:** Full paths.
* **Isolated Requirements Sub-list:** Explicit grouping by Frontend Routes, API Endpoints, Integration Contracts, Message Queues, and Background Services (Jobs/Workers).

## 4. Wave-Based Execution Planning (BLOCKING)

Every investigation must be planned in advance using the `planning-and-task-breakdown` skill.

* The agent will formulate a plan in dynamic waves based on the YAML (e.g., Wave 1 - Integrations, Wave 2 - Queues and Workers, Wave 3 - Endpoints, Wave 4 - Frontend Routes).
* **Complexity Division:** If there are a large number of database routines, multiple queues, or dozens of identified routes/endpoints, the agent must break the topic into multiple waves.
* **Explicit Approval:** The plan must be presented to the user. It is absolutely unacceptable to begin the deep investigation (Guide 2) without explicit consent.
