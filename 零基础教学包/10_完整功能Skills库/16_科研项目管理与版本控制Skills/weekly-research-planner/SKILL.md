---
name: weekly-research-planner
description: "Create weekly research plans and reviews for doctoral projects. Use for weekly_plan.md, weekly_review.md, priority setting, task dependencies, research sprint planning, meeting preparation, advisor questions, and project continuity."
---

# Weekly Research Planner

Use this skill at the start or end of each week.

## Inputs

- Project dashboard.
- Recent research logs.
- Deadlines.
- Advisor or committee feedback.
- Current blockers.

## Workflow

1. Review current project status and recent logs.
2. Separate tasks into must-do, should-do, and can-wait.
3. Define inputs, outputs, dependencies, and estimated time for each task.
4. Identify questions for advisor discussion.
5. End the week by writing a review: completed, unfinished, blockers, and next week priorities.

## Hard Constraints

- Do not overload the week with impossible task volume.
- Do not hide blockers.
- Do not plan analysis before required data or decisions exist.

## Script

Use `scripts/create_weekly_plan_template.py` to create a weekly plan template.

## Output

```text
This week's goal:
Must-do tasks:
Should-do tasks:
Can-wait tasks:
Advisor questions:
Risks:
End-of-week review template:
```

