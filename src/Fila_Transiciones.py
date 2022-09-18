
from hmac import trans_36


class Fila:
    def __init__(self, estados_existentes, followpost, tabla_f, alfabeto):
        # "dato" puede ser de cualquier tipo, incluso un objeto si se sobrescriben los operadores de comparación
        
        self.conjunto = followpost
        self.transiciones   = {}

        self.alf = alfabeto

        self.trabajo = tabla_f
        self.new_estates = []
        self.info = []
        self.ex = estados_existentes
    
        for x in self.alf:
            self.transiciones[x] = set()

        for x in self.conjunto:
            for y in self.trabajo:
                if x == y.id:
                    self.info.append(y)


        for x in self.alf:
            for y in self.info:
                if x == y.dato:
                    self.transiciones[x] = self.transiciones[x] | y.followpost


        
        

        # for x in self.info:
        #     impresion = "\tID: "+ str(x.id) + "\tsimbolo: "+x.dato +"\tFollowpost: " +str(x.followpost)
        #     print(impresion)


        for x in self.transiciones:
            if self.transiciones[x] not in self.ex and str(self.transiciones[x]) != "set()":
                self.new_estates.append(self.transiciones[x]) 


    def __str__(self):
        #+ "\tnuevos estados: "+str(self.new_estates)
        #"estados existentes" +str(self.ex) + 
        cadena="\t" + str(self.conjunto) +"\t" +"\t" + str(self.transiciones)
        return cadena