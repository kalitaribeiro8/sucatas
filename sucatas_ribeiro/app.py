from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Banco de dados inicial
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS compras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    preco REAL NOT NULL,
                    peso REAL NOT NULL,
                    data TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    # Preços fictícios
    precos = {
        'Ferro': 1.50,
        'Alumínio': 4.00,
        'Cobre': 15.00,
        'Latão': 10.00
    }
    return render_template('index.html', precos=precos)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        tipo = request.form['tipo']
        preco = float(request.form['preco'])
        peso = float(request.form['peso'])
        data = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO compras (tipo, preco, peso, data) VALUES (?, ?, ?, ?)", 
                  (tipo, preco, peso, data))
        conn.commit()
        conn.close()
        return redirect('/')
    
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
