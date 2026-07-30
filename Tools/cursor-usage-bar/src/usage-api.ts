export interface PlanUsage {
  totalSpend: number;
  includedSpend: number;
  remaining: number;
  limit: number;
  totalPercentUsed: number;
  autoPercentUsed?: number;
  apiPercentUsed?: number;
}

export interface SpendLimitUsage {
  totalSpend: number;
  individualUsed?: number;
  individualLimit?: number;
  individualRemaining?: number;
  pooledUsed?: number;
  pooledLimit?: number;
  limitType?: string;
}

export interface PeriodUsage {
  billingCycleStart?: string;
  billingCycleEnd?: string;
  planUsage?: PlanUsage;
  spendLimitUsage?: SpendLimitUsage;
  displayMessage?: string;
  /** Fallback enterprise (requests). */
  requestsUsed?: number;
  requestsMax?: number;
}

const DEFAULT_BASE = "https://api2.cursor.sh";

function centsToNumber(value: unknown): number {
  const n = typeof value === "number" ? value : Number(value);
  return Number.isFinite(n) ? n : 0;
}

function parseDashboardUsage(data: Record<string, unknown>): PeriodUsage {
  const planRaw = (data.planUsage || {}) as Record<string, unknown>;
  const spendRaw = (data.spendLimitUsage || {}) as Record<string, unknown>;

  const planUsage: PlanUsage | undefined = planRaw.limit !== undefined ||
    planRaw.totalPercentUsed !== undefined
    ? {
        totalSpend: centsToNumber(planRaw.totalSpend),
        includedSpend: centsToNumber(planRaw.includedSpend),
        remaining: centsToNumber(planRaw.remaining),
        limit: centsToNumber(planRaw.limit),
        totalPercentUsed: centsToNumber(planRaw.totalPercentUsed),
        autoPercentUsed:
          planRaw.autoPercentUsed !== undefined
            ? centsToNumber(planRaw.autoPercentUsed)
            : undefined,
        apiPercentUsed:
          planRaw.apiPercentUsed !== undefined
            ? centsToNumber(planRaw.apiPercentUsed)
            : undefined,
      }
    : undefined;

  const spendLimitUsage: SpendLimitUsage | undefined =
    spendRaw.totalSpend !== undefined ||
    spendRaw.individualUsed !== undefined
      ? {
          totalSpend: centsToNumber(spendRaw.totalSpend),
          individualUsed:
            spendRaw.individualUsed !== undefined
              ? centsToNumber(spendRaw.individualUsed)
              : undefined,
          individualLimit:
            spendRaw.individualLimit !== undefined
              ? centsToNumber(spendRaw.individualLimit)
              : undefined,
          individualRemaining:
            spendRaw.individualRemaining !== undefined
              ? centsToNumber(spendRaw.individualRemaining)
              : undefined,
          pooledUsed:
            spendRaw.pooledUsed !== undefined
              ? centsToNumber(spendRaw.pooledUsed)
              : undefined,
          pooledLimit:
            spendRaw.pooledLimit !== undefined
              ? centsToNumber(spendRaw.pooledLimit)
              : undefined,
          limitType:
            typeof spendRaw.limitType === "string"
              ? spendRaw.limitType
              : undefined,
        }
      : undefined;

  return {
    billingCycleStart:
      data.billingCycleStart !== undefined
        ? String(data.billingCycleStart)
        : undefined,
    billingCycleEnd:
      data.billingCycleEnd !== undefined
        ? String(data.billingCycleEnd)
        : undefined,
    planUsage,
    spendLimitUsage,
    displayMessage:
      typeof data.displayMessage === "string" ? data.displayMessage : undefined,
  };
}

async function fetchDashboardUsage(
  token: string,
  baseUrl: string
): Promise<PeriodUsage> {
  const url = `${baseUrl.replace(/\/$/, "")}/aiserver.v1.DashboardService/GetCurrentPeriodUsage`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      "Connect-Protocol-Version": "1",
    },
    body: "{}",
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(
      `GetCurrentPeriodUsage falhou (${res.status}): ${body.slice(0, 200)}`
    );
  }

  const data = (await res.json()) as Record<string, unknown>;
  return parseDashboardUsage(data);
}

/** Fallback Enterprise: GET /auth/usage com buckets por modelo. */
async function fetchAuthUsageFallback(
  token: string,
  baseUrl: string
): Promise<PeriodUsage> {
  const url = `${baseUrl.replace(/\/$/, "")}/auth/usage`;
  const res = await fetch(url, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`GET /auth/usage falhou (${res.status}): ${body.slice(0, 200)}`);
  }

  const data = (await res.json()) as Record<string, Record<string, unknown>>;
  const preferredKeys = ["gpt-4", "gpt-4o", "default"];
  let bucket: Record<string, unknown> | undefined;
  for (const key of preferredKeys) {
    if (data[key] && typeof data[key] === "object") {
      bucket = data[key];
      break;
    }
  }
  if (!bucket) {
    const first = Object.values(data).find(
      (v) => v && typeof v === "object" && "numRequests" in v
    );
    bucket = first as Record<string, unknown> | undefined;
  }

  if (!bucket) {
    throw new Error("Resposta /auth/usage sem buckets de requests");
  }

  const used = centsToNumber(bucket.numRequests);
  const max = centsToNumber(bucket.maxRequestUsage);
  const percent = max > 0 ? (used / max) * 100 : 0;

  return {
    planUsage: {
      totalSpend: 0,
      includedSpend: 0,
      remaining: Math.max(0, max - used),
      limit: max,
      totalPercentUsed: percent,
    },
    requestsUsed: used,
    requestsMax: max,
  };
}

/**
 * Busca uso do período atual. Preferência: Dashboard Connect RPC; fallback: /auth/usage.
 */
export async function fetchPeriodUsage(
  token: string,
  baseUrl: string = DEFAULT_BASE
): Promise<PeriodUsage> {
  try {
    return await fetchDashboardUsage(token, baseUrl);
  } catch (primaryError) {
    try {
      return await fetchAuthUsageFallback(token, baseUrl);
    } catch {
      throw primaryError;
    }
  }
}

/** On-demand usado em centavos (individual se existir, senão total). */
export function getOverageCents(usage: PeriodUsage): number {
  const s = usage.spendLimitUsage;
  if (!s) {
    return 0;
  }
  if (s.individualUsed !== undefined && s.individualUsed > 0) {
    return s.individualUsed;
  }
  return s.totalSpend > 0 ? s.totalSpend : 0;
}
