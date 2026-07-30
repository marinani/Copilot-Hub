"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const auth_1 = require("./auth");
const format_1 = require("./format");
const status_bar_1 = require("./status-bar");
const usage_api_1 = require("./usage-api");
let statusBar;
let output;
let pollTimer;
let refreshing = false;
function getOutput() {
    if (!output) {
        output = vscode.window.createOutputChannel("Cursor Usage Bar");
    }
    return output;
}
function log(message) {
    getOutput().appendLine(`[${new Date().toISOString()}] ${message}`);
}
function readConfig() {
    const cfg = vscode.workspace.getConfiguration("cursorUsageBar");
    const poll = Math.max(60, cfg.get("pollIntervalSeconds", 300));
    const warningPercent = cfg.get("warningPercent", 80);
    const criticalPercent = cfg.get("criticalPercent", 95);
    return { poll, warningPercent, criticalPercent };
}
async function refreshUsage() {
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
        const token = await (0, auth_1.getAccessToken)();
        log("Consultando usage na API…");
        const usage = await (0, usage_api_1.fetchPeriodUsage)(token);
        const presentation = (0, format_1.buildPresentation)(usage, {
            warningPercent,
            criticalPercent,
            updatedAt: new Date(),
        });
        statusBar.update(presentation);
        log(`OK: ${presentation.text}`);
    }
    catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        log(`Erro: ${message}`);
        statusBar.update((0, format_1.buildErrorPresentation)(message));
    }
    finally {
        refreshing = false;
    }
}
function restartPoll() {
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
function activate(context) {
    statusBar = new status_bar_1.UsageStatusBar();
    context.subscriptions.push({
        dispose: () => statusBar?.dispose(),
    });
    context.subscriptions.push(vscode.commands.registerCommand("cursorUsageBar.refresh", () => {
        void refreshUsage();
    }));
    context.subscriptions.push(vscode.commands.registerCommand("cursorUsageBar.showOutput", () => {
        getOutput().show(true);
    }));
    context.subscriptions.push(vscode.workspace.onDidChangeConfiguration((e) => {
        if (e.affectsConfiguration("cursorUsageBar")) {
            restartPoll();
            void refreshUsage();
        }
    }));
    restartPoll();
    void refreshUsage();
}
function deactivate() {
    if (pollTimer) {
        clearInterval(pollTimer);
        pollTimer = undefined;
    }
    statusBar?.dispose();
    statusBar = undefined;
    output?.dispose();
    output = undefined;
}
//# sourceMappingURL=extension.js.map