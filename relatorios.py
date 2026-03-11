import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import Database
from datetime import datetime
import csv

class TelaRelatorios:
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.db = Database()
        self.janela = tk.Toplevel()
        self.janela.title("Sistema de Estoque - Relatórios")
        self.janela.geometry("800x500")
        
        # Centralizar a janela
        self.janela.update_idletasks()
        largura = 800
        altura = 500
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.criar_interface()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar_menu)
        self.janela.mainloop()
    
    def criar_interface(self):
        # Frame esquerdo (opções)
        frame_opcoes = tk.Frame(self.janela, bg='#f0f0f0', width=200)
        frame_opcoes.pack(side='left', fill='y')
        
        tk.Label(frame_opcoes, text="RELATÓRIOS", font=("Arial", 14, "bold"),
                bg='#f0f0f0').pack(pady=20)
        
        # Botões de relatórios
        botoes = [
            ("📊 Estoque Atual", self.mostrar_estoque_atual),
            ("⚠️ Estoque Baixo", self.mostrar_estoque_baixo),
            ("💰 Vendas do Dia", self.mostrar_vendas_dia)
        ]
        
        for texto, comando in botoes:
            btn = tk.Button(frame_opcoes, text=texto, font=("Arial", 10),
                          bg="#2196F3", fg="white", width=20, pady=5,
                          command=comando)
            btn.pack(pady=5, padx=10)
        
        btn_voltar = tk.Button(frame_opcoes, text="VOLTAR", font=("Arial", 10),
                              bg="#f44336", fg="white", width=20, pady=5,
                              command=self.voltar_menu)
        btn_voltar.pack(pady=5, padx=10)
        
        # Frame direito (conteúdo)
        frame_conteudo = tk.Frame(self.janela, bg='white')
        frame_conteudo.pack(side='right', fill='both', expand=True)
        
        # Área de texto para mostrar o relatório
        self.texto_relatorio = tk.Text(frame_conteudo, font=("Courier", 10), bg='white', wrap='word')
        self.texto_relatorio.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.texto_relatorio)
        scrollbar.pack(side='right', fill='y')
        self.texto_relatorio.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.texto_relatorio.yview)
        
        # Frame para botão de exportar
        frame_exportar = tk.Frame(frame_conteudo, bg='white')
        frame_exportar.pack(pady=5)
        
        btn_exportar = tk.Button(frame_exportar, text="EXPORTAR PARA CSV", 
                                bg="#4CAF50", fg="white", font=("Arial", 10),
                                command=self.exportar_csv)
        btn_exportar.pack()
        
        # Variável para armazenar o último relatório gerado
        self.ultimo_relatorio = ""
    
    def mostrar_estoque_atual(self):
        self.texto_relatorio.delete('1.0', tk.END)
        relatorio = "=" * 60 + "\n"
        relatorio += " " * 20 + "RELATÓRIO DE ESTOQUE ATUAL\n"
        relatorio += "=" * 60 + "\n\n"
        
        self.db.cursor.execute('''
            SELECT codigo, nome, categoria, tamanho, cor, quantidade, preco_venda, fornecedor
            FROM produtos
            ORDER BY nome
        ''')
        
        produtos = self.db.cursor.fetchall()
        
        if not produtos:
            relatorio += "Nenhum produto cadastrado.\n"
        else:
            # Cabeçalho
            relatorio += f"{'Código':<10} {'Nome':<25} {'Categoria':<12} {'Tam':<5} {'Cor':<10} {'Qtd':<6} {'Preço':<10} {'Fornecedor':<15}\n"
            relatorio += "-" * 93 + "\n"
            
            total_produtos = 0
            valor_total = 0
            
            for produto in produtos:
                codigo, nome, categoria, tamanho, cor, quantidade, preco, fornecedor = produto
                relatorio += f"{codigo:<10} {nome[:24]:<25} {categoria:<12} {tamanho:<5} {cor:<10} {quantidade:<6} R${preco:<8.2f} {fornecedor[:14]:<15}\n"
                
                total_produtos += quantidade
                valor_total += quantidade * preco
            
            relatorio += "-" * 93 + "\n"
            relatorio += f"TOTAL: {total_produtos} unidades | Valor em estoque: R$ {valor_total:.2f}\n"
        
        self.ultimo_relatorio = relatorio
        self.texto_relatorio.insert('1.0', relatorio)
    
    def mostrar_estoque_baixo(self):
        self.texto_relatorio.delete('1.0', tk.END)
        relatorio = "=" * 60 + "\n"
        relatorio += " " * 18 + "RELATÓRIO DE ESTOQUE BAIXO (< 5 UNIDADES)\n"
        relatorio += "=" * 60 + "\n\n"
        
        self.db.cursor.execute('''
            SELECT codigo, nome, categoria, tamanho, cor, quantidade, preco_venda, fornecedor
            FROM produtos
            WHERE quantidade < 5
            ORDER BY quantidade
        ''')
        
        produtos = self.db.cursor.fetchall()
        
        if not produtos:
            relatorio += "Nenhum produto com estoque baixo.\n"
        else:
            # Cabeçalho
            relatorio += f"{'Código':<10} {'Nome':<25} {'Categoria':<12} {'Tam':<5} {'Cor':<10} {'Qtd':<6} {'Fornecedor':<15}\n"
            relatorio += "-" * 83 + "\n"
            
            for produto in produtos:
                codigo, nome, categoria, tamanho, cor, quantidade, _, fornecedor = produto
                relatorio += f"{codigo:<10} {nome[:24]:<25} {categoria:<12} {tamanho:<5} {cor:<10} {quantidade:<6} {fornecedor[:14]:<15}\n"
        
        self.ultimo_relatorio = relatorio
        self.texto_relatorio.insert('1.0', relatorio)
    
    def mostrar_vendas_dia(self):
        self.texto_relatorio.delete('1.0', tk.END)
        hoje = datetime.now().strftime("%d/%m/%Y")
        
        relatorio = "=" * 60 + "\n"
        relatorio += f" " * 20 + f"RELATÓRIO DE VENDAS - {hoje}\n"
        relatorio += "=" * 60 + "\n\n"
        
        self.db.cursor.execute('''
            SELECT v.codigo_produto, p.nome, v.quantidade, v.preco_unitario, v.total, v.hora_venda
            FROM vendas v
            JOIN produtos p ON v.codigo_produto = p.codigo
            WHERE v.data_venda = ?
            ORDER BY v.hora_venda
        ''', (hoje,))
        
        vendas = self.db.cursor.fetchall()
        
        if not vendas:
            relatorio += "Nenhuma venda registrada hoje.\n"
        else:
            # Cabeçalho
            relatorio += f"{'Hora':<8} {'Código':<10} {'Produto':<25} {'Qtd':<6} {'Preço':<10} {'Total':<10}\n"
            relatorio += "-" * 69 + "\n"
            
            total_vendas = 0
            quantidade_total = 0
            
            for venda in vendas:
                codigo, nome, quantidade, preco, total, hora = venda
                relatorio += f"{hora:<8} {codigo:<10} {nome[:24]:<25} {quantidade:<6} R${preco:<8.2f} R${total:<8.2f}\n"
                
                total_vendas += total
                quantidade_total += quantidade
            
            relatorio += "-" * 69 + "\n"
            relatorio += f"TOTAL: {quantidade_total} unidades | Valor total: R$ {total_vendas:.2f}\n"
        
        self.ultimo_relatorio = relatorio
        self.texto_relatorio.insert('1.0', relatorio)
    
    def exportar_csv(self):
        if not self.ultimo_relatorio:
            messagebox.showwarning("Aviso", "Nenhum relatório gerado para exportar!")
            return
        
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivo CSV", "*.csv"), ("Todos os arquivos", "*.*")],
            title="Salvar relatório como"
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', newline='', encoding='utf-8') as f:
                    f.write(self.ultimo_relatorio)
                messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso!\n{arquivo}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
    
    def voltar_menu(self):
        self.db.fechar_conexao()
        self.janela.destroy()
        self.menu_principal.deiconify()