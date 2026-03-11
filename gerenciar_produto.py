import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from datetime import datetime

class TelaGerenciarProduto:
    def __init__(self, menu_principal, codigo_produto=None):
        self.menu_principal = menu_principal
        self.codigo_produto = codigo_produto
        self.db = Database()
        self.janela = tk.Toplevel()
        self.janela.title("Sistema de Estoque - Gerenciar Produto")
        self.janela.geometry("700x750")
        self.janela.resizable(False, False)
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 700
        altura = 750
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        self.entries = {}
        self.criar_interface()
        
        if codigo_produto:
            self.carregar_produto()
        
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)
        self.janela.mainloop()
    
    def criar_interface(self):
        # Notebook (abas)
        notebook = ttk.Notebook(self.janela)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ABA 1: Dados do Produto
        frame_dados = ttk.Frame(notebook)
        notebook.add(frame_dados, text="📦 Dados do Produto")
        self.criar_aba_dados(frame_dados)
        
        # ABA 2: Movimentação de Estoque
        frame_mov = ttk.Frame(notebook)
        notebook.add(frame_mov, text="📊 Movimentação")
        self.criar_aba_movimentacao(frame_mov)
        
        # ABA 3: Histórico
        frame_hist = ttk.Frame(notebook)
        notebook.add(frame_hist, text="📜 Histórico")
        self.criar_aba_historico(frame_hist)
    
    def criar_aba_dados(self, parent):
        # Canvas com scroll
        canvas = tk.Canvas(parent)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        frame = tk.Frame(scrollable_frame, padx=30, pady=20)
        frame.pack(expand=True, fill='both')
        
        # Título
        titulo = tk.Label(frame, text="GERENCIAR PRODUTO", 
                          font=("Arial", 16, "bold"), fg="#333")
        titulo.pack(pady=20)
        
        # Campos do formulário
        campos = [
            ("Código de Barras:", "codigo_barras", "entry"),
            ("Nome do Produto:", "nome", "entry"),
            ("Categoria:", "categoria", "combobox"),
            ("Tamanho:", "tamanho", "combobox"),
            ("Cor:", "cor", "entry"),
            ("Quantidade:", "quantidade", "entry"),
            ("Quantidade Mínima:", "quantidade_minima", "entry"),
            ("Preço de Custo (R$):", "preco_custo", "entry"),
            ("Preço de Venda (R$):", "preco_venda", "entry"),
            ("Fornecedor:", "fornecedor", "entry"),
            ("Localização:", "localizacao", "entry")
        ]
        
        for label_text, campo, tipo in campos:
            campo_frame = tk.Frame(frame)
            campo_frame.pack(fill='x', pady=5)
            
            tk.Label(campo_frame, text=label_text, font=("Arial", 10, "bold"),
                    anchor='w').pack(anchor='w')
            
            if tipo == "combobox":
                if campo == "categoria":
                    valores = ["Vestido", "Blusa", "Calça", "Acessório", "Saia", "Camisa", "Bermuda", "Jaqueta"]
                else:  # tamanho
                    valores = ["PP", "P", "M", "G", "GG", "XG", "XXG", "Único"]
                
                entry = ttk.Combobox(campo_frame, values=valores, state='readonly', 
                                    font=("Arial", 10))
                entry.pack(fill='x', pady=5, ipady=3)
            else:
                entry = tk.Entry(campo_frame, font=("Arial", 10), relief='solid', bd=1)
                entry.pack(fill='x', pady=5, ipady=5)
            
            self.entries[campo] = entry
        
        # Frame para botões
        frame_botoes = tk.Frame(frame, bg='#f0f0f0', pady=20)
        frame_botoes.pack(fill='x', pady=30)
        
        # Botão Salvar
        btn_salvar = tk.Button(frame_botoes, text="💾 SALVAR ALTERAÇÕES", 
                               bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                               padx=30, pady=10, command=self.salvar_alteracoes)
        btn_salvar.pack(side='left', padx=10, expand=True)
        
        # Botão Voltar
        btn_voltar = tk.Button(frame_botoes, text="↩️ VOLTAR", 
                               bg="#f44336", fg="white", font=("Arial", 12, "bold"),
                               padx=30, pady=10, command=self.voltar)
        btn_voltar.pack(side='left', padx=10, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def criar_aba_movimentacao(self, parent):
        frame = tk.Frame(parent, padx=20, pady=20)
        frame.pack(expand=True, fill='both')
        
        tk.Label(frame, text="AJUSTAR ESTOQUE", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame para entrada
        entrada_frame = tk.LabelFrame(frame, text="Registrar Movimentação", padx=20, pady=20)
        entrada_frame.pack(fill='x', pady=10)
        
        tk.Label(entrada_frame, text="Quantidade:", font=("Arial", 11)).pack(anchor='w')
        self.mov_quantidade = tk.Entry(entrada_frame, font=("Arial", 11), width=20)
        self.mov_quantidade.pack(fill='x', pady=5)
        
        tk.Label(entrada_frame, text="Motivo:", font=("Arial", 11)).pack(anchor='w')
        self.mov_motivo = tk.Entry(entrada_frame, font=("Arial", 11), width=40)
        self.mov_motivo.pack(fill='x', pady=5)
        
        tk.Label(entrada_frame, text="Número da Nota (opcional):", font=("Arial", 11)).pack(anchor='w')
        self.mov_nota = tk.Entry(entrada_frame, font=("Arial", 11), width=30)
        self.mov_nota.pack(fill='x', pady=5)
        
        # Botões
        botoes_frame = tk.Frame(entrada_frame)
        botoes_frame.pack(pady=20)
        
        btn_entrada = tk.Button(botoes_frame, text="📥 ENTRADA", 
                                bg="#2196F3", fg="white", font=("Arial", 11, "bold"),
                                padx=20, pady=8, command=lambda: self.movimentar("entrada"))
        btn_entrada.pack(side='left', padx=5)
        
        btn_saida = tk.Button(botoes_frame, text="📤 SAÍDA", 
                              bg="#FF9800", fg="white", font=("Arial", 11, "bold"),
                              padx=20, pady=8, command=lambda: self.movimentar("saida"))
        btn_saida.pack(side='left', padx=5)
        
        btn_ajuste = tk.Button(botoes_frame, text="⚖️ AJUSTE", 
                               bg="#9C27B0", fg="white", font=("Arial", 11, "bold"),
                               padx=20, pady=8, command=lambda: self.movimentar("ajuste"))
        btn_ajuste.pack(side='left', padx=5)
        
        # Estoque atual
        self.estoque_label = tk.Label(frame, text="Estoque atual: --", 
                                      font=("Arial", 12, "bold"))
        self.estoque_label.pack(pady=10)
    
    def criar_aba_historico(self, parent):
        frame = tk.Frame(parent, padx=10, pady=10)
        frame.pack(expand=True, fill='both')
        
        # Treeview para histórico
        colunas = ('Data', 'Hora', 'Tipo', 'Quantidade', 'Anterior', 'Nova', 'Motivo', 'Nota')
        self.tree_historico = ttk.Treeview(frame, columns=colunas, show='headings', height=15)
        
        for col in colunas:
            self.tree_historico.heading(col, text=col)
            self.tree_historico.column(col, width=80)
        
        self.tree_historico.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree_historico.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree_historico.configure(yscrollcommand=scrollbar.set)
    
    def carregar_produto(self):
        """Carrega os dados do produto para edição"""
        self.db.cursor.execute('''
            SELECT * FROM produtos WHERE codigo = ?
        ''', (self.codigo_produto,))
        
        produto = self.db.cursor.fetchone()
        
        if produto:
            # Limpar entradas existentes
            for entry in self.entries.values():
                if isinstance(entry, tk.Entry):
                    entry.delete(0, tk.END)
                elif isinstance(entry, ttk.Combobox):
                    entry.set('')
            
            # Inserir novos valores
            self.entries["codigo_barras"].insert(0, produto[2] or "")
            self.entries["nome"].insert(0, produto[3])
            self.entries["categoria"].set(produto[4])
            self.entries["tamanho"].set(produto[5])
            self.entries["cor"].insert(0, produto[6])
            self.entries["quantidade"].insert(0, str(produto[7]))
            self.entries["quantidade_minima"].insert(0, str(produto[8]))
            self.entries["preco_venda"].insert(0, str(produto[9]))
            self.entries["preco_custo"].insert(0, str(produto[10] or ""))
            self.entries["fornecedor"].insert(0, produto[11])
            self.entries["localizacao"].insert(0, produto[12] or "")
            
            # Atualizar label de estoque
            self.estoque_label.config(text=f"Estoque atual: {produto[7]} unidades")
            
            # Carregar histórico
            self.carregar_historico()
    
    def carregar_historico(self):
        """Carrega o histórico de movimentações"""
        for item in self.tree_historico.get_children():
            self.tree_historico.delete(item)
        
        self.db.cursor.execute('''
            SELECT data_movimento, hora_movimento, tipo, quantidade, 
                   quantidade_anterior, quantidade_nova, motivo, numero_nota
            FROM movimentacoes
            WHERE codigo_produto = ?
            ORDER BY data_movimento DESC, hora_movimento DESC
        ''', (self.codigo_produto,))
        
        movs = self.db.cursor.fetchall()
        
        for mov in movs:
            self.tree_historico.insert('', 'end', values=mov)
    
    def salvar_alteracoes(self):
        """Salva as alterações do produto com validação detalhada"""
        try:
            # Coletar dados
            codigo_barras = self.entries["codigo_barras"].get().strip()
            nome = self.entries["nome"].get().strip()
            categoria = self.entries["categoria"].get().strip()
            tamanho = self.entries["tamanho"].get().strip()
            cor = self.entries["cor"].get().strip()
            quantidade = self.entries["quantidade"].get().strip()
            quantidade_minima = self.entries["quantidade_minima"].get().strip()
            preco_custo = self.entries["preco_custo"].get().strip()
            preco_venda = self.entries["preco_venda"].get().strip()
            fornecedor = self.entries["fornecedor"].get().strip()
            localizacao = self.entries["localizacao"].get().strip()
            
            # VALIDAÇÃO DETALHADA - Campo por campo
            campos_obrigatorios = {
                "Nome do Produto": nome,
                "Categoria": categoria,
                "Tamanho": tamanho,
                "Cor": cor,
                "Quantidade": quantidade,
                "Preço de Venda": preco_venda,
                "Fornecedor": fornecedor
            }
            
            # Verificar campos obrigatórios vazios
            campos_vazios = []
            for nome_campo, valor in campos_obrigatorios.items():
                if not valor:
                    campos_vazios.append(nome_campo)
            
            if campos_vazios:
                messagebox.showerror("Erro de Validação", 
                                   f"Os seguintes campos são obrigatórios:\n\n" + 
                                   "\n".join(f"• {campo}" for campo in campos_vazios))
                return
            
            # VALIDAÇÃO DE QUANTIDADE
            try:
                if not quantidade:
                    messagebox.showerror("Erro", "O campo Quantidade não pode estar vazio!")
                    return
                quantidade = int(quantidade)
                if quantidade < 0:
                    messagebox.showerror("Erro", "Quantidade não pode ser negativa!")
                    return
            except ValueError:
                messagebox.showerror("Erro de Validação", 
                                   f"O campo 'Quantidade' deve conter um número inteiro válido.\n"
                                   f"Valor fornecido: '{quantidade}'")
                return
            
            # VALIDAÇÃO DE QUANTIDADE MÍNIMA
            try:
                if quantidade_minima:
                    quantidade_minima = int(quantidade_minima)
                    if quantidade_minima < 0:
                        messagebox.showerror("Erro", "Quantidade mínima não pode ser negativa!")
                        return
                else:
                    quantidade_minima = 5  # valor padrão
            except ValueError:
                messagebox.showerror("Erro de Validação", 
                                   f"O campo 'Quantidade Mínima' deve conter um número inteiro válido.\n"
                                   f"Valor fornecido: '{quantidade_minima}'")
                return
            
            # VALIDAÇÃO DE PREÇO DE VENDA
            try:
                if not preco_venda:
                    messagebox.showerror("Erro", "O campo Preço de Venda não pode estar vazio!")
                    return
                # Substituir vírgula por ponto e remover espaços
                preco_venda = preco_venda.replace(',', '.').strip()
                preco_venda = float(preco_venda)
                if preco_venda <= 0:
                    messagebox.showerror("Erro", "Preço de venda deve ser maior que zero!")
                    return
            except ValueError:
                messagebox.showerror("Erro de Validação", 
                                   f"O campo 'Preço de Venda' deve conter um número válido.\n"
                                   f"Use ponto ou vírgula como separador decimal.\n"
                                   f"Valor fornecido: '{preco_venda}'")
                return
            
            # VALIDAÇÃO DE PREÇO DE CUSTO (opcional)
            try:
                if preco_custo:
                    preco_custo = preco_custo.replace(',', '.').strip()
                    preco_custo = float(preco_custo)
                    if preco_custo < 0:
                        messagebox.showerror("Erro", "Preço de custo não pode ser negativo!")
                        return
                else:
                    preco_custo = 0.0
            except ValueError:
                messagebox.showerror("Erro de Validação", 
                                   f"O campo 'Preço de Custo' deve conter um número válido.\n"
                                   f"Use ponto ou vírgula como separador decimal.\n"
                                   f"Valor fornecido: '{preco_custo}'")
                return
            
            # Se chegou até aqui, todos os campos estão válidos
            from datetime import datetime
            data_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            if self.codigo_produto:  # UPDATE
                self.db.cursor.execute('''
                    UPDATE produtos SET
                        codigo_barras = ?, nome = ?, categoria = ?, tamanho = ?, cor = ?,
                        quantidade = ?, quantidade_minima = ?, preco_custo = ?, 
                        preco_venda = ?, fornecedor = ?, localizacao = ?, data_atualizacao = ?
                    WHERE codigo = ?
                ''', (codigo_barras, nome, categoria, tamanho, cor, quantidade, 
                      quantidade_minima, preco_custo, preco_venda, fornecedor, 
                      localizacao, data_atualizacao, self.codigo_produto))
                
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                
            else:  # INSERT (novo produto)
                from models import Produto
                produto = Produto(nome, categoria, tamanho, cor, quantidade, preco_venda,
                                 fornecedor, codigo_barras, preco_custo, quantidade_minima, localizacao)
                codigo = produto.gerar_codigo(self.db)
                
                if not codigo_barras:
                    codigo_barras = produto.gerar_codigo_barras()
                
                self.db.cursor.execute('''
                    INSERT INTO produtos 
                    (codigo, codigo_barras, nome, categoria, tamanho, cor, quantidade,
                     quantidade_minima, preco_custo, preco_venda, fornecedor, localizacao,
                     data_cadastro, data_atualizacao)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (codigo, codigo_barras, nome, categoria, tamanho, cor, quantidade,
                      quantidade_minima, preco_custo, preco_venda, fornecedor, localizacao,
                      produto.data_cadastro, data_atualizacao))
                
                messagebox.showinfo("Sucesso", f"Produto cadastrado com sucesso!\nCódigo: {codigo}")
            
            self.db.conn.commit()
            self.janela.destroy()  # Fecha a janela após salvar
            from consulta_estoque import TelaConsulta
            TelaConsulta(self.menu_principal)  # Reabre a consulta
            
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Erro ao salvar: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def movimentar(self, tipo):
        """Registra movimentação de estoque"""
        if not self.codigo_produto:
            messagebox.showerror("Erro", "Carregue um produto primeiro!")
            return
        
        try:
            quantidade = int(self.mov_quantidade.get())
            if quantidade <= 0:
                messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
                return
            
            motivo = self.mov_motivo.get().strip()
            numero_nota = self.mov_nota.get().strip()
            
            # Buscar quantidade atual
            self.db.cursor.execute('''
                SELECT quantidade FROM produtos WHERE codigo = ?
            ''', (self.codigo_produto,))
            
            quantidade_atual = self.db.cursor.fetchone()[0]
            
            # Calcular nova quantidade
            if tipo == "entrada":
                nova_quantidade = quantidade_atual + quantidade
            elif tipo == "saida":
                if quantidade > quantidade_atual:
                    messagebox.showerror("Erro", "Quantidade insuficiente em estoque!")
                    return
                nova_quantidade = quantidade_atual - quantidade
            else:  # ajuste
                nova_quantidade = quantidade  # define diretamente
            
            # Atualizar estoque
            self.db.cursor.execute('''
                UPDATE produtos SET quantidade = ? WHERE codigo = ?
            ''', (nova_quantidade, self.codigo_produto))
            
            # Registrar movimentação
            self.db.registrar_movimentacao(
                self.codigo_produto, tipo, quantidade, quantidade_atual, 
                nova_quantidade, motivo, numero_nota, "admin"
            )
            
            self.db.conn.commit()
            
            messagebox.showinfo("Sucesso", 
                f"Movimentação registrada!\n"
                f"Estoque anterior: {quantidade_atual}\n"
                f"Estoque atual: {nova_quantidade}")
            
            # Limpar campos
            self.mov_quantidade.delete(0, tk.END)
            self.mov_motivo.delete(0, tk.END)
            self.mov_nota.delete(0, tk.END)
            
            # Atualizar labels e histórico
            self.estoque_label.config(text=f"Estoque atual: {nova_quantidade} unidades")
            self.carregar_historico()
            
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {str(e)}")
    
    def voltar(self):
        self.db.fechar_conexao()
        self.janela.destroy()
        self.menu_principal.deiconify()