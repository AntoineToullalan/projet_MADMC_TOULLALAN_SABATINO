import numpy as np
from utils_PL import *
from gurobipy import *

def solve_wowa(U, p_vect, alpha):
    n = len(U)
    p = len(U[0])
    m = Model()
    x=[]
    for i in range(1,n+1):
        agent_objet=[]
        for j in range(1,p+1):
            agent_objet.append((m.addVar(vtype='B', lb=0, name="x_"+str(i)+"_"+str(j))))
        x.append(agent_objet)
    m.update()
    obj = LinExpr()
    
    index_ord, Uc = index_ordonne(n, p, U)
    for i in range(n):
        phi_ki=ponderations_phi(np.sum(p_vect[i:]),alpha)
        phi_kip=ponderations_phi(np.sum(p_vect[i+1:]),alpha)
        
        for j in range(p):
            obj +=(phi_ki-phi_kip) * Uc[i][index_ord[i][j]]* x[i][j]

    m.setObjective(obj,GRB.MAXIMIZE)
    
    t=0
    for j in range(p):
        m.addConstr(quicksum(x[i][j] for i in [y for y in range(n)]) <= 1)
    
    m.optimize()
    sol=[]
    for i in range(n):
        sol.append([])
        for j in range(p):
            sol[i].append(x[i][j].x)
    return sol, m.objval


######################### MAIN ##########################
'''
alpha = 5
U = [[12,20,6,5,8],
     [5,12,6,8,5],
     [8,5,11,5,6],
     [6,8,6,11,5],
     [5,6,8,7,7]]


opt_list = []            
for liste_vect in liste_vect_tests_WOWA():
    for vect in liste_vect:
        sol, valeur_sol =solve_wowa(U,vect,alpha)
        opt_list.append(valeur_sol)
    
'''