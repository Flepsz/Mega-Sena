from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

from connect import con, cursor


class Web:
    def __init__(self, year):
        self.year = str(year)
        self.site = f'https://asloterias.com.br/resultados-da-mega-sena-{self.year}'
        self.map = {
            'sorteio': {
                'xpath': '/html/body/main/div[2]/div/div/div[1]/strong[%nsorteio%]'
            },
            'numero': {
                'xpath': '/html/body/main/div[2]/div/div/div[1]/span[%numero%]'
            }
        }
        self.con = con
        self.cursor = cursor
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.criar_tabela()
        self.abrir_site()

    def abrir_site(self):
        self.driver.get(self.site)
        sleep(5)
        k = 0
        resultados = []
        num_sorteios = len(self.driver.find_elements(By.XPATH, '/html/body/main/div[2]/div/div/div[1]/strong'))
        print(num_sorteios)
        for i in range(num_sorteios - 4):
            sorteio = int(
                self.driver.find_element(By.XPATH, self.map['sorteio']['xpath'].replace('%nsorteio%', f'{i + 4}')).text)
            numeros = []
            for j in range(6):
                numero = (int(self.driver.find_element(By.XPATH, self.map['numero']['xpath'].replace('%numero%',
                                                                                                     f'{k + 1}')).text))
                if numero != "Mega da Virada":
                    numeros.append(numero)
                    k += 1

            resultados.append((sorteio, *numeros))

        query = f"INSERT INTO ms_{self.year} (sorteio, numero1, numero2, numero3, numero4, numero5, numero6) VALUES (" \
                f"%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.executemany(query, resultados)

        self.con.commit()

    def criar_tabela(self):
        self.cursor.execute(
            f"SELECT * FROM information_schema.tables WHERE table_name = 'ms_{self.year}'")
        table_exists = self.cursor.fetchone()

        if table_exists:
            self.cursor.execute(f"DROP TABLE IF EXISTS ms_{self.year}")

        self.cursor.execute(
            f"CREATE TABLE ms_{self.year} (id INT AUTO_INCREMENT PRIMARY KEY, sorteio INT NOT NULL, numero1 NUMERIC("
            f"2) NOT NULL, numero2 NUMERIC(2) NOT NULL, numero3 NUMERIC(2) NOT NULL, numero4 NUMERIC(2) NOT NULL, "
            f"numero5 NUMERIC(2) NOT NULL, numero6 NUMERIC(2) NOT NULL)")
        self.con.commit()
