# Functional Requirements — Master Document

> **Single source of truth** for all Functional Requirements (FR) of the project.
> Numbering is **global and continuous** — never restarts per requirement.
> Every FR creation or change must occur **in this file first**, then be replicated to the documents that use it.

## Metadata

| Field  | Value                                                               |
|--------|---------------------------------------------------------------------|
| Version | 1.0                                                                 |
| Date   | DD/MM/YYYY                                                          |
| Author | [Full name — "AI", "Copilot", "Automated" or similar is prohibited] |

---

## How to Use This Document (Blocking Rule)

1. **Before creating an FR in ANY req-XXXX:** you MUST open this file and check the "Next available number". **Never assume numbering starts at RF-0001** — it is continuous throughout the project.
2. **When creating an FR:** add the entry in this document with all fields filled in FIRST, then update the "Next available number" field to the following number.
3. **When referencing an FR in another document:** copy the description exactly as it appears here and update "Documents that use it".
4. **When modifying an FR:** update this document first, then replicate the change to all documents listed in "Documents that use it". Record in the history.

> **Frequent error:** creating req-0002 with RF-0001 without consulting this master. If req-0001 already used RF-0001 and RF-0002, req-0002 must start from RF-0003.

---

## Next available number: RF-0001

---

## Functional Requirements

### RF-0001 — [Short title of the functional requirement]

| Field                  | Value                         |
|------------------------|-------------------------------|
| Source Requirement     | req-XXXX                      |
| Priority               | High / Medium / Low           |
| Documents that use it  | req-XXXX, tec-req-XXXX       |

**Description:**
[Complete and unambiguous description of the functional requirement. It must be self-sufficient — any reader should understand what the system must do without consulting other documents.]

---

> Add new FRs below, following the pattern above and maintaining sequential numbering.

---

## Change History

| Version | Date       | Author | Description           |
|---------|------------|--------|-----------------------|
| 1.0     | DD/MM/YYYY |        | Document creation     |
