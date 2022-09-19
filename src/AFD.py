
from Nodo import Nodo
from Fila_Transiciones import Fila
# import graphviz

class AFD:
    __states = {}
    __alphabet = {}
    __mapping = {}
    __initial_state = ""
    __acceptance_states = ""

    ## Funciones privadas
    def __init__(self, postfijo):

        ##Variables a escribir AFD directo txt 
        self.estados_AFD = []
        self.alfabeto = set()
        self.mapeo = {}
        self.estado_inicial_AFD = []
        self.aceptacion = []

        ##Analisis
        self.analisis = list(postfijo)
        self.operadores = list("*|.")

        self.arbol = []
        self.tabla_followpost = []
        self.tabla_transiciones_AFD = []

        for x in self.analisis:
            if x not in self.operadores and x != "##":
                self.alfabeto.add(x)

        ##Construccion del AFD
        self.__analizar(self.analisis)

        ##Llenar variables AFD para escribir
            ##Estados
        for x in self.tabla_transiciones_AFD:
            self.estados_AFD.append(x.conjunto) 
            ##alfbeto se realiza antes
            ##mapeo
        for x in self.tabla_transiciones_AFD:
            self.mapeo[str(x.conjunto)] = x.transiciones
        
            ##Estados iniciales
        self.estado_inicial_AFD.append(self.arbol[-1].firstpost)

            ##Aceptacion se realiza con analizar

        ##Escribir AFD en archivo de texto
        archivo = open("AFD_directo.txt","w")

        ##Estados existentes
        archivo.write("ESTADOS = {")
        for x in range(len(self.estados_AFD)):
            if x != len(self.estados_AFD) -1:
                archivo.write(str(self.estados_AFD[x]))
                archivo.write(" ,")
            else:
                archivo.write(str(self.estados_AFD[x]))
        archivo.write("}\n")

        ##Simbolos
        archivo.write("SIMBOLOS = ")
        archivo.write(str(self.alfabeto))
        archivo.write("\n")

        ##Inicio
        archivo.write("INICIO = {")
        archivo.write(str(self.estado_inicial_AFD[0]))
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
        ## ##Transiciones
        archivo.write("TRANSICIONES = ")
        for estoy in self.mapeo:
            i = 0
            for va in self.mapeo[estoy]:
                archivo.write(" (")
                archivo.write(str(estoy))
                archivo.write(", ")
                archivo.write(str(va))
                archivo.write(", ")
                archivo.write(str(self.mapeo[estoy][va]))
                i += 1
                if i == len(self.mapeo[estoy]):
                    archivo.write(")")
                else:
                    archivo.write(") -")
        ## archivo.write("\n")
        archivo.close()

        ## print("\n-------------------Tabla de aarbol--------------------\n")

        ## for x in self.arbol:
        ##     print(x)

        ## print("\n-------------------Tabla de followpost--------------------\n")

        ## for x in self.tabla_followpost:
        ##     impresion = "\tID: "+ str(x.id) + "\tsimbolo: "+x.dato +"\tFollowpost: " +str(x.followpost)
        ##     print(impresion)
    
    def simulation_afd(self,oracion):
        print("\nCadena a evaluar (w): ", oracion)
        self.recorrido = []
        self.recorrido.append(self.arbol[-1].firstpost)

        self.sentencia = list(oracion)

        Aceptada_Alf = True
        Valida = False

        for x in self.sentencia:
            if x not in self.alfabeto:
                Aceptada_Alf = False

        if Aceptada_Alf == True:
            for x in self.sentencia:

                self.recorrido.append(self.__mover(self.recorrido[-1], x))

            
            if "Nada" not in self.recorrido and self.recorrido[-1] in self.aceptacion:
                Valida = True
            else:
                Valida = False
        respuesta = ""
        if Valida == False:
            respuesta = "NO"
        elif Valida == True:
            respuesta = "SI"
            print("\nTransiciones realizadas durante validacion: ",str(self.recorrido),"\n")
        print("\n¿La cadena: ",oracion, " pertenece a L(r)\n")
        return respuesta

    def __mover(self, estado, transition):
        self.valid_transaction = False
        for y in self.tabla_transiciones_AFD:
            if estado == y.conjunto:
                self.valid_transaction =  y.transiciones[transition]


        return self.valid_transaction 

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

        ##firstpost, lastpost y anulable de hojas de caracteres
        nodo = 1
        for x in self.arbol:
            if x.dato not in self.operadores:
                x.firstpost.add(nodo)
                x.lastpost.add(nodo)
                x.anulable = False


                self.tabla_followpost.append(Nodo(x.dato, nodo))

                nodo += 1
        
        ##anulable de operaciones

        for x in range (len(self.arbol)):
            if self.arbol[x].dato in self.operadores:
                if self.arbol[x].dato == "*":
                    self.arbol[x].anulable = True
                elif self.arbol[x].dato == ".":
                    self.arbol[x].anulable = self.arbol[x-1].anulable and self.arbol[x-2].anulable
                elif self.arbol[x].dato == "|":
                    self.arbol[x].anulable = self.arbol[x-1].anulable or self.arbol[x-2].anulable

        ##firstpost de operaciones
                

        for x in range (len(self.arbol)):
            if self.arbol[x].dato in self.operadores:
                ##si es un | se realiza UNION
                if self.arbol[x].dato == "|":
                    self.arbol[x].firstpost = self.arbol[self.__encontrarhijos(x, self.arbol)[1]].firstpost  | self.arbol[self.__encontrarhijos(x, self.arbol)[0]].firstpost 

                    self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
                ##si es un . 
                elif self.arbol[x].dato == ".":
                    if self.arbol[self.__encontrarhijos(x, self.arbol)[1]].anulable == True:
                        self.arbol[x].firstpost = self.arbol[self.__encontrarhijos(x, self.arbol)[1]].firstpost  | self.arbol[self.__encontrarhijos(x, self.arbol)[0]].firstpost 

                        self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
                        self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
                    else:
                        self.arbol[x].firstpost = self.arbol[self.__encontrarhijos(x, self.arbol)[1]].firstpost
                        self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
            
                ##Si es un *
                elif self.arbol[x].dato == "*":
                    self.arbol[x].firstpost = self.arbol[self.__encontrarhijos(x, self.arbol)[0]].firstpost

                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True


            ##limpiar usados

        for x in self.arbol:
            x.usado = False

            ##lastpost de operaciones

        for x in range (len(self.arbol)):
            if self.arbol[x].dato in self.operadores:
                ##si es un | se realiza UNION
                if self.arbol[x].dato == "|":
                    self.arbol[x].lastpost = self.arbol[self.__encontrarhijos(x, self.arbol)[1]].lastpost  | self.arbol[self.__encontrarhijos(x, self.arbol)[0]].lastpost 

                    self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
                ##si es un . 
                elif self.arbol[x].dato == ".":
                    if self.arbol[self.__encontrarhijos(x, self.arbol)[0]].anulable == True:
                        self.arbol[x].lastpost = self.arbol[self.__encontrarhijos(x, self.arbol)[1]].lastpost  | self.arbol[self.__encontrarhijos(x, self.arbol)[0]].lastpost 

                        self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
                        self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
                    else:
                        self.arbol[x].lastpost = self.arbol[self.__encontrarhijos(x, self.arbol)[0]].lastpost
                        self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
            
                ##Si es un *
                elif self.arbol[x].dato == "*":
                    self.arbol[x].lastpost = self.arbol[self.__encontrarhijos(x, self.arbol)[0]].lastpost

                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
        ##limpiar usados

        for x in self.arbol:
            x.usado = False


        ##Recoleccion de followpost
        for x in range (len(self.arbol)):
            if self.arbol[x].dato in self.operadores:
                ##si es un | se realiza UNION
                if self.arbol[x].dato == "|":

                    self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True
                ##si es un . 
                elif self.arbol[x].dato == ".":
                    A = self.arbol[self.__encontrarhijos(x, self.arbol)[1]].lastpost
                    B = self.arbol[self.__encontrarhijos(x, self.arbol)[0]].firstpost
                    

                    self.arbol[self.__encontrarhijos(x, self.arbol)[1]].usado = True
                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True

                    for x in self.tabla_followpost:
                        if x.id in A:
                            x.followpost = x.followpost | B
                ##Si es un *
                elif self.arbol[x].dato == "*":
                    A = self.arbol[self.__encontrarhijos(x, self.arbol)[0]].lastpost
                    B = self.arbol[self.__encontrarhijos(x, self.arbol)[0]].firstpost

                    self.arbol[self.__encontrarhijos(x, self.arbol)[0]].usado = True

                    for x in self.tabla_followpost:
                        if x.id in A:
                            x.followpost = x.followpost | B


        ##Tabla de transiciones AFD


        self.tabla_transiciones_AFD.append(Fila([self.arbol[-1].firstpost], self.arbol[-1].firstpost, self.tabla_followpost, self.alfabeto))

        
        ## for x in range (len(self.tabla_transiciones_AFD)):
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


        ##Impresion AFD
        print("\n-------------------AFD (Tabla de Transacciones) --------------------\n")
        for x in self.tabla_transiciones_AFD:
            print(x)
        print("\n")

        ##Estados de aceptacion
        for x in self.tabla_transiciones_AFD:
            if self.tabla_followpost[-1].id in x.conjunto:
                self.aceptacion.append(x.conjunto)
                
        ##Graficas       
        # f= graphviz.Digraph(name="AFD_directo")
        # f.attr(rankdir='LR')


        # for x in self.tabla_transiciones_AFD:
        #     if x.conjunto in self.aceptacion:
        #         f.node(str(x.conjunto), shape = "doublecircle")
        #     else:
        #         f.node(str(x.conjunto), shape = "circle")


        # for x in self.tabla_transiciones_AFD:
        #     for y in x.transiciones:
        #         if str(x.transiciones[y]) != "set()":
        #             f.edge(str(x.conjunto),str(x.transiciones[y]), label = y, arrowhead='vee')
        # f.node("", height = "0",width = "0", shape = "box")
        # f.edge("",str(self.tabla_transiciones_AFD[0].conjunto), arrowhead='vee', )
        # f.render("AFD_directo", view = "True")

        # return self.tabla_transiciones_AFD

                