-- Criação das tabelas do Vedas Market

CREATE TABLE IF NOT EXISTS produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Usando AUTOINCREMENT para facilitar testes locais (SQLite)
    nome VARCHAR(80) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    estoque INT NOT NULL,
    categoria VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS venda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2) NOT NULL,
    pagamento VARCHAR(50)
);

-- Inserção de dados iniciais para teste (Seed)
INSERT INTO produto (nome, preco, estoque, categoria) VALUES 
('Arroz Tio João 5kg', 26.90, 50, 'Mercearia'),
('Feijão Camil 1kg', 8.50, 60, 'Mercearia'),
('Coca-Cola 2L', 9.50, 120, 'Bebidas'),
('Detergente Ypê', 2.89, 100, 'Limpeza'),
('Batata Inglesa (kg)', 5.99, 15, 'Hortifruti');