# Step 8 - Tables, Figures, and Artifact Manifest

Use fixed output scripts:

| Task | Script |
|---|---|
| Format tidy regression results | `scripts/table_factory.py` |
| Coefficient plot | `scripts/plot_factory.py --kind coef` |
| Event-study plot | `scripts/plot_factory.py --kind event` |
| Binscatter | `scripts/plot_factory.py --kind binscatter` |
| Love plot | `scripts/plot_factory.py --kind love` |
| Artifact manifest | `scripts/render_manifest.py` |

Goal: collect generated tables and figures into a manifest so the final empirical outputs are auditable.

## Use When

- The analysis has produced multiple tables and figures.
- The user asks for publication-ready outputs, an output inventory, or a reproducibility index.

## Main Parameters

| Parameter | Use |
|---|---|
| `--results-dir` | Root directory containing generated tables and figures. |
| `--output-dir` | Directory for `artifact_manifest.json` and `artifact_manifest.md`. |

## Typical Invocation

Use an inline command shaped like `python scripts/render_manifest.py --results-dir output/empirical --output-dir output/empirical`.

To format a tidy regression table, use an inline command shaped like `python scripts/table_factory.py --input output/empirical/tables/panel_results.csv --kind regression --stem table_panel_formatted --output-dir output/empirical/tables --formats csv,xlsx,tex`.

To create a coefficient plot, use an inline command shaped like `python scripts/plot_factory.py --input output/empirical/tables/panel_results.csv --kind coef --term treat --label-col model --stem fig_coefplot --output-dir output/empirical/figures`.

To create an event-study plot, use an inline command shaped like `python scripts/plot_factory.py --input output/empirical/tables/did_results.csv --kind event --rel-col rel_time --stem fig_event_study --output-dir output/empirical/figures`.

## Outputs

- `artifact_manifest.json` listing table files, figure files, Python version, platform, and working directory.
- `artifact_manifest.md` for human-readable review.

## Table and Figure Standards

- Tables should normally be exported as CSV, XLSX, and LaTeX.
- Add DOCX only when the environment has `python-docx` and the user needs Word output.
- Figures should be exported as PNG and PDF when figure generation is enabled.
- Keep table stems stable: `table1_summary`, `table1_balance`, `table2_main`, `table2_main_tidy`, `table3_mechanism`, `table4_heterogeneity`, and `table5_robustness`.

## Decision Rules

- Run `render` after the last analysis step.
- If an expected artifact is missing, run the corresponding earlier subcommand rather than creating a manual placeholder.
- Do not manually copy regression numbers into markdown. The final answer should point to generated artifact paths and summarize key outputs.
