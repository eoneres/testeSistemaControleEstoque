# styles.py - Estilos compartilhados para todo o sistema
import tkinter as tk
from tkinter import ttk

class Estilos:
    # Cores padrão
    COR_PRIMARIA = '#ff751f'
    COR_BOTAO = '#ffffff'
    COR_TEXTO_BOTAO = '#ff751f'
    COR_SOMBRA = '#e65c00'
    COR_FUNDO = '#ff751f'
    COR_FUNDO_CONTEUDO = '#ffffff'
    
    @staticmethod
    def criar_botao_arredondado(parent, texto, comando, cor_fundo='#ffffff', cor_texto='#ff751f', 
                                largura=20, altura=2, icone=""):
        """Cria um botão com cantos arredondados e sombra no hover"""
        
        frame_btn = tk.Frame(parent, bg=parent['bg'], highlightthickness=0)
        
        btn_texto = f"{icone} {texto}" if icone else texto
        
        btn = tk.Button(
            frame_btn,
            text=btn_texto,
            font=("Arial", 11, "bold"),
            bg=cor_fundo,
            fg=cor_texto,
            bd=2,
            relief='solid',
            padx=20,
            pady=10,
            cursor='hand2',
            command=comando,
            width=largura,
            height=altura,
            highlightbackground='#dddddd',
            highlightthickness=1,
            activebackground='#f0f0f0',
            activeforeground=cor_texto
        )
        btn.pack()
        
        def on_enter(e):
            btn.config(
                relief='raised',
                bd=3,
                bg='#f5f5f5',
                fg=Estilos.COR_SOMBRA
            )
        
        def on_leave(e):
            btn.config(
                relief='solid',
                bd=2,
                bg=cor_fundo,
                fg=cor_texto
            )
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return frame_btn, btn
    
    @staticmethod
    def criar_card_cabecalho(parent, texto, valor, unidade, cor, largura=280, altura=130):
        """Cria um card estilizado para cabeçalho com tamanho adequado"""
        card = tk.Frame(
            parent,
            bg='white',
            highlightbackground='#e0e0e0',
            highlightthickness=1,
            bd=0,
            width=largura,
            height=altura
        )
        card.pack_propagate(False)
        
        def on_enter(e):
            card.config(highlightbackground=Estilos.COR_PRIMARIA, highlightthickness=2)
        
        def on_leave(e):
            card.config(highlightbackground='#e0e0e0', highlightthickness=1)
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
        
        conteudo = tk.Frame(card, bg='white', padx=15, pady=10)
        conteudo.pack(fill='both', expand=True)
        
        # Título
        lbl_titulo = tk.Label(
            conteudo,
            text=texto,
            font=("Arial", 11, "bold"),
            fg='#666666',
            bg='white',
            anchor='w'
        )
        lbl_titulo.pack(anchor='w', fill='x')
        
        # Valor principal
        lbl_valor = tk.Label(
            conteudo,
            text=str(valor),
            font=("Arial", 26, "bold"),
            fg=cor,
            bg='white',
            anchor='w'
        )
        lbl_valor.pack(anchor='w', pady=(5, 2))
        
        # Unidade
        lbl_unidade = tk.Label(
            conteudo,
            text=unidade,
            font=("Arial", 10),
            fg='#999999',
            bg='white',
            anchor='w'
        )
        lbl_unidade.pack(anchor='w')
        
        return card
    
    @staticmethod
    def aplicar_estilo_tabela(treeview):
        """Aplica estilo personalizado à treeview"""
        style = ttk.Style()
        style.theme_use('default')
        
        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#333333",
                        rowheight=30,
                        fieldbackground="#ffffff",
                        font=('Arial', 10))
        
        style.configure("Treeview.Heading",
                        background="#f0f0f0",
                        foreground="#333333",
                        font=('Arial', 10, 'bold'))
        
        style.map('Treeview',
                  background=[('selected', Estilos.COR_PRIMARIA)],
                  foreground=[('selected', 'white')])
        
        return treeview
    
    @staticmethod
    def aplicar_estilo_notebook(notebook):
        """Aplica estilo personalizado ao notebook"""
        style = ttk.Style()
        style.theme_use('default')
        
        style.configure('TNotebook', 
                        background=Estilos.COR_FUNDO_CONTEUDO, 
                        borderwidth=0)
        
        style.configure('TNotebook.Tab', 
                        background='#f0f0f0',
                        foreground='#333333',
                        padding=[15, 8],
                        font=('Arial', 10),
                        borderwidth=1,
                        relief='solid')
        
        style.map('TNotebook.Tab',
                  background=[('selected', Estilos.COR_PRIMARIA)],
                  foreground=[('selected', 'white')])
        
        return notebook
    
    @staticmethod
    def criar_entry_estilizado(parent, largura=30, mostrar=None):
        """Cria um campo de entrada estilizado"""
        entry = tk.Entry(
            parent,
            font=("Arial", 10),
            width=largura,
            relief='solid',
            bd=1,
            highlightbackground='#dddddd',
            highlightthickness=1,
            show=mostrar
        )
        
        def on_focus_in(e):
            entry.config(highlightbackground=Estilos.COR_PRIMARIA, highlightthickness=2)
        
        def on_focus_out(e):
            entry.config(highlightbackground='#dddddd', highlightthickness=1)
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry