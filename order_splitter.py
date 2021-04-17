import numpy as np
from scipy.optimize import linprog
def split_order(order_qty, suppliers):
    n=len(suppliers)
    c=[s["unit_cost"]+s["shipping"]/max(1,order_qty) for s in suppliers]
    A_ub=[]; b_ub=[]
    for i,s in enumerate(suppliers):
        row=[0]*n; row[i]=1; A_ub.append(row); b_ub.append(s["capacity"])
        row2=[0]*n; row2[i]=-1; A_ub.append(row2); b_ub.append(-s.get("min_order",0))
    A_eq=[[1]*n]; b_eq=[order_qty]
    bounds=[(0,s["capacity"]) for s in suppliers]
    res=linprog(c,A_ub=A_ub,b_ub=b_ub,A_eq=A_eq,b_eq=b_eq,bounds=bounds,method='highs')
    if res.success:
        alloc={suppliers[i]["name"]:round(res.x[i]) for i in range(n)}
        return {"allocation":alloc,"total_cost":round(res.fun,2)}
    return {"error":"infeasible"}
if __name__=="__main__":
    suppliers=[{"name":"S1","unit_cost":10,"shipping":200,"capacity":600,"min_order":100},
               {"name":"S2","unit_cost":12,"shipping":100,"capacity":400,"min_order":50},
               {"name":"S3","unit_cost":9,"shipping":350,"capacity":500,"min_order":200}]
    print(split_order(800,suppliers))
