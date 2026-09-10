---
name: wechat-miniprogram-builder
description: 从需求到交付构建、修复、测试和发布微信小程序。适用于将想法梳理为可控范围的 MVP、编写或修改原生微信小程序项目（WXML/WXSS/JavaScript/TypeScript）、选择本地或云端数据方案、排查微信开发者工具或真机问题、进行发布前隐私/域名/接口审计，以及指导体验版、上传和提审准备。
---

# 微信小程序构建

Deliver a usable MVP before extending scope. Treat the user as product owner and the agent as the technical lead: make assumptions explicit, keep platform-console actions separate from code changes, and never invent identifiers, credentials, qualifications, or approval results.

## Operating rules

- Work in native Mini Program conventions unless the existing project establishes another stack. Do not use browser-only DOM APIs, HTML, CSS features, or hover-dependent interaction without checking compatibility.
- Keep the first release to one complete core flow plus essential empty/loading/error states. Defer account systems, social features, payments, and complex analytics unless they are the core value.
- Do not expose an AppID, secret, private key, user data, or a production cloud environment ID in a public repository. Use documented placeholders or local configuration ignored by Git.
- Treat publication rules, supported APIs, quotas, eligibility, fees, and review timelines as changeable. Verify them in the current official WeChat documentation or console before advising the user to submit.
- Use the native component and API documentation as the source of truth where a simulator differs from a device. Ask for a screenshot and the complete console error if UI labels or tooling have changed.

## 1. Frame the release before coding

Start by restating the idea in one sentence and propose a v1. Gather missing decisions in **one batch**; give a sensible default for each so the user can approve or edit quickly.

Required decisions:

1. Target user and the job they are trying to complete.
2. One primary success action, input fields, and what happens after it.
3. Pages, navigation, and every important tap/long-press/swipe.
4. Data fields, ownership, retention/deletion, and whether data must survive reinstall, sync across devices, or be shared.
5. Login, location, media, payment, notification, and other sensitive capabilities.
6. Visual direction: logo/assets, brand colors, content tone, and accessibility needs.
7. Release target: personal local use, invited experience testers, public release, or commercial service.

Produce a compact product brief containing: scope/non-goals, page map, user flow, data model, acceptance criteria, risks, and unresolved choices. Read [prompt-templates.md](references/prompt-templates.md) when the user needs copyable prompts or a requirements interview.

## 2. Validate direction cheaply

For a new or visually significant product, build an interactive browser prototype of the key flow before creating the native project. Use it to validate layout, wording, and state transitions only; label it as a prototype, not Mini Program code.

Create a visual specification before implementation: named colors with hex values, spacing scale, typography scale, component states, image treatment, and touch targets. If a logo exists, derive a restrained palette from it rather than guessing unrelated colors.

For an existing Mini Program or a narrowly scoped bug fix, skip the prototype and record why.

## 3. Build the native project

Inspect the project before modifying it. Identify its framework, package manager, app/page configuration, components, cloud functions, environment configuration, and existing lint/test commands. Preserve established conventions.

For a new native project, make every page complete enough to test:

- Register routes in `app.json`; keep page-level `.json`, `.wxml`, `.wxss`, and `.js`/`.ts` files aligned.
- Implement explicit loading, empty, validation-error, and failure states. Disable or guard repeat submissions.
- Use responsive `rpx` layout deliberately; verify on a small and a large device viewport. Do not rely on mouse hover or fixed desktop geometry.
- Centralize theme tokens and reusable components before duplicating styles across pages.
- Validate input on both client and server/cloud-function boundaries. Show actionable Chinese copy instead of raw errors.
- Include only the permissions and APIs required by the defined flow. For each sensitive API, record purpose, trigger, fallback, and deletion path.

### Choose data storage deliberately

