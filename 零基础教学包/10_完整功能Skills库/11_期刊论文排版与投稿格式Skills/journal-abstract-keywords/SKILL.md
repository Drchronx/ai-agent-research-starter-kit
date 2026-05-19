---
name: journal-abstract-keywords
description: "Audit and format abstracts and keywords for journal submission. Use for abstract word count, structured versus unstructured abstracts, APA 7 abstract formatting, keyword capitalization, alphabetical ordering, punctuation, MeSH or journal keyword rules, and length compliance without changing scientific claims."
---

# Journal Abstract And Keywords

Use this skill to make abstracts and keyword lists comply with target journal constraints.

## Inputs

- Abstract text.
- Keyword list.
- Target journal rules: word limit, structured headings, keyword count, capitalization, separator, and order.

## Workflow

1. Count words using the rule requested by the journal.
2. Identify whether the abstract is structured or unstructured.
3. Check required headings such as Objective, Method, Results, Conclusion when applicable.
4. Format keywords according to separator, capitalization, order, and maximum count.
5. Flag over-limit text for author revision.

## Hard Constraints

- Do not alter scientific meaning, results, sample size, p-values, or claims.
- If over the word limit, flag the exact excess and suggest compression targets instead of deleting content automatically.
- Do not add keywords that are not supplied or clearly derivable from the manuscript.

## Output

```text
Formatted abstract:
Formatted keywords:
Word-count audit:
Journal-rule compliance:
Manual revision flags:
```

