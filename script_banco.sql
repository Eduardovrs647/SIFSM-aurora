-- Banco de dados do SIFSM - Aurora Siger
-- Compatível com SQLite 3.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS modulos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    ativo INTEGER NOT NULL CHECK (ativo IN (0, 1)),
    critico INTEGER NOT NULL DEFAULT 0 CHECK (critico IN (0, 1)),
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS sensores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    modulo_codigo TEXT NOT NULL,
    tipo TEXT NOT NULL,
    unidade TEXT NOT NULL,
    FOREIGN KEY (modulo_codigo) REFERENCES modulos(codigo)
);

CREATE TABLE IF NOT EXISTS telemetria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_codigo TEXT NOT NULL,
    ciclo INTEGER NOT NULL,
    valor REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'NORMAL',
    FOREIGN KEY (sensor_codigo) REFERENCES sensores(codigo)
);

CREATE TABLE IF NOT EXISTS alertas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ciclo INTEGER NOT NULL,
    modulo_codigo TEXT,
    mensagem TEXT NOT NULL,
    nivel TEXT NOT NULL CHECK (nivel IN ('INFO', 'ATENCAO', 'CRITICO')),
    resolvido INTEGER NOT NULL DEFAULT 0 CHECK (resolvido IN (0, 1)),
    FOREIGN KEY (modulo_codigo) REFERENCES modulos(codigo)
);

CREATE TABLE IF NOT EXISTS manutencoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modulo_codigo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    prioridade INTEGER NOT NULL DEFAULT 2,
    status TEXT NOT NULL DEFAULT 'PENDENTE',
    FOREIGN KEY (modulo_codigo) REFERENCES modulos(codigo)
);

CREATE INDEX IF NOT EXISTS idx_telemetria_sensor_ciclo
ON telemetria(sensor_codigo, ciclo);
CREATE INDEX IF NOT EXISTS idx_alertas_nivel
ON alertas(nivel);
