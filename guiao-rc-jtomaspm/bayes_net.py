

class BayesNet:

    def __init__(self, ldep=None):  # Why not ldep={}? See footnote 1.
        if not ldep:
            ldep = {}
        self.dependencies = ldep

    # The network data is stored in a dictionary that
    # associates the dependencies to each variable:
    # { v1:deps1, v2:deps2, ... }
    # These dependencies are themselves given
    # by another dictionary that associates conditional
    # probabilities to conjunctions of mother variables:
    # { mothers1:cp1, mothers2:cp2, ... }
    # The conjunctions are frozensets of pairs (mothervar,boolvalue)
    def add(self,var,mothers,prob):
        self.dependencies.setdefault(var,{})[frozenset(mothers)] = prob

    # Joint probability for a given conjunction of
    # all variables of the network
    def jointProb(self,conjunction):
        prob = 1.0
        for (var,val) in conjunction:
            for (mothers,p) in self.dependencies[var].items():
                if mothers.issubset(conjunction):
                    prob*=(p if val else 1-p)
        return prob


# Footnote 1:
# Default arguments are evaluated on function definition,
# not on function evaluation.
# This creates surprising behaviour when the default argument is mutable.
# See:
# http://docs.python-guide.org/en/latest/writing/gotchas/#mutable-default-arguments
    def conjunctions(self, variaveis):
        if len(variaveis) == 1:
            return [
                [(variaveis[0], True)],
                [(variaveis[0], False)]
            ]

        l = []
        for c in self.conjunctions(variaveis[1:]):
            l.append([(variaveis[0], True)] + c)
            l.append([(variaveis[0], False)] + c)

        return l

    def get_conjunctions(self, vars):
        if len(vars) == 1:
            return [(vars[0], True) , (vars[0], False)]
        return [(vars[0], True), (vars[0], False)] + self.get_conjunctions(vars[1:])

    def individualProb(self, var, val):
        variaveis = [v for v in self.dependencies.keys() if v != var] 
        print(self.conjunctions(variaveis))
        conj = [((var,val) , e) for c in self.conjunctions(variaveis) for e in c]
        r= []
        for c in conj:
            print(c)
            if val: 
                l = [c for c in conj if c[1]]
            else:
                l = [c for c in conj if not c[1]]
            for c in l:
                print(c)
            r.append(sum([self.jointProb(c) for c in l]))
        return sum(r)
