
class Post(object):


    def __init__(self):
        pass

    def prioridad(self, operando, pilalast):
        valor = -1
        if operando== "." and pilalast == "|":
            valor = 1
        elif pilalast == "." and operando == "|":
            valor = 0
        elif pilalast == operando:
            valor = 0
        return valor

    def postfix(self, regex):
        # regex = "(ab(a|b)*abb)"
        regex = "("+regex

        temp = len(regex)

        for x in regex:
            if x != "#":
                regex += x+"."
            else:
                regex += x

        regex = list( regex[temp : temp*3])

        operadores = ["(",")","|","*"]

        for x in range(len(regex)):

            if (regex[x]=="." and x != 0 and x != len(regex)-1):
                if regex[x-1] not in operadores and regex[x+1] not in operadores:
                    regex[x]="."
                elif regex[x-1] =="*" and  regex[x+1] not in operadores:
                    regex[x]="."
                elif regex[x-1] ==")" and  regex[x+1] not in operadores:
                    regex[x]="."
                elif regex[x-1] not in operadores and  regex[x+1] == "(":
                    regex[x]="."
                else:
                    regex[x]=" "

            else:
                None

        regex = "".join(regex)
        regex = regex.replace(" ","")
        #regex = regex + "#"
        regex = regex + "#)"


        print("\nExpresion regular (r#): ", regex)
        postfix = ""
        pila = []

        operadores = ["(",".","|",")"]

        regex = list(regex)

        for c in regex:
            # print("caracter leido",c)
            #Operadores
            # if(c=="|" or c=="("):
            #     pila.append(c)
            # #Parentesis
            # elif(c==")"):
            #     while(pila[-1]!="("):
            #         postfix += pila.pop()
            # #Operandos
            # else:
            #     postfix += c


            if c not in operadores:
                postfix += c
                # print("operando")
                # print("pila",pila)
                # print("postfix: ", postfix,"\n")

            elif c == ")":
                # print("fin parentesis")
                while(pila[-1]!="("):
                    postfix += pila.pop()
                pila.pop()
                # print("algo", pila)
                # print("postfix: ", postfix,"\n")
            elif c == "(":
                pila += c
                # print("algo", pila)
                # print("postfix: ", postfix,"\n")  
            else:
                # print("operador")
                if len(pila)==0:
                    pila += c
                    # print("vacia",pila)
                    # print("postfix: ", postfix,"\n")
                else:
                    if self.prioridad(c, pila[-1]) == 1 or self.prioridad(c, pila[-1]) == -1:
                        pila += c
                        # print("algo", pila)
                        # print("postfix: ", postfix,"\n")
                    elif self.prioridad(c, pila[-1]) == 0 :
                        postfix += pila.pop()
                        pila += c
                        # print("algo", pila)
                        # print("postfix: ", postfix,"\n")

            
        print("\nPostfix obtenida: ", postfix)
        # print("Pila debe de ser vacia", pila)


        return postfix