import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'novo_usuario',
    'password': 'nova_senha',
    'database': 'task_manager'
}

# Função para conectar ao banco de dados
def connect_to_database():
    return mysql.connector.connect(**db_config)

# Função para adicionar uma tarefa
def adicionar_tarefa(descricao, data_termino, status):
    conexao = connect_to_database()
    cursor = conexao.cursor()

    query = "INSERT INTO tarefas (descricao, data_termino, status) VALUES (%s, %s, %s)"
    dados = (descricao, data_termino, status)

    try:
        cursor.execute(query, dados)
        conexao.commit()
        print("Tarefa adicionada com sucesso!")
    except mysql.connector.Error as erro:
        print(f"Erro ao adicionar a tarefa: {erro}")
    finally:
        cursor.close()
        conexao.close()

# Função para listar as tarefas
def listar_tarefas():
    conexao = connect_to_database()
    cursor = conexao.cursor()

    query = "SELECT id, descricao, data_termino, status FROM tarefas"

    try:
        cursor.execute(query)
        tarefas = cursor.fetchall()
        return tarefas
    except mysql.connector.Error as erro:
        print(f"Erro ao listar as tarefas: {erro}")
    finally:
        cursor.close()
        conexao.close()

@app.route('/')
def index():
    tarefas = listar_tarefas()
    return render_template('index.html', tarefas=tarefas)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    descricao = request.form['descricao']
    data_termino = request.form['data_termino']
    status = request.form['status']
    adicionar_tarefa(descricao, data_termino, status)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
