from finite_automata import NFA

class Regex(object):
  
  def __init__(self, expression):
    self.__expression = expression

  def __str__(self):
    return self.__expression

  def convert_to_NFA(self) -> NFA:
    nfa = []
    for char in self.__expression:
      if (char == "*"):
        nfa.append("")
