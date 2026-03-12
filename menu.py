# menu.py
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
        self.janela.configure(bg='#f5f5f5')
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 1100
        altura = 720
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        self.cards = {}
        self.criar_interface()
        self.atualizar_cards()  # Atualização inicial
        self.janela.mainloop()
    
    def criar_interface(self):
        # ===== HEADER =====
        header = tk.Frame(self.janela, bg='white', height=70)
        header.pack(fill='x', padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        # Logo e título
        tk.Label(
            header,
            text="📦 STOCKMASTER",
            font=("Arial", 20, "bold"),
            fg=Estilos.COR_PRIMARIA,
            bg='white'
        ).pack(side='left', padx=20)
        
        tk.Label(
            header,
            text=datetime.now().strftime("%d/%m/%Y"),
            font=("Arial", 11),
            fg=Estilos.COR_TEXTO_SECUNDARIO,
            bg='white'
        ).pack(side='right', padx=20)
        
        # ===== CARDS DE INDICADORES =====
        frame_cards = tk.Frame(self.janela, bg='#f5f5f5')
        frame_cards.pack(fill='x', padx=20, pady=10)
        
        for i in range(3):
            frame_cards.columnconfigure(i, weight=1)
        
        # Buscar dados iniciais
        vendas_count, vendas_total = self.calcular_vendas_dia()
        estoque_baixo = self.calcular_estoque_baixo()
        mais_vendido = self.calcular_mais_vendidos()
        
        # Card 1 - Vendas do Dia
        self.cards['vendas'] = Estilos.criar_card_moderno(
            frame_cards,
            "Vendas Hoje",
            vendas_count,
            f"Total: {vendas_total}",
            "📊",
            largura=330,
            altura=110
        )
        self.cards['vendas'].grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        
        # Card 2 - Estoque Baixo
        self.cards['estoque'] = Estilos.criar_card_moderno(
            frame_cards,
            "Estoque Baixo",
            estoque_baixo,
            "produtos críticos",
            "⚠️",
            largura=330,
            altura=110
        )
        self.cards['estoque'].grid(row=0, column=1, padx=10, pady=5, sticky='nsew')
        
        # Card 3 - Mais Vendido
        self.cards['top'] = Estilos.criar_card_moderno(
            frame_cards,
            "Mais Vendido",
            mais_vendido,
            "item do dia",
            "🔥",
            largura=330,
            altura=110
        )
        self.cards['top'].grid(row=0, column=2, padx=10, pady=5, sticky='nsew')
        
        # ===== SEÇÃO PRINCIPAL =====
        secao_principal = Estilos.criar_secao(self.janela, "Módulos do Sistema")
        
        # ===== BOTÕES PRINCIPAIS =====
        frame_botoes = tk.Frame(self.janela, bg='#f5f5f5')
        frame_botoes.pack(expand=True, fill='both', padx=30, pady=10)
        
        # Grid 2x3
        for i in range(2):
            frame_botoes.rowconfigure(i, weight=1)
        for j in range(3):
            frame_botoes.columnconfigure(j, weight=1)
        
        # Botões com ícones
        botoes = [
            ("📦 PRODUTOS", self.abrir_cadastro, "Cadastrar", "primario"),
            ("🔍 CONSULTAR", self.abrir_consulta, "Estoque", "secundario"),
            ("💰 VENDAS", self.abrir_venda, "Registrar", "primario"),
            ("👥 CLIENTES", self.abrir_clientes, "Gerenciar", "secundario"),
            ("💵 FINANCEIRO", self.abrir_financeiro, "Controle", "primario"),
            ("📊 RELATÓRIOS", self.abrir_relatorios, "Gerar", "secundario")
        ]
        
        posicoes = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)]
        
        for (titulo, comando, subtitulo, tipo), (row, col) in zip(botoes, posicoes):
            self.criar_botao_card(frame_botoes, titulo, subtitulo, comando, tipo, row, col)
        
        # ===== BOTÃO SAIR =====
        frame_sair = tk.Frame(self.janela, bg='#f5f5f5')
        frame_sair.pack(fill='x', padx=20, pady=10)
        
        btn_sair_frame, btn_sair = Estilos.criar_botao_moderno(
            frame_sair,
            "Sair do Sistema",
            self.confirmar_sair,
            tipo='secundario',
            icone="🚪"
        )
        btn_sair_frame.pack(side='right')
    
    def criar_botao_card(self, parent, titulo, subtitulo, comando, tipo, row, col):
        """Cria um card de botão no estilo moderno"""
        frame = tk.Frame(
            parent,
            bg='white',
            highlightbackground=Estilos.COR_BORDA,
            highlightthickness=1,
            bd=0
        )
        frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Efeito hover
        def on_enter(e):
            frame.config(highlightbackground=Estilos.COR_PRIMARIA, highlightthickness=2)
        
        def on_leave(e):
            frame.config(highlightbackground=Estilos.COR_BORDA, highlightthickness=1)
        
        frame.bind('<Enter>', on_enter)
        frame.bind('<Leave>', on_leave)
        
        # Conteúdo
        conteudo = tk.Frame(frame, bg='white', padx=15, pady=15)
        conteudo.pack(fill='both', expand=True)
        
        tk.Label(
            conteudo,
            text=titulo,
            font=("Arial", 16, "bold"),
            fg=Estilos.COR_TEXTO,
            bg='white'
        ).pack(anchor='w')
        
        tk.Label(
            conteudo,
            text=subtitulo,
            font=("Arial", 11),
            fg=Estilos.COR_TEXTO_SECUNDARIO,
            bg='white'
        ).pack(anchor='w', pady=(5, 10))
        
        # Botão no estilo "ADICIONAR"
        btn_frame, btn = Estilos.criar_botao_moderno(
            conteudo,
            "Acessar",
            comando,
            tipo=tipo
        )
        btn_frame.pack(anchor='w')
        
        # Vincular clique no card também
        def card_click(e):
            comando()
        
        frame.bind('<Button-1>', card_click)
        conteudo.bind('<Button-1>', card_click)
        for child in conteudo.winfo_children():
            child.bind('<Button-1>', card_click)
    
    def atualizar_cards(self):
        """Atualiza os cards com dados reais"""
        print("🔄 Atualizando cards do menu...")
        
        vendas_count, vendas_total = self.calcular_vendas_dia()
        estoque_baixo = self.calcular_estoque_baixo()
        mais_vendido = self.calcular_mais_vendidos()
        
        print(f"📊 Vendas: {vendas_count} - {vendas_total}")
        print(f"⚠️ Estoque baixo: {estoque_baixo}")
        print(f"🔥 Mais vendido: {mais_vendido}")
        
        # Atualizar card de vendas
        self.atualizar_card(self.cards['vendas'], vendas_count, f"Total: {vendas_total}")
        
        # Atualizar card de estoque
        self.atualizar_card(self.cards['estoque'], estoque_baixo, "produtos críticos")
        
        # Atualizar card de mais vendido
        self.atualizar_card(self.cards['top'], mais_vendido, "item do dia")
        
        print("✅ Cards atualizados!")
    
    def atualizar_card(self, card, novo_valor, novo_subtitulo):
        """Atualiza os valores de um card"""
        if not card:
            print("❌ Card não encontrado!")
            return
        
        try:
            # Procura pela estrutura do card moderno
            # card -> frame_icone (right) e frame_info (left)
            for widget in card.winfo_children():
                if isinstance(widget, tk.Frame):
                    # Verifica se é o frame_info (tem vários labels)
                    if widget.winfo_children():
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Label):
                                # Label do valor (fonte 20)
                                if child.cget('font')[1] == 20:
                                    child.config(text=str(novo_valor))
                                    print(f"✅ Valor atualizado para: {novo_valor}")
                                # Label do subtítulo (fonte 9)
                                elif child.cget('font')[1] == 9:
                                    child.config(text=novo_subtitulo)
                                    print(f"✅ Subtítulo atualizado para: {novo_subtitulo}")
        except Exception as e:
            print(f"❌ Erro ao atualizar card: {e}")
    
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
            
            print(f"📊 Vendas encontradas: {count} - R$ {total:.2f}")
            return str(count), f"R$ {total:.2f}"
        except Exception as e:
            print(f"❌ Erro ao calcular vendas: {e}")
            return "0", "R$ 0,00"
    
    def calcular_estoque_baixo(self):
        """Calcula quantidade de produtos com estoque baixo"""
        try:
            self.db.cursor.execute('''
                SELECT COUNT(*) FROM produtos WHERE quantidade < 5
            ''')
            count = self.db.cursor.fetchone()[0] or 0
            print(f"⚠️ Produtos com estoque baixo: {count}")
            return str(count)
        except Exception as e:
            print(f"❌ Erro ao calcular estoque baixo: {e}")
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
            if resultado and resultado[0]:
                nome = resultado[0]
                print(f"🔥 Produto mais vendido: {nome}")
                return nome[:15] + "..." if len(nome) > 15 else nome
            else:
                print("📭 Nenhuma venda hoje")
                return "Nenhuma venda"
        except Exception as e:
            print(f"❌ Erro ao calcular mais vendido: {e}")
            return "Erro"
    
    def abrir_cadastro(self):
        from cadastro_produto import TelaCadastro
        self.janela.withdraw()
        tela = TelaCadastro(self.janela)
        self.janela.wait_window(tela.janela)
        self.atualizar_cards()
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
        self.atualizar_cards()
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