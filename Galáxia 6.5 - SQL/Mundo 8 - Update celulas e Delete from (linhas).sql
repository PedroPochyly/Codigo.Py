USE codigopy;

SELECT * FROM stocks;

# Manipulando Linhas

UPDATE stocks
SET sector = "Petroleo"
WHERE id = 5;

# Condição sem chave primária

UPDATE stocks
SET sector = "Petroleo"
WHERE symbol = "PETR4";

SET SQL_SAFE_UPDATES = 0;

UPDATE stocks
SET volume = 10000, name = "Petrobras"
WHERE id = 1;

UPDATE stocks
SET symbol = "PETR4"
WHERE id = 1;

UPDATE stocks
SET price = 100
WHERE id = 1;

#deletando linhas interias

DELETE FROM stocks
WHERE id = 1;



