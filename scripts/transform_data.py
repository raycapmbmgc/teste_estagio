import pandas as pd
import re
from pathlib import Path
import os

def extrair_e_consolidar():
    path_extracted = Path("data/extracted")
    all_data = []

    if not path_extracted.exists():
        print("❌ Pasta data/extracted não encontrada.")
        return

    for trimestre_dir in path_extracted.iterdir():
        if not trimestre_dir.is_dir():
            continue

        print(f"📂 Lendo pasta: {trimestre_dir.name}")

        match_info = re.search(r'(\d)T(\d{4})', trimestre_dir.name)
        tri_fallback = int(match_info.group(1)) if match_info else None
        ano_fallback = int(match_info.group(2)) if match_info else None

        for arquivo in trimestre_dir.iterdir():
            if not arquivo.name.lower().endswith(('.csv', '.txt')):
                continue

            print(f"  ↳ Processando: {arquivo.name}")

            try:
                chunks = pd.read_csv(
                    arquivo,
                    sep=';',
                    encoding='latin1',
                    chunksize=100_000,
                    dtype=str
                )
            except Exception as e:
                print(f"⚠️ Erro ao ler {arquivo.name}: {e}")
                continue

            for chunk in chunks:
                chunk.columns = [
                    c.strip().upper().replace('"', '')
                    for c in chunk.columns
                ]

                col_cnpj  = next((c for c in chunk.columns if 'CNPJ' in c or c == 'REG_ANS'), None)
                col_razao = next((c for c in chunk.columns if 'RAZAO' in c or 'NOME' in c or 'DESCRICAO' in c), None)
                col_data  = next((c for c in chunk.columns if 'DATA' in c or 'DT_REF' in c), None)
                col_conta = next((c for c in chunk.columns if 'CONTA' in c), None)
                col_valor = next((c for c in chunk.columns if c == 'VL_SALDO_FINAL'), None)

                if not col_cnpj or not col_valor:
                    continue

                if col_conta:
                    chunk = chunk[
                        chunk[col_conta].astype(str).str.startswith('4')
                    ].copy()

                chunk[col_valor] = (
                    chunk[col_valor]
                    .astype(str)
                    .str.replace(',', '.', regex=False)
                )
                chunk[col_valor] = pd.to_numeric(chunk[col_valor], errors='coerce')
                chunk = chunk[chunk[col_valor] > 0]

                if chunk.empty:
                    continue

                res = pd.DataFrame()

                res["CNPJ"] = (
                    chunk[col_cnpj]
                    .astype(str)
                    .str.replace(r"\D", "", regex=True)
                    .str.zfill(14)
                )

                if col_razao:
                    res["RAZAOSOCIAL"] = (
                        chunk[col_razao]
                        .astype(str)
                        .str.strip()
                        .str.upper()
                    )
                else:
                    res["RAZAOSOCIAL"] = "DESCONHECIDO"

                res["RAZAOSOCIAL"] = res["RAZAOSOCIAL"].replace(
                    {"NAN": "DESCONHECIDO", "NONE": "DESCONHECIDO"}
                )

                if col_data:
                    datas = pd.to_datetime(chunk[col_data], errors="coerce")
                    res["TRIMESTRE"] = datas.dt.quarter
                    res["ANO"] = datas.dt.year
                else:
                    res["TRIMESTRE"] = tri_fallback
                    res["ANO"] = ano_fallback

                res["VALORDESPESAS"] = chunk[col_valor]

                all_data.append(
                    res[["CNPJ", "RAZAOSOCIAL", "TRIMESTRE", "ANO", "VALORDESPESAS"]]
                )

    if not all_data:
        print("❌ Nenhum dado válido processado.")
        return

    print("🧠 Consolidando dados...")
    df_final = pd.concat(all_data, ignore_index=True)

    df_final = df_final.sort_values(["CNPJ", "RAZAOSOCIAL"])
    df_final["RAZAOSOCIAL"] = (
        df_final.groupby("CNPJ")["RAZAOSOCIAL"].transform("first")
    )

    df_final = (
        df_final
        .groupby(["CNPJ", "RAZAOSOCIAL", "TRIMESTRE", "ANO"], as_index=False)
        ["VALORDESPESAS"].sum()
    )

    df_final = df_final.dropna(subset=["TRIMESTRE", "ANO"])

    os.makedirs("data/processed", exist_ok=True)
    df_final.to_csv(
        "data/processed/consolidado_despesas.csv",
        index=False,
        sep=";",
        encoding="utf-8"
    )

    print(f"✅ Consolidado gerado com {len(df_final)} registros")

if __name__ == "__main__":
    extrair_e_consolidar()
