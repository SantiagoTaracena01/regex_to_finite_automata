from finite_automata import NFA
from set import PersonalSet
from Postfix import Post
from arbol2 import Arbol2

if (__name__ == "__main__"):

  """
  (0|1)*00

  nfa = NFA(
    states=Set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]),
    alphabet=Set(["0", "1"]),
    mapping={
      "0": { "EPSILON": ["1", "7"], "0": [], "1": [] },
      "1": { "EPSILON": ["2", "3"], "0": [], "1": [] },
      "2": { "EPSILON": [], "0": ["4"], "1": [] },
      "3": { "EPSILON": [], "0": [], "1": ["5"] },
      "4": { "EPSILON": ["6"], "0": [], "1": [] },
      "5": { "EPSILON": ["6"], "0": [], "1": [] },
      "6": { "EPSILON": ["7"], "0": [], "1": [] },
      "7": { "EPSILON": [], "0": ["8"], "1": [] },
      "8": { "EPSILON": [], "0": ["9"], "1": [] },
      "9": { "EPSILON": [], "0": [], "1": [] },
    }
    initial_state="0",
    final_states=Set(["9"])
  )
  """

  states=PersonalSet(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
  alphabet=PersonalSet(["0", "1"])
  mapping={
      "0": { "E": ["1", "7"] },
      "1": { "E": ["2", "3"] },
      "2": { "0": ["4"] },
      "3": { "1": ["5"] },
      "4": { "E": ["6"] },
      "5": { "E": ["6"] },
      "6": { "E": ["1", "7"] },
      "7": { "0": ["8"]},
      "8": {"0": ["9"]},
      "9": {  },
    }
  initial_state="0"
  final_states=PersonalSet(["9"])

  my_nfa: NFA = NFA(states, alphabet, mapping, initial_state, final_states)

  my_nfa.to_dfa()
