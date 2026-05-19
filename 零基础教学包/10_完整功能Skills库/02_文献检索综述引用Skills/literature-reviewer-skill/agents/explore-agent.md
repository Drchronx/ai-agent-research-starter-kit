# Explore Agent Replacement

This file is intentionally reduced. The old browser automation explore-agent has been replaced by pluggable retrieval skills.

Use `../references/search-backends.md` for the backend contract.

Required behavior:

1. Select a retrieval backend by database/source.
2. Delegate retrieval to that backend skill.
3. Normalize backend output to the shared paper schema.
4. Return normalized papers to the literature reviewer workflow.

Do not implement CNKI browser automation here. For CNKI, use `cnki-crawler`.