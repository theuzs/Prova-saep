from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conectar ao banco de dados
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            descricao TEXT NOT NULL,
            setor TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            data_cadastro TEXT NOT NULL,
            status TEXT DEFAULT 'a fazer',
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    conn.close()

# Rota principal
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
    SELECT tarefas.id, tarefas.id_usuario, tarefas.descricao, tarefas.setor, 
           tarefas.prioridade, tarefas.data_cadastro, tarefas.status, usuarios.nome 
    FROM tarefas
    JOIN usuarios ON tarefas.id_usuario = usuarios.id
    """)
    tarefas = c.fetchall()

    # c.execute("SELECT * FROM tarefas")
    # tarefas = c.fetchall()
    conn.close()
    return render_template('index.html', tarefas=tarefas)

# Rota para adicionar usuário
@app.route('/add_usuario', methods=['GET', 'POST'])
def add_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_usuario.html')

# Rota para adicionar tarefa
@app.route('/add_tarefa', methods=['GET', 'POST'])
def add_tarefa():
    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        descricao = request.form['descricao']
        setor = request.form['setor']
        prioridade = request.form['prioridade']
        data_cadastro = request.form['data_cadastro']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO tarefas (id_usuario, descricao, setor, prioridade, data_cadastro)
            VALUES (?, ?, ?, ?, ?)
        """, (id_usuario, descricao, setor, prioridade, data_cadastro))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    # Buscar usuários para exibir no formulário
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, nome FROM usuarios")
    usuarios = c.fetchall()
    conn.close()
    return render_template('add_tarefa.html', usuarios=usuarios)

# Rota para mudar o status da tarefa
@app.route('/mudar_status/<int:tarefa_id>', methods=['POST'])
def mudar_status(tarefa_id):
    novo_status = request.form['status']
    if novo_status in ['a fazer', 'fazendo', 'pronto']:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE tarefas SET status = ? WHERE id = ?", (novo_status, tarefa_id))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

    # Rota para excluir tarefa
@app.route('/excluir_tarefa/<int:tarefa_id>', methods=['POST'])
def excluir_tarefa(tarefa_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Rota para editar tarefa
@app.route('/editar_tarefa/<int:tarefa_id>', methods=['GET', 'POST'])
def editar_tarefa(tarefa_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if request.method == 'POST':
        descricao = request.form['descricao']
        setor = request.form['setor']
        prioridade = request.form['prioridade']
        status = request.form['status']
        c.execute("""
            UPDATE tarefas
            SET descricao = ?, setor = ?, prioridade = ?, status = ?
            WHERE id = ?
        """, (descricao, setor, prioridade, status, tarefa_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    c.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,))
    tarefa = c.fetchone()
    conn.close()
    return render_template('editar_tarefa.html', tarefa=tarefa)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)