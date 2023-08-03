import mysql.connector
import matplotlib.pyplot as plt


conexao = mysql.connector.connect(
    host='localhost',
    user='novo_usuario',
    password='nova_senha',
    database='biblioteca'
)

def gerar_relatorios_graficos(conexao):
    cursor = conexao.cursor()

    # Total de Despesas
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'Despesa'")
    total_despesas = cursor.fetchone()[0]

    # Total de Receitas
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'Receita'")
    total_receitas = cursor.fetchone()[0]

    # Distribuição de Categorias
    cursor.execute("SELECT categoria, SUM(valor) FROM transacoes GROUP BY categoria")
    dados_categorias = dict(cursor.fetchall())

    # Exibir relatório
    print("\n--- RESUMO DAS TRANSAÇÕES ---")
    print(f"Total de Despesas: R$ {total_despesas:.2f}")
    print(f"Total de Receitas: R$ {total_receitas:.2f}")

    # Gráfico de Pizza
    if dados_categorias:
        plt.figure(figsize=(8, 6))
        plt.pie(dados_categorias.values(), labels=dados_categorias.keys(), autopct='%1.1f%%')
        plt.title("Distribuição de Categorias das Transações")
        plt.show()
    else:
        print("Não há transações cadastradas para exibir o gráfico de pizza.")

    cursor.close()


def cadastrar_livro(conexao):
    cursor = conexao.cursor()

    titulo = input("Digite o título do livro: ")
    autor = input("Digite o autor do livro: ")
    ano_publicacao = int(input("Digite o ano de publicação do livro: "))
    categoria = input("Digite a categoria do livro: ")

    inserir_livro = """
    INSERT INTO livros (titulo, autor, ano_publicacao, categoria) VALUES (%s, %s, %s, %s)
    """
    cursor.execute(inserir_livro, (titulo, autor, ano_publicacao, categoria))
    conexao.commit()
    cursor.close()

    print("Livro cadastrado com sucesso.")


def cadastrar_usuario(conexao):
    cursor = conexao.cursor()

    nome = input("Digite o nome do usuário: ")
    email = input("Digite o email do usuário: ")
    telefone = input("Digite o telefone do usuário: ")
    endereco = input("Digite o endereço do usuário: ")

    inserir_usuario = """
    INSERT INTO usuarios (nome, email, telefone, endereco) VALUES (%s, %s, %s, %s)
    """
    cursor.execute(inserir_usuario, (nome, email, telefone, endereco))
    conexao.commit()
    cursor.close()

    print("Usuário cadastrado com sucesso.")

def emprestimo_livro(conexao):
    cursor = conexao.cursor()

    # Exibir lista de livros disponíveis para empréstimo
    cursor.execute("SELECT id, titulo FROM livros WHERE status = 'disponivel'")
    livros_disponiveis = cursor.fetchall()

    if not livros_disponiveis:
        print("Não há livros disponíveis para empréstimo no momento.")
        return

    print("Livros Disponíveis para Empréstimo:")
    for livro in livros_disponiveis:
        print(f"{livro[0]}. {livro[1]}")

    livro_id = int(input("Digite o ID do livro que deseja emprestar: "))

    # Verificar se o livro selecionado está disponível
    if livro_id not in [livro[0] for livro in livros_disponiveis]:
        print("Livro não encontrado ou não está disponível para empréstimo.")
        return

    # Exibir lista de usuários cadastrados
    cursor.execute("SELECT id, nome FROM usuarios")
    usuarios = cursor.fetchall()

    print("Usuários Cadastrados:")
    for usuario in usuarios:
        print(f"{usuario[0]}. {usuario[1]}")

    usuario_id = int(input("Digite o ID do usuário que irá pegar o livro emprestado: "))

    # Verificar se o usuário selecionado está cadastrado
    if usuario_id not in [usuario[0] for usuario in usuarios]:
        print("Usuário não encontrado ou não está cadastrado.")
        return

    # Registrar o empréstimo do livro na tabela de empréstimos
    registrar_emprestimo = """
    INSERT INTO emprestimos (livro_id, usuario_id, data_emprestimo, data_devolucao) 
    VALUES (%s, %s, CURRENT_DATE, NULL)
    """
    cursor.execute(registrar_emprestimo, (livro_id, usuario_id))
    conexao.commit()

    # Atualizar o status do livro para emprestado na tabela de livros
    atualizar_status_livro = """
    UPDATE livros SET status = 'emprestado' WHERE id = %s
    """
    cursor.execute(atualizar_status_livro, (livro_id,))
    conexao.commit()

    print("Empréstimo registrado com sucesso.")

    cursor.close()

