INSERT INTO nome_da_tabela (column1, column2, column3) VALUES (value1, value2, value3);

USE codigopy;

INSERT INTO stocks(symbol, name, sector, price, volume) VALUES ('APPL', 'Apple Inc.', 'Tecnologia', 102.20, 123456);

#e se eu quiser inserir varias informações ao mesmo tempo?

INSERT INTO stocks(symbol, name, sector, price, volume) VALUES ('APPL', 'Apple Inc.', 'Tecnologia', 102.20, 123456),
																('GOOG', 'Google LLC', 'Tecnologia', 131.22, 45456),
                                                                ('FB', 'Facebook Inc.', 'Tecnologia', 90.15, 1231233);

