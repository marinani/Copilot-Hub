import {
  PeriodUsage,
  getOverageCents,
} from "./usage-api";

export type StatusSeverity = "normal" | "warning" | "critical" | "error";

export interface StatusPresentation {
  text: string;
  tooltip: string;
  severity: StatusSeverity;
}

/** Traduz mensagens comuns da API Cursor (vêm em inglês). */
export function traduzirMensagemApi(message: string): string {
  const mapa: Array<[RegExp, string]> = [
    [/you've hit your usage limit/i, "Você atingiu o limite de uso do plano"],
    [/you've used (\d+)% of your usage limit/i, "Você usou $1% do limite do plano"],
    [/you have used (\d+)% of your usage limit/i, "Você usou $1% do limite do plano"],
    [/usage limit/i, "limite de uso"],
    [/on-demand/i, "sob demanda"],
  ];

  let out = message.trim();
  for (const [re, repl] of mapa) {
    if (re.test(out)) {
      out = out.replace(re, repl);
      break;
    }
  }
  return out;
}

function formatUsdFromCents(cents: number): string {
  const dollars = cents / 100;
  return dollars.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

function formatPercent(value: number): string {
  if (!Number.isFinite(value)) {
    return "0";
  }
  return String(Math.round(value));
}

function formatCycleDate(msOrIso?: string): string {
  if (!msOrIso) {
    return "—";
  }
  const asNum = Number(msOrIso);
  const date = Number.isFinite(asNum) ? new Date(asNum) : new Date(msOrIso);
  if (Number.isNaN(date.getTime())) {
    return "—";
  }
  return date.toLocaleDateString("pt-BR");
}

function diasRestantesCiclo(billingCycleEnd?: string): string | undefined {
  if (!billingCycleEnd) {
    return undefined;
  }
  const asNum = Number(billingCycleEnd);
  const fim = Number.isFinite(asNum) ? new Date(asNum) : new Date(billingCycleEnd);
  if (Number.isNaN(fim.getTime())) {
    return undefined;
  }
  const ms = fim.getTime() - Date.now();
  const dias = Math.max(0, Math.ceil(ms / (24 * 60 * 60 * 1000)));
  if (dias === 0) {
    return "Renova hoje";
  }
  if (dias === 1) {
    return "Renova amanhã";
  }
  return `Renova em ${dias} dias`;
}

export function buildPresentation(
  usage: PeriodUsage,
  opts: {
    warningPercent: number;
    criticalPercent: number;
    updatedAt: Date;
  }
): StatusPresentation {
  const percent = usage.planUsage?.totalPercentUsed ?? 0;
  const overageCents = getOverageCents(usage);
  const hasOverage = overageCents > 0;

  let text = `Cursor ${formatPercent(percent)}%`;
  if (hasOverage) {
    text += ` · +${formatUsdFromCents(overageCents)}`;
  }

  let severity: StatusSeverity = "normal";
  if (hasOverage || percent >= opts.criticalPercent) {
    severity = "critical";
  } else if (percent >= opts.warningPercent) {
    severity = "warning";
  }

  const lines: string[] = ["Uso do Cursor", ""];

  if (usage.requestsMax !== undefined) {
    lines.push(
      `Requisições: ${usage.requestsUsed ?? 0} / ${usage.requestsMax}`
    );
  }

  if (usage.planUsage) {
    const p = usage.planUsage;
    lines.push(`Uso do plano: ${formatPercent(p.totalPercentUsed)}%`);
    if (p.limit > 0) {
      lines.push(
        `Incluso: ${formatUsdFromCents(p.includedSpend)} / ${formatUsdFromCents(p.limit)}`
      );
      lines.push(`Restante: ${formatUsdFromCents(p.remaining)}`);
    }
    if (p.autoPercentUsed !== undefined) {
      lines.push(`Modo Auto: ${formatPercent(p.autoPercentUsed)}%`);
    }
    if (p.apiPercentUsed !== undefined) {
      lines.push(`Modo API: ${formatPercent(p.apiPercentUsed)}%`);
    }
  }

  if (hasOverage) {
    lines.push(`Excedente (sob demanda): ${formatUsdFromCents(overageCents)}`);
    const s = usage.spendLimitUsage;
    if (s?.individualLimit !== undefined && s.individualLimit > 0) {
      lines.push(
        `Limite sob demanda: ${formatUsdFromCents(s.individualLimit)}`
      );
    }
    if (s?.pooledUsed !== undefined && s.pooledLimit !== undefined && s.pooledLimit > 0) {
      lines.push(
        `Pool do time: ${formatUsdFromCents(s.pooledUsed)} / ${formatUsdFromCents(s.pooledLimit)}`
      );
    }
  } else {
    lines.push("Excedente (sob demanda): $0.00");
  }

  const renovacao = diasRestantesCiclo(usage.billingCycleEnd);
  lines.push(
    `Ciclo: ${formatCycleDate(usage.billingCycleStart)} → ${formatCycleDate(usage.billingCycleEnd)}` +
      (renovacao ? ` (${renovacao})` : "")
  );

  if (usage.displayMessage) {
    lines.push("");
    lines.push(traduzirMensagemApi(usage.displayMessage));
  }
  lines.push("");
  lines.push(`Atualizado: ${opts.updatedAt.toLocaleString("pt-BR")}`);
  lines.push("Clique para atualizar");

  return {
    text,
    tooltip: lines.join("\n"),
    severity,
  };
}

export function buildErrorPresentation(message: string): StatusPresentation {
  const isLogin =
    /login|token|state\.vscdb|logado/i.test(message);
  return {
    text: isLogin ? "Cursor: faça login" : "Cursor: —",
    tooltip: `Uso do Cursor\n\n${message}\n\nComando: "Cursor Usage Bar: Atualizar agora"`,
    severity: "error",
  };
}
