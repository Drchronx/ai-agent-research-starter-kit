# Journal Scope Map For Scenario Experiment Benchmarking

Use this map to choose sources. It is a search aid, not a ranking claim.

## Ranking And Reporting Sources To Verify

- UTD Top 100 Business School Research Rankings: UT Dallas Jindal states that the ranking tracks publications in 24 leading peer-reviewed business journals and uses a rolling five-year window. Verify the current official journal list on the UTD ranking site before labeling a journal "UTD24".
- FT50: Financial Times' FT50 list is the 50 journals used in the FT research rank. The FT review in 2016 expanded the list from 45 to 50. Verify the current FT page or a university library mirror if the FT page is behind access control.
- AJG/ABS: Chartered ABS Academic Journal Guide ratings are year-specific. Verify AJG 2024 or the target-year guide before calling a journal 4 or 4*.
- APA JARS-Quant: use for psychology-style transparent quantitative and experimental reporting.
- AGReMA: use when reporting mediation analyses, especially when causal language around mediators could be challenged.

Reference links:

- UTD overview: https://jsom.utdallas.edu/the-utd-top-100-business-school-research-rankings/?t=ad
- UTD journal list: https://jsom.utdallas.edu/the-utd-top-100-business-school-research-rankings/list-of-journals
- FT50 library reference: https://guides.lib.purdue.edu/ft50
- AJG 2024 methodology: https://assets.charteredabs.org/ajg-2024-methodology.pdf
- APA JARS: https://www.apa.org/education-career/training/reporting-research-jars.html
- AGReMA: https://jamanetwork.com/journals/jama/fullarticle/2784353

## Journal Families

| Family | Example journals | What to learn from scenario experiments |
|---|---|---|
| Consumer research and marketing | JCR, JCP, JM, JMR, Marketing Science, JAMS | construct clarity, consumer psychology mechanisms, multi-study packages, managerial relevance |
| Applied and organizational psychology | JAP, OBHDP, JPSP, Psychological Science, Personnel Psychology | experimental control, validated measures, moderation/mediation logic, transparent reporting |
| Information systems and HCI | ISR, MISQ, JAIS, JMIS | technology-use contexts, AI/user interaction manipulations, system realism, behavioral intention and use outcomes |
| Management and organizations | AMJ, ASQ, Organization Science, SMJ, JOM | theory contribution, boundary conditions, organizational scenario realism |

## Search Recipes

### Topic-first

```text
("[topic]" AND ("scenario" OR "vignette") AND ("experiment" OR "randomly assigned"))
("[topic]" AND "manipulation check" AND "Study 1")
("[topic]" AND "mediated" AND "scenario experiment")
```

### Journal-first

```text
"Journal of Consumer Research" "[topic]" "scenario"
"Journal of Applied Psychology" "[topic]" "vignette"
"Information Systems Research" "[topic]" "experiment"
"Journal of Marketing" "[topic]" "randomly assigned"
```

### AI agent and HCI topics

```text
("AI agent" OR "algorithm" OR "automation" OR "chatbot" OR "recommendation system") AND ("scenario" OR "vignette" OR "experiment")
("explainability" OR "anthropomorphism" OR "autonomy") AND ("trust" OR "adoption" OR "blame") AND "experiment"
```

## Screening Rules

Include a paper only if it has at least one experimental study with random assignment, clear manipulation, or a vignette/scenario stimulus. Exclude purely correlational surveys unless the user asks for comparison cases.

When a paper uses multiple studies, code each experiment separately if the designs differ materially.
