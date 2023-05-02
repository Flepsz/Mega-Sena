CREATE DATABASE mega_sena;

USE mega_sena;

CREATE TABLE resultados_ms_2022 (
    id INT AUTO_INCREMENT PRIMARY KEY,
	sorteio INT NOT NULL,
	numero1 NUMERIC(2) NOT NULL,
    numero2 NUMERIC(2) NOT NULL,
    numero3 NUMERIC(2) NOT NULL,
    numero4 NUMERIC(2) NOT NULL,
    numero5 NUMERIC(2) NOT NULL,
    numero6 NUMERIC(2) NOT NULL
);