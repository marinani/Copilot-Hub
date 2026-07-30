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
exports.getStateDbPath = getStateDbPath;
exports.getAccessToken = getAccessToken;
const fs = __importStar(require("fs"));
const os = __importStar(require("os"));
const path = __importStar(require("path"));
/** Caminho do state.vscdb do Cursor no SO atual. */
function getStateDbPath() {
    if (process.platform === "darwin") {
        return path.join(os.homedir(), "Library", "Application Support", "Cursor", "User", "globalStorage", "state.vscdb");
    }
    if (process.platform === "win32") {
        return path.join(process.env.APPDATA || path.join(os.homedir(), "AppData", "Roaming"), "Cursor", "User", "globalStorage", "state.vscdb");
    }
    return path.join(os.homedir(), ".config", "Cursor", "User", "globalStorage", "state.vscdb");
}
function readEntireFileSync(filePath) {
    const { size } = fs.statSync(filePath);
    if (size === 0) {
        return Buffer.alloc(0);
    }
    const buf = Buffer.allocUnsafe(size);
    const fd = fs.openSync(filePath, "r");
    try {
        const chunkSize = 64 * 1024 * 1024;
        let offset = 0;
        while (offset < size) {
            const len = Math.min(chunkSize, size - offset);
            const read = fs.readSync(fd, buf, offset, len, offset);
            if (read === 0) {
                throw new Error("Fim inesperado ao ler state.vscdb");
            }
            offset += read;
        }
    }
    finally {
        fs.closeSync(fd);
    }
    return buf;
}
/**
 * Lê o access token da sessão Cursor já logada.
 * Nunca pede senha — só leitura do banco local.
 */
async function getAccessToken() {
    const dbPath = getStateDbPath();
    if (!fs.existsSync(dbPath)) {
        throw new Error("Banco state.vscdb não encontrado. Faça login no Cursor e tente de novo.");
    }
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    const initSqlJs = require("sql.js");
    const SQL = await initSqlJs();
    const fileBuffer = readEntireFileSync(dbPath);
    const db = new SQL.Database(fileBuffer);
    try {
        const result = db.exec("SELECT value FROM ItemTable WHERE key = 'cursorAuth/accessToken' LIMIT 1");
        if (!result.length || !result[0].values.length) {
            throw new Error("Token não encontrado. Confirme que você está logado no Cursor.");
        }
        return String(result[0].values[0][0]);
    }
    finally {
        db.close();
    }
}
//# sourceMappingURL=auth.js.map