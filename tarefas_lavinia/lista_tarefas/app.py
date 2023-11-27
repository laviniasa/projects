from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista de tarefas (cada tarefa é um dicionário)
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    if task_text:
        task = {'text': task_text, 'completed': False}
        tasks.append(task)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        del tasks[task_id]
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>')
def edit_task(task_id):
    task = tasks[task_id]['text']
    return render_template('edit_task.html', task=task, task_id=task_id)

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    updated_text = request.form.get('updated_task')
    if 0 <= task_id < len(tasks):
        tasks[task_id]['text'] = updated_text
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
