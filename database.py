import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('estoque.db')
        self.cursor = self.conn.cursor()
        self.criar_tabelas()
        self.criar_usuario_padrao()
    
    def criar_tabelas(self):
        # Tabela de usuários
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                nome TEXT NOT NULL
            )
        ''')
        
        # Tabela de produtos (ATUALIZADA com codigo_barras)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                codigo_barras TEXT UNIQUE,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                tamanho TEXT NOT NULL,
                cor TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                quantidade_minima INTEGER DEFAULT 5,
                preco_venda REAL NOT NULL,
                preco_custo REAL,
                fornecedor TEXT NOT NULL,
                localizacao TEXT,
                data_cadastro TEXT NOT NULL,
                data_atualizacao TEXT
            )
        ''')
        
        # Tabela de vendas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                total REAL NOT NULL,
                data_venda TEXT NOT NULL,
                hora_venda TEXT NOT NULL,
                numero_nota TEXT,
                FOREIGN KEY (codigo_produto) REFERENCES produtos (codigo)
            )
        ''')
        
        # NOVA TABELA: Movimentação de Estoque
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_produto TEXT NOT NULL,
                tipo TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                quantidade_anterior INTEGER NOT NULL,
                quantidade_nova INTEGER NOT NULL,
                motivo TEXT,
                numero_nota TEXT,
                data_movimento TEXT NOT NULL,
                hora_movimento TEXT NOT NULL,
                usuario TEXT,
                FOREIGN KEY (codigo_produto) REFERENCES produtos (codigo)
            )
        ''')
        
        # NOVA TABELA: Notas Fiscais
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_nota TEXT UNIQUE NOT NULL,
                tipo TEXT NOT NULL,
                data_emissao TEXT NOT NULL,
                valor_total REAL NOT NULL,
                fornecedor TEXT,
                cliente TEXT,
                arquivo_pdf TEXT,
                observacoes TEXT
            )
        ''')
        
        # NOVA TABELA: Itens da Nota
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS nota_itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_nota TEXT NOT NULL,
                codigo_produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (numero_nota) REFERENCES notas (numero_nota),
                FOREIGN KEY (codigo_produto) REFERENCES produtos (codigo)
            )
        ''')
        
        self.conn.commit()
    
    def criar_usuario_padrao(self):
        self.cursor.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
        if not self.cursor.fetchone():
            self.cursor.execute('''
                INSERT INTO usuarios (usuario, senha, nome)
                VALUES (?, ?, ?)
            ''', ('admin', '123456', 'Administrador'))
            self.conn.commit()
    
    def verificar_login(self, usuario, senha):
        self.cursor.execute('''
            SELECT * FROM usuarios WHERE usuario = ? AND senha = ?
        ''', (usuario, senha))
        return self.cursor.fetchone()
    
    def registrar_movimentacao(self, codigo_produto, tipo, quantidade, quantidade_anterior, 
                               quantidade_nova, motivo="", numero_nota="", usuario=""):
        """Registra movimentação de estoque"""
        data = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")
        
        self.cursor.execute('''
            INSERT INTO movimentacoes 
            (codigo_produto, tipo, quantidade, quantidade_anterior, quantidade_nova, 
             motivo, numero_nota, data_movimento, hora_movimento, usuario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (codigo_produto, tipo, quantidade, quantidade_anterior, quantidade_nova,
              motivo, numero_nota, data, hora, usuario))
        self.conn.commit()
    
    def fechar_conexao(self):
        self.conn.close()