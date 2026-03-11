import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class TelaConsulta:
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.db = Database()
        self.janela = tk.Toplevel()
        self.janela.title("Sistema de Estoque - Consultar Estoque")
        self.janela.geometry("900x500")
        
        # Centralizar a janela
        self.janela.update_idletasks()
        largura = 900
        altura = 500
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.criar_interface()
        self.carregar_produtos()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar_menu)
        self.janela.mainloop()
    
    def criar_interface(self):
        # Frame superior (busca)
        frame_busca = tk.Frame(self.janela, bg='#f0f0f0', padx=10, pady=10)
        frame_busca.pack(fill='x')
        
        tk.Label(frame_busca, text="Buscar:", bg='#f0f0f0', font=("Arial", 10)).pack(side='left', padx=5)
        
        self.busca_entry = tk.Entry(frame_busca, font=("Arial", 10), width=30)
        self.busca_entry.pack(side='left', padx=5)
        
        self.filtro_var = tk.StringVar(value="todos")
        filtros = [("Todos", "todos"), ("Nome", "nome"), ("Categoria", "categoria"), ("Código", "codigo")]
        
        for texto, valor in filtros:
            rb = tk.Radiobutton(frame_busca, text=texto, variable=self.filtro_var, 
                              value=valor, bg='#f0f0f0', font=("Arial", 9))
            rb.pack(side='left', padx=5)
        
        btn_buscar = tk.Button(frame_busca, text="BUSCAR", bg="#2196F3", fg="white",
                              font=("Arial", 9, "bold"), command=self.buscar_produtos)
        btn_buscar.pack(side='left', padx=5)
        
        btn_limpar = tk.Button(frame_busca, text="LIMPAR", bg="#FF9800", fg="white",
                              font=("Arial", 9, "bold"), command=self.limpar_busca)
        btn_limpar.pack(side='left', padx=5)
        
        # Frame da tabela
        frame_tabela = tk.Frame(self.janela)
        frame_tabela.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbars
        scroll_y = tk.Scrollbar(frame_tabela)
        scroll_y.pack(side='right', fill='y')
        
        scroll_x = tk.Scrollbar(frame_tabela, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')
        
        # Treeview
        colunas = ('Código', 'Nome', 'Categoria', 'Tamanho', 'Cor', 'Quantidade', 'Preço', 'Fornecedor')
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show='headings',
                                 yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Configurar colunas
        for col in colunas:
            self.tree.heading(col, text=col)
            if col == 'Nome':
                self.tree.column(col, width=200)
            elif col == 'Preço':
                self.tree.column(col, width=100)
            else:
                self.tree.column(col, width=120)
        
        self.tree.pack(fill='both', expand=True)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Tags para cores
        self.tree.tag_configure('estoque_baixo', background='#ffcdd2')
        
        # Vincular duplo clique para editar
        self.tree.bind('<Double-1>', self.abrir_para_editar)
        
        # Frame inferior (botões)
        frame_botoes = tk.Frame(self.janela, pady=10)
        frame_botoes.pack()
        
        btn_atualizar = tk.Button(frame_botoes, text="ATUALIZAR", bg="#4CAF50", fg="white",
                                 font=("Arial", 10, "bold"), padx=20, command=self.carregar_produtos)
        btn_atualizar.pack(side='left', padx=5)
        
        # Botão para editar produto selecionado
        btn_editar = tk.Button(frame_botoes, text="EDITAR SELECIONADO", bg="#FF9800", fg="white",
                              font=("Arial", 10, "bold"), padx=20, command=self.editar_selecionado)
        btn_editar.pack(side='left', padx=5)
        
        btn_voltar = tk.Button(frame_botoes, text="VOLTAR", bg="#f44336", fg="white",
                              font=("Arial", 10, "bold"), padx=20, command=self.voltar_menu)
        btn_voltar.pack(side='left', padx=5)
    
    # Abrir para editar com duplo clique
    def abrir_para_editar(self, event):
        """Abre o produto selecionado para edição quando dá duplo clique"""
        try:
            # Pegar o item selecionado
            item = self.tree.selection()[0]
            # Pegar o código do produto (primeira coluna)
            codigo = self.tree.item(item, 'values')[0]
            
            # Fechar a tela de consulta
            self.janela.destroy()
            
            # Abrir a tela de gerenciamento com o código do produto
            from gerenciar_produto import TelaGerenciarProduto
            TelaGerenciarProduto(self.menu_principal, codigo)
            
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um produto para editar!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir produto: {str(e)}")
    
    # Editar produto selecionado (pelo botão)
    def editar_selecionado(self):
        """Abre o produto selecionado para edição quando clica no botão"""
        try:
            # Pegar o item selecionado
            item = self.tree.selection()[0]
            # Pegar o código do produto
            codigo = self.tree.item(item, 'values')[0]
            
            # Fechar a tela de consulta
            self.janela.destroy()
            
            # Abrir a tela de gerenciamento
            from gerenciar_produto import TelaGerenciarProduto
            TelaGerenciarProduto(self.menu_principal, codigo)
            
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um produto para editar!")
    
    def carregar_produtos(self):
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar todos os produtos
        self.db.cursor.execute('''
            SELECT codigo, nome, categoria, tamanho, cor, quantidade, preco_venda, fornecedor
            FROM produtos
            ORDER BY nome
        ''')
        
        produtos = self.db.cursor.fetchall()
        
        for produto in produtos:
            codigo, nome, categoria, tamanho, cor, quantidade, preco, fornecedor = produto
            
            # Formatar preço
            preco_formatado = f"R$ {preco:.2f}"
            
            # Inserir na tree
            item = self.tree.insert('', 'end', values=(codigo, nome, categoria, tamanho, 
                                                       cor, quantidade, preco_formatado, fornecedor))
            
            # Destacar em vermelho se estoque baixo
            if quantidade < 5:
                self.tree.item(item, tags=('estoque_baixo',))
    
    def buscar_produtos(self):
        termo = self.busca_entry.get()
        filtro = self.filtro_var.get()
        
        if not termo:
            self.carregar_produtos()
            return
        
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Construir query baseada no filtro
        if filtro == "todos":
            query = '''
                SELECT codigo, nome, categoria, tamanho, cor, quantidade, preco_venda, fornecedor
                FROM produtos
                WHERE nome LIKE ? OR categoria LIKE ? OR codigo LIKE ?
                ORDER BY nome
            '''
            params = (f'%{termo}%', f'%{termo}%', f'%{termo}%')
        else:
            coluna = filtro
            query = f'''
                SELECT codigo, nome, categoria, tamanho, cor, quantidade, preco_venda, fornecedor
                FROM produtos
                WHERE {coluna} LIKE ?
                ORDER BY nome
            '''
            params = (f'%{termo}%',)
        
        self.db.cursor.execute(query, params)
        produtos = self.db.cursor.fetchall()
        
        for produto in produtos:
            codigo, nome, categoria, tamanho, cor, quantidade, preco, fornecedor = produto
            preco_formatado = f"R$ {preco:.2f}"
            
            item = self.tree.insert('', 'end', values=(codigo, nome, categoria, tamanho, 
                                                       cor, quantidade, preco_formatado, fornecedor))
            
            if quantidade < 5:
                self.tree.item(item, tags=('estoque_baixo',))
    
    def limpar_busca(self):
        self.busca_entry.delete(0, tk.END)
        self.filtro_var.set("todos")
        self.carregar_produtos()
    
    def voltar_menu(self):
        self.db.fechar_conexao()
        self.janela.destroy()
        self.menu_principal.deiconify()
