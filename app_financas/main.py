import mysql.connector
import matplotlib.pyplot as plt  # Adicionar esta linha para importar o módulo de plotagem
import mysql.connector
from datetime import datetime

# Função para conectar ao banco de dados MySQL
def conectar_banco_dados():
# Substitua 'seu_usuario', 'sua_senha' e 'seu_host' pelas credenciais do seu banco de dados
    conexao = mysql.connector.connect(
        user='novo_usuario',
        password='nova_senha',
        host='localhost',
        database='gerenciamento_financeiro'
)
    return conexao

# Função para criar a tabela "transacoes" no banco de dados
def criar_tabela_transacoes(conexao):
    cursor = conexao.cursor()

    criar_tabela = """
    CREATE TABLE IF NOT EXISTS transacoes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        data DATE NOT NULL,
        descricao VARCHAR(255) NOT NULL,
        valor DECIMAL(10, 2) NOT NULL,
        tipo VARCHAR(10) NOT NULL,
        categoria VARCHAR(50)
    )
    """

    cursor.execute(criar_tabela)
    conexao.commit()
    cursor.close()

# Função para adicionar transações ao banco de dados
def adicionar_transacao(conexao):
    cursor = conexao.cursor()

    data = input("Digite a data da transação (YYYY-MM-DD): ")
    descricao = input("Digite a descrição da transação: ")
    valor = float(input("Digite o valor da transação: "))
    tipo = input("Digite o tipo da transação (Receita ou Despesa): ")
    categoria = input("Digite a categoria da transação: ")

    inserir_transacao = """
    INSERT INTO transacoes (data, descricao, valor, tipo, categoria) VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(inserir_transacao, (data, descricao, valor, tipo, categoria))
    conexao.commit()
    print("Transação adicionada com sucesso.")
    # Gerar relatórios e gráficos após adicionar a transação
    gerar_relatorios_graficos(conexao)
    cursor.close()

# Função para exibir as transações do banco de dados
def exibir_transacoes(conexao):
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM transacoes")
    transacoes = cursor.fetchall()

    print("\nTransações Registradas:")
    for transacao in transacoes:
        print(f"ID: {transacao[0]}, Data: {transacao[1]}, Descrição: {transacao[2]}, Valor: {transacao[3]}, Tipo: {transacao[4]}, Categoria: {transacao[5]}")

    cursor.close()

# Função editar_transacao

def editar_transacao(conexao):
    cursor = conexao.cursor()

    transacao_id = int(input("Digite o ID da transação que deseja editar: "))

    # Verificar se a transação com o ID informado existe
    cursor.execute("SELECT * FROM transacoes WHERE id = %s", (transacao_id,))
    transacao = cursor.fetchone()

    if not transacao:
        print("Transação não encontrada.")
        return

    print("Transação encontrada:")
    print(f"ID: {transacao[0]}, Data: {transacao[1]}, Descrição: {transacao[2]}, Valor: {transacao[3]}, Tipo: {transacao[4]}, Categoria: {transacao[5]}")

    # Receber as novas informações da transação
    nova_data = input("Digite a nova data da transação (YYYY-MM-DD): ")
    nova_descricao = input("Digite a nova descrição da transação: ")
    novo_valor = float(input("Digite o novo valor da transação: "))
    novo_tipo = input("Digite o novo tipo da transação (Receita ou Despesa): ")
    nova_categoria = input("Digite a nova categoria da transação: ")

    # Atualizar a transação no banco de dados
    atualizar_transacao = """
    UPDATE transacoes
    SET data = %s, descricao = %s, valor = %s, tipo = %s, categoria = %s
    WHERE id = %s
    """
    cursor.execute(atualizar_transacao, (nova_data, nova_descricao, novo_valor, novo_tipo, nova_categoria, transacao_id))
    conexao.commit()

    print("Transação atualizada com sucesso.")

    cursor.close()

# Função excluir_transacao

def excluir_transacao(conexao):
    cursor = conexao.cursor()

    transacao_id = int(input("Digite o ID da transação que deseja excluir: "))

    # Verificar se a transação com o ID informado existe
    cursor.execute("SELECT * FROM transacoes WHERE id = %s", (transacao_id,))
    transacao = cursor.fetchone()

    if not transacao:
        print("Transação não encontrada.")
        return

    print("Transação encontrada:")
    print(f"ID: {transacao[0]}, Data: {transacao[1]}, Descrição: {transacao[2]}, Valor: {transacao[3]}, Tipo: {transacao[4]}, Categoria: {transacao[5]}")

    # Confirmar a exclusão da transação
    confirmacao = input("Tem certeza que deseja excluir esta transação? (S/N): ").strip().lower()

    if confirmacao == 's':
        # Excluir a transação do banco de dados
        excluir_transacao = "DELETE FROM transacoes WHERE id = %s"
        cursor.execute(excluir_transacao, (transacao_id,))
        conexao.commit()

        print("Transação excluída com sucesso.")
    else:
        print("Exclusão cancelada.")

    cursor.close()

# Função para gerar relatórios e gráficos
def gerar_relatorios_graficos(conexao):
    cursor = conexao.cursor()

    # Cálculo das despesas totais
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'Despesa'")
    total_despesas = cursor.fetchone()[0]
    if total_despesas is None:
        total_despesas = 0.0

    # Cálculo das receitas totais
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'Receita'")
    total_receitas = cursor.fetchone()[0]
    if total_receitas is None:
        total_receitas = 0.0

    # Exibição do resumo das transações
    print("\n--- RESUMO DAS TRANSAÇÕES ---")
    print(f"Total de Despesas: R$ {total_despesas:.2f}")
    print(f"Total de Receitas: R$ {total_receitas:.2f}")

    # Cálculo e criação do gráfico de distribuição de categorias
    #cursor.execute("SELECT categoria, SUM(valor) FROM transacoes GROUP BY categoria")
    #dados_categorias = dict(cursor.fetchall())

    cursor.close()

# Função para excluir todas as transações do banco de dados
def excluir_todas_transacoes(conexao):
    cursor = conexao.cursor()

    # Confirmar a exclusão de todas as transações
    confirmacao = input("Tem certeza que deseja excluir TODAS as transações? (S/N): ").strip().lower()

    if confirmacao == 's':
        # Excluir todas as transações do banco de dados
        excluir_todas_transacoes = "DELETE FROM transacoes"
        cursor.execute(excluir_todas_transacoes)
        conexao.commit()

        print("Todas as transações foram excluídas com sucesso.")
    else:
        print("Exclusão cancelada.")

    cursor.close()
# Função para calcular o saldo
def verificar_saldo(conexao):
    cursor = conexao.cursor()

    # Calcular total de receitas
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'Receita'")
    total_receitas = cursor.fetchone()[0]
    if total_receitas is None:
        total_receitas = 0

    # Calcular total de despesas
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'Despesa'")
    total_despesas = cursor.fetchone()[0]
    if total_despesas is None:
        total_despesas = 0

    # Calcular o saldo total
    saldo_total = total_receitas - total_despesas

    if saldo_total >= 0:
        print(f"Você não está devendo. Seu saldo é R$ {saldo_total:.2f}")
    else:
        print(f"Você está devendo. Seu saldo é R$ {saldo_total:.2f}")

    cursor.close()

# Função para validar o formato da data (YYYY-MM-DD)
def validar_data(data):
    try:
        # Verifica se a data está no formato correto (YYYY-MM-DD)
        # e se é uma data válida
        return bool(datetime.strptime(data, '%Y-%m-%d'))
    
    except ValueError:
        return False

# Função para validar o formato do valor (decimal)
def validar_valor(valor):
    try:
        # Verifica se o valor pode ser convertido para float
        float(valor)
        return True
    except ValueError:
        return False

# Função para validar o tipo da transação (Receita ou Despesa)
def validar_tipo(tipo):
    tipos_validos = ['Receita', 'Despesa']
    return tipo in tipos_validos

# Função para adicionar transações ao banco de dados com validações
def adicionar_transacao(conexao):
    cursor = conexao.cursor()

    data = input("Digite a data da transação (YYYY-MM-DD): ")
    while not validar_data(data):
        print("Data inválida. Digite no formato YYYY-MM-DD.")
        data = input("Digite a data da transação (YYYY-MM-DD): ")

    descricao = input("Digite a descrição da transação: ")
    valor = input("Digite o valor da transação: ")
    while not validar_valor(valor):
        print("Valor inválido. Digite um valor numérico.")
        valor = input("Digite o valor da transação: ")

    tipo = input("Digite o tipo da transação (Receita ou Despesa): ")
    while not validar_tipo(tipo):
        print("Tipo inválido. Digite Receita ou Despesa.")
        tipo = input("Digite o tipo da transação (Receita ou Despesa): ")

    categoria = input("Digite a categoria da transação: ")

    inserir_transacao = """
    INSERT INTO transacoes (data, descricao, valor, tipo, categoria) VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(inserir_transacao, (data, descricao, valor, tipo, categoria))
    conexao.commit()
    cursor.close()

# Função principal do menu
def menu():
    conexao = conectar_banco_dados()
    criar_tabela_transacoes(conexao)

    while True:
        print("\n--- MENU ---")
        print("1. Adicionar Transação")
        print("2. Exibir Transações")
        print("3. Editar Transação")
        print("4. Excluir Transação")
        print("5. Excluir Todas as Transações")
        print("6. Gerar Relatórios")
        print("7. Verificar Saldo")
        print("8. Sair")

        opcao = input("Escolha uma opção (de 1 à 8): ")

        if opcao == '1':
            adicionar_transacao(conexao)
        elif opcao == '2':
            exibir_transacoes(conexao)
        elif opcao == '3':
            editar_transacao(conexao)
        elif opcao == '4':
            excluir_transacao(conexao)
        elif opcao == '5':
            excluir_todas_transacoes(conexao)
        elif opcao == '6':
            gerar_relatorios_graficos(conexao)
        elif opcao == '7':
            verificar_saldo(conexao)  # Chamar a nova função criada
        elif opcao == '8':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

    conexao.close()

if __name__ == "__main__":
    menu()
