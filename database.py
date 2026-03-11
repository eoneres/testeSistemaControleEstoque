import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('estoque.db')
        self.cursor = self.conn.cursor()
        self.criar_tabelas()
        self.criar_usuario_padrao()
    
    def criar_tabelas(self):
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                nome TEXT NOT NULL
            )
        ''')
        
        
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
        
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                rg TEXT,
                telefone TEXT NOT NULL,
                celular TEXT,
                email TEXT,
                data_nascimento TEXT,
                sexo TEXT,
                endereco TEXT NOT NULL,
                numero TEXT,
                complemento TEXT,
                bairro TEXT NOT NULL,
                cidade TEXT NOT NULL,
                estado TEXT NOT NULL,
                cep TEXT,
                data_cadastro TEXT NOT NULL,
                observacoes TEXT,
                pontos INTEGER DEFAULT 0,
                status TEXT DEFAULT 'ativo'  -- 'ativo', 'inativo', 'bloqueado'
            )
        ''')
        
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pontos_fidelidade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_codigo TEXT NOT NULL,
                data_movimento TEXT NOT NULL,
                hora_movimento TEXT NOT NULL,
                tipo TEXT NOT NULL,  -- 'ganho', 'resgate', 'ajuste'
                quantidade INTEGER NOT NULL,
                saldo_anterior INTEGER NOT NULL,
                saldo_novo INTEGER NOT NULL,
                venda_codigo TEXT,
                motivo TEXT,
                FOREIGN KEY (cliente_codigo) REFERENCES clientes (codigo)
            )
        ''')
        
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_venda TEXT UNIQUE NOT NULL,
                codigo_produto TEXT NOT NULL,
                cliente_codigo TEXT,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                total REAL NOT NULL,
                data_venda TEXT NOT NULL,
                hora_venda TEXT NOT NULL,
                numero_nota TEXT,
                pontos_ganhos INTEGER DEFAULT 0,
                FOREIGN KEY (codigo_produto) REFERENCES produtos (codigo),
                FOREIGN KEY (cliente_codigo) REFERENCES clientes (codigo)
            )
        ''')
        
        # NOVA TABELA: Blacklist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS blacklist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_codigo TEXT UNIQUE NOT NULL,
                motivo TEXT NOT NULL,
                data_bloqueio TEXT NOT NULL,
                data_vencimento TEXT,
                observacoes TEXT,
                FOREIGN KEY (cliente_codigo) REFERENCES clientes (codigo)
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
    
    def gerar_codigo_cliente(self):
        """Gera código automático para cliente"""
        self.cursor.execute("SELECT COUNT(*) FROM clientes")
        count = self.cursor.fetchone()[0] + 1
        return f"CLI{count:04d}"
    
    def gerar_codigo_venda(self):
        """Gera código automático para venda"""
        self.cursor.execute("SELECT COUNT(*) FROM vendas")
        count = self.cursor.fetchone()[0] + 1
        data = datetime.now().strftime("%Y%m%d")
        return f"VENDA{data}{count:04d}"
    
    def fechar_conexao(self):
        self.conn.close()