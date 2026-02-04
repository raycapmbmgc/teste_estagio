import pandas as pd
from database import get_connection

def query_db(query, params=()):
    conn = get_connection()
    try:
        # Usamos o pandas para ler o SQL; ele retorna um DataFrame
        df = pd.read_sql_query(query, conn, params=params)
        return df
    finally:
        conn.close()

def get_operadoras(page: int, limit: int, search: str | None = None):
    offset = (page - 1) * limit
    
    # Base da Query - Note que os nomes das colunas devem bater com seu CREATE TABLE
    if search:
        search_term = f"%{search}%"
        sql = """
            SELECT cnpj, razao_social, uf
            FROM operadoras
            WHERE razao_social LIKE ? OR cnpj LIKE ?
            LIMIT ? OFFSET ?
        """
        params = (search_term, search_term, limit, offset)
        count_sql = "SELECT COUNT(*) FROM operadoras WHERE razao_social LIKE ? OR cnpj LIKE ?"
        count_params = (search_term, search_term)
    else:
        sql = "SELECT cnpj, razao_social, uf FROM operadoras LIMIT ? OFFSET ?"
        params = (limit, offset)
        count_sql = "SELECT COUNT(*) FROM operadoras"
        count_params = ()

    data = query_db(sql, params)
    total_df = query_db(count_sql, count_params)
    
    # Extrai o valor do count de forma segura
    total = int(total_df.iloc[0, 0]) if not total_df.empty else 0
    
    return data.to_dict(orient="records"), total


def get_operadora(cnpj: str):
    sql = "SELECT * FROM operadoras WHERE cnpj = ?"
    df = query_db(sql, (cnpj,))
    if df.empty:
        return None
    return df.to_dict(orient="records")[0]

def get_historico_despesas(cnpj: str):
    # Remove qualquer máscara do CNPJ (pontos, traços)
    cnpj_limpo = ''.join(filter(str.isdigit, str(cnpj)))
    
    sql = """
        SELECT 
            d.ano, 
            d.trimestre, 
            SUM(d.valordespesas) as valor_despesas 
        FROM despesas_consolidadas d
        JOIN operadoras o ON TRIM(CAST(d.cnpj AS TEXT)) = TRIM(CAST(o.registro_operadora AS TEXT))
        WHERE REPLACE(REPLACE(o.cnpj, '.', ''), '-', '') = ?
        GROUP BY d.ano, d.trimestre
        ORDER BY d.ano DESC, d.trimestre DESC
    """
    
    df = query_db(sql, (cnpj_limpo,))
    return df.to_dict(orient="records")
def get_estatisticas():
    df = query_db("""
        SELECT
            SUM(totaldespesas) AS total_despesas,
            AVG(totaldespesas) AS media_despesas
        FROM despesas_agregadas
    """)

    totais = df.iloc[0].to_dict()

    top_5 = query_db("""
        SELECT
            RAZAOSOCIAL AS razao_social,
            TotalDespesas AS total_despesas
        FROM despesas_agregadas
        ORDER BY TotalDespesas DESC
        LIMIT 5
    """).to_dict(orient="records")

    return {
        "total_despesas": totais["total_despesas"],
        "media_despesas": totais["media_despesas"],
        "top_5_operadoras": top_5
    }
