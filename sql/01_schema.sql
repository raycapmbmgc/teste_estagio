-- ===============================
-- Tabela de Operadoras (Cadastro)
-- ===============================
CREATE TABLE operadoras (
    cnpj VARCHAR(14) PRIMARY KEY,
    registro_ans VARCHAR(20),
    razao_social TEXT NOT NULL,
    modalidade TEXT,
    uf CHAR(2)
);

CREATE INDEX idx_operadoras_uf ON operadoras(uf);

-- ===================================
-- Tabela de Despesas Consolidadas
-- ===================================
CREATE TABLE despesas_consolidadas (
    id SERIAL PRIMARY KEY,
    cnpj VARCHAR(14),
    razao_social TEXT,
    ano INTEGER,
    trimestre INTEGER,
    valor_despesas DECIMAL(18,2) NOT NULL,
    cnpj_valido BOOLEAN,
    FOREIGN KEY (cnpj) REFERENCES operadoras(cnpj)
);

CREATE INDEX idx_despesas_cnpj ON despesas_consolidadas(cnpj);
CREATE INDEX idx_despesas_periodo ON despesas_consolidadas(ano, trimestre);

-- ===================================
-- Tabela de Despesas Agregadas
-- ===================================
CREATE TABLE despesas_agregadas (
    id SERIAL PRIMARY KEY,
    razao_social TEXT,
    uf CHAR(2),
    total_despesas DECIMAL(18,2),
    media_despesas DECIMAL(18,2),
    desvio_padrao DECIMAL(18,2)
);

CREATE INDEX idx_agregado_uf ON despesas_agregadas(uf);
CREATE INDEX idx_agregado_total ON despesas_agregadas(total_despesas);
