from set import PersonalSet
from stack import Stack
import utils

EPSILON = "E"

"""
OR de prueba
or_nfa = {
  "states": PersonalSet(["0", "1", "2", "3", "4", "5"]),
  "alphabet": PersonalSet(["a", "b"]),
  "mapping": {
    "0": { EPSILON: PersonalSet(["1", "2"]) },
    "1": { "a": PersonalSet(["3"]) },
    "2": { "b": PersonalSet(["4"]) },
    "3": { EPSILON: PersonalSet(["5"]) },
    "4": { EPSILON: PersonalSet(["5"]) },
    "5": {}
  },
  "initial_state": "0",
  "acceptance_states": PersonalSet(["5"]),
}
"""

class NFA(object):

  __states = PersonalSet([])
  __alphabet = PersonalSet([])
  __mapping = {}
  __initial_state = None
  __acceptance_states = PersonalSet([])

  # Método constructor del AFN.
  def __init__(self, regex):
    
    # Simplificación previa de la expresión regular.
    simplified_regex = utils.simplify_regex(regex)
    postfix_regex = utils.regex_infix_to_postfix(simplified_regex)

    print(postfix_regex)

    # Stack de autómatas a concatenar.
    nfa_stack = Stack()

    # Iteración sobre cada caracter en la expresión regular en postfix.
    for char in postfix_regex:

      # Si el caracter no es un operador, se crea un AFN de la transición y se inserta en el stack.
      if (char not in utils.OPERATORS):
        concatenation_nfa = self.__symbol_transition(char)
        nfa_stack.push(concatenation_nfa)

      elif (char == "*"):
        kleene_char = nfa_stack.pop()
        kleene_nfa = self.__ship(postfix_regex, kleene_char)
        nfa_stack.push(kleene_nfa)

      # Si el operador es una concatenación, se concatenan los últimos dos AFNs almacenados en el stack.
      elif (char == "."):
        second_char = nfa_stack.pop()
        first_char = nfa_stack.pop()
        concatenation_nfa = self.__concatenation(postfix_regex, first_char, second_char)
        nfa_stack.push(concatenation_nfa)
      
      elif (char == "+"):
        lower_union_character = nfa_stack.pop()
        upper_union_character = nfa_stack.pop()
        union_nfa = self.__burger(upper_union_character, lower_union_character)
        nfa_stack.push(union_nfa)
    
    final_nfa = nfa_stack.pop()
    self.__states = final_nfa["states"]
    self.__alphabet = final_nfa["alphabet"]
    self.__mapping = final_nfa["mapping"]
    self.__initial_state = final_nfa["initial_state"]
    self.__acceptance_states = final_nfa["acceptance_states"]

  def __symbol_transition(self, char):
    return {
      "states": PersonalSet(["0", "1"]),
      "alphabet": PersonalSet([char]),
      "mapping": {
        "0": { char: PersonalSet(["1"]) },
        "1": {},
      },
      "initial_state": "0",
      "acceptance_states": PersonalSet(["1"]),
    }

  def __ship(self, regex, original_nfa):
    original_nfa_states = original_nfa["states"]
    additional_states = PersonalSet([str(len(original_nfa_states)), str((len(original_nfa_states) + 1))])
    states = original_nfa_states.union(additional_states)
    
    alphabet = original_nfa["alphabet"]
    
    mapping = {}
    
    chars = utils.get_regex_operands(regex)
    
    for index, state in enumerate(states.get_content()):
      if (index == 0):
        next_state = str((index + 1))
        last_state = states.get_content()[-1]
        mapping[state] = { EPSILON: PersonalSet([next_state, last_state]) }
      elif (index < (len(states.get_content()) - 2)):
        next_state = str((index + 1))
        mapping[state] = { chars[(index - 1)]: PersonalSet([next_state]) }
      elif (index == (len(states.get_content()) - 2)):
        last_state = states.get_content()[-1]
        mapping[state] = { EPSILON: PersonalSet(["1", last_state]) }
      else:
        mapping[state] = {}
    
    last_state = states.get_content()[-1]
    acceptance_states = PersonalSet([last_state])

    return {
      "states": states,
      "alphabet": alphabet,
      "mapping": mapping,
      "initial_state": "0",
      "acceptance_states": acceptance_states
    }
  
  def __concatenation(self, regex, first, second):
    
    if (utils.check_epsilon_transitions(first["mapping"]) > 0):

      print()

    else:
      
      # Estados del primer conjunto.
      first_states = first["states"]
      states = first_states.union(PersonalSet([str((len(first_states) - 1)), str(len(first_states))]))
      
      alphabet = first["alphabet"].union(second["alphabet"])
      
      mapping = {}
      
      chars = utils.get_regex_operands(regex)
      
      for index, state in enumerate(states.get_content()):
        if (index < (len(states.get_content()) - 1)):
          mapping[state] = { chars[index]: PersonalSet([str((int(state) + 1))]) }
        else:
          mapping[state] = {}
      
      last_state = states.get_content()[-1]
      acceptance_states = PersonalSet([last_state])
    
    return {
      "states": states,
      "alphabet": alphabet,
      "mapping": mapping,
      "initial_state": "0",
      "acceptance_states": acceptance_states
    }

  def __map_concatenation_automata(self, mapping, automata):
    if (len(automata["mapping"]) == 2):
      for entry in automata["mapping"]:
        if (automata["mapping"][entry] == {}):
          continue
        print("Entry", entry)
        numerical_entry = int(entry)
        entry_mapping = automata["mapping"][entry]
        print("Entry mapping", entry_mapping)
        entry_mapping_key = list(entry_mapping.keys())[0]
        numerical_state = int(entry_mapping[entry_mapping_key].get_content()[0])
        new_entry = str((numerical_entry + 1))
        mapping[new_entry] = { entry_mapping_key: PersonalSet([str((numerical_state + 2))]) }
        print(new_entry, mapping[new_entry])
    return mapping

  def __burger(self, upper_nfa, lower_nfa):
    
    # Mapeo inicial del autómata.
    mapping = { "0": { EPSILON: PersonalSet(["1", "2"]) } }
    
    # Alfabetos de los autómatas en forma de listas.
    upper_alphabet = upper_nfa["alphabet"].get_content()
    lower_alphabet = lower_nfa["alphabet"].get_content()
    
    mapping = self.__map_concatenation_automata(mapping, upper_nfa)
    mapping = self.__map_concatenation_automata(mapping, lower_nfa)
    print("Mapping after concatenation", mapping)
    
    # # Si la longitud del alfabeto de arriba es 1, puede ser una concatenación o un kleene.
    # if (len(upper_nfa["mapping"]) == 2):
    #   for entry in upper_nfa["mapping"]:
        
    #     # entry = 0
    #     # upper_nfa["mapping"][entry] = { a: {1} }
        
    #     # entry_mapping = { a: {1} }
    #     entry_mapping = upper_nfa["mapping"][entry]
    #     entry_mapping_key = entry_mapping.keys()[0]
        
    #     # numerical_entry = 0 como int
    #     numerical_entry = int(entry)
    #     numerical_state = int(entry_mapping[entry_mapping_key].get_content()[0])
        
    #     # new_entry = 1
    #     new_entry = str((numerical_entry + 1))
    #     mapping[new_entry] = { entry_mapping_key: PersonalSet([str((numerical_state + 2))]) }
        
    #     # ACABAR CON: { 1: { a: {3} } } para hacer mapping[1] = { a: {3} }
    
    return {
      "states": PersonalSet(["0", "1", "2", "3", "4", "5"]),
      "alphabet": upper_nfa["alphabet"].union(lower_nfa["alphabet"]),
      "mapping": mapping,
      "initial_state": "0",
      "acceptance_states": "5"
    }

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
