<p align="center">
  <img src="assets/wxxcx.jpg" alt="微信小程序生成器" width="520" />
</p>

# wechat-miniprogram-builder

> 微信小程序 AI 编程 Skill：从需求梳理到真机测试、发布提审的完整工作流。开箱即用，适配 **WorkBuddy**、Claude Code 等支持 Skills 的 AI 编程助手。

## 这是什么

`wechat-miniprogram-builder` 不是一个代码框架，而是一套写给 AI 编程助手的**执行指令集（Skill）**。它把微信小程序开发的完整链路固化为标准流程：

```text
需求访谈 → 产品简报 → 浏览器原型 → 分片开发 → 真机测试 → 发布审计 → 提审自查
```

AI 助手装上它之后，会像一个懂微信小程序规则的技术负责人一样工作：先把需求问清楚、先给你看交互样品、按完整用户流程一片片开发、收集可复现的报错证据再修 bug、提审前跑静态审计并把"代码问题"和"需要你去微信后台操作的事"严格分开。

## 解决什么问题

直接用 AI 写小程序常见的坑：

| 没有 Skill | 装上本 Skill 后 |
| --- | --- |
| 一句话需求直接开写，返工不断 | 先一次性问清需求，输出可确认的 v1 产品简报 |
| 写完才发现视觉/交互方向不对 | 写原生代码前先做浏览器交互原型，低成本确认方向 |
| 用浏览器 DOM/CSS 写 WXML，真机翻车 | 全程遵循原生小程序约束，明确禁止浏览器专属 API |
| 报错截图发来就乱改 | 要求完整报错原文 + 复现步骤 + 设备信息，修后跑全流程回归 |
| 提审被驳回才知道配置不对 | 内置静态审计脚本 + 发布证据清单，提前暴露问题 |
| AI 拍脑袋猜后台规则 | 明确"以微信官方文档和当前后台为准"，不把猜测写成结论 |

## 安装到 WorkBuddy

把整个目录放进 WorkBuddy 的用户级 Skills 目录即可：

```bash
# 克隆到用户级 skills 目录（所有项目可用）
git clone https://github.com/godup233-hash/wechat-miniprogram-builder.git ~/.workbuddy/skills/wechat-miniprogram-builder
```

如果只想在单个项目里用，克隆到 `{你的项目}/.workbuddy/skills/` 下。

之后在 WorkBuddy 对话中直接描述任务即可触发，例如：

```text
使用 $wechat-miniprogram-builder：我想做一个给自己用的每日喝水打卡小程序。先不要写代码，请一次性问清需求，给我一版可确认的 v1 产品简报。
```

## 典型用法

**从零做 MVP**

```text
使用 $wechat-miniprogram-builder：帮我做一个记账小程序，数据存本地就行。
```

**迭代 / 修 bug**

```text
使用 $wechat-miniprogram-builder 修复这个小程序的问题。复现步骤：[步骤]。期望：[结果]。
实际：[结果]。完整报错：[原文]。环境：[模拟器/真机型号，微信版本]。
```

**提审前自查**

```text
使用 $wechat-miniprogram-builder 检查这个小程序能否准备提审。先运行静态审计，
把问题分成：代码已改、需要我去微信后台操作、未验证、受阻。不要猜后台配置。
```

`references/prompt-templates.md` 里提供了需求访谈、原型、分片开发、报错修复、提审审计等**可直接复制的中文提示词**。

## 内置静态审计工具

无需任何第三方依赖，发布前对项目做一次离线扫描：

```bash
python3 scripts/audit_miniprogram.py /绝对路径/你的小程序项目 --format markdown
```

扫描内容：

- 路由与 `app.json` 配置盘点
- AppID 配置检查（是否残留测试号/示例 AppID）
- 所有外部网络调用（request / upload / download / socket）的域名清单
- 隐私相关 API（位置、相册、联系人等）的文件与行号定位
- `console.log` 等调试输出残留

> 报告只是静态盘点，不代表真机运行成功，也不代表微信后台配置正确——真机测试和后台确认仍然必须做。

## 目录结构

```text
SKILL.md                         # 主工作流与执行原则（AI 助手读取的核心文件）
agents/openai.yaml               # Skills 界面元数据
references/
  prompt-templates.md            # 中文可复制提示词模板
  release-playbook.md            # 发布证据清单与审计结果解读
scripts/
  audit_miniprogram.py           # 离线静态审计工具（纯标准库）
```

## 兼容环境

- **WorkBuddy**（推荐）：放入 `~/.workbuddy/skills/` 即可
- **Claude Code / 其他支持 SKILL.md 的助手**：放入对应 skills 目录，或用 `references/prompt-templates.md` 手动投喂提示词
- 纯命令行场景：审计脚本可独立运行，不依赖 Skill 环境

## 设计原则

- **先 MVP 后扩展**：首个版本只做一条完整核心流程 + 必要状态页，账号体系、社交、支付默认推迟。
- **代码与后台分离**：AI 能改的和必须人工去微信后台操作的，永远分开列。
- **不编造**：不虚构 AppID、凭证、资质或审核结果；没验证过的一律标 `not verified`。
- **平台规则会过期**：类目、资质、备案、费用、审核周期、API 能力以提交时微信官方文档和当前后台为准。

## License

MIT
