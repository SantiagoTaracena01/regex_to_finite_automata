from finite_automata import NFA

if (__name__ == "__main__"):
  regex = input("Regex: ")
  print(NFA(regex))
