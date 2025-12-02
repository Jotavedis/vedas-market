import sqlite3
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
DB_NAME = "vedas_market.db"

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Permite acessar colunas pelo nome
    return conn

# Inicializa o banco de dados na primeira execução
def init_db():
    with app.app_context():
        conn = get_db_connection()
        with open('schema.sql', mode='r') as f:
            conn.cursor().executescript(f.read())
        conn.commit()
        conn.close()

# ROTA 1: Página Principal (Frontend)
@app.route('/')
def index():
    return render_template('index.html')

# ROTA 2: API para listar produtos (GET)
@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM produto').fetchall()
    conn.close()
    # Converte para lista de dicionários
    lista_produtos = [dict(ix) for ix in produtos]
    return jsonify(lista_produtos)

# ROTA 3: API para registrar venda (POST)
@app.route('/api/vendas', methods=['POST'])
def registrar_venda():
    dados = request.get_json()
    itens = dados.get('itens')
    total = dados.get('total')
    pagamento = dados.get('pagamento')

    if not itens:
        return jsonify({"erro": "Carrinho vazio"}), 400

    conn = get_db_connection()
    try:
        # 1. Registrar a Venda (Cabeçalho)
        cur = conn.cursor()
        cur.execute("INSERT INTO venda (total, pagamento) VALUES (?, ?)", (total, pagamento))
        venda_id = cur.lastrowid

        # 2. Baixar Estoque (Simulação simples sem tabela N:M para brevidade do código)
        for item in itens:
            # Verifica estoque atual
            prod = conn.execute("SELECT estoque FROM produto WHERE id = ?", (item['id'],)).fetchone()
            if prod['estoque'] < item['quantidade']:
                raise Exception(f"Estoque insuficiente para o produto ID {item['id']}")
            
            # Atualiza estoque
            conn.execute("UPDATE produto SET estoque = estoque - ? WHERE id = ?", 
                         (item['quantidade'], item['id']))

        conn.commit()
        return jsonify({"mensagem": "Venda realizada com sucesso!", "venda_id": venda_id}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    # Cria o banco se não existir e roda o app
    try:
        init_db()
        print("Banco de dados inicializado.")
    except Exception as e:
        print("Banco já existe ou erro na criação:", e)
    
    app.run(debug=True, port=5000)