# financeiro.py - Módulo de Gestão Financeira com Fluxo de Caixa Completo
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from styles import Estilos

class TelaFinanceiro:
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.db = Database()
        self.janela = tk.Toplevel()
        self.janela.title("StockMaster - Gestão Financeira")
        self.janela.geometry("1300x750")
        self.janela.resizable(False, False)
        self.janela.configure(bg='#f5f5f5')
        
        # Cores
        self.cor_primaria = Estilos.COR_PRIMARIA
        self.cor_sucesso = Estilos.COR_SUCESSO
        self.cor_perigo = Estilos.COR_PERIGO
        self.cor_alerta = Estilos.COR_ALERTA
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 1300
        altura = 750
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        # Variáveis de controle
        self.movimentacoes = []  # Lista de todas as movimentações
        self.saldo_atual = 0.0
        self.projecoes = {}
        
        self.criar_interface()
        self.carregar_dados_reais()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)
        self.janela.mainloop()
    
    def carregar_dados_reais(self):
        """Carrega dados reais do banco de dados"""
        self.carregar_movimentacoes()
        self.calcular_resumo()
        self.atualizar_fluxo_direto()
        self.atualizar_analise_operacional()
        self.atualizar_projecoes()
        self.atualizar_analise_categorias()
    
    def carregar_movimentacoes(self):
        """Carrega movimentações do banco de dados (vendas e despesas)"""
        self.movimentacoes = []
        
        try:
            # 1. Carregar vendas como entradas
            self.db.cursor.execute('''
                SELECT data_venda, 'Venda #' || id, 'Vendas', 'entrada', 
                       total, 'Dinheiro', 'conciliado'
                FROM vendas
                ORDER BY data_venda DESC
            ''')
            
            vendas = self.db.cursor.fetchall()
            for venda in vendas:
                self.movimentacoes.append({
                    'data': venda[0],
                    'descricao': venda[1],
                    'categoria': 'Vendas',
                    'tipo': 'entrada',
                    'valor': float(venda[4]),
                    'forma_pagamento': 'Dinheiro',
                    'status': 'conciliado'
                })
            
            # 2. Carregar compras de produtos como saídas
            self.db.cursor.execute('''
                SELECT data_cadastro, 'Compra de ' || nome, 'Compras', 'saida',
                       quantidade * preco_custo, 'Boleto', 'pendente'
                FROM produtos
                WHERE preco_custo > 0
                ORDER BY data_cadastro DESC
            ''')
            
            compras = self.db.cursor.fetchall()
            for compra in compras:
                self.movimentacoes.append({
                    'data': compra[0],
                    'descricao': compra[1],
                    'categoria': 'Compras',
                    'tipo': 'saida',
                    'valor': float(compra[4]),
                    'forma_pagamento': 'Boleto',
                    'status': 'pendente'
                })
            
            # Se não houver dados, criar dados simulados para teste
            if not self.movimentacoes:
                self.criar_dados_simulados()
            
            # Ordenar por data
            self.movimentacoes.sort(
                key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y') if '/' in x['data'] else datetime.now(),
                reverse=True
            )
            
        except Exception as e:
            print(f"Erro ao carregar movimentações: {e}")
            self.criar_dados_simulados()
    
    def criar_dados_simulados(self):
        """Cria dados simulados para teste"""
        hoje = datetime.now()
        
        dados_simulados = [
            {
                'data': (hoje - timedelta(days=0)).strftime("%d/%m/%Y"),
                'descricao': 'Venda #1245 - Cliente A',
                'categoria': 'Vendas',
                'tipo': 'entrada',
                'valor': 1250.00,
                'forma_pagamento': 'Dinheiro',
                'status': 'conciliado'
            },
            {
                'data': (hoje - timedelta(days=0)).strftime("%d/%m/%Y"),
                'descricao': 'Compra Fornecedor X',
                'categoria': 'Compras',
                'tipo': 'saida',
                'valor': 890.00,
                'forma_pagamento': 'Boleto',
                'status': 'pendente'
            },
            {
                'data': (hoje - timedelta(days=1)).strftime("%d/%m/%Y"),
                'descricao': 'Venda #1244 - Cliente B',
                'categoria': 'Vendas',
                'tipo': 'entrada',
                'valor': 2300.00,
                'forma_pagamento': 'Cartão',
                'status': 'conciliado'
            },
            {
                'data': (hoje - timedelta(days=1)).strftime("%d/%m/%Y"),
                'descricao': 'Pagamento Energia',
                'categoria': 'Despesas Fixas',
                'tipo': 'saida',
                'valor': 350.00,
                'forma_pagamento': 'Débito',
                'status': 'conciliado'
            },
            {
                'data': (hoje - timedelta(days=2)).strftime("%d/%m/%Y"),
                'descricao': 'Venda #1243 - Cliente C',
                'categoria': 'Vendas',
                'tipo': 'entrada',
                'valor': 890.00,
                'forma_pagamento': 'PIX',
                'status': 'conciliado'
            },
            {
                'data': (hoje - timedelta(days=2)).strftime("%d/%m/%Y"),
                'descricao': 'Aluguel',
                'categoria': 'Despesas Fixas',
                'tipo': 'saida',
                'valor': 1500.00,
                'forma_pagamento': 'Boleto',
                'status': 'pendente'
            },
            {
                'data': (hoje - timedelta(days=3)).strftime("%d/%m/%Y"),
                'descricao': 'Venda #1242 - Cliente D',
                'categoria': 'Vendas',
                'tipo': 'entrada',
                'valor': 450.00,
                'forma_pagamento': 'Dinheiro',
                'status': 'conciliado'
            },
            {
                'data': (hoje - timedelta(days=3)).strftime("%d/%m/%Y"),
                'descricao': 'Material de Escritório',
                'categoria': 'Despesas Variáveis',
                'tipo': 'saida',
                'valor': 120.00,
                'forma_pagamento': 'Débito',
                'status': 'conciliado'
            }
        ]
        
        self.movimentacoes = dados_simulados
    
    def criar_interface(self):
        # Frame principal com scroll
        canvas = tk.Canvas(self.janela, bg='#f5f5f5', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.janela, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f5f5f5')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # ===== CABEÇALHO =====
        frame_cabecalho = tk.Frame(scrollable_frame, bg='white', height=80)
        frame_cabecalho.pack(fill='x', padx=20, pady=(20, 10))
        frame_cabecalho.pack_propagate(False)
        
        # Título
        titulo = tk.Label(
            frame_cabecalho,
            text="💰 GESTÃO FINANCEIRA",
            font=("Arial", 22, "bold"),
            fg=self.cor_primaria,
            bg='white'
        )
        titulo.pack(side='left', padx=20)
        
        # Data atual
        self.data_atual = datetime.now().strftime("%d/%m/%Y")
        tk.Label(
            frame_cabecalho,
            text=f"📅 {self.data_atual}",
            font=("Arial", 12),
            fg=Estilos.COR_TEXTO_SECUNDARIO,
            bg='white'
        ).pack(side='right', padx=20)
        
        # Botão Voltar
        btn_voltar_frame, btn_voltar = Estilos.criar_botao_moderno(
            frame_cabecalho,
            "Voltar",
            self.voltar,
            tipo='secundario',
            icone="↩️"
        )
        btn_voltar_frame.pack(side='right', padx=10)
        
        # Botão Nova Movimentação
        btn_novo_frame, btn_novo = Estilos.criar_botao_moderno(
            frame_cabecalho,
            "Nova Movimentação",
            self.nova_movimentacao,
            tipo='primario',
            icone="➕"
        )
        btn_novo_frame.pack(side='right', padx=10)
        
        # Botão Atualizar
        btn_atualizar_frame, btn_atualizar = Estilos.criar_botao_moderno(
            frame_cabecalho,
            "Atualizar",
            self.carregar_dados_reais,
            tipo='secundario',
            icone="🔄"
        )
        btn_atualizar_frame.pack(side='right', padx=10)
        
        # ===== CARDS DE RESUMO =====
        frame_resumo = tk.Frame(scrollable_frame, bg='#f5f5f5', height=120)
        frame_resumo.pack(fill='x', padx=20, pady=10)
        frame_resumo.pack_propagate(False)
        
        for i in range(4):
            frame_resumo.columnconfigure(i, weight=1)
        
        # Card 1 - Saldo Atual
        self.card_saldo = self.criar_card_resumo(
            frame_resumo,
            "Saldo Atual",
            "R$ 0,00",
            "disponível",
            "💰",
            self.cor_primaria,
            0
        )
        
        # Card 2 - Entradas do Mês
        self.card_entradas = self.criar_card_resumo(
            frame_resumo,
            "Entradas do Mês",
            "R$ 0,00",
            "receitas",
            "📈",
            self.cor_sucesso,
            1
        )
        
        # Card 3 - Saídas do Mês
        self.card_saidas = self.criar_card_resumo(
            frame_resumo,
            "Saídas do Mês",
            "R$ 0,00",
            "despesas",
            "📉",
            self.cor_perigo,
            2
        )
        
        # Card 4 - Saldo Projetado
        self.card_projetado = self.criar_card_resumo(
            frame_resumo,
            "Saldo Projetado",
            "R$ 0,00",
            "em 30 dias",
            "📊",
            self.cor_alerta,
            3
        )
        
        # ===== NOTEBOOK COM ABAS =====
        self.notebook = ttk.Notebook(scrollable_frame)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        Estilos.aplicar_estilo_notebook(self.notebook)
        
        # ABA 1: Fluxo de Caixa Direto
        frame_fluxo_direto = ttk.Frame(self.notebook)
        self.notebook.add(frame_fluxo_direto, text="📊 Fluxo de Caixa Direto")
        self.criar_aba_fluxo_direto(frame_fluxo_direto)
        
        # ABA 2: Análise Operacional
        frame_operacional = ttk.Frame(self.notebook)
        self.notebook.add(frame_operacional, text="📈 Análise Operacional")
        self.criar_aba_operacional(frame_operacional)
        
        # ABA 3: Fluxo Projetado
        frame_projetado = ttk.Frame(self.notebook)
        self.notebook.add(frame_projetado, text="🔮 Fluxo Projetado")
        self.criar_aba_projetado(frame_projetado)
        
        # ABA 4: Análise por Categoria
        frame_categorias = ttk.Frame(self.notebook)
        self.notebook.add(frame_categorias, text="📋 Análise por Categoria")
        self.criar_aba_categorias(frame_categorias)
        
        # ABA 5: Conciliação Bancária
        frame_conciliacao = ttk.Frame(self.notebook)
        self.notebook.add(frame_conciliacao, text="🏦 Conciliação Bancária")
        self.criar_aba_conciliacao(frame_conciliacao)
        
        # Empacotar canvas com scroll
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def criar_card_resumo(self, parent, titulo, valor, subtitulo, icone, cor, coluna):
        """Cria um card de resumo financeiro"""
        card = tk.Frame(
            parent,
            bg='white',
            highlightbackground=Estilos.COR_BORDA,
            highlightthickness=1,
            bd=0,
            width=280,
            height=100
        )
        card.grid(row=0, column=coluna, padx=10, pady=5, sticky='nsew')
        card.grid_propagate(False)
        
        # Layout do card
        frame_info = tk.Frame(card, bg='white', padx=15, pady=10)
        frame_info.pack(side='left', fill='both', expand=True)
        
        tk.Label(
            frame_info,
            text=titulo,
            font=("Arial", 10),
            fg=Estilos.COR_TEXTO_SECUNDARIO,
            bg='white'
        ).pack(anchor='w')
        
        lbl_valor = tk.Label(
            frame_info,
            text=valor,
            font=("Arial", 16, "bold"),
            fg=cor,
            bg='white'
        )
        lbl_valor.pack(anchor='w', pady=(2, 0))
        
        tk.Label(
            frame_info,
            text=subtitulo,
            font=("Arial", 8),
            fg='#999999',
            bg='white'
        ).pack(anchor='w')
        
        frame_icone = tk.Frame(card, bg='white', width=50)
        frame_icone.pack(side='right', fill='y')
        
        tk.Label(
            frame_icone,
            text=icone,
            font=("Arial", 24),
            fg=cor,
            bg='white'
        ).pack(expand=True)
        
        card.lbl_valor = lbl_valor
        return card
    
    def criar_aba_fluxo_direto(self, parent):
        """Aba de Fluxo de Caixa Direto"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame de filtros
        frame_filtros = tk.Frame(frame, bg='white', height=50)
        frame_filtros.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            frame_filtros,
            text="Período:",
            font=("Arial", 10),
            bg='white'
        ).pack(side='left', padx=(0, 5))
        
        self.periodo_var = tk.StringVar(value="30")
        periodo_combo = ttk.Combobox(
            frame_filtros,
            textvariable=self.periodo_var,
            values=["7", "15", "30", "60", "90", "180", "365"],
            font=("Arial", 10),
            width=10,
            state='readonly'
        )
        periodo_combo.pack(side='left', padx=(0, 10))
        periodo_combo.bind('<<ComboboxSelected>>', lambda e: self.atualizar_fluxo_direto())
        
        tk.Label(
            frame_filtros,
            text="dias",
            font=("Arial", 10),
            bg='white'
        ).pack(side='left')
        
        # Frame da tabela
        frame_tabela = tk.Frame(frame, bg='white')
        frame_tabela.pack(fill='both', expand=True)
        
        # Treeview
        colunas = ('Data', 'Descrição', 'Categoria', 'Tipo', 'Valor', 'Forma Pagto', 'Saldo', 'Status')
        self.tree_movimentos = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show='headings',
            height=15
        )
        
        for col in colunas:
            self.tree_movimentos.heading(col, text=col)
        
        self.tree_movimentos.column('Data', width=90)
        self.tree_movimentos.column('Descrição', width=250)
        self.tree_movimentos.column('Categoria', width=150)
        self.tree_movimentos.column('Tipo', width=80)
        self.tree_movimentos.column('Valor', width=120)
        self.tree_movimentos.column('Forma Pagto', width=100)
        self.tree_movimentos.column('Saldo', width=120)
        self.tree_movimentos.column('Status', width=100)
        
        scrollbar = ttk.Scrollbar(frame_tabela, orient='vertical', command=self.tree_movimentos.yview)
        self.tree_movimentos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_movimentos.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Tags para cores
        self.tree_movimentos.tag_configure('entrada', foreground=self.cor_sucesso)
        self.tree_movimentos.tag_configure('saida', foreground=self.cor_perigo)
        self.tree_movimentos.tag_configure('pendente', foreground=self.cor_alerta)
        self.tree_movimentos.tag_configure('conciliado', background='#e8f5e8')
        
        # Frame de resumo
        frame_resumo = tk.Frame(frame, bg='white', height=40)
        frame_resumo.pack(fill='x', pady=(10, 0))
        
        self.lbl_total_periodo = tk.Label(
            frame_resumo,
            text="Total do período: R$ 0,00",
            font=("Arial", 11, "bold"),
            fg=self.cor_primaria,
            bg='white'
        )
        self.lbl_total_periodo.pack(side='left')
        
        self.lbl_saldo_final = tk.Label(
            frame_resumo,
            text="Saldo final: R$ 0,00",
            font=("Arial", 11, "bold"),
            fg=self.cor_sucesso,
            bg='white'
        )
        self.lbl_saldo_final.pack(side='right')
    
    def criar_aba_operacional(self, parent):
        """Aba de Análise Operacional"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame para gráfico
        frame_grafico = tk.Frame(frame, bg='white', height=250)
        frame_grafico.pack(fill='x', pady=(0, 10))
        
        self.fig_operacional, self.ax_operacional = plt.subplots(figsize=(12, 3))
        self.canvas_operacional = FigureCanvasTkAgg(self.fig_operacional, master=frame_grafico)
        self.canvas_operacional.get_tk_widget().pack(fill='both', expand=True)
        
        # Tabela de indicadores
        frame_indicadores = tk.Frame(frame, bg='white')
        frame_indicadores.pack(fill='both', expand=True, pady=10)
        
        colunas = ('Indicador', 'Valor', 'Período', 'Tendência')
        self.tree_indicadores = ttk.Treeview(
            frame_indicadores,
            columns=colunas,
            show='headings',
            height=8
        )
        
        for col in colunas:
            self.tree_indicadores.heading(col, text=col)
        
        self.tree_indicadores.column('Indicador', width=200)
        self.tree_indicadores.column('Valor', width=150)
        self.tree_indicadores.column('Período', width=150)
        self.tree_indicadores.column('Tendência', width=150)
        
        self.tree_indicadores.pack(fill='both', expand=True)
    
    def criar_aba_projetado(self, parent):
        """Aba de Fluxo Projetado"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame de controles
        frame_controles = tk.Frame(frame, bg='white', height=60)
        frame_controles.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            frame_controles,
            text="Cenário:",
            font=("Arial", 10),
            bg='white'
        ).pack(side='left', padx=(0, 5))
        
        self.cenario_var = tk.StringVar(value="moderado")
        cenario_combo = ttk.Combobox(
            frame_controles,
            textvariable=self.cenario_var,
            values=["otimista", "moderado", "pessimista"],
            font=("Arial", 10),
            width=15,
            state='readonly'
        )
        cenario_combo.pack(side='left', padx=(0, 10))
        cenario_combo.bind('<<ComboboxSelected>>', lambda e: self.atualizar_projecoes())
        
        tk.Label(
            frame_controles,
            text="Período:",
            font=("Arial", 10),
            bg='white'
        ).pack(side='left', padx=(10, 5))
        
        self.projecao_periodo_var = tk.StringVar(value="30")
        projecao_combo = ttk.Combobox(
            frame_controles,
            textvariable=self.projecao_periodo_var,
            values=["30", "60", "90", "180"],
            font=("Arial", 10),
            width=10,
            state='readonly'
        )
        projecao_combo.pack(side='left', padx=(0, 10))
        projecao_combo.bind('<<ComboboxSelected>>', lambda e: self.atualizar_projecoes())
        
        # Frame para gráfico
        frame_grafico = tk.Frame(frame, bg='white', height=250)
        frame_grafico.pack(fill='x', pady=10)
        
        self.fig_projetado, self.ax_projetado = plt.subplots(figsize=(12, 3))
        self.canvas_projetado = FigureCanvasTkAgg(self.fig_projetado, master=frame_grafico)
        self.canvas_projetado.get_tk_widget().pack(fill='both', expand=True)
        
        # Tabela de projeções
        frame_tabela = tk.Frame(frame, bg='white')
        frame_tabela.pack(fill='both', expand=True)
        
        colunas = ('Data', 'Previsão Entrada', 'Previsão Saída', 'Saldo Projetado', 'Cenário')
        self.tree_projecoes = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show='headings',
            height=10
        )
        
        for col in colunas:
            self.tree_projecoes.heading(col, text=col)
        
        self.tree_projecoes.column('Data', width=100)
        self.tree_projecoes.column('Previsão Entrada', width=150)
        self.tree_projecoes.column('Previsão Saída', width=150)
        self.tree_projecoes.column('Saldo Projetado', width=150)
        self.tree_projecoes.column('Cenário', width=100)
        
        self.tree_projecoes.pack(fill='both', expand=True)
    
    def criar_aba_categorias(self, parent):
        """Aba de Análise por Categoria"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame para gráficos
        frame_graficos = tk.Frame(frame, bg='white', height=250)
        frame_graficos.pack(fill='x', pady=(0, 10))
        
        self.fig_categorias, (self.ax_entradas, self.ax_saidas) = plt.subplots(1, 2, figsize=(12, 4))
        self.canvas_categorias = FigureCanvasTkAgg(self.fig_categorias, master=frame_graficos)
        self.canvas_categorias.get_tk_widget().pack(fill='both', expand=True)
        
        # Notebook interno
        cat_notebook = ttk.Notebook(frame)
        cat_notebook.pack(fill='both', expand=True)
        
        # Aba Entradas
        frame_entradas = ttk.Frame(cat_notebook)
        cat_notebook.add(frame_entradas, text="💰 Entradas por Categoria")
        
        colunas_entradas = ('Categoria', 'Valor', '%', 'Qtd. Movimentos')
        self.tree_entradas_cat = ttk.Treeview(
            frame_entradas,
            columns=colunas_entradas,
            show='headings',
            height=10
        )
        
        for col in colunas_entradas:
            self.tree_entradas_cat.heading(col, text=col)
        
        self.tree_entradas_cat.column('Categoria', width=200)
        self.tree_entradas_cat.column('Valor', width=150)
        self.tree_entradas_cat.column('%', width=100)
        self.tree_entradas_cat.column('Qtd. Movimentos', width=120)
        
        self.tree_entradas_cat.pack(fill='both', expand=True)
        
        # Aba Saídas
        frame_saidas = ttk.Frame(cat_notebook)
        cat_notebook.add(frame_saidas, text="📉 Saídas por Categoria")
        
        colunas_saidas = ('Categoria', 'Valor', '%', 'Qtd. Movimentos')
        self.tree_saidas_cat = ttk.Treeview(
            frame_saidas,
            columns=colunas_saidas,
            show='headings',
            height=10
        )
        
        for col in colunas_saidas:
            self.tree_saidas_cat.heading(col, text=col)
        
        self.tree_saidas_cat.column('Categoria', width=200)
        self.tree_saidas_cat.column('Valor', width=150)
        self.tree_saidas_cat.column('%', width=100)
        self.tree_saidas_cat.column('Qtd. Movimentos', width=120)
        
        self.tree_saidas_cat.pack(fill='both', expand=True)
    
    def criar_aba_conciliacao(self, parent):
        """Aba de Conciliação Bancária"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame de instruções
        frame_instrucoes = tk.Frame(frame, bg='#f8f9fa', height=40)
        frame_instrucoes.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            frame_instrucoes,
            text="Conciliação Bancária - Selecione os lançamentos conciliados",
            font=("Arial", 11),
            fg=Estilos.COR_TEXTO_SECUNDARIO,
            bg='#f8f9fa'
        ).pack(pady=10)
        
        # Frame de ações
        frame_acoes = tk.Frame(frame, bg='white', height=50)
        frame_acoes.pack(fill='x', pady=(0, 10))
        
        btn_conciliar_frame, btn_conciliar = Estilos.criar_botao_moderno(
            frame_acoes,
            "Conciliar Selecionados",
            self.conciliar_lancamentos,
            tipo='sucesso',
            icone="✅"
        )
        btn_conciliar_frame.pack(side='left', padx=5)
        
        # Tabela de conciliação
        frame_tabela = tk.Frame(frame, bg='white')
        frame_tabela.pack(fill='both', expand=True)
        
        colunas = ('Data', 'Descrição', 'Valor', 'Tipo', 'Status', 'Selecionar')
        self.tree_conciliacao = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show='headings',
            height=12
        )
        
        for col in colunas:
            self.tree_conciliacao.heading(col, text=col)
        
        self.tree_conciliacao.column('Data', width=100)
        self.tree_conciliacao.column('Descrição', width=300)
        self.tree_conciliacao.column('Valor', width=120)
        self.tree_conciliacao.column('Tipo', width=80)
        self.tree_conciliacao.column('Status', width=100)
        self.tree_conciliacao.column('Selecionar', width=80)
        
        self.tree_conciliacao.pack(fill='both', expand=True)
        
        # Carregar dados de conciliação
        self.carregar_conciliacao()
    
    def carregar_conciliacao(self):
        """Carrega dados para conciliação bancária"""
        for item in self.tree_conciliacao.get_children():
            self.tree_conciliacao.delete(item)
        
        # Mostrar apenas movimentos pendentes
        for mov in self.movimentacoes:
            if mov['status'] == 'pendente':
                self.tree_conciliacao.insert('', 'end', values=(
                    mov['data'],
                    mov['descricao'],
                    f"R$ {mov['valor']:.2f}",
                    mov['tipo'].upper(),
                    mov['status'].upper(),
                    "☐"
                ))
    
    def calcular_resumo(self):
        """Calcula os resumos financeiros"""
        hoje = datetime.now()
        inicio_mes = hoje.replace(day=1)
        
        total_entradas_mes = 0
        total_saidas_mes = 0
        saldo = 0
        
        for mov in self.movimentacoes:
            try:
                data_mov = datetime.strptime(mov['data'], '%d/%m/%Y')
                
                if mov['tipo'] == 'entrada':
                    saldo += mov['valor']
                    if data_mov >= inicio_mes:
                        total_entradas_mes += mov['valor']
                else:
                    saldo -= mov['valor']
                    if data_mov >= inicio_mes:
                        total_saidas_mes += mov['valor']
            except:
                continue
        
        self.saldo_atual = saldo
        
        # Atualizar cards
        self.card_saldo.lbl_valor.config(text=f"R$ {saldo:.2f}")
        self.card_entradas.lbl_valor.config(text=f"R$ {total_entradas_mes:.2f}")
        self.card_saidas.lbl_valor.config(text=f"R$ {total_saidas_mes:.2f}")
        
        # Calcular projeção
        if self.movimentacoes:
            total_entradas = sum(m['valor'] for m in self.movimentacoes if m['tipo'] == 'entrada')
            total_dias = len(set(m['data'] for m in self.movimentacoes))
            media_diaria_entrada = total_entradas / max(total_dias, 1)
            
            total_saidas = sum(m['valor'] for m in self.movimentacoes if m['tipo'] == 'saida')
            media_diaria_saida = total_saidas / max(total_dias, 1)
            
            projecao = saldo + (media_diaria_entrada - media_diaria_saida) * 30
            self.card_projetado.lbl_valor.config(text=f"R$ {projecao:.2f}")
    
    def atualizar_fluxo_direto(self):
        """Atualiza a tabela de fluxo de caixa direto"""
        for item in self.tree_movimentos.get_children():
            self.tree_movimentos.delete(item)
        
        dias = int(self.periodo_var.get())
        hoje = datetime.now()
        data_limite = hoje - timedelta(days=dias)
        
        saldo_acumulado = 0
        total_periodo = 0
        
        # Filtrar e ordenar movimentações
        movimentos_periodo = []
        for mov in self.movimentacoes:
            try:
                data_mov = datetime.strptime(mov['data'], '%d/%m/%Y')
                if data_mov >= data_limite:
                    movimentos_periodo.append(mov)
            except:
                continue
        
        movimentos_periodo.sort(key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'))
        
        for mov in movimentos_periodo:
            if mov['tipo'] == 'entrada':
                saldo_acumulado += mov['valor']
                total_periodo += mov['valor']
                tags = ('entrada',)
            else:
                saldo_acumulado -= mov['valor']
                total_periodo -= mov['valor']
                tags = ('saida',)
            
            if mov['status'] == 'pendente':
                tags = tags + ('pendente',)
            elif mov['status'] == 'conciliado':
                tags = tags + ('conciliado',)
            
            self.tree_movimentos.insert('', 'end', values=(
                mov['data'],
                mov['descricao'],
                mov['categoria'],
                mov['tipo'].upper(),
                f"R$ {mov['valor']:.2f}",
                mov['forma_pagamento'],
                f"R$ {saldo_acumulado:.2f}",
                mov['status'].upper()
            ), tags=tags)
        
        self.lbl_total_periodo.config(text=f"Total do período: R$ {total_periodo:.2f}")
        self.lbl_saldo_final.config(text=f"Saldo final: R$ {saldo_acumulado:.2f}")
    
    def atualizar_analise_operacional(self):
        """Atualiza a análise operacional"""
        # Calcular ticket médio
        vendas = [m for m in self.movimentacoes if m['categoria'] == 'Vendas' and m['tipo'] == 'entrada']
        if vendas:
            ticket_medio = sum(m['valor'] for m in vendas) / len(vendas)
        else:
            ticket_medio = 0
        
        # Atualizar gráfico
        self.ax_operacional.clear()
        
        datas = []
        entradas = []
        saidas = []
        
        for i in range(7, 0, -1):
            data = (datetime.now() - timedelta(days=i)).strftime("%d/%m")
            data_completa = (datetime.now() - timedelta(days=i)).strftime("%d/%m/%Y")
            datas.append(data)
            
            entrada_dia = sum(m['valor'] for m in self.movimentacoes 
                            if m['tipo'] == 'entrada' and m['data'] == data_completa)
            saida_dia = sum(m['valor'] for m in self.movimentacoes 
                          if m['tipo'] == 'saida' and m['data'] == data_completa)
            
            entradas.append(entrada_dia)
            saidas.append(saida_dia)
        
        x = range(len(datas))
        self.ax_operacional.bar([i-0.2 for i in x], entradas, width=0.4, label='Entradas', color=self.cor_sucesso, alpha=0.7)
        self.ax_operacional.bar([i+0.2 for i in x], saidas, width=0.4, label='Saídas', color=self.cor_perigo, alpha=0.7)
        
        self.ax_operacional.set_xlabel('Data')
        self.ax_operacional.set_ylabel('Valor (R$)')
        self.ax_operacional.set_title('Fluxo Operacional - Últimos 7 dias')
        self.ax_operacional.set_xticks(x)
        self.ax_operacional.set_xticklabels(datas)
        self.ax_operacional.legend()
        self.ax_operacional.grid(True, alpha=0.3)
        
        self.fig_operacional.tight_layout()
        self.canvas_operacional.draw()
        
        # Atualizar tabela de indicadores
        for item in self.tree_indicadores.get_children():
            self.tree_indicadores.delete(item)
        
        total_entradas = sum(m['valor'] for m in self.movimentacoes if m['tipo'] == 'entrada')
        total_saidas = sum(m['valor'] for m in self.movimentacoes if m['tipo'] == 'saida')
        
        indicadores = [
            ('Ticket Médio', f"R$ {ticket_medio:.2f}", 'Mês atual', '📊'),
            ('Total Entradas', f"R$ {total_entradas:.2f}", 'Acumulado', '📈'),
            ('Total Saídas', f"R$ {total_saidas:.2f}", 'Acumulado', '📉'),
            ('Resultado', f"R$ {self.saldo_atual:.2f}", 'Líquido', '💰'),
        ]
        
        for ind in indicadores:
            self.tree_indicadores.insert('', 'end', values=ind)
    
    def atualizar_projecoes(self):
        """Atualiza as projeções futuras"""
        for item in self.tree_projecoes.get_children():
            self.tree_projecoes.delete(item)
        
        cenario = self.cenario_var.get()
        dias = int(self.projecao_periodo_var.get())
        
        if not self.movimentacoes:
            return
        
        # Calcular médias
        total_entradas = sum(m['valor'] for m in self.movimentacoes if m['tipo'] == 'entrada')
        total_saidas = sum(m['valor'] for m in self.movimentacoes if m['tipo'] == 'saida')
        total_dias = len(set(m['data'] for m in self.movimentacoes))
        
        media_entrada_dia = total_entradas / max(total_dias, 1)
        media_saida_dia = total_saidas / max(total_dias, 1)
        
        # Fatores por cenário
        fatores = {
            'otimista': {'entrada': 1.2, 'saida': 0.9},
            'moderado': {'entrada': 1.0, 'saida': 1.0},
            'pessimista': {'entrada': 0.8, 'saida': 1.1}
        }
        
        fator = fatores.get(cenario, fatores['moderado'])
        
        # Gerar projeções
        saldo_projetado = self.saldo_atual
        datas_proj = []
        saldos_proj = []
        
        for i in range(1, dias + 1):
            data_proj = (datetime.now() + timedelta(days=i)).strftime("%d/%m/%Y")
            
            # Pequena variação para simular realidade
            variacao_entrada = 1 + (i % 5) * 0.02
            variacao_saida = 1 + (i % 3) * 0.01
            
            entrada_proj = media_entrada_dia * fator['entrada'] * variacao_entrada
            saida_proj = media_saida_dia * fator['saida'] * variacao_saida
            
            saldo_projetado += entrada_proj - saida_proj
            
            self.tree_projecoes.insert('', 'end', values=(
                data_proj,
                f"R$ {entrada_proj:.2f}",
                f"R$ {saida_proj:.2f}",
                f"R$ {saldo_projetado:.2f}",
                cenario.capitalize()
            ))
            
            datas_proj.append(data_proj)
            saldos_proj.append(saldo_projetado)
        
        # Atualizar gráfico
        self.ax_projetado.clear()
        self.ax_projetado.plot(range(len(saldos_proj)), saldos_proj, marker='o', color=self.cor_primaria, linewidth=2)
        self.ax_projetado.set_xlabel('Dias')
        self.ax_projetado.set_ylabel('Saldo Projetado (R$)')
        self.ax_projetado.set_title(f'Projeção de Saldo - Cenário {cenario.capitalize()}')
        self.ax_projetado.grid(True, alpha=0.3)
        
        step = max(1, dias // 10)
        self.ax_projetado.set_xticks(range(0, dias, step))
        self.ax_projetado.set_xticklabels([str(i+1) for i in range(0, dias, step)])
        
        self.fig_projetado.tight_layout()
        self.canvas_projetado.draw()
    
    def atualizar_analise_categorias(self):
        """Atualiza a análise por categorias"""
        for item in self.tree_entradas_cat.get_children():
            self.tree_entradas_cat.delete(item)
        
        for item in self.tree_saidas_cat.get_children():
            self.tree_saidas_cat.delete(item)
        
        # Agrupar por categoria
        categorias_entradas = {}
        categorias_saidas = {}
        total_entradas = 0
        total_saidas = 0
        
        for mov in self.movimentacoes:
            if mov['tipo'] == 'entrada':
                cat = mov['categoria']
                categorias_entradas[cat] = categorias_entradas.get(cat, 0) + mov['valor']
                total_entradas += mov['valor']
            else:
                cat = mov['categoria']
                categorias_saidas[cat] = categorias_saidas.get(cat, 0) + mov['valor']
                total_saidas += mov['valor']
        
        # Preencher tabelas
        for cat, valor in sorted(categorias_entradas.items(), key=lambda x: x[1], reverse=True):
            percentual = (valor / total_entradas * 100) if total_entradas > 0 else 0
            qtd = len([m for m in self.movimentacoes if m['categoria'] == cat and m['tipo'] == 'entrada'])
            self.tree_entradas_cat.insert('', 'end', values=(
                cat,
                f"R$ {valor:.2f}",
                f"{percentual:.1f}%",
                qtd
            ))
        
        for cat, valor in sorted(categorias_saidas.items(), key=lambda x: x[1], reverse=True):
            percentual = (valor / total_saidas * 100) if total_saidas > 0 else 0
            qtd = len([m for m in self.movimentacoes if m['categoria'] == cat and m['tipo'] == 'saida'])
            self.tree_saidas_cat.insert('', 'end', values=(
                cat,
                f"R$ {valor:.2f}",
                f"{percentual:.1f}%",
                qtd
            ))
        
        # Gráficos de pizza
        self.ax_entradas.clear()
        if categorias_entradas:
            labels = list(categorias_entradas.keys())
            sizes = list(categorias_entradas.values())
            self.ax_entradas.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            self.ax_entradas.set_title('Entradas por Categoria')
        else:
            self.ax_entradas.text(0.5, 0.5, 'Sem dados', ha='center', va='center')
        
        self.ax_saidas.clear()
        if categorias_saidas:
            labels = list(categorias_saidas.keys())
            sizes = list(categorias_saidas.values())
            self.ax_saidas.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            self.ax_saidas.set_title('Saídas por Categoria')
        else:
            self.ax_saidas.text(0.5, 0.5, 'Sem dados', ha='center', va='center')
        
        self.fig_categorias.tight_layout()
        self.canvas_categorias.draw()
    
    def nova_movimentacao(self):
        """Abre diálogo para nova movimentação financeira"""
        dialog = tk.Toplevel(self.janela)
        dialog.title("Nova Movimentação")
        dialog.geometry("550x650")
        dialog.configure(bg='white')
        dialog.transient(self.janela)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (550 // 2)
        y = (dialog.winfo_screenheight() // 2) - (650 // 2)
        dialog.geometry(f'{550}x{650}+{x}+{y}')
        
        frame = tk.Frame(dialog, bg='white', padx=25, pady=20)
        frame.pack(fill='both', expand=True)
        
        tk.Label(
            frame,
            text="NOVA MOVIMENTAÇÃO FINANCEIRA",
            font=("Arial", 16, "bold"),
            fg=self.cor_primaria,
            bg='white'
        ).pack(pady=(0, 20))
        
        # Campos do formulário
        entries = {}
        
        # Data
        tk.Label(frame, text="Data (DD/MM/AAAA):", font=("Arial", 10, "bold"),
                fg=Estilos.COR_TEXTO, bg='white').pack(anchor='w', pady=(10, 2))
        data_entry = tk.Entry(frame, font=("Arial", 10), relief='solid', bd=1)
        data_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        data_entry.pack(fill='x', pady=(0, 5), ipady=5)
        entries['data'] = data_entry
        
        # Descrição
        tk.Label(frame, text="Descrição:", font=("Arial", 10, "bold"),
                fg=Estilos.COR_TEXTO, bg='white').pack(anchor='w', pady=(10, 2))
        desc_entry = tk.Entry(frame, font=("Arial", 10), relief='solid', bd=1)
        desc_entry.pack(fill='x', pady=(0, 5), ipady=5)
        entries['descricao'] = desc_entry
        
        # Categoria
        tk.Label(frame, text="Categoria:", font=("Arial", 10, "bold"),
                fg=Estilos.COR_TEXTO, bg='white').pack(anchor='w', pady=(10, 2))
        cat_combo = ttk.Combobox(
            frame,
            values=["Vendas", "Compras", "Despesas Fixas", "Despesas Variáveis", 
                   "Investimentos", "Retirada", "Empréstimo", "Outros"],
            state='readonly',
            font=("Arial", 10)
        )
        cat_combo.set("Vendas")
        cat_combo.pack(fill='x', pady=(0, 5), ipady=3)
        entries['categoria'] = cat_combo
        
        # Tipo
        tk.Label(frame, text="Tipo:", font=("Arial", 10, "bold"),
                fg=Estilos.COR_TEXTO, bg='white').pack(anchor='w', pady=(10, 2))
        tipo_combo = ttk.Combobox(
            frame,
            values=["entrada", "saida"],
            state='readonly',
            font=("Arial", 10)
        )
        tipo_combo.set("entrada")
        tipo_combo.pack(fill='x', pady=(0, 5), ipady=3)
        entries['tipo'] = tipo_combo
        
        # Valor
        tk.Label(frame, text="Valor (R$):", font=("Arial", 10, "bold"),
                fg=Estilos.COR_TEXTO, bg='white').pack(anchor='w', pady=(10, 2))
        valor_entry = tk.Entry(frame, font=("Arial", 10), relief='solid', bd=1)
        valor_entry.pack(fill='x', pady=(0, 5), ipady=5)
        entries['valor'] = valor_entry
        
        # Forma de Pagamento
        tk.Label(frame, text="Forma de Pagamento:", font=("Arial", 10, "bold"),
                fg=Estilos.COR_TEXTO, bg='white').pack(anchor='w', pady=(10, 2))
        forma_combo = ttk.Combobox(
            frame,
            values=["Dinheiro", "Cartão", "PIX", "Boleto", "Débito", "Transferência"],
            state='readonly',
            font=("Arial", 10)
        )
        forma_combo.set("Dinheiro")
        forma_combo.pack(fill='x', pady=(0, 5), ipady=3)
        entries['forma_pagamento'] = forma_combo
        
        # Status
        tk.Label(frame, text="Status:", font=("Arial", 10, "bold"),
                fg=Estilos.COR_TEXTO, bg='white').pack(anchor='w', pady=(10, 2))
        status_combo = ttk.Combobox(
            frame,
            values=["conciliado", "pendente"],
            state='readonly',
            font=("Arial", 10)
        )
        status_combo.set("pendente")
        status_combo.pack(fill='x', pady=(0, 5), ipady=3)
        entries['status'] = status_combo
        
        # Frame para botões (AGORA VISÍVEL)
        frame_botoes = tk.Frame(frame, bg='white', pady=25)
        frame_botoes.pack(fill='x', side='bottom')
        
        def salvar_movimentacao():
            try:
                nova_mov = {
                    'data': entries['data'].get(),
                    'descricao': entries['descricao'].get(),
                    'categoria': entries['categoria'].get(),
                    'tipo': entries['tipo'].get(),
                    'valor': float(entries['valor'].get().replace(',', '.')),
                    'forma_pagamento': entries['forma_pagamento'].get(),
                    'status': entries['status'].get()
                }
                
                # Validar
                if not all([nova_mov['data'], nova_mov['descricao'], nova_mov['categoria'], 
                           nova_mov['tipo'], nova_mov['valor'], nova_mov['forma_pagamento']]):
                    messagebox.showerror("Erro", "Preencha todos os campos!")
                    return
                
                # Adicionar à lista
                self.movimentacoes.insert(0, nova_mov)
                
                # Recalcular tudo
                self.calcular_resumo()
                self.atualizar_fluxo_direto()
                self.atualizar_analise_operacional()
                self.atualizar_projecoes()
                self.atualizar_analise_categorias()
                self.carregar_conciliacao()
                
                messagebox.showinfo("Sucesso", "Movimentação adicionada com sucesso!")
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")
        
        # Botão Salvar
        btn_salvar_frame, btn_salvar = Estilos.criar_botao_moderno(
            frame_botoes,
            "Salvar Movimentação",
            salvar_movimentacao,
            tipo='primario',
            icone="✅"
        )
        btn_salvar_frame.pack(side='left', padx=5, expand=True, fill='x')
        
        # Botão Cancelar
        btn_cancelar_frame, btn_cancelar = Estilos.criar_botao_moderno(
            frame_botoes,
            "Cancelar",
            dialog.destroy,
            tipo='secundario',
            icone="✖"
        )
        btn_cancelar_frame.pack(side='left', padx=5, expand=True, fill='x')
    
    def conciliar_lancamentos(self):
        """Simula conciliação de lançamentos selecionados"""
        messagebox.showinfo("Conciliação", 
                          "Funcionalidade de conciliação em desenvolvimento.\n\n"
                          "Na versão final, você poderá selecionar lançamentos e marcá-los como conciliados.")
    
    def voltar(self):
        """Volta para o menu principal"""
        self.db.fechar_conexao()
        self.janela.destroy()
        self.menu_principal.deiconify()