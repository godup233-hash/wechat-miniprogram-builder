#!/usr/bin/env python3
"""为微信小程序项目生成保守的发布前静态盘点报告。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

CODE_SUFFIXES = {".js", ".ts", ".wxml", ".json"}
REQUEST_APIS = {
    "request": "wx.request",
    "upload": "wx.uploadFile",
    "download": "wx.downloadFile",
    "socket": "wx.connectSocket",
}
PRIVACY_APIS = {
    "profile": "wx.getUserProfile",
    "location": "wx.getLocation",
    "chooseLocation": "wx.chooseLocation",
    "chooseMedia": "wx.chooseMedia",
    "chooseImage": "wx.chooseImage",
    "chooseVideo": "wx.chooseVideo",
    "record": "wx.startRecord",
    "microphone": "wx.getRecorderManager",
    "clipboard": "wx.getClipboardData",
    "address": "wx.chooseAddress",
    "phone": "wx.getPhoneNumber",
}
URL_RE = re.compile(r"(?:https?|wss?)://[^\s'\"`<>)}]+")


def files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in CODE_SUFFIXES and ".git" not in path.parts:
            yield path


def line_hits(path: Path, needles: dict[str, str], root: Path) -> list[tuple[str, int, str, str]]:
    results: list[tuple[str, int, str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return results
    for number, line in enumerate(lines, 1):
        for label, needle in needles.items():
            if needle in line:
                results.append((str(path.relative_to(root)), number, label, line.strip()))
    return results


def read_json(path: Path) -> tuple[object | None, str | None]:
    if not path.exists():
        return None, None
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as exc:
        return None, str(exc)


def routes_from_app_config(config: object) -> list[str]:
    if not isinstance(config, dict):
        return []
    pages = config.get("pages", [])
    subpackages = config.get("subpackages", config.get("subPackages", []))
    routes = [route for route in pages if isinstance(route, str)]
    if isinstance(subpackages, list):
        for package in subpackages:
            if not isinstance(package, dict):
                continue
            root = package.get("root", "")
            for page in package.get("pages", []):
                if isinstance(root, str) and isinstance(page, str):
                    routes.append(f"{root.rstrip('/')}/{page.lstrip('/')}")
    return routes


def audit(root: Path) -> dict[str, object]:
    app_config, app_error = read_json(root / "app.json")
    project_config, project_error = read_json(root / "project.config.json")
    scanned = list(files(root))
    network: list[dict[str, object]] = []
    privacy: list[dict[str, object]] = []
    logs: list[dict[str, object]] = []
    urls: list[dict[str, object]] = []
    for path in scanned:
        for file_name, line, label, excerpt in line_hits(path, REQUEST_APIS, root):
            network.append({"file": file_name, "line": line, "kind": label, "excerpt": excerpt})
        for file_name, line, label, excerpt in line_hits(path, PRIVACY_APIS, root):
            privacy.append({"file": file_name, "line": line, "kind": label, "excerpt": excerpt})
        for file_name, line, _, excerpt in line_hits(path, {"console": "console.log"}, root):
            logs.append({"file": file_name, "line": line, "excerpt": excerpt})
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines, 1):
            for url in URL_RE.findall(line):
                urls.append({"file": str(path.relative_to(root)), "line": number, "url": url.rstrip(".,;"), "secure": url.startswith(("https://", "wss://"))})
    project = project_config if isinstance(project_config, dict) else {}
    return {
        "project": str(root),
        "files_scanned": len(scanned),
        "configuration": {
            "app_json": "present" if app_config is not None else "missing or invalid",
            "app_json_error": app_error,
            "project_config": "present" if project_config is not None else "missing or invalid",
            "project_config_error": project_error,
            "appid": project.get("appid", "not found"),
            "urlCheck": project.get("setting", {}).get("urlCheck", "not found") if isinstance(project.get("setting"), dict) else "not found",
        },
        "routes": routes_from_app_config(app_config),
        "network_calls": network,
        "url_literals": urls,
        "privacy_apis": privacy,
        "console_logs": logs,
    }


def markdown(report: dict[str, object]) -> str:
    def rows(items: list[dict[str, object]], keys: list[str]) -> list[str]:
        if not items:
            return ["_None found by this static scan._"]
        header = "| " + " | ".join(keys) + " |"
        divider = "| " + " | ".join("---" for _ in keys) + " |"
        body = ["| " + " | ".join(str(item.get(key, "")).replace("|", "\\|") for key in keys) + " |" for item in items]
        return [header, divider, *body]

    config = report["configuration"]
    assert isinstance(config, dict)
    lines = ["# 微信小程序静态审计", "", f"项目：`{report['project']}`", f"扫描文件数：{report['files_scanned']}", "", "## 配置"]
    lines.extend(f"- `{key}`: `{value}`" for key, value in config.items() if value is not None)
    lines += ["", "## 已声明页面路由"]
    route_items = [{"route": route} for route in report["routes"]]
    lines.extend(rows(route_items, ["route"]))
    for title, items, keys in [
        ("网络 API 调用", report["network_calls"], ["file", "line", "kind", "excerpt"]),
        ("URL 字面量", report["url_literals"], ["file", "line", "url", "secure"]),
        ("隐私相关 API 调用", report["privacy_apis"], ["file", "line", "kind", "excerpt"]),
        ("console.log 调用", report["console_logs"], ["file", "line", "excerpt"]),
    ]:
        lines += ["", f"## {title}"]
        lines.extend(rows(items, keys))
    lines += ["", "## 说明", "本报告仅为静态盘点，不能证明真机运行结果或微信后台配置。请逐项复核；缺少证据时必须标记为“未验证”。"]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="微信小程序项目目录")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()
    root = args.project.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"不是目录：{root}")
    report = audit(root)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(markdown(report), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
