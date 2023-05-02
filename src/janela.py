from collections import Counter
from tkinter import *
from tkinter import ttk
from connect import cursor
import matplotlib.pyplot as plt
import numpy as np
from web01 import Web

janela = Tk()


class AppMS:
    def __init__(self):
        self.myears = [str(year) for year in range(1996, 2023)]
        self.janela = janela
        self.tela()
        self.frames()
        self.labels()
        self.botoes()
        self.lista_frame1()
        janela.mainloop()

    def tela(self):
        self.janela.title('MEGA SENA')
        self.janela.geometry('700x700')
        self.janela.iconbitmap('megasena.ico')
        self.janela.configure(background='#2FA84F')
        self.janela.resizable(True, True)
        self.janela.maxsize(width=700, height=700)

    def frames(self):
        self.frame_0 = Frame(self.janela, bg='#7AFF9E', highlightthickness=1, highlightbackground='#011013')
        self.frame_0.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.10)

        self.frame_1 = Frame(self.janela, bg='#7AFF9E', highlightthickness=1, highlightbackground='#011013')
        self.frame_1.place(relx=0.03, rely=0.15, relwidth=0.94, relheight=0.40)

        self.frame_2 = Frame(self.janela, bg='#7AFF9E', highlightthickness=1, highlightbackground='#011013')
        self.frame_2.place(relx=0.03, rely=0.57, relwidth=0.94, relheight=0.40)

    def botoes(self):
        self.btAtualizar = ttk.Button(self.frame_0, text="Atualizar", command=self.atualizar)
        self.btAtualizar.pack(side=RIGHT, padx=10, pady=10)

        self.btPesquisar = ttk.Button(self.frame_0, text="Pesquisar", command=self.pesquisar)
        self.btPesquisar.pack(side=RIGHT, padx=10, pady=10)

        self.btGrafico = ttk.Button(self.frame_2, text="Gráfico", command=self.graph)
        self.btGrafico.pack(side=LEFT, padx=10, pady=1)

    def labels(self):
        self.label_titulo = Label(self.frame_0, text="MEGA SENA", font=("Arial", 20), bg='#7AFF9E')
        self.label_titulo.place(relx=0.05, rely=0.21)

        self.label_ano = Label(self.frame_0, text="Ano:", font=("Arial", 12), bg='#7AFF9E')
        self.label_ano.place(relx=0.35, rely=0.32)

        self.combo_ano = ttk.Combobox(self.frame_0, values=self.myears, font=("sans-serif", 12))
        self.combo_ano.set(self.myears[0])
        self.combo_ano.pack()
        self.combo_ano.place(relx=0.42, rely=0.32, relwidth=0.2, relheight=0.40)

    def lista_frame1(self):
        self.listaCli = ttk.Treeview(self.frame_1, height=3, columns=('col1',
                                                                      'col2',
                                                                      'col3',
                                                                      'col4',
                                                                      'col5',
                                                                      'col6',
                                                                      'col7',
                                                                      'col8'))
        self.listaCli.heading('#0', text='')
        self.listaCli.heading('#1', text='ID')
        self.listaCli.heading('#2', text='Sorteio')
        self.listaCli.heading('#3', text='N1')
        self.listaCli.heading('#4', text='N2')
        self.listaCli.heading('#5', text='N3')
        self.listaCli.heading('#6', text='N4')
        self.listaCli.heading('#7', text='N5')
        self.listaCli.heading('#8', text='N6')

        self.listaCli.column('#0', width=0)
        self.listaCli.column('#1', width=15)
        self.listaCli.column('#2', width=50)
        self.listaCli.column('#3', width=50)
        self.listaCli.column('#4', width=50)
        self.listaCli.column('#5', width=50)
        self.listaCli.column('#6', width=50)
        self.listaCli.column('#7', width=50)
        self.listaCli.column('#8', width=50)

        self.listaCli.place(relx=0.025, rely=0.05, relwidth=0.95, relheight=0.90)

        self.scroolLista = Scrollbar(self.frame_1, orient='vertical')
        self.listaCli.configure(yscrollcommand=self.scroolLista.set)
        self.scroolLista.place(relx=0.9745, rely=0.05, relwidth=0.02, relheight=0.90)

    def atualizar(self):
        self.limpar()
        ano = self.combo_ano.get()

        cursor.execute(f"SELECT id, sorteio, numero1, numero2, numero3, numero4, numero5, numero6 FROM ms_{ano}")

        for row in cursor.fetchall():
            self.listaCli.insert("", "end", values=row)

    def pesquisar(self):
        ano = self.combo_ano.get()
        Web(ano)

        self.limpar()
        query = f"SELECT * FROM ms_{ano}"
        cursor.execute(query)

        resultados = cursor.fetchall()

        frame = []
        for resultado in resultados:
            frame.append(resultado)

    def limpar(self):
        self.listaCli.delete(*self.listaCli.get_children())

    def graph(self):
        ano = self.combo_ano.get()

        cursor.execute(f"SELECT numero1, numero2, numero3, numero4, numero5, numero6 FROM ms_{ano}")

        numeros = []
        for row in cursor.fetchall():
            numeros += row

        unique, counts = np.unique(numeros, return_counts=True)
        frequencias = dict(zip(unique, counts))
        mais_frequentes = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)[:6]

        labels = [str(n) for n, freq in mais_frequentes]
        sizes = [freq for n, freq in mais_frequentes]
        explode = [0.1] + [0] * (len(mais_frequentes) - 1)

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title(f'Números mais frequentes na Mega Sena {ano}')
        plt.axis('equal')
        plt.show()
