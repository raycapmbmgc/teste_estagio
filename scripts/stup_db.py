import sqlite3
import pandas as pd
import os

def setup_database():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/ans_database.db")

    def fix_columns(df):
        # Transforma tudo em minusculo e remove espaços/pontos
        df.columns = [c.strip().lower().replace(" ", "_").replace(".", "") for c in df.columns]
        return df

    # --- TABELA 1: Despesas Consolidadas ---
    df1 = pd.read_csv("data/processed/consolidado_despesas.csv", sep=";", encoding="latin1")
    fix_columns(df1).to_sql("despesas_consolidadas", conn, if_exists="replace", index=False)

    # --- TABELA 2: Despesas Agregadas ---
    # Adicionando o sep=";" que faltava aqui também!
    df2 = pd.read_csv("data/processed/despesas_agregadas.csv", sep=";", encoding="latin1")
    fix_columns(df2).to_sql("despesas_agregadas", conn, if_exists="replace", index=False)

    # --- TABELA 3: Operadoras ---
    try:
        df3 = pd.read_csv("data/raw/operadoras_ativas.csv", sep=";", encoding="latin1")
        fix_columns(df3).to_sql("operadoras", conn, if_exists="replace", index=False)
    except FileNotFoundError:
        print("Aviso: Arquivo de operadoras nao encontrado.")

    conn.close()
    print("Banco atualizado com sucesso e colunas normalizadas!")

if __name__ == "__main__":
    setup_database()