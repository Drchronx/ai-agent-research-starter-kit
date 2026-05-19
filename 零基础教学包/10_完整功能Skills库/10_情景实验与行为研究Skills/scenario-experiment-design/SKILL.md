---
name: scenario-experiment-design
description: "Design rigorous scenario/vignette experiments for behavioral research in management, marketing, information systems, consumer psychology, applied psychology, and interdisciplinary social science. Use when the user asks for 情景实验, scenario experiment, vignette design, experimental stimuli, manipulation design, pretest, pilot study, random assignment, UTD24/FT50/AJG/ABS4 journal-style experiment design, or wants to learn from JCR, JCP, JM, JMR, ISR, MISQ, JAP, OBHDP, JPSP, Psychological Science, or related top journals."
---

# Scenario Experiment Design

Use this skill to design top-journal-style scenario experiments. It is for experiments where participants read, view, or interact with a constructed situation and then report perceptions, judgments, intentions, emotions, choices, or behavioral proxies.

## Journal Benchmark

Use the reference file `references/top-journal-benchmark.md` when the user wants UTD24, FT50, AJG/ABS4, JCR, JCP, JAP, JCR, ISR, JM, JMR, MISQ, OBHDP, JPSP, Psychological Science, or similar top-journal positioning.

Do not claim a journal is in UTD24, FT50, or AJG 4/4* unless verified for the target year. Journal lists can change.

If the user wants to learn from real published articles before designing a new study, use or recommend `scenario-experiment-benchmark-mining` first to build a verified benchmark matrix.

## Design Workflow

### 1. Convert research idea into causal structure

Extract:

- Independent variable or treatment.
- Dependent variable.
- Mediator.
- Moderator.
- Boundary condition.
- Competing explanation.
- Unit of randomization.
- Target population.
- Theoretical mechanism.

Reject vague designs. A scenario experiment must manipulate a theoretically meaningful cause, not merely describe a condition.

### 2. Choose experiment type

| Type | Use when | Example |
|---|---|---|
| Single-factor between-subjects | One clear causal contrast | AI agent present vs absent |
| 2 x 2 between-subjects | Two IVs or IV x boundary condition | High vs low autonomy x high vs low task complexity |
| Mediated design | Mechanism is central | AI explainability -> trust -> adoption |
| Moderated mediation | Top-journal mechanism + boundary | Anthropomorphism -> perceived agency -> blame, moderated by expertise |
| Choice experiment | DV is selection, tradeoff, or preference | Choose human expert vs AI agent |
| Multi-study package | Contribution requires triangulation | Pretest + main experiment + robustness + field or behavioral follow-up |

Prefer the simplest design that can identify the theory.

### 3. Build scenario stimulus

Each condition should vary only the manipulated feature.

Stimulus checklist:

- Same length across conditions unless length is itself the manipulation.
- Same actor, context, stakes, and outcome.
- Manipulated construct is salient but not demand-heavy.
- No unintended confound such as competence, warmth, severity, risk, cost, or social desirability.
- Language is realistic for the target population.
- Scenario contains enough detail for immersion but not enough to reveal the hypothesis.

### 4. Add manipulation and validity checks

Use:

- Manipulation check: whether participants perceived the manipulated construct.
- Attention check: whether participants read the scenario.
- Realism check: scenario plausibility and clarity.
- Confound check: alternative perceptions that should not differ.
- Demand suspicion check if the mechanism is obvious.

Do not use manipulation checks as a substitute for clean stimulus design.

### 5. Define measures

For each construct:

- Use validated scales when possible.
- Specify source, item wording, response anchor, and reliability target.
- Separate manipulation check items from mediator/DV items.
- Avoid using almost identical items for manipulation check and mediator.

### 6. Plan pretest and pilot

Pretest goals:

- Verify manipulation strength.
- Detect confounds.
- Check clarity and realism.
- Estimate variance and completion time.

Pilot goals:

- Test randomization.
- Test attention checks.
- Estimate effect size.
- Identify ceiling/floor effects.
- Confirm analysis plan.

### 7. Plan main study

Specify:

- Sampling platform and inclusion criteria.
- Planned sample size and power rationale.
- Exclusion rules before seeing outcomes.
- Randomization method.
- Primary DV and secondary outcomes.
- Confirmatory vs exploratory analyses.
- Data, code, and materials sharing plan.

## Output Template

```text
Research question:
Target journal family:
Core theory:
Causal model:
Design:
Conditions:
Stimuli:
Manipulation checks:
Confound checks:
Measures:
Sample and power:
Procedure:
Analysis plan:
Expected pattern:
Threats to validity:
Pretest plan:
Main-study readiness:
```

## Quality Bar

Top-journal scenario experiments usually need:

- A clear theoretical reason why the manipulation changes the mediator or DV.
- Pretested manipulations.
- Confound checks.
- Exact operational definitions.
- Multiple studies or robustness designs when the claim is broad.
- Transparent exclusion, randomization, and reporting.

If the user's idea is only a questionnaire correlation study, say so and convert it into a real experimental design.
