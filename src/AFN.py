
from Nodo_afn import Nodo_afn
from AFN_transicion import AFN_tran
import graphviz

class AFN:


    ## Funciones privadas
    def __init__(self, postfijo):

        #Variables de escritura
        self.estados = []
        self.mapeo = {}
        self.alfabeto_e= set()
        self.inicio = ""
        self.aceptacion = []

        #Variables de ambiente
        self.sentencia = list(postfijo)
        self.operadores = list("*|.")
        self.transiciones = []


        self.__analizar(self.sentencia)

        
        ##Escribir AFN en archivo de texto
        archivo = open("AFN.txt","w")

        ##Estados existentes
        archivo.write("ESTADOS = {")
        for x in range(len(self.estados)):
            if x != len(self.estados) -1:
                archivo.write(str(self.estados[x]))
                archivo.write(" ,")
            else:
                archivo.write(str(self.estados[x]))
        archivo.write("}\n")

        ##Simbolos
        archivo.write("SIMBOLOS = ")
        self.alfabeto_e.pop(self.alfabeto_e.index("E"))
        archivo.write(str(self.alfabeto_e))
        archivo.write("\n")

        ##Inicio
        archivo.write("INICIO = {")
        archivo.write(str(self.inicio))
        archivo.write("}\n")

        ##Aceptacion
        archivo.write("ACEPTACION = {")
        for x in range(len(self.aceptacion)):
            if x != len(self.aceptacion) -1 :
                archivo.write(str(self.aceptacion[x]))
                archivo.write(" ,")
            else:
                archivo.write(str(self.aceptacion[x]))

        archivo.write("}\n")

        ## print(self.mapeo)
        ## ####Transiciones
        archivo.write("TRANSICIONES = ")
        i = 0
        for x in self.transiciones:
            archivo.write(" (")
            archivo.write(str(x.inicio))
            archivo.write(", ")
            archivo.write(str(x.dato))
            archivo.write(", ")
            archivo.write(str(x.fin))
            i += 1
            if i == len(self.transiciones):
                archivo.write(")")
            else:
                archivo.write(") -")
        ## archivo.write("\n")
        archivo.close()


    # def simular_afn(self, oracion):
    def pasar_info(self):
        self.informacition_afn = []
        self.informacition_afn.append(self.estados)
        self.informacition_afn.append(self.alfabeto_e)
        self.informacition_afn.append(self.mapeo)
        self.informacition_afn.append(self.inicio)
        self.informacition_afn.append(self.aceptacion)

        return self.informacition_afn

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
        # print("Tabla estados existentes:", self.estados)

        # print("\nTabla analisis")
        # for x in self.analisis:
        #     print(x)

        # print("\nTabla transiciones")
        # for x in self.transiciones:
        #     print(x)


        #Ver posible transiciones que un estado a otro puede tener

        for x in self.sentencia:
            if x not in self.operadores and x != "#":
                self.alfabeto_e.add(x)

        self.alfabeto_e.add("E")
        self.alfabeto_e = list(self.alfabeto_e)
        # print(self.alfabeto_e)

        # print("\nAFN tabla resumida")
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
                        
        print("\n-------------------Tabla de transiciones AFN--------------------\n")
        for x in self.mapeo:
            print(x, "", self.mapeo[x])

        self.aceptacion.append(self.analisis[-1].final)
        self.inicio = self.analisis[-1].inicial
        
        #Graficas       
        # f= graphviz.Digraph(name="AFN")
        # f.attr(rankdir='LR')





        # for x in self.mapeo:
        #     if x == self.aceptacion[0]:
        #         f.node(str(x), shape = "doublecircle")
        #     else:
        #         f.node(str(x), shape = "circle")


        # for x in self.mapeo:
        #     for y in self.mapeo[x]:
        #             if len(self.mapeo[x][y]) != 0:
        #                 for w in self.mapeo[x][y]:
        #                     f.edge(x,w, label = y, arrowhead='vee')


        # f.node("", height = "0",width = "0", shape = "box")
        # f.render("AFN", view = "True")
