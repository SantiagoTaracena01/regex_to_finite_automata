
from operator import index
from Nodo import Nodo
from Fila_Transiciones import Fila
import graphviz

class AFDmin:
    __states = {}
    __alphabet = {}
    __mapping = {}
    __initial_state = ""
    __acceptance_states = ""

    # Funciones privadas
    def __init__(self, estados, alfabeto, mapeo, estados_iniciales, aceptacion):
        self.estados_existentes = estados
        self.alfabeto = alfabeto
        self.mapeo = mapeo
        self.estados_i = estados_iniciales
        self.aceptacion = aceptacion


        self.orden = list(self.alfabeto)

        print(self.orden)
        
        self.nuevo_nombramiento = {}
        self.letras = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        i = 0 
        for x in self.estados_existentes:
            self.nuevo_nombramiento[str(x)] = self.letras[i]
            i += 1

        self.nuevo_mapeo = {}

        for x in self.mapeo:
            temp = {}
            for y in self.mapeo[x]:
                temp[y]
            self.nuevo_mapeo[self.nuevo_nombramiento[str(x)]] = self.mapeo[x]




    def imprimir(self):
        print(self.estados_existentes)
        print(self.alfabeto)
        print(self.mapeo)
        print(self.estados_i)
        print(self.aceptacion)

    def minimizar(self):
        self.p= [[]]
        self.pila_estados = []
        self.pila_transiciones = []
        for x in self.estados_existentes:
            if x not in self.aceptacion:
                self.p[0].append(x)

        self.p.append(self.aceptacion)
        print("P = ",self.p)

        for grupo in self.p:

            self.tabla_g = {}

            for x in grupo:
                self.tabla_g[str(x)] = self.obtener_nombres_conjuntos(x,self.p)

            for x in self.tabla_g:
                for y in self.tabla_g:
                    if x != y:
                        comparando = self.comparar(self.tabla_g[x],self.tabla_g[y])



            print("tablag")
            for x in self.tabla_g:
                print(x, " ", self.tabla_g[x])

            print("P = ",self.p)

    def obtener_nombres_conjuntos(self,a,p):
        direcciones = []
        trans = self.mapeo[str(a)]


        for x in self.orden:
            for y in p:
                if trans[x] in y and str(trans[x]) != "set()":
                    cadena = "Grupo " + str(p.index(y))
                    direcciones.append(cadena)

                    break
                elif str(trans[x]) == "set()":
                    cadena = "Grupo vacio"
                    direcciones.append(cadena)

                    break
        
        return direcciones

    def comparar(self, a, b):
        if a == b:
            return True
        else:
            return False