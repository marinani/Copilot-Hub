# System Risk Matrix

## Metadata

- **Document code:** `matriz-risco-sistema`
- **Title:** Global System Risk Matrix
- **Creation date:** DD/MM/YYYY
- **Last update:** DD/MM/YYYY
- **Author:** Author name
- **Version:** 1.0.0
- **Status:** Draft | In review | Approved

> This is the unique system risk matrix document and must be updated whenever a requirement is included, changed, or removed.

## Purpose

Consolidate and prioritize risks across the entire system based on impact and probability.

## Assessment Scale

### Impact

| Level | Description   |
| ----- | ------------- |
| 1     | Very low      |
| 2     | Low           |
| 3     | Medium        |
| 4     | High          |
| 5     | Critical      |

### Probability

| Level | Description        |
| ----- | ------------------ |
| 1     | Very unlikely      |
| 2     | Unlikely           |
| 3     | Possible           |
| 4     | Likely             |
| 5     | Almost certain     |

### Score Classification

- **Low:** 1 to 6
- **Medium:** 8 to 12
- **High:** 15 to 19
- **Critical:** 20 to 25

$$\text{Risk Score} = \text{Impact} \times \text{Probability}$$

## Global Risk Matrix

| Risk ID   | Related Requirement(s) | Risk Description | Impact (1-5) | Probability (1-5) | Score (I×P) | Level | Mitigation | Responsible | Status  |
| --------- | ---------------------- | ---------------- | ------------ | ----------------- | ----------- | ----- | ---------- | ----------- | ------- |
| RSK-0001  | REQ-XXXX               | Describe risk    | -            | -                 | -           | -     | -          | -           | Open    |

## Maintenance Rules

1. Every update to `req-XXXX-...md` must update this document.
2. The requirement must contain a local section with only directly related risks/requirements.
3. The local section must reference the global items in this document (e.g., `RSK-0001`).
4. Do not duplicate risk: update the existing item when it is the same context.

## Change History

| Date       | Author | Version | Change               |
| ---------- | ------ | ------- | -------------------- |
| DD/MM/YYYY | Name   | 1.0.0   | Document creation    |

## Clarifications

- Assumptions considered:
- Pending questions:
- Decisions made:
