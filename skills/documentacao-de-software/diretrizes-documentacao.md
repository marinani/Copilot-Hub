# Documentation Guidelines, Templates, Risk, and FPA

## 1. Template Integrity and Eight Quality Criteria

It is strictly prohibited to alter the structural format of templates during updates to existing documents.

Structural integrity blocking rule:

- Do not alter heading/subheading hierarchy.
- Do not alter section order.
- Do not alter table structure (columns, order, header).
- Do not remove/rename mandatory sections.
- Do not convert document format into routine update tasks.

During updates, only content changes are allowed:

- Filling in/adjusting text and fields;
- Updating data rows in existing tables;
- Updating version and change history.

Every documented requirement (`req-XXXX`) must pass the **8 Quality Criteria**:

1. **Correct:** The requirement reflects a real need.
2. **Precise:** Has a single, unambiguous interpretation.
3. **Complete:** Covers normal flows, exceptions, and responses to invalid inputs.
4. **Consistent:** No conflicts with other requirements.
5. **Prioritized:** Classified as Essential, Desirable, or Optional.
6. **Verifiable:** The requirement can be objectively tested. Use of vague qualitative terms is prohibited (e.g., "easy", "fast").
7. **Modifiable:** Written without redundancies.
8. **Traceable:** Linked to impacted artifacts.

## 2. Requirement Granularity and Identification (Scope Rule)

During the investigation and documentation phase, the identification of systemic requirements must follow strict, atomic granularity. The division rule is as follows:

- **APIs (Backend):** Each individual API endpoint must be considered and documented as a unique, independent requirement.
- **Systems with Frontend (e.g., MVC pattern):** Each application interaction route must be considered a requirement. For example: in the scope of a "Person Registration", the `GET` endpoint/route responsible for loading and displaying the form page is **one requirement**, and the `POST` endpoint/route triggered to save the data entered in the form is **another distinct requirement**.
- **External Integrations:** For each integration with external systems, a mandatory and independent requirement must be documented. If the integration has multiple actions (search, insert, update), each operation generates its own isolated requirement.
- **Background Services (Jobs/Workers):** Each service, routine, or job that runs in the background (whether scheduled via CRON or continuous execution) must be considered and documented as an independent requirement.
- **Queues and Messaging:** Each queue or interactive topic must be considered a requirement. A consumer routine of a queue is a requirement; a publisher routine with a distinct business purpose is also considered an independent requirement.

## 3. UI/UX and Messaging Guidelines

Every requirement with user interaction MUST have wireframes. **req-XXXX:** generate a PNG image of the interface; include ASCII wireframe ONLY as fallback if PNG is not possible. **tec-req-XXXX:** BOTH ASCII wireframe (embedded) AND PNG image (referenced) are mandatory. Follow `padrao-visual.md`. For wireframe/mockup image generation, the `design-lead` agent must be invoked. If `design-lead` is not available, use available design skills and the `capture-mockup.cjs` script as a fallback.

- **System Messages:** Error message wording must be **positive, polite, and non-threatening**. Documenting messages that blame the user is prohibited (e.g., "fatal error", "illegal operation"). The message should inform about the problem and suggest corrective action.
- **Error Prevention:** Documentation must account for disabling invalid options at each interface state to prevent user errors.
- **Reversibility:** Document whether the system allows undoing the action (Undo/Redo).

## 4. Risk Matrix Management

Mandatory format in Markdown Table:

- **Global Matrix (`matriz-risco-sistema.md`):** Evaluates technical debt and architecture.
- **Local GUT Matrix (`tec-req`):** Prioritizes technical issues of the requirement (Severity × Urgency × Trend, scale 1 to 5).
- **Impact × Probability Matrix (`req`):** Business risks (scale 1 to 5). Calculation: `Score = Impact × Probability`.

## 5. Advanced FPA: Transactional, DW, and ETL

The creation of `apf-req-XXXX.md` is blocking and must follow:

- **ALI / AIE (Data):** Based on Data Types (ERD) and Logical Records (RLR).
- **EE / SE / CE (Transactional):** Based on ERDs and Referenced Files (ALR).

**Strict rules for BI / Data Warehouse (DW) / ETL Projects:**

- **ALI:** Count 1 ALI for each Fact, Dimension, and Aggregation table. *Static Dimensions (Code Data) do not score.*
- **AIE:** Count 1 AIE for source system tables read, or Shared Dimensions consulted to validate data in ETL.
- **EE (Load/ETL):** Count 1 EE of medium complexity for the data load of each ALI (Fact or Dimension). If there is a *Full* and *Incremental* load requirement for the same table, count two EEs.
- **SE / CE (Presentation):** Count 1 SE for each Cube generated. Count 1 SE or CE for pre-defined reports.
