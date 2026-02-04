-- =====================================================
-- QUERY 1
-- 5 operadoras com maior crescimento percentual
-- entre o primeiro e o último trimestre analisado
--
-- Estratégia:
-- - Window Functions
-- - Ignora operadoras sem dados suficientes
-- - Evita divisão por zero
-- =====================================================

WITH base AS (
    SELECT
        cnpj,
        razao_social,
        ano,
        trimestre,
        SUM(valor_despesas) AS total_despesas
    FROM despesas_consolidadas
    GROUP BY cnpj, razao_social, ano, trimestre
),
valores_extremos AS (
    SELECT
        cnpj,
        razao_social,
        FIRST_VALUE(total_despesas) OVER (
            PARTITION BY cnpj
            ORDER BY ano, trimestre
        ) AS primeiro_valor,
        LAST_VALUE(total_despesas) OVER (
            PARTITION BY cnpj
            ORDER BY ano, trimestre
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS ultimo_valor
    FROM base
)
SELECT DISTINCT
    razao_social,
    ROUND(
        ((ultimo_valor - primeiro_valor) / NULLIF(primeiro_valor, 0)) * 100,
        2
    ) AS crescimento_percentual
FROM valores_extremos
WHERE primeiro_valor IS NOT NULL
  AND ultimo_valor IS NOT NULL
ORDER BY crescimento_percentual DESC
LIMIT 5;


-- =====================================================
-- QUERY 2
-- Distribuição de despesas por UF
-- + média de despesas por operadora em cada UF
--
-- Estratégia:
-- - Usa tabela agregada (menos custo)
-- =====================================================

SELECT
    uf,
    SUM(total_despesas) AS total_despesas_uf,
    AVG(total_despesas) AS media_por_operadora
FROM despesas_agregadas
GROUP BY uf
ORDER BY total_despesas_uf DESC
LIMIT 5;


-- =====================================================
-- QUERY 3
-- Quantas operadoras tiveram despesas acima da média
-- geral em pelo menos 2 dos 3 trimestres
--
-- Estratégia:
-- - CTE para média geral
-- - Contagem por CNPJ
-- - Foco em legibilidade e performance
-- =====================================================

WITH media_geral AS (
    SELECT AVG(valor_despesas) AS media
    FROM despesas_consolidadas
),
acima_da_media AS (
    SELECT
        cnpj,
        COUNT(*) AS qtd_trimestres
    FROM despesas_consolidadas d
    CROSS JOIN media_geral m
    WHERE d.valor_despesas > m.media
    GROUP BY cnpj
)
SELECT
    COUNT(*) AS total_operadoras
FROM acima_da_media
WHERE qtd_trimestres >= 2;
