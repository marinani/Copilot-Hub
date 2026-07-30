import * as vscode from "vscode";
import { StatusPresentation, StatusSeverity } from "./format";

export class UsageStatusBar {
  private readonly item: vscode.StatusBarItem;

  constructor() {
    this.item = vscode.window.createStatusBarItem(
      vscode.StatusBarAlignment.Right,
      100
    );
    this.item.command = "cursorUsageBar.refresh";
    this.item.text = "Cursor …";
    this.item.tooltip = "Carregando uso do plano Cursor…";
    this.item.show();
  }

  update(presentation: StatusPresentation): void {
    this.item.text = `$(pulse) ${presentation.text}`;
    this.item.tooltip = presentation.tooltip;
    this.applySeverity(presentation.severity);
  }

  private applySeverity(severity: StatusSeverity): void {
    switch (severity) {
      case "warning":
        this.item.backgroundColor = new vscode.ThemeColor(
          "statusBarItem.warningBackground"
        );
        break;
      case "critical":
        this.item.backgroundColor = new vscode.ThemeColor(
          "statusBarItem.errorBackground"
        );
        break;
      default:
        this.item.backgroundColor = undefined;
        break;
    }
  }

  dispose(): void {
    this.item.dispose();
  }
}
