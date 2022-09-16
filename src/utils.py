from ast import operator
from tabnanny import check
from stack import Stack

OPERATORS = ("*", ".", "+")
OPERATORS_AND_PARENTHESIS = ("(", ")", "*", ".", "+")
OPERATOR_PRECEDENCE = { "*": 3, ".": 2, "+": 1, "(": 0, ")": 0, "": 0 }
IMPOSSIBLY_HIGH_PRECEDENCE = 99

def simplify_regex(regex):
  simplified_regex = ""
  for i in reversed(range(1, len(regex))):
    if ((regex[i] == "*") and (regex[i - 1] == "*")):
      pass
    else:
      simplified_regex += regex[i]
  return (regex[0] + simplified_regex[::-1])

def check_concatenations(regex):
  output = ""
  for index, char in enumerate(regex):
    output += char
    try:
      if ((char == "+") or (char == "(")):
        continue
      elif (((char == ")") or (char == "*") or (char not in OPERATORS_AND_PARENTHESIS)) and (regex[index + 1] not in ("*", "+", ")"))):
        output += "."
    except:
      pass
  return output

# Función que convierte una expresión regular de infix a postfix.
def regex_infix_to_postfix(regex):
  
  # Conversión a una expresión con concatenaciones explícitas.
  regex = check_concatenations(regex)
  
  # Expresión postfix y stack de operaciones.
  postfix = ""
  operator_stack = Stack()
  
  # Análisis de cada caracter de la expresión regular.
  for char in regex:
    
    # Si el caracter es un paréntesis izquierdo, se agrega al stack.
    if (char == "("):
      operator_stack.push(char)
    
    # Si el caracter es un paréntesis derecho, se busca su par izquierdo.
    elif (char == ")"):
      while (operator_stack.peek() != "("):
        postfix += operator_stack.pop()
      operator_stack.pop()
    
    # Si el caracter es un operador en el conjunto {*, ., +}.
    elif (char in OPERATORS):
      
      # Si el stack aún está vacío, el operador se guarda en el stack.
      if (operator_stack.is_empty()):
        operator_stack.push(char)
      
      # El caracter se agrega a la expresión si hay un paréntesis izquierdo en el stack.
      elif (operator_stack.peek() == "("):
        operator_stack.push(char)
      
      # Para cualquier otro caso, se verifica la precedencia del operador.      
      else:

        # Precedencia del operador actual y anterior.
        actual_precedence = OPERATOR_PRECEDENCE[char]
        last_precedence = IMPOSSIBLY_HIGH_PRECEDENCE

        # Mientras el operador actual tenga menor precedencia o el stack no esté vacío.
        while (last_precedence >= actual_precedence):

          # Si el stack está vacío, el ciclo debe detenerse.
          if (operator_stack.is_empty()):
            break

          # El operador con mayor precedencia se agrega a la expresión postfix.
          postfix += (operator_stack.pop() if (last_precedence != IMPOSSIBLY_HIGH_PRECEDENCE) else "")
          last_operator = operator_stack.peek()
          last_precedence = OPERATOR_PRECEDENCE[last_operator]

        operator_stack.push(char)
    
    # Si el caracter es un operando, agregar a la expresión postfix.
    else:
      postfix += char
  
  # Si el stack aún no está vacío, todos los demás operadores se agregan a la expresión.
  while (not operator_stack.is_empty()):
    postfix += operator_stack.pop()

  return postfix

print(regex_infix_to_postfix("abb((a+b)+b)a*b")) # ESPERADO: aab+*.b.
