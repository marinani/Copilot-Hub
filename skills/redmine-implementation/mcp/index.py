#!/usr/bin/env python3
"""Redmine MCP-like helper script (Python).

It connects to Redmine using the REST API and exposes commands similar to
MCP "tools": list_projects, list_issues, get_issue, create_issue, update_issue,
list_issue_statuses, list_trackers, list_versions, search_issues, and add_issue_tag.

Usage:
  python index.py list_issues --status_id 2 --limit 50

Configuration:
  REDMINE_URL:  Redmine base URL (default: https://redmine.ici.curitiba.org.br)
  REDMINE_API_KEY: API key for authentication
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_URL = os.environ.get("REDMINE_URL", "https://redmine.ici.curitiba.org.br")


def persist_api_key(key: str) -> None:
    """Persist REDMINE_API_KEY in the user's environment variables."""
    if platform.system() == "Windows":
        try:
            subprocess.run(["setx", "REDMINE_API_KEY", key], check=True, capture_output=True)
            print("REDMINE_API_KEY saved to user environment variables (new terminal window may be required).")
        except Exception as e:
            print(f"Could not save REDMINE_API_KEY: {e}", file=sys.stderr)
    else:
        print(
            "REDMINE_API_KEY not found. Set it in your shell (e.g.: export REDMINE_API_KEY=...)."
        )


def _try_load_api_key_from_windows_registry() -> Optional[str]:
    """Attempts to read REDMINE_API_KEY from HKCU\\Environment on Windows."""
    if platform.system() != "Windows":
        return None

    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, "REDMINE_API_KEY")
            return value
    except Exception:
        return None


