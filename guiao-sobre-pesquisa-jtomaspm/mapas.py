from constraintsearch import *

region = ['A', 'B', 'C', 'D', 'E']
colors = ['red', 'blue', 'green', 'yellow', 'white']

mapa = {
    'A' : "BED",
    'B' : "AEC",
    'C' : "BED",
    'D' : "AEC",
    'E' : "ABCD"
        }

def constraint(r1,c1,r2,c2):
    return c1 != c2

cs = ConstraintSearch(
        {R : colors for R in region},
        {(R1,R2): constraint for R1 in region for R2 in mapa[R1]}
        )


print({(R1,R2): constraint for R1 in region for R2 in mapa[R1]})
print(cs.search())
