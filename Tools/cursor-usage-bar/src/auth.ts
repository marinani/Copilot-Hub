import * as fs from "fs";
import * as os from "os";
import * as path from "path";

/** Caminho do state.vscdb do Cursor no SO atual. */
export function getStateDbPath(): string {
  if (process.platform === "darwin") {
    return path.join(
      os.homedir(),
      "Library",
      "Application Support",
      "Cursor",
      "User",
      "globalStorage",
      "state.vscdb"
    );
  }
  if (process.platform === "win32") {
    return path.join(
      process.env.APPDATA || path.join(os.homedir(), "AppData", "Roaming"),
      "Cursor",
      "User",
      "globalStorage",
      "state.vscdb"
    );
  }
  return path.join(
    os.homedir(),
    ".config",
    "Cursor",
    "User",
    "globalStorage",
    "state.vscdb"
  );
}

function readEntireFileSync(filePath: string): Buffer {
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
  } finally {
    fs.closeSync(fd);
  }
  return buf;
}

/**
 * Lê o access token da sessão Cursor já logada.
 * Nunca pede senha — só leitura do banco local.
 */
export async function getAccessToken(): Promise<string> {
  const dbPath = getStateDbPath();

  if (!fs.existsSync(dbPath)) {
    throw new Error(
      "Banco state.vscdb não encontrado. Faça login no Cursor e tente de novo."
    );
  }

  // eslint-disable-next-line @typescript-eslint/no-require-imports
  const initSqlJs = require("sql.js");
  const SQL = await initSqlJs();
  const fileBuffer = readEntireFileSync(dbPath);
  const db = new SQL.Database(fileBuffer);

  try {
    const result = db.exec(
      "SELECT value FROM ItemTable WHERE key = 'cursorAuth/accessToken' LIMIT 1"
    );
    if (!result.length || !result[0].values.length) {
      throw new Error(
        "Token não encontrado. Confirme que você está logado no Cursor."
      );
    }
    return String(result[0].values[0][0]);
  } finally {
    db.close();
  }
}
