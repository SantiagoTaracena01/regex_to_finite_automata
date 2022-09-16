from finite_automata import NFA

if (__name__ == "__main__"):
  
  regex: str = input("\nIngresa una expresión regular: ")
  my_nfa: NFA = NFA(regex)
  print(my_nfa)
