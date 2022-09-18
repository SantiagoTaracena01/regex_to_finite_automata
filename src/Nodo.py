
class Nodo:
    def __init__(self, dato, id):
        # "dato" puede ser de cualquier tipo, incluso un objeto si se sobrescriben los operadores de comparación
        
        self.id = id
        self.dato = dato
        self.anulable = None
        self.usado = False
        self.firstpost = set([])
        self.lastpost = set([])
        self.followpost = set([])

    def __str__(self):
        cadena="\t"+self.dato+"\t\tAnulable:" +str(self.anulable)+"\t\tFirstopsot:" +str(self.firstpost)+"\t\tLastopsot:" +str(self.lastpost) 
        return cadena