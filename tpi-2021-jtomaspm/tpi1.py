from tree_search import *
from cidades import *

class MyNode(SearchNode):
    def __init__(self,state,parent,arg3=None,arg4=None,arg5=None):
        super().__init__(state,parent)
        self.cost = 0
        self.heuristic = 0

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',seed=0): 
        super().__init__(problem,strategy,seed)
        root = MyNode(problem.initial, None)
        self.all_nodes = [root]
        self.solution_tree = None

    def astar_add_to_open(self,lnewnodes):
        #IMPLEMENT HERE
        #cost + heuristic

        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key=lambda node_ID: self.all_nodes[node_ID].heuristic + self.all_nodes[node_ID].cost)


    def propagate_eval_upwards(self,node):
        #IMPLEMENT HERE
        pass

    def search2(self,atmostonce=False):
        #IMPLEMENT HERE
        while self.open_nodes != []:
            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes)+1
                return self.get_path(node)
            lnewnodes = []
            self.non_terminals += 1
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    newnode = MyNode(newstate,nodeID)
                    newnode.cost = self.problem.domain.cost(node.state, a) + node.cost
                    newnode.heuristic = self.problem.domain.heuristic(newstate, self.problem.goal)
                    self.all_nodes.append(newnode)
                    lnewnodes.append(len(self.all_nodes)-1)
            if self.strategy == 'rand_depth':
                self.add_to_open(lnewnodes)    
            else:
                self.astar_add_to_open(lnewnodes)

        return None

    def update_solution_tree(self):
        if self.solution_tree == None:
            self.solution_tree = MyTree(self.problem, self.strategy, self.curr_pseudo_rand_number)
        self.solution_tree.all_nodes = self.all_nodes
        self.solution_tree.terminals = self.terminals
        self.solution_tree.non_terminals = self.non_terminals
        self.solution_tree.open_nodes = self.open_nodes
        self.solution_tree.solution = self.solution


    def repeated_random_depth(self,numattempts=3,atmostonce=False):
        #IMPLEMENT HERE
        #returns the path for the best result
        #implementar limit 
        #correr search n vezes c 
        #guardar e retornar a melhor arvore
    
        trees = None
        costs = None
        
        for i in range(numattempts):
            self.open_nodes = [0]
            self.all_nodes = [MyNode(self.problem.initial, None)]
            self.non_terminals = 0
            temp = self.search2()
            if costs == None:
                costs = self.solution.cost
                trees = temp
                self.update_solution_tree()

            elif self.solution.cost < costs:
                trees = temp
                costs = self.solution.cost
                self.update_solution_tree()

                
        
        return trees 
            
        

        

        

    def make_shortcuts(self):
        #IMPLEMENT HERE
        pass



class MyCities(Cidades):
    def __init__(self, connections, coordinates):
        super().__init__(connections, coordinates)

    def maximum_tree_size(self,depth):   # assuming there is no loop prevention
        #IMPLEMENT HERE
        count = 0
        for city in self.coordinates:
            for conn in self.connections:
                if city in conn:
                    count += 1

        avg_neighbors = count / len(self.coordinates.keys())
        count = 0
        for n in range(depth+1):
            count += avg_neighbors**n
        return count
        


