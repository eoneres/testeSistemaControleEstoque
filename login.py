import tkinter as tk
from tkinter import messagebox
from database import Database

class TelaLogin:
    def __init__(self):
        self.db = Database()
        self.janela = tk.Tk()
        self.janela.title("Sistema de Estoque - Login")
        self.janela.geometry("300x200")
        self.janela.resizable(False, False)
        
        # Centralizar (antes do mainloop)
        self.janela.update_idletasks()
        largura = 300
        altura = 200
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        # Trazer para frente (antes do mainloop)
        self.janela.lift()
        self.janela.focus_force()
        
        self.criar_widgets()
        
        # mainloop é a ÚLTIMA coisa no __init__
        self.janela.mainloop()
    
    def criar_widgets(self):
        # Frame principal
        frame = tk.Frame(self.janela, padx=20, pady=20)
        frame.pack(expand=True, fill='both')
        
        # Título
        titulo = tk.Label(frame, text="SISTEMA DE ESTOQUE", 
                          font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Usuário
        tk.Label(frame, text="Usuário:", font=("Arial", 10)).pack(anchor='w')
        self.usuario_entry = tk.Entry(frame, font=("Arial", 10), width=30)
        self.usuario_entry.pack(pady=5)
        
        # Senha
        tk.Label(frame, text="Senha:", font=("Arial", 10)).pack(anchor='w')
        self.senha_entry = tk.Entry(frame, font=("Arial", 10), width=30, show="*")
        self.senha_entry.pack(pady=5)
        
        # Botão Login
        btn_login = tk.Button(frame, text="ENTRAR", font=("Arial", 10, "bold"),
                             bg="#4CAF50", fg="white", padx=20, pady=5,
                             command=self.fazer_login)
        btn_login.pack(pady=15)
        
        # Vincular Enter
        self.janela.bind('<Return>', lambda event: self.fazer_login())
    
    def fazer_login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()
        
        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        resultado = self.db.verificar_login(usuario, senha)
        
        if resultado:
            messagebox.showinfo("Sucesso", f"Bem-vindo(a), {resultado[3]}!")
            self.janela.destroy()  # Isso fecha a janela de login
            
            # Importa e abre o menu
            from menu import TelaMenu
            TelaMenu()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
            # Limpa os campos
            self.usuario_entry.delete(0, tk.END)
            self.senha_entry.delete(0, tk.END)
            self.usuario_entry.focus()