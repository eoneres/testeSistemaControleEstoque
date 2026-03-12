import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import Database
from datetime import datetime, timedelta
import csv

class TelaRelatorios:
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.db = Database()
        self.janela = tk.Toplevel()
        self.janela.title("StockMaster - Relatórios")
        self.janela.geometry("1000x600")
        self.janela.resizable(False, False)
        self.janela.configure(bg='#ff751f')
        
        # Cores como atributos da classe
        self.cor_primaria = '#ff751f'
        self.cor_botao = '#ffffff'
        self.cor_texto_botao = '#ff751f'
        self.cor_sombra = '#e65c00'
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 1000
        altura = 600
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        self.ultimo_relatorio = ""
        self.criar_interface()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar_menu)
        self.janela.mainloop()
    
    def criar_interface(self):
        # Frame branco principal
        frame_conteudo = tk.Frame(self.janela, bg='white', bd=0)
        frame_conteudo.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            frame_conteudo,
            text="📊 RELATÓRIOS GERENCIAIS",
            font=("Arial", 20, "bold"),
            fg=self.cor_primaria,
            bg='white'
        )
        titulo.pack(pady=20)
        
        # Frame principal dividido (menu esquerdo + conteúdo direito)
        frame_principal = tk.Frame(frame_conteudo, bg='white')
        frame_principal.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ===== MENU LATERAL ESQUERDO =====
        frame_menu = tk.Frame(frame_principal, bg='#f8f8f8', width=200, relief='solid', bd=1)
        frame_menu.pack(side='left', fill='y', padx=(0, 10))
        frame_menu.pack_propagate(False)
        
        tk.Label(
            frame_menu,
            text="RELATÓRIOS",
            font=("Arial", 14, "bold"),
            fg=self.cor_primaria,
            bg='#f8f8f8'
        ).pack(pady=20)
        
        # Botões de relatório
        relatorios = [
            ("📦 Estoque Atual", self.mostrar_estoque_atual),
            ("⚠️ Estoque Baixo", self.mostrar_estoque_baixo),
            ("💰 Vendas do Dia", self.mostrar_vendas_dia),
            ("📅 Vendas por Período", self.mostrar_vendas_periodo),
            ("👥 Compras por Cliente", self.mostrar_compras_cliente),
            ("⭐ Histórico de Pontos", self.mostrar_pontos)
        ]
        
        for texto, comando in relatorios:
            btn = tk.Button(
                frame_menu,
                text=texto,
                font=("Arial", 10),
                bg='white',
                fg='#333333',
                bd=1,
                relief='solid',
                width=20,
                pady=8,
                cursor='hand2',
                command=comando
            )
            btn.pack(pady=3, padx=10)
            
            def on_enter(e, b=btn):
                b['bg'] = '#f0f0f0'
                b['fg'] = self.cor_primaria
            
            def on_leave(e, b=btn):
                b['bg'] = 'white'
                b['fg'] = '#333333'
            
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
        
        btn_voltar = tk.Button(
            frame_menu,
            text="↩️ VOLTAR",
            font=("Arial", 10, "bold"),
            bg=self.cor_botao,
            fg=self.cor_texto_botao,
            bd=1,
            relief='solid',
            width=20,
            pady=8,
            cursor='hand2',
            command=self.voltar_menu
        )
        btn_voltar.pack(pady=20, padx=10)
        
        def on_enter_voltar(e):
            btn_voltar['bg'] = '#f5f5f5'
            btn_voltar['fg'] = self.cor_sombra
        
        def on_leave_voltar(e):
            btn_voltar['bg'] = self.cor_botao
            btn_voltar['fg'] = self.cor_texto_botao
        
        btn_voltar.bind('<Enter>', on_enter_voltar)
        btn_voltar.bind('<Leave>', on_leave_voltar)
        
        # ===== ÁREA DE CONTEÚDO =====
        frame_direito = tk.Frame(frame_principal, bg='white')
        frame_direito.pack(side='right', fill='both', expand=True)
        
        # Área de texto para o relatório
        self.texto_relatorio = tk.Text(
            frame_direito,
            font=("Courier", 10),
            bg='white',
            wrap='word',
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.texto_relatorio.pack(fill='both', expand=True, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.texto_relatorio)
        scrollbar.pack(side='right', fill='y')
        self.texto_relatorio.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.texto_relatorio.yview)
        
        # Botão exportar
        frame_exportar = tk.Frame(frame_direito, bg='white', pady=10)
        frame_exportar.pack(fill='x')
        
        btn_exportar = tk.Button(
            frame_exportar,
            text="📥 EXPORTAR PARA CSV",
            font=("Arial", 10, "bold"),
            bg=self.cor_botao,
            fg=self.cor_texto_botao,
            bd=1,
            relief='solid',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.exportar_csv
        )
        btn_exportar.pack()
        
        def on_enter_exportar(e):
            btn_exportar['bg'] = '#f5f5f5'
            btn_exportar['fg'] = self.cor_sombra
        
        def on_leave_exportar(e):
            btn_exportar['bg'] = self.cor_botao
            btn_exportar['fg'] = self.cor_texto_botao
        
        btn_exportar.bind('<Enter>', on_enter_exportar)
        btn_exportar.bind('<Leave>', on_leave_exportar)
    
    def mostrar_estoque_atual(self):
        self.texto_relatorio.delete('1.0', tk.END)
        relatorio = "=" * 80 + "\n"
        relatorio += " " * 30 + "RELATÓRIO DE ESTOQUE ATUAL\n"
        relatorio += "=" * 80 + "\n\n"
        
        self.db.cursor.execute('''
            SELECT codigo, nome, categoria, tamanho, cor, quantidade, preco_venda, fornecedor
            FROM produtos
            ORDER BY nome
        ''')
        
        produtos = self.db.cursor.fetchall()
        
        if not produtos:
            relatorio += "Nenhum produto cadastrado.\n"
        else:
            relatorio += f"{'Código':<10} {'Nome':<25} {'Categoria':<12} {'Tam':<5} {'Cor':<10} {'Qtd':<6} {'Preço':<12} {'Fornecedor':<15}\n"
            relatorio += "-" * 95 + "\n"
            
            total_produtos = 0
            valor_total = 0
            
            for produto in produtos:
                codigo, nome, categoria, tamanho, cor, quantidade, preco, fornecedor = produto
                relatorio += f"{codigo:<10} {nome[:24]:<25} {categoria:<12} {tamanho:<5} {cor:<10} {quantidade:<6} R$ {preco:<9.2f} {fornecedor[:14]:<15}\n"
                
                total_produtos += quantidade
                valor_total += quantidade * preco
            
            relatorio += "-" * 95 + "\n"
            relatorio += f"TOTAL: {total_produtos} unidades | Valor em estoque: R$ {valor_total:.2f}\n"
        
        self.ultimo_relatorio = relatorio
        self.texto_relatorio.insert('1.0', relatorio)
    
    def mostrar_estoque_baixo(self):
        self.texto_relatorio.delete('1.0', tk.END)
        relatorio = "=" * 80 + "\n"
        relatorio += " " * 25 + "RELATÓRIO DE ESTOQUE BAIXO (< 5 UNIDADES)\n"
        relatorio += "=" * 80 + "\n\n"
        
        self.db.cursor.execute('''
            SELECT codigo, nome, categoria, tamanho, cor, quantidade, fornecedor
            FROM produtos
            WHERE quantidade < 5
            ORDER BY quantidade
        ''')
        
        produtos = self.db.cursor.fetchall()
        
        if not produtos:
            relatorio += "Nenhum produto com estoque baixo.\n"
        else:
            relatorio += f"{'Código':<10} {'Nome':<25} {'Categoria':<12} {'Tam':<5} {'Cor':<10} {'Qtd':<6} {'Fornecedor':<15}\n"
            relatorio += "-" * 83 + "\n"
            
            for produto in produtos:
                codigo, nome, categoria, tamanho, cor, quantidade, fornecedor = produto
                relatorio += f"{codigo:<10} {nome[:24]:<25} {categoria:<12} {tamanho:<5} {cor:<10} {quantidade:<6} {fornecedor[:14]:<15}\n"
        
        self.ultimo_relatorio = relatorio
        self.texto_relatorio.insert('1.0', relatorio)
    
    def mostrar_vendas_dia(self):
        self.texto_relatorio.delete('1.0', tk.END)
        hoje = datetime.now().strftime("%d/%m/%Y")
        
        relatorio = "=" * 80 + "\n"
        relatorio += f" " * 28 + f"RELATÓRIO DE VENDAS - {hoje}\n"
        relatorio += "=" * 80 + "\n\n"
        
        self.db.cursor.execute('''
            SELECT v.id, p.nome, v.quantidade, v.preco_unitario, v.total, v.hora_venda,
                   c.nome
            FROM vendas v
            JOIN produtos p ON v.codigo_produto = p.codigo
            LEFT JOIN clientes c ON v.cliente_codigo = c.codigo
            WHERE v.data_venda = ?
            ORDER BY v.hora_venda
        ''', (hoje,))
        
        vendas = self.db.cursor.fetchall()
        
        if not vendas:
            relatorio += "Nenhuma venda registrada hoje.\n"
        else:
            relatorio += f"{'Hora':<8} {'ID':<6} {'Produto':<25} {'Qtd':<6} {'Preço':<10} {'Total':<10} {'Cliente':<20}\n"
            relatorio += "-" * 85 + "\n"
            
            total_vendas = 0
            quantidade_total = 0
            
            for venda in vendas:
                venda_id, produto, qtd, preco, total, hora, cliente = venda
                cliente = cliente or "---"
                relatorio += f"{hora:<8} {venda_id:<6} {produto[:24]:<25} {qtd:<6} R${preco:<8.2f} R${total:<8.2f} {cliente[:19]:<20}\n"
                
                total_vendas += total
                quantidade_total += qtd
            
            relatorio += "-" * 85 + "\n"
            relatorio += f"TOTAL: {quantidade_total} unidades | Valor total: R$ {total_vendas:.2f}\n"
        
        self.ultimo_relatorio = relatorio
        self.texto_relatorio.insert('1.0', relatorio)
    
    def mostrar_vendas_periodo(self):
        """Abre janela para selecionar período e mostra vendas do período"""
        # Janela para selecionar período
        periodo_janela = tk.Toplevel(self.janela)
        periodo_janela.title("Selecionar Período")
        periodo_janela.geometry("400x300")
        periodo_janela.configure(bg='white')
        periodo_janela.resizable(False, False)
        
        # Centralizar
        periodo_janela.update_idletasks()
        x = (periodo_janela.winfo_screenwidth() // 2) - (400 // 2)
        y = (periodo_janela.winfo_screenheight() // 2) - (300 // 2)
        periodo_janela.geometry(f'{400}x{300}+{x}+{y}')
        
        # Frame principal
        frame = tk.Frame(periodo_janela, bg='white', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        tk.Label(
            frame,
            text="📅 SELECIONAR PERÍODO",
            font=("Arial", 14, "bold"),
            fg=self.cor_primaria,
            bg='white'
        ).pack(pady=10)
        
        # Data inicial
        tk.Label(
            frame,
            text="Data Inicial (DD/MM/AAAA):",
            font=("Arial", 10),
            bg='white',
            fg='#333333'
        ).pack(anchor='w', pady=(10, 2))
        
        data_inicial_entry = tk.Entry(
            frame,
            font=("Arial", 11),
            width=20,
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        data_inicial_entry.pack(pady=(0, 10), ipady=5)
        
        # Data final
        tk.Label(
            frame,
            text="Data Final (DD/MM/AAAA):",
            font=("Arial", 10),
            bg='white',
            fg='#333333'
        ).pack(anchor='w', pady=(10, 2))
        
        data_final_entry = tk.Entry(
            frame,
            font=("Arial", 11),
            width=20,
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        data_final_entry.pack(pady=(0, 10), ipady=5)
        
        # Preencher com datas padrão (últimos 30 dias)
        hoje = datetime.now()
        trinta_dias_atras = hoje - timedelta(days=30)
        data_inicial_entry.insert(0, trinta_dias_atras.strftime("%d/%m/%Y"))
        data_final_entry.insert(0, hoje.strftime("%d/%m/%Y"))
        
        def gerar_relatorio():
            data_inicial = data_inicial_entry.get().strip()
            data_final = data_final_entry.get().strip()
            
            if not data_inicial or not data_final:
                messagebox.showerror("Erro", "Preencha as duas datas!")
                return
            
            periodo_janela.destroy()
            self._mostrar_vendas_periodo(data_inicial, data_final)
        
        # Botões
        frame_botoes = tk.Frame(frame, bg='white', pady=10)
        frame_botoes.pack(fill='x')
        
        btn_gerar = tk.Button(
            frame_botoes,
            text="📊 GERAR RELATÓRIO",
            font=("Arial", 11, "bold"),
            bg=self.cor_botao,
            fg=self.cor_texto_botao,
            bd=1,
            relief='solid',
            padx=15,
            pady=8,
            cursor='hand2',
            command=gerar_relatorio
        )
        btn_gerar.pack(side='left', padx=5, expand=True, fill='x')
        
        btn_cancelar = tk.Button(
            frame_botoes,
            text="✖ CANCELAR",
            font=("Arial", 11, "bold"),
            bg='#f0f0f0',
            fg='#666666',
            bd=1,
            relief='solid',
            padx=15,
            pady=8,
            cursor='hand2',
            command=periodo_janela.destroy
        )
        btn_cancelar.pack(side='left', padx=5, expand=True, fill='x')
        
        # Efeito hover
        for btn in [btn_gerar, btn_cancelar]:
            def on_enter(e, b=btn):
                if b == btn_gerar:
                    b['bg'] = '#f5f5f5'
                    b['fg'] = self.cor_sombra
                else:
                    b['bg'] = '#e0e0e0'
            
            def on_leave(e, b=btn):
                if b == btn_gerar:
                    b['bg'] = self.cor_botao
                    b['fg'] = self.cor_texto_botao
                else:
                    b['bg'] = '#f0f0f0'
                    b['fg'] = '#666666'
            
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
    
    def _mostrar_vendas_periodo(self, data_inicial, data_final):
        """Mostra vendas em um período específico"""
        self.texto_relatorio.delete('1.0', tk.END)
        
        relatorio = "=" * 80 + "\n"
        relatorio += f" " * 20 + f"RELATÓRIO DE VENDAS - PERÍODO\n"
        relatorio += f" " * 25 + f"{data_inicial} a {data_final}\n"
        relatorio += "=" * 80 + "\n\n"
        
        self.db.cursor.execute('''
            SELECT v.data_venda, v.id, p.nome, v.quantidade, v.preco_unitario, 
                   v.total, v.hora_venda, c.nome
            FROM vendas v
            JOIN produtos p ON v.codigo_produto = p.codigo
            LEFT JOIN clientes c ON v.cliente_codigo = c.codigo
            WHERE v.data_venda BETWEEN ? AND ?
            ORDER BY v.data_venda DESC, v.hora_venda DESC
        ''', (data_inicial, data_final))
        
        vendas = self.db.cursor.fetchall()
        
        if not vendas:
            relatorio += "Nenhuma venda encontrada no período.\n"
        else:
            relatorio += f"{'Data':<12} {'Hora':<8} {'ID':<6} {'Produto':<25} {'Qtd':<6} {'Preço':<10} {'Total':<10} {'Cliente':<20}\n"
            relatorio += "-" * 97 + "\n"
            
            total_vendas = 0
            quantidade_total = 0
            
            for venda in vendas:
                data, venda_id, produto, qtd, preco, total, hora, cliente = venda
                cliente = cliente or "---"
                relatorio += f"{data:<12} {hora:<8} {venda_id:<6} {produto[:24]:<25} {qtd:<6} R${preco:<8.2f} R${total:<8.2f} {cliente[:19]:<20}\n"
                
                total_vendas += total
                quantidade_total += qtd
            
            relatorio += "-" * 97 + "\n"
            relatorio += f"TOTAL DO PERÍODO: {quantidade_total} unidades | Valor total: R$ {total_vendas:.2f}\n"
        
        self.ultimo_relatorio = relatorio
        self.texto_relatorio.insert('1.0', relatorio)
    
    def mostrar_compras_cliente(self):
        """Mostra relatório de compras por cliente"""
        # Primeiro, buscar lista de clientes
        self.db.cursor.execute('''
            SELECT codigo, nome FROM clientes ORDER BY nome
        ''')
        
        clientes = self.db.cursor.fetchall()
        
        if not clientes:
            messagebox.showinfo("Info", "Não há clientes cadastrados.")
            return
        
        # Criar janela de seleção
        cliente_janela = tk.Toplevel(self.janela)
        cliente_janela.title("Selecionar Cliente")
        cliente_janela.geometry("400x200")
        cliente_janela.configure(bg='white')
        
        # Centralizar
        cliente_janela.update_idletasks()
        x = (cliente_janela.winfo_screenwidth() // 2) - (400 // 2)
        y = (cliente_janela.winfo_screenheight() // 2) - (200 // 2)
        cliente_janela.geometry(f'{400}x{200}+{x}+{y}')
        
        frame = tk.Frame(cliente_janela, bg='white', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        tk.Label(
            frame,
            text="👥 SELECIONAR CLIENTE",
            font=("Arial", 14, "bold"),
            fg=self.cor_primaria,
            bg='white'
        ).pack(pady=10)
        
        tk.Label(
            frame,
            text="Cliente:",
            font=("Arial", 10),
            bg='white',
            fg='#333333'
        ).pack(anchor='w', pady=(10, 2))
        
        # Combobox com clientes
        cliente_var = tk.StringVar()
        cliente_combo = ttk.Combobox(
            frame,
            textvariable=cliente_var,
            values=[f"{c[0]} - {c[1]}" for c in clientes],
            font=("Arial", 10),
            width=40
        )
        cliente_combo.pack(pady=(0, 10))
        
        def gerar_relatorio_cliente():
            selecao = cliente_var.get()
            if not selecao:
                messagebox.showerror("Erro", "Selecione um cliente!")
                return
            
            codigo_cliente = selecao.split(" - ")[0]
            cliente_janela.destroy()
            self._mostrar_compras_cliente(codigo_cliente)
        
        btn_gerar = tk.Button(
            frame,
            text="📊 GERAR RELATÓRIO",
            font=("Arial", 11, "bold"),
            bg=self.cor_botao,
            fg=self.cor_texto_botao,
            bd=1,
            relief='solid',
            padx=15,
            pady=8,
            cursor='hand2',
            command=gerar_relatorio_cliente
        )
        btn_gerar.pack(pady=10)
    
    def _mostrar_compras_cliente(self, codigo_cliente):
        """Mostra histórico de compras de um cliente específico"""
        # Buscar dados do cliente
        self.db.cursor.execute('''
            SELECT nome, pontos FROM clientes WHERE codigo = ?
        ''', (codigo_cliente,))
        
        cliente = self.db.cursor.fetchone()
        
        if not cliente:
            return
        
        nome_cliente, pontos = cliente
        
        self.texto_relatorio.delete('1.0', tk.END)
        
        relatorio = "=" * 80 + "\n"
        relatorio += f" " * 25 + f"HISTÓRICO DE COMPRAS\n"
        relatorio += f" " * 20 + f"Cliente: {nome_cliente}\n"
        relatorio += "=" * 80 + "\n\n"
        
        self.db.cursor.execute('''
            SELECT v.data_venda, v.id, p.nome, v.quantidade, v.preco_unitario, 
                   v.total, v.pontos_ganhos
            FROM vendas v
            JOIN produtos p ON v.codigo_produto = p.codigo
            WHERE v.cliente_codigo = ?
            ORDER BY v.data_venda DESC, v.hora_venda DESC
        ''', (codigo_cliente,))
        
        compras = self.db.cursor.fetchall()
        
        if not compras:
            relatorio += "Este cliente não possui compras registradas.\n"
        else:
            relatorio += f"{'Data':<12} {'ID':<6} {'Produto':<25} {'Qtd':<6} {'Preço':<10} {'Total':<10} {'Pontos':<8}\n"
            relatorio += "-" * 77 + "\n"
            
            total_compras = 0
            total_pontos = 0
            
            for compra in compras:
                data, venda_id, produto, qtd, preco, total, pontos_compra = compra
                relatorio += f"{data:<12} {venda_id:<6} {produto[:24]:<25} {qtd:<6} R${preco:<8.2f} R${total:<8.2f} {pontos_compra:<8}\n"
                
                total_compras += total
                total_pontos += pontos_compra
            
            relatorio += "-" * 77 + "\n"
            relatorio += f"TOTAL GASTO: R$ {total_compras:.2f} | Total de pontos ganhos: {total_pontos}\n"
            relatorio += f"SALDO ATUAL DE PONTOS: {pontos}\n"
        
        self.ultimo_relatorio = relatorio
        self.texto_relatorio.insert('1.0', relatorio)
    
    def mostrar_pontos(self):
        """Mostra histórico de pontos de um cliente"""
        # Similar ao mostrar_compras_cliente, mas focado em pontos
        self.db.cursor.execute('''
            SELECT codigo, nome, pontos FROM clientes ORDER BY nome
        ''')
        
        clientes = self.db.cursor.fetchall()
        
        if not clientes:
            messagebox.showinfo("Info", "Não há clientes cadastrados.")
            return
        
        # Criar janela de seleção
        pontos_janela = tk.Toplevel(self.janela)
        pontos_janela.title("Selecionar Cliente")
        pontos_janela.geometry("400x250")
        pontos_janela.configure(bg='white')
        
        # Centralizar
        pontos_janela.update_idletasks()
        x = (pontos_janela.winfo_screenwidth() // 2) - (400 // 2)
        y = (pontos_janela.winfo_screenheight() // 2) - (250 // 2)
        pontos_janela.geometry(f'{400}x{250}+{x}+{y}')
        
        frame = tk.Frame(pontos_janela, bg='white', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        tk.Label(
            frame,
            text="⭐ HISTÓRICO DE PONTOS",
            font=("Arial", 14, "bold"),
            fg=self.cor_primaria,
            bg='white'
        ).pack(pady=10)
        
        tk.Label(
            frame,
            text="Cliente:",
            font=("Arial", 10),
            bg='white',
            fg='#333333'
        ).pack(anchor='w', pady=(10, 2))
        
        # Combobox com clientes
        cliente_var = tk.StringVar()
        cliente_combo = ttk.Combobox(
            frame,
            textvariable=cliente_var,
            values=[f"{c[0]} - {c[1]} (Saldo: {c[2]} pts)" for c in clientes],
            font=("Arial", 10),
            width=40
        )
        cliente_combo.pack(pady=(0, 10))
        
        def gerar_relatorio_pontos():
            selecao = cliente_var.get()
            if not selecao:
                messagebox.showerror("Erro", "Selecione um cliente!")
                return
            
            codigo_cliente = selecao.split(" - ")[0]
            pontos_janela.destroy()
            self._mostrar_historico_pontos(codigo_cliente)
        
        btn_gerar = tk.Button(
            frame,
            text="📊 GERAR RELATÓRIO",
            font=("Arial", 11, "bold"),
            bg=self.cor_botao,
            fg=self.cor_texto_botao,
            bd=1,
            relief='solid',
            padx=15,
            pady=8,
            cursor='hand2',
            command=gerar_relatorio_pontos
        )
        btn_gerar.pack(pady=10)
    
    def _mostrar_historico_pontos(self, codigo_cliente):
        """Mostra histórico de pontos de um cliente"""
        # Buscar dados do cliente
        self.db.cursor.execute('''
            SELECT nome, pontos FROM clientes WHERE codigo = ?
        ''', (codigo_cliente,))
        
        cliente = self.db.cursor.fetchone()
        
        if not cliente:
            return
        
        nome_cliente, saldo_atual = cliente
        
        self.texto_relatorio.delete('1.0', tk.END)
        
        relatorio = "=" * 80 + "\n"
        relatorio += f" " * 25 + f"HISTÓRICO DE PONTOS\n"
        relatorio += f" " * 20 + f"Cliente: {nome_cliente}\n"
        relatorio += "=" * 80 + "\n\n"
        
        # Tentar buscar de pontos_fidelidade se existir
        try:
            self.db.cursor.execute('''
                SELECT data_movimento, tipo, quantidade, saldo_anterior, saldo_novo, venda_codigo
                FROM pontos_fidelidade
                WHERE cliente_codigo = ?
                ORDER BY data_movimento DESC
            ''', (codigo_cliente,))
            
            movimentos = self.db.cursor.fetchall()
            
            if movimentos:
                relatorio += f"{'Data':<12} {'Tipo':<10} {'Quantidade':<12} {'Saldo Ant.':<12} {'Saldo Novo':<12} {'Venda':<12}\n"
                relatorio += "-" * 70 + "\n"
                
                for mov in movimentos:
                    data, tipo, qtd, saldo_ant, saldo_novo, venda = mov
                    venda = venda or "---"
                    relatorio += f"{data:<12} {tipo:<10} {qtd:<12} {saldo_ant:<12} {saldo_novo:<12} {venda:<12}\n"
            else:
                # Se não tem histórico, mostrar apenas compras com pontos
                self.db.cursor.execute('''
                    SELECT data_venda, id, total, pontos_ganhos
                    FROM vendas
                    WHERE cliente_codigo = ? AND pontos_ganhos > 0
                    ORDER BY data_venda DESC
                ''', (codigo_cliente,))
                
                compras_com_pontos = self.db.cursor.fetchall()
                
                if compras_com_pontos:
                    relatorio += f"{'Data':<12} {'Venda':<8} {'Valor':<12} {'Pontos':<10}\n"
                    relatorio += "-" * 42 + "\n"
                    
                    for compra in compras_com_pontos:
                        data, venda_id, total, pontos = compra
                        relatorio += f"{data:<12} {venda_id:<8} R${total:<9.2f} {pontos:<10}\n"
                else:
                    relatorio += "Nenhum movimento de pontos registrado.\n"
        except:
            relatorio += "Histórico de pontos não disponível.\n"
        
        relatorio += "\n" + "=" * 80 + "\n"
        relatorio += f"SALDO ATUAL DE PONTOS: {saldo_atual}\n"
        
        self.ultimo_relatorio = relatorio
        self.texto_relatorio.insert('1.0', relatorio)
    
    def exportar_csv(self):
        """Exporta o relatório atual para CSV"""
        if not self.ultimo_relatorio:
            messagebox.showwarning("Aviso", "Nenhum relatório gerado para exportar!")
            return
        
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de texto", "*.txt"), ("Arquivo CSV", "*.csv"), ("Todos os arquivos", "*.*")],
            title="Salvar relatório como"
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(self.ultimo_relatorio)
                messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso!\n{arquivo}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
    
    def voltar_menu(self):
        """Volta para o menu principal"""
        self.db.fechar_conexao()
        self.janela.destroy()
        self.menu_principal.deiconify()