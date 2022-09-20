class Nodo_afn:
    def __init__(self, dato, inicio, fin):
        

        self.dato = dato
        self.inicial = inicio
        self.final = fin
        self.usado = False


    def __str__(self):
        cadena="\t"+self.dato+"\t\tInicio:" +str(self.inicial)+"\t\tFin:" +str(self.final)
        return cadena