| Need | Default | Implementation requirement |
| --- | --- | --- |
| Temporary, single-device prototype | Local storage | Namespace keys, handle corrupt/missing values, provide reset/export guidance. |
| Persistent or cross-device personal data | Cloud development or an approved backend | Model ownership and access rules first; keep privileged operations server-side. |
| Shared, moderated, paid, or regulated data | Approved backend with explicit design review | Define authorization, audit, deletion, abuse controls, and compliance constraints before coding. |

Never claim that cloud data is configured merely because client calls exist. Record the environment ID as user-provided configuration, create only the needed collections/functions, apply least-privilege rules, and test the real persistence path on a device.

## 4. Develop in observable slices

Implement one complete user flow at a time, preferably core screens before a decorative landing page. After each slice:

1. Compile in WeChat Developer Tools.
2. Exercise the acceptance criteria in the simulator.
3. Check layout, text clipping, tap behavior, asset loading, loading/error/empty states, and persistence where applicable.
4. Capture actual errors and repair the cause, then rerun the full core-flow regression—not only the changed case.

For a defect report, collect: exact reproduction steps, expected versus actual behavior, full console/error text, device/OS/WeChat version if device-only, and a screenshot or video. Do not diagnose from a partial error paraphrase.

When a browser implementation is incompatible, replace it with a native component/API pattern rather than suppressing the warning. When a code edit appears not to apply, rebuild/reload deliberately, confirm the edited file is part of the imported project, then inspect cache/build output before making unrelated changes.

## 5. Test on real devices

Use the Developer Tools feature appropriate to the question:

| Goal | Use | Evidence to collect |
| --- | --- | --- |
| Fast visual check | Preview | Screenshot and build identity |
| Cross-platform behavior | Real-device test/preview on representative iOS and Android devices | Device, OS, WeChat version, pass/fail notes |
| Device-only defect | Remote debugging | Full logs, reproduction steps, screenshots |

Before sharing any build, execute the core-flow regression: create/add, edit or change state, relaunch and verify persistence, delete/reset, invalid/empty input, no-network or failed request (where relevant), and a complete return navigation path. Add product-specific edge cases to the product brief.

## 6. Audit before sharing, uploading, or submitting

Run the repository audit first:

```bash
python3 scripts/audit_miniprogram.py /absolute/path/to/project --format markdown
```

If the project lives elsewhere, invoke the script from this skill's `scripts/` directory. It is a static inventory, not a certification: review every finding and mark unavailable evidence as `not verified`, never as a pass.

Then prepare a release checklist containing four owners:

- **Code:** build succeeds; routes work; errors/logging reviewed; generated/test files excluded; AppID is deliberate; no secrets are tracked.
- **Network and cloud:** list every external host by API type; require secure endpoints and current console configuration where applicable; verify cloud environment, data rules, and deployed functions.
- **Privacy:** inventory all information/permission-related APIs with file and line; map each to a user-visible purpose and current privacy declaration. Remove unused collection.
- **Platform console:** owner verifies account subject, service category, basic information, screenshots, test access, record/filing or verification requirements, and submission text in the current WeChat console.

Generate the inventory with the audit script and read [release-playbook.md](references/release-playbook.md) before guiding a release. Clearly distinguish: `changed in code`, `needs user action in console`, `not verified`, and `blocked`.

## 7. Hand off cleanly

Deliver the project path, how to import it, required configuration values (without secrets), implemented v1 scope, test results with device coverage, known limitations, and exact next actions. For review copy, describe what a reviewer sees, what they can do, and the result—truthfully and concretely.

Do not promise that an upload is published, an experience build is publicly accessible, or a review will pass. These are platform-controlled states that must be confirmed by the account owner.

## References and tools

- [prompt-templates.md](references/prompt-templates.md): Requirements interview, prototype, implementation, bug-report, and audit prompt templates.
- [release-playbook.md](references/release-playbook.md): Static-audit interpretation and release evidence checklist.
- [audit_miniprogram.py](scripts/audit_miniprogram.py): Offline static inventory for routes, configuration, network calls, privacy-related APIs, and debug logging.
