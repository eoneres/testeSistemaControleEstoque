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
        self.janela.title("Sistema de Estoque - Registrar Venda")
        self.janela.geometry("700x650")
        self.janela.resizable(False, False)
        
        # Centralizar
        self.janela.update_idletasks()
        largura = 700
        altura = 650
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.janela.lift()
        self.janela.focus_force()
        
        self.produto_atual = None
        self.cliente_atual = None
        self.pontos_por_real = 10  # 10 pontos por real gasto
        
        self.criar_interface()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar_menu)
        self.janela.mainloop()
    
    def criar_interface(self):
        # Canvas com scroll
        canvas = tk.Canvas(self.janela)
        scrollbar = tk.Scrollbar(self.janela, orient="vertical", command=canvas.yview)
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
        titulo = tk.Label(frame, text="REGISTRAR VENDA", 
                          font=("Arial", 18, "bold"), fg="#333")
        titulo.pack(pady=20)
        
        # Data e hora atual
        agora = datetime.now()
        data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
        tk.Label(frame, text=f"Data/Hora: {data_hora}", font=("Arial", 12, "italic"),
                fg="#666").pack(pady=5)
        
        # FRAME 1: Cliente
        frame_cliente = tk.LabelFrame(frame, text="1. CLIENTE (opcional)", 
                                     font=("Arial", 11, "bold"),
                                     padx=15, pady=15, bg='#e8f5e8')
        frame_cliente.pack(fill='x', pady=10)
        
        tk.Label(frame_cliente, text="CPF do Cliente:", font=("Arial", 11)).pack(anchor='w')
        
        cpf_frame = tk.Frame(frame_cliente)
        cpf_frame.pack(fill='x', pady=5)
        
        self.cpf_entry = tk.Entry(cpf_frame, font=("Arial", 11), width=30, 
                                  relief='solid', bd=1)
        self.cpf_entry.pack(side='left', padx=(0,5), ipady=5)
        
        btn_buscar_cliente = tk.Button(cpf_frame, text="🔍 BUSCAR", 
                                      bg="#2196F3", fg="white", font=("Arial", 10),
                                      command=self.buscar_cliente)
        btn_buscar_cliente.pack(side='left')
        
        btn_limpar_cliente = tk.Button(cpf_frame, text="✖ LIMPAR", 
                                      bg="#FF9800", fg="white", font=("Arial", 10),
                                      command=self.limpar_cliente)
        btn_limpar_cliente.pack(side='left', padx=5)
        
        # Informações do cliente
        self.cliente_info = tk.Label(frame_cliente, text="Nenhum cliente selecionado", 
                                    font=("Arial", 10), fg="#666")
        self.cliente_info.pack(anchor='w', pady=5)
        
        # FRAME 2: Produto
        frame_produto = tk.LabelFrame(frame, text="2. PRODUTO", 
                                     font=("Arial", 11, "bold"),
                                     padx=15, pady=15, bg='#e3f2fd')
        frame_produto.pack(fill='x', pady=10)
        
        tk.Label(frame_produto, text="Código do Produto:", font=("Arial", 11)).pack(anchor='w')
        
        produto_frame = tk.Frame(frame_produto)
        produto_frame.pack(fill='x', pady=5)
        
        self.codigo_entry = tk.Entry(produto_frame, font=("Arial", 11), width=30, 
                                     relief='solid', bd=1)
        self.codigo_entry.pack(side='left', padx=(0,5), ipady=5)
        
        btn_buscar_produto = tk.Button(produto_frame, text="🔍 BUSCAR", 
                                      bg="#2196F3", fg="white", font=("Arial", 10),
                                      command=self.buscar_produto)
        btn_buscar_produto.pack(side='left')
        
        # Informações do produto
        self.info_text = tk.Text(frame_produto, height=6, width=60, 
                                 font=("Courier", 10), bg='white', 
                                 relief='solid', bd=1)
        self.info_text.pack(fill='x', pady=10)
        self.info_text.config(state='disabled')
        
        # FRAME 3: Quantidade e Total
        frame_venda = tk.LabelFrame(frame, text="3. FINALIZAR VENDA", 
                                   font=("Arial", 11, "bold"),
                                   padx=15, pady=15, bg='#fff3e0')
        frame_venda.pack(fill='x', pady=10)
        
        tk.Label(frame_venda, text="Quantidade:", font=("Arial", 11)).pack(anchor='w')
        
        self.quantidade_entry = tk.Entry(frame_venda, font=("Arial", 11), width=20,
                                        relief='solid', bd=1)
        self.quantidade_entry.pack(fill='x', pady=5, ipady=5)
        
        # Frame para totais
        totais_frame = tk.Frame(frame_venda)
        totais_frame.pack(fill='x', pady=10)
        
        # Total da venda
        tk.Label(totais_frame, text="Total da Venda:", font=("Arial", 11)).pack(side='left')
        self.total_label = tk.Label(totais_frame, text="R$ 0,00", 
                                   font=("Arial", 12, "bold"), fg="#4CAF50")
        self.total_label.pack(side='left', padx=10)
        
        # Pontos a ganhar
        tk.Label(totais_frame, text="Pontos:", font=("Arial", 11)).pack(side='left', padx=(20,0))
        self.pontos_label = tk.Label(totais_frame, text="0 pts", 
                                    font=("Arial", 12, "bold"), fg="#9C27B0")
        self.pontos_label.pack(side='left', padx=10)
        
        # Vincular evento para calcular total enquanto digita
        self.quantidade_entry.bind('<KeyRelease>', self.calcular_total)
        
        # FRAME 4: Botões
        frame_botoes = tk.Frame(frame, bg='#f0f0f0', pady=20)
        frame_botoes.pack(fill='x', pady=20)
        
        # Botão CONFIRMAR VENDA
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
        self.cpf_entry.bind('<Return>', lambda event: self.buscar_cliente())
        self.codigo_entry.bind('<Return>', lambda event: self.buscar_produto())
        self.quantidade_entry.bind('<Return>', lambda event: self.registrar_venda())
        
        # Empacotar canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def buscar_cliente(self):
        """Busca cliente por CPF"""
        cpf = self.cpf_entry.get().strip()
        
        if not cpf:
            messagebox.showerror("Erro", "Digite o CPF do cliente!")
            return
        
        # Remover formatação do CPF
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
                fg="#4CAF50"
            )
            
            # Recalcular pontos se já houver quantidade
            self.calcular_total()
            
        else:
            messagebox.showerror("Erro", "Cliente não encontrado!")
            self.limpar_cliente()
    
    def limpar_cliente(self):
        """Limpa cliente selecionado"""
        self.cliente_atual = None
        self.cliente_info.config(text="Nenhum cliente selecionado", fg="#666")
        self.cpf_entry.delete(0, tk.END)
        self.calcular_total()
    
    def buscar_produto(self):
        """Busca produto por código"""
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
        """Mostra informações do produto"""
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
        """Limpa produto selecionado"""
        self.produto_atual = None
        self.info_text.config(state='normal')
        self.info_text.delete('1.0', tk.END)
        self.info_text.config(state='disabled')
        self.codigo_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.total_label.config(text="R$ 0,00")
        self.pontos_label.config(text="0 pts")
    
    def calcular_total(self, event=None):
        """Calcula o total da venda e pontos"""
        if self.produto_atual:
            try:
                quantidade = int(self.quantidade_entry.get() or 0)
                preco = self.produto_atual[9]  # preco_venda
                total = quantidade * preco
                
                self.total_label.config(text=f"R$ {total:.2f}")
                
                # Calcular pontos se cliente selecionado
                if self.cliente_atual:
                    pontos = int(total * self.pontos_por_real)
                    self.pontos_label.config(text=f"{pontos} pts")
                else:
                    self.pontos_label.config(text="0 pts")
                    
            except ValueError:
                self.total_label.config(text="R$ 0,00")
                self.pontos_label.config(text="0 pts")
    
    def registrar_venda(self):
        """Registra a venda e atualiza estoque e pontos"""
        if not self.produto_atual:
            messagebox.showerror("Erro", "Busque um produto primeiro!")
            return
        
        try:
            quantidade = int(self.quantidade_entry.get())
            
            if quantidade <= 0:
                messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
                return
            
            # Dados do produto
            codigo_produto = self.produto_atual[1]
            nome_produto = self.produto_atual[3]
            estoque_atual = self.produto_atual[7]
            preco_unitario = self.produto_atual[9]
            
            # Verificar estoque
            if quantidade > estoque_atual:
                messagebox.showerror("Erro", 
                    f"ESTOQUE INSUFICIENTE!\n\n"
                    f"Disponível: {estoque_atual} unidades\n"
                    f"Solicitado: {quantidade} unidades")
                return
            
            # Calcular total e pontos
            total = quantidade * preco_unitario
            pontos_ganhos = int(total * self.pontos_por_real) if self.cliente_atual else 0
            
            # Mensagem de confirmação
            msg = f"📋 CONFIRMAR VENDA\n\n"
            msg += f"Produto: {nome_produto}\n"
            msg += f"Quantidade: {quantidade}\n"
            msg += f"Total: R$ {total:.2f}\n\n"
            
            if self.cliente_atual:
                msg += f"Cliente: {self.cliente_atual[1]}\n"
                msg += f"Pontos a ganhar: {pontos_ganhos}\n"
                msg += f"Saldo atual de pontos: {self.cliente_atual[2]}\n"
                msg += f"Novo saldo: {self.cliente_atual[2] + pontos_ganhos}\n"
            
            msg += f"\nEstoque após venda: {estoque_atual - quantidade}"
            
            if messagebox.askyesno("Confirmar Venda", msg):
                
                # Gerar código da venda
                codigo_venda = self.db.gerar_codigo_venda()
                
                # 1. ATUALIZAR ESTOQUE
                novo_estoque = estoque_atual - quantidade
                self.db.cursor.execute('''
                    UPDATE produtos SET quantidade = ? WHERE codigo = ?
                ''', (novo_estoque, codigo_produto))
                
                # 2. REGISTRAR VENDA - VERSAO CORRIGIDA (sem codigo_venda se não existir)
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
                
                # 3. ATUALIZAR PONTOS DO CLIENTE (se houver)
                if self.cliente_atual and pontos_ganhos > 0:
                    novo_saldo = self.cliente_atual[2] + pontos_ganhos
                    self.db.cursor.execute('''
                        UPDATE clientes SET pontos = ? WHERE codigo = ?
                    ''', (novo_saldo, self.cliente_atual[0]))
                    
                    # Registrar movimentação de pontos
                    try:
                        self.db.cursor.execute('''
                            INSERT INTO pontos_fidelidade 
                            (cliente_codigo, data_movimento, hora_movimento, tipo,
                             quantidade, saldo_anterior, saldo_novo)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (self.cliente_atual[0], 
                              datetime.now().strftime("%d/%m/%Y"),
                              datetime.now().strftime("%H:%M:%S"),
                              'ganho', pontos_ganhos, 
                              self.cliente_atual[2], novo_saldo))
                    except:
                        # Tabela pode não existir ainda
                        pass
                
                self.db.conn.commit()
                
                
                sucesso_msg = f"✅ VENDA REGISTRADA COM SUCESSO!\n\n"
                sucesso_msg += f"Produto: {nome_produto}\n"
                sucesso_msg += f"Quantidade: {quantidade}\n"
                sucesso_msg += f"Total: R$ {total:.2f}\n"
                sucesso_msg += f"Estoque atualizado: {novo_estoque}\n"
                
                if self.cliente_atual:
                    sucesso_msg += f"\nPontos ganhos: {pontos_ganhos}\n"
                    sucesso_msg += f"Saldo de pontos: {novo_saldo}"
                
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