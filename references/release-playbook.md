# Release evidence playbook

Use this after the code works. Console names, requirements, fees, eligibility, and approval rules can change; verify current instructions in the account's official console and documentation.

## Interpret static-audit output

- `AppID`: confirm that the imported project's identifier matches the intended account; do not commit credentials or secrets.
- `Routes`: open every declared route and capture a result. A route list is not proof that the route renders.
- `External hosts`: classify each call by request/upload/download/socket semantics. Confirm each live host and transport setting in the current platform configuration; do not infer allowlisting from a development bypass.
- `Privacy APIs`: inspect surrounding code to determine whether the API is reachable and what data is collected. Declare only actual collection/use, with an in-product purpose and fallback.
- `console.log`: remove or gate sensitive/noisy development output before release; retain only intentional, non-sensitive operational logging.

## Minimum evidence matrix

| Area | Evidence | Owner |
| --- | --- | --- |
| Import/build | Project imported, exact build identifier, clean compile result | Developer |
| Core flow | Steps, expected/actual result, screenshots | Developer/tester |
| Devices | At least one representative real device per targeted platform | Tester |
| Persistence | Relaunch/reinstall or cross-device case appropriate to storage choice | Developer/tester |
| Backend/cloud | Environment selected, rules reviewed, functions deployed/tested | Account owner + developer |
| Privacy | API inventory mapped to current declaration and user purpose | Account owner + developer |
| Submission metadata | Name/category/service description/screenshots/test instructions | Account owner |

## Evidence language

Use exact status labels:

- `changed in code` — include file path and concise effect.
- `needs user action in console` — name the factual value or screen to verify, without claiming its current state.
- `not verified` — evidence is absent or inaccessible.
- `blocked` — a required value, permission, account role, test device, or platform decision is missing.

Never turn `not verified` into an implied pass.
