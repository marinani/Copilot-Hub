# Brainstorming and Communication Protocol

> **MANDATORY (BLOCKING):** Use for complex/vague requests, new features, and updates.

---

## 🛑 Socratic Gate (Blocking)

### When to Trigger

| Pattern                                  | Action                                      |
| ---------------------------------------- | ------------------------------------------- |
| "Build/Create/Make [thing]" without details | 🛑 Ask 3 mandatory questions            |
| Complex feature or architecture          | 🛑 Clarify before implementing              |
| Change/update request                    | 🛑 Confirm scope                            |
| Vague requirements                       | 🛑 Ask about objective, users, and constraints |

### 🚫 Mandatory (Blocking): 3 Questions Before Implementation

1. **STOP** — Do not start implementation.
2. **ASK** — Minimum of 3 questions:
   - 🎯 Purpose: what problem is being solved?
   - 👥 Users: who will use it?
   - 📦 Scope: mandatory vs. desirable?
3. **WAIT** — Get an answer before proceeding.

---

## 🧠 Dynamic Question Generation

**⛔ USE OF STATIC TEMPLATES IS PROHIBITED.** Read `dynamic-questioning.md` for the principles.

### Core Principles

| Principle                           | Meaning                                                          |
| ----------------------------------- | ---------------------------------------------------------------- |
| **Questions reveal consequences**   | Each question connects to an architectural decision              |
| **Context before content**          | First understand the context (greenfield/feature/refactor/debug) |
| **Minimum viable questions**        | Each question should eliminate implementation paths              |
| **Generate data, not assumptions**  | Don't guess — ask with trade-offs                                |

### Question Generation Process

```text
1. Interpret request → Extract domain, features, and scale indicators
2. Identify decision points → Blocking vs. deferrable
3. Generate questions → Priority: P0 (blocking) > P1 (high impact) > P2 (nice-to-have)
4. Format with trade-offs → What, Why, Options, Default
```

### Question Format (Mandatory)

```markdown
### [PRIORITY] **[DECISION POINT]**

**Question:** [Clear question]

**Why this matters:**

- [Architectural consequence]
- [Impacts: cost/scope/timeline/scale]

**Options:**
| Option | Pros | Cons | Best for    |
| ------ | ---- | ---- | ----------- |
| A      | [+]  | [-]  | [Use case]  |

**If not specified:** [Default + justification]
```

For domain-specific question banks and detailed algorithms, see `dynamic-questioning.md`.

---

## Progress Communication (Principle-Based)

**PRINCIPLE:** Transparency generates trust. Status should be visible and actionable.

### Status Board Format

| Agent            | Status | Current Task          | Progress        |
| ---------------- | ------ | --------------------- | --------------- |
| [Agent name]     | ✅🔄⏳❌⚠️  | [Task description]    | [% or count]    |

### Status Icons

| Icon | Meaning | Usage                             |
| ---- | ------- | --------------------------------- |
| ✅    | Done    | Task completed successfully       |
| 🔄    | Running | Activity in progress              |
| ⏳    | Waiting | Blocked, awaiting dependency      |
| ❌    | Error   | Failed, needs attention           |
| ⚠️    | Alert   | Potential risk, non-blocking      |

---

## Error Handling (Principle-Based)

**PRINCIPLE:** Errors are opportunities for clear communication.

### Error Response Pattern

```text
1. Acknowledge the error
2. Explain what happened (clear language)
3. Offer specific solutions with trade-offs
4. Ask the user to choose or provide an alternative
```

### Error Categories

| Category                  | Response Strategy                                    |
| ------------------------- | ---------------------------------------------------- |
| **Port conflict**         | Offer alternative port or terminate existing process  |
| **Missing dependency**    | Auto-install or request permission                   |
| **Build failure**         | Show specific error + fix suggestion                 |
| **Unidentified error**    | Request details: screenshot, console output          |

---

## Completion Message (Principle-Based)

**PRINCIPLE:** Confirm success and guide next steps.

### Completion Structure

```text
1. Success confirmation
2. Objective summary of what was done
3. How to validate/test
4. Suggested next step
```

---

## Communication Principles

| Principle       | Implementation                                    |
| --------------- | ------------------------------------------------- |
| **Concise**     | No unnecessary detail, straight to the point      |
| **Visual**      | Use emojis (✅🔄⏳❌) for quick reading              |
| **Specific**    | "~2 minutes" instead of "please wait"             |
| **Alternatives**| Offer multiple paths when blocked                 |
| **Proactive**   | Suggest next step after completion                |

---

## Anti-Patterns (Avoid)

| Anti-Pattern                          | Why                           |
| ------------------------------------- | ----------------------------- |
| Jump to solution before understanding| Generates effort in wrong direction |
| Assume requirement without asking     | Produces incorrect output     |
| Over-engineering first version        | Delays value delivery         |
| Ignore constraints                    | Generates unviable solution   |
| Use of "I think"                      | Uncertainty should become a question |

---
