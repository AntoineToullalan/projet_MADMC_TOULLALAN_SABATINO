from gurobipy import *

dic_graphe={}
dic_graphe[('a','b')]=(5,3)
dic_graphe[('a','c')]=(10,4)
dic_graphe[('a','d')]=(2,6)
dic_graphe[('b','d')]=(1,3)
dic_graphe[('b','c')]=(4,2)
dic_graphe[('b','e')]=(4,6)
dic_graphe[('d','c')]=(1,4)
dic_graphe[('d','f')]=(3,5)
dic_graphe[('c','e')]=(3,1)
dic_graphe[('c','f')]=(1,2)
dic_graphe[('e','g')]=(1,1)
dic_graphe[('f','g')]=(1,1)

sommets_graphe=['a','b','c','d','e','f','g']

def PL_graphe_choquet(fonction_croyance):
    
    m = Model()
    
    var_arcs={}
    contr1=0
    contr2=0
    for s1,s2 in dic_graphe.keys():
        var_arcs[(s1,s2)]=m.addVar(vtype='B', name="x_"+s1+"_"+s2)
        xij = var_arcs[(s1,s2)]
        contr1 += xij * dic_graphe[(s1,s2)][0]
        contr2 += xij * dic_graphe[(s1,s2)][1]
        
    d_1=m.addVar(vtype='C', name="d_1")
    d_2=m.addVar(vtype='C', name="d_2")
    d_1_2=m.addVar(vtype='C', name="d_1_2")
    
    m.addConstr(d_1 + d_2 >= contr1)
    m.addConstr(d_2 + d_1_2 >= contr2)
    
    for sommet in sommets_graphe:
        sommet_entrant=0
        sommet_sortant=0
        for s1,s2 in dic_graphe.keys():
            if(s1 == sommet):
                sommet_sortant += var_arcs[(s1,s2)]
            elif(s2 == sommet):
                sommet_entrant += var_arcs[(s1,s2)]
        if(sommet == 'a'):
            m.addConstr(sommet_sortant - sommet_entrant == 1)   
        elif(sommet == 'g'):
            m.addConstr(sommet_sortant - sommet_entrant == -1) 
        else:
            m.addConstr(sommet_sortant - sommet_entrant == 0) 
    
    m.update()
    
    obj = fonction_croyance[0]*d_1 + fonction_croyance[1]*d_2 + fonction_croyance[2]*d_1_2
    m.setObjective(obj,GRB.MINIMIZE)
    
    m.update()
    m.optimize() 
    
    sol={}
    for s1,s2 in dic_graphe.keys():
        sol[(s1,s2)]=var_arcs[(s1,s2)].x
    return sol
    
fonction_croyance = [0.,0.9,1] # d1=0.4, d2=0.5 et d12=1
sol = PL_graphe_choquet(fonction_croyance) 
print(sol)   
    



