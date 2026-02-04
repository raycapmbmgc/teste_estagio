-- ===============================
-- Importar Operadoras
-- ===============================
COPY operadoras (cnpj, registro_ans, razao_social, modalidade, uf)
FROM '/data/operadoras_ativas.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

-- ===============================
-- Importar Despesas Consolidadas
-- ===============================
COPY despesas_consolidadas (
    cnpj,
    razao_social,
    trimestre,
    ano,
    valor_despesas,
    cnpj_valido
)
FROM '/data/consolidado_despesas.csv'
DELIMITER ','
CSV HEADER
ENCODING 'UTF8';

-- ===============================
-- Importar Despesas Agregadas
-- ===============================
COPY despesas_agregadas (
    razao_social,
    uf,
    total_despesas,
    media_despesas,
    desvio_padrao
)
FROM '/data/despesas_agregadas.csv'
DELIMITER ','
CSV HEADER
ENCODING 'UTF8';
