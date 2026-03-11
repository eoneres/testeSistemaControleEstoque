import traceback
import sys

print("="*60)
print("🔍 DIAGNÓSTICO RÁPIDO")
print("="*60)

# Teste 1: Importar database
print("\n1. Testando database.py...")
try:
    from database import Database
    print("   ✅ database importado")
    
    # Tenta instanciar
    db = Database()
    print("   ✅ Database instanciado")
    db.fechar_conexao()
    print("   ✅ Conexão fechada")
except Exception as e:
    print(f"   ❌ ERRO: {e}")
    traceback.print_exc()

# Teste 2: Importar models
print("\n2. Testando models.py...")
try:
    from models import Produto, Venda
    print("   ✅ models importado")
except Exception as e:
    print(f"   ❌ ERRO: {e}")
    traceback.print_exc()

# Teste 3: Importar login
print("\n3. Testando login.py...")
try:
    from login import TelaLogin
    print("   ✅ login importado")
except Exception as e:
    print(f"   ❌ ERRO: {e}")
    traceback.print_exc()

# Teste 4: Tentar criar instância da TelaLogin SEM o mainloop
print("\n4. Testando criação da TelaLogin (sem mainloop)...")
try:
    # Criar uma versão mock do Tkinter para teste
    import tkinter as tk
    
    # Salvar o mainloop original
    original_mainloop = tk.Tk.mainloop
    
    # Substituir por uma versão que não trava
    def mock_mainloop(self):
        print("   ⏰ mock_mainloop chamado - não vai travar")
        self.quit()
    
    tk.Tk.mainloop = mock_mainloop
    
    # Tentar criar a tela de login
    app = TelaLogin()
    print("   ✅ TelaLogin instanciada")
    
    # Restaurar mainloop
    tk.Tk.mainloop = original_mainloop
    
except Exception as e:
    print(f"   ❌ ERRO: {e}")
    traceback.print_exc()
    # Restaurar mainloop
    tk.Tk.mainloop = original_mainloop

print("\n" + "="*60)
print("🏁 DIAGNÓSTICO CONCLUÍDO")
print("="*60)