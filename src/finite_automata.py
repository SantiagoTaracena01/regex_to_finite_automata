from set import PersonalSet

EPSILON = "E"

class NFA(object):

  __states = PersonalSet([])
  __alphabet = PersonalSet([])
  __mapping = {}
  __initial_state = None
  __acceptance_states = PersonalSet([])

  # Método constructor del AFN.
  def __init__(self, regex):
    
    # Creación del estado inicial.
    created_state = 0
    self.__initial_state = created_state
    
    # Ciclo for que itera la expresión regular a convertir.
    for index, char in enumerate(regex):
      
      # Si el caracter de la expresión regular es un *, creamos un barco.
      if (char == "*"):
        created_state = self.__ship(regex, index, created_state)
      
      # Para cualquier caracter del alfabeto, hacemos el proceso siguiente.
      else:
        
        # Si el caracter aún no está en el alfabeto, este se agrega al mismo.
        if (char not in self.__alphabet.get_content()):
          self.__alphabet.add(char)
        
        
        if (regex[index - 1] == "*"):
          self.__states.add(created_state)
        try:
          next_char = regex[index + 1]
          if ((next_char != "*") and (next_char != "+") and (next_char != "(") and (next_char != ")")):
            self.__mapping[created_state] = { regex[index + 1]: [(created_state + 1)] }
          else:
            self.__mapping[created_state] = { EPSILON: [(created_state + 1)] }
        except:
          self.__mapping[created_state] = {}
        created_state += 1
    
    # Búsqueda y creación del estado de aceptación del AFN.
    for key in self.__mapping:
      if (self.__mapping[key] == {}):
        self.__acceptance_states.add(key)

  def __ship(self, regex, index, state):
    for i in range(4):
      self.__states.add(state)
      if (i == 0):
        self.__mapping[state] = { EPSILON: [(state + 1), (state + 3)], }
      elif (i == 1):
        self.__mapping[state] = { regex[index - 1]: [(state + 1)] }
      elif (i == 2):
        self.__mapping[state] = { EPSILON: [(state - 1), (state + 1)] }
      else:
        try:
          next_char = regex[index + 1]
          try:
            second_next_char = regex[index + 2]
            if (second_next_char == "*"):
              self.__mapping[state] = { EPSILON: [(state + 1)] }
              break
          except:
            self.__mapping[state] = { next_char: [(state + 1)] }
        except: 
          self.__mapping[state] = {}
      state += 1
    return state

  def __str__(self):
    return f"States: {self.__states}\nInitial State: {self.__initial_state}\nAcceptance States: {self.__acceptance_states}\nAlphabet: {self.__alphabet}\nMapping: {self.__mapping}\n"

class DFA(object):

  def __init__(self, regex):
    for char in regex:
      print(char)

"""
nfa = NFA(
  states=Set(["0", "1", ..., "n"]),
  alphabet=Set(["a", "b"]),
  mapping={
    "0": { "a": "1", "b": "2" },
    "1": { "a": "2", "b": "3" },
    ...
  }
  initial_state="0",
  final_states=Set(["n"])
)
"""
