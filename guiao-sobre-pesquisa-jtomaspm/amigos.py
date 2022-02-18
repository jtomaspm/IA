from constraintsearch import *

amigos = ["Andre", "Bernardo", "Claudio"]

def constraint(a1, t1, a2, t2):
    b1, c1 = t1
    b2, c2 = t2

    if a1 in t1 or a2 in t2:
        return False

    if b1 == c2 or b2 == c2:
        return False

    if c1 == c2 or b1 == b2:
        return False

    if "Bernardo" in [b1, b2] and ("Bernardo", "Claudio") not in [t1,t2]:
        return False

    return True

cs = ConstraintSearch(
        {A: [(B,C) for B in amigos for C in amigos ] for A in amigos},
        {(A1, A2) : constraint for A1 in amigos for A2 in amigos if A1 != A2}
        )

print(cs.search())