def devolucao_livro(conexao):
    cursor = conexao.cursor()

    # Exibir lista de livros emprestados
    cursor.execute("SELECT emprestimos.id, livros.titulo, usuarios.nome FROM emprestimos "
                   "JOIN livros ON emprestimos.livro_id = livros.id "
                   "JOIN usuarios ON emprestimos.usuario_id = usuarios.id "
                   "WHERE emprestimos.data_devolucao IS NULL")
    livros_emprestados = cursor.fetchall()

    if not livros_emprestados:
        print("Não há livros emprestados no momento.")
        return

    print("Livros Emprestados:")
    for emprestimo in livros_emprestados:
        print(f"{emprestimo[0]}. Livro: {emprestimo[1]}, Usuário: {emprestimo[2]}")

    emprestimo_id = int(input("Digite o ID do empréstimo que deseja registrar a devolução: "))

    # Encontrar o empréstimo com o ID fornecido pelo usuário
    emprestimo_encontrado = None
    for emprestimo in livros_emprestados:
        if emprestimo[0] == emprestimo_id:
            emprestimo_encontrado = emprestimo
            break

    if emprestimo_encontrado is None:
        print("ID de empréstimo inválido.")
        return

    # Registrar a devolução do livro na tabela de empréstimos
    registrar_devolucao = """
    UPDATE emprestimos SET data_devolucao = CURRENT_DATE WHERE id = %s
    """
    cursor.execute(registrar_devolucao, (emprestimo_id,))
    conexao.commit()

    # Atualizar o status do livro para disponível na tabela de livros
    livro_id = emprestimo_encontrado[0]
    atualizar_status_livro = """
    UPDATE livros SET status = 'disponivel' WHERE id = %s
    """
    cursor.execute(atualizar_status_livro, (livro_id,))
    conexao.commit()

    print("Devolução registrada com sucesso.")

    cursor.close()


def excluir_transacoes(conexao):
    cursor = conexao.cursor()

    confirmacao = input("Tem certeza que deseja excluir TODAS as transações? (S/N): ").strip().lower()

    if confirmacao == 's':
        excluir_todas_transacoes = "DELETE FROM transacoes"
        cursor.execute(excluir_todas_transacoes)
        conexao.commit()

        print("Todas as transações foram excluídas.")
    else:
        print("Exclusão cancelada.")

    cursor.close()

def verificar_debito(conexao):
    cursor = conexao.cursor()

    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'Despesa'")
    total_despesas = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'Receita'")
    total_receitas = cursor.fetchone()[0]

    saldo_debito = total_receitas - total_despesas

    if saldo_debito < 0:
        print(f"Você está devendo R$ {abs(saldo_debito):.2f}.")
    elif saldo_debito == 0:
        print("Seu saldo está zerado.")
    else:
        print(f"Seu saldo credor é de R$ {saldo_debito:.2f}.")

    cursor.close()

def consultar_livro_por_titulo(conexao, titulo):
    cursor = conexao.cursor()
    consulta = "SELECT * FROM livros WHERE titulo = %s"
    cursor.execute(consulta, (titulo,))
    livros_encontrados = cursor.fetchall()
    cursor.close()
    return livros_encontrados

def consultar_usuario_por_nome(conexao, nome):
    cursor = conexao.cursor()
    consulta = "SELECT * FROM usuarios WHERE nome = %s"
    cursor.execute(consulta, (nome,))
    usuarios_encontrados = cursor.fetchall()
    cursor.close()
    return usuarios_encontrados

def consultar_emprestimos_por_titulo_livro(conexao, titulo_livro):
    cursor = conexao.cursor()
    consulta = "SELECT emprestimos.*, usuarios.nome FROM emprestimos " \
               "JOIN livros ON emprestimos.livro_id = livros.id " \
               "JOIN usuarios ON emprestimos.usuario_id = usuarios.id " \
               "WHERE livros.titulo = %s"
    cursor.execute(consulta, (titulo_livro,))
    emprestimos_encontrados = cursor.fetchall()
    cursor.close()
    return emprestimos_encontrados


def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Cadastrar Livro")
        print("2. Cadastrar Usuário")
        print("3. Empréstimo de Livro")
        print("4. Devolução de Livro")
        print("5. Consultar Livro por Título")
        print("6. Consultar Usuário por Nome")
        print("7. Consultar Empréstimos por Título do Livro")
        print("8. Relatórios e Gráficos")
        print("9. Excluir Todas as Transações")
        print("10. Verificar Se Estou Devendo")
        print("0. Sair")

        opcao = input("Escolha uma opção (1/2/3/4/5/6/7/8/9/10/0): ")

        if opcao == '1':
            cadastrar_livro(conexao)
        elif opcao == '2':
            cadastrar_usuario(conexao)
        elif opcao == '3':
            emprestimo_livro(conexao)
        elif opcao == '4':
            devolucao_livro(conexao)
        elif opcao == '5':
            titulo_livro = input("Digite o título do livro que deseja consultar: ")
            livros_encontrados = consultar_livro_por_titulo(conexao, titulo_livro)
            exibir_resultado_consulta("Livros Encontrados", livros_encontrados)
        elif opcao == '6':
            nome_usuario = input("Digite o nome do usuário que deseja consultar: ")
            usuarios_encontrados = consultar_usuario_por_nome(conexao, nome_usuario)
            exibir_resultado_consulta("Usuários Encontrados", usuarios_encontrados)
        elif opcao == '7':
            titulo_livro = input("Digite o título do livro para consultar os empréstimos relacionados: ")
            emprestimos_encontrados = consultar_emprestimos_por_titulo_livro(conexao, titulo_livro)
            exibir_resultado_consulta("Empréstimos Encontrados", emprestimos_encontrados)
        elif opcao == '8':
            gerar_relatorios_graficos(conexao)
        elif opcao == '9':
            excluir_transacoes(conexao)
        elif opcao == '10':
            verificar_debito(conexao)
        elif opcao == '0':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

    conexao.close()


def exibir_resultado_consulta(titulo, resultados):
    if not resultados:
        print(f"{titulo}: Nenhum resultado encontrado.")
    else:
        print(f"\n{titulo}:")
        for resultado in resultados:
            print(resultado)

if __name__ == "__main__":
    menu()

