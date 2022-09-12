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

  def __str__(self):
    return f"""
      States: {self.__states}
      Alphabet: {self.__alphabet}
      Mapping: {self.__mapping}
    """

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
