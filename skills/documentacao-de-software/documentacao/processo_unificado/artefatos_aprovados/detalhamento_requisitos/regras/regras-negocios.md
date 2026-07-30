# Business Rules — Master Document

> **Single source of truth** for all Business Rules (BR) of the project.
> Numbering is **global and continuous** — never restarts per requirement.
> Every BR creation or change must occur **in this file first**, then be replicated to the documents that use it.

## Metadata

| Field  | Value                                                               |
|--------|---------------------------------------------------------------------|
| Version | 1.0                                                                 |
| Date   | DD/MM/YYYY                                                          |
| Author | [Full name — "AI", "Copilot", "Automated" or similar is prohibited] |

---

## How to Use This Document (Blocking Rule)

1. **Before creating a BR in ANY req-XXXX:** you MUST open this file and check the "Next available number". **Never assume numbering starts at RN-0001** — it is continuous throughout the project.
2. **When creating a BR:** add the entry in this document with all fields filled in FIRST, then update the "Next available number" field to the following number.
3. **When referencing a BR in another document:** copy the description exactly as it appears here and update "Documents that use it".
4. **When modifying a BR:** update this document first, then replicate the change to all documents listed in "Documents that use it". Record in the history.

> **Frequent error:** creating req-0002 with RN-0001 without consulting this master. If req-0001 already used RN-0001, req-0002 must start from RN-0002.

---

## Next available number: RN-0001

---

## Business Rules

### RN-0001 — [Short title of the business rule]

| Field                   | Value                         |
|-------------------------|-------------------------------|
| Source Requirement      | req-XXXX                      |
| Impact                  | [Describe functional impact]  |
| Documents that use it   | req-XXXX, tec-req-XXXX        |

**Description:**
[Complete and unambiguous description of the business rule. It must be precise, verifiable, and free of ambiguities. Example: "The maximum discount allowed per order is 30% of the total value. Discounts above this limit require manager approval."]

---

> Add new BRs below, following the pattern above and maintaining sequential numbering.

---

## Change History

| Version | Date       | Author | Description           |
|---------|------------|--------|-----------------------|
| 1.0     | DD/MM/YYYY |        | Document creation     |
