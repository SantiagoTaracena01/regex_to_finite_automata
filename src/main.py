from Postfix import Post
from AFD import AFD
from timeit import default_timer

if (__name__ == "__main__"):
    #"(ab(a|b)*abb)"--> ab.ab|*.a.b.b.#.
    #"(a*|b*)*"     --> a*b*|*#. 
    #"((a|b)|a)*"   --> ab|a|*#.
    #"(a|b)*a"      --> ab|*a.#. 
    inicio = default_timer()
    print(AFD( Post().postfix("(ab(a|b)*abb)")).simulation_afd("abbbbbbbbbbbbbbababababb"))
    fin = default_timer()
    print("\nTiempo de validacion: ", fin - inicio)


  
