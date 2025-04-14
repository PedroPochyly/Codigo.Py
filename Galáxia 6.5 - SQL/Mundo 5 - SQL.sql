CREATE DATABASE codigopy;

USE codigopy;

CREATE TABLE stocks (
id int primary key auto_increment, 
symbol varchar(10) not null,
name varchar(100),
sector varchar(50) default 'indefinido',
price decimal(10,2), #Números totais na frente e quantas casas decimais a direita.
volume BIGINT
);
	DROP TABLE stocks
    DESCRIBE stocks;
    
    
    #podemos criar a tabela de transações também

CREATE TABLE transactions (
	id INTEGER PRIMARY KEY,
    date DATE,
    type ENUM('compra', 'venda'), #ENUM - limita as possibilidades do que você pode colocar na coluna
    symbol VARCHAR(10),
    shares INTEGER UNSIGNED, #unsigned é apenas para permitir números positivos
    price DECIMAL(10,2),
    customer_id INTEGER
    );
    
CREATE TABLE customers (
	customer_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(15)
);

#Exercício 116 - 
CREATE DATABASE exercício116;

OPEN DATABASE exercício116;

CREATE TABLE exercício116 (
	id INTEGER PRIMARY KEY auto_increment NOT NULL,
    date DATE NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    open DECIMAL(10,2),
    high DECIMAL(10,2),
    low DECIMAL(10,2),
    close DECIMAL(10,2),
);
