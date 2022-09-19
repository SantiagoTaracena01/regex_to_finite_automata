from utility_classes import State, SimpleNFA
from set import PersonalSet
from stack import Stack
import utils
import collections

EPSILON = "E"

class NFA(object):

  __states = PersonalSet([])
  __alphabet = PersonalSet([])
  __mapping = {}
  __initial_state = None
  __acceptance_states = PersonalSet([])
  
  def __init__(self, regex):
    
    postfix_regex = utils.regex_infix_to_postfix(regex)
    
    nfa_stack = Stack()
    
    for char in postfix_regex:
      
      # Creación del alfabeto del AFN.
      if ((char not in utils.OPERATORS) and (char not in self.__alphabet)):
        self.__alphabet.add(char)

      # Si el caracter encontrado es un operador kleene.
      if (char == "*"):

        # Contenido actual de los estados del AFN.
        content_from_states = self.__states.get_content()
        new_content = list(map(lambda n: n + 1, content_from_states))
        new_states = [0]

        # Nuevos estados luego de la creación del kleene.
        for state in new_content:
          new_states.append(state)

        # Finalización de la nueva lista de estados.
        new_acceptance_state = (new_states[-1] + 1)
        new_states.append(new_acceptance_state)

        # AFN al cual aplicar la operación kleene.
        first_nfa = nfa_stack.pop()

        # Nuevo estado inicial y de aceptación del AFN.
        new_initial = State(0)
        new_acceptance = State(new_acceptance_state)

        # El nuevo estado inicial va al estado inicial del AFN anterior y al estado de aceptación.
        new_initial.set_first_edge(first_nfa.get_initial_state())
        new_initial.set_last_edge(new_acceptance)

        # El estado de aceptación del AFN ahora se dirige al estado inicial anterior y al de aceptación.
        first_nfa_acceptante_states = first_nfa.get_acceptance_states()
        first_nfa_acceptante_states.set_first_edge(first_nfa.get_initial_state())
        first_nfa_acceptante_states.set_last_edge(new_acceptance)

        # El nuevo AFN se almacena en el stack.
        new_nfa = SimpleNFA("*", new_initial, new_acceptance)
        nfa_stack.push(new_nfa)

        # Nuevo conjunto de estados del AFN.
        self.__states = PersonalSet(new_states)
        
        new_mapping = {}

        # Iteración sobre cada entrada del mapeo para actualizarlo.
        for entrance in self.__mapping:

          # Diccionario de cada entrada y llave.
          entrance_content = self.__mapping[entrance] # { a: [3] }, { EPSILON: [2, 4] }
          
          try:
            entrance_key = list(entrance_content.keys())[0] # a, EPSILON
          except:
            entrance_key = 0

          if (entrance_content == {}):
            new_mapping[entrance + 1] = { EPSILON: [new_acceptance_state, 1] }
          elif (entrance_key == EPSILON):
            entrance_list = entrance_content[entrance_key]
            new_mapping[entrance + 1] = { entrance_key: [(entrance_list[0] + 1), (entrance_list[1] + 1)] }
          else:
            new_mapping[entrance + 1] = { entrance_key: [(n + 1) for n in entrance_content[entrance_key]] }
        
        new_mapping[0] = { EPSILON: [1, new_acceptance_state] }
        new_mapping[new_acceptance_state] = {}
        
        # Organización del mapeo del AFN.
        new_sorted_mapping = dict(collections.OrderedDict(sorted(new_mapping.items())))

        # Cambio del mapeo del AFN.
        self.__mapping = new_sorted_mapping

      elif (char == "."):
        
        # Sacamos los dos primeros AFNs del stack, los necesitamos para concatenar.
        first_nfa = nfa_stack.pop()
        second_nfa = nfa_stack.pop()
        
        # El estado de aceptación del primer AFN pasa a ser el inicial del segundo AFN.
        first_nfa_acceptante_states = first_nfa.get_acceptance_states()
        first_nfa_acceptante_states.set_first_edge(second_nfa.get_initial_state())
        
        # El nuevo AFN se almacena en el stack.
        new_nfa = SimpleNFA(".", first_nfa.get_initial_state(), second_nfa.get_acceptance_states())
        nfa_stack.push(new_nfa)
      
      # Si el caracter es un operando, se crea un AFN de un caracter único.
      else:
        
        # Nuevo estado inicial y de aceptación del AFN.
        content_from_states = self.__states.get_content()
        last_created_state = content_from_states[-1] if content_from_states else 0
        
        # Creación de los nuevos estados inicial y de aceptación del AFN.
        new_initial = State(last_created_state)
        new_acceptance = State(last_created_state + 1)
        
        # El nuevo estado permite llegar a un estado de aceptación con el caracter hallado.
        new_initial.set_label(char)
        new_initial.set_first_edge(new_acceptance)

        # El nuevo AFN creado se agrega al stack de AFNs.
        new_nfa = SimpleNFA("", new_initial, new_acceptance)
        nfa_stack.push(new_nfa)

        # Los nuevos estados son agregados al conjunto de estados de AFN.
        self.__states.add(last_created_state)
        self.__states.add(last_created_state + 1)
        
        # El mapping del AFN es actualizado con la incorporación del nuevo AFN.
        self.__mapping[new_initial.get_state()] = { char: [new_acceptance.get_state()] }
        self.__mapping[new_acceptance.get_state()] = {}
    
    listed_states = self.__states.get_content()
    self.__initial_state = listed_states[0]
    self.__acceptance_states = PersonalSet([listed_states[-1]])

  def __repr__(self):
    return f"States: {self.__states}\nInitial State: {self.__initial_state}\nAcceptance States: {self.__acceptance_states}\nAlphabet: {self.__alphabet}\nMapping: {self.__mapping}\n"

class DFA(object):

  def __init__(self, regex):
    for char in regex:
      print(char)
