import tkinter as tk
from tkinter import messagebox
from database import Database
from datetime import datetime
from styles import Estilos

class TelaMenu:
    def __init__(self):
        self.db = Database()
        self.janela = tk.Tk()
        self.janela.title("StockMaster - Menu Principal")
        self.janela.geometry("1100x720")
        self.janela.resizable(False, False)
        self.janela.configure(bg=Estilos.COR_FUNDO)
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 1100
        altura = 720
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        # Variáveis para os cards (para poder atualizar)
        self.card_vendas = None
        self.card_estoque = None
        self.card_mais_vendido = None
        self.frame_cards = None
        
        self.criar_interface()
        self.atualizar_cards()  # Atualização inicial
        self.janela.mainloop()
    
    def criar_interface(self):
        # Frame branco principal
        frame_conteudo = tk.Frame(
            self.janela,
            bg=Estilos.COR_FUNDO_CONTEUDO,
            bd=0,
            highlightthickness=0
        )
        frame_conteudo.pack(expand=True, fill='both', padx=25, pady=25)
        
        # ===== ÁREA DO CABEÇALHO COM BOTÃO SAIR =====
        frame_cabecalho_completo = tk.Frame(frame_conteudo, bg='white', height=150)
        frame_cabecalho_completo.pack(fill='x', padx=20, pady=(10, 10))
        frame_cabecalho_completo.pack_propagate(False)
        
        # Botão SAIR no canto superior esquerdo
        btn_sair_frame, btn_sair = Estilos.criar_botao_arredondado(
            frame_cabecalho_completo,
            "Sair",
            self.confirmar_sair,
            cor_fundo='white',
            cor_texto=Estilos.COR_PRIMARIA,
            largura=8,
            altura=1,
            icone="🚪"
        )
        btn_sair_frame.place(x=10, y=10)
        
        # Título "StockMaster" no centro do cabeçalho
        titulo_sistema = tk.Label(
            frame_cabecalho_completo,
            text="STOCKMASTER",
            font=("Arial", 18, "bold"),
            fg=Estilos.COR_PRIMARIA,
            bg='white'
        )
        titulo_sistema.place(relx=0.5, y=25, anchor='center')
        
        # Subtítulo
        subtitulo = tk.Label(
            frame_cabecalho_completo,
            text="Sistema de Gestão de Estoque",
            font=("Arial", 10),
            fg='#666666',
            bg='white'
        )
        subtitulo.place(relx=0.5, y=55, anchor='center')
        
        # Botão Atualizar (novo)
        btn_atualizar_frame, btn_atualizar = Estilos.criar_botao_arredondado(
            frame_cabecalho_completo,
            "Atualizar",
            self.atualizar_cards,
            cor_fundo='white',
            cor_texto=Estilos.COR_PRIMARIA,
            largura=8,
            altura=1,
            icone="🔄"
        )
        btn_atualizar_frame.place(x=950, y=10)
        
        # ===== CARDS =====
        self.frame_cards = tk.Frame(frame_conteudo, bg='white', height=140)
        self.frame_cards.pack(fill='x', padx=30, pady=(20, 20))
        self.frame_cards.pack_propagate(False)
        
        for i in range(3):
            self.frame_cards.columnconfigure(i, weight=1)
        
        # Criar cards (serão atualizados depois)
        self.criar_cards()
        
        # ===== TÍTULO DA SEÇÃO DE MENU =====
        titulo_secao = tk.Label(
            frame_conteudo,
            text="MENU PRINCIPAL",
            font=("Arial", 22, "bold"),
            fg=Estilos.COR_PRIMARIA,
            bg='white'
        )
        titulo_secao.pack(pady=(10, 25))
        
        # ===== BOTÕES PRINCIPAIS =====
        frame_botoes = tk.Frame(frame_conteudo, bg='white')
        frame_botoes.pack(expand=True, fill='both', padx=50, pady=10)
        
        # Configurar grid 2x3
        for i in range(2):
            frame_botoes.rowconfigure(i, weight=1)
        for j in range(3):
            frame_botoes.columnconfigure(j, weight=1)
        
        # Lista de botões (agora incluindo Financeiro)
        botoes = [
            ("📦 CADASTRAR\nPRODUTO", self.abrir_cadastro),
            ("🔍 CONSULTAR\nESTOQUE", self.abrir_consulta),
            ("💰 REGISTRAR\nVENDA", self.abrir_venda),
            ("👥 GERENCIAR\nCLIENTES", self.abrir_clientes),
            ("💵 FINANCEIRO", self.abrir_financeiro),
            ("📊 RELATÓRIOS", self.abrir_relatorios)
        ]
        
        posicoes = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)]
        
        for (texto, comando), (row, col) in zip(botoes, posicoes):
            frame_btn, btn = Estilos.criar_botao_arredondado(
                frame_botoes,
                texto,
                comando,
                cor_fundo='white',
                cor_texto=Estilos.COR_PRIMARIA,
                largura=16,
                altura=3
            )
            frame_btn.grid(row=row, column=col, padx=20, pady=15, sticky='nsew')
        
        # ===== RODAPÉ =====
        rodape = tk.Label(
            frame_conteudo,
            text="© 2025 StockMaster - Todos os direitos reservados",
            font=("Arial", 8),
            fg='#cccccc',
            bg='white'
        )
        rodape.pack(side='bottom', pady=10)
    
    def criar_cards(self):
        """Cria os cards (ou recria se já existirem)"""
        # Limpar cards antigos se existirem
        if self.card_vendas:
            self.card_vendas.destroy()
        if self.card_estoque:
            self.card_estoque.destroy()
        if self.card_mais_vendido:
            self.card_mais_vendido.destroy()
        
        # Buscar dados atualizados
        vendas_valor, vendas_unidade = self.calcular_vendas_dia()
        estoque_valor = self.calcular_estoque_baixo()
        mais_vendido = self.calcular_mais_vendidos()
        
        # Card 1 - Vendas do Dia
        self.card_vendas = Estilos.criar_card_cabecalho(
            self.frame_cards,
            "📊 VENDAS DO DIA",
            vendas_valor,
            vendas_unidade,
            Estilos.COR_PRIMARIA,
            largura=280,
            altura=130
        )
        self.card_vendas.grid(row=0, column=0, padx=15, pady=5, sticky='nsew')
        
        # Card 2 - Estoque Baixo
        self.card_estoque = Estilos.criar_card_cabecalho(
            self.frame_cards,
            "⚠️ ESTOQUE BAIXO",
            estoque_valor,
            "produtos críticos",
            Estilos.COR_PRIMARIA,
            largura=280,
            altura=130
        )
        self.card_estoque.grid(row=0, column=1, padx=15, pady=5, sticky='nsew')
        
        # Card 3 - Mais Vendido
        self.card_mais_vendido = Estilos.criar_card_cabecalho(
            self.frame_cards,
            "🔥 MAIS VENDIDO",
            mais_vendido,
            "item do dia",
            Estilos.COR_PRIMARIA,
            largura=280,
            altura=130
        )
        self.card_mais_vendido.grid(row=0, column=2, padx=15, pady=5, sticky='nsew')
    
    def atualizar_cards(self):
        """Atualiza os dados dos cards"""
        print("🔄 Atualizando cards do menu...")  # Debug
        
        vendas_valor, vendas_unidade = self.calcular_vendas_dia()
        estoque_valor = self.calcular_estoque_baixo()
        mais_vendido = self.calcular_mais_vendidos()
        
        # Atualizar cada card individualmente (mais eficiente que recriar)
        self.atualizar_card(self.card_vendas, vendas_valor, vendas_unidade)
        self.atualizar_card(self.card_estoque, estoque_valor, "produtos críticos")
        self.atualizar_card(self.card_mais_vendido, mais_vendido, "item do dia")
        
        print("✅ Cards atualizados!")
    
    def atualizar_card(self, card, novo_valor, nova_unidade):
        """Atualiza os valores de um card específico"""
        if not card:
            return
        
        # Encontrar os labels dentro do card
        for widget in card.winfo_children():
            if isinstance(widget, tk.Frame):  # Frame do conteúdo
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        if child.cget('font')[1] == 22:  # Label do valor (fonte 22)
                            child.config(text=str(novo_valor))
                        elif child.cget('font')[1] == 9:  # Label da unidade (fonte 9)
                            child.config(text=nova_unidade)
    
    def calcular_vendas_dia(self):
        """Calcula o total de vendas do dia"""
        try:
            hoje = datetime.now().strftime("%d/%m/%Y")
            self.db.cursor.execute('''
                SELECT COUNT(*), COALESCE(SUM(total), 0) FROM vendas WHERE data_venda = ?
            ''', (hoje,))
            
            resultado = self.db.cursor.fetchone()
            count = resultado[0] or 0
            total = resultado[1] or 0
            
            return str(count), f"R$ {total:.2f}"
        except Exception as e:
            print(f"Erro ao calcular vendas: {e}")
            return "0", "R$ 0,00"
    
    def calcular_estoque_baixo(self):
        """Calcula quantidade de produtos com estoque baixo"""
        try:
            self.db.cursor.execute('''
                SELECT COUNT(*) FROM produtos WHERE quantidade < 5
            ''')
            count = self.db.cursor.fetchone()[0] or 0
            return str(count)
        except Exception as e:
            print(f"Erro ao calcular estoque baixo: {e}")
            return "0"
    
    def calcular_mais_vendidos(self):
        """Calcula os produtos mais vendidos do dia"""
        try:
            hoje = datetime.now().strftime("%d/%m/%Y")
            self.db.cursor.execute('''
                SELECT p.nome, SUM(v.quantidade) as total
                FROM vendas v
                JOIN produtos p ON v.codigo_produto = p.codigo
                WHERE v.data_venda = ?
                GROUP BY p.nome
                ORDER BY total DESC
                LIMIT 1
            ''', (hoje,))
            
            resultado = self.db.cursor.fetchone()
            if resultado:
                nome = resultado[0]
                return nome[:20] + "..." if len(nome) > 20 else nome
            else:
                return "Nenhuma venda"
        except Exception as e:
            print(f"Erro ao calcular mais vendido: {e}")
            return "Carregando..."
    
    def abrir_cadastro(self):
        from cadastro_produto import TelaCadastro
        self.janela.withdraw()
        tela = TelaCadastro(self.janela)
        self.janela.wait_window(tela.janela)  # Aguarda a tela fechar
        self.atualizar_cards()  # Atualiza quando voltar
        self.janela.deiconify()
    
    def abrir_consulta(self):
        from consulta_estoque import TelaConsulta
        self.janela.withdraw()
        tela = TelaConsulta(self.janela)
        self.janela.wait_window(tela.janela)
        self.atualizar_cards()
        self.janela.deiconify()
    
    def abrir_venda(self):
        from registrar_venda import TelaVenda
        self.janela.withdraw()
        tela = TelaVenda(self.janela)
        self.janela.wait_window(tela.janela)
        self.atualizar_cards()  # Atualiza após a venda
        self.janela.deiconify()
    
    def abrir_clientes(self):
        from clientes import TelaClientes
        self.janela.withdraw()
        tela = TelaClientes(self.janela)
        self.janela.wait_window(tela.janela)
        self.atualizar_cards()
        self.janela.deiconify()
    
    def abrir_financeiro(self):
        from financeiro import TelaFinanceiro
        self.janela.withdraw()
        tela = TelaFinanceiro(self.janela)
        self.janela.wait_window(tela.janela)
        self.atualizar_cards()
        self.janela.deiconify()
    
    def abrir_relatorios(self):
        from relatorios import TelaRelatorios
        self.janela.withdraw()
        tela = TelaRelatorios(self.janela)
        self.janela.wait_window(tela.janela)
        self.janela.deiconify()
    
    def confirmar_sair(self):
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            self.db.fechar_conexao()
            self.janela.quit()