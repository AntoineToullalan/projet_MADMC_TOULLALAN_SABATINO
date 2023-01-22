from gurobipy import *
from utils_PL import *


def solve_owa(n,p,w,matrice):
    #n : nombre d'agents
    #p : nompre d'objets
    #w : poids de la fonction objectif
    #matrice : matrice utilité
    
    m = Model()
    w_prime = ponderation_lorenz(w)
    
    b=[]
    r=[]
    z=[]
    for i in range(1,n+1):
        r.append(m.addVar(vtype='C', name="r_"+str(i)))
        z.append([])
        b.append([])
        for j in range(1,p+1):
            z[i-1].append(m.addVar(vtype='B', name="z_"+str(i)+"_"+str(j)))
            b[i-1].append(m.addVar(vtype='C', name="b_"+str(i)+"_"+str(j)))
    maxi=m.addVar(vtype='C', name="Max")
    
    #un objet n'est assigné qu'à un individu
    for j in range(p):
            m.addConstr(sum([z[i][j] for i in range(n)])==1,"L'objet %d est assigné à 1 seule personne"%j)
            
    for i in range(n):
        for k in range(n):
            yi = sum(z[i][j] * matrice[i][j] for j in range(p))
            m.addConstr(maxi >= yi,"maxi est supérieur ou égal à l'utilité de la personne %d"%i)
            m.addConstr(r[k] + b[i][k] >= maxi - yi,"Calcul de la  composante de Lorenz L%d"%i)
    m.update()
    
    obj = LinExpr();
    obj = 0
    for k in range(n):
            obj += (w_prime[k]*(maxi * (k+1) - (k+1)*r[k] - sum([b[i][k] for i in range(n)])))
            
    m.setObjective(obj,GRB.MAXIMIZE)
    m.update()
    m.optimize()    
    sol=[]
    for i in range(n):
        sol.append([])
        for j in range(p):
            sol[i].append(z[i][j].x)  
    return sol
  

#########################  MAIN  ##########################

'''
# matrice[i][j] -> utilité de l'objet i pour l'individu j

matrice = [[12,20,6,5,8],
     [5,12,6,8,5],
     [8,5,11,5,6],
     [6,8,6,11,5],
     [5,6,8,7,7]]

alpha=1.4

n = len(matrice)
p = len(matrice[0])
w = vecteurs_ponderations_w(alpha,n)

sol = solve_owa(n,p,w,matrice)
print(sol)
'''

            
    
    


