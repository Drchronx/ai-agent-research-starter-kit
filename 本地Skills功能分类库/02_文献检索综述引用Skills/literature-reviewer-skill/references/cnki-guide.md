# CNKI Retrieval

CNKI retrieval is handled by the `cnki-crawler` skill. Do not maintain CNKI browser automation in this literature-review skill.

## Required Flow

1. Use the sibling `cnki-crawler` skill at `..`.
2. Read `../reference/专业检索语法.md` before generating CNKI professional search expressions.
3. Configure the CNKI skill `.env` file.
4. Run `python scripts/main.py "SU='主题词'" --start-year YYYY --end-year YYYY` from the CNKI skill root.
5. Normalize results according to `search-backends.md`.

CNKI-specific syntax belongs in the CNKI skill, not here.