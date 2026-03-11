import tkinter as tk
from tkinter import ttk, messagebox
from models import Produto
from database import Database

class TelaCadastro:
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.janela = tk.Toplevel()
        self.janela.title("Sistema de Estoque - Cadastrar Produto")
        self.janela.geometry("550x700")  # Aumentei um pouco
        self.janela.resizable(False, False)
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 550
        altura = 700
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        # Trazer para frente
        self.janela.lift()
        self.janela.focus_force()
        
        self.entries = {}
        self.criar_formulario()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar_menu)
        self.janela.mainloop()
    
    def criar_formulario(self):
        # Canvas com scrollbar para garantir que tudo apareça
        canvas = tk.Canvas(self.janela)
        scrollbar = tk.Scrollbar(self.janela, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame principal dentro do scrollable_frame
        frame = tk.Frame(scrollable_frame, padx=30, pady=20)
        frame.pack(expand=True, fill='both')
        
        # Título
        titulo = tk.Label(frame, text="CADASTRO DE PRODUTO", 
                          font=("Arial", 18, "bold"), fg="#333")
        titulo.pack(pady=20)
        
        # Instruções
        instrucoes = tk.Label(frame, text="Preencha todos os campos abaixo:", 
                             font=("Arial", 10, "italic"), fg="#666")
        instrucoes.pack(pady=(0, 20))
        
        # Campos do formulário
        campos = [
            ("Nome do Produto:", "nome", "entry"),
            ("Categoria:", "categoria", "combobox"),
            ("Tamanho:", "tamanho", "combobox"),
            ("Cor:", "cor", "entry"),
            ("Quantidade:", "quantidade", "entry"),
            ("Preço de Venda (R$):", "preco", "entry"),
            ("Fornecedor:", "fornecedor", "entry")
        ]
        
        for i, (label_text, campo, tipo) in enumerate(campos):
            # Frame para cada campo (melhor organização)
            campo_frame = tk.Frame(frame)
            campo_frame.pack(fill='x', pady=5)
            
            # Label
            tk.Label(campo_frame, text=label_text, font=("Arial", 10, "bold"),
                    anchor='w').pack(anchor='w')
            
            # Entry ou Combobox
            if tipo == "combobox":
                if campo == "categoria":
                    valores = ["Vestido", "Blusa", "Calça", "Acessório", "Saia", "Camisa"]
                else:  # tamanho
                    valores = ["PP", "P", "M", "G", "GG", "XG"]
                
                entry = ttk.Combobox(campo_frame, values=valores, state='readonly', 
                                    font=("Arial", 10))
                entry.pack(fill='x', pady=5, ipady=3)  # ipady dá altura
            else:
                entry = tk.Entry(campo_frame, font=("Arial", 10), relief='solid', bd=1)
                entry.pack(fill='x', pady=5, ipady=5)  # ipady dá altura
            
            self.entries[campo] = entry
        
        # Frame para botões (com fundo colorido para destacar)
        frame_botoes = tk.Frame(frame, bg='#f0f0f0', pady=20)
        frame_botoes.pack(fill='x', pady=30)
        
        # Botão Salvar (VERDE BEM VISÍVEL)
        btn_salvar = tk.Button(frame_botoes, text="✅ SALVAR PRODUTO", 
                               bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                               padx=30, pady=10, relief='raised', bd=3,
                               command=self.salvar_produto)
        btn_salvar.pack(side='left', padx=10, expand=True)
        
        # Botão Voltar (VERMELHO)
        btn_voltar = tk.Button(frame_botoes, text="↩️ VOLTAR", 
                               bg="#f44336", fg="white", font=("Arial", 12, "bold"),
                               padx=30, pady=10, relief='raised', bd=3,
                               command=self.voltar_menu)
        btn_voltar.pack(side='left', padx=10, expand=True)
        
        # Empacotar o canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def salvar_produto(self):
        print("🔵 Botão SALVAR clicado!")
        
        db = Database()
        
        try:
            # Coletar dados
            nome = self.entries["nome"].get().strip()
            categoria = self.entries["categoria"].get().strip()
            tamanho = self.entries["tamanho"].get().strip()
            cor = self.entries["cor"].get().strip()
            quantidade = self.entries["quantidade"].get().strip()
            preco = self.entries["preco"].get().strip()
            fornecedor = self.entries["fornecedor"].get().strip()
            
            # Validar campos
            if not all([nome, categoria, tamanho, cor, quantidade, preco, fornecedor]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                db.fechar_conexao()
                return
            
            # Validar quantidade
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
            
            # Validar preço
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
            
            # Criar objeto produto
            produto = Produto(nome, categoria, tamanho, cor, quantidade, preco, fornecedor)
            codigo = produto.gerar_codigo(db)
            
            # Inserir no banco
            db.cursor.execute('''
                INSERT INTO produtos (codigo, nome, categoria, tamanho, cor, 
                                     quantidade, preco_venda, fornecedor, data_cadastro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (codigo, nome, categoria, tamanho, cor, quantidade, preco, fornecedor, produto.data_cadastro))
            
            db.conn.commit()
            
            messagebox.showinfo("Sucesso", f"Produto cadastrado com sucesso!\nCódigo: {codigo}")
            
            # Limpar campos
            for entry in self.entries.values():
                if isinstance(entry, tk.Entry):
                    entry.delete(0, tk.END)
                elif isinstance(entry, ttk.Combobox):
                    entry.set('')
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar produto: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            db.fechar_conexao()
    
    def voltar_menu(self):
        self.janela.destroy()
        self.menu_principal.deiconify()