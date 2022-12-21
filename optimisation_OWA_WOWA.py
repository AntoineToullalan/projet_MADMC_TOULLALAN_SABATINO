#import gurobipy as gp


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
        wi = round(wi,4)
        vecteurs.append(wi)
    return vecteurs

def fonction_objectif_OWA(alpha,x):
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

########################  CREATE PL ######################
def programme_lineaire():
    nb_objets = len(U)
    nb_individus = len(U[0])
    
    m = gp.Model()
    
    # Create variables
    x = m.addVar(vtype='B', name="x")
    y = m.addVar(vtype='B', name="y")
    z = m.addVar(vtype='B', name="z")
    
    # Set objective function
    m.setObjective(x + y + 2 * z, gp.GRB.MAXIMIZE)
    
    # Add constraints
    m.addConstr(x + 2 * y + 3 * z <= 4)
    m.addConstr(x + y >= 1)
    
    # Solve it!
    m.optimize()
    
    return m
    

print(f"Optimal objective value: {m.objVal}")
print(f"Solution values: x={x.X}, y={y.X}, z={z.X}")


#########################  MAIN  ##########################

x=[[1,0,0,0,0],
   [0,1,0,0,0],
   [0,0,1,0,0],
   [0,0,0,1,0],
   [0,0,0,0,1]
   ]

alpha=2

z,w = fonction_objectif_OWA(alpha,x)   
print("z ordonné : ")
print(z)

print("poids w : ")
print(w)

print("valeur de la fonction objectif : ")

f = 0
for i in range(len(z)):
    f += z[i]*w[i]

print(f)

'''
MODELE :
    
# Solve the following MIP:
#  maximize
#        x +   y + 2 z
#  subject to
#        x + 2 y + 3 z <= 4
#        x +   y       >= 1
#        x, y, z binary

import gurobipy as gp

# Create a new model
m = gp.Model()

# Create variables
x = m.addVar(vtype='B', name="x")
y = m.addVar(vtype='B', name="y")
z = m.addVar(vtype='B', name="z")

# Set objective function
m.setObjective(x + y + 2 * z, gp.GRB.MAXIMIZE)

# Add constraints
m.addConstr(x + 2 * y + 3 * z <= 4)
m.addConstr(x + y >= 1)

# Solve it!
m.optimize()

print(f"Optimal objective value: {m.objVal}")
print(f"Solution values: x={x.X}, y={y.X}, z={z.X}")
'''
    



