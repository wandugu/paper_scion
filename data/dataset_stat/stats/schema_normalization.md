# Schema Normalization Spec

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

