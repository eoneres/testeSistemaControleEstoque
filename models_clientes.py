from datetime import datetime

class Cliente:
    def __init__(self, nome, cpf, telefone, endereco, bairro, cidade, estado,
                 rg="", celular="", email="", data_nascimento="", sexo="",
                 numero="", complemento="", cep="", observacoes=""):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.telefone = telefone
        self.celular = celular
        self.email = email
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.endereco = endereco
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.observacoes = observacoes
        self.data_cadastro = datetime.now().strftime("%d/%m/%Y")
        self.pontos = 0
        self.status = "ativo"
    
    def formatar_cpf(self, cpf):
        """Formata CPF: 123.456.789-00"""
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf
    
    def formatar_telefone(self, tel):
        """Formata telefone: (11) 1234-5678 ou (11) 91234-5678"""
        tel = ''.join(filter(str.isdigit, tel))
        if len(tel) == 10:
            return f"({tel[:2]}) {tel[2:6]}-{tel[6:]}"
        elif len(tel) == 11:
            return f"({tel[:2]}) {tel[2:7]}-{tel[7:]}"
        return tel

class PontosFidelidade:
    def __init__(self, cliente_codigo, quantidade, tipo, motivo="", venda_codigo=""):
        self.cliente_codigo = cliente_codigo
        self.quantidade = quantidade
        self.tipo = tipo  # 'ganho', 'resgate', 'ajuste'
        self.motivo = motivo
        self.venda_codigo = venda_codigo
        self.data = datetime.now().strftime("%d/%m/%Y")
        self.hora = datetime.now().strftime("%H:%M:%S")