from sre_parse import State
from set import PersonalSet

EPSILON: str = "E"

class NFA(object):

  __states = PersonalSet([])
  __alphabet = PersonalSet([])
  __mapping = {}
  __initial_state = None
  __acceptance_states = PersonalSet([])

  def __init__(self, regex):
    created_states = 0
    for index, char in enumerate(regex):
      print(index, char)
      if (char == "*"):
        for i in range(4):
          self.__states.add(created_states)
          if (i == 0):
            self.__mapping.add({
              created_states: {
                EPSILON: [(created_states + 1), (created_states + 3)]
              }
            })
          elif (i == 1):
            self.__mapping.add({
              created_states: {
                regex[index - 1]: [(created_states + 1)]
              }
            })
          elif (i == 2):
            self.__mapping.add({
              created_states: {
                EPSILON: [(created_states - 2), (created_states + 1)]
              }
            })
          elif (i == 3):
            self.__mapping.add({
              created_states: {
                0: None
              }
            })
          created_states += 1
      else:
        if (char not in self.__alphabet):
          self.__alphabet.add(char)
    self.__initial_state = self.__states[0]
    self.__acceptance_states = self.__states[-1]
  
  # Override para meter un afn directamente
  def __init__(self, states, alphabet, mapping, initial_state, final_states):
    self.__states = states
    self.__alphabet = alphabet
    self.__mapping = mapping
    self.__initial_state = initial_state
    self.__acceptance_states = final_states

  def __str__(self):
    return f"""
      States: {self.__states}
      Alphabet: {self.__alphabet}
      Mapping: {self.__mapping}
      Initial State: {self.__initial_state}
      Acceptance States: {self.__acceptance_states}
    """

  # Codigo dedicado a pasar a AFD
  def e_closure(self, states):
    #Añadir los estados a los que cada estado se mueve con EPSILON
    stacky = [*states]

    result = [*states]

    while(len(stacky) != 0):
      t = stacky.pop()
      reachable_states = self.__mapping.get(t).get("EPSILON")

      for state in reachable_states:
        if state not in result:
          result.append(state)
          stacky.append(state)

    return PersonalSet(result)
  
  def move(self, states, symbol):
    #Añadir los estados a los que cada estado se mueve con el simbolo
    stacky = [*states]

    result = []

    while(len(stacky) != 0):
      t = stacky.pop()
      reachable_states = self.__mapping.get(t).get(symbol)

      for state in reachable_states:
        if state not in result:
          result.append(state)

    return PersonalSet(result)
  
  def to_dfa(self):

    # Diccionario de estados de este dfa
    dfa_states = {}

  

    # Pïla de estados, para compararlos entre ellos
    # elementos que deberia admitir: Personalsets
    dfa_states_set = []

    # Iniciar obteniendo el conjunto del estado inicial, su e-closure
    A = self.e_closure([self.__initial_state])
    dfa_states_set.append(A)

    # Añadir el estado al diccionario con su respectivo indice
    i = 0
    dfa_states[i] = A

    # a partir de aca, se trata de hacer moves y añadir al stack los conjuntos
    # nuevos que son nuevos generados por e-closure
    # y descartar los que ya existen
    
    for state in dfa_states_set:
      #Hacer moves, con los simbolos del alfabeto
      for symbol in self.__alphabet.get_content():
        
        # Cambiar el indice del estado
        # Hacerlo aca, ya que este for es el que tiene
        # el verificador de estados
        i += 1


        # Realizar el move del estado
        # Y luego un e-closure de este
        movement = self.move(state.get_content(), symbol)
        new_state = self.e_closure(movement.get_content())

        #Si el estaado ya se encuentra en la pila, descartarlo
        #De lo contrario, agregarlo
        verifier = 0
        
        for j in range(len(dfa_states_set)):
          # Si se encuentra un estado al que es igual, sumar uno al verificador
          if dfa_states_set[j] == new_state:
            verifier += 1
        # Si el verificador no se activo, agregarlo al stack
        if verifier < 1:
          
          dfa_states_set.append(new_state)
          dfa_states[i] = new_state

    # Ahora solo toca encontrar a que estado se mueve cada quie
    # Crear una lista para almacenar los estados por conjunto
    # Se usara para comparar ya signar las transiciones
    set_states = []

    # ESte array guardara las transiciones
    transitions = []

    for value in list(dfa_states.values()):
      set_states.append(value.get_content())

    for current_state in dfa_states:
      # REvisar por cada simbolo del alfabeto

      for symbol in self.__alphabet.get_content():
        # Realizar el move del estado
        # Y luego un e-closure de este
        movement = self.move(dfa_states[current_state].get_content(), symbol)
        new_state = self.e_closure(movement.get_content())

        #Ver a cual es igual y añadirlo al array de map
        for state in dfa_states:
          if new_state == dfa_states[state]:
            # Al encontrar a que estado se mueve
            # lo agregamos al array de transiciones
            # El estaado al que se mueve lo encontre en base a la comparacion de index
            transition = (current_state, symbol, set_states.index(new_state.get_content()))
            transitions.append(transition)
            
    print("Estados:")
    for state in dfa_states:
      print(state, dfa_states[state])
    print("transiciones:")
    print(transitions)

class DFA(object):
  
  def __init__(self, regex):
    for char in regex:
      print(char)

# from visual_automata.fa.nfa import VisualNFA

# # a*

# nfa = VisualNFA(
#   states={"0", "1", "2", "3"},
#   input_symbols={"a"},
#   transitions={
#     "0": { "": {"1", "3"} },
#     "1": { "a": {"2"} },
#     "2": { "": {"1", "3"} },
#     "3": {}
#   },
#   initial_state="0",
#   final_states={"3"},
# )

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