def get_api_key() -> str:
    """Gets REDMINE_API_KEY from the environment. If not present, emits a structured error for the agent to handle via chat."""
    key = os.environ.get("REDMINE_API_KEY")
    if key:
        return key

    # If not in environment, try reading from user environment key on Windows
    key = _try_load_api_key_from_windows_registry()
    if key:
        os.environ["REDMINE_API_KEY"] = key
        return key

    # Do not use input() — the agent should request the key via chat and pass it as an environment variable.
    error = {
        "error": "REDMINE_API_KEY_MISSING",
        "message": (
            "The REDMINE_API_KEY environment variable is not configured. "
            "Provide the Redmine API key in the chat so the agent can proceed."
        ),
    }
    print(json.dumps(error, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(2)


API_KEY = get_api_key()

# Configuration loaded from `.github/config.yaml` or `.vscode/config.yaml`.
REDMINE_CONFIG: Dict[str, Any] = {}


def _parse_yaml_scalar(value: str) -> Any:
    """Parses a simple YAML value (int/bool/string)."""
    if not value:
        return ""
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.isdigit():
        return int(value)
    # remove quotes
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def _find_repo_root() -> Path:
    """Attempts to find the repository root.

    Looks for a directory containing `.git` or a `*.csproj` file.
    """
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / ".git").exists() or any(parent.glob("*.csproj")):
            return parent
    return p.parents[-1]


def _find_or_create_config_path() -> Path:
    """Determines the config file to use, creating directories if needed."""
    repo_root = _find_repo_root()
    candidates = [
        repo_root / ".github" / "config.yaml",
        repo_root / ".github" / "config.yml",
        repo_root / ".vscode" / "config.yaml",
        repo_root / ".vscode" / "config.yml",
    ]

    for p in candidates:
        if p.exists():
            return p

    # default: .github/config.yaml
    default = repo_root / ".github" / "config.yaml"
    default.parent.mkdir(parents=True, exist_ok=True)
    return default


def _format_value_for_yaml(key: str, value: Any) -> str:
    """Formats values for simple YAML writing.

    Ensures certain fields are always treated as strings.
    """
    # Ensures project_id and project_name are strings (even if numeric)
    if key in {"project_name", "project_id"}:
        s = str(value)
        if not (s.startswith('"') and s.endswith('"')) and not (s.startswith("'") and s.endswith("'")):
            return f'"{s}"'
        return s
    return str(value)


def _rewrite_yaml_section(path: Path, section: str, values: Dict[str, Any]) -> bool:
    """Rewrites (or creates) a YAML section with the provided values.

    Returns True if the file was modified.
    """
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = text.splitlines(keepends=True)

    def _write_value(k: str, v: Any) -> List[str]:
        if isinstance(v, dict):
            out = [f"  {k}:\n"]
            for sk, sv in v.items():
                out.append(f"    {sk}: {_format_value_for_yaml(sk, sv)}\n")
            return out
        return [f"  {k}: {_format_value_for_yaml(k, v)}\n"]

    # Locate existing section
    section_start = None
    section_indent = 0
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith(f"{section}:") and (line.startswith(section) or line.startswith(" ")):
            section_start = i
            section_indent = len(line) - len(stripped)
            break

    if section_start is None:
        # Append to end
        if lines and not lines[-1].endswith("\n"):
            lines[-1] = lines[-1] + "\n"
        lines.append(f"{section}:\n")
        for k, v in values.items():
            lines.extend(_write_value(k, v))
        path.write_text("".join(lines), encoding="utf-8")
        return True

    # Find end of current section
    end = len(lines)
    for j in range(section_start + 1, len(lines)):
        if not lines[j].strip():
            continue
        indent = len(lines[j]) - len(lines[j].lstrip(" "))
        if indent <= section_indent:
            end = j
            break

    # Replace the entire section
    new_lines = lines[:section_start]
    new_lines.append(f"{section}:\n")
    for k, v in values.items():
        new_lines.extend(_write_value(k, v))
    new_lines.extend(lines[end:])

    new_text = "".join(new_lines)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def _read_redmine_config(cfg_path: Path) -> Dict[str, Any]:
    """Reads the `redmine` section from the YAML configuration file (no external dependencies)."""
    if not cfg_path.exists():
        return {}

    cfg: Dict[str, Any] = {}
    current_section = None
    current_subsection = None

    for line in cfg_path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        # Start section
        if stripped.startswith("redmine:") and indent == 0:
            current_section = "redmine"
            current_subsection = None
            continue

        if current_section != "redmine":
            continue

        # New section or end of section
        if indent == 0:
            current_section = None
            current_subsection = None
            continue

        # Top-level keys within redmine
        if indent == 2:
            if ":" not in stripped:
                continue
            key, raw = stripped.split(":", 1)
            key = key.strip()
            value = _parse_yaml_scalar(raw.strip())
            if key == "status_ids" and isinstance(value, str) and value == "":
                cfg["status_ids"] = {}
                current_subsection = "status_ids"
            else:
                cfg[key] = value
                current_subsection = None
            continue

        # Subsection items (e.g., status_ids)
        if indent >= 4 and current_subsection == "status_ids":
            if ":" not in stripped:
                continue
            sk, raw = stripped.split(":", 1)
            sk = sk.strip()
            sv = _parse_yaml_scalar(raw.strip())
            cfg.setdefault("status_ids", {})[sk] = sv

    return cfg


def ensure_redmine_config() -> Dict[str, Any]:
    """Ensures Redmine configuration exists in config.yaml without using terminal prompts."""
    cfg_path = _find_or_create_config_path()

    # If it already exists, try reading existing values in the redmine section
    existing_values = _read_redmine_config(cfg_path)

    project_name = existing_values.get("project_name")
    if not project_name:
        error = {
            "error": "REDMINE_PROJECT_NAME_MISSING",
            "message": (
                "The Redmine 'project_name' configuration is not set. "
                "Provide the project name in the chat so the agent can proceed."
            ),
        }
        print(json.dumps(error, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(3)

    # Fetch project information directly from Redmine and populate project_id/project_id_numeric
    try:
        # We use /projects.json because we don't have the numeric ID yet
        projects = api_request("GET", "/projects.json", {"limit": 100}).get("projects", [])
        match = next((p for p in projects if p.get("name") == project_name), None)
        if not match:
            raise ValueError("Project not found (exact name not located).")
        project_id_numeric = str(match.get("id"))
        project_id = match.get("identifier")
        if not project_id or not project_id_numeric:
            raise ValueError("Unexpected response from Redmine")

        # Fetch Redmine issue statuses to populate status_ids
        statuses = api_request("GET", "/issue_statuses.json").get("issue_statuses", [])
        status_ids: Dict[str, int] = {}
        for s in statuses:
            name = s.get("name") or ""
            key = name.lower().replace(" ", "_")
            status_ids[key] = s.get("id")
    except Exception as e:
        raise SystemExit(f"Could not retrieve Redmine project data ('{project_name}'): {e}")

    required_keys = {
        "project_name": project_name,
        "project_id": project_id,
        "project_id_numeric": project_id_numeric,
        "status_ids": status_ids,
    }

    changed = _rewrite_yaml_section(cfg_path, "redmine", required_keys)
    if changed:
        print(f"Redmine configuration updated at: {cfg_path}")

    # Returns the configuration that will be used to limit operations.
    existing_values.update(required_keys)
    return existing_values


def _get_config_project_id() -> str:
    """Returns the project_id (identifier) of the configured project."""
    pid = REDMINE_CONFIG.get("project_id")
    if not pid:
        raise SystemExit("Redmine project configuration was not loaded.")
    return str(pid)


def _ensure_project_scope(requested_project_id: Optional[str], param_name: str = "project_id") -> str:
    """Validates whether the provided project_id (if any) matches the configured project."""
    configured = _get_config_project_id()
    numeric = str(REDMINE_CONFIG.get("project_id_numeric") or "")
    if requested_project_id:
        if requested_project_id != configured and requested_project_id != numeric:
            raise SystemExit(
                f"Operation can only be performed on the configured project ({configured}). "
                f"Parameter {param_name}='{requested_project_id}' is not allowed."
            )
    return configured


def _ensure_issue_in_project(issue: Dict[str, Any]) -> None:
    """Checks whether the issue belongs to the project configured in the config file."""
    configured = _get_config_project_id()
    project_identifier = issue.get("project", {}).get("identifier")
    project_id = issue.get("project", {}).get("id")
    if str(project_identifier) != configured and str(project_id) != str(REDMINE_CONFIG.get("project_id_numeric")):
        raise SystemExit(
            f"The issue belongs to project '{project_identifier or project_id}', "
            f"but operations are only allowed on the configured project ({configured})."
        )


class RedmineError(Exception):
    pass


def api_request(method: str, path: str, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None) -> Any:
    url = urllib.parse.urljoin(BASE_URL, path)

    if params:
        url = f"{url}?{urllib.parse.urlencode({k: v for k, v in params.items() if v is not None and v != ''})}"

    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("X-Redmine-API-Key", API_KEY)
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            if not raw:
                return None
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8")
        raise RedmineError(f"Redmine API error {e.code}: {msg}")


def format_issue(issue: Dict[str, Any]) -> str:
    lines: List[str] = [
        f"#{issue.get('id')} [{issue.get('tracker', {}).get('name')}] {issue.get('subject')}",
        f"  Project: {issue.get('project', {}).get('name')}",
        f"  Status: {issue.get('status', {}).get('name')}  |  Priority: {issue.get('priority', {}).get('name')}",
    ]
    if issue.get("assigned_to"):
        lines.append(f"  Assignee: {issue['assigned_to'].get('name')}")
    if issue.get("fixed_version"):
        lines.append(f"  Version: {issue['fixed_version'].get('name')}")
    if issue.get("created_on"):
        lines.append(f"  Created: {issue['created_on'].split('T')[0]}  |  Updated: {issue.get('updated_on', '').split('T')[0]}")
    if issue.get("description"):
        desc = issue["description"]
        lines.append(f"\n  Description: {desc[:300]}{('...' if len(desc) > 300 else '')}")
    return "\n".join(lines)


def cmd_list_projects(args: argparse.Namespace) -> int:
    # We limit to the configured project's information.
    project_id = _ensure_project_scope(None)
    data = api_request("GET", f"/projects/{project_id}.json")
    p = data.get("project", {})
    desc = p.get("description") or "no description"
    print(f"[{p.get('id')}] {p.get('name')} ({p.get('identifier')}) — {desc[:80]}")
    return 0


def cmd_list_issues(args: argparse.Namespace) -> int:
    project_id = _ensure_project_scope(args.project_id)
    params: Dict[str, Any] = {
        "project_id": project_id,
        "status_id": args.status_id or "open",
        "assigned_to_id": args.assigned_to_id,
        "tracker_id": args.tracker_id,
        "limit": args.limit or 25,
        "offset": args.offset,
        "sort": args.sort or "updated_on:desc",
    }
    data = api_request("GET", "/issues.json", params)
    issues = data.get("issues", [])
    if not issues:
        print("No issues found.")
        return 0
    for issue in issues:
        print(format_issue(issue))
        print()
    return 0


def cmd_get_issue(args: argparse.Namespace) -> int:
    data = api_request("GET", f"/issues/{args.id}.json", {"include": "journals,attachments,children"})
    issue = data.get("issue", {})
    _ensure_issue_in_project(issue)
    lines: List[str] = [
        f"═══ Issue #{issue.get('id')} ═══",
        f"Subject: {issue.get('subject')}",
        f"Project: {issue.get('project', {}).get('name')}",
        f"Tracker: {issue.get('tracker', {}).get('name')}",
        f"Status: {issue.get('status', {}).get('name')}",
        f"Priority: {issue.get('priority', {}).get('name')}",
    ]
    if issue.get("assigned_to"):
        lines.append(f"Assignee: {issue['assigned_to'].get('name')}")
    else:
        lines.append("Assignee: (unassigned)")
    if issue.get("author"):
        lines.append(f"Author: {issue['author'].get('name')}")
    if issue.get("fixed_version"):
        lines.append(f"Target version: {issue['fixed_version'].get('name')}")
    if issue.get("start_date"):
        lines.append(f"Start: {issue.get('start_date')}")
    if issue.get("due_date"):
        lines.append(f"Due: {issue.get('due_date')}")
    if issue.get("done_ratio") is not None:
        lines.append(f"Progress: {issue.get('done_ratio')}%")
    if issue.get("created_on"):
        lines.append(f"Created: {issue.get('created_on').split('T')[0]}")
    if issue.get("updated_on"):
        lines.append(f"Updated: {issue.get('updated_on').split('T')[0]}")

    lines.append("\n── Description ──")
    lines.append(issue.get("description") or "(no description)")

    if issue.get("journals"):
        journals = [j for j in issue["journals"] if j.get("notes")]
        if journals:
            lines.append(f"\n── Notes/History ({len(journals)} entries) ──")
            for j in journals[-5:]:
                created = j.get("created_on", "")
                user = j.get("user", {}).get("name")
                lines.append(f"[{created.split('T')[0]}] {user}: {j.get('notes')}")

    print("\n".join(lines))
    return 0


def cmd_create_issue(args: argparse.Namespace) -> int:
    project_id = _ensure_project_scope(args.project_id)
    issue = {
        "project_id": project_id,
        "subject": args.subject,
        "description": args.description,
        "tracker_id": args.tracker_id,
        "status_id": args.status_id,
        "priority_id": args.priority_id or 2,
        "assigned_to_id": args.assigned_to_id,
        "fixed_version_id": args.fixed_version_id,
    }
    data = api_request("POST", "/issues.json", body={"issue": issue})
    issue = data.get("issue", {})
    print(f"Issue created successfully!\n#{issue.get('id')} — {issue.get('subject')}\nURL: {BASE_URL}/issues/{issue.get('id')}")
    return 0


def cmd_update_issue(args: argparse.Namespace) -> int:
    issue: Dict[str, Any] = {
        "subject": args.subject,
        "status_id": args.status_id,
        "assigned_to_id": args.assigned_to_id,
        "priority_id": args.priority_id,
        "done_ratio": args.done_ratio,
        "notes": args.notes,
        "fixed_version_id": args.fixed_version_id,
    }
    issue = {k: v for k, v in issue.items() if v is not None}

    # Comment visibility control:
    # - Default (no --public): private
    # - With --public: public
    if args.notes is not None:
        issue["private_notes"] = not args.public

    api_request("PUT", f"/issues/{args.id}.json", body={"issue": issue})
    print(f"Issue #{args.id} updated successfully.\nURL: {BASE_URL}/issues/{args.id}")
    return 0


def _get_issue_or_fail(issue_id: int, include: Optional[str] = None) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if include:
        params["include"] = include
    data = api_request("GET", f"/issues/{issue_id}.json", params)
    issue = data.get("issue", {})
    _ensure_issue_in_project(issue)
    return issue


def _find_custom_field(issue: Dict[str, Any], field_id: int) -> Optional[Dict[str, Any]]:
    for cf in issue.get("custom_fields", []) or []:
        if int(cf.get("id", -1)) == int(field_id):
            return cf
    return None


def _normalize_custom_field_values(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if str(v) != ""]
    text = str(value)
    return [text] if text != "" else []


def _payload_value_for_custom_field(existing_field: Optional[Dict[str, Any]], values: List[str]) -> Any:
    """Maintains the value format according to the current custom field type."""
    if existing_field is not None and isinstance(existing_field.get("value"), list):
        return values
    if not values:
        return ""
    return values[0]


def _normalize_tag_values(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value).strip()
    if not text:
        return []
    if "," in text:
        return [p.strip() for p in text.split(",") if p.strip()]
    return [text]


def _extract_issue_tags(issue: Dict[str, Any]) -> List[str]:
    tags: List[str] = []
    for key in ("tag_list", "tags"):
        tags.extend(_normalize_tag_values(issue.get(key)))

    # dedupe maintaining order
    deduped: List[str] = []
    seen = set()
    for tag in tags:
        marker = tag.lower()
        if marker in seen:
            continue
        seen.add(marker)
        deduped.append(tag)
    return deduped


def _has_tag_evidence(issue: Dict[str, Any], tag: str) -> bool:
    tag_lower = tag.lower()

    # Direct evidence in issue payload (when the instance exposes the field)
    if any(t.lower() == tag_lower for t in _extract_issue_tags(issue)):
        return True

    # Evidence in history/journal (when default GET doesn't expose tag_list/tags)
    for journal in issue.get("journals", []) or []:
        for detail in journal.get("details", []) or []:
            if detail.get("property") != "attr":
                continue
            if str(detail.get("name", "")).lower() not in {"tag_list", "tags"}:
                continue
            new_values = _normalize_tag_values(detail.get("new_value"))
            if any(v.lower() == tag_lower for v in new_values):
                return True

    return False


def cmd_get_issue_custom_fields(args: argparse.Namespace) -> int:
    issue = _get_issue_or_fail(args.id)
    custom_fields = issue.get("custom_fields", []) or []
    if not custom_fields:
        print(f"Issue #{args.id} has no custom fields returned by the API.")
        return 0

    if args.field_id is not None:
        field = _find_custom_field(issue, args.field_id)
        if not field:
            print(f"Custom field id={args.field_id} not found on issue #{args.id}.")
            return 0
        value = field.get("value")
        if isinstance(value, list):
            value_out = ", ".join(str(v) for v in value if str(v) != "") or "(empty)"
        else:
            value_out = str(value) if value not in (None, "") else "(empty)"
        print(f"Issue #{args.id} | Field [{field.get('id')}] {field.get('name')}: {value_out}")
        return 0

    print(f"Custom fields of issue #{args.id}:")
    for field in custom_fields:
        value = field.get("value")
        if isinstance(value, list):
            value_out = ", ".join(str(v) for v in value if str(v) != "") or "(empty)"
        else:
            value_out = str(value) if value not in (None, "") else "(empty)"
        print(f"- [{field.get('id')}] {field.get('name')}: {value_out}")
    return 0


def cmd_add_issue_custom_field_value(args: argparse.Namespace) -> int:
    issue = _get_issue_or_fail(args.id)
    existing_field = _find_custom_field(issue, args.field_id)
    current_values = _normalize_custom_field_values(existing_field.get("value") if existing_field else None)

    if args.value in current_values:
        print(
            f"Issue #{args.id}: value '{args.value}' already exists in custom field {args.field_id}. No changes made."
        )
        return 0

    new_values = current_values + [args.value]
    payload_value = _payload_value_for_custom_field(existing_field, new_values)

    api_request(
        "PUT",
        f"/issues/{args.id}.json",
        body={
            "issue": {
                "custom_fields": [
                    {
                        "id": args.field_id,
                        "value": payload_value,
                    }
                ]
            }
        },
    )
    print(
        f"Issue #{args.id}: value '{args.value}' added to custom field {args.field_id} successfully.\n"
        f"URL: {BASE_URL}/issues/{args.id}"
    )
    return 0


def cmd_remove_issue_custom_field_value(args: argparse.Namespace) -> int:
    issue = _get_issue_or_fail(args.id)
    existing_field = _find_custom_field(issue, args.field_id)
    if not existing_field:
        print(f"Issue #{args.id}: custom field {args.field_id} not found. No changes made.")
        return 0

    current_values = _normalize_custom_field_values(existing_field.get("value"))
    if args.value not in current_values:
        print(
            f"Issue #{args.id}: value '{args.value}' does not exist in custom field {args.field_id}. No changes made."
        )
        return 0

    new_values = [v for v in current_values if v != args.value]
    payload_value = _payload_value_for_custom_field(existing_field, new_values)

    api_request(
        "PUT",
        f"/issues/{args.id}.json",
        body={
            "issue": {
                "custom_fields": [
                    {
                        "id": args.field_id,
                        "value": payload_value,
                    }
                ]
            }
        },
    )
    print(
        f"Issue #{args.id}: value '{args.value}' removed from custom field {args.field_id} successfully.\n"
        f"URL: {BASE_URL}/issues/{args.id}"
    )
    return 0


def cmd_add_issue_tag(args: argparse.Namespace) -> int:
    tag = (args.tag or "").strip()
    if not tag:
        raise RedmineError("The provided tag is empty.")
    # Get existing tags and prepare payload that preserves already-applied tags
    issue_before = _get_issue_or_fail(args.id, include="journals")
    existing_tags = _extract_issue_tags(issue_before)

    # If it already exists, do nothing
    if any(t.lower() == tag.lower() for t in existing_tags):
        print(f"Issue #{args.id}: tag '{tag}' already exists. No changes made.")
        return 0

    # Merge preserving order and avoiding duplicates (case-insensitive)
    merged: List[str] = []
    seen = set()
    for t in existing_tags:
        key = t.lower()
        if key in seen:
            continue
        seen.add(key)
        merged.append(t)
    if tag.lower() not in seen:
        merged.append(tag)

    # Try variations keeping all existing tags + the new one
    attempts = [
        ("tag_list_array", {"tag_list": merged}),
        ("tag_list_string", {"tag_list": ", ".join(merged)}),
        ("tags_array", {"tags": merged}),
        ("tags_string", {"tags": ", ".join(merged)}),
    ]

    errors: List[str] = []
    for attempt_name, issue_payload in attempts:
        try:
            api_request("PUT", f"/issues/{args.id}.json", body={"issue": issue_payload})
        except RedmineError as e:
            errors.append(f"{attempt_name}: {e}")
            continue

        issue_after = _get_issue_or_fail(args.id, include="journals")
        if _has_tag_evidence(issue_after, tag):
            print(
                f"Issue #{args.id}: tag '{tag}' added successfully using attempt '{attempt_name}'.\n"
                f"URL: {BASE_URL}/issues/{args.id}"
            )
            return 0

        errors.append(f"{attempt_name}: PUT accepted, but no tag evidence in response/journal")

    raise RedmineError(
        "Failed to add native tag to issue. Attempts executed: " + " | ".join(errors)
    )


def cmd_list_issue_statuses(args: argparse.Namespace) -> int:
    data = api_request("GET", "/issue_statuses.json")
    lines = [f"[{s.get('id')}] {s.get('name')}{' (closed)' if s.get('is_closed') else ''}" for s in data.get('issue_statuses', [])]
    print("\n".join(lines))
    return 0


def cmd_list_trackers(args: argparse.Namespace) -> int:
    data = api_request("GET", "/trackers.json")
    lines = [f"[{t.get('id')}] {t.get('name')}" for t in data.get('trackers', [])]
    print("\n".join(lines))
    return 0


def cmd_list_versions(args: argparse.Namespace) -> int:
    project_id = _ensure_project_scope(args.project_id)
    data = api_request("GET", f"/projects/{project_id}/versions.json")
    versions = data.get("versions", [])
    if not versions:
        print("No versions found.")
        return 0
    for v in versions:
        line = f"[{v.get('id')}] {v.get('name')} — Status: {v.get('status')}"
        if v.get("due_date"):
            line += f" | Due: {v.get('due_date')}"
        print(line)
    return 0


def cmd_search_issues(args: argparse.Namespace) -> int:
    params: Dict[str, Any] = {"q": args.query, "issues": 1, "limit": args.limit or 20}
    project_id = _ensure_project_scope(args.project_id)
    params["scope"] = "project"
    path = f"/projects/{project_id}/search.json"
    data = api_request("GET", path, params)
    results = data.get("results") or []
    if not results:
        print("No results found.")
        return 0
    for r in results:
        title = r.get("title")
        desc = (r.get("description") or "")[:100]
        print(f"#{r.get('id')} {title}\n  {desc}\n  URL: {BASE_URL}{r.get('url')}\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Redmine helper script (Python)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list_projects", help="Lists all available projects in Redmine").add_argument("--limit", type=int, default=100)

    li = sub.add_parser("list_issues", help="Lists Redmine issues with optional filters")
    li.add_argument("--project_id", type=str)
    li.add_argument("--status_id", type=str)
    li.add_argument("--assigned_to_id", type=str)
    li.add_argument("--tracker_id", type=str)
    li.add_argument("--limit", type=int, default=25)
    li.add_argument("--offset", type=int)
    li.add_argument("--sort", type=str)

    gi = sub.add_parser("get_issue", help="Fetches full details of an issue by ID")
    gi.add_argument("id", type=int)

    ci = sub.add_parser("create_issue", help="Creates a new issue in Redmine (always uses the configured project)")
    ci.add_argument("--project_id", type=str, help="Optional (will be validated against the configured project)")
    ci.add_argument("--subject", required=True, type=str)
    ci.add_argument("--description", type=str)
    ci.add_argument("--tracker_id", type=int)
    ci.add_argument("--status_id", type=int)
    ci.add_argument("--priority_id", type=int)
    ci.add_argument("--assigned_to_id", type=int)
    ci.add_argument("--fixed_version_id", type=int)

    ui = sub.add_parser("update_issue", help="Updates fields of an existing issue")
    ui.add_argument("id", type=int)
    ui.add_argument("--subject", type=str)
    ui.add_argument("--status_id", type=int)
    ui.add_argument("--assigned_to_id", type=int)
    ui.add_argument("--priority_id", type=int)
    ui.add_argument("--done_ratio", type=int)
    ui.add_argument("--notes", type=str)
    ui.add_argument("--public", action="store_true", help="Marks the note as public (default: private)")
    ui.add_argument("--fixed_version_id", type=int)

    sub.add_parser("list_issue_statuses", help="Lists all available issue statuses in Redmine")
    sub.add_parser("list_trackers", help="Lists available trackers (issue types) in Redmine")

    lv = sub.add_parser("list_versions", help="Lists versions (sprints/milestones) of the configured project")
    lv.add_argument("--project_id", type=str, help="Optional (will be validated against the configured project)")

    si = sub.add_parser("search_issues", help="Searches issues by text in Redmine")
    si.add_argument("query", type=str)
    si.add_argument("--project_id", type=str)
    si.add_argument("--limit", type=int, default=20)

    gcf = sub.add_parser(
        "get_issue_custom_fields",
        help="Gets custom fields of a specific issue (all or by field_id)",
    )
    gcf.add_argument("id", type=int)
    gcf.add_argument("--field_id", type=int)

    acf = sub.add_parser(
        "add_issue_custom_field_value",
        help="Adds a value to a custom field of a specific issue",
    )
    acf.add_argument("id", type=int)
    acf.add_argument("--field_id", type=int, required=True)
    acf.add_argument("--value", type=str, required=True)

    rcf = sub.add_parser(
        "remove_issue_custom_field_value",
        help="Removes a value from a custom field of a specific issue",
    )
    rcf.add_argument("id", type=int)
    rcf.add_argument("--field_id", type=int, required=True)
    rcf.add_argument("--value", type=str, required=True)

    ait = sub.add_parser(
        "add_issue_tag",
        help="Adds a native tag to an issue using automatic fallback (tag_list/tags)",
    )
    ait.add_argument("id", type=int)
    ait.add_argument("--tag", type=str, required=True)

    args = parser.parse_args()

    # Ensures Redmine configuration exists in YAML (.github/config.yaml or .vscode/config.yaml)
    # and loads the configured project into memory to limit operations.
    global REDMINE_CONFIG
    REDMINE_CONFIG = ensure_redmine_config()

    try:
        if args.command == "list_projects":
            return cmd_list_projects(args)
        if args.command == "list_issues":
            return cmd_list_issues(args)
        if args.command == "get_issue":
            return cmd_get_issue(args)
        if args.command == "create_issue":
            return cmd_create_issue(args)
        if args.command == "update_issue":
            return cmd_update_issue(args)
        if args.command == "list_issue_statuses":
            return cmd_list_issue_statuses(args)
        if args.command == "list_trackers":
            return cmd_list_trackers(args)
        if args.command == "list_versions":
            return cmd_list_versions(args)
        if args.command == "search_issues":
            return cmd_search_issues(args)
        if args.command == "get_issue_custom_fields":
            return cmd_get_issue_custom_fields(args)
        if args.command == "add_issue_custom_field_value":
            return cmd_add_issue_custom_field_value(args)
        if args.command == "remove_issue_custom_field_value":
            return cmd_remove_issue_custom_field_value(args)
        if args.command == "add_issue_tag":
            return cmd_add_issue_tag(args)
    except RedmineError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
