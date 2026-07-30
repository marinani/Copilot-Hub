# Clarification Skill — Structured Specification Disambiguation

> **When to use (MANDATORY):** Vague specifications, complex features, incomplete requirements, before implementation or planning.

---

## What This Skill Does

1. **Coverage Scan:** Analyzes the specification in 10 categories (functional scope, data model, UX, non-functional, integrations, edge cases, constraints, terminology, completion signals, and placeholders).
2. **Question Generation:** Creates up to 5 questions prioritized by impact × uncertainty, with multiple-choice or short answers.
3. **Sequential Interaction via Handoff:** Presents ONE question at a time in chat with technical recommendation, options, and answer validation.
4. **Incremental Integration:** After each answer, updates the specification with history, applied clarifications, and term normalization.
5. **Final Report:** Summarizes questions, updated sections, and final coverage.

---

## Question Structure

### Category Taxonomy

```text
├── Scope and Functional Behavior
│   ├── Core user objectives and success criteria
│   ├── Explicit out-of-scope declarations
│   └── Differences between roles/personas
├── Domain and Data Model
│   ├── Entities, attributes, and relationships
│   ├── Identity and uniqueness rules
│   ├── Lifecycle and state transitions
│   └── Volume and scale assumptions
├── Interaction and UX Flow
│   ├── Critical journeys and sequences
│   ├── Error/empty/loading states
│   └── Accessibility and localization notes
├── Non-Functional Quality Attributes
│   ├── Performance (latency, throughput)
│   ├── Scalability (horizontal/vertical, limits)
│   ├── Reliability and availability
│   ├── Observability (logs, metrics, tracing)
│   ├── Security and privacy (authN/Z, data protection)
│   └── Regulatory/compliance constraints
├── Integrations and External Dependencies
│   ├── External services/APIs and failure modes
│   ├── Import/export formats
│   └── Protocol/versioning assumptions
├── Edge Cases and Failure Handling
│   ├── Negative scenarios
│   ├── Rate limiting / throttling
│   └── Conflict resolution (concurrent edits)
├── Constraints and Trade-offs
│   ├── Technical constraints (language, storage, hosting)
│   └── Explicit trade-offs and rejected alternatives
├── Terminology and Consistency
│   ├── Canonical glossary
│   └── Avoided synonyms / deprecated terms
├── Completion Signals
│   ├── Testability of acceptance criteria
│   └── Measurable definition of done
└── Placeholders / Pending Items
    ├── TODO markers / pending decisions
    └── Vague adjectives without quantification
```

### Question Quality Criteria

✅ **Include when:**

- The answer materially impacts architecture, data model, task decomposition, test design, UX, or operational readiness.
- It reduces downstream rework risk.
- It prevents misalignment in acceptance tests.

❌ **Exclude when:**

- The point is better postponed to planning.
- It does not impact implementation/validation strategy.
- It is purely stylistic or trivial.

---

## Interaction Flow with Handoff

### Step 1: Load and Analyze the Specification

```text
Specification → Structured Scan → Coverage Map (internal)
                                  ├── Clear ✅
                                  ├── Partial ⚠️
                                  └── Missing ❌
```

### Step 2: Generate Prioritized Questions

```text
Partial/Missing Categories → Question Candidates → Prioritization (Impact × Uncertainty)
                                                   ↓
                                         Max. 5 questions selected
```

### Step 3: Question-Answer Loop (Interactive Handoff)

**Multiple-choice question format:**

```markdown
### [PRIORITY] **[DECISION POINT]**

**Question:** [Clear and specific question]

**Recommended:** Option [X] - [1-2 line technical justification]

| Options | Description              |
| ------- | ------------------------ |
| A       | [Description of option A] |
| B       | [Description of option B] |
| C       | [Description of option C] |

**Answer with:** Option letter (e.g., "A"), "yes"/"recommended" to accept,
or short custom answer (≤5 words).
```

**Short open-ended question format:**

```markdown
### [PRIORITY] **[DECISION POINT]**

**Question:** [Clear question]

**Suggested:** [Default answer] - [Technical justification]

**Format:** short answer (≤5 words).
Answer "yes"/"suggested" to accept, or your own answer.
```

### Step 4: Validation and Integration

After answer acceptance:

