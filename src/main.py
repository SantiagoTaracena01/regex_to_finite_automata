from finite_automata import NFA

if (__name__ == "__main__"):
  
  regex: str = input("Ingresa una expresión regular: ")
  regex_chain: str = input("Ingresa una cadena: ")
  my_nfa: NFA = NFA(regex)
  print(my_nfa)
