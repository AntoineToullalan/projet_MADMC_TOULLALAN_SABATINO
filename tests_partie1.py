from PL_OWA import *
from utils_PL import *
import numpy as np
import matplotlib.pyplot as plt
import time

def tests_1_1(affiche_valeurs=False,affiche_composantes=False,affiche_Lorenz=False):
    #affiche... -(si affiche_valeurs=True) l'évolution de la somme des utilités en fonction de alpha
    #           -(si affiche_composantes=True) la valeur des utilités des individus pour différentes valeurs de alpha
    #           -(si affiche_Lorenz=True) les composantes de Lorenz pour différentes valeurs de alpha
    # U[i][j] -> utilité de l'objet i pour l'individu j
    U = [[12,20,6,5,8],
         [5,12,6,8,5],
         [8,5,11,5,6],
         [6,8,6,11,5],
         [5,6,8,7,7]]
    n = len(U)
    p = len(U[0])
    
    all_alpha = [1 + 0.1*i for i in range(5)]
    all_val = []
    all_z = []
    all_lorenz = []
    
    for alpha in all_alpha:
        w = vecteurs_ponderations_w(alpha,n)
        sol = solve_owa(n,p,w,U)
        
        val_lorenz,z = composantes_solution(sol,alpha,U)
        all_val.append(sum(z))
        all_z.append(z)
        all_lorenz.append(val_lorenz)
    
    if(affiche_valeurs):
        #Affichage de la somme des utilités des individus pour les solutions optimales en fonction de alpha
        plt.plot(all_alpha,all_val,'ro')
        plt.xlabel('valeur de alpha')
        plt.ylabel('somme des utilités des individus')
        plt.show()
    
    if(affiche_composantes or affiche_Lorenz):
        #Affichage des valeurs de la fonction objectif pour les solutions optimales en fonction de alpha
        if(affiche_composantes):
            i=0
            for z in all_z:
                fig = plt.figure()
                ax = fig.add_axes([0,0,1,1])
                ax.bar(["z ("+str(i)+")" for i in range(len(z))],z)
                print(z)
                plt.title("alpha = "+str(all_alpha[i]))
                plt.show()
                i+=1
        if(affiche_Lorenz):
            i=0
            for z in all_lorenz:
                fig = plt.figure()
                ax = fig.add_axes([0,0,1,1])
                ax.bar(["L "+str(i) for i in range(len(z))],z)
                print(z)
                plt.title("alpha = "+str(all_alpha[i]))
                plt.show()
                i+=1

    plt.show()

def tests_1_2():
    #calcul les temps de résolution moyen du PL OWA pour n=5,10,15
    temps_moyen_n=[]
   
    for n in [5,10,15]:
        dix_matrices = genere_matrice_ensemble(n)
        temps_moyen = 0
        i = 0
        for matrice in dix_matrices:
            for alpha in [1+0.1*i for i in range(10)]:
                print(alpha)
                p=len(matrice[0])
                w = vecteurs_ponderations_w(alpha,n)
                t=time.time()
                sol = solve_owa(n, p, w, matrice)
                temps_moyen+= (time.time() - t)
                i+=1
        temps_moyen_n.append(temps_moyen/i)
    return temps_moyen_n
                
                
            
    
################################## MAIN ################################
tests_1_1(affiche_Lorenz=True)
temps = tests_1_2()
print("temps de calcul du PL OWA pour des matrices de différentes tailles : ")
print(temps)


            
    


