import sqlite3

# Caminho do seu banco
conn = sqlite3.connect("data/ans_database.db")
cursor = conn.cursor()

# Lista todas as tabelas do banco
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()
print("Tabelas:", tabelas)

# Lista todas as colunas da tabela 'despesas_consolidadas'
cursor.execute("PRAGMA table_info(despesas_consolidadas);")
colunas = cursor.fetchall()
print("Colunas da tabela despesas_consolidadas:")
for col in colunas:
    print(col)

# Opcional: ver os primeiros registros
cursor.execute("SELECT * FROM despesas_consolidadas LIMIT 5;")
print("Primeiros 5 registros:")
for linha in cursor.fetchall():
    print(linha)

conn.close()
