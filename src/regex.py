from finite_automata import NFA
from stack import Stack

class Regex(object):
  
  def __init__(self, expression):
    self.__expression = expression

  def __str__(self):
    return self.__expression

  def thompson_algorithm(self) -> NFA:
    ...
