from regex import Regex
from finite_automata import NFA, DFA

if (__name__ == "__main__"):
  
  regex_expression: str = input("Ingresa una expresión regular: ")
  regex_chain: str = input("Ingresa una cadena: ")
  
  my_regex: Regex = Regex(regex_expression)
  my_nfa: NFA = NFA({"a", "b", "c"}, {"a", "b"}, {("a", "a"), ("a", "b"), ("b", "b")})
  print(my_regex)
