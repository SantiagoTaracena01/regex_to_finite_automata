
from Nodo_afn import Nodo_afn
from AFN_transicion import AFN_tran
import graphviz

class AFN:


    ## Funciones privadas
    def __init__(self, postfijo):
        self.sentencia = list(postfijo)
        self.operadores = list("*|.")
        self.transiciones = []
        self.mapeo = {}

        self.alfabeto_e= set()


        self.__analizar(self.sentencia)



    def __encontrarhijos(self, x, analisis):
        recorrido = x - 1
        hijos = []

        while (recorrido != -1):
            if analisis[recorrido].usado == False and len(hijos) < 2:
                hijos.append(recorrido)
            recorrido -= 1
        
        return hijos

    def __analizar(self,exp):

        exp.pop()
        exp.pop()
        self.analisis = []

        for x in range (len(exp)):
             self.analisis.append(Nodo_afn(exp[x], 0, 0))


        

        #Agregar estados a todo lo que no sea operador y su transicion

        self.estados = []
        for x in self.analisis:
            if x.dato not in self.operadores:
                x.inicial = str(len(self.estados))
                x.final = str(len(self.estados) + 1)
                self.estados.append(str(len(self.estados)))
                self.estados.append(str(len(self.estados)))
                self.transiciones.append(AFN_tran(x.dato, x.inicial, x.final))
        
        #Registrar los nodos de inicio y fin de operaciones y registrar en transicion
        for x in range (len(self.analisis)):
            if self.analisis[x].dato in self.operadores:
                if self.analisis[x].dato == "*":

                    #Inicio y fin del nodo

                    self.analisis[x].inicial = str(len(self.estados))
                    self.analisis[x].final = str(len(self.estados) + 1)
                    self.estados.append(str(len(self.estados)))
                    self.estados.append(str(len(self.estados)))


                    #Registro de transiciones

                    #EL fin de su hijo se conecta con el inicio de su hijo

                    self.transiciones.append(AFN_tran("E",self.analisis[self.__encontrarhijos(x, self.analisis)[0]].final, self.analisis[self.__encontrarhijos(x, self.analisis)[0]].inicial))

                    #El inicio de Lkene se conecta con el inicio de su hijo
                    self.transiciones.append(AFN_tran("E",self.analisis[x].inicial, self.analisis[self.__encontrarhijos(x, self.analisis)[0]].inicial))
                 

                    #el fin de su hijo se conecta al fin de Kleene

                    self.transiciones.append(AFN_tran("E",self.analisis[self.__encontrarhijos(x, self.analisis)[0]].final,self.analisis[x].final))
                    
                    #El inicio de Klene se conecta con el fin de kleene

                    self.transiciones.append(AFN_tran("E",self.analisis[x].inicial,self.analisis[x].final))

                    #Marcar que ya fue visitado
                    
                    self.analisis[self.__encontrarhijos(x, self.analisis)[0]].usado = True

                elif self.analisis[x].dato == ".":

                    #Inicio y fin del nodo


                    self.analisis[x].inicial = self.analisis[self.__encontrarhijos(x, self.analisis)[1]].inicial
                    self.analisis[x].final = self.analisis[self.__encontrarhijos(x, self.analisis)[0]].final


                    #El final del hijo izquierdo se conecta al inico del hijo derecho
                   
                    self.transiciones.append(AFN_tran("E",self.analisis[self.__encontrarhijos(x, self.analisis)[1]].final,self.analisis[self.__encontrarhijos(x, self.analisis)[0]].inicial))

                    self.analisis[self.__encontrarhijos(x, self.analisis)[1]].usado = True
                    self.analisis[self.__encontrarhijos(x, self.analisis)[0]].usado = True


                elif self.analisis[x].dato == "|":

                    #Inicio y fin del nodo

                    self.analisis[x].inicial = str(len(self.estados))
                    self.analisis[x].final = str(len(self.estados) + 1)
                    self.estados.append(str(len(self.estados)))
                    self.estados.append(str(len(self.estados)))                   

                    #Registro de transiciones

                    #El inicio de or se conecta a los inicios de sus hijos
                    self.transiciones.append(AFN_tran("E",self.analisis[x].inicial, self.analisis[self.__encontrarhijos(x, self.analisis)[1]].inicial))
                    self.transiciones.append(AFN_tran("E",self.analisis[x].inicial, self.analisis[self.__encontrarhijos(x, self.analisis)[0]].inicial))

                    #Los finales de sus hijos se conectan al final de or

                    self.transiciones.append(AFN_tran("E",self.analisis[self.__encontrarhijos(x, self.analisis)[1]].final,self.analisis[x].final))
                    self.transiciones.append(AFN_tran("E",self.analisis[self.__encontrarhijos(x, self.analisis)[0]].final,self.analisis[x].final))

                    #Marcar que ya fue visitado
                    
                    self.analisis[self.__encontrarhijos(x, self.analisis)[1]].usado = True
                    self.analisis[self.__encontrarhijos(x, self.analisis)[0]].usado = True

        #Print todo
        print("Tabla estados existentes:", self.estados)

        print("\nTabla analisis")
        for x in self.analisis:
            print(x)

        print("\nTabla transiciones")
        for x in self.transiciones:
            print(x)


        #Ver posible transiciones que un estado a otro puede tener

        for x in self.sentencia:
            if x not in self.operadores and x != "#":
                self.alfabeto_e.add(x)

        self.alfabeto_e.add("E")
        self.alfabeto_e = list(self.alfabeto_e)
        print(self.alfabeto_e)

        print("\nAFN tabla resumida")
        for x in self.estados:
            self.mapeo[x] = {}
        
        for x in self.mapeo:
            for letra in self.alfabeto_e:
                self.mapeo[x][letra] = []
        
        for x in self.mapeo:
            for letra in self.alfabeto_e:
                for tran in self.transiciones:
                    if x == tran.inicio and tran.dato == letra:
                        self.mapeo[x][letra].append(tran.fin)

        for x in self.mapeo:
            print(x, "", self.mapeo[x])
        
        #Graficas       
        f= graphviz.Digraph(name="AFN")
        f.attr(rankdir='LR')


        self.aceptacion = []

        self.aceptacion.append(self.analisis[-1].final)

        for x in self.mapeo:
            if x == self.aceptacion[0]:
                f.node(str(x), shape = "doublecircle")
            else:
                f.node(str(x), shape = "circle")


        for x in self.mapeo:
            for y in self.mapeo[x]:
                    if len(self.mapeo[x][y]) != 0:
                        for w in self.mapeo[x][y]:
                            f.edge(x,w, label = y, arrowhead='vee')


        f.node("", height = "0",width = "0", shape = "box")
        # f.edge("",str(0), arrowhead='vee', )
        f.render("AFN", view = "True")