1. ✅ Validate answer (multiple-choice or ≤5 words).
2. 📝 Record in session memory.
3. 📄 Apply to the relevant specification section.
4. 💾 Save file atomically.
5. ➡️ Proceed to the next question.

### Step 5: Final Report

```text
Questions asked: N/5 ✅
File path: [path]
Modified sections: [list]

Final coverage:
├── Clear       ✅ [N categories]
├── Resolved    ⚡ [N categories updated]
├── Postponed   ⏳ [N categories + justification]
└── Pending     ❌ [N categories + justification]

Suggested next command: [recommendation]
```

---

## Specification Update Structure

### `## Updates` Section

#### Automatic Creation (First Clarification)

```markdown
## Updates

| Update Date   | Update Author       | Update Description                                    |
| ------------- | ------------------- | ----------------------------------------------------- |
| 03/19/2026    | AI Clarification Bot | Clarification incorporated: Q: [question] → A: [answer] |
| ...           | ...                 | ...                                                   |

### Session 2026-03-19

- Q: [question 1] → A: [answer 1]
- Q: [question 2] → A: [answer 2]
```

#### Integration Rule by Category

| Ambiguity Category    | Target Section                           | Action                                                   |
| --------------------- | ---------------------------------------- | -------------------------------------------------------- |
| Functional scope      | `## Functional Requirements`             | Add/clarify bullet                                       |
| Actor distinction     | `## User Stories` or `## Actors`         | Update role, constraint, and scenario                    |
| Data model            | `## Data Model`                          | Add fields, types, relationships, and rules              |
| Vague non-functional  | `## Non-Functional / Quality Attributes` | Convert adjective to explicit metric                     |
| Edge case/error       | `## Edge Cases / Error Handling`         | New bullet or subsection                                 |
| Terminology           | All (normalization)                      | Replace term and preserve origin when applicable         |

#### Post-Integration Validation

- ✅ One bullet per accepted answer (no duplicates).
- ✅ Total questions ≤ 5.
- ✅ No obsolete vague placeholders (e.g., "robust", "intuitive" without quantification).
- ✅ No contradictions (invalidated assertions must be removed).
- ✅ Valid Markdown; new headings consistent.
- ✅ Canonical terminology consistent throughout the document.

---

## Behavioral Rules

### ✅ Proceed with Caution

- Always confirm: "No critical ambiguity detected?" before skipping clarification.
- If the specification file does not exist, instruct the user to create it first.
- Maximum 5 questions per session; retries of the same question do not count as new questions.

### ❌ Avoid

- Speculative stack questions (except when blocking functionality).
- Stylistic/preference/trivial questions.
- More than 5 questions per session.
- Contradictions with already accepted answers.

### ⚠️ Termination Signals

Terminate when:

- All critical ambiguities are resolved.
- User signals "ready", "done", "finished", "no more questions".
- The 5-question limit is reached.
- There are no significant remaining questions.

### 📢 Incomplete Conclusion

If the 5-question limit is reached with high-impact ambiguities:

- List items as **Postponed** with justification.
- Recommend running `/clarification` again after planning/design.

---

## VS Code Chat Handoff Integration

### Chat Invocation

```markdown
/clarification [path/to/specification.md]
```

**Examples:**

- `/clarification documentacao/features/login.md`
- `/clarification src/specs/payment-integration.md`

### Interactive Flow

1. First message: analysis + 1st question.
2. User response: validation + integration + 2nd question.
3. Repeat: until completion/stop signal.
4. Last message: final report + next steps.

### Failsafe: No Ambiguity

```text
Analysis complete.

| Category                         | Status  |
| -------------------------------- | ------- |
| Scope and functional behavior    | ✅ Clear |
| Domain and data model            | ✅ Clear |
| ...                              | ✅ Clear |

No critical ambiguity detected.
The specification is ready for implementation.

Next: proceed to planning/design or run /architecture.
```

---

## References

- **Original prompt:** `.github/prompts/clarify.prompt.md`
- **Specification file:** provided by the user or automatically identified
- **Output:** updated specification + clarification history

---

## Troubleshooting

### "File Not Found"

```text
❌ I could not find the specification at [path].

Options:
1. Provide the correct path: /clarification [correct/path]
2. Create the specification first:
   - Use /featurize or /spec-driven-workflow
   - Then run /clarification
```

