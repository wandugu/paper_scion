# Schema Normalization

## RE

| Key | Value |
| --- | --- |
| direction_policy | directed |
| symmetric_policy | none |
| missing_type_policy | Entity |
| type_path_policy | keep_atomic |
| label_for_embedding | replace '/' -> ' ' |

## EE

| Key | Value |
| --- | --- |
| label_casing_en | lower |
| separator_policy | collapse_whitespace + unify(_,-) |
| edge_form | (event_type, role, ARG) |
| ARG_semantics | placeholder |

## DEDUP

| Key | Value |
| --- | --- |
| dedup_mode | normalized |
| normalize_text_en | strip + collapse spaces (+ optional lowercase) |
| normalize_text_zh | strip + collapse spaces |
| provenance_fields_kept | source_sample_ids, source_groups, source_dataset |

## Examples

- before: InstructIE: Person/Place -> Located_In
  after: Person Place -> located_in
- before: Event/Attack Role:Victim
  after: attack victim

