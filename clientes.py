import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from datetime import datetime

class TelaClientes:
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.db = Database()
        self.janela = tk.Toplevel()
        self.janela.title("StockMaster - Gerenciar Clientes")
        self.janela.geometry("1100x700")
        self.janela.resizable(False, False)
        self.janela.configure(bg='#f5f5f5')  # Fundo cinza claro
        
        # Cores
        self.cor_primaria = '#ff751f'
        self.cor_botao = '#ffffff'
        self.cor_texto_botao = '#ff751f'
        self.cor_sombra = '#e65c00'
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 1100
        altura = 700
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        self.entries = {}
        self.cliente_atual = None
        
        self.criar_interface()
        self.carregar_clientes()
        self.carregar_blacklist()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)
        self.janela.mainloop()
    
    def criar_interface(self):
        # Frame branco principal (card)
        frame_conteudo = tk.Frame(
            self.janela,
            bg='white',
            highlightbackground='#e0e0e0',
            highlightthickness=1,
            bd=0
        )
        frame_conteudo.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Cabeçalho
        frame_cabecalho = tk.Frame(frame_conteudo, bg='white', height=60)
        frame_cabecalho.pack(fill='x', padx=20, pady=(10, 5))
        frame_cabecalho.pack_propagate(False)
        
        tk.Label(
            frame_cabecalho,
            text="👥 GERENCIAR CLIENTES",
            font=("Arial", 22, "bold"),
            fg=self.cor_primaria,
            bg='white'
        ).pack(side='left', padx=10)
        
        # Data atual
        data_atual = datetime.now().strftime("%d/%m/%Y")
        tk.Label(
            frame_cabecalho,
            text=f"📅 {data_atual}",
            font=("Arial", 11),
            fg='#666666',
            bg='white'
        ).pack(side='right', padx=10)
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(frame_conteudo)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ABA 1: Lista de Clientes
        frame_lista = ttk.Frame(self.notebook)
        self.notebook.add(frame_lista, text="📋 Lista de Clientes")
        self.criar_aba_lista(frame_lista)
        
        # ABA 2: Cadastro de Cliente
        frame_cadastro = ttk.Frame(self.notebook)
        self.notebook.add(frame_cadastro, text="➕ Novo Cliente")
        self.criar_aba_cadastro(frame_cadastro)
        
        # ABA 3: Blacklist
        frame_blacklist = ttk.Frame(self.notebook)
        self.notebook.add(frame_blacklist, text="🚫 Blacklist")
        self.criar_aba_blacklist(frame_blacklist)
        
        # Botão Voltar
        frame_rodape = tk.Frame(frame_conteudo, bg='white', height=50)
        frame_rodape.pack(fill='x', padx=20, pady=10)
        frame_rodape.pack_propagate(False)
        
        btn_voltar = tk.Button(
            frame_rodape,
            text="↩️ Voltar ao Menu",
            font=("Arial", 11, "bold"),
            bg='white',
            fg=self.cor_primaria,
            bd=1,
            relief='solid',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.voltar
        )
        btn_voltar.pack(side='right')
        
        def on_enter_voltar(e):
            btn_voltar.config(bg='#f5f5f5', fg=self.cor_sombra)
        
        def on_leave_voltar(e):
            btn_voltar.config(bg='white', fg=self.cor_primaria)
        
        btn_voltar.bind('<Enter>', on_enter_voltar)
        btn_voltar.bind('<Leave>', on_leave_voltar)
    
    def criar_aba_lista(self, parent):
        # Frame de busca
        frame_busca = tk.Frame(parent, bg='#f8f9fa', padx=15, pady=10)
        frame_busca.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            frame_busca,
            text="🔍 Buscar:",
            font=("Arial", 10, "bold"),
            bg='#f8f9fa',
            fg='#333333'
        ).pack(side='left', padx=(0, 10))
        
        self.busca_entry = tk.Entry(
            frame_busca,
            font=("Arial", 10),
            width=25,
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.busca_entry.pack(side='left', padx=(0, 10), ipady=5)
        
        self.filtro_var = tk.StringVar(value="nome")
        filtros = [("Nome", "nome"), ("CPF", "cpf"), ("Telefone", "telefone")]
        
        for texto, valor in filtros:
            rb = tk.Radiobutton(
                frame_busca,
                text=texto,
                variable=self.filtro_var,
                value=valor,
                bg='#f8f9fa',
                fg='#333333',
                font=("Arial", 9),
                cursor='hand2'
            )
            rb.pack(side='left', padx=5)
        
        btn_buscar = tk.Button(
            frame_busca,
            text="🔍 BUSCAR",
            bg='white',
            fg=self.cor_primaria,
            font=("Arial", 9, "bold"),
            bd=1,
            relief='solid',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.buscar_clientes
        )
        btn_buscar.pack(side='left', padx=5)
        
        btn_limpar = tk.Button(
            frame_busca,
            text="✖ LIMPAR",
            bg='white',
            fg=self.cor_primaria,
            font=("Arial", 9, "bold"),
            bd=1,
            relief='solid',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.limpar_busca
        )
        btn_limpar.pack(side='left', padx=5)
        
        # Frame da tabela
        frame_tabela = tk.Frame(parent, bg='white')
        frame_tabela.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollbars
        scroll_y = tk.Scrollbar(frame_tabela)
        scroll_y.pack(side='right', fill='y')
        
        scroll_x = tk.Scrollbar(frame_tabela, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')
        
        # Treeview
        colunas = ('Código', 'Nome', 'CPF', 'Telefone', 'Cidade', 'Pontos', 'Status')
        self.tree_clientes = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )
        
        # Configurar colunas
        larguras = [100, 250, 150, 120, 150, 80, 100]
        for col, larg in zip(colunas, larguras):
            self.tree_clientes.heading(col, text=col)
            self.tree_clientes.column(col, width=larg)
        
        self.tree_clientes.pack(fill='both', expand=True)
        
        scroll_y.config(command=self.tree_clientes.yview)
        scroll_x.config(command=self.tree_clientes.xview)
        
        # Tags para cores
        self.tree_clientes.tag_configure('bloqueado', background='#ffe5e5')
        self.tree_clientes.tag_configure('inativo', background='#fff3e0')
        
        # Bind para duplo clique
        self.tree_clientes.bind('<Double-1>', self.ver_detalhes_cliente)
        
        # Frame de botões de ação
        frame_acoes = tk.Frame(parent, bg='white', pady=10)
        frame_acoes.pack(fill='x', padx=10)
        
        botoes = [
            ("➕ NOVO", self.novo_cliente, self.cor_primaria),
            ("📋 DETALHES", self.ver_detalhes, self.cor_primaria),
            ("✏️ EDITAR", self.editar_cliente, '#ff9800'),
            ("📊 HISTÓRICO", self.ver_historico_compras, '#9c27b0'),
            ("🚫 BLOQUEAR", self.bloquear_cliente, '#f44336')
        ]
        
        for texto, comando, cor in botoes:
            btn = tk.Button(
                frame_acoes,
                text=texto,
                font=("Arial", 10, "bold"),
                bg='white',
                fg=cor,
                bd=1,
                relief='solid',
                padx=15,
                pady=6,
                cursor='hand2',
                command=comando
            )
            btn.pack(side='left', padx=5, expand=True, fill='x')
            
            def on_enter(e, b=btn, c=cor):
                b.config(bg='#f5f5f5', fg=c)
            
            def on_leave(e, b=btn, c=cor):
                b.config(bg='white', fg=c)
            
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
    
    def criar_aba_cadastro(self, parent):
        # Canvas com scroll
        canvas = tk.Canvas(parent, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        frame = tk.Frame(scrollable_frame, bg='white', padx=30, pady=20)
        frame.pack(expand=True, fill='both')
        
        # Título do cadastro
        self.titulo_cadastro = tk.Label(
            frame,
            text="CADASTRO DE CLIENTE",
            font=("Arial", 18, "bold"),
            fg=self.cor_primaria,
            bg='white'
        )
        self.titulo_cadastro.pack(pady=10)
        
        # Subtítulo
        tk.Label(
            frame,
            text="Preencha os campos obrigatórios (*)",
            font=("Arial", 10, "italic"),
            fg='#666666',
            bg='white'
        ).pack(pady=(0, 20))
        
        # Criar um notebook interno para organizar
        interno_notebook = ttk.Notebook(frame)
        interno_notebook.pack(fill='both', expand=True, pady=10)
        
        # Aba Dados Pessoais
        frame_dados = ttk.Frame(interno_notebook)
        interno_notebook.add(frame_dados, text="Dados Pessoais")
        self.criar_dados_pessoais(frame_dados)
        
        # Aba Endereço
        frame_endereco = ttk.Frame(interno_notebook)
        interno_notebook.add(frame_endereco, text="Endereço")
        self.criar_endereco(frame_endereco)
        
        # Aba Observações
        frame_obs = ttk.Frame(interno_notebook)
        interno_notebook.add(frame_obs, text="Observações")
        self.criar_observacoes(frame_obs)
        
        # Frame para botões
        frame_botoes = tk.Frame(frame, bg='white', pady=20)
        frame_botoes.pack(fill='x')
        
        self.btn_salvar = tk.Button(
            frame_botoes,
            text="✅ SALVAR CLIENTE",
            font=("Arial", 12, "bold"),
            bg=self.cor_primaria,
            fg='white',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2',
            command=self.salvar_cliente
        )
        self.btn_salvar.pack(side='left', padx=5, expand=True, fill='x')
        
        btn_limpar = tk.Button(
            frame_botoes,
            text="🔄 LIMPAR",
            font=("Arial", 12, "bold"),
            bg='#f5f5f5',
            fg='#666666',
            bd=1,
            relief='solid',
            padx=25,
            pady=10,
            cursor='hand2',
            command=self.limpar_cadastro
        )
        btn_limpar.pack(side='left', padx=5, expand=True, fill='x')
        
        btn_cancelar = tk.Button(
            frame_botoes,
            text="↩️ CANCELAR",
            font=("Arial", 12, "bold"),
            bg='#f5f5f5',
            fg='#666666',
            bd=1,
            relief='solid',
            padx=25,
            pady=10,
            cursor='hand2',
            command=self.cancelar_edicao
        )
        btn_cancelar.pack(side='left', padx=5, expand=True, fill='x')
        
        # Efeito hover nos botões
        def on_enter_salvar(e):
            self.btn_salvar.config(bg=self.cor_sombra)
        
        def on_leave_salvar(e):
            self.btn_salvar.config(bg=self.cor_primaria)
        
        self.btn_salvar.bind('<Enter>', on_enter_salvar)
        self.btn_salvar.bind('<Leave>', on_leave_salvar)
        
        for btn in [btn_limpar, btn_cancelar]:
            def on_enter(e, b=btn):
                b.config(bg='#e0e0e0')
            
            def on_leave(e, b=btn):
                b.config(bg='#f5f5f5')
            
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def criar_dados_pessoais(self, parent):
        frame = tk.Frame(parent, bg='white', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        # Configurar grid
        for i in range(3):
            frame.columnconfigure(i, weight=1)
        
        # Linha 0-1: Nome Completo
        tk.Label(
            frame,
            text="Nome Completo:*",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["nome"] = tk.Entry(
            frame,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.entries["nome"].grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5, ipady=5)
        
        # CPF
        tk.Label(
            frame,
            text="CPF:*",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=0, column=2, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["cpf"] = tk.Entry(
            frame,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.entries["cpf"].grid(row=1, column=2, sticky='ew', padx=5, pady=5, ipady=5)
        
        # Linha 2-3: RG
        tk.Label(
            frame,
            text="RG:",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=2, column=0, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["rg"] = tk.Entry(
            frame,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.entries["rg"].grid(row=3, column=0, sticky='ew', padx=5, pady=5, ipady=5)
        
        # Data Nascimento
        tk.Label(
            frame,
            text="Data Nascimento:",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=2, column=1, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["data_nascimento"] = tk.Entry(
            frame,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.entries["data_nascimento"].grid(row=3, column=1, sticky='ew', padx=5, pady=5, ipady=5)
        
        tk.Label(
            frame,
            text="Sexo:",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=2, column=2, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["sexo"] = ttk.Combobox(
            frame,
            values=["Masculino", "Feminino", "Outro"],
            state='readonly',
            font=("Arial", 10)
        )
        self.entries["sexo"].grid(row=3, column=2, sticky='ew', padx=5, pady=5, ipady=5)
        
        # Linha 4-5: E-mail
        tk.Label(
            frame,
            text="E-mail:",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=4, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["email"] = tk.Entry(
            frame,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.entries["email"].grid(row=5, column=0, columnspan=3, sticky='ew', padx=5, pady=5, ipady=5)
        
        # Linha 6-7: Telefone Fixo
        tk.Label(
            frame,
            text="Telefone Fixo:*",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=6, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["telefone"] = tk.Entry(
            frame,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.entries["telefone"].grid(row=7, column=0, columnspan=2, sticky='ew', padx=5, pady=5, ipady=5)
        
        # Celular
        tk.Label(
            frame,
            text="Celular:",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=6, column=2, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["celular"] = tk.Entry(
            frame,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.entries["celular"].grid(row=7, column=2, sticky='ew', padx=5, pady=5, ipady=5)
    
    def criar_endereco(self, parent):
        frame = tk.Frame(parent, bg='white', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        # Configurar grid
        for i in range(4):
            frame.columnconfigure(i, weight=1)
        
        # Linha 0-1: CEP
        tk.Label(
            frame,
            text="CEP:",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=0, column=0, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["cep"] = tk.Entry(
            frame,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.entries["cep"].grid(row=1, column=0, sticky='ew', padx=5, pady=5, ipady=5)
        
        # Endereço
        tk.Label(
            frame,
            text="Endereço:*",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=0, column=1, columnspan=2, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["endereco"] = tk.Entry(
            frame,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.entries["endereco"].grid(row=1, column=1, columnspan=2, sticky='ew', padx=5, pady=5, ipady=5)
        
        # Número
        tk.Label(
            frame,
            text="Número:",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=0, column=3, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["numero"] = tk.Entry(
            frame,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd',
            width=10
        )
        self.entries["numero"].grid(row=1, column=3, sticky='ew', padx=5, pady=5, ipady=5)
        
        # Linha 2-3: Complemento
        tk.Label(
            frame,
            text="Complemento:",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["complemento"] = tk.Entry(
            frame,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.entries["complemento"].grid(row=3, column=0, columnspan=2, sticky='ew', padx=5, pady=5, ipady=5)
        
        # Bairro
        tk.Label(
            frame,
            text="Bairro:*",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=2, column=2, columnspan=2, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["bairro"] = tk.Entry(
            frame,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.entries["bairro"].grid(row=3, column=2, columnspan=2, sticky='ew', padx=5, pady=5, ipady=5)
        
        # Linha 4-5: Cidade
        tk.Label(
            frame,
            text="Cidade:*",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=4, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["cidade"] = tk.Entry(
            frame,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.entries["cidade"].grid(row=5, column=0, columnspan=2, sticky='ew', padx=5, pady=5, ipady=5)
        
        # Estado
        tk.Label(
            frame,
            text="Estado:*",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).grid(row=4, column=2, columnspan=2, sticky='w', padx=5, pady=(10, 2))
        
        self.entries["estado"] = ttk.Combobox(
            frame,
            values=["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
                    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
                    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"],
            state='readonly',
            font=("Arial", 10)
        )
        self.entries["estado"].grid(row=5, column=2, columnspan=2, sticky='ew', padx=5, pady=5, ipady=5)
    
    def criar_observacoes(self, parent):
        frame = tk.Frame(parent, bg='white', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        tk.Label(
            frame,
            text="Observações:",
            font=("Arial", 10, "bold"),
            fg='#333333',
            bg='white'
        ).pack(anchor='w')
        
        self.entries["observacoes"] = tk.Text(
            frame,
            height=6,
            font=("Arial", 10),
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.entries["observacoes"].pack(fill='both', expand=True, pady=10)
    
    def criar_aba_blacklist(self, parent):
        frame = tk.Frame(parent, bg='white', padx=10, pady=10)
        frame.pack(fill='both', expand=True)
        
        # Treeview para blacklist
        colunas = ('Código', 'Nome', 'CPF', 'Motivo', 'Data Bloqueio', 'Vencimento')
        self.tree_blacklist = ttk.Treeview(
            frame,
            columns=colunas,
            show='headings',
            height=15
        )
        
        for col in colunas:
            self.tree_blacklist.heading(col, text=col)
        
        self.tree_blacklist.column('Código', width=100)
        self.tree_blacklist.column('Nome', width=250)
        self.tree_blacklist.column('CPF', width=150)
        self.tree_blacklist.column('Motivo', width=200)
        self.tree_blacklist.column('Data Bloqueio', width=120)
        self.tree_blacklist.column('Vencimento', width=120)
        
        self.tree_blacklist.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree_blacklist.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree_blacklist.configure(yscrollcommand=scrollbar.set)
        
        # Frame de botões
        frame_botoes = tk.Frame(frame, bg='white', pady=10)
        frame_botoes.pack(fill='x')
        
        btn_desbloquear = tk.Button(
            frame_botoes,
            text="🔓 DESBLOQUEAR SELECIONADO",
            font=("Arial", 10, "bold"),
            bg='white',
            fg=self.cor_primaria,
            bd=1,
            relief='solid',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.desbloquear_cliente
        )
        btn_desbloquear.pack()
        
        def on_enter(e):
            btn_desbloquear.config(bg='#f5f5f5', fg=self.cor_sombra)
        
        def on_leave(e):
            btn_desbloquear.config(bg='white', fg=self.cor_primaria)
        
        btn_desbloquear.bind('<Enter>', on_enter)
        btn_desbloquear.bind('<Leave>', on_leave)
    
    def carregar_clientes(self):
        """Carrega lista de clientes"""
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        self.db.cursor.execute('''
            SELECT codigo, nome, cpf, telefone, cidade, pontos, status
            FROM clientes
            ORDER BY nome
        ''')
        
        clientes = self.db.cursor.fetchall()
        
        for cliente in clientes:
            codigo, nome, cpf, telefone, cidade, pontos, status = cliente
            
            # Formatar CPF
            if cpf and len(cpf) == 11:
                cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            
            item = self.tree_clientes.insert('', 'end', values=(
                codigo, nome, cpf, telefone, cidade, pontos, status
            ))
            
            if status == 'bloqueado':
                self.tree_clientes.item(item, tags=('bloqueado',))
            elif status == 'inativo':
                self.tree_clientes.item(item, tags=('inativo',))
    
    def carregar_blacklist(self):
        """Carrega lista de clientes bloqueados"""
        for item in self.tree_blacklist.get_children():
            self.tree_blacklist.delete(item)
        
        self.db.cursor.execute('''
            SELECT c.codigo, c.nome, c.cpf, b.motivo, b.data_bloqueio, b.data_vencimento
            FROM blacklist b
            JOIN clientes c ON b.cliente_codigo = c.codigo
            ORDER BY b.data_bloqueio DESC
        ''')
        
        bloqueados = self.db.cursor.fetchall()
        
        for b in bloqueados:
            # Formatar CPF
            cpf = b[2]
            if cpf and len(cpf) == 11:
                cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            
            self.tree_blacklist.insert('', 'end', values=(
                b[0], b[1], cpf, b[3], b[4], b[5] or ""
            ))
    
    def buscar_clientes(self):
        """Busca clientes conforme filtro"""
        termo = self.busca_entry.get()
        filtro = self.filtro_var.get()
        
        if not termo:
            self.carregar_clientes()
            return
        
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        query = f'''
            SELECT codigo, nome, cpf, telefone, cidade, pontos, status
            FROM clientes
            WHERE {filtro} LIKE ?
            ORDER BY nome
        '''
        
        self.db.cursor.execute(query, (f'%{termo}%',))
        clientes = self.db.cursor.fetchall()
        
        for cliente in clientes:
            codigo, nome, cpf, telefone, cidade, pontos, status = cliente
            
            if cpf and len(cpf) == 11:
                cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            
            item = self.tree_clientes.insert('', 'end', values=(
                codigo, nome, cpf, telefone, cidade, pontos, status
            ))
            
            if status == 'bloqueado':
                self.tree_clientes.item(item, tags=('bloqueado',))
            elif status == 'inativo':
                self.tree_clientes.item(item, tags=('inativo',))
    
    def limpar_busca(self):
        """Limpa busca e recarrega clientes"""
        self.busca_entry.delete(0, tk.END)
        self.filtro_var.set("nome")
        self.carregar_clientes()
    
    def novo_cliente(self):
        """Muda para aba de cadastro"""
        self.cliente_atual = None
        self.limpar_cadastro()
        self.titulo_cadastro.config(text="CADASTRO DE CLIENTE")
        self.btn_salvar.config(text="✅ SALVAR CLIENTE", command=self.salvar_cliente)
        self.notebook.select(1)
    
    def editar_cliente(self):
        """Editar cliente selecionado"""
        try:
            item = self.tree_clientes.selection()[0]
            codigo = self.tree_clientes.item(item, 'values')[0]
            
            # Buscar dados completos do cliente
            self.db.cursor.execute('SELECT * FROM clientes WHERE codigo = ?', (codigo,))
            cliente = self.db.cursor.fetchone()
            
            if cliente:
                self.cliente_atual = cliente
                
                # Limpar campos
                self.limpar_cadastro()
                
                # Preencher campos do formulário
                self.entries["nome"].insert(0, cliente[2])
                self.entries["cpf"].insert(0, cliente[3])
                self.entries["rg"].insert(0, cliente[4] or "")
                self.entries["telefone"].insert(0, cliente[5])
                self.entries["celular"].insert(0, cliente[6] or "")
                self.entries["email"].insert(0, cliente[7] or "")
                self.entries["data_nascimento"].insert(0, cliente[8] or "")
                self.entries["sexo"].set(cliente[9] or "")  # CORRIGIDO: sexo
                self.entries["endereco"].insert(0, cliente[10])
                self.entries["numero"].insert(0, cliente[11] or "")
                self.entries["complemento"].insert(0, cliente[12] or "")
                self.entries["bairro"].insert(0, cliente[13])
                self.entries["cidade"].insert(0, cliente[14])
                self.entries["estado"].set(cliente[15])
                self.entries["cep"].insert(0, cliente[16] or "")
                self.entries["observacoes"].insert("1.0", cliente[18] or "")
                
                # Mudar título e botão
                self.titulo_cadastro.config(text="EDITAR CLIENTE")
                self.btn_salvar.config(text="✅ ATUALIZAR CLIENTE", command=self.atualizar_cliente)
                
                # Ir para aba de edição
                self.notebook.select(1)
                
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar!")
    
    def cancelar_edicao(self):
        """Cancela edição e volta para lista"""
        self.cliente_atual = None
        self.limpar_cadastro()
        self.titulo_cadastro.config(text="CADASTRO DE CLIENTE")
        self.btn_salvar.config(text="✅ SALVAR CLIENTE", command=self.salvar_cliente)
        self.notebook.select(0)
    
    def limpar_cadastro(self):
        """Limpa todos os campos do cadastro"""
        for campo, entry in self.entries.items():
            if campo == "observacoes":
                entry.delete("1.0", tk.END)
            elif isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, ttk.Combobox):
                entry.set('')
    
    def salvar_cliente(self):
        """Salva novo cliente no banco"""
        try:
            # Coletar dados
            nome = self.entries["nome"].get().strip()
            cpf = self.entries["cpf"].get().strip()
            telefone = self.entries["telefone"].get().strip()
            endereco = self.entries["endereco"].get().strip()
            bairro = self.entries["bairro"].get().strip()
            cidade = self.entries["cidade"].get().strip()
            estado = self.entries["estado"].get().strip()
            
            # Campos opcionais
            rg = self.entries["rg"].get().strip()
            celular = self.entries["celular"].get().strip()
            email = self.entries["email"].get().strip()
            data_nascimento = self.entries["data_nascimento"].get().strip()
            sexo = self.entries["sexo"].get().strip()  # CORRIGIDO: sexo (não gênero)
            numero = self.entries["numero"].get().strip()
            complemento = self.entries["complemento"].get().strip()
            cep = self.entries["cep"].get().strip()
            observacoes = self.entries["observacoes"].get("1.0", tk.END).strip()
            
            # Validar campos obrigatórios
            campos_obrigatorios = {
                "Nome": nome,
                "CPF": cpf,
                "Telefone": telefone,
                "Endereço": endereco,
                "Bairro": bairro,
                "Cidade": cidade,
                "Estado": estado
            }
            
            campos_vazios = [nome_campo for nome_campo, valor in campos_obrigatorios.items() if not valor]
            
            if campos_vazios:
                messagebox.showerror("Erro", 
                                   f"Campos obrigatórios:\n" + 
                                   "\n".join(f"• {campo}" for campo in campos_vazios))
                return
            
            # Validar CPF (apenas números)
            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            if len(cpf_limpo) != 11:
                messagebox.showerror("Erro", "CPF deve conter 11 dígitos!")
                return
            
            # Verificar se CPF já existe
            self.db.cursor.execute("SELECT codigo FROM clientes WHERE cpf = ?", (cpf_limpo,))
            if self.db.cursor.fetchone():
                messagebox.showerror("Erro", "CPF já cadastrado!")
                return
            
            # Gerar código do cliente
            codigo = self.db.gerar_codigo_cliente()
            
            # Inserir no banco - CORRIGIDO: usando 'sexo' (não 'gênero')
            self.db.cursor.execute('''
                INSERT INTO clientes (
                    codigo, nome, cpf, rg, telefone, celular, email,
                    data_nascimento, sexo, endereco, numero, complemento,
                    bairro, cidade, estado, cep, data_cadastro, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (codigo, nome, cpf_limpo, rg, telefone, celular, email,
                  data_nascimento, sexo, endereco, numero, complemento,
                  bairro, cidade, estado, cep, datetime.now().strftime("%d/%m/%Y"),
                  observacoes))
            
            self.db.conn.commit()
            
            messagebox.showinfo("Sucesso", f"Cliente cadastrado com sucesso!\nCódigo: {codigo}")
            
            # Limpar campos e recarregar lista
            self.limpar_cadastro()
            self.carregar_clientes()
            self.carregar_blacklist()
            
            # Voltar para aba de lista
            self.notebook.select(0)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar cliente: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def atualizar_cliente(self):
        """Atualiza dados do cliente existente"""
        try:
            if not self.cliente_atual:
                return
            
            # Coletar dados
            nome = self.entries["nome"].get().strip()
            cpf = self.entries["cpf"].get().strip()
            telefone = self.entries["telefone"].get().strip()
            endereco = self.entries["endereco"].get().strip()
            bairro = self.entries["bairro"].get().strip()
            cidade = self.entries["cidade"].get().strip()
            estado = self.entries["estado"].get().strip()
            
            # Campos opcionais
            rg = self.entries["rg"].get().strip()
            celular = self.entries["celular"].get().strip()
            email = self.entries["email"].get().strip()
            data_nascimento = self.entries["data_nascimento"].get().strip()
            sexo = self.entries["sexo"].get().strip()  # CORRIGIDO: sexo
            numero = self.entries["numero"].get().strip()
            complemento = self.entries["complemento"].get().strip()
            cep = self.entries["cep"].get().strip()
            observacoes = self.entries["observacoes"].get("1.0", tk.END).strip()
            
            # Validar campos obrigatórios
            if not all([nome, cpf, telefone, endereco, bairro, cidade, estado]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            # Validar CPF
            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            if len(cpf_limpo) != 11:
                messagebox.showerror("Erro", "CPF deve conter 11 dígitos!")
                return
            
            # Verificar se CPF já existe para outro cliente
            self.db.cursor.execute('''
                SELECT codigo FROM clientes 
                WHERE cpf = ? AND codigo != ?
            ''', (cpf_limpo, self.cliente_atual[1]))
            
            if self.db.cursor.fetchone():
                messagebox.showerror("Erro", "CPF já cadastrado para outro cliente!")
                return
            
            self.db.cursor.execute('''
                UPDATE clientes SET
                    nome = ?, cpf = ?, rg = ?, telefone = ?, celular = ?, email = ?,
                    data_nascimento = ?, sexo = ?, endereco = ?, numero = ?, complemento = ?,
                    bairro = ?, cidade = ?, estado = ?, cep = ?, observacoes = ?
                WHERE codigo = ?
            ''', (nome, cpf_limpo, rg, telefone, celular, email,
                  data_nascimento, sexo, endereco, numero, complemento,
                  bairro, cidade, estado, cep, observacoes,
                  self.cliente_atual[1]))
            
            self.db.conn.commit()
            
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            
            # Limpar e recarregar
            self.cliente_atual = None
            self.limpar_cadastro()
            self.carregar_clientes()
            self.carregar_blacklist()
            
            # Resetar formulário e voltar para lista
            self.titulo_cadastro.config(text="CADASTRO DE CLIENTE")
            self.btn_salvar.config(text="✅ SALVAR CLIENTE", command=self.salvar_cliente)
            self.notebook.select(0)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar cliente: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def ver_detalhes_cliente(self, event):
        """Ver detalhes do cliente com duplo clique"""
        self.ver_detalhes()
    
    def ver_detalhes(self):
        """Ver detalhes do cliente selecionado"""
        try:
            item = self.tree_clientes.selection()[0]
            codigo = self.tree_clientes.item(item, 'values')[0]
            
            # Buscar dados completos do cliente
            self.db.cursor.execute('SELECT * FROM clientes WHERE codigo = ?', (codigo,))
            cliente = self.db.cursor.fetchone()
            
            if cliente:
                # Formatar CPF
                cpf = cliente[3]
                if cpf and len(cpf) == 11:
                    cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
                
                detalhes = f"""
╔════════════════════════════════════════════════════════════╗
║                    DETALHES DO CLIENTE                     ║
╠════════════════════════════════════════════════════════════╣
║ Código: {cliente[1]}                                       
║ Nome: {cliente[2]}                                          
║ CPF: {cpf}                                                  
║ RG: {cliente[4] or '---'}                                   
║ Telefone: {cliente[5]}                                      
║ Celular: {cliente[6] or '---'}                              
║ E-mail: {cliente[7] or '---'}                               
║ Data Nasc.: {cliente[8] or '---'}                           
║ Sexo: {cliente[9] or '---'}                                 
╠════════════════════════════════════════════════════════════╣
║                    ENDEREÇO                                 ║
╠════════════════════════════════════════════════════════════╣
║ {cliente[10]}, {cliente[11] or 's/n'} {cliente[12] or ''}   
║ {cliente[13]} - {cliente[14]}/{cliente[15]}                 
║ CEP: {cliente[16] or '---'}                                 
╠════════════════════════════════════════════════════════════╣
║ Pontos: {cliente[19]}  |  Status: {cliente[20]}             
╚════════════════════════════════════════════════════════════╝
                """
                
                # Criar janela de detalhes
                detalhes_janela = tk.Toplevel(self.janela)
                detalhes_janela.title("Detalhes do Cliente")
                detalhes_janela.geometry("600x500")
                detalhes_janela.configure(bg='white')
                
                # Centralizar
                detalhes_janela.update_idletasks()
                x = (detalhes_janela.winfo_screenwidth() // 2) - (600 // 2)
                y = (detalhes_janela.winfo_screenheight() // 2) - (500 // 2)
                detalhes_janela.geometry(f'{600}x{500}+{x}+{y}')
                
                # Área de texto
                texto = tk.Text(
                    detalhes_janela,
                    font=("Courier", 10),
                    padx=20,
                    pady=20,
                    bg='#f9f9f9',
                    relief='solid',
                    bd=1
                )
                texto.pack(fill='both', expand=True, padx=10, pady=10)
                texto.insert('1.0', detalhes)
                texto.config(state='disabled')
                
                # Botão fechar
                btn_fechar = tk.Button(
                    detalhes_janela,
                    text="FECHAR",
                    font=("Arial", 10, "bold"),
                    bg='white',
                    fg=self.cor_primaria,
                    bd=1,
                    relief='solid',
                    padx=20,
                    pady=8,
                    cursor='hand2',
                    command=detalhes_janela.destroy
                )
                btn_fechar.pack(pady=10)
                
                def on_enter(e):
                    btn_fechar.config(bg='#f5f5f5', fg=self.cor_sombra)
                
                def on_leave(e):
                    btn_fechar.config(bg='white', fg=self.cor_primaria)
                
                btn_fechar.bind('<Enter>', on_enter)
                btn_fechar.bind('<Leave>', on_leave)
                
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um cliente para ver detalhes!")
    
    def ver_historico_compras(self):
        """Ver histórico de compras do cliente selecionado"""
        try:
            item = self.tree_clientes.selection()[0]
            codigo = self.tree_clientes.item(item, 'values')[0]
            nome = self.tree_clientes.item(item, 'values')[1]
            
            # Buscar compras do cliente
            self.db.cursor.execute('''
                SELECT v.data_venda, v.id, p.nome, v.quantidade, 
                       v.preco_unitario, v.total, v.pontos_ganhos
                FROM vendas v
                JOIN produtos p ON v.codigo_produto = p.codigo
                WHERE v.cliente_codigo = ?
                ORDER BY v.data_venda DESC, v.hora_venda DESC
            ''', (codigo,))
            
            compras = self.db.cursor.fetchall()
            
            if not compras:
                messagebox.showinfo("Histórico", f"Cliente {nome} não possui compras registradas.")
                return
            
            # Criar janela de histórico
            hist_janela = tk.Toplevel(self.janela)
            hist_janela.title(f"Histórico de Compras - {nome}")
            hist_janela.geometry("900x400")
            hist_janela.configure(bg='white')
            
            # Centralizar
            hist_janela.update_idletasks()
            x = (hist_janela.winfo_screenwidth() // 2) - (900 // 2)
            y = (hist_janela.winfo_screenheight() // 2) - (400 // 2)
            hist_janela.geometry(f'{900}x{400}+{x}+{y}')
            
            # Frame para a tabela
            frame = tk.Frame(hist_janela, bg='white', padx=10, pady=10)
            frame.pack(fill='both', expand=True)
            
            # Scrollbars
            scroll_y = tk.Scrollbar(frame)
            scroll_y.pack(side='right', fill='y')
            
            scroll_x = tk.Scrollbar(frame, orient='horizontal')
            scroll_x.pack(side='bottom', fill='x')
            
            # Treeview
            colunas = ('Data', 'ID', 'Produto', 'Qtd', 'Preço Unit.', 'Total', 'Pontos')
            tree = ttk.Treeview(
                frame,
                columns=colunas,
                show='headings',
                yscrollcommand=scroll_y.set,
                xscrollcommand=scroll_x.set
            )
            
            for col in colunas:
                tree.heading(col, text=col)
            
            tree.column('Data', width=100)
            tree.column('ID', width=80)
            tree.column('Produto', width=250)
            tree.column('Qtd', width=50)
            tree.column('Preço Unit.', width=100)
            tree.column('Total', width=100)
            tree.column('Pontos', width=80)
            
            tree.pack(fill='both', expand=True)
            
            scroll_y.config(command=tree.yview)
            scroll_x.config(command=tree.xview)
            
            # Inserir dados
            for compra in compras:
                data, venda_id, produto, qtd, preco, total, pontos = compra
                tree.insert('', 'end', values=(
                    data, venda_id, produto, qtd, f"R$ {preco:.2f}", 
                    f"R$ {total:.2f}", pontos
                ))
            
            # Botão fechar
            btn_fechar = tk.Button(
                hist_janela,
                text="FECHAR",
                font=("Arial", 10, "bold"),
                bg='white',
                fg=self.cor_primaria,
                bd=1,
                relief='solid',
                padx=15,
                pady=5,
                cursor='hand2',
                command=hist_janela.destroy
            )
            btn_fechar.pack(pady=5)
            
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um cliente para ver o histórico!")
    
    def bloquear_cliente(self):
        """Bloqueia o cliente selecionado"""
        try:
            item = self.tree_clientes.selection()[0]
            codigo = self.tree_clientes.item(item, 'values')[0]
            nome = self.tree_clientes.item(item, 'values')[1]
            
            # Dialog para motivo
            motivo_janela = tk.Toplevel(self.janela)
            motivo_janela.title("Bloquear Cliente")
            motivo_janela.geometry("450x300")
            motivo_janela.configure(bg='white')
            motivo_janela.transient(self.janela)
            motivo_janela.grab_set()
            
            # Centralizar
            motivo_janela.update_idletasks()
            x = (motivo_janela.winfo_screenwidth() // 2) - (450 // 2)
            y = (motivo_janela.winfo_screenheight() // 2) - (300 // 2)
            motivo_janela.geometry(f'{450}x{300}+{x}+{y}')
            
            frame = tk.Frame(motivo_janela, bg='white', padx=20, pady=20)
            frame.pack(fill='both', expand=True)
            
            tk.Label(
                frame,
                text=f"🚫 BLOQUEAR CLIENTE",
                font=("Arial", 14, "bold"),
                fg=self.cor_primaria,
                bg='white'
            ).pack(pady=10)
            
            tk.Label(
                frame,
                text=f"Cliente: {nome}",
                font=("Arial", 11, "bold"),
                fg='#333333',
                bg='white'
            ).pack(pady=5)
            
            tk.Label(
                frame,
                text="Motivo do bloqueio:*",
                font=("Arial", 10),
                bg='white',
                fg='#333333'
            ).pack(anchor='w', pady=(10, 2))
            
            motivo_entry = tk.Entry(
                frame,
                font=("Arial", 10),
                width=40,
                relief='solid',
                bd=1,
                highlightbackground='#dddddd'
            )
            motivo_entry.pack(pady=(0, 10), ipady=5)
            
            tk.Label(
                frame,
                text="Data de vencimento (opcional):",
                font=("Arial", 10),
                bg='white',
                fg='#333333'
            ).pack(anchor='w', pady=(10, 2))
            
            vencimento_entry = tk.Entry(
                frame,
                font=("Arial", 10),
                width=20,
                relief='solid',
                bd=1,
                highlightbackground='#dddddd'
            )
            vencimento_entry.pack(pady=(0, 10), ipady=5)
            vencimento_entry.insert(0, "DD/MM/AAAA")
            
            def confirmar_bloqueio():
                motivo = motivo_entry.get().strip()
                if not motivo:
                    messagebox.showerror("Erro", "Informe o motivo do bloqueio!")
                    return
                
                vencimento = vencimento_entry.get().strip()
                if vencimento == "DD/MM/AAAA":
                    vencimento = ""
                
                # Atualizar status do cliente
                self.db.cursor.execute('''
                    UPDATE clientes SET status = 'bloqueado' WHERE codigo = ?
                ''', (codigo,))
                
                # Inserir na blacklist
                data_atual = datetime.now().strftime("%d/%m/%Y")
                self.db.cursor.execute('''
                    INSERT INTO blacklist (cliente_codigo, motivo, data_bloqueio, data_vencimento)
                    VALUES (?, ?, ?, ?)
                ''', (codigo, motivo, data_atual, vencimento))
                
                self.db.conn.commit()
                
                messagebox.showinfo("Sucesso", f"Cliente {nome} bloqueado com sucesso!")
                motivo_janela.destroy()
                self.carregar_clientes()
                self.carregar_blacklist()
            
            # Botões
            frame_botoes = tk.Frame(frame, bg='white', pady=10)
            frame_botoes.pack(fill='x')
            
            btn_confirmar = tk.Button(
                frame_botoes,
                text="🚫 CONFIRMAR BLOQUEIO",
                font=("Arial", 11, "bold"),
                bg='#f44336',
                fg='white',
                bd=0,
                padx=15,
                pady=8,
                cursor='hand2',
                command=confirmar_bloqueio
            )
            btn_confirmar.pack(side='left', padx=5, expand=True, fill='x')
            
            btn_cancelar = tk.Button(
                frame_botoes,
                text="✖ CANCELAR",
                font=("Arial", 11, "bold"),
                bg='#f5f5f5',
                fg='#666666',
                bd=1,
                relief='solid',
                padx=15,
                pady=8,
                cursor='hand2',
                command=motivo_janela.destroy
            )
            btn_cancelar.pack(side='left', padx=5, expand=True, fill='x')
            
            def on_enter_confirmar(e):
                btn_confirmar.config(bg='#d32f2f')
            
            def on_leave_confirmar(e):
                btn_confirmar.config(bg='#f44336')
            
            btn_confirmar.bind('<Enter>', on_enter_confirmar)
            btn_confirmar.bind('<Leave>', on_leave_confirmar)
            
            def on_enter_cancelar(e):
                btn_cancelar.config(bg='#e0e0e0')
            
            def on_leave_cancelar(e):
                btn_cancelar.config(bg='#f5f5f5')
            
            btn_cancelar.bind('<Enter>', on_enter_cancelar)
            btn_cancelar.bind('<Leave>', on_leave_cancelar)
            
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um cliente para bloquear!")
    
    def desbloquear_cliente(self):
        """Desbloqueia o cliente selecionado na blacklist"""
        try:
            item = self.tree_blacklist.selection()[0]
            codigo = self.tree_blacklist.item(item, 'values')[0]
            nome = self.tree_blacklist.item(item, 'values')[1]
            
            if messagebox.askyesno("Confirmar", f"Deseja desbloquear o cliente {nome}?"):
                # Atualizar status do cliente
                self.db.cursor.execute('''
                    UPDATE clientes SET status = 'ativo' WHERE codigo = ?
                ''', (codigo,))
                
                # Remover da blacklist
                self.db.cursor.execute('''
                    DELETE FROM blacklist WHERE cliente_codigo = ?
                ''', (codigo,))
                
                self.db.conn.commit()
                
                messagebox.showinfo("Sucesso", f"Cliente {nome} desbloqueado!")
                self.carregar_clientes()
                self.carregar_blacklist()
            
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um cliente na blacklist para desbloquear!")
    
    def voltar(self):
        """Volta para o menu principal"""
        self.db.fechar_conexao()
        self.janela.destroy()
        self.menu_principal.deiconify()