import * as vscode from "vscode";
import { getAccessToken } from "./auth";
import {
  buildErrorPresentation,
  buildPresentation,
} from "./format";
import { UsageStatusBar } from "./status-bar";
import { fetchPeriodUsage } from "./usage-api";

let statusBar: UsageStatusBar | undefined;
let output: vscode.OutputChannel | undefined;
let pollTimer: ReturnType<typeof setInterval> | undefined;
let refreshing = false;

function getOutput(): vscode.OutputChannel {
  if (!output) {
    output = vscode.window.createOutputChannel("Cursor Usage Bar");
  }
  return output;
}

function log(message: string): void {
  getOutput().appendLine(`[${new Date().toISOString()}] ${message}`);
}

function readConfig() {
  const cfg = vscode.workspace.getConfiguration("cursorUsageBar");
  const poll = Math.max(60, cfg.get<number>("pollIntervalSeconds", 300));
  const warningPercent = cfg.get<number>("warningPercent", 80);
  const criticalPercent = cfg.get<number>("criticalPercent", 95);
  return { poll, warningPercent, criticalPercent };
}

async function refreshUsage(): Promise<void> {
  if (!statusBar) {
    return;
  }
  if (refreshing) {
    return;
  }
  refreshing = true;
  try {
    const { warningPercent, criticalPercent } = readConfig();
    log("Lendo token local…");
    const token = await getAccessToken();
    log("Consultando usage na API…");
    const usage = await fetchPeriodUsage(token);
    const presentation = buildPresentation(usage, {
      warningPercent,
      criticalPercent,
      updatedAt: new Date(),
    });
    statusBar.update(presentation);
    log(`OK: ${presentation.text}`);
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    log(`Erro: ${message}`);
    statusBar.update(buildErrorPresentation(message));
  } finally {
    refreshing = false;
  }
}

function restartPoll(): void {
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = undefined;
  }
  const { poll } = readConfig();
  pollTimer = setInterval(() => {
    void refreshUsage();
  }, poll * 1000);
  log(`Poll a cada ${poll}s`);
}

export function activate(context: vscode.ExtensionContext): void {
  statusBar = new UsageStatusBar();
  context.subscriptions.push({
    dispose: () => statusBar?.dispose(),
  });

  context.subscriptions.push(
    vscode.commands.registerCommand("cursorUsageBar.refresh", () => {
      void refreshUsage();
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("cursorUsageBar.showOutput", () => {
      getOutput().show(true);
    })
  );

  context.subscriptions.push(
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration("cursorUsageBar")) {
        restartPoll();
        void refreshUsage();
      }
    })
  );

  restartPoll();
  void refreshUsage();
}

export function deactivate(): void {
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = undefined;
  }
  statusBar?.dispose();
  statusBar = undefined;
  output?.dispose();
  output = undefined;
}
