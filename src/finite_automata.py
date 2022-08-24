EPSILON: str = "E"

class NFA(object):
  
  def __init__(self, states, alphabet, mapping):
    self.__states = states
    self.__alphabet = alphabet
    self.__mapping = mapping

class DFA(object):
  
  def __init__(self, states, alphabet):
    self.__states = states
    self.__alphabet = alphabet
