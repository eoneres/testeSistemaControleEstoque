# 📦 STOCKMASTER - Sistema Completo de Gestão Empresarial

![Version](https://img.shields.io/badge/version-2.0.0-orange)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)

## 🚀 Sobre o Projeto

**StockMaster** é um sistema desktop completo desenvolvido em Python para gestão de pequenas e médias empresas. Com interface moderna e intuitiva, o sistema integra todas as áreas essenciais de um negócio em uma única plataforma: **estoque, vendas, clientes, financeiro e relatórios gerenciais**.

O projeto foi desenvolvido como trabalho acadêmico, mas com foco em aplicação real, oferecendo funcionalidades profissionais que atendem às necessidades do dia a dia de qualquer comércio.

---

## ✨ Funcionalidades Principais

### 📊 **Dashboard Inteligente**
- Cards dinâmicos com indicadores em tempo real
- Vendas do dia, estoque baixo e produto mais vendido
- Atualização automática após cada operação

### 🔐 **Sistema de Login**
- Acesso seguro com usuário e senha
- Usuário padrão: admin / 123456
- Interface moderna com card central

### 📦 **Gestão de Produtos**
- ✅ Cadastro completo com código de barras
- ✅ Consulta avançada com múltiplos filtros
- ✅ Edição e exclusão de produtos
- ✅ Controle de estoque mínimo
- ✅ Destaque visual para produtos com estoque baixo
- ✅ Histórico completo de movimentações

### 💰 **Registro de Vendas**
- ✅ Busca de produtos por código ou código de barras
- ✅ Integração com clientes via CPF
- ✅ Programa de fidelidade com pontos
- ✅ Baixa automática no estoque
- ✅ Cálculo em tempo real do total e pontos
- ✅ Confirmação antes da finalização

### 👥 **Gestão de Clientes**
- ✅ Cadastro completo (dados pessoais, endereço, contato)
- ✅ Busca por nome, CPF ou telefone
- ✅ Edição de dados
- ✅ Programa de pontos acumulativos
- ✅ **Blacklist** com bloqueio de clientes
- ✅ Histórico de compras por cliente
- ✅ Destaque visual para clientes bloqueados

### 💵 **Módulo Financeiro**
- ✅ **Fluxo de Caixa Direto** com todas as movimentações
- ✅ **Análise Operacional** com gráficos comparativos
- ✅ **Fluxo Projetado** com cenários (otimista, moderado, pessimista)
- ✅ **Análise por Categoria** com gráficos de pizza
- ✅ **Conciliação Bancária** de lançamentos
- ✅ Cards de resumo (saldo, entradas, saídas, projeção)
- ✅ Cálculos automáticos baseados em dados reais

### 📈 **Relatórios Gerenciais**
- ✅ Estoque atual completo
- ✅ Produtos com estoque baixo
- ✅ Vendas do dia
- ✅ Vendas por período
- ✅ Compras por cliente
- ✅ Histórico de pontos
- ✅ Exportação para CSV

---

## 🎨 **Design e Interface**

O sistema possui interface moderna e intuitiva, inspirada em tendências atuais de UX/UI:

- **Cores:** Laranja (#ff751f) como destaque, fundo cinza claro
- **Cards elegantes** com ícones e informações hierárquicas
- **Botões arredondados** com efeitos hover
- **Abas organizadas** para melhor navegação
- **Tabelas com scroll** e formatação condicional
- **Feedback visual** para todas as ações

---

## 🛠️ **Tecnologias Utilizadas**

| Tecnologia | Aplicação |
|------------|-----------|
| **Python 3.11+** | Linguagem principal |
| **Tkinter** | Interface gráfica |
| **SQLite3** | Banco de dados local |
| **Matplotlib** | Gráficos e visualizações |
| **Datetime** | Controle de datas |
| **CSV** | Exportação de relatórios |
| **Git/GitHub** | Versionamento |

---

## 🗄️ **Banco de Dados**

O sistema utiliza SQLite com as seguintes tabelas:

- **usuarios** - Controle de acesso
- **produtos** - Cadastro com código de barras
- **clientes** - Cadastro com pontos e status
- **vendas** - Registro com cliente e pontos
- **movimentacoes** - Histórico de estoque
- **pontos_fidelidade** - Histórico de pontos
- **blacklist** - Clientes bloqueados

---

📊 Funcionalidades em Detalhe
🎯 Dashboard
text
┌─────────────────────────────────────────────────────────────┐
│  📊 VENDAS HOJE    ⚠️ ESTOQUE BAIXO    🔥 MAIS VENDIDO     │
│     5                 3                    Camiseta...     │
│  Total: R$ 450,00    produtos críticos    item do dia      │
└─────────────────────────────────────────────────────────────┘
💰 Módulo Financeiro
Fluxo de Caixa Direto: Todas as movimentações com saldo acumulado

Análise Operacional: Gráficos comparativos de entradas vs saídas

Fluxo Projetado: Projeções para 30, 60, 90 e 180 dias

Análise por Categoria: Distribuição de gastos e receitas

Conciliação Bancária: Controle de lançamentos pendentes

👥 Gestão de Clientes
Cadastro completo com validação de CPF

Programa de pontos automático (10 pontos por R$ 1,00)

Blacklist com motivo e data de bloqueio

Histórico completo de compras

🔮 Futuras Implementações
📱 Aplicativo mobile para consulta rápida

☁️ Sincronização em nuvem multi-dispositivo

📊 Mais gráficos e indicadores financeiros

🔔 Notificações por email e WhatsApp

🖨️ Impressão de relatórios e etiquetas

💳 Integração com leitor de código de barras

📈 Análise preditiva com machine learning

👨‍💻 Sobre o Desenvolvedor
StockMaster foi desenvolvido como projeto acadêmico para a disciplina de Programação Desktop, com o objetivo de criar uma solução completa e profissional para gestão empresarial.

Tecnologias aprendidas e aplicadas:

Programação Orientada a Objetos em Python

Desenvolvimento de interfaces gráficas com Tkinter

Modelagem de banco de dados relacional

SQL e integração com Python

Versionamento com Git/GitHub

UX/UI Design aplicado

©️ Licença e Direitos Autorais
Copyright © 2025 Filipe Neres Fernandes. Todos os direitos reservados.

Este software é de propriedade exclusiva de Filipe Neres Fernandes.

🔒 Termos de Uso:
Uso Pessoal e Acadêmico: Este código pode ser visualizado e estudado para fins educacionais, mas não pode ser copiado, modificado ou distribuído sem autorização expressa do autor.

Proibição de Uso Comercial: Não é permitido utilizar este software ou qualquer parte dele para fins comerciais sem uma licença formal do autor.

Integridade do Código: O código-fonte não pode ser alterado e redistribuído como trabalho próprio.

Atribuição: Qualquer referência a este projeto deve creditar Filipe Neres Fernandes como autor original.

Para solicitar permissões de uso comercial ou contribuições, entre em contato através dos canais abaixo.

📞 Contato
GitHub: github.com/eoneres

LinkedIn: Filipe Neres Fernandes

Email: filipeneresfernandes@gmail.com