### "Ambiguous Answer"

```text
❌ Response unclear. You answered: "[answer]"

Expected options: A, B, C, D, or short answer (≤5 words).

Rephrase your answer or choose an option.
```

### "Question Limit Reached with Remaining Ambiguities"

```text
⚠️ 5-question limit reached. Categories still ambiguous:
- [Category A]: [Postponement justification]
- [Category B]: ...

Recommendation: run /clarification again after planning/design
to refine these areas.
```

---

## When to Use This Skill

✅ **Use when:**

- The specification is incomplete or vague.
- Before starting planning/design.
- Collected requirements need refinement.
- There are multiple possible interpretations.
- You want to reduce rework risk before implementation.
- Acceptance tests are not yet clear.

❌ **Do not use when:**

- The specification is complete and aligned.
- It is an exploratory spike (may skip, but warn of increased risk).
- It is a simple bugfix or small task.

---

## Complete Session Example

**User:**

```text
/clarification documentacao/features/user-authentication.md
```

**Bot (analysis + 1st question):**

```text
## Coverage Analysis

Specification: documentacao/features/user-authentication.md

| Category         | Status    |
| ---------------- | --------- |
| Functional scope | ⚠️ Partial |
| Domain and data  | ⚠️ Partial |
| Interaction/UX   | ✅ Clear   |
| Non-functional   | ❌ Missing  |
| ...              | ...       |

5 prioritized questions generated. Starting loop...

---

### **P0 - Password Storage and Hashing**

**Question:** What is the minimum requirement for password storage?

**Recommended:** Option A - PBKDF2 is a solid standard for authentication
with broad support in enterprise frameworks.

| Options | Description                                          |
| ------- | ---------------------------------------------------- |
| A       | PBKDF2 (or bcrypt equivalent) with 10k+ iterations   |
| B       | SHA-256 with salt (less robust for this scenario)     |
| C       | Plain text with TLS                                  |
| D       | HSM with PKI                                         |

**Answer with:** letter (e.g., "A"), "yes"/"recommended", or short answer (≤5 words).
```

**User:**

```text
A
```

**Bot (integration + 2nd question):**

```text
✅ Answer recorded: PBKDF2 (or bcrypt equivalent) with 10k+ iterations

Integrating... file updated.

| Date       | Author               | Description                                          |
| ---------- | -------------------- | ---------------------------------------------------- |
| 03/19/2026 | AI Clarification Bot | Q: storage requirement? → A: PBKDF2 with 10k+        |

**Updated Section:** Non-Functional → Security and Privacy
- Password hashing: PBKDF2 (or bcrypt equivalent) with ≥10,000 iterations

---

### **P1 - 2FA Requirement**

**Question:** Is 2FA mandatory for all users or optional?

**Recommended:** Option B - gradual adoption with lower initial friction.
```

**[Continues until 5 questions or completion]**

**Bot (final report):**

```text
## ✅ Clarifications Complete

**Questions:** 3 of 5 asked and answered

**File:** documentacao/features/user-authentication.md

**Updated Sections:**
- Functional Requirements (2 clarifications)
- Non-Functional / Security (1 clarification)
- Data Model (0 clarifications)

**Final Coverage:**

| Category         | Status      | Notes                            |
| ---------------- | ----------- | -------------------------------- |
| Functional scope | ✅ Clear     | Resolved: roles and scope        |
| Domain and data  | ⚠️ Partial   | Postponed: 2FA structure         |
| Interaction/UX   | ✅ Clear     | Already covered                  |
| Non-functional   | ✅ Resolved  | Hash and 2FA scope added         |

**Postponed:**
- Email verification flow (exceeds quota, refine in design)
- IP/user rate limiting (low impact, planning decision)

**Recommended Next Command:**
/planning-and-task-breakdown documentacao/features/user-authentication.md

Or, to deepen remaining ambiguities:
/clarification documentacao/features/user-authentication.md
```

---

## Version History

| Version | Date       | Changes                                                  |
| ------- | ---------- | -------------------------------------------------------- |
| 1.0     | 03/19/2026 | Initial skill, derived from `clarify.prompt.md` with handoff |
