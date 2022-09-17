from Nodo import Nodo
from Fila_Transiciones import Fila
import networkx as nx
import matplotlib.pyplot as plt

class Arbol2:
    # Funciones privadas
    def __init__(self, postfijo):
        self.analisis = list(postfijo)
        self.operadores = list("*|.")

        self.arbol = []
        self.tabla_followpost = []
        self.tabla_transiciones_AFD = []
        self.alfabeto = set()
        for x in self.analisis:
            if x not in self.operadores and x != "#":
                self.alfabeto.add(x)

        self.__analizar(self.analisis)



        # print("\n-------------------Tabla de aarbol--------------------\n")

        # for x in self.arbol:
        #     print(x)

        # print("\n-------------------Tabla de followpost--------------------\n")

        # for x in self.tabla_followpost:
        #     impresion = "\tID: "+ str(x.id) + "\tsimbolo: "+x.dato +"\tFollowpost: " +str(x.followpost)
        #     print(impresion)

    def __encontrarhijos(self, x, arbol):
        recorrido = x - 1
        hijos = []

        while (recorrido != -1):
            if arbol[recorrido].usado == False and len(hijos) < 2:
                hijos.append(recorrido)
            recorrido -= 1
        
        return hijos

    def __analizar(self,exp):
        for x in range(len(exp)):
            self.arbol.append(Nodo(exp[x], 0))

        #firstpost, lastpost y anulable de hojas de caracteres
        nodo = 1
        for x in self.arbol:
            if x.dato not in self.operadores:
                x.firstpost.add(nodo)
                x.lastpost.add(nodo)
                x.anulable = False


                self.tabla_followpost.append(Nodo(x.dato, nodo))

                nodo += 1
        
        #anulable de operaciones

        for x in range (len(self.arbol)):
            if self.arbol[x].dato in self.operadores:
                if self.arbol[x].dato == "*":
                    self.arbol[x].anulable = True
                elif self.arbol[x].dato == ".":
                    self.arbol[x].anulable = self.arbol[x-1].anulable and self.arbol[x-2].anulable
                elif self.arbol[x].dato == "|":
                    self.arbol[x].anulable = self.arbol[x-1].anulable or self.arbol[x-2].anulable

        #firstpost de operaciones
                

        for x in range (len(self.arbol)):
            if self.arbol[x].dato in self.operadores:
                #si es un | se realiza UNION
                if self.arbol[x].dato == "|":
                    self.arbol[x].firstpost = self.arbol[self.__encontrarhijos(x, self.arbol)[1]].firstpost  | self.arbol[self.__encontrarhijos(x, self.arbol)[0]].firstpost 

                    self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
                #si es un . 
                elif self.arbol[x].dato == ".":
                    if self.arbol[self.__encontrarhijos(x, self.arbol)[1]].anulable == True:
                        self.arbol[x].firstpost = self.arbol[self.__encontrarhijos(x, self.arbol)[1]].firstpost  | self.arbol[self.__encontrarhijos(x, self.arbol)[0]].firstpost 

                        self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
                        self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
                    else:
                        self.arbol[x].firstpost = self.arbol[self.__encontrarhijos(x, self.arbol)[1]].firstpost
                        self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
            
                #Si es un *
                elif self.arbol[x].dato == "*":
                    self.arbol[x].firstpost = self.arbol[self.__encontrarhijos(x, self.arbol)[0]].firstpost

                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True


            #limpiar usados

        for x in self.arbol:
            x.usado = False

            #lastpost de operaciones

        for x in range (len(self.arbol)):
            if self.arbol[x].dato in self.operadores:
                #si es un | se realiza UNION
                if self.arbol[x].dato == "|":
                    self.arbol[x].lastpost = self.arbol[self.__encontrarhijos(x, self.arbol)[1]].lastpost  | self.arbol[self.__encontrarhijos(x, self.arbol)[0]].lastpost 

                    self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
                #si es un . 
                elif self.arbol[x].dato == ".":
                    if self.arbol[self.__encontrarhijos(x, self.arbol)[0]].anulable == True:
                        self.arbol[x].lastpost = self.arbol[self.__encontrarhijos(x, self.arbol)[1]].lastpost  | self.arbol[self.__encontrarhijos(x, self.arbol)[0]].lastpost 

                        self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
                        self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
                    else:
                        self.arbol[x].lastpost = self.arbol[self.__encontrarhijos(x, self.arbol)[0]].lastpost
                        self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
            
                #Si es un *
                elif self.arbol[x].dato == "*":
                    self.arbol[x].lastpost = self.arbol[self.__encontrarhijos(x, self.arbol)[0]].lastpost

                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
        #limpiar usados

        for x in self.arbol:
            x.usado = False


        #Recoleccion de followpost
        for x in range (len(self.arbol)):
            if self.arbol[x].dato in self.operadores:
                #si es un | se realiza UNION
                if self.arbol[x].dato == "|":

                    self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
                #si es un . 
                elif self.arbol[x].dato == ".":
                    A = self.arbol[self.__encontrarhijos(x, self.arbol)[1]].lastpost
                    B = self.arbol[self.__encontrarhijos(x, self.arbol)[0]].firstpost
                    

                    self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True

                    for x in self.tabla_followpost:
                        if x.id in A:
                            x.followpost = x.followpost | B
                #Si es un *
                elif self.arbol[x].dato == "*":
                    A = self.arbol[self.__encontrarhijos(x, self.arbol)[0]].lastpost
                    B = self.arbol[self.__encontrarhijos(x, self.arbol)[0]].firstpost

                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True

                    for x in self.tabla_followpost:
                        if x.id in A:
                            x.followpost = x.followpost | B


        #Tabla de transiciones AFD

        print("\n-------------------Tabla de Transacciones--------------------\n")
        self.tabla_transiciones_AFD.append(Fila([self.arbol[-1].firstpost], self.arbol[-1].firstpost, self.tabla_followpost, self.alfabeto))

        
        # for x in range (len(self.tabla_transiciones_AFD)):
        self.verificador = False
        estados_existentes = []
        while self.verificador == False:
            if len(self.tabla_transiciones_AFD[-1].new_estates) != 0 :
                for y in self.tabla_transiciones_AFD[-1].new_estates:
                        if str(y) != "set()":
                            estados_existentes.append(self.tabla_transiciones_AFD[-1].conjunto )
                            for x in self.tabla_transiciones_AFD[-1].new_estates:
                                estados_existentes.append(x)
                            self.tabla_transiciones_AFD.append(Fila(estados_existentes, y, self.tabla_followpost, self.alfabeto)) 
            else:
                self.verificador = True
        for x in self.tabla_transiciones_AFD:
            print(x)

        #Graficas


        # self.g = nx.DiGraph()

        # for x in self.tabla_transiciones_AFD:
        #     for y in x.transiciones:
        #         i = 1
        #         for w in self.alfabeto:
        #             if str(x.transiciones[w]) != "set()":
        #                 self.g.add_weighted_edges_from([(str(x.conjunto),str(x.transiciones[w]), i)])
        #             i +=1
        # self.pos = nx.spring_layout(self.g)
        # nx.draw_networkx_nodes(self.g,self.pos, node_size=500 )
        # nx.draw_networkx_edges(self.g, self.pos, edgelist = self.g.edges(), edge_color = 'black')
        # nx.draw_networkx_labels(self.g, self.pos)
        # weight = nx.get_edge_attributes(self.g, 'weight')
        # nx.draw_networkx_edge_labels(self.g, self.pos, edge_labels=weight)
        # plt.show()

        return self.tabla_transiciones_AFD

                