#!/usr/bin/env python3
import argparse
import concurrent.futures
import json
import os
import sys
import unicodedata
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple


BASE_URL = os.environ.get("REDMINE_URL", "https://redmine.ici.curitiba.org.br")
API_KEY = os.environ.get("REDMINE_API_KEY", "")


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch)).lower()


def api_get(path: str, params: Optional[Dict[str, Any]] = None) -> Any:
    if not API_KEY:
        print(json.dumps({"error": "REDMINE_API_KEY_MISSING"}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)

    url = urllib.parse.urljoin(BASE_URL, path)
    if params:
        safe_params = {key: value for key, value in params.items() if value not in (None, "")}
        if safe_params:
            url += "?" + urllib.parse.urlencode(safe_params)

    request = urllib.request.Request(url)
    request.add_header("X-Redmine-API-Key", API_KEY)
    request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_all_time_entries(from_date: str, to_date: str, project_id: Optional[str]) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    offset = 0
    limit = 100

    while True:
        payload = api_get(
            "/time_entries.json",
            {
                "from": from_date,
                "to": to_date,
                "project_id": project_id,
                "limit": limit,
                "offset": offset,
            },
        )
        batch = payload.get("time_entries", [])
        entries.extend(batch)
        total_count = int(payload.get("total_count", len(entries)))
        offset += len(batch)
        if not batch or offset >= total_count:
            break

    return entries


def collect_issue_ids(entries: Iterable[Dict[str, Any]]) -> List[int]:
    issue_ids: Set[int] = set()
    for entry in entries:
        issue = entry.get("issue") or {}
        issue_id = issue.get("id")
        if issue_id:
            issue_ids.add(int(issue_id))
    return sorted(issue_ids)


def fetch_issue_details(issue_ids: Iterable[int]) -> Dict[int, Dict[str, Any]]:
    details: Dict[int, Dict[str, Any]] = {}

    def fetch_one(issue_id: int) -> Tuple[int, Dict[str, Any]]:
        try:
            payload = api_get(f"/issues/{issue_id}.json")
            return issue_id, payload.get("issue", {})
        except Exception:
            return issue_id, {}

    issue_id_list = list(issue_ids)
    if not issue_id_list:
        return details

    max_workers = min(12, max(1, len(issue_id_list)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for issue_id, issue in executor.map(fetch_one, issue_id_list):
            details[issue_id] = issue

    return details


def issue_estimate(issue: Dict[str, Any]) -> float:
    value = issue.get("estimated_hours")
    if value in (None, ""):
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def build_activity_key(entry: Dict[str, Any], issue_id: Optional[int]) -> str:
    if issue_id is not None:
        return f"issue:{issue_id}"
    entry_id = entry.get("id")
    if entry_id is not None:
        return f"time-entry:{entry_id}"
    spent_on = str(entry.get("spent_on", "sem-data"))
    comments = str(entry.get("comments", "sem-comentario"))
    activity_name = str((entry.get("activity") or {}).get("name", "sem-atividade"))
    return f"fallback:{spent_on}:{activity_name}:{comments}"


def to_group_rows(groups: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for name, data in groups.items():
        estimated = sum(float(data["issue_estimates"].get(issue_id, 0.0)) for issue_id in data["issue_ids"])
        hours = float(data["hours"])
        rows.append(
            {
                "name": name,
                "hours": round(hours, 2),
                "estimated": round(estimated, 2),
                "delta": round(hours - estimated, 2),
                "entries": len(data["activity_keys"]),
            }
        )
    rows.sort(key=lambda item: (-float(item["hours"]), item["name"]))
    return rows


def to_sd_rows(groups: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for classification, data in groups.items():
        estimated = sum(float(data["issue_estimates"].get(issue_id, 0.0)) for issue_id in data["issue_ids"])
        hours = float(data["hours"])
        rows.append(
            {
                "classification": classification,
                "hours": round(hours, 2),
                "estimated": round(estimated, 2),
                "delta": round(hours - estimated, 2),
                "entries": len(data["activity_keys"]),
            }
        )
    rows.sort(key=lambda item: (-float(item["hours"]), item["classification"]))
    return rows


def classify_service_desk(entry: Dict[str, Any], issue: Dict[str, Any]) -> Tuple[bool, str]:
    fields = [
        str((entry.get("project") or {}).get("name", "")),
        str((issue.get("project") or {}).get("name", "")),
        str((entry.get("activity") or {}).get("name", "")),
        str((issue.get("tracker") or {}).get("name", "")),
        str((issue.get("category") or {}).get("name", "")),
        str(issue.get("subject", "")),
    ]
    haystack = " ".join(normalize_text(field) for field in fields if field)

    incident_terms = ("incidente",)
    request_terms = ("requisicao", "requisicao de servico", "solicitacao", "solicitacao de servico")
    sd_terms = ("service desk", "servicedesk", "central de servicos")

    is_incident = any(term in haystack for term in incident_terms)
    is_request = any(term in haystack for term in request_terms)
    is_service_desk = is_incident or is_request or any(term in haystack for term in sd_terms)

    if is_incident:
        return is_service_desk, "Incidente de Service Desk"
    if is_request:
        return is_service_desk, "Requisição de Service Desk"
    if is_service_desk:
        return True, "Não classificado"
    return False, "Não classificado"


def build_planning_stats(
    total_hours: float,
    total_estimated: float,
    total_entries: int,
    project_count: int,
    issues_total: int,
    issues_with_estimate: int,
    start_date: date,
    end_date: date,
) -> List[Dict[str, str]]:
    days = max(1, (end_date - start_date).days + 1)
    weeks = max(1, round(days / 7))
    coverage = (issues_with_estimate / issues_total) * 100 if issues_total else 0.0
    variation = ((total_hours - total_estimated) / total_estimated) * 100 if total_estimated else 0.0

    return [
        {
            "name": "Capacidade média semanal da equipe",
            "formula": "Horas lançadas / semanas do mês",
            "value": f"{(total_hours / weeks):.2f}h/semana",
        },
        {
            "name": "Carga média por projeto",
            "formula": "Horas lançadas / projetos ativos",
            "value": f"{(total_hours / project_count if project_count else 0.0):.2f}h/projeto",
        },
        {
            "name": "Carga média por lançamento",
            "formula": "Horas lançadas / lançamentos",
            "value": f"{(total_hours / total_entries if total_entries else 0.0):.2f}h/lancamento",
        },
        {
            "name": "Cobertura de estimativas",
            "formula": "Issues com estimativa / issues totais",
            "value": f"{coverage:.2f}%",
        },
        {
            "name": "Variação relativa de esforço",
            "formula": "(L-E) / E",
            "value": f"{variation:.2f}%",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Consolida dados do Redmine para o relatório mensal de desenvolvedores.")
    parser.add_argument("--output", required=True, help="Arquivo JSON consolidado de saída.")
    parser.add_argument("--from-date", required=True, help="Data inicial no formato YYYY-MM-DD.")
    parser.add_argument("--to-date", required=True, help="Data final no formato YYYY-MM-DD.")
    parser.add_argument("--project-id", help="ID do projeto no Redmine.")
    args = parser.parse_args()

    start_date = datetime.strptime(args.from_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(args.to_date, "%Y-%m-%d").date()

    entries = fetch_all_time_entries(args.from_date, args.to_date, args.project_id)
    issue_ids = collect_issue_ids(entries)
    issue_details = fetch_issue_details(issue_ids)
    issue_estimates = {issue_id: issue_estimate(detail) for issue_id, detail in issue_details.items()}

    collaborator_groups: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"hours": 0.0, "activity_keys": set(), "issue_ids": set(), "issue_estimates": issue_estimates})
    project_groups: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"hours": 0.0, "activity_keys": set(), "issue_ids": set(), "issue_estimates": issue_estimates})
    activity_groups: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"hours": 0.0, "activity_keys": set(), "issue_ids": set(), "issue_estimates": issue_estimates})
    subtables: Dict[str, Dict[str, Dict[str, Dict[str, Any]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"hours": 0.0, "activity_keys": set(), "issue_ids": set(), "issue_estimates": issue_estimates})))
    service_desk_groups: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"hours": 0.0, "activity_keys": set(), "issue_ids": set(), "issue_estimates": issue_estimates})
    service_desk_subtables: Dict[str, Dict[str, Dict[Tuple[str, str], Dict[str, Any]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"hours": 0.0, "activity_keys": set(), "issue_ids": set(), "issue_estimates": issue_estimates})))

    for entry in entries:
        hours = float(entry.get("hours", 0.0) or 0.0)
        issue_info = entry.get("issue") or {}
        issue_id = int(issue_info["id"]) if issue_info.get("id") else None
        issue = issue_details.get(issue_id, {}) if issue_id else {}
        activity_key = build_activity_key(entry, issue_id)

        collaborator = str((entry.get("user") or {}).get("name", "Não informado"))
        project = str((entry.get("project") or {}).get("name", "Sem projeto"))
        activity = str((entry.get("activity") or {}).get("name", "Sem atividade"))

        for groups, key in (
            (collaborator_groups, collaborator),
            (project_groups, project),
            (activity_groups, activity),
        ):
            groups[key]["hours"] += hours
            groups[key]["activity_keys"].add(activity_key)
            if issue_id:
                groups[key]["issue_ids"].add(issue_id)

        sub_group = subtables[project][activity][collaborator]
        sub_group["hours"] += hours
        sub_group["activity_keys"].add(activity_key)
        if issue_id:
            sub_group["issue_ids"].add(issue_id)

        is_service_desk, classification = classify_service_desk(entry, issue)
        if is_service_desk:
            service_desk_groups[classification]["hours"] += hours
            service_desk_groups[classification]["activity_keys"].add(activity_key)
            if issue_id:
                service_desk_groups[classification]["issue_ids"].add(issue_id)

            sd_sub_group = service_desk_subtables[project][activity][(classification, collaborator)]
            sd_sub_group["hours"] += hours
            sd_sub_group["activity_keys"].add(activity_key)
            if issue_id:
                sd_sub_group["issue_ids"].add(issue_id)

    collaborators = to_group_rows(collaborator_groups)
    projects = to_group_rows(project_groups)
    activity_types = to_group_rows(activity_groups)
    service_desk = to_sd_rows(service_desk_groups)

    subtables_payload: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
    for project_name, activity_map in sorted(subtables.items()):
        subtables_payload[project_name] = {}
        for activity_name, collaborator_map in sorted(activity_map.items()):
            rows: List[Dict[str, Any]] = []
            for collaborator_name, data in collaborator_map.items():
                estimated = sum(float(issue_estimates.get(issue_id, 0.0)) for issue_id in data["issue_ids"])
                hours = float(data["hours"])
                rows.append(
                    {
                        "name": collaborator_name,
                        "hours": round(hours, 2),
                        "estimated": round(estimated, 2),
                        "delta": round(hours - estimated, 2),
                        "entries": len(data["activity_keys"]),
                    }
                )
            rows.sort(key=lambda item: (-float(item["hours"]), item["name"]))
            subtables_payload[project_name][activity_name] = rows

    service_desk_subtables_payload: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
    for project_name, activity_map in sorted(service_desk_subtables.items()):
        service_desk_subtables_payload[project_name] = {}
        for activity_name, detail_map in sorted(activity_map.items()):
            rows = []
            for (classification, collaborator_name), data in detail_map.items():
                estimated = sum(float(issue_estimates.get(issue_id, 0.0)) for issue_id in data["issue_ids"])
                hours = float(data["hours"])
                rows.append(
                    {
                        "name": collaborator_name,
                        "classification": classification,
                        "hours": round(hours, 2),
                        "estimated": round(estimated, 2),
                        "delta": round(hours - estimated, 2),
                        "entries": len(data["activity_keys"]),
                    }
                )
            rows.sort(key=lambda item: (item["classification"], -float(item["hours"]), item["name"]))
            service_desk_subtables_payload[project_name][activity_name] = rows

    total_hours = round(sum(float(entry.get("hours", 0.0) or 0.0) for entry in entries), 2)
    total_entries = len(entries)
    total_estimated = round(sum(issue_estimates.values()), 2)
    issues_with_estimate = sum(1 for value in issue_estimates.values() if value > 0)

    payload = {
        "collaborators": collaborators,
        "projects": projects,
        "activity_types": activity_types,
        "service_desk": service_desk,
        "subtables": subtables_payload,
        "service_desk_subtables": service_desk_subtables_payload,
        "planning_stats": build_planning_stats(
            total_hours=total_hours,
            total_estimated=total_estimated,
            total_entries=total_entries,
            project_count=len(projects),
            issues_total=len(issue_ids),
            issues_with_estimate=issues_with_estimate,
            start_date=start_date,
            end_date=end_date,
        ),
        "meta": {
            "total_hours": total_hours,
            "total_estimated_unique_issues": total_estimated,
            "total_entries": total_entries,
            "issues_total": len(issue_ids),
            "issues_with_estimate": issues_with_estimate,
        },
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())