---
name: Requirement Change Estimation (Bottom-Up) v2
description: "Generate technical estimates for one or more requirements, with percentage validation, multiple hour format support, and markdown file generation."
---

# Skill: Requirement Change Estimation (Bottom-Up) v2

## Objective

Generate a technical estimate for **one or more functional requirements**, following the rules of the `Estimativa-Bottom-Up-1.3.xlsx` spreadsheet, with percentage validation, multiple hour format support, and markdown file generation.

## Supported Hour Formats

- `hh:mm` e.g. `03:30` (3 hours and 30 minutes)
- `h` decimal e.g. `3.5`
- `X days, hh:mm` e.g. `2 days, 02:00` (50 hours)

## Markdown File Structure

The template `estimativas/estimativa-template.md` must be used as the mandatory structure for generating the estimate file, filling in the sections with the provided information.

## Automatic Validation Rules

1. **Per requirement:** `Total Hours = RequirementsEngineering + Implementation + Testing + DataScientist`
2. **Per activity (aggregate):** `%Activity = TotalHoursActivity / TotalHoursRequirements * 100`
3. **Limits:**
   - Requirements Engineering: 40% or less
   - Implementation: 75% or less
   - Testing: 20% or less
   - Data Scientist: 10% or less
4. **Acceptance and Deployment:** calculated separately, applied to the total requirements or to an explicitly provided value
5. **If type = IMPROVEMENT:** suggest lower weights for requirements engineering (e.g., 20% instead of 40%)

## Expected Behavior

- **Multiple requirements:** allows adding N rows to the table
- **Automatic calculation:** sums all rows and generates totals
- **Visual alert:** warning when percentage exceeds limit
- **Automatic conversion:** converts `2 days, 02:00` to `50:00`
- **File generation:** `estimativa-req-XXXX-{YYYY-MM-DD-HHmmSS}.md`

## Advanced Usage Example

> "Create an estimate with 2 requirements:
>
> 1. REQ001 - Maintain User (Improvement) - 3h engineering, 12h implementation, 3.5h testing
> 2. REQ012 - Address API (New) - 7h engineering, 2 days, 2:00 implementation, 15h testing
>    Client: ABC, System: Portal, Technology: DotNet"

The skill must:

- Convert `2 days, 02:00` to `50:00`
- Sum both requirements
- Validate percentages
- Generate the markdown with two rows in the table

---

## Summary of Proposed Improvements

| Gap                                  | Improvement                               |
| ------------------------------------ | ----------------------------------------- |
| Only one requirement                 | Multiple requirement support              |
| Mixed acceptance/deployment          | Separate section with specific limits     |
| No limit comparison                  | "Status" column with check/warning icons  |
| `2 days, 2:00:00` format            | Automatic conversion to hours             |
| No rules by type                     | Different rules for IMPROVEMENT vs NEW    |
| No sum validation                    | Per-row and total validation              |
| Missing explicit data scientist      | Dedicated column in the table             |

---
