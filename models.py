from datetime import datetime

class Produto:
    def __init__(self, nome, categoria, tamanho, cor, quantidade, preco_venda, 
                 fornecedor, codigo_barras="", preco_custo=0, quantidade_minima=5, localizacao=""):
        self.nome = nome
        self.categoria = categoria
        self.tamanho = tamanho
        self.cor = cor
        self.quantidade = quantidade
        self.quantidade_minima = quantidade_minima
        self.preco_venda = preco_venda
        self.preco_custo = preco_custo
        self.fornecedor = fornecedor
        self.codigo_barras = codigo_barras
        self.localizacao = localizacao
        self.data_cadastro = datetime.now().strftime("%d/%m/%Y")
        self.data_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def gerar_codigo(self, db):
        db.cursor.execute("SELECT COUNT(*) FROM produtos")
        count = db.cursor.fetchone()[0] + 1
        return f"PROD{count:04d}"
    
    def gerar_codigo_barras(self):
        """Gera um código de barras fictício (EAN-13 simulado)"""
        import random
        # Simula um código EAN-13 (8 dígitos + 5 aleatórios)
        prefixo = "789"  # Código do Brasil
        resto = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        return prefixo + resto

class Venda:
    def __init__(self, codigo_produto, quantidade, preco_unitario, numero_nota=""):
        self.codigo_produto = codigo_produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.total = quantidade * preco_unitario
        self.data_venda = datetime.now().strftime("%d/%m/%Y")
        self.hora_venda = datetime.now().strftime("%H:%M:%S")
        self.numero_nota = numero_nota

class Movimentacao:
    def __init__(self, codigo_produto, tipo, quantidade, motivo=""):
        self.codigo_produto = codigo_produto
        self.tipo = tipo  # 'entrada', 'saida', 'ajuste', 'venda', 'compra'
        self.quantidade = quantidade
        self.motivo = motivo
        self.data = datetime.now().strftime("%d/%m/%Y")
        self.hora = datetime.now().strftime("%H:%M:%S")