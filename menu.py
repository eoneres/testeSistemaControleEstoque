import tkinter as tk
from tkinter import messagebox
from database import Database

class TelaMenu:
    def __init__(self):
        self.db = Database()
        self.janela = tk.Tk()
        self.janela.title("Sistema de Estoque - Menu Principal")
        self.janela.geometry("450x400")  # Aumentei um pouco para caber mais botões
        self.janela.resizable(False, False)
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 450
        altura = 400
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        self.criar_menu()
        self.janela.mainloop()
    
    def criar_menu(self):
        # Frame principal
        frame = tk.Frame(self.janela, padx=20, pady=20)
        frame.pack(expand=True, fill='both')
        
        # Título
        titulo = tk.Label(frame, text="MENU PRINCIPAL", 
                          font=("Arial", 16, "bold"), fg="#333")
        titulo.pack(pady=20)
        
        
        botoes = [
            ("📦 CADASTRAR PRODUTO", self.abrir_cadastro),
            ("🔍 CONSULTAR ESTOQUE", self.abrir_consulta),
            ("💰 REGISTRAR VENDA", self.abrir_venda),
            ("👥 GERENCIAR CLIENTES", self.abrir_clientes),  # ← NOVO BOTÃO
            ("📊 RELATÓRIOS", self.abrir_relatorios),
            ("🚪 SAIR", self.sair)
        ]
        
        for texto, comando in botoes:
            btn = tk.Button(frame, text=texto, font=("Arial", 11),
                          bg="#2196F3" if texto != "🚪 SAIR" else "#f44336",
                          fg="white", padx=20, pady=8, width=25,
                          command=comando)
            btn.pack(pady=5)
    
    def abrir_cadastro(self):
        from cadastro_produto import TelaCadastro
        self.janela.withdraw()
        TelaCadastro(self.janela)
    
    def abrir_consulta(self):
        from consulta_estoque import TelaConsulta
        self.janela.withdraw()
        TelaConsulta(self.janela)
    
    def abrir_venda(self):
        from registrar_venda import TelaVenda
        self.janela.withdraw()
        TelaVenda(self.janela)
    
    def abrir_clientes(self):  # ← NOVO MÉTODO
        from clientes import TelaClientes
        self.janela.withdraw()
        TelaClientes(self.janela)
    
    def abrir_relatorios(self):
        from relatorios import TelaRelatorios
        self.janela.withdraw()
        TelaRelatorios(self.janela)
    
    def sair(self):
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            self.db.fechar_conexao()
            self.janela.quit()