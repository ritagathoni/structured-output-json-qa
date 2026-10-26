# Structured Output & JSON QA

**Focus:** schema compliance, field validation, conditional business policies and function-call quality.

## Executive summary
A response can contain plausible content but fail machine consumption because it lacks required fields, returns a string where a number is expected, or omits approval logic. This project demonstrates a transparent validator for **synthetic enterprise-style records**.

## Architecture
`data/outputs.json` (candidate payloads) → `src/validator.py` (type/required/enum/extra-field checks) → business rules → diagnostic output. A separate function checks tool selection and required function arguments.

## Run
```bash
python -m src.validator
python -m unittest discover -s tests -v
```

## Failure taxonomy
| Category | Example | Severity rationale |
|---|---|---|
| Type error | Boolean where a number is expected | Parser/consumer mismatch |
| Missing field | `deal_id` absent | Incomplete contract |
| Unexpected field | Undeclared property | Schema drift |
| Conditional policy | Approved without approver | Invalid business conclusion |
| Function call | Wrong tool or missing argument | Workflow failure |

## Important technical boundary
The included validator deliberately implements **a documented subset** of JSON Schema (`type`, `required`, `properties`, `enum`, `items`, `additionalProperties`). It is not a full standards-compliant JSON Schema implementation. In production, use a maintained JSON Schema library and pin a supported schema draft. Record business-rule versions and test complex nested/conditional constraints.

## Research extensions
- Multi-step function-call traces and argument provenance.
- `oneOf`/`anyOf`/`if-then-else` using a full JSON Schema validator.
- Fuzzing edge values, null handling and malformed JSON.
- Error severity, traceability IDs and longitudinal quality trends.

## Skills demonstrated
JSON · Structured outputs · Schema validation · Python · Function calling · Business-rule QA · Error analysis

# Scope and evidence

This is a **synthetic, independently developed demonstration**, not a reproduction of confidential employer data. All prompts, labels, examples, names and records are fabricated for demonstration. Sample counts and test outcomes are software demonstrations, **not historical workplace impact statistics**.

The repository demonstrates evaluation methodology and runnable code; it does not certify that the author achieved a specific result at a named client.

