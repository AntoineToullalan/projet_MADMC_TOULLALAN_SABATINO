from optimisation_OWA_WOWA import *
import numpy as np
import matplotlib.pyplot as plt

def tests_1_1(affiche_valeurs=False,affiche_composantes=False,affiche_Lorenz=False):
    # U[i][j] -> utilité de l'objet i pour l'individu j
    U = [[12,20,6,5,8],
         [5,12,6,8,5],
         [8,5,11,5,6],
         [6,8,6,11,5],
         [5,6,8,7,7]]
    
    all_alpha = [1 + 0.1*i for i in range(5)]
    all_val = []
    all_z = []
    all_lorenz = []
    
    for alpha in all_alpha:
        f,sol = methode_exhaustive(alpha,U)
        
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
    for n in [5,10,15]:
        dix_matrices = genere_matrice_ensemble(n)
        temps_moyen = 0
        for matrice in dix_matrices:
            for alpha in [1+0.1*i for i in range(10)]:
                print(alpha)
                f,sol = methode_exhaustive(alpha,matrice)
            
    
################################## MAIN ################################
#tests_1_1(affiche_valeurs=True)
tests_1_2()


            
    


