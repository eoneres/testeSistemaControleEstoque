# login.py
import tkinter as tk
from tkinter import messagebox
from database import Database
from styles import Estilos

class TelaLogin:
    def __init__(self):
        self.db = Database()
        self.janela = tk.Tk()
        self.janela.title("StockMaster - Login")
        self.janela.geometry("400x550")
        self.janela.resizable(False, False)
        self.janela.configure(bg='#f5f5f5')  # Fundo cinza claro
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 400
        altura = 550
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        self.criar_interface()
        self.janela.mainloop()
    
    def criar_interface(self):
        # Card central branco (como na imagem)
        card = tk.Frame(
            self.janela,
            bg='white',
            highlightbackground=Estilos.COR_BORDA,
            highlightthickness=1,
            bd=0
        )
        card.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Logo
        tk.Label(
            card,
            text="📦",
            font=("Arial", 48),
            fg=Estilos.COR_PRIMARIA,
            bg='white'
        ).pack(pady=(30, 10))
        
        tk.Label(
            card,
            text="STOCKMASTER",
            font=("Arial", 20, "bold"),
            fg=Estilos.COR_PRIMARIA,
            bg='white'
        ).pack()
        
        tk.Label(
            card,
            text="Sistema de Gestão de Estoque",
            font=("Arial", 10),
            fg=Estilos.COR_TEXTO_SECUNDARIO,
            bg='white'
        ).pack(pady=(5, 30))
        
        # Frame para os campos
        frame_campos = tk.Frame(card, bg='white', padx=30)
        frame_campos.pack(fill='x')
        
        # Usuário
        tk.Label(
            frame_campos,
            text="Usuário",
            font=("Arial", 10, "bold"),
            fg=Estilos.COR_TEXTO,
            bg='white'
        ).pack(anchor='w')
        
        self.usuario_entry = Estilos.criar_campo_personalizado(
            frame_campos,
            "",  # Rótulo vazio porque já temos o label acima
            largura=30
        )
        self.usuario_entry.pack(fill='x', pady=(0, 15))
        self.usuario_entry.focus()
        
        # Senha
        tk.Label(
            frame_campos,
            text="Senha",
            font=("Arial", 10, "bold"),
            fg=Estilos.COR_TEXTO,
            bg='white'
        ).pack(anchor='w')
        
        self.senha_entry = Estilos.criar_campo_personalizado(
            frame_campos,
            "",
            largura=30,
            mostrar="*"
        )
        self.senha_entry.pack(fill='x', pady=(0, 25))
        
        # Botão de login
        btn_frame, btn_login = Estilos.criar_botao_moderno(
            frame_campos,
            "ENTRAR",
            self.fazer_login,
            tipo='primario',
            icone="🔐"
        )
        btn_frame.pack(pady=10)
        
        # Link para recuperar senha
        link_frame = tk.Frame(frame_campos, bg='white')
        link_frame.pack(pady=10)
        
        link_recuperar = tk.Label(
            link_frame,
            text="Esqueceu sua senha?",
            font=("Arial", 9),
            fg='#999999',
            bg='white',
            cursor='hand2'
        )
        link_recuperar.pack()
        
        def on_enter_link(e):
            link_recuperar['fg'] = Estilos.COR_PRIMARIA
            link_recuperar['font'] = ("Arial", 9, "underline")
        
        def on_leave_link(e):
            link_recuperar['fg'] = '#999999'
            link_recuperar['font'] = ("Arial", 9)
        
        link_recuperar.bind('<Enter>', on_enter_link)
        link_recuperar.bind('<Leave>', on_leave_link)
        
        # Versão
        tk.Label(
            card,
            text="v2.0.0",
            font=("Arial", 8),
            fg='#cccccc',
            bg='white'
        ).pack(side='bottom', pady=15)
        
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
            self.janela.destroy()
            from menu import TelaMenu
            TelaMenu()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
            self.senha_entry.delete(0, tk.END)
            self.senha_entry.focus()