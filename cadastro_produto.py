import tkinter as tk
from tkinter import ttk, messagebox
from models import Produto
from database import Database

class TelaCadastro:
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.db = Database()
        self.janela = tk.Toplevel()
        self.janela.title("StockMaster - Cadastrar Produto")
        self.janela.geometry("600x700")
        self.janela.resizable(False, False)
        self.janela.configure(bg='#ff751f')
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 600
        altura = 700
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        self.entries = {}
        self.criar_interface()
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
            text="📦 CADASTRO DE PRODUTO",
            font=("Arial", 18, "bold"),
            fg=cor_primaria,
            bg='white'
        )
        titulo.pack(pady=20)
        
        # Subtítulo
        subtitulo = tk.Label(
            frame_conteudo,
            text="Preencha todos os campos obrigatórios (*)",
            font=("Arial", 10, "italic"),
            fg='#666666',
            bg='white'
        )
        subtitulo.pack(pady=(0, 20))
        
        # Canvas com scroll
        canvas = tk.Canvas(frame_conteudo, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_conteudo, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Formulário
        frame_form = tk.Frame(scrollable_frame, bg='white', padx=30, pady=10)
        frame_form.pack(fill='both', expand=True)
        
        # Campos
        campos = [
            ("Código de Barras:", "codigo_barras", "entry"),
            ("Nome do Produto:*", "nome", "entry"),
            ("Categoria:*", "categoria", "combobox"),
            ("Tamanho:*", "tamanho", "combobox"),
            ("Cor:*", "cor", "entry"),
            ("Quantidade:*", "quantidade", "entry"),
            ("Quantidade Mínima:", "quantidade_minima", "entry"),
            ("Preço de Custo (R$):", "preco_custo", "entry"),
            ("Preço de Venda (R$):*", "preco_venda", "entry"),
            ("Fornecedor:*", "fornecedor", "entry"),
            ("Localização:", "localizacao", "entry")
        ]
        
        for label_text, campo, tipo in campos:
            # Label
            tk.Label(
                frame_form,
                text=label_text,
                font=("Arial", 10, "bold"),
                fg='#333333',
                bg='white'
            ).pack(anchor='w', pady=(10, 2))
            
            # Campo
            if tipo == "combobox":
                if campo == "categoria":
                    valores = ["Vestido", "Blusa", "Calça", "Acessório", "Saia", "Camisa", "Bermuda", "Jaqueta"]
                else:  # tamanho
                    valores = ["PP", "P", "M", "G", "GG", "XG", "XXG", "Único"]
                
                entry = ttk.Combobox(
                    frame_form,
                    values=valores,
                    state='readonly',
                    font=("Arial", 10)
                )
            else:
                entry = tk.Entry(
                    frame_form,
                    font=("Arial", 10),
                    relief='solid',
                    bd=1,
                    highlightbackground='#dddddd'
                )
            
            entry.pack(fill='x', pady=(0, 5), ipady=5)
            self.entries[campo] = entry
        
        # Frame para botões
        frame_botoes = tk.Frame(frame_conteudo, bg='white', pady=20)
        frame_botoes.pack(fill='x')
        
        # Botão Salvar
        btn_salvar = tk.Button(
            frame_botoes,
            text="💾 SALVAR PRODUTO",
            font=("Arial", 12, "bold"),
            bg=cor_botao,
            fg=cor_texto_botao,
            bd=1,
            relief='solid',
            padx=30,
            pady=10,
            cursor='hand2',
            command=self.salvar_produto
        )
        btn_salvar.pack(side='left', padx=5, expand=True, fill='x')
        
        # Botão Voltar
        btn_voltar = tk.Button(
            frame_botoes,
            text="↩️ VOLTAR",
            font=("Arial", 12, "bold"),
            bg=cor_botao,
            fg=cor_texto_botao,
            bd=1,
            relief='solid',
            padx=30,
            pady=10,
            cursor='hand2',
            command=self.voltar_menu
        )
        btn_voltar.pack(side='left', padx=5, expand=True, fill='x')
        
        # Efeito hover nos botões
        for btn in [btn_salvar, btn_voltar]:
            def on_enter(e, b=btn):
                b['bg'] = '#f5f5f5'
                b['fg'] = '#e65c00'
            
            def on_leave(e, b=btn):
                b['bg'] = cor_botao
                b['fg'] = cor_texto_botao
            
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
        
        # Empacotar canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def salvar_produto(self):
        db = Database()
        
        try:
            nome = self.entries["nome"].get().strip()
            categoria = self.entries["categoria"].get().strip()
            tamanho = self.entries["tamanho"].get().strip()
            cor = self.entries["cor"].get().strip()
            quantidade = self.entries["quantidade"].get().strip()
            preco = self.entries["preco_venda"].get().strip()
            fornecedor = self.entries["fornecedor"].get().strip()
            
            if not all([nome, categoria, tamanho, cor, quantidade, preco, fornecedor]):
                messagebox.showerror("Erro", "Todos os campos obrigatórios devem ser preenchidos!")
                db.fechar_conexao()
                return
            
            try:
                quantidade = int(quantidade)
                if quantidade <= 0:
                    messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
                    db.fechar_conexao()
                    return
            except ValueError:
                messagebox.showerror("Erro", "Quantidade deve ser um número inteiro!")
                db.fechar_conexao()
                return
            
            try:
                preco = float(preco.replace(',', '.'))
                if preco <= 0:
                    messagebox.showerror("Erro", "Preço deve ser maior que zero!")
                    db.fechar_conexao()
                    return
            except ValueError:
                messagebox.showerror("Erro", "Preço inválido!")
                db.fechar_conexao()
                return
            
            produto = Produto(nome, categoria, tamanho, cor, quantidade, preco, fornecedor)
            codigo = produto.gerar_codigo(db)
            
            db.cursor.execute('''
                INSERT INTO produtos (codigo, codigo_barras, nome, categoria, tamanho, cor, 
                                     quantidade, preco_venda, fornecedor, data_cadastro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (codigo, self.entries["codigo_barras"].get().strip(), nome, categoria, 
                  tamanho, cor, quantidade, preco, fornecedor, produto.data_cadastro))
            
            db.conn.commit()
            db.fechar_conexao()
            
            messagebox.showinfo("Sucesso", f"Produto cadastrado com sucesso!\nCódigo: {codigo}")
            
            for entry in self.entries.values():
                if isinstance(entry, tk.Entry):
                    entry.delete(0, tk.END)
                elif isinstance(entry, ttk.Combobox):
                    entry.set('')
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar produto: {str(e)}")
            db.fechar_conexao()
    
    def voltar_menu(self):
        self.janela.destroy()
        self.menu_principal.deiconify()