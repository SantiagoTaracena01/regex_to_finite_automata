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

    # Iteración sobre cada caracter en la expresión regular en postfix.
    for char in postfix_regex:

      # Si el caracter no es un operador, se crea un AFN de la transición y se inserta en el stack.
      if (char not in utils.OPERATORS):
        concatenation_nfa = self.__symbol_transition(char)
        nfa_stack.push(concatenation_nfa)

      # Si el operador es un kleene, se hace el kleene del último AFN del stack.
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
        union_nfa = self.__burger(postfix_regex, upper_union_character, lower_union_character)
        nfa_stack.push(union_nfa)
    
    # Asignación de valores finales luego del proceso de conversión.
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
        "0": { char: ["1"] },
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
        mapping[state] = { EPSILON: [next_state, last_state] }
      elif (index < (len(states.get_content()) - 2)):
        next_state = str((index + 1))
        mapping[state] = { chars[(index - 1)]: [next_state] }
      elif (index == (len(states.get_content()) - 2)):
        last_state = states.get_content()[-1]
        mapping[state] = { EPSILON: ["1", last_state] }
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

    if ((utils.check_epsilon_transitions(first["mapping"]) > 0) or (utils.check_epsilon_transitions(second["mapping"]) > 0)):
      
      states = []
      
      complex_nfa = (first if (utils.check_epsilon_transitions(first["mapping"]) > 0) else second)
      
      if (complex_nfa == first):
        for state in complex_nfa["states"].get_content():
          states.append(state)

      states.append(str((int(states[-1]) + 1)))

      alphabet = first["alphabet"].union(second["alphabet"])

      mapping = complex_nfa["mapping"]
      
      chars = utils.get_regex_operands(regex)
      
      mapping[states[-2]] = { chars[-1]: [states[-1]] }
      mapping[states[-1]] = {}
      
      last_state = states[-1]
      acceptance_states = PersonalSet([last_state])
      
      states = PersonalSet([states])

    else:
      
      # Estados del primer conjunto.
      first_states = first["states"]
      states = first_states.union(PersonalSet([str((len(first_states) - 1)), str(len(first_states))]))
      
      alphabet = first["alphabet"].union(second["alphabet"])
      
      mapping = {}
      
      chars = utils.get_regex_operands(regex)
      
      for index, state in enumerate(states.get_content()):
        if (index < (len(states.get_content()) - 1)):
          mapping[state] = { chars[index]: [str((int(state) + 1))] }
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

  def __burger(self, regex, upper_nfa, lower_nfa):

    states = ["0"]
    upper_states = len(upper_nfa["states"])
    lower_states = len(lower_nfa["states"])
    united_states = (upper_states + lower_states)
    
    for index in range(united_states):
      states.append(str((index + 1)))

    states.append(str((int(states[-1]) + 1)))
    
    mapping = {}
    
    chars = utils.get_regex_operands(regex)
    
    for index, state in enumerate(states):
      if (state == "0"):
        mapping[state] = { EPSILON: ["1", str((upper_states + 1))] }
      elif (1 <= int(state) <= (upper_states - 1)):
        mapping[state] = { chars[index - 1]: [str((int(state) + 1))] }
      elif (state == str(upper_states)):
        mapping[state] = { EPSILON: [states[-1]] }
      elif ((upper_states + 1) <= int(state) <= int(states[-3])):
        mapping[state] = { chars[index - 2]: [str((int(state) + 1))] }
      elif (state == states[-2]):
        mapping[state] = { EPSILON: [states[-1]] }
      else:
        mapping[state] = {}
    
    return {
      "states": PersonalSet(states),
      "alphabet": upper_nfa["alphabet"].union(lower_nfa["alphabet"]),
      "mapping": mapping,
      "initial_state": "0",
      "acceptance_states": PersonalSet(["5"])
    }

  def __str__(self):
    return f"States: {self.__states}\nInitial State: {self.__initial_state}\nAcceptance States: {self.__acceptance_states}\nAlphabet: {self.__alphabet}\nMapping: {self.__mapping}\n"

class DFA(object):

  def __init__(self, regex):
    for char in regex:
      print(char)
