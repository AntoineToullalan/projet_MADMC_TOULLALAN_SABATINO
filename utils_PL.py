#from gurobipy import *
import random
import numpy as np

################## fonctions pour le PL OWA #######################

def vecteurs_ponderations_w(alpha,n):
    #renvoie le famille de vecteurs de pondérations wi(alpha) pour i=1...n
    if alpha < 1 :
        raise Exception("alpha est inférieure à 1 dans la fonction vecteurs_ponderations_w")
    
    vecteurs = []
    for i in range(1,n+1):
        wi = pow((n-i+1)/n,alpha) - pow((n-i)/n,alpha)
        wi = round(wi,4)
        vecteurs.append(wi)
    return vecteurs

def ponderation_lorenz(w):
    #ponderations pour le PL OWA
    w_prime = []
    for i in range(len(w)-1):
        w_prime.append(w[i]-w[i+1])
    w_prime.append(w[-1])
    return w_prime


########################  fonctions pour résoudre le PL OWA de manière exhaustive ######################
def valeur_fonction_objectif(z,w):
    f=0
    for i in range(len(z)):
        f += z[i]*w[i]
    return f

def fonction_objectif_OWA(alpha,x,U):
    #renvoie un tuple composé de la liste z(i) ordonnée et la liste des poids wi pour la solution x
    n = len(x[0]) #nombre d'individus
    m = len(x) #nombre d'objets
    
    z = [0 for _ in range(n)]
    w = vecteurs_ponderations_w(alpha,n)
    
    for i in range(m):
        for j in range(n):
            if(x[i][j] == 1): #si l'objet i est attribué à j on ajoute l'utilité de l'objet à l'utilité de j
                z[j] += U[i][j]
    z.sort()           
    return (z,w)

def solutions_attributions(alpha,n_objet,nb_individus):
    res = []
    
    if(n_objet==0):
        return res
    
    sol_rec = solutions_attributions(alpha,n_objet-1,nb_individus)
    
    res2=[]
    #pour l'objet n_objet on regarde toute les solutions possibles (tout les individus auquel il peut être attribué)
    for i in range(nb_individus):
        ligne=[0 for _ in range(nb_individus)]
        ligne[i] = 1 #attribué à l'individu i
        res2.append([ligne])
        
        if(sol_rec != []):
            for sol in sol_rec:
                sol_copie = sol.copy()
                sol_copie.append(ligne)
                res += [sol_copie]
        else:
            res = res2

    return res
   

def methode_exhaustive(alpha,U):
    fmax=0
    sol_max=[]
    print(U)
    nb_objets = len(U)
    nb_individus = len(U[0])
    solutions = solutions_attributions(alpha,nb_objets,nb_individus)
    for x in solutions:
        z,w = fonction_objectif_OWA(alpha,x,U)
        f = valeur_fonction_objectif(z,w)
        if(f>fmax):
            fmax=f
            sol_max=x
    
    return (fmax,sol_max)
    
def composantes_solution(sol,alpha,U):
    #renvoie les composantes non modifiées et les composantes de Lorenz de la solution 
    z,_ = fonction_objectif_OWA(alpha,sol,U)
    val_lorenz = []
    somme = 0
    for zi in z:
        somme+=zi
        val_lorenz.append(somme)
    return (val_lorenz,z)

################# fonctions génératrice de matrices pour les tests #####################

def genere_matrice_unite(n,p,upper_bound_cost):
    #les couts de la matrice sont entre 0 et upper_bound_cost et la taille est de n * p
    if(p < n):
        raise Exception("p est inférieur à n dans la matrice de coût")
    if(upper_bound_cost < 0):
        raise Exception("Les coûts de la matrice doivent être supérieur à 0")
    matrice = []
    for i in range(n):
        matrice.append([])
        for j in range(p):
            matrice[i].append(random.randrange(upper_bound_cost+1))
    return matrice

def genere_matrice_ensemble(n):
    #genere 10 matrice pour n = n et p = 5*n et upper_bound_cost=20
    p = 5*n
    upper_bound_cost = 20
    
    ensemble_matrice = []
    for i in range(10):
        ensemble_matrice.append(genere_matrice_unite(n,p,upper_bound_cost))
    return ensemble_matrice

####################### PL WOWA #######################

def index_ordonne(n, p, U):
    #retourne la matrice des ordres des valeurs de la matrice utilité et la matrice avec les utilités ordonnées
    index_ord=[[i for i in range(0,p)] for j in range(0,n)]
    U1=U.copy()
    U2=U.copy()
    for i in range(n):
        U1[i]=np.sort(U1[i],axis=0)
        U2[i]=np.sort(U1[i],axis=0)
        for j in range(p):
            index=np.where(np.array(U1[i]) == U[i][j])[0][0]
            index_ord[i][j]=index
            U1[i][index]=-1
    return index_ord, U2

def ponderations_phi(p, alpha):
    return p**alpha

def utilite_solution(sol,U):
    #renvoie les composantes de Lorenz de la solution
    z=[]
    for i in range(len(sol)):
        somme=0
        for j in range(len(sol[i])):
            somme += sol[i][j] * U[i][j]
        z.append(somme)
        i+=1
    
    z.sort()
    for i in range(len(z)-1):
        z[i+1]=z[i]+z[i+1]
    
    return z
            
    
def composantes_lorenz(sol,alpha,U):
    #les composantes de Lorenz de la solution 
    z = utilite_solution(sol,U)
    val_lorenz = []
    somme = 0
    for zi in z:
        somme+=zi
        val_lorenz.append(somme)
    return val_lorenz

def liste_vect_tests_WOWA():
    #renvoie les vecteurs poids pour les tests du WOWA
    liste_vect=[]
    n_steps=4
    for i in range(5):
        liste_vect.append([])
        poids = [1/5]*5
        for j in range(n_steps+1):
            if(j!=0):
                incr=(1-1/5)/n_steps
                decr=(1/5)/n_steps
                for k in range(len(poids)):
                    if(k==i):
                        poids[k]+=incr
                    else:
                        poids[k]-=decr
                    poids[k]=round(poids[k],2)
            liste_vect[i].append(poids.copy())  
    return liste_vect


