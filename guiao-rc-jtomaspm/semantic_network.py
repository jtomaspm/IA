

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

from typing import SupportsBytes


class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __eq__(self, r) -> bool:
        return self.entity1 == r.entity1 and self.name == r.name and self.entity2 == r.entity2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)
    def __hash__(self) -> int:
        return hash(str(self))


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse AssocOne
class AssocOne(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

# Subclasse AssocNum
class AssocNum(Relation):
    def __init__(self,e1,assoc,e2):
        try:
            e2 = float(e2)
            Relation.__init__(self,e1,assoc,e2)
        except ValueError:
            return None

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)
    def __eq__(self, d) -> bool:
        return self.relation == d.relation and self.user == d.user
    def __hash__(self) -> int:
        return hash(str(self))
#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None,rel_type=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) 
                and (rel_type == None or isinstance(d.relation, rel_type)) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    def list_associations(self):
        return set([d.relation.name for d in self.declarations if isinstance(d.relation, Association)])

    def list_objects(self):
        return set([d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member)])
    
    def list_users(self):
        return set([d.user for d in self.declarations])
    
    def list_types(self):
        return set([d.relation.entity2 for d in self.declarations if isinstance(d.relation, Subtype)] + [d.relation.entity2 for d in self.declarations if isinstance(d.relation, Member)])

    def list_local_associations(self, e):
        return set([d.relation.name for d in self.declarations if isinstance(d.relation, Association) and (d.relation.entity1 == e or d.relation.entity2 == e)])
    
    def list_relations_by_user(self, user):
        return set([d.relation.name for d in self.declarations if user == d.user])

    def associations_by_user(self, user):
        return len(set([d.relation.name for d in self.declarations if user == d.user and isinstance(d.relation, Association)]))
    
    def list_local_associations_by_user(self, e):
        return set([(d.relation.name, d.user) for d in self.declarations if isinstance(d.relation, Association) and (d.relation.entity1 == e or d.relation.entity2 == e)])
    
    def predecessor(self, a, b):
        dp = [d.relation for d in self.declarations if (isinstance(d.relation, Subtype) or isinstance(d.relation, Member)) and b == d.relation.entity1]

        if [d for d in dp if a == d.entity2] != []:
            return True
        
        
        return any([self.predecessor(a, d.entity2) for d in dp])

    def predecessor_path(self, a, b):
        dp = [d.relation for d in self.declarations if (isinstance(d.relation, Subtype) or isinstance(d.relation, Member)) and b == d.relation.entity1]

        if [d for d in dp if a == d.entity2] != []:
            return [a, b]
        
        
        for d in dp:
            path = self.predecessor_path(a, d.entity2)

            if path != []:
                return path + [b]
        
        return None
    
    def query(self, entity, rel=None):
        # Find direct predecessors of entity and foreach one make query for Association
        predecessorsQueries = [self.query(d.relation.entity2, rel) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        # Transform list of lists of declarations in list of declarations
        predecessorsQuery = [declaration for listOfQueries in predecessorsQueries for declaration in listOfQueries]

        # Make local query for Association
        localQuery = self.query_local(e1=entity, rel=rel, rel_type=Association)

        return localQuery + predecessorsQuery
    
    def query2(self, entity, rel=None):
        query = self.query(entity, rel)
        q2 = self.query_local(e1=entity, rel=rel, rel_type=(Member, Subtype))
        return query + q2
    
    def query_cancel(self, entity, rel=None):
        predecessors = [d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]

        return [d for d in self.declarations if isinstance(d.relation, Association) and d.relation.entity1 in predecessors and (rel == None or d.relation.name == rel)]
    
    def query_down(self, entity, rel=None, first=True):
        predecessorsQueries = [self.query_down(d.relation.entity1, rel, False) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity2 == entity]
        
        predecessorsQuery = [declaration for listOfQueries in predecessorsQueries for declaration in listOfQueries]

        
        localQuery = self.query_local(e1=entity, rel=rel, rel_type=Association) if not first else []

        return localQuery + predecessorsQuery

    def query_induce(self, entity, rel=None):
        qd = self.query_down(entity, rel)
        
        freq = {}
        for d in qd:
            if d.relation.name in freq.keys() and freq[d.relation.name] < d.relation.entity2:
                freq[d.relation.name] = d.relation.entity2
            else:
                freq[d.relation.name] = d.relation.entity2
        
        return freq[max(freq, key=freq.get)]
    
    def query_local_assoc(self, e1, rel):
        freq_assoc = {}
        count = 0
        
        for d in [d for d in self.declarations if isinstance(d.relation, Association) and d.relation.entity1 == e1 and d.relation.name == rel]:
       
            if freq_assoc != {} and sum([val for val in freq_assoc.values()])/count < 0.75:
                break

            count += 1
            if d.relation.entity2 in freq_assoc.keys():
                freq_assoc[d.relation.entity2] = freq_assoc[d.relation.entity2] + 1
            else:
                freq_assoc[d.relation.entity2] = 1
            
        if count != 0:
            freq = [(f, freq_assoc[f]/count) for f in freq_assoc.keys()]
            return [x for i, x in enumerate(freq) if x[1] == max(freq, key=lambda x:x[1])[1]]
        


        freq_assoc = {}
        count = 0
        
        for d in [d for d in self.declarations if isinstance(d.relation, AssocOne) and d.relation.entity1 == e1 and d.relation.name == rel]:
            count += 1
            if d.relation.entity2 in freq_assoc.keys():
                freq_assoc[d.relation.entity2] = freq_assoc[d.relation.entity2] + 1
            else:
                freq_assoc[d.relation.entity2] = 1
            
        if count != 0:
            freq = [(f, freq_assoc[f]/count) for f in freq_assoc.keys()]
            return max(freq, key=lambda x:x[1])
        


        freq_assoc = {}
        count = 0
        
        for d in [d for d in self.declarations if isinstance(d.relation, AssocNum) and d.relation.entity1 == e1 and d.relation.name == rel]:
            count += 1
            if d.relation.entity2 in freq_assoc.keys():
                freq_assoc[d.relation.entity2] = freq_assoc[d.relation.entity2] + 1
            else:
                freq_assoc[d.relation.entity2] = 1
            
        if count != 0:
            return sum(freq_assoc.keys())/len(freq_assoc.values())
        

    def query_assoc_value(self, e1, rel):
        locals = self.query_local(e1=e1, rel=rel, rel_type=(Association, AssocNum, AssocOne))
        locals_values = [d.relation.entity2 for d in locals]

        if len(set(locals_values)) == 1:
            return locals_values[0]


        predecessors = self.query(e1, rel)
        predecessors = [p for p in predecessors if p not in locals]
        predecessors_values = [p.relation.entity2 for p in predecessors]
        
        def percentage(lst, v):
            if lst == []:
                return 0
            return len([l for l in lst if l == v])/(len(lst))
        

        return max(locals_values + predecessors_values, key=lambda v: (percentage(locals_values, v) + percentage(predecessors_values, v))/2)