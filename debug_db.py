import sqlite3
import pandas as pd

def debug_data():
    conn = sqlite3.connect("data/ans_database.db")
    
    print("🔍 --- VERIFICANDO TABELA DE DESPESAS ---")
    # 1. Ver as colunas reais
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(despesas_consolidadas)")
    cols = cursor.fetchall()
    print(f"\nColunas encontradas: {[c[1] for c in cols]}")

    # 2. Ver como o CNPJ está gravado (pegando os 5 primeiros)
    print("\nAmostra de dados (primeiras 5 linhas):")
    df_sample = pd.read_sql_query("SELECT * FROM despesas_consolidadas LIMIT 5", conn)
    print(df_sample)

    # 3. Teste de busca manual (substitua pelo CNPJ que você sabe que existe)
    # Vamos listar os CNPJs únicos para ver se há espaços ou pontos
    print("\nAlguns CNPJs únicos no banco (Top 10):")
    df_cnpjs = pd.read_sql_query("SELECT DISTINCT cnpj FROM despesas_consolidadas LIMIT 10", conn)
    print(df_cnpjs['cnpj'].tolist())

    conn.close()

if __name__ == "__main__":
    debug_data()