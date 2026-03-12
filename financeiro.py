# financeiro.py - Módulo de Gestão Financeira
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
        self.janela.geometry("1200x700")
        self.janela.resizable(False, False)
        self.janela.configure(bg='#f5f5f5')  # Fundo cinza claro
        
        # Cores (usando Estilos)
        self.cor_primaria = Estilos.COR_PRIMARIA
        self.cor_sucesso = Estilos.COR_SUCESSO
        self.cor_perigo = Estilos.COR_PERIGO
        self.cor_alerta = Estilos.COR_ALERTA
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 1200
        altura = 700
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        self.criar_interface()
        self.atualizar_dados()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)
        self.janela.mainloop()
    
    def criar_interface(self):
        # Frame branco principal (card)
        frame_conteudo = tk.Frame(
            self.janela,
            bg='white',
            highlightbackground=Estilos.COR_BORDA,
            highlightthickness=1,
            bd=0
        )
        frame_conteudo.pack(expand=True, fill='both', padx=20, pady=20)
        
        # ===== CABEÇALHO =====
        frame_cabecalho = tk.Frame(frame_conteudo, bg='white', height=80)
        frame_cabecalho.pack(fill='x', padx=20, pady=(10, 5))
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
        data_atual = datetime.now().strftime("%d/%m/%Y")
        tk.Label(
            frame_cabecalho,
            text=f"📅 {data_atual}",
            font=("Arial", 12),
            fg=Estilos.COR_TEXTO_SECUNDARIO,
            bg='white'
        ).pack(side='right', padx=20)
        
        # ===== BOTÃO VOLTAR =====
        btn_voltar_frame, btn_voltar = Estilos.criar_botao_moderno(
            frame_cabecalho,
            "Voltar",
            self.voltar,
            tipo='secundario',
            icone="↩️"
        )
        btn_voltar_frame.pack(side='right', padx=10)
        
        # ===== INDICADORES PRINCIPAIS (CARDS) =====
        frame_indicadores = tk.Frame(frame_conteudo, bg='white', height=120)
        frame_indicadores.pack(fill='x', padx=20, pady=10)
        frame_indicadores.pack_propagate(False)
        
        for i in range(4):
            frame_indicadores.columnconfigure(i, weight=1)
        
        # Buscar dados financeiros
        dados = self.calcular_indicadores()
        
        # Card 1 - Saldo Atual
        self.card_saldo = self.criar_card_financeiro(
            frame_indicadores,
            "Saldo Atual",
            f"R$ {dados['saldo']:.2f}",
            "disponível",
            "💵",
            self.cor_primaria,
            0
        )
        
        # Card 2 - Receitas do Mês
        self.card_receitas = self.criar_card_financeiro(
            frame_indicadores,
            "Receitas do Mês",
            f"R$ {dados['receitas_mes']:.2f}",
            "entradas",
            "📈",
            self.cor_sucesso,
            1
        )
        
        # Card 3 - Despesas do Mês
        self.card_despesas = self.criar_card_financeiro(
            frame_indicadores,
            "Despesas do Mês",
            f"R$ {dados['despesas_mes']:.2f}",
            "saídas",
            "📉",
            self.cor_perigo,
            2
        )
        
        # Card 4 - Lucro Líquido
        lucro = dados['receitas_mes'] - dados['despesas_mes']
        cor_lucro = self.cor_sucesso if lucro >= 0 else self.cor_perigo
        self.card_lucro = self.criar_card_financeiro(
            frame_indicadores,
            "Lucro Líquido",
            f"R$ {lucro:.2f}",
            "resultado do mês",
            "📊",
            cor_lucro,
            3
        )
        
        # ===== NOTEBOOK COM ABAS =====
        self.notebook = ttk.Notebook(frame_conteudo)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        Estilos.aplicar_estilo_notebook(self.notebook)
        
        # ABA 1: Fluxo de Caixa
        frame_fluxo = ttk.Frame(self.notebook)
        self.notebook.add(frame_fluxo, text="📊 Fluxo de Caixa")
        self.criar_aba_fluxo(frame_fluxo)
        
        # ABA 2: Contas a Pagar
        frame_pagar = ttk.Frame(self.notebook)
        self.notebook.add(frame_pagar, text="💳 Contas a Pagar")
        self.criar_aba_pagar(frame_pagar)
        
        # ABA 3: Contas a Receber
        frame_receber = ttk.Frame(self.notebook)
        self.notebook.add(frame_receber, text="💰 Contas a Receber")
        self.criar_aba_receber(frame_receber)
        
        # ABA 4: Relatórios Financeiros
        frame_relatorios = ttk.Frame(self.notebook)
        self.notebook.add(frame_relatorios, text="📑 Relatórios")
        self.criar_aba_relatorios(frame_relatorios)
    
    def criar_card_financeiro(self, parent, titulo, valor, subtitulo, icone, cor, coluna):
        """Cria um card financeiro no estilo moderno"""
        card = tk.Frame(
            parent,
            bg='white',
            highlightbackground=Estilos.COR_BORDA,
            highlightthickness=1,
            bd=0,
            width=250,
            height=100
        )
        card.grid(row=0, column=coluna, padx=10, pady=5, sticky='nsew')
        card.grid_propagate(False)
        
        # Layout do card
        frame_info = tk.Frame(card, bg='white', padx=12, pady=8)
        frame_info.pack(side='left', fill='both', expand=True)
        
        tk.Label(
            frame_info,
            text=titulo,
            font=("Arial", 10),
            fg=Estilos.COR_TEXTO_SECUNDARIO,
            bg='white'
        ).pack(anchor='w')
        
        tk.Label(
            frame_info,
            text=valor,
            font=("Arial", 16, "bold"),
            fg=cor,
            bg='white'
        ).pack(anchor='w', pady=(2, 0))
        
        tk.Label(
            frame_info,
            text=subtitulo,
            font=("Arial", 8),
            fg='#999999',
            bg='white'
        ).pack(anchor='w')
        
        frame_icone = tk.Frame(card, bg='white', width=50)
        frame_icone.pack(side='right', fill='y', padx=(0, 10))
        
        tk.Label(
            frame_icone,
            text=icone,
            font=("Arial", 24),
            fg=cor,
            bg='white'
        ).pack(expand=True)
        
        return card
    
    def criar_aba_fluxo(self, parent):
        """Cria a aba de fluxo de caixa com gráfico"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame superior com filtros
        frame_filtros = tk.Frame(frame, bg='white', height=50)
        frame_filtros.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            frame_filtros,
            text="Período:",
            font=("Arial", 10),
            bg='white'
        ).pack(side='left', padx=(0, 10))
        
        self.periodo_var = tk.StringVar(value="30")
        periodo_combo = ttk.Combobox(
            frame_filtros,
            textvariable=self.periodo_var,
            values=["7", "15", "30", "60", "90"],
            font=("Arial", 10),
            width=10,
            state='readonly'
        )
        periodo_combo.pack(side='left', padx=(0, 10))
        periodo_combo.bind('<<ComboboxSelected>>', lambda e: self.atualizar_grafico())
        
        tk.Label(
            frame_filtros,
            text="dias",
            font=("Arial", 10),
            bg='white'
        ).pack(side='left')
        
        # Frame do gráfico
        frame_grafico = tk.Frame(frame, bg='white', height=300)
        frame_grafico.pack(fill='both', expand=True, pady=10)
        
        # Criar figura do matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_grafico)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Frame da tabela de movimentações
        frame_tabela = tk.Frame(frame, bg='white', height=200)
        frame_tabela.pack(fill='both', expand=True, pady=(10, 0))
        
        # Treeview para últimas movimentações
        colunas = ('Data', 'Descrição', 'Tipo', 'Categoria', 'Valor', 'Status')
        self.tree_movimentos = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show='headings',
            height=8
        )
        
        for col in colunas:
            self.tree_movimentos.heading(col, text=col)
        
        self.tree_movimentos.column('Data', width=100)
        self.tree_movimentos.column('Descrição', width=250)
        self.tree_movimentos.column('Tipo', width=100)
        self.tree_movimentos.column('Categoria', width=150)
        self.tree_movimentos.column('Valor', width=120)
        self.tree_movimentos.column('Status', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabela, orient='vertical', command=self.tree_movimentos.yview)
        self.tree_movimentos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_movimentos.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Tags para cores
        self.tree_movimentos.tag_configure('entrada', foreground=self.cor_sucesso)
        self.tree_movimentos.tag_configure('saida', foreground=self.cor_perigo)
        
        self.atualizar_grafico()
    
    def criar_aba_pagar(self, parent):
        """Cria a aba de contas a pagar"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame de botões
        frame_botoes = tk.Frame(frame, bg='white', height=50)
        frame_botoes.pack(fill='x', pady=(0, 10))
        
        btn_novo_frame, btn_novo = Estilos.criar_botao_moderno(
            frame_botoes,
            "Nova Conta",
            self.nova_conta_pagar,
            tipo='primario',
            icone="➕"
        )
        btn_novo_frame.pack(side='left', padx=5)
        
        btn_pagar_frame, btn_pagar = Estilos.criar_botao_moderno(
            frame_botoes,
            "Baixar Selecionada",
            self.baixar_conta,
            tipo='sucesso',
            icone="✅"
        )
        btn_pagar_frame.pack(side='left', padx=5)
        
        # Treeview de contas a pagar
        colunas = ('ID', 'Descrição', 'Fornecedor', 'Vencimento', 'Valor', 'Dias', 'Status')
        self.tree_pagar = ttk.Treeview(
            frame,
            columns=colunas,
            show='headings',
            height=15
        )
        
        for col in colunas:
            self.tree_pagar.heading(col, text=col)
        
        self.tree_pagar.column('ID', width=60)
        self.tree_pagar.column('Descrição', width=250)
        self.tree_pagar.column('Fornecedor', width=200)
        self.tree_pagar.column('Vencimento', width=100)
        self.tree_pagar.column('Valor', width=120)
        self.tree_pagar.column('Dias', width=80)
        self.tree_pagar.column('Status', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree_pagar.yview)
        self.tree_pagar.configure(yscrollcommand=scrollbar.set)
        
        self.tree_pagar.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Tags para status
        self.tree_pagar.tag_configure('vencido', background='#ffe5e5')
        self.tree_pagar.tag_configure('hoje', background='#fff3e0')
        self.tree_pagar.tag_configure('pago', foreground='#999999')
        
        self.carregar_contas_pagar()
    
    def criar_aba_receber(self, parent):
        """Cria a aba de contas a receber"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame de botões
        frame_botoes = tk.Frame(frame, bg='white', height=50)
        frame_botoes.pack(fill='x', pady=(0, 10))
        
        btn_novo_frame, btn_novo = Estilos.criar_botao_moderno(
            frame_botoes,
            "Nova Conta",
            self.nova_conta_receber,
            tipo='primario',
            icone="➕"
        )
        btn_novo_frame.pack(side='left', padx=5)
        
        btn_receber_frame, btn_receber = Estilos.criar_botao_moderno(
            frame_botoes,
            "Receber",
            self.receber_conta,
            tipo='sucesso',
            icone="💰"
        )
        btn_receber_frame.pack(side='left', padx=5)
        
        # Treeview de contas a receber
        colunas = ('ID', 'Descrição', 'Cliente', 'Vencimento', 'Valor', 'Dias', 'Status')
        self.tree_receber = ttk.Treeview(
            frame,
            columns=colunas,
            show='headings',
            height=15
        )
        
        for col in colunas:
            self.tree_receber.heading(col, text=col)
        
        self.tree_receber.column('ID', width=60)
        self.tree_receber.column('Descrição', width=250)
        self.tree_receber.column('Cliente', width=200)
        self.tree_receber.column('Vencimento', width=100)
        self.tree_receber.column('Valor', width=120)
        self.tree_receber.column('Dias', width=80)
        self.tree_receber.column('Status', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree_receber.yview)
        self.tree_receber.configure(yscrollcommand=scrollbar.set)
        
        self.tree_receber.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Tags para status
        self.tree_receber.tag_configure('vencido', background='#ffe5e5')
        self.tree_receber.tag_configure('hoje', background='#fff3e0')
        self.tree_receber.tag_configure('recebido', foreground='#999999')
        
        self.carregar_contas_receber()
    
    def criar_aba_relatorios(self, parent):
        """Cria a aba de relatórios financeiros"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame de opções
        frame_opcoes = tk.Frame(frame, bg='white', width=250)
        frame_opcoes.pack(side='left', fill='y', padx=(0, 10))
        
        tk.Label(
            frame_opcoes,
            text="RELATÓRIOS",
            font=("Arial", 14, "bold"),
            fg=self.cor_primaria,
            bg='white'
        ).pack(pady=10)
        
        relatorios = [
            ("📊 Fluxo de Caixa", self.gerar_relatorio_fluxo),
            ("📈 DRE", self.gerar_relatorio_dre),
            ("📉 Contas a Pagar", self.gerar_relatorio_pagar),
            ("💰 Contas a Receber", self.gerar_relatorio_receber),
            ("📅 Fluxo Projetado", self.gerar_relatorio_projetado)
        ]
        
        for texto, comando in relatorios:
            btn_frame, btn = Estilos.criar_botao_moderno(
                frame_opcoes,
                texto,
                comando,
                tipo='secundario'
            )
            btn_frame.pack(pady=5)
        
        # Área de visualização do relatório
        frame_visualizacao = tk.Frame(frame, bg='white', relief='solid', bd=1)
        frame_visualizacao.pack(side='right', fill='both', expand=True)
        
        self.texto_relatorio = tk.Text(
            frame_visualizacao,
            font=("Courier", 10),
            bg='white',
            wrap='word',
            padx=10,
            pady=10
        )
        self.texto_relatorio.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.texto_relatorio)
        scrollbar.pack(side='right', fill='y')
        self.texto_relatorio.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.texto_relatorio.yview)
    
    def calcular_indicadores(self):
        """Calcula os indicadores financeiros"""
        # Dados simulados (depois implementar com banco real)
        return {
            'saldo': 15750.80,
            'receitas_mes': 23450.00,
            'despesas_mes': 12580.50
        }
    
    def atualizar_grafico(self):
        """Atualiza o gráfico de fluxo de caixa"""
        dias = int(self.periodo_var.get())
        
        # Dados simulados
        datas = [(datetime.now() - timedelta(days=i)).strftime("%d/%m") for i in range(dias-1, -1, -1)]
        entradas = [1000 + i * 50 + (i % 3) * 200 for i in range(dias)]
        saidas = [800 + i * 30 + (i % 4) * 150 for i in range(dias)]
        
        self.ax.clear()
        
        # Plotar gráfico
        x = range(len(datas))
        self.ax.plot(x, entradas, marker='o', color=self.cor_sucesso, linewidth=2, label='Entradas')
        self.ax.plot(x, saidas, marker='s', color=self.cor_perigo, linewidth=2, label='Saídas')
        
        # Configurar
        self.ax.set_xlabel('Data', fontsize=10)
        self.ax.set_ylabel('Valor (R$)', fontsize=10)
        self.ax.set_title(f'Fluxo de Caixa - Últimos {dias} dias', fontsize=12, fontweight='bold')
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
        
        # Ajustar rótulos do eixo x
        step = max(1, dias // 10)
        self.ax.set_xticks(x[::step])
        self.ax.set_xticklabels(datas[::step], rotation=45)
        
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Carregar movimentações
        self.carregar_movimentacoes()
    
    def carregar_movimentacoes(self):
        """Carrega as últimas movimentações"""
        for item in self.tree_movimentos.get_children():
            self.tree_movimentos.delete(item)
        
        # Dados simulados
        movimentos = [
            ("15/03/2025", "Venda #1245 - Cliente A", "Entrada", "Vendas", "R$ 1.250,00", "Confirmado"),
            ("15/03/2025", "Compra Fornecedor X", "Saída", "Compras", "R$ 890,00", "Pago"),
            ("14/03/2025", "Venda #1244 - Cliente B", "Entrada", "Vendas", "R$ 2.300,00", "Confirmado"),
            ("14/03/2025", "Pagamento Energia", "Saída", "Despesas Fixas", "R$ 350,00", "Pago"),
            ("13/03/2025", "Venda #1243 - Cliente C", "Entrada", "Vendas", "R$ 890,00", "Confirmado"),
            ("13/03/2025", "Aluguel", "Saída", "Despesas Fixas", "R$ 1.500,00", "Pago"),
        ]
        
        for mov in movimentos:
            tags = ('entrada',) if mov[2] == 'Entrada' else ('saida',)
            self.tree_movimentos.insert('', 'end', values=mov, tags=tags)
    
    def carregar_contas_pagar(self):
        """Carrega as contas a pagar"""
        for item in self.tree_pagar.get_children():
            self.tree_pagar.delete(item)
        
        # Dados simulados
        contas = [
            (1, "Compra de Mercadorias", "Fornecedor ABC", "20/03/2025", "R$ 3.500,00", "5 dias", "A Pagar"),
            (2, "Aluguel", "Imobiliária XP", "25/03/2025", "R$ 2.000,00", "10 dias", "A Pagar"),
            (3, "Energia Elétrica", "Cemig", "18/03/2025", "R$ 450,00", "3 dias", "A Pagar"),
            (4, "Água", "Copasa", "15/03/2025", "R$ 180,00", "0 dias", "Vence Hoje"),
            (5, "Internet", "Vivo", "10/03/2025", "R$ 200,00", "-5 dias", "Vencido"),
            (6, "Telefone", "Claro", "05/03/2025", "R$ 150,00", "-10 dias", "Vencido"),
        ]
        
        for conta in contas:
            tags = []
            if conta[6] == "Vencido":
                tags = ('vencido',)
            elif conta[6] == "Vence Hoje":
                tags = ('hoje',)
            self.tree_pagar.insert('', 'end', values=conta, tags=tags)
    
    def carregar_contas_receber(self):
        """Carrega as contas a receber"""
        for item in self.tree_receber.get_children():
            self.tree_receber.delete(item)
        
        # Dados simulados
        contas = [
            (1, "Venda #1245", "Cliente A", "22/03/2025", "R$ 1.250,00", "7 dias", "A Receber"),
            (2, "Venda #1244", "Cliente B", "25/03/2025", "R$ 2.300,00", "10 dias", "A Receber"),
            (3, "Venda #1243", "Cliente C", "18/03/2025", "R$ 890,00", "3 dias", "A Receber"),
            (4, "Venda #1242", "Cliente D", "15/03/2025", "R$ 450,00", "0 dias", "Vence Hoje"),
            (5, "Venda #1241", "Cliente E", "10/03/2025", "R$ 1.800,00", "-5 dias", "Vencido"),
        ]
        
        for conta in contas:
            tags = []
            if conta[6] == "Vencido":
                tags = ('vencido',)
            elif conta[6] == "Vence Hoje":
                tags = ('hoje',)
            self.tree_receber.insert('', 'end', values=conta, tags=tags)
    
    def atualizar_dados(self):
        """Atualiza todos os dados da tela"""
        # Atualizar cards
        dados = self.calcular_indicadores()
        lucro = dados['receitas_mes'] - dados['despesas_mes']
        cor_lucro = self.cor_sucesso if lucro >= 0 else self.cor_perigo
        
        self.atualizar_card(self.card_saldo, f"R$ {dados['saldo']:.2f}")
        self.atualizar_card(self.card_receitas, f"R$ {dados['receitas_mes']:.2f}")
        self.atualizar_card(self.card_despesas, f"R$ {dados['despesas_mes']:.2f}")
        self.atualizar_card(self.card_lucro, f"R$ {lucro:.2f}")
    
    def atualizar_card(self, card, novo_valor):
        """Atualiza o valor de um card"""
        for widget in card.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):  # frame_info
                        for label in child.winfo_children():
                            if isinstance(label, tk.Label):
                                if label.cget('font')[1] == 16:  # valor
                                    label.config(text=novo_valor)
    
    def nova_conta_pagar(self):
        """Abre diálogo para nova conta a pagar"""
        messagebox.showinfo("Nova Conta", "Funcionalidade em desenvolvimento!")
    
    def nova_conta_receber(self):
        """Abre diálogo para nova conta a receber"""
        messagebox.showinfo("Nova Conta", "Funcionalidade em desenvolvimento!")
    
    def baixar_conta(self):
        """Baixa uma conta selecionada"""
        messagebox.showinfo("Baixar Conta", "Funcionalidade em desenvolvimento!")
    
    def receber_conta(self):
        """Registra recebimento de conta"""
        messagebox.showinfo("Receber", "Funcionalidade em desenvolvimento!")
    
    def gerar_relatorio_fluxo(self):
        """Gera relatório de fluxo de caixa"""
        relatorio = "=" * 60 + "\n"
        relatorio += " " * 18 + "RELATÓRIO DE FLUXO DE CAIXA\n"
        relatorio += "=" * 60 + "\n\n"
        
        relatorio += f"Período: Últimos {self.periodo_var.get()} dias\n"
        relatorio += f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        relatorio += f"{'Data':<12} {'Entradas':>15} {'Saídas':>15} {'Saldo':>15}\n"
        relatorio += "-" * 57 + "\n"
        
        # Dados simulados
        saldo = 0
        for i in range(7):
            data = (datetime.now() - timedelta(days=6-i)).strftime("%d/%m/%Y")
            entrada = 1500 + i * 50
            saida = 1200 + i * 30
            saldo += entrada - saida
            relatorio += f"{data:<12} R${entrada:>13.2f} R${saida:>13.2f} R${saldo:>13.2f}\n"
        
        relatorio += "-" * 57 + "\n"
        relatorio += f"{'TOTAIS:':<12} R${self.calcular_indicadores()['receitas_mes']:>13.2f} R${self.calcular_indicadores()['despesas_mes']:>13.2f} R${self.calcular_indicadores()['saldo']:>13.2f}\n"
        
        self.texto_relatorio.delete('1.0', tk.END)
        self.texto_relatorio.insert('1.0', relatorio)
    
    def gerar_relatorio_dre(self):
        """Gera relatório DRE (Demonstração de Resultados)"""
        relatorio = "=" * 60 + "\n"
        relatorio += " " * 18 + "DEMONSTRAÇÃO DE RESULTADOS\n"
        relatorio += "=" * 60 + "\n\n"
        
        relatorio += f"Período: Março/2025\n"
        relatorio += f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        receitas = 23450.00
        deducoes = 2345.00
        receita_liquida = receitas - deducoes
        
        custos = 8900.00
        lucro_bruto = receita_liquida - custos
        
        despesas = 3650.50
        lucro_operacional = lucro_bruto - despesas
        
        impostos = lucro_operacional * 0.15
        lucro_liquido = lucro_operacional - impostos
        
        relatorio += "RECEITAS:\n"
        relatorio += f"  Receita Bruta:          R$ {receitas:>13.2f}\n"
        relatorio += f"  (-) Deduções:           R$ {deducoes:>13.2f}\n"
        relatorio += f"  (=) Receita Líquida:    R$ {receita_liquida:>13.2f}\n\n"
        
        relatorio += "CUSTOS:\n"
        relatorio += f"  (-) CMV:                 R$ {custos:>13.2f}\n"
        relatorio += f"  (=) Lucro Bruto:         R$ {lucro_bruto:>13.2f}\n\n"
        
        relatorio += "DESPESAS:\n"
        relatorio += f"  (-) Despesas Operacionais: R$ {despesas:>13.2f}\n"
        relatorio += f"  (=) Lucro Operacional:   R$ {lucro_operacional:>13.2f}\n\n"
        
        relatorio += "IMPOSTOS:\n"
        relatorio += f"  (-) Impostos (15%):      R$ {impostos:>13.2f}\n"
        relatorio += f"  (=) LUCRO LÍQUIDO:       R$ {lucro_liquido:>13.2f}\n"
        
        self.texto_relatorio.delete('1.0', tk.END)
        self.texto_relatorio.insert('1.0', relatorio)
    
    def gerar_relatorio_pagar(self):
        """Gera relatório de contas a pagar"""
        relatorio = "=" * 60 + "\n"
        relatorio += " " * 18 + "CONTAS A PAGAR\n"
        relatorio += "=" * 60 + "\n\n"
        
        relatorio += f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        relatorio += f"{'Descrição':<30} {'Fornecedor':<20} {'Vencimento':<12} {'Valor':>12}\n"
        relatorio += "-" * 74 + "\n"
        
        total = 0
        for item in self.tree_pagar.get_children():
            valores = self.tree_pagar.item(item)['values']
            if valores[6] != 'Pago':
                relatorio += f"{valores[1][:28]:<30} {valores[2][:18]:<20} {valores[3]:<12} {valores[4]:>12}\n"
                total += float(valores[4].replace('R$', '').replace('.', '').replace(',', '.'))
        
        relatorio += "-" * 74 + "\n"
        relatorio += f"{'TOTAL A PAGAR:':<62} R$ {total:>11.2f}\n"
        
        self.texto_relatorio.delete('1.0', tk.END)
        self.texto_relatorio.insert('1.0', relatorio)
    
    def gerar_relatorio_receber(self):
        """Gera relatório de contas a receber"""
        relatorio = "=" * 60 + "\n"
        relatorio += " " * 18 + "CONTAS A RECEBER\n"
        relatorio += "=" * 60 + "\n\n"
        
        relatorio += f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        relatorio += f"{'Descrição':<30} {'Cliente':<20} {'Vencimento':<12} {'Valor':>12}\n"
        relatorio += "-" * 74 + "\n"
        
        total = 0
        for item in self.tree_receber.get_children():
            valores = self.tree_receber.item(item)['values']
            if valores[6] != 'Recebido':
                relatorio += f"{valores[1][:28]:<30} {valores[2][:18]:<20} {valores[3]:<12} {valores[4]:>12}\n"
                total += float(valores[4].replace('R$', '').replace('.', '').replace(',', '.'))
        
        relatorio += "-" * 74 + "\n"
        relatorio += f"{'TOTAL A RECEBER:':<62} R$ {total:>11.2f}\n"
        
        self.texto_relatorio.delete('1.0', tk.END)
        self.texto_relatorio.insert('1.0', relatorio)
    
    def gerar_relatorio_projetado(self):
        """Gera relatório de fluxo projetado"""
        relatorio = "=" * 60 + "\n"
        relatorio += " " * 16 + "FLUXO DE CAIXA PROJETADO\n"
        relatorio += "=" * 60 + "\n\n"
        
        relatorio += f"Data base: {datetime.now().strftime('%d/%m/%Y')}\n\n"
        
        relatorio += f"{'Período':<12} {'Previsão Entrada':>20} {'Previsão Saída':>20} {'Saldo Projetado':>20}\n"
        relatorio += "-" * 72 + "\n"
        
        saldo_atual = self.calcular_indicadores()['saldo']
        
        for i in range(1, 31):
            data = (datetime.now() + timedelta(days=i)).strftime("%d/%m")
            entrada = 1500 + (i % 5) * 100
            saida = 1200 + (i % 3) * 80
            saldo_atual += entrada - saida
            relatorio += f"{data:<12} R${entrada:>18.2f} R${saida:>18.2f} R${saldo_atual:>18.2f}\n"
        
        self.texto_relatorio.delete('1.0', tk.END)
        self.texto_relatorio.insert('1.0', relatorio)
    
    def voltar(self):
        """Volta para o menu principal"""
        self.db.fechar_conexao()
        self.janela.destroy()
        self.menu_principal.deiconify()