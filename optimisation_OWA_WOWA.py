#from gurobipy import *
import random
#une solution x sera une liste [[x11,x12,...,x1n]
#                                ...
#                                [xi1,xi2,...,xin]
#                                ...
#                                [xm1,xm2,...,xmn]]
# où les variables xij sont binaires : xij vaut 1 si l'objet i est attribué à l'individu j


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

def valeur_fonction_objectif(z,w):
    f=0
    for i in range(len(z)):
        f += z[i]*w[i]
    return f

########################  on résoud le PL de manière exhaustive ######################
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
    

########################  solve PL with gurobi ######################

def PL_OWA(w,U):
    nb_objets = len(U)
    nb_individus = len(U[0])
    
    m = Model()
    
    # Create variables
    x=[]
    for i in range(1,nb_objets+1):
        x.append([])
        for j in range(1,nb_individus+1):
            x[i-1].append(m.addVar(vtype='B', name="x_"+str(i)+"_"+str(j)))
    
    # maj du modele pour integrer les nouvelles variables
    m.update()
    
    # ajout de la fonction objectif
    
    liste_zi=[]
    for i in range(nb_objets):
        zi = 0
        for j in range(nb_individus):
            zi += U[i][j] * x[i][j]
        liste_zi.append(zi)

    obj = LinExpr();
    obj=0
        
    for i in range(nb_individus):
        obj += liste_zi[i] * w[i]
            
    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)
    
    # Add constraints
    for i in range(nb_objets):
        m.addConstr(quicksum(x[i][j] for j in range(nb_individus)) <= 1, "Contrainte %d" % i) #chaque objet est attribué à au plus un individu
    
    # Solve it!
    m.update()
    m.optimize()
    print(f"Optimal objective value: {m.objVal}")
    sol=[]
    for i in range(nb_objets):
        sol.append([])
        for j in range(nb_individus):
            sol[i].append(x[i][j].x)
    
    return sol
    


#########################  MAIN  ##########################

# U[i][j] -> utilité de l'objet i pour l'individu j

U = [[12,20,6,5,8],
     [5,12,6,8,5],
     [8,5,11,5,6],
     [6,8,6,11,5],
     [5,6,8,7,7]]

alpha=2
'''
n = len(U)
w = vecteurs_ponderations_w(alpha,n)
sol = PL_OWA(w,U)
print(sol)


f,sol = methode_exhaustive(alpha,U)
print(f)
print(sol)
'''

