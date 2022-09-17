from set import PersonalSet
from stack import Stack
import utils

EPSILON = "E"

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

    # Stack de autómatas a concatenar.
    nfa_stack = Stack()

    for char in postfix_regex:
      
      print("Char", char)
      
      if (char not in utils.OPERATORS):
        concatenation_nfa = self.__symbol_transition(char)
        nfa_stack.push(concatenation_nfa)
      
      elif (char == "."):
        second_char = nfa_stack.pop()
        first_char = nfa_stack.pop()
        concatenation_nfa = self.__concatenation(first_char, second_char)
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
  
  def __concatenation(self, first, second):

    first_states = first["states"]
    states = first_states.union(PersonalSet([str((len(first_states) - 1)), str(len(first_states))]))
    
    alphabet = first["alphabet"].union(second["alphabet"])
    
    mapping = {}
    
    last_state = states.get_content()[-1]
    acceptance_states = PersonalSet([last_state])
    
    return {
      "states": states,
      "alphabet": alphabet,
      "mapping": mapping,
      "initial_state": "0",
      "acceptance_states": acceptance_states
    }
    
    # first_states = first["states"].get_content()
    # second_states = second["states"].get_content()
    
    # if (len(first_states) == len(second_states)):
    #   first_char = first["alphabet"].get_content()[0]
    #   second_char = second["alphabet"].get_content()[0]
    #   mapping["0"] = { first_char: PersonalSet(["1"]) }
    #   mapping["1"] = { second_char: PersonalSet(["2"]) }
    #   mapping["2"] = {}
    
    # else:
    #   first_states = first["states"]
    #   mapping["states"] = first_states.union(PersonalSet([str(0 + len(first_states) - 1), str(1 + len(first_states) - 1)]))
    
    return new_automata

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
