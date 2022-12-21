
#une solution x sera une liste [[x11,x12,...,x1n]
#                                ...
#                                [xi1,xi2,...,xin]
#                                ...
#                                [xm1,xm2,...,xmn]]
# où les variables xij sont binaires : xij vaut 1 si l'objet i est attribué à l'individu j

# U[i][j] -> utilité de l'objet i pour l'individu j
U = [[12,20,6,5,8],
     [5,12,6,8,5],
     [8,5,11,5,6],
     [6,8,6,11,5],
     [5,6,8,7,7]]

def vecteurs_ponderations_w(alpha,n):
    #renvoie le famille de vecteurs de pondérations wi(alpha) pour i=1...n
    if alpha < 1 :
        raise Exception("alpha est inférieure à 1 dans la fonction vecteurs_ponderations_w")
    
    vecteurs = []
    for i in range(1,n+1):
        wi = pow((n-i+1)/n,alpha) - pow((n-i)/n,alpha)
        vecteurs.append(wi)
    return vecteurs

def fonction_objectif_OWA(alpha,x):
    #renvoie un tuple composé de la liste z(i) ordonnée et la liste des poids wi pour la solution x
    n = len(x[0]) #nombre d'individus
    m = len(x) #nombre d'objets
    
    z = [0 for _ in range(n)]
    w = vecteurs_ponderations_w(alpha,n)
    
    for i in m:
        for j in n:
            if(x[i][j] == 1): #si l'objet i est attribué à j on ajoute l'utilité de l'objet à l'utilité de j
                z[j] += U[i][j]
                
    return (z.sort(),w)
    
    



