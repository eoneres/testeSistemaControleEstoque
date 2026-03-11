
import sqlite3
from datetime import datetime

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

print("🔧 ATUALIZANDO BANCO DE DADOS...")
print("-" * 50)


cursor.execute("PRAGMA table_info(vendas)")
colunas = cursor.fetchall()
print("Colunas atuais na tabela vendas:")
for col in colunas:
    print(f"  - {col[1]}")


cursor.execute("PRAGMA table_info(vendas)")
colunas_existentes = [col[1] for col in cursor.fetchall()]

if 'codigo_venda' not in colunas_existentes:
    print("\n📦 Adicionando coluna 'codigo_venda'...")
    cursor.execute('''
        ALTER TABLE vendas ADD COLUMN codigo_venda TEXT
    ''')
    print("✅ Coluna 'codigo_venda' adicionada!")
else:
    print("\n✅ Coluna 'codigo_venda' já existe.")


if 'cliente_codigo' not in colunas_existentes:
    print("\n📦 Adicionando coluna 'cliente_codigo'...")
    cursor.execute('''
        ALTER TABLE vendas ADD COLUMN cliente_codigo TEXT
    ''')
    print("✅ Coluna 'cliente_codigo' adicionada!")
else:
    print("✅ Coluna 'cliente_codigo' já existe.")


if 'pontos_ganhos' not in colunas_existentes:
    print("\n📦 Adicionando coluna 'pontos_ganhos'...")
    cursor.execute('''
        ALTER TABLE vendas ADD COLUMN pontos_ganhos INTEGER DEFAULT 0
    ''')
    print("✅ Coluna 'pontos_ganhos' adicionada!")
else:
    print("✅ Coluna 'pontos_ganhos' já existe.")

conn.commit()
print("\n" + "-" * 50)
print("✅ BANCO DE DADOS ATUALIZADO COM SUCESSO!")
conn.close()