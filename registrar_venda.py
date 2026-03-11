import tkinter as tk
from tkinter import messagebox
from database import Database
from models import Venda
from datetime import datetime

class TelaVenda:
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.db = Database()
        self.janela = tk.Toplevel()
        self.janela.title("Sistema de Estoque - Registrar Venda")
        self.janela.geometry("600x550")  # Aumentei a janela
        self.janela.resizable(False, False)
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 600
        altura = 550
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        # Trazer para frente
        self.janela.lift()
        self.janela.focus_force()
        
        self.produto_atual = None
        self.criar_interface()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar_menu)
        self.janela.mainloop()
    
    def criar_interface(self):
        # Frame principal com scrollbar
        canvas = tk.Canvas(self.janela)
        scrollbar = tk.Scrollbar(self.janela, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame principal
        frame = tk.Frame(scrollable_frame, padx=30, pady=20)
        frame.pack(expand=True, fill='both')
        
        # Título
        titulo = tk.Label(frame, text="REGISTRAR VENDA", 
                          font=("Arial", 18, "bold"), fg="#333")
        titulo.pack(pady=20)
        
        # Data e hora atual
        agora = datetime.now()
        data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
        tk.Label(frame, text=f"Data/Hora: {data_hora}", font=("Arial", 12, "italic"),
                fg="#666").pack(pady=5)
        
        # FRAME 1: Buscar Produto
        frame_busca = tk.LabelFrame(frame, text="1. BUSCAR PRODUTO", 
                                   font=("Arial", 11, "bold"),
                                   padx=15, pady=15, bg='#e3f2fd')
        frame_busca.pack(fill='x', pady=10)
        
        tk.Label(frame_busca, text="Código do Produto:", font=("Arial", 11)).pack(anchor='w')
        
        self.codigo_entry = tk.Entry(frame_busca, font=("Arial", 11), width=30, 
                                     relief='solid', bd=1)
        self.codigo_entry.pack(fill='x', pady=5, ipady=5)
        
        btn_buscar = tk.Button(frame_busca, text="🔍 BUSCAR PRODUTO", 
                              bg="#2196F3", fg="white", font=("Arial", 11, "bold"),
                              padx=20, pady=8, command=self.buscar_produto)
        btn_buscar.pack(pady=10)
        
        # FRAME 2: Informações do Produto
        self.frame_info = tk.LabelFrame(frame, text="2. INFORMAÇÕES DO PRODUTO", 
                                       font=("Arial", 11, "bold"),
                                       padx=15, pady=15, bg='#fff3e0')
        self.frame_info.pack(fill='x', pady=10)
        
        self.info_text = tk.Text(self.frame_info, height=6, width=50, 
                                 font=("Courier", 10), bg='white', 
                                 relief='solid', bd=1)
        self.info_text.pack(fill='x', pady=5)
        self.info_text.config(state='disabled')
        
        # FRAME 3: Registrar Venda
        self.frame_venda = tk.LabelFrame(frame, text="3. REGISTRAR VENDA", 
                                        font=("Arial", 11, "bold"),
                                        padx=15, pady=15, bg='#e8f5e8')
        self.frame_venda.pack(fill='x', pady=10)
        
        tk.Label(self.frame_venda, text="Quantidade:", font=("Arial", 11)).pack(anchor='w')
        
        self.quantidade_entry = tk.Entry(self.frame_venda, font=("Arial", 11), width=20,
                                        relief='solid', bd=1)
        self.quantidade_entry.pack(fill='x', pady=5, ipady=5)
        
        # Label para mostrar o total
        self.total_label = tk.Label(self.frame_venda, text="Total: R$ 0,00", 
                                   font=("Arial", 12, "bold"), fg="#4CAF50")
        self.total_label.pack(pady=10)
        
        # Vincular evento para calcular total enquanto digita
        self.quantidade_entry.bind('<KeyRelease>', self.calcular_total)
        
        # FRAME 4: Botões de Ação
        frame_botoes = tk.Frame(frame, bg='#f0f0f0', pady=20)
        frame_botoes.pack(fill='x', pady=20)
        
        # Botão CONFIRMAR VENDA (VERDE BEM GRANDE)
        btn_vender = tk.Button(frame_botoes, text="✅ CONFIRMAR VENDA", 
                              bg="#4CAF50", fg="white", font=("Arial", 14, "bold"),
                              padx=40, pady=15, relief='raised', bd=3,
                              command=self.registrar_venda)
        btn_vender.pack(side='left', padx=10, expand=True, fill='x')
        
        # Botão VOLTAR
        btn_voltar = tk.Button(frame_botoes, text="↩️ VOLTAR", 
                              bg="#f44336", fg="white", font=("Arial", 14, "bold"),
                              padx=40, pady=15, relief='raised', bd=3,
                              command=self.voltar_menu)
        btn_voltar.pack(side='left', padx=10, expand=True, fill='x')
        
        # Vincular Enter para buscar
        self.codigo_entry.bind('<Return>', lambda event: self.buscar_produto())
        self.quantidade_entry.bind('<Return>', lambda event: self.registrar_venda())
        
        # Empacotar canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def calcular_total(self, event=None):
        """Calcula o total da venda enquanto digita"""
        if self.produto_atual:
            try:
                quantidade = int(self.quantidade_entry.get() or 0)
                preco = self.produto_atual[7]
                total = quantidade * preco
                self.total_label.config(text=f"Total: R$ {total:.2f}")
            except ValueError:
                self.total_label.config(text="Total: R$ 0,00")
    
    def buscar_produto(self):
        codigo = self.codigo_entry.get().strip()
        
        if not codigo:
            messagebox.showerror("Erro", "Digite o código do produto!")
            return
        
        self.db.cursor.execute('''
            SELECT * FROM produtos WHERE codigo = ?
        ''', (codigo,))
        
        produto = self.db.cursor.fetchone()
        
        if produto:
            self.produto_atual = produto
            self.mostrar_info_produto(produto)
            self.quantidade_entry.focus()
            self.calcular_total()
        else:
            messagebox.showerror("Erro", "Produto não encontrado!")
            self.limpar_campos()
    
    def mostrar_info_produto(self, produto):
        info = f"""
CÓDIGO: {produto[1]}
NOME: {produto[2]}
CATEGORIA: {produto[3]} | TAMANHO: {produto[4]} | COR: {produto[5]}
PREÇO UNITÁRIO: R$ {produto[7]:.2f}
ESTOQUE DISPONÍVEL: {produto[6]} unidades
FORNECEDOR: {produto[8]}
        """
        
        self.info_text.config(state='normal')
        self.info_text.delete('1.0', tk.END)
        self.info_text.insert('1.0', info)
        self.info_text.config(state='disabled')
    
    def registrar_venda(self):
        """Registra a venda e ATUALIZA O ESTOQUE"""
        if not self.produto_atual:
            messagebox.showerror("Erro", "Busque um produto primeiro!")
            return
        
        try:
            quantidade = int(self.quantidade_entry.get())
            
            if quantidade <= 0:
                messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
                return
            
            # Dados do produto atual
            codigo_produto = self.produto_atual[1]
            nome_produto = self.produto_atual[2]
            estoque_atual = self.produto_atual[6]
            preco_unitario = self.produto_atual[7]
            
            # Verificar estoque
            if quantidade > estoque_atual:
                messagebox.showerror("Erro", 
                    f"ESTOQUE INSUFICIENTE!\n\n"
                    f"Disponível: {estoque_atual} unidades\n"
                    f"Solicitado: {quantidade} unidades")
                return
            
            # Calcular total
            total = quantidade * preco_unitario
            
            # Confirmar venda
            if messagebox.askyesno("Confirmar Venda", 
                                   f"📋 CONFIRMAR VENDA\n\n"
                                   f"Produto: {nome_produto}\n"
                                   f"Código: {codigo_produto}\n"
                                   f"Quantidade: {quantidade}\n"
                                   f"Preço unitário: R$ {preco_unitario:.2f}\n"
                                   f"TOTAL: R$ {total:.2f}\n\n"
                                   f"Estoque atual: {estoque_atual}\n"
                                   f"Estoque após venda: {estoque_atual - quantidade}"):
                
                # CRIAR OBJETO VENDA
                venda = Venda(codigo_produto, quantidade, preco_unitario)
                
                # 1. ATUALIZAR ESTOQUE (subtrair a quantidade vendida)
                novo_estoque = estoque_atual - quantidade
                self.db.cursor.execute('''
                    UPDATE produtos SET quantidade = ? WHERE codigo = ?
                ''', (novo_estoque, codigo_produto))
                
                # 2. REGISTRAR VENDA na tabela de vendas
                self.db.cursor.execute('''
                    INSERT INTO vendas (codigo_produto, quantidade, preco_unitario, 
                                       total, data_venda, hora_venda)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (venda.codigo_produto, venda.quantidade, venda.preco_unitario,
                     venda.total, venda.data_venda, venda.hora_venda))
                
                # 3. COMMIT (salvar as alterações no banco)
                self.db.conn.commit()
                
                # 4. VERIFICAR se o estoque foi atualizado (opcional - debug)
                self.db.cursor.execute('''
                    SELECT quantidade FROM produtos WHERE codigo = ?
                ''', (codigo_produto,))
                novo_estoque_confirmado = self.db.cursor.fetchone()[0]
                
                messagebox.showinfo("Sucesso", 
                    f"✅ VENDA REGISTRADA COM SUCESSO!\n\n"
                    f"Produto: {nome_produto}\n"
                    f"Quantidade: {quantidade}\n"
                    f"Total: R$ {total:.2f}\n\n"
                    f"Estoque atualizado: {novo_estoque_confirmado} unidades")
                
                # Limpar campos para nova venda
                self.limpar_campos()
                
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar venda: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def limpar_campos(self):
        self.codigo_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.info_text.config(state='normal')
        self.info_text.delete('1.0', tk.END)
        self.info_text.config(state='disabled')
        self.total_label.config(text="Total: R$ 0,00")
        self.produto_atual = None
        self.codigo_entry.focus()
    
    def voltar_menu(self):
        self.db.fechar_conexao()
        self.janela.destroy()
        self.menu_principal.deiconify()