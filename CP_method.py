from ortools.sat.python import cp_model

def solve(N, m, M, fields):

    model = cp_model.CpModel()

    
    x = {}
    y = {}
    for i in range(N):
        for j in range(fields[i][1], fields[i][2] + 1):
            x[(i, j)] = model.NewIntVar(0, 1, '')
            y[j] = model.NewIntVar(0, 1, '')

    for i in range(N):
        model.Add(sum([x[(i, j)] for j in range(fields[i][1], fields[i][2] + 1)]) <= 1)
        
    for j in range(1, max(e for d, s, e in fields) + 1):
        model.Add(sum([x[(i, j)] * fields[i][0] for i in range(N) if j >= fields[i][1] and j <= fields[i][2]]) <= M * y[j])
        model.Add(sum([x[(i, j)] * fields[i][0] for i in range(N) if j >= fields[i][1] and j <= fields[i][2]]) >= m * y[j])

    objective = sum([x[(i, j)] * fields[i][0] for i in range(N) for j in range(fields[i][1], fields[i][2] + 1)])
    model.Maximize(objective)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)


    if status == cp_model.OPTIMAL:
        print('Total harvested =', int(solver.ObjectiveValue()))
        harvested_fields = [(i+1, j) for i in range(N) for j in range(fields[i][1], fields[i][2] + 1) if solver.Value(x[(i, j)]) > 0]
        print('Num of field(s):',len(harvested_fields))
        days_2=set(x[1] for x in harvested_fields)
        print("Total day(s):",len(days_2))
        # for field, day in harvested_fields:
        #     print(field, day)
    else:
        print('The problem does not have an optimal solution.')

N, m, M = map(int, input().split())
fields = []
for i in range(N):
    d, s, e = map(int, input().split())
    fields.append((d, s, e))
    
# split = lambda x: x.split() # split the line into individual "string" number
# fields=list(map(split, input().splitlines()))  # take the input
# for x in fields:
#     for i in range(3):
#         x[i]=int(x[i]) 
# N,m,M =fields[0]
# fields=fields[1:]      
from timeit import default_timer as timer
start = timer()

solve(N, m, M, fields)

end =  timer()
print(end-start)
