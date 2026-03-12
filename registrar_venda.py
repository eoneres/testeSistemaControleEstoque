import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from models import Venda
from datetime import datetime

class TelaVenda:
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.db = Database()
        self.janela = tk.Toplevel()
        self.janela.title("StockMaster - Registrar Venda")
        self.janela.geometry("750x700")
        self.janela.resizable(False, False)
        self.janela.configure(bg='#ff751f')
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 750
        altura = 700
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        # Cores como atributos da classe
        self.cor_primaria = '#ff751f'
        self.cor_botao = '#ffffff'
        self.cor_texto_botao = '#ff751f'
        self.cor_sombra = '#e65c00'
        
        self.produto_atual = None
        self.cliente_atual = None
        self.pontos_por_real = 10
        
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
            text="💰 REGISTRAR VENDA",
            font=("Arial", 20, "bold"),
            fg=self.cor_primaria,
            bg='white'
        )
        titulo.pack(pady=20)
        
        # Data e hora
        agora = datetime.now()
        data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
        tk.Label(
            frame_conteudo,
            text=f"📅 {data_hora}",
            font=("Arial", 11, "italic"),
            fg='#666666',
            bg='white'
        ).pack(pady=(0, 20))
        
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
        
        # ===== FRAME CLIENTE =====
        frame_cliente = tk.LabelFrame(
            scrollable_frame,
            text="👤 CLIENTE (opcional)",
            font=("Arial", 12, "bold"),
            fg=self.cor_primaria,
            bg='white',
            padx=15,
            pady=15
        )
        frame_cliente.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            frame_cliente,
            text="CPF do Cliente:",
            font=("Arial", 10),
            bg='white',
            fg='#333333'
        ).pack(anchor='w')
        
        frame_cpf = tk.Frame(frame_cliente, bg='white')
        frame_cpf.pack(fill='x', pady=5)
        
        self.cpf_entry = tk.Entry(
            frame_cpf,
            font=("Arial", 11),
            width=25,
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.cpf_entry.pack(side='left', padx=(0, 5), ipady=5, expand=True, fill='x')
        
        btn_buscar_cliente = tk.Button(
            frame_cpf,
            text="🔍 BUSCAR",
            bg=self.cor_botao,
            fg=self.cor_texto_botao,
            font=("Arial", 10, "bold"),
            bd=1,
            relief='solid',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.buscar_cliente
        )
        btn_buscar_cliente.pack(side='left', padx=2)
        
        btn_limpar_cliente = tk.Button(
            frame_cpf,
            text="✖ LIMPAR",
            bg=self.cor_botao,
            fg=self.cor_texto_botao,
            font=("Arial", 10, "bold"),
            bd=1,
            relief='solid',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.limpar_cliente
        )
        btn_limpar_cliente.pack(side='left', padx=2)
        
        self.cliente_info = tk.Label(
            frame_cliente,
            text="Nenhum cliente selecionado",
            font=("Arial", 10),
            fg='#999999',
            bg='white'
        )
        self.cliente_info.pack(anchor='w', pady=5)
        
        # ===== FRAME PRODUTO =====
        frame_produto = tk.LabelFrame(
            scrollable_frame,
            text="📦 PRODUTO",
            font=("Arial", 12, "bold"),
            fg=self.cor_primaria,
            bg='white',
            padx=15,
            pady=15
        )
        frame_produto.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            frame_produto,
            text="Código do Produto:",
            font=("Arial", 10),
            bg='white',
            fg='#333333'
        ).pack(anchor='w')
        
        frame_codigo = tk.Frame(frame_produto, bg='white')
        frame_codigo.pack(fill='x', pady=5)
        
        self.codigo_entry = tk.Entry(
            frame_codigo,
            font=("Arial", 11),
            width=25,
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.codigo_entry.pack(side='left', padx=(0, 5), ipady=5, expand=True, fill='x')
        
        btn_buscar_produto = tk.Button(
            frame_codigo,
            text="🔍 BUSCAR",
            bg=self.cor_botao,
            fg=self.cor_texto_botao,
            font=("Arial", 10, "bold"),
            bd=1,
            relief='solid',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.buscar_produto
        )
        btn_buscar_produto.pack(side='left')
        
        # Informações do produto
        self.info_text = tk.Text(
            frame_produto,
            height=6,
            font=("Courier", 10),
            bg='#f9f9f9',
            relief='solid',
            bd=1,
            highlightbackground='#dddddd'
        )
        self.info_text.pack(fill='x', pady=10)
        self.info_text.config(state='disabled')
        
        # ===== FRAME QUANTIDADE =====
        frame_quantidade = tk.LabelFrame(
            scrollable_frame,
            text="🔢 QUANTIDADE",
            font=("Arial", 12, "bold"),
            fg=self.cor_primaria,
            bg='white',
            padx=15,
            pady=15
        )
        frame_quantidade.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            frame_quantidade,
            text="Quantidade:",
            font=("Arial", 10),
            bg='white',
            fg='#333333'
        ).pack(anchor='w')
        
        self.quantidade_entry = tk.Entry(
            frame_quantidade,
            font=("Arial", 14, "bold"),
            width=10,
            relief='solid',
            bd=1,
            highlightbackground='#dddddd',
            justify='center'
        )
        self.quantidade_entry.pack(pady=5, ipady=8)
        
        # Frame para totais
        frame_totais = tk.Frame(frame_quantidade, bg='white')
        frame_totais.pack(fill='x', pady=10)
        
        tk.Label(
            frame_totais,
            text="Total da Venda:",
            font=("Arial", 11, "bold"),
            bg='white',
            fg='#333333'
        ).pack(side='left')
        
        self.total_label = tk.Label(
            frame_totais,
            text="R$ 0,00",
            font=("Arial", 16, "bold"),
            fg=self.cor_primaria,
            bg='white'
        )
        self.total_label.pack(side='left', padx=10)
        
        tk.Label(
            frame_totais,
            text="Pontos:",
            font=("Arial", 11, "bold"),
            bg='white',
            fg='#333333'
        ).pack(side='left', padx=(20, 5))
        
        self.pontos_label = tk.Label(
            frame_totais,
            text="0 pts",
            font=("Arial", 14, "bold"),
            fg='#9C27B0',
            bg='white'
        )
        self.pontos_label.pack(side='left')
        
        # Vincular evento
        self.quantidade_entry.bind('<KeyRelease>', self.calcular_total)
        
        # ===== BOTÕES =====
        frame_botoes = tk.Frame(frame_conteudo, bg='white', pady=20)
        frame_botoes.pack(fill='x')
        
        btn_vender = tk.Button(
            frame_botoes,
            text="✅ CONFIRMAR VENDA",
            font=("Arial", 14, "bold"),
            bg=self.cor_botao,
            fg=self.cor_texto_botao,
            bd=1,
            relief='solid',
            padx=30,
            pady=15,
            cursor='hand2',
            command=self.registrar_venda
        )
        btn_vender.pack(side='left', padx=5, expand=True, fill='x')
        
        btn_voltar = tk.Button(
            frame_botoes,
            text="↩️ VOLTAR",
            font=("Arial", 14, "bold"),
            bg=self.cor_botao,
            fg=self.cor_texto_botao,
            bd=1,
            relief='solid',
            padx=30,
            pady=15,
            cursor='hand2',
            command=self.voltar_menu
        )
        btn_voltar.pack(side='left', padx=5, expand=True, fill='x')
        
        # Efeito hover nos botões
        for btn in [btn_buscar_cliente, btn_limpar_cliente, btn_buscar_produto, btn_vender, btn_voltar]:
            def on_enter(e, b=btn):
                b['bg'] = '#f5f5f5'
                b['fg'] = self.cor_sombra
            
            def on_leave(e, b=btn):
                b['bg'] = self.cor_botao
                b['fg'] = self.cor_texto_botao
            
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
        
        # Bind Enter
        self.cpf_entry.bind('<Return>', lambda event: self.buscar_cliente())
        self.codigo_entry.bind('<Return>', lambda event: self.buscar_produto())
        self.quantidade_entry.bind('<Return>', lambda event: self.registrar_venda())
        
        # Empacotar canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def buscar_cliente(self):
        cpf = self.cpf_entry.get().strip()
        if not cpf:
            messagebox.showerror("Erro", "Digite o CPF do cliente!")
            return
        
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        self.db.cursor.execute('''
            SELECT codigo, nome, pontos, status FROM clientes 
            WHERE cpf = ? OR cpf LIKE ? 
            ORDER BY CASE WHEN cpf = ? THEN 0 ELSE 1 END
        ''', (cpf_limpo, f'%{cpf_limpo}%', cpf_limpo))
        
        cliente = self.db.cursor.fetchone()
        
        if cliente:
            codigo, nome, pontos, status = cliente
            
            if status == 'bloqueado':
                messagebox.showerror("Cliente Bloqueado", 
                                   f"Este cliente está na blacklist!\n"
                                   f"Não é possível realizar vendas.")
                self.limpar_cliente()
                return
            
            self.cliente_atual = cliente
            self.cliente_info.config(
                text=f"✓ Cliente: {nome} | Pontos: {pontos} | Status: {status}",
                fg=self.cor_primaria
            )
            self.calcular_total()
        else:
            messagebox.showerror("Erro", "Cliente não encontrado!")
            self.limpar_cliente()
    
    def limpar_cliente(self):
        self.cliente_atual = None
        self.cliente_info.config(text="Nenhum cliente selecionado", fg='#999999')
        self.cpf_entry.delete(0, tk.END)
        self.calcular_total()
    
    def buscar_produto(self):
        codigo = self.codigo_entry.get().strip()
        
        if not codigo:
            messagebox.showerror("Erro", "Digite o código do produto!")
            return
        
        self.db.cursor.execute('''
            SELECT * FROM produtos WHERE codigo = ? OR codigo_barras = ?
        ''', (codigo, codigo))
        
        produto = self.db.cursor.fetchone()
        
        if produto:
            self.produto_atual = produto
            self.mostrar_info_produto(produto)
            self.quantidade_entry.focus()
            self.calcular_total()
        else:
            messagebox.showerror("Erro", "Produto não encontrado!")
            self.limpar_produto()
    
    def mostrar_info_produto(self, produto):
        info = f"""
CÓDIGO: {produto[1]}
NOME: {produto[3]}
CATEGORIA: {produto[4]} | TAMANHO: {produto[5]} | COR: {produto[6]}
PREÇO UNITÁRIO: R$ {produto[9]:.2f}
ESTOQUE DISPONÍVEL: {produto[7]} unidades
FORNECEDOR: {produto[11]}
        """
        
        self.info_text.config(state='normal')
        self.info_text.delete('1.0', tk.END)
        self.info_text.insert('1.0', info)
        self.info_text.config(state='disabled')
    
    def limpar_produto(self):
        self.produto_atual = None
        self.info_text.config(state='normal')
        self.info_text.delete('1.0', tk.END)
        self.info_text.config(state='disabled')
        self.codigo_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.total_label.config(text="R$ 0,00")
        self.pontos_label.config(text="0 pts")
    
    def calcular_total(self, event=None):
        if self.produto_atual:
            try:
                quantidade = int(self.quantidade_entry.get() or 0)
                preco = self.produto_atual[9]
                total = quantidade * preco
                
                self.total_label.config(text=f"R$ {total:.2f}")
                
                if self.cliente_atual:
                    pontos = int(total * self.pontos_por_real)
                    self.pontos_label.config(text=f"{pontos} pts")
                else:
                    self.pontos_label.config(text="0 pts")
                    
            except ValueError:
                self.total_label.config(text="R$ 0,00")
                self.pontos_label.config(text="0 pts")
    
    def registrar_venda(self):
        if not self.produto_atual:
            messagebox.showerror("Erro", "Busque um produto primeiro!")
            return
        
        try:
            quantidade = int(self.quantidade_entry.get())
            
            if quantidade <= 0:
                messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
                return
            
            codigo_produto = self.produto_atual[1]
            nome_produto = self.produto_atual[3]
            estoque_atual = self.produto_atual[7]
            preco_unitario = self.produto_atual[9]
            
            if quantidade > estoque_atual:
                messagebox.showerror("Erro", 
                    f"ESTOQUE INSUFICIENTE!\n\n"
                    f"Disponível: {estoque_atual} unidades\n"
                    f"Solicitado: {quantidade} unidades")
                return
            
            total = quantidade * preco_unitario
            pontos_ganhos = int(total * self.pontos_por_real) if self.cliente_atual else 0
            
            msg = f"📋 CONFIRMAR VENDA\n\n"
            msg += f"Produto: {nome_produto}\n"
            msg += f"Quantidade: {quantidade}\n"
            msg += f"Total: R$ {total:.2f}\n\n"
            
            if self.cliente_atual:
                msg += f"Cliente: {self.cliente_atual[1]}\n"
                msg += f"Pontos a ganhar: {pontos_ganhos}\n"
                msg += f"Saldo atual: {self.cliente_atual[2]}\n"
                msg += f"Novo saldo: {self.cliente_atual[2] + pontos_ganhos}\n"
            
            msg += f"\nEstoque após venda: {estoque_atual - quantidade}"
            
            if messagebox.askyesno("Confirmar Venda", msg):
                
                novo_estoque = estoque_atual - quantidade
                self.db.cursor.execute('''
                    UPDATE produtos SET quantidade = ? WHERE codigo = ?
                ''', (novo_estoque, codigo_produto))
                
                if self.cliente_atual:
                    self.db.cursor.execute('''
                        INSERT INTO vendas 
                        (codigo_produto, cliente_codigo, quantidade, 
                         preco_unitario, total, data_venda, hora_venda, pontos_ganhos)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (codigo_produto, self.cliente_atual[0], quantidade, 
                          preco_unitario, total,
                          datetime.now().strftime("%d/%m/%Y"),
                          datetime.now().strftime("%H:%M:%S"),
                          pontos_ganhos))
                else:
                    self.db.cursor.execute('''
                        INSERT INTO vendas 
                        (codigo_produto, quantidade, preco_unitario, total, data_venda, hora_venda)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (codigo_produto, quantidade, preco_unitario, total,
                          datetime.now().strftime("%d/%m/%Y"),
                          datetime.now().strftime("%H:%M:%S")))
                
                if self.cliente_atual and pontos_ganhos > 0:
                    novo_saldo = self.cliente_atual[2] + pontos_ganhos
                    self.db.cursor.execute('''
                        UPDATE clientes SET pontos = ? WHERE codigo = ?
                    ''', (novo_saldo, self.cliente_atual[0]))
                
                self.db.conn.commit()
                
                sucesso_msg = f"✅ VENDA REGISTRADA COM SUCESSO!\n\n"
                sucesso_msg += f"Produto: {nome_produto}\n"
                sucesso_msg += f"Quantidade: {quantidade}\n"
                sucesso_msg += f"Total: R$ {total:.2f}\n"
                sucesso_msg += f"Estoque atualizado: {novo_estoque}\n"
                
                if self.cliente_atual:
                    sucesso_msg += f"\nPontos ganhos: {pontos_ganhos}"
                
                messagebox.showinfo("Sucesso", sucesso_msg)
                self.limpar_produto()
                
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar venda: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def voltar_menu(self):
        self.db.fechar_conexao()
        self.janela.destroy()
        self.menu_principal.deiconify()