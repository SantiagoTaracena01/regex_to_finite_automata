class AFN_tran:
    def __init__(self, dato, inicio, fin):
        

        self.dato = dato
        self.inicio = inicio
        self.fin = fin



    def __str__(self):
        cadena="Estoy:" +str(self.inicio)+"\t\t"+self.dato+"\t\tPaso:" +str(self.fin)
        return cadena