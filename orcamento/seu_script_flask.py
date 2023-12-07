from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Certifique-se de alterar isso para uma chave secreta mais segura

# Lista de clientes (simulação, substitua por um banco de dados real)
clientes = []

# Função utilitária para encontrar um cliente pelo ID
def encontrar_cliente_por_id(cliente_id):
    for cliente in clientes:
        if cliente['id'] == cliente_id:
            return cliente
    return None

# Página de login
@app.route('/login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Simulação de autenticação (substitua por lógica real)
        if username == 'admin' and password == 'admin123':
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Credenciais inválidas')

    return render_template('login.html')

# Página principal (cadastro de clientes)
@app.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        pedido = request.form['pedido']

        novo_cliente = {'id': len(clientes) + 1, 'nome': nome, 'email': email, 'telefone': telefone, 'pedido': pedido}
        clientes.append(novo_cliente)

    return render_template('cadastro_cliente.html', clientes=clientes)

# Rota para editar cliente
@app.route('/editar_cliente/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    if 'username' not in session:
        return redirect(url_for('index'))

    cliente = encontrar_cliente_por_id(cliente_id)

    if cliente is None:
        return redirect(url_for('cadastro_cliente'))

    if request.method == 'POST':
        # Atualize os dados do cliente
        cliente['nome'] = request.form['nome']
        cliente['email'] = request.form['email']
        cliente['telefone'] = request.form['telefone']
        cliente['pedido'] = request.form['pedido']

        return redirect(url_for('cadastro_cliente'))

    return render_template('editar_cliente.html', cliente=cliente)

# Rota para excluir cliente
@app.route('/excluir_cliente/<int:cliente_id>', methods=['GET'])
def excluir_cliente(cliente_id):
    if 'username' not in session:
        return redirect(url_for('index'))

    cliente = encontrar_cliente_por_id(cliente_id)

    if cliente is not None:
        clientes.remove(cliente)

    return redirect(url_for('cadastro_cliente'))

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
