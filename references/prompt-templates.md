# Copyable prompts

## Requirements interview

```text
I want to build [idea]. Do not write code yet. Turn this into a v1 product brief with: target user, one core outcome, pages and navigation, key interactions, data fields and ownership, storage recommendation, privacy-sensitive capabilities, visual direction, non-goals, acceptance criteria, and risks. List every unknown decision in one batch; propose a default beside each question so I can reply “approve” or edit it. Update the brief after my reply.
```

## Prototype

```text
Do not build the Mini Program yet. Create an interactive browser prototype for the key user flow from this product brief. Include realistic empty, filled, validation-error, and completion states. Keep it self-contained, explain what is deliberately fake, and wait for approval before native implementation.
```

## Native implementation slice

```text
Implement only [page/flow] of the approved Mini Program brief. Follow the visual specification and native Mini Program constraints. List changed files, acceptance criteria exercised, any configuration I must supply, and any capability that needs a platform-console action. Do not introduce permissions, cloud collections, or external services not required for this slice.
```

## Precise defect report

```text
Fix this Mini Program issue. Reproduction: [steps]. Expected: [result]. Actual: [result]. Environment: [simulator/device, OS, WeChat version]. Full error: [paste verbatim]. Evidence: [screenshot/video]. First identify the likely cause and affected files; make the smallest safe fix, then rerun the whole core-flow regression.
```

## Pre-submission audit

```text
Prepare this Mini Program for upload/submission. Run the static audit and inspect its findings. Separate results into: changed in code, needs my action in the WeChat console, not verified, and blocked. For each external host and privacy-related API, show source file and line plus the evidence needed. Do not guess console settings, current rules, eligibility, or approval status.
```
