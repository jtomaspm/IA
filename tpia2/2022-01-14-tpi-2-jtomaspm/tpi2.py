#encoding: utf8

from semantic_network import *
from bayes_net import *
from time import time


###########################EX1
class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)
        # IMPLEMENT HERE (if needed)
        pass



    def get_best_from_topic(self, topics):
        #iterate topics to find general best opinion
        res = {}
        for topic in topics.keys():
            topic_declarations = []
            for d in self.declarations:
                if d.relation.entity1 == topic[0] and d.relation.name == topic[1]:
                    topic_declarations.append(d)
            temp_count = {}
            for td in topic_declarations:
                if td.relation.entity2 in temp_count.keys(): 
                    temp_count[td.relation.entity2] += 1
                else:
                    temp_count[td.relation.entity2] = 1
            #get best cases
            best = []
            bestnames = []
            for k in temp_count.keys():
                if not best:
                    best = [k, temp_count[k]]
                    bestnames = [k]
                elif best[1] < temp_count[k]:
                    best = [k, temp_count[k]]
                    bestnames = [k]
                elif best[1] == temp_count[k]:
                    bestnames.append(k)

            #in case of a draw choose user's option
            if topics[topic][0] in bestnames:
                res[topic] = (topics[topic][0], topics[topic][0])
            else:
                res[topic] = (topics[topic][0], best[0])
        return res

                        
    def source_confidence(self,user):
        # IMPLEMENT HERE
        #get user AssocOne's
        du = [d for d in self.declarations if d.user == user and isinstance(d.relation, AssocOne)]
        #populate topics with user's opinion
        topics = {}
        for d in du:
            topics[(d.relation.entity1,d.relation.name)] = (d.relation.entity2, None)
        #populate topics with general opinion
        topics = self.get_best_from_topic(topics)
        correct = 0
        wrong = 0
        #check for correct and wrong answers
        for topic in topics.keys():
            if topics[topic][0] == topics[topic][1]:
                correct += 1
            else:
                wrong += 1
        #confidence formula
        return (1- 0.75**correct)*0.75**wrong
            



###########################EX2
    #confidence formula
    def conf(self, n ,t):
        return (n/(2*t)) + (1 - (n/(2*t)))*(1 - 0.95**n)*0.95**(t-n)


    def query_with_confidence(self, entity, assoc):
        #initial set up
        #direct prodecessors
        direct_prodecessors = [d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        #local results
        local_query = [d.relation.entity2 for d in self.query_local(e1=entity,relname=assoc) if isinstance(d.relation, AssocOne)]
        #recursivly get prodecessor's confidence
        prodecessor_confidence = [self.query_with_confidence(p, assoc) for p in direct_prodecessors]
        #calculate values for n
        n_dict = {e2 :  local_query.count(e2) for e2 in set(local_query)}
        T = len(local_query)
        #calculate confidance for local values
        local_confidance = {}
        if local_query:
            for k,v in n_dict.items():
                local_confidance[k] = self.conf(v, T)

        #get prodecessor entities
        prodecessors = []
        temp = [p.keys() for p in prodecessor_confidence]
        for l in temp:
            prodecessors.extend(l)
        prodecessors = set(prodecessors)

        #calc prodecessor confidance
        prodecessor_confidence_res = {}
        for p in prodecessors:
            r = 0
            for pc in prodecessor_confidence:
                if p in pc:
                    r += pc[p]
            r /= len(prodecessor_confidence)
            prodecessor_confidence_res[p] = r
        #calc result
        res = {}
        if local_confidance and prodecessor_confidence_res:
            for l in local_confidance:
                res[l] = local_confidance[l]*0.9

            for p in prodecessor_confidence_res:
                if p in res:
                    res[p] += prodecessor_confidence_res[p]*0.1
                else:
                    res[p] = prodecessor_confidence_res[p]*0.1
        elif not prodecessor_confidence_res:
            return local_confidance
        else:
            for l in local_confidance:
                res[l] = local_confidance[l]
            for p in prodecessor_confidence_res:
                res[p] = prodecessor_confidence_res[p]*0.9

        return res




        

###########################EX3


        
class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)
        # IMPLEMENT HERE (if needed)
        #known probabilities
        self.known = {}
        pass



    def individualProb(self, var, val):
        variaveis = [ k for k in self.dependencies.keys() if k!=var ]
        res = []
        for c in self.conjunctions(variaveis):
            c = frozenset([(var,val)] + c)
            #if prob is known dont calculate it
            if c in self.known:
                res.append(self.known[c])
            else:
                self.known[c] = self.jointProb(c)
                res.append(self.known[c])

        return sum(res)

    #get all possible conjunctions
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


    def individual_probabilities(self):
        start = time()
        vars = [d for d in self.dependencies]
        res = {}
        for var in vars:
            res[var] = round(self.individualProb(var, True), 3)
        print(time()-start)
        return res 
