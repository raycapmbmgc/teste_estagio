import pandas as pd
import os
from pandas.errors import EmptyDataError

# =========================
# Validação de CNPJ
# =========================
def validar_cnpj(cnpj: str) -> bool:
    cnpj = ''.join(filter(str.isdigit, str(cnpj)))

    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    def calc_digito(cnpj, pesos):
        soma = sum(int(d) * p for d, p in zip(cnpj, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    d1 = calc_digito(cnpj[:12], [5,4,3,2,9,8,7,6,5,4,3,2])
    d2 = calc_digito(cnpj[:13], [6,5,4,3,2,9,8,7,6,5,4,3,2])

    return cnpj[-2:] == d1 + d2


def enriquecer_e_agregar():
    path_consolidado = "data/processed/consolidado_despesas.csv"
    path_cadastral = "data/raw/operadoras_ativas.csv"
    output_final = "data/processed/despesas_agregadas.csv"

    if not os.path.exists(path_consolidado):
        print("❌ consolidado_despesas.csv não encontrado.")
        return

    print("📥 Carregando despesas consolidadas...")

    # 🔧 CORREÇÃO PRINCIPAL: sep=";"
    df = pd.read_csv(
        path_consolidado,
        sep=";",
        dtype=str
    )

    df.columns = [c.upper().strip() for c in df.columns]

    # =========================
    # 2.1 – Validações
    # =========================
    print("🔍 Validando dados...")

    # CNPJ
    df["CNPJ"] = df["CNPJ"].str.replace(r"\D", "", regex=True).str.zfill(14)
    df["CNPJ_VALIDO"] = df["CNPJ"].apply(validar_cnpj)

    # Estratégia:
    # ➜ manter CNPJs inválidos (marcados), não descartar
    df["VALORDESPESAS"] = pd.to_numeric(df["VALORDESPESAS"], errors="coerce")
    df = df[df["VALORDESPESAS"] > 0]

    # Razão Social obrigatória
    df["RAZAOSOCIAL"] = df["RAZAOSOCIAL"].fillna("NOME NAO ENCONTRADO")

    # =========================
    # 2.2 – Enriquecimento
    # =========================
    enriquecido = False

    if os.path.exists(path_cadastral):
        try:
            df_cad = pd.read_csv(
                path_cadastral,
                sep=";",
                encoding="latin1",
                dtype=str
            )

            df_cad.columns = [c.upper().strip() for c in df_cad.columns]

            df_cad["CNPJ"] = (
                df_cad["CNPJ"]
                .str.replace(r"\D", "", regex=True)
                .str.zfill(14)
            )

            # Estratégia:
            # ➜ manter primeiro registro em caso de duplicidade
            df_cad = df_cad.drop_duplicates(subset=["CNPJ"], keep="first")

            col_reg = next(c for c in df_cad.columns if "REG" in c)
            col_mod = next(c for c in df_cad.columns if "MODAL" in c)
            col_uf  = "UF"

            df = df.merge(
                df_cad[["CNPJ", col_reg, col_mod, col_uf]],
                on="CNPJ",
                how="left"
            )

            df = df.rename(columns={
                col_reg: "REGISTROANS",
                col_mod: "MODALIDADE",
                col_uf: "UF"
            })

            enriquecido = True

        except EmptyDataError:
            print("⚠️ Cadastro de operadoras vazio. Enriquecimento ignorado.")

    # Fallback (pipeline nunca quebra)
    if not enriquecido:
        df["REGISTROANS"] = "NAO_ENCONTRADO"
        df["MODALIDADE"] = "NAO_ENCONTRADO"
        df["UF"] = "NA"

    # =========================
    # 2.3 – Agregação
    # =========================
    print("📊 Agregando dados...")

    df_agregado = (
        df
        .groupby(["RAZAOSOCIAL", "UF"], dropna=False)
        .agg(
            TotalDespesas=("VALORDESPESAS", "sum"),
            MediaDespesas=("VALORDESPESAS", "mean"),
            DesvioPadrao=("VALORDESPESAS", "std")
        )
        .reset_index()
    )

    df_agregado["DesvioPadrao"] = df_agregado["DesvioPadrao"].fillna(0)
    df_agregado = df_agregado.sort_values("TotalDespesas", ascending=False)

    os.makedirs("data/processed", exist_ok=True)
    df_agregado.to_csv(output_final, index=False, encoding="utf-8")

    print(f"✅ despesas_agregadas.csv gerado com {len(df_agregado)} linhas.")


if __name__ == "__main__":
    enriquecer_e_agregar()
