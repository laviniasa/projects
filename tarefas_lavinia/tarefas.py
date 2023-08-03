import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Função para adicionar uma tarefa
def adicionar_tarefa():
    # Código da função adicionar_tarefa que você criou anteriormente.

# Função para listar as tarefas
def listar_tarefas():
    # Código da função listar_tarefas que você criou anteriormente.

# Função para remover uma tarefa pelo ID
def remover_tarefa():
    # Código da função remover_tarefa que você criou anteriormente.

# Função para alterar o status de uma tarefa pelo ID
def alterar_status_tarefa():
    # Código da função alterar_status_tarefa que você criou anteriormente.

# Função para apagar todas as tarefas
def apagar_todas_tarefas():
    # Código da função apagar_todas_tarefas que você criou anteriormente.

# Rota para a página inicial (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de adicionar tarefa
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        adicionar_tarefa()
        return redirect(url_for('index'))
    return render_template('adicionar.html')

# Rota para a página de listar tarefas
@app.route('/listar')
def listar():
    listar_tarefas()
    return render_template('listar.html')

# Rota para a página de remover tarefa
@app.route('/remover', methods=['GET', 'POST'])
def remover():
    if request.method == 'POST':
        remover_tarefa()
        return redirect(url_for('index'))
    return render_template('remover.html')

# Rota para a página de alterar status da tarefa
@app.route('/alterar_status', methods=['GET', 'POST'])
def alterar_status():
    if request.method == 'POST':
        alterar_status_tarefa()
        return redirect(url_for('index'))
    return render_template('alterar_status.html')

# Rota para a página de apagar todas as tarefas
@app.route('/apagar_todas', methods=['GET', 'POST'])
def apagar_todas():
    if request.method == 'POST':
        apagar_todas_tarefas()
        return redirect(url_for('index'))
    return render_template('apagar_todas.html')

if __name__ == "__main__":
    app.run(debug=True)
