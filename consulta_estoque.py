import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class TelaConsulta:
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.db = Database()
        self.janela = tk.Toplevel()
        self.janela.title("StockMaster - Consultar Estoque")
        self.janela.geometry("1100x600")
        self.janela.resizable(False, False)
        self.janela.configure(bg='#ff751f')
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 1100
        altura = 600
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        self.criar_interface()
        self.carregar_produtos()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar_menu)
        self.janela.mainloop()
    
    def criar_interface(self):
        # Cores
        cor_primaria = '#ff751f'
        cor_botao = '#ffffff'
        cor_texto_botao = '#ff751f'
        
        # Frame branco principal
        frame_conteudo = tk.Frame(self.janela, bg='white', bd=0)
        frame_conteudo.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            frame_conteudo,
            text="🔍 CONSULTAR ESTOQUE",
            font=("Arial", 18, "bold"),
            fg=cor_primaria,
            bg='white'
        )
        titulo.pack(pady=20)
        
        # Frame de busca
        frame_busca = tk.Frame(frame_conteudo, bg='white')
        frame_busca.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            frame_busca,
            text="Buscar:",
            font=("Arial", 11),
            bg='white',
            fg='#333333'
        ).pack(side='left', padx=(0, 10))
        
        self.busca_entry = tk.Entry(
            frame_busca,
            font=("Arial", 11),
            width=25,
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.busca_entry.pack(side='left', padx=(0, 10), ipady=5)
        
        self.filtro_var = tk.StringVar(value="todos")
        filtros = [("Todos", "todos"), ("Nome", "nome"), ("Categoria", "categoria"), 
                   ("Código", "codigo"), ("Cód. Barras", "codigo_barras")]
        
        for texto, valor in filtros:
            rb = tk.Radiobutton(
                frame_busca,
                text=texto,
                variable=self.filtro_var,
                value=valor,
                bg='white',
                fg='#333333',
                font=("Arial", 9),
                cursor='hand2'
            )
            rb.pack(side='left', padx=5)
        
        btn_buscar = tk.Button(
            frame_busca,
            text="🔍 BUSCAR",
            bg=cor_botao,
            fg=cor_texto_botao,
            font=("Arial", 9, "bold"),
            bd=1,
            relief='solid',
            padx=10,
            pady=5,
            cursor='hand2',
            command=self.buscar_produtos
        )
        btn_buscar.pack(side='left', padx=5)
        
        btn_limpar = tk.Button(
            frame_busca,
            text="✖ LIMPAR",
            bg=cor_botao,
            fg=cor_texto_botao,
            font=("Arial", 9, "bold"),
            bd=1,
            relief='solid',
            padx=10,
            pady=5,
            cursor='hand2',
            command=self.limpar_busca
        )
        btn_limpar.pack(side='left', padx=5)
        
        # Frame da tabela
        frame_tabela = tk.Frame(frame_conteudo, bg='white')
        frame_tabela.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbars
        scroll_y = tk.Scrollbar(frame_tabela)
        scroll_y.pack(side='right', fill='y')
        
        scroll_x = tk.Scrollbar(frame_tabela, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')
        
        # Treeview
        colunas = ('Código', 'Cód. Barras', 'Nome', 'Categoria', 'Tamanho', 'Cor', 
                   'Quantidade', 'Preço', 'Fornecedor')
        self.tree = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )
        
        # Configurar colunas
        for col in colunas:
            self.tree.heading(col, text=col)
        
        self.tree.column('Código', width=100)
        self.tree.column('Cód. Barras', width=120)
        self.tree.column('Nome', width=200)
        self.tree.column('Categoria', width=100)
        self.tree.column('Tamanho', width=80)
        self.tree.column('Cor', width=100)
        self.tree.column('Quantidade', width=80)
        self.tree.column('Preço', width=100)
        self.tree.column('Fornecedor', width=150)
        
        self.tree.pack(fill='both', expand=True)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Tags para cores
        self.tree.tag_configure('estoque_baixo', background='#ffe5e5')
        
        # Bind para duplo clique
        self.tree.bind('<Double-1>', self.abrir_para_editar)
        
        # Frame de botões inferiores
        frame_botoes = tk.Frame(frame_conteudo, bg='white', pady=15)
        frame_botoes.pack(fill='x')
        
        btn_atualizar = tk.Button(
            frame_botoes,
            text="🔄 ATUALIZAR",
            bg=cor_botao,
            fg=cor_texto_botao,
            font=("Arial", 10, "bold"),
            bd=1,
            relief='solid',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.carregar_produtos
        )
        btn_atualizar.pack(side='left', padx=5, expand=True, fill='x')
        
        btn_editar = tk.Button(
            frame_botoes,
            text="✏️ EDITAR SELECIONADO",
            bg=cor_botao,
            fg=cor_texto_botao,
            font=("Arial", 10, "bold"),
            bd=1,
            relief='solid',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.editar_selecionado
        )
        btn_editar.pack(side='left', padx=5, expand=True, fill='x')
        
        btn_voltar = tk.Button(
            frame_botoes,
            text="↩️ VOLTAR",
            bg=cor_botao,
            fg=cor_texto_botao,
            font=("Arial", 10, "bold"),
            bd=1,
            relief='solid',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.voltar_menu
        )
        btn_voltar.pack(side='left', padx=5, expand=True, fill='x')
        
        # Efeito hover nos botões
        for btn in [btn_buscar, btn_limpar, btn_atualizar, btn_editar, btn_voltar]:
            def on_enter(e, b=btn):
                b['bg'] = '#f5f5f5'
                b['fg'] = '#e65c00'
            
            def on_leave(e, b=btn):
                b['bg'] = cor_botao
                b['fg'] = cor_texto_botao
            
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
    
    def carregar_produtos(self):
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.db.cursor.execute('''
            SELECT codigo, codigo_barras, nome, categoria, tamanho, cor, 
                   quantidade, preco_venda, fornecedor
            FROM produtos
            ORDER BY nome
        ''')
        
        produtos = self.db.cursor.fetchall()
        
        for produto in produtos:
            codigo, codigo_barras, nome, categoria, tamanho, cor, quantidade, preco, fornecedor = produto
            preco_formatado = f"R$ {preco:.2f}"
            codigo_barras = codigo_barras or ""
            
            item = self.tree.insert('', 'end', values=(
                codigo, codigo_barras, nome, categoria, tamanho, cor,
                quantidade, preco_formatado, fornecedor
            ))
            
            if quantidade < 5:
                self.tree.item(item, tags=('estoque_baixo',))
    
    def buscar_produtos(self):
        termo = self.busca_entry.get()
        filtro = self.filtro_var.get()
        
        if not termo:
            self.carregar_produtos()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if filtro == "todos":
            query = '''
                SELECT codigo, codigo_barras, nome, categoria, tamanho, cor, 
                       quantidade, preco_venda, fornecedor
                FROM produtos
                WHERE nome LIKE ? OR categoria LIKE ? OR codigo LIKE ? OR codigo_barras LIKE ?
                ORDER BY nome
            '''
            params = (f'%{termo}%', f'%{termo}%', f'%{termo}%', f'%{termo}%')
        elif filtro == "codigo":
            query = '''
                SELECT codigo, codigo_barras, nome, categoria, tamanho, cor, 
                       quantidade, preco_venda, fornecedor
                FROM produtos
                WHERE codigo LIKE ? OR codigo_barras LIKE ?
                ORDER BY nome
            '''
            params = (f'%{termo}%', f'%{termo}%')
        else:
            coluna = filtro
            query = f'''
                SELECT codigo, codigo_barras, nome, categoria, tamanho, cor, 
                       quantidade, preco_venda, fornecedor
                FROM produtos
                WHERE {coluna} LIKE ?
                ORDER BY nome
            '''
            params = (f'%{termo}%',)
        
        self.db.cursor.execute(query, params)
        produtos = self.db.cursor.fetchall()
        
        for produto in produtos:
            codigo, codigo_barras, nome, categoria, tamanho, cor, quantidade, preco, fornecedor = produto
            preco_formatado = f"R$ {preco:.2f}"
            codigo_barras = codigo_barras or ""
            
            item = self.tree.insert('', 'end', values=(
                codigo, codigo_barras, nome, categoria, tamanho, cor,
                quantidade, preco_formatado, fornecedor
            ))
            
            if quantidade < 5:
                self.tree.item(item, tags=('estoque_baixo',))
    
    def limpar_busca(self):
        self.busca_entry.delete(0, tk.END)
        self.filtro_var.set("todos")
        self.carregar_produtos()
    
    def abrir_para_editar(self, event):
        self.editar_selecionado()
    
    def editar_selecionado(self):
        try:
            item = self.tree.selection()[0]
            codigo = self.tree.item(item, 'values')[0]
            
            self.janela.destroy()
            
            from gerenciar_produto import TelaGerenciarProduto
            TelaGerenciarProduto(self.menu_principal, codigo)
            
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um produto para editar!")
    
    def voltar_menu(self):
        self.db.fechar_conexao()
        self.janela.destroy()
        self.menu_principal.deiconify()