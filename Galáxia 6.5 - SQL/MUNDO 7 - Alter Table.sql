USE codigopy;

DESCRIBE stocks;

SELECT * FROM stocks;

ALTER TABLE stocks
ADD COLUMN price_date DATE after symbol;

DESCRIBE stocks;

ALTER TABLE stocks
DROP COLUMN price_date;

ALTER TABLE stocks
MODIFY COLUMN symbol VARCHAR(20) NOT NULL;
