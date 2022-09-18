# Clases y archivos importantes.
from stack import Stack

# Constantes importantes para el archivo.
OPERATORS = ("*", ".", "+")
OPERATORS_AND_PARENTHESIS = ("(", ")", "*", ".", "+")
OPERATOR_PRECEDENCE = { "*": 3, ".": 2, "+": 1, "(": 0, ")": 0, "": 0 }
IMPOSSIBLY_HIGH_PRECEDENCE = 99

# Funciones lambda.
get_regex_operands = lambda regex: [char for char in regex if (char not in OPERATORS)]

# Función que simplifica una expresión regular a su mínima expresión.
def simplify_regex(regex):
  
  # Expresión regular simplificada inicial.
  simplified_regex = ""
  
  # Recorrido de la expresión del final al inicio.
  for i in reversed(range(1, len(regex))):
    
    # Si hay dos operadores kleene seguidos, la expresión se simplifica.
    if ((regex[i] == "*") and (regex[i - 1] == "*")):
      pass
    else:
      simplified_regex += regex[i]
  
  # Retorno de la expresión regular simplificada.
  return (regex[0] + simplified_regex[::-1])

# Función que agrega símbolos de concatenación explícitos a la expresión regular.
def check_concatenations(regex):

  # Expresión regular finalizada.
  output = ""

  # Iteración sobre el índice y caracter de una expresión regular.
  for index, char in enumerate(regex):

    # Cualquier caracter se agrega a la expresión regular convertida.
    output += char

    # Lectura de caracteres y su letra siguiente.
    try:

      # Los caracteres +, ( y . nunca llevarán una concatenación después de ellos.
      if ((char == "+") or (char == "(") or (char == ".")):
        continue

      # Condiciones para llevar una concatenación luego del caracter analizado.
      elif (((char == ")") or (char == "*") or (char not in OPERATORS_AND_PARENTHESIS)) and (regex[index + 1] not in ("*", "+", ")"))):
        output += "."

    # Si ocurre un error buscando el siguiente caracter, el proceso finaliza.
    except:
      pass

  # Retorno de la expresión regular convertida.
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

      # Si el stack aún está vacío, o hay un paréntesis izquierdo en el stack, se guarda el operador.
      if ((operator_stack.is_empty()) or (operator_stack.peek() == "(")):
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

        # Al finalizar, el operador actual se agrega al stack.
        operator_stack.push(char)

    # Si el caracter es un operando, agregar a la expresión postfix.
    else:
      postfix += char

  # Si el stack aún no está vacío, todos los demás operadores se agregan a la expresión.
  while (not operator_stack.is_empty()):
    postfix += operator_stack.pop()

  # Retorno de la expresión postfix.
  return postfix

# Función que verifica si un mapeo tiene transiciones con epsilon y retorna su cuenta.
def check_epsilon_transitions(mapping):

  # Transiciones del mapeo.  
  transitions = []

  # Obtención de todos los símbolos de transición del mapeo.
  for key in mapping:
    for state in mapping[key]:
      transitions.append(state)

  # Retorno de la cuenta de las transiciones con epsilon.
  return transitions.count("E")
