from Postfix import Post
from AFD import AFD
from AFN import AFN


from min_AFD import AFDmin
from timeit import default_timer

    #"(ab(a|b)*abb)"--> ab.ab|*.a.b.b.#.
    #"(a*|b*)*"     --> a*b*|*#. 
    #"((a|b)|a)*"   --> ab|a|*#.
    #"(a|b)*a"      --> ab|*a.#. 

if (__name__ == "__main__"):

    ##AFN apartir de regex
    inicio = default_timer()
    AFN( Post().postfix("((aaa)*|b)"))
    fin = default_timer()
    print("\nTiempo de validacion AFN: ", fin - inicio)

    ##AFD directo
    inicio2 = default_timer()
    print(AFD( Post().postfix("((aaa)*|b)")).simulation_afd(""))
    fin2 = default_timer()
    print("\nTiempo de validacion AFD directo: ", fin2 - inicio2)

    ##Minimizacion de AFD
    # AFDmin(AFD( Post().postfix("(ab(a|b)*abb)")).pasar_info()[0],AFD( Post().postfix("(ab(a|b)*abb)")).pasar_info()[1],AFD( Post().postfix("(ab(a|b)*abb)")).pasar_info()[2],AFD( Post().postfix("(ab(a|b)*abb)")).pasar_info()[3],AFD( Post().postfix("(ab(a|b)*abb)")).pasar_info()[4])

    


  
