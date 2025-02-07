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
    c.execute("SELECT * FROM tarefas")
    tarefas = c.fetchall()
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
    return render_template('add_tarefa.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
