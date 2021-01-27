from texttable import *
from datetime import datetime
from heapq import *



class Puzzle(object):
    def __init__(self, izmesana):
        self._cilj = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']
        self.nova_igra = izmesana
        self.p = self.prazna(self.nova_igra)
        self.otvoreni = []
        self.zatvoreni = []

    def zameni_dve(self, ploca):
        self.otvoreni = []
        self.nova_igra = ploca
        potezi = []
        potezi.extend(ploca)
        self.p = self.prazna(ploca)
        if self.p + 4 <= 15:
            potezi[self.p] = potezi[self.p + 4]
            potezi[self.p + 4] = '0'
            self.otvoreni.append(potezi)
            potezi = []
            potezi.extend(self.nova_igra)

        if self.p - 4 >= 0:
            potezi[self.p] = potezi[self.p - 4]
            potezi[self.p - 4] = '0'
            self.otvoreni.append(potezi)
            potezi = []
            potezi.extend(self.nova_igra)

        if self.p % 4 != 0:
            potezi[self.p] = potezi[self.p - 1]
            potezi[self.p - 1] = '0'
            self.otvoreni.append(potezi)
            potezi = []
            potezi.extend(self.nova_igra)

        if self.p % 4 != 3:
            potezi[self.p] = potezi[self.p + 1]
            potezi[self.p + 1] = '0'
            self.otvoreni.append(potezi)
            potezi = []
            potezi.extend(self.nova_igra)

        return self.otvoreni

    def algoritam(self):
        putanja = {str(self.nova_igra):None}
        zatvoreni = []
        hip = []
        heappush(hip, (self.proceni(self.nova_igra) + 2 * self.konflikt(self.nova_igra), self.nova_igra))
        while True:
            cvor = heappop(hip)
            if cvor[1] == self._cilj:
                zatvoreni.append(cvor[1])
                self.stampa(cvor[1])
                return putanja
            if cvor[1] in zatvoreni:
                continue
            zatvoreni.append(cvor[1])
            resi = self.zameni_dve(cvor[1])
            for potez in resi:
                if potez in zatvoreni:
                    continue
                heappush(hip, (self.proceni(potez) + 2 * self.konflikt(potez), potez))
                putanja.update({str(potez):cvor[1]})

    def proceni(self, lista):
        procena = 0
        for plocica in xrange(16):
            if lista[plocica] == "0":
                continue
            if lista[plocica] != self._cilj[plocica]:
                trenutna_pozicija = plocica
                ciljna_pozicija = self._cilj.index(lista[plocica])
                x = trenutna_pozicija // 4
                x1 = ciljna_pozicija // 4
                y = trenutna_pozicija % 4
                y1 = ciljna_pozicija % 4
                procena = procena + abs(x - x1) + abs(y - y1)
        return procena

    def konflikt(self, cvor):
        procena = 0
        for i in xrange(16):
            if i == 16:
                break
            if not (i % 4 == 3):
                if int(cvor[i]) == i + 1 + 1:
                    if i + 1 == int(cvor[i + 1]):
                        if '0' != cvor[i] and '0' != cvor[i + 1]:
                            procena += 1
            if i < 11:
                if i + 1 == int(cvor[i + 4]) and int(cvor[i]) == i + 4 + 1 and '0' != cvor[i] and '0' != cvor[i + 4]:
                    procena += 1
        return procena

    def prazna(self, x):
        p = x.index("0")
        return p

    def __repr__(self):
        table = Texttable()
        table.add_row(self.nova_igra[0:4])
        table.add_row(self.nova_igra[4:8])
        table.add_row(self.nova_igra[8:12])
        table.add_row(self.nova_igra[12:])
        return table.draw() + "\n"

    def stampa(self, lista):
        table = Texttable()
        table.add_row(lista[0:4])
        table.add_row(lista[4:8])
        table.add_row(lista[8:12])
        table.add_row(lista[12:])
        print table.draw() + "\n"

#5,1,7,3,9,2,11,4,13,6,15,8,0,10,14,12
#2,5,13,12,1,0,3,15,9,7,14,6,10,11,8,4
#5,2,4,8,10,0,3,14,13,6,11,12,1,15,9,7
#11,4,12,2,5,10,3,15,14,1,6,7,0,9,8,13
#5,8,7,11,1,6,12,2,9,0,13,10,14,3,4,15
if __name__ == "__main__":
    unos = raw_input("Unesite brojeve razmaknute zarezom i koristite broj 0 za prazno polje: ")
    lista = []
    splitovan_unos = unos.split(",")
    for n in splitovan_unos:
        lista.append(n)
    start = datetime.now()
    nova = Puzzle(lista)
    putanje = nova.algoritam()
    kraj = datetime.now()
    resenje = putanje["['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']"]
    broj_koraka = 0
    while putanje[str(resenje)] is not None:
        nova.stampa(resenje)
        print "======================\n"
        resenje = putanje[str(resenje)]
        broj_koraka = broj_koraka + 1
    print broj_koraka
    vreme = kraj - start
    print 'Proteklo vreme: ', vreme