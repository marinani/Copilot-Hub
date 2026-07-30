"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchPeriodUsage = fetchPeriodUsage;
exports.getOverageCents = getOverageCents;
const DEFAULT_BASE = "https://api2.cursor.sh";
function centsToNumber(value) {
    const n = typeof value === "number" ? value : Number(value);
    return Number.isFinite(n) ? n : 0;
}
function parseDashboardUsage(data) {
    const planRaw = (data.planUsage || {});
    const spendRaw = (data.spendLimitUsage || {});
    const planUsage = planRaw.limit !== undefined ||
        planRaw.totalPercentUsed !== undefined
        ? {
            totalSpend: centsToNumber(planRaw.totalSpend),
            includedSpend: centsToNumber(planRaw.includedSpend),
            remaining: centsToNumber(planRaw.remaining),
            limit: centsToNumber(planRaw.limit),
            totalPercentUsed: centsToNumber(planRaw.totalPercentUsed),
            autoPercentUsed: planRaw.autoPercentUsed !== undefined
                ? centsToNumber(planRaw.autoPercentUsed)
                : undefined,
            apiPercentUsed: planRaw.apiPercentUsed !== undefined
                ? centsToNumber(planRaw.apiPercentUsed)
                : undefined,
        }
        : undefined;
    const spendLimitUsage = spendRaw.totalSpend !== undefined ||
        spendRaw.individualUsed !== undefined
        ? {
            totalSpend: centsToNumber(spendRaw.totalSpend),
            individualUsed: spendRaw.individualUsed !== undefined
                ? centsToNumber(spendRaw.individualUsed)
                : undefined,
            individualLimit: spendRaw.individualLimit !== undefined
                ? centsToNumber(spendRaw.individualLimit)
                : undefined,
            individualRemaining: spendRaw.individualRemaining !== undefined
                ? centsToNumber(spendRaw.individualRemaining)
                : undefined,
            pooledUsed: spendRaw.pooledUsed !== undefined
                ? centsToNumber(spendRaw.pooledUsed)
                : undefined,
            pooledLimit: spendRaw.pooledLimit !== undefined
                ? centsToNumber(spendRaw.pooledLimit)
                : undefined,
            limitType: typeof spendRaw.limitType === "string"
                ? spendRaw.limitType
                : undefined,
        }
        : undefined;
    return {
        billingCycleStart: data.billingCycleStart !== undefined
            ? String(data.billingCycleStart)
            : undefined,
        billingCycleEnd: data.billingCycleEnd !== undefined
            ? String(data.billingCycleEnd)
            : undefined,
        planUsage,
        spendLimitUsage,
        displayMessage: typeof data.displayMessage === "string" ? data.displayMessage : undefined,
    };
}
async function fetchDashboardUsage(token, baseUrl) {
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
        throw new Error(`GetCurrentPeriodUsage falhou (${res.status}): ${body.slice(0, 200)}`);
    }
    const data = (await res.json());
    return parseDashboardUsage(data);
}
/** Fallback Enterprise: GET /auth/usage com buckets por modelo. */
async function fetchAuthUsageFallback(token, baseUrl) {
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
    const data = (await res.json());
    const preferredKeys = ["gpt-4", "gpt-4o", "default"];
    let bucket;
    for (const key of preferredKeys) {
        if (data[key] && typeof data[key] === "object") {
            bucket = data[key];
            break;
        }
    }
    if (!bucket) {
        const first = Object.values(data).find((v) => v && typeof v === "object" && "numRequests" in v);
        bucket = first;
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
async function fetchPeriodUsage(token, baseUrl = DEFAULT_BASE) {
    try {
        return await fetchDashboardUsage(token, baseUrl);
    }
    catch (primaryError) {
        try {
            return await fetchAuthUsageFallback(token, baseUrl);
        }
        catch {
            throw primaryError;
        }
    }
}
/** On-demand usado em centavos (individual se existir, senão total). */
function getOverageCents(usage) {
    const s = usage.spendLimitUsage;
    if (!s) {
        return 0;
    }
    if (s.individualUsed !== undefined && s.individualUsed > 0) {
        return s.individualUsed;
    }
    return s.totalSpend > 0 ? s.totalSpend : 0;
}
//# sourceMappingURL=usage-api.js.map