import tkinter as tk
from tkinter import messagebox
from database import Database
from styles import Estilos

class TelaLogin:
    def __init__(self):
        self.db = Database()
        self.janela = tk.Tk()
        self.janela.title("StockMaster - Login")
        self.janela.geometry("400x500")
        self.janela.resizable(False, False)
        self.janela.configure(bg=Estilos.COR_FUNDO)
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 400
        altura = 500
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        self.criar_widgets()
        self.janela.mainloop()
    
    def criar_widgets(self):
        # Frame branco principal com bordas arredondadas
        frame_conteudo = tk.Frame(
            self.janela,
            bg=Estilos.COR_FUNDO_CONTEUDO,
            bd=0,
            highlightthickness=0
        )
        frame_conteudo.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Logo
        logo = tk.Label(
            frame_conteudo,
            text="📦 STOCKMASTER",
            font=("Arial", 24, "bold"),
            fg=Estilos.COR_PRIMARIA,
            bg='white'
        )
        logo.pack(pady=(30, 10))
        
        subtitulo = tk.Label(
            frame_conteudo,
            text="Sistema de Gestão de Estoque",
            font=("Arial", 11),
            fg='#666666',
            bg='white'
        )
        subtitulo.pack(pady=(0, 30))
        
        # Frame para os campos
        frame_campos = tk.Frame(frame_conteudo, bg='white')
        frame_campos.pack(pady=10)
        
        # Usuário
        tk.Label(
            frame_campos,
            text="Usuário:",
            font=("Arial", 11, "bold"),
            fg='#333333',
            bg='white'
        ).pack(anchor='w', pady=(10, 5))
        
        self.usuario_entry = tk.Entry(
            frame_campos,
            font=("Arial", 11),
            width=25,
            relief='solid',
            bd=1,
            highlightbackground='#dddddd',
            highlightthickness=1
        )
        self.usuario_entry.pack(pady=(0, 15), ipady=8)
        self.usuario_entry.focus()
        
        # Senha
        tk.Label(
            frame_campos,
            text="Senha:",
            font=("Arial", 11, "bold"),
            fg='#333333',
            bg='white'
        ).pack(anchor='w', pady=(10, 5))
        
        self.senha_entry = tk.Entry(
            frame_campos,
            font=("Arial", 11),
            width=25,
            show="*",
            relief='solid',
            bd=1,
            highlightbackground='#dddddd',
            highlightthickness=1
        )
        self.senha_entry.pack(pady=(0, 20), ipady=8)
        
        # Botão Login arredondado
        frame_btn, btn_login = Estilos.criar_botao_arredondado(
            frame_campos,
            "ENTRAR",
            self.fazer_login,
            cor_fundo='white',
            cor_texto=Estilos.COR_PRIMARIA,
            largura=20,
            altura=1,
            icone="🔐"
        )
        frame_btn.pack(pady=15)
        
        # Link para recuperar senha
        link_recuperar = tk.Label(
            frame_campos,
            text="Esqueceu sua senha?",
            font=("Arial", 9),
            fg='#999999',
            bg='white',
            cursor='hand2'
        )
        link_recuperar.pack(pady=(10, 0))
        
        def on_enter_link(e):
            link_recuperar['fg'] = Estilos.COR_PRIMARIA
            link_recuperar['font'] = ("Arial", 9, "underline")
        
        def on_leave_link(e):
            link_recuperar['fg'] = '#999999'
            link_recuperar['font'] = ("Arial", 9)
        
        link_recuperar.bind('<Enter>', on_enter_link)
        link_recuperar.bind('<Leave>', on_leave_link)
        
        # Versão
        versao = tk.Label(
            frame_conteudo,
            text="v2.0.0",
            font=("Arial", 8),
            fg='#cccccc',
            bg='white'
        )
        versao.pack(side='bottom', pady=10)
        
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