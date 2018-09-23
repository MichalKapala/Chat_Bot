import sqlite3
import random as rd

class Chat():
    def __init__(self):
        self.connection = sqlite3.connect('Pytania.db')
        self.c = self.connection.cursor()
        self.d = self.connection.cursor()
        self.confidence = 1.0

    def zamien(self,wyraz):
        wyraz = wyraz.replace('?', '')
        wyraz = wyraz.replace(' ', '')
        wyraz = wyraz.replace('!', '')

        return wyraz

    def wyrazy(self, pytanie):

        list = []
        wyraz = ''

        for i in pytanie:
            if i != ' ':
                wyraz += i
            else:
                if len(wyraz) > 0:
                    list.append(self.zamien(wyraz))
                    wyraz = ''
        if len(wyraz) > 0:
            list.append(self.zamien(wyraz))
        return list

    def get_odp(self, pytanie):
        pytanie = pytanie.title()
        wyraz = self.wyrazy(pytanie)
        self.confidence = len(wyraz)
        a = []
        b = []
        c =[]
        poczatek = wyraz[0]
        licznik = 0
        pyt= (pytanie, )
        print(pytanie)
        self.c.execute("SELECT odpowiedz FROM przywitanie WHERE pytanie=?", pyt)
        odp_c = self.c.fetchall()
        if len(odp_c) > 0:
            return list(odp_c)
        else:
            for i in range(len(wyraz)):
                fraza = '%' + wyraz[i] + '%'
                fr = (poczatek, fraza,)
                self.d.execute("SELECT odpowiedz FROM przywitanie WHERE poczatek=? AND pytanie LIKE ?", fr)
                wsk = self.d.fetchall()
                #print(wyraz[i])
                #print('wsk: ', wsk)


                if i == 0:
                    for j in wsk:
                        a.append(j)
                else:
                    for j in wsk:
                        b.append(j)
                    print('A:', a)
                    print('B:', b)
                    c = set(a) & set(b)
                    print('C:', c)
                    if len(c) == 0:
                        c =set(a)| set(b)
                        licznik +=1
                    a = c
                    b = []

            self.confidence = (self.confidence - licznik) / self.confidence
            if len(c)==0: c = a
            return list(c)

    def odpowiedz(self, pytanie):
        odp = self.get_odp(pytanie)
        print(self.confidence)
        print(odp)

        if len(odp) > 0 and self.confidence > 0.49 :
            odp = odp[rd.randint(0, len(odp) - 1)]
            odp = str(odp)
            odp = odp[2:len(odp) - 3]
        else:
            odp = "Nie rozumiem cię, dopiero się ucze"
            plik = open("wyjatki.txt", 'a')
            plik.write(pytanie + '\n')
            plik.close()
        return odp

    def exit(self):
        self.d.close()
        self.c.close()
        self.connection.close()