# styles.py - Estilos compartilhados para todo o sistema (versão unificada)
import tkinter as tk
from tkinter import ttk

class Estilos:
    # Cores base
    COR_PRIMARIA = '#ff751f'      # Laranja (destaque)
    COR_SECUNDARIA = '#f5f5f5'     # Cinza muito claro (fundo de cards)
    COR_FUNDO = '#ffffff'           # Branco
    COR_TEXTO = '#333333'           # Cinza escuro para texto
    COR_TEXTO_SECUNDARIO = '#666666' # Cinza médio
    COR_BORDA = '#e0e0e0'           # Cinza claro para bordas
    COR_SUCESSO = '#28a745'         # Verde
    COR_PERIGO = '#dc3545'          # Vermelho
    COR_ALERTA = '#ffc107'          # Amarelo
    
    @staticmethod
    def criar_card_moderno(parent, titulo, valor, subtitulo, icone, largura=280, altura=120):
        """Cria um card no estilo moderno (como na imagem)"""
        card = tk.Frame(
            parent,
            bg='white',
            highlightbackground=Estilos.COR_BORDA,
            highlightthickness=1,
            bd=0,
            width=largura,
            height=altura
        )
        card.pack_propagate(False)
        
        # Efeito hover sutil
        def on_enter(e):
            card.config(highlightbackground=Estilos.COR_PRIMARIA, highlightthickness=2)
        
        def on_leave(e):
            card.config(highlightbackground=Estilos.COR_BORDA, highlightthickness=1)
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
        
        # Layout do card (informações à esquerda, ícone à direita)
        frame_info = tk.Frame(card, bg='white', padx=15, pady=10)
        frame_info.pack(side='left', fill='both', expand=True)
        
        # Título
        lbl_titulo = tk.Label(
            frame_info,
            text=titulo,
            font=("Arial", 10),
            fg=Estilos.COR_TEXTO_SECUNDARIO,
            bg='white'
        )
        lbl_titulo.pack(anchor='w')
        
        # Valor (fonte 20) - GUARDAR REFERÊNCIA
        lbl_valor = tk.Label(
            frame_info,
            text=str(valor),
            font=("Arial", 20, "bold"),
            fg=Estilos.COR_PRIMARIA,
            bg='white'
        )
        lbl_valor.pack(anchor='w')
        
        # Subtítulo (fonte 9) - GUARDAR REFERÊNCIA
        lbl_subtitulo = tk.Label(
            frame_info,
            text=subtitulo,
            font=("Arial", 9),
            fg='#999999',
            bg='white'
        )
        lbl_subtitulo.pack(anchor='w')
        
        # Ícone à direita
        frame_icone = tk.Frame(card, bg='white', width=50)
        frame_icone.pack(side='right', fill='y', padx=(0, 15))
        
        lbl_icone = tk.Label(
            frame_icone,
            text=icone,
            font=("Arial", 28),
            fg=Estilos.COR_PRIMARIA,
            bg='white'
        )
        lbl_icone.pack(expand=True)
        
        # Guardar referências aos labels para facilitar atualização
        card.lbl_valor = lbl_valor
        card.lbl_subtitulo = lbl_subtitulo
        
        return card
    
    @staticmethod
    def criar_botao_moderno(parent, texto, comando, tipo='primario', icone=""):
        """Cria botões no estilo moderno"""
        frame_btn = tk.Frame(parent, bg=parent['bg'] if parent else '#f5f5f5')
        
        cores = {
            'primario': {'bg': Estilos.COR_PRIMARIA, 'fg': 'white', 'hover': '#e65c00'},
            'secundario': {'bg': 'white', 'fg': Estilos.COR_PRIMARIA, 'hover': '#f5f5f5'},
            'perigo': {'bg': Estilos.COR_PERIGO, 'fg': 'white', 'hover': '#c82333'},
            'sucesso': {'bg': Estilos.COR_SUCESSO, 'fg': 'white', 'hover': '#218838'}
        }
        
        cor = cores.get(tipo, cores['primario'])
        
        btn_texto = f"{icone} {texto}" if icone else texto
        
        btn = tk.Button(
            frame_btn,
            text=btn_texto,
            font=("Arial", 11, "bold"),
            bg=cor['bg'],
            fg=cor['fg'],
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=comando,
            relief='flat'
        )
        btn.pack()
        
        def on_enter(e):
            btn.config(bg=cor['hover'])
        
        def on_leave(e):
            btn.config(bg=cor['bg'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return frame_btn, btn
    
    @staticmethod
    def criar_campo_personalizado(parent, rotulo, largura=30, mostrar=None):
        """Cria campo de entrada com rótulo"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='x', pady=8)
        
        tk.Label(
            frame,
            text=rotulo,
            font=("Arial", 10),
            fg=Estilos.COR_TEXTO_SECUNDARIO,
            bg='white'
        ).pack(anchor='w')
        
        entry = tk.Entry(
            frame,
            font=("Arial", 11),
            width=largura,
            relief='solid',
            bd=1,
            highlightbackground=Estilos.COR_BORDA,
            highlightthickness=1,
            bg='white',
            show=mostrar
        )
        entry.pack(fill='x', pady=(2, 0), ipady=6)
        
        def on_focus_in(e):
            entry.config(highlightbackground=Estilos.COR_PRIMARIA, highlightthickness=2)
        
        def on_focus_out(e):
            entry.config(highlightbackground=Estilos.COR_BORDA, highlightthickness=1)
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry
    
    @staticmethod
    def criar_secao(parent, titulo):
        """Cria uma seção com título"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='x', pady=10)
        
        tk.Label(
            frame,
            text=titulo,
            font=("Arial", 14, "bold"),
            fg=Estilos.COR_TEXTO,
            bg='white'
        ).pack(anchor='w')
        
        tk.Frame(
            frame,
            height=1,
            bg=Estilos.COR_BORDA
        ).pack(fill='x', pady=(5, 10))
        
        return frame
    
    @staticmethod
    def aplicar_estilo_tabela(treeview):
        """Aplica estilo personalizado à treeview"""
        style = ttk.Style()
        style.theme_use('default')
        
        style.configure("Treeview",
                        background="#ffffff",
                        foreground=Estilos.COR_TEXTO,
                        rowheight=30,
                        fieldbackground="#ffffff",
                        font=('Arial', 10))
        
        style.configure("Treeview.Heading",
                        background=Estilos.COR_SECUNDARIA,
                        foreground=Estilos.COR_TEXTO,
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
                        background='#f5f5f5', 
                        borderwidth=0)
        
        style.configure('TNotebook.Tab', 
                        background='#f0f0f0',
                        foreground=Estilos.COR_TEXTO,
                        padding=[15, 8],
                        font=('Arial', 10),
                        borderwidth=1,
                        relief='solid')
        
        style.map('TNotebook.Tab',
                  background=[('selected', Estilos.COR_PRIMARIA)],
                  foreground=[('selected', 'white')])
        
        return notebook