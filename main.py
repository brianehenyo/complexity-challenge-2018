import pandas as pd
import numpy as np

class Pool:

    def __init__(self, name, payoff):
        self.in_agents = []
        self.hist_payoff = []
        self.hist_n_agents = []
        self.name = name
        self.payoff = payoff

    def addAgent(self, new_agent):
        self.in_agents.append(new_agent)

    def payAgents(self):
        self.hist_n_agents.append(len(self.in_agents))
        print(self.name + " is paying " + str(len(self.in_agents)) + ", hist -" + str(self.hist_payoff) + " " + str(self.hist_n_agents))
        
        if len(self.in_agents)>0:
            for a in self.in_agents:
                a.getPayoff(self.payoff)
                print(a)

        self.hist_payoff.append(self.payoff)
        self.in_agents = []

    def __str__(self):
        return "This pool has a payoff of {}".format(self.payoff)

class UnstablePool(Pool):

    def __init__(self, name, payoff, p):
        self.in_agents = []
        self.hist_payoff = []
        self.hist_n_agents = []
        self.name = name
        self.payoff = payoff
        self.p = p

    def payAgents(self):
        self.hist_n_agents.append(len(self.in_agents))
        print(self.name + " is paying " + str(len(self.in_agents)) + ", hist -" + str(self.hist_payoff) + " " + str(self.hist_n_agents))

        curr_payoff = np.random.choice(self.payoff, p=self.p)
        print(curr_payoff)
        if len(self.in_agents)>0:
            curr_payoff = int(curr_payoff/len(self.in_agents))
            for a in self.in_agents:
                a.getPayoff(curr_payoff)
                print(a)

        self.hist_payoff.append(curr_payoff)
        self.in_agents = []

# Parent Agent class
class Agent:

    def __init__(self, a_id):
        self.my_payoffs = []
        self.my_choices = []
        self.my_switches = 0
        self.strat_type = "parent"
        self.a_id = a_id
        self.wealth = 0

    def getPayoff(self, payoff):
        self.my_payoffs.append(payoff)

    def __str__(self):
        return "I'm #{}:{}, have {} and made {} switches".format(self.a_id, self.strat_type, self.my_payoffs, self.my_switches)

# Agent Strategies
class StableAgent(Agent):

    def __init__(self, a_id):
        super().__init__(a_id)
        self.strat_type = "stable"
    
    def choosePool(self):
        self.chosenPool = stable_pool
        self.chosenPool.addAgent(self)
        self.my_choices.append(self.chosenPool.name)

class SafeAgent(Agent):

    def __init__(self, a_id):
        super().__init__(a_id)
        self.strat_type = "safe"
    
    def choosePool(self):
        if len(self.my_choices) == 0:
            self.chosenPool = np.random.choice(pool_choices)
        else:
            values = []
            i = 1
            for pool in pool_choices:
                if pool.hist_payoff[len(pool.hist_payoff)-1]>0:
                    values.append((i, pool.hist_payoff[len(pool.hist_payoff)-1], pool.hist_n_agents[len(pool.hist_n_agents)-1]))
                i += 1
            temp_a = np.array(values, dtype=pool_dtype)
            sorted_pools = np.sort(temp_a, order='hist_n_agents')
            self.chosenPool = getPool(sorted_pools[len(sorted_pools)-1][0])
        
        self.chosenPool.addAgent(self)
        if len(self.my_choices)>0 and self.chosenPool.name != self.my_choices[len(self.my_choices)-1]:
            self.my_switches += 1

        self.my_choices.append(self.chosenPool.name)

class StickyAgent(Agent):

    def __init__(self, a_id):
        super().__init__(a_id)
        self.strat_type = "sticky"
    
    def choosePool(self):
        if len(self.my_choices) == 0:
            self.chosenPool = np.random.choice(pool_choices)
        self.chosenPool.addAgent(self)
        self.my_choices.append(self.chosenPool.name)

class AlwaysNewAgent(Agent):

    def __init__(self, a_id):
        super().__init__(a_id)
        self.strat_type = "alwaysnew"
    
    def choosePool(self):
        new_pool_choices = []
        for pool in pool_choices:
            if len(self.my_choices)>0 and pool.name != self.my_choices[len(self.my_choices)-1]:
                new_pool_choices.append(pool)
                self.chosenPool = np.random.choice(new_pool_choices)
            else:
                self.chosenPool = np.random.choice(pool_choices)
        
        self.chosenPool.addAgent(self)
        if len(self.my_choices)>0 and self.chosenPool.name != self.my_choices[len(self.my_choices)-1]:
            self.my_switches += 1

        self.my_choices.append(self.chosenPool.name)

class RandomAgent(Agent):

    def __init__(self, a_id):
        super().__init__(a_id)
        self.strat_type = "random"
    
    def choosePool(self):
        self.chosenPool = np.random.choice(pool_choices)
        self.chosenPool.addAgent(self)
        if len(self.my_choices)>0 and self.chosenPool.name != self.my_choices[len(self.my_choices)-1]:
            self.my_switches += 1

        self.my_choices.append(self.chosenPool.name)

class FrostAgent(Agent):

    def __init__(self, a_id):
        super().__init__(a_id)
        self.strat_type = "frost"
    
    def choosePool(self):
        if len(self.my_choices) == 0:
            self.chosenPool = np.random.choice(pool_choices)
        else:
            values = []
            i = 1
            for pool in pool_choices:
                values.append((i, pool.hist_payoff[len(pool.hist_payoff)-1], int(np.sum(pool.hist_n_agents)/len(pool.hist_n_agents))))
                i += 1
            temp_a = np.array(values, dtype=pool_dtype)
            sorted_pools = np.sort(temp_a, order=['hist_n_agents', 'hist_payoffs'])
            self.chosenPool = getPool(sorted_pools[0][0])
        
        self.chosenPool.addAgent(self)
        if len(self.my_choices)>0 and self.chosenPool.name != self.my_choices[len(self.my_choices)-1]:
            self.my_switches += 1

        self.my_choices.append(self.chosenPool.name)

class HighRollerAgent(Agent):

    def __init__(self, a_id):
        super().__init__(a_id)
        self.strat_type = "highroller"
    
    def choosePool(self):
        if len(self.my_choices) == 0:
            self.chosenPool = np.random.choice(pool_choices)
        else:
            values = []
            i = 1
            for pool in pool_choices:
                values.append((i, pool.hist_payoff[len(pool.hist_payoff)-1], pool.hist_n_agents[len(pool.hist_n_agents)-1]))
                i += 1
            temp_a = np.array(values, dtype=pool_dtype)
            sorted_pools = np.sort(temp_a, order='hist_payoffs')
            self.chosenPool = getPool(sorted_pools[len(sorted_pools)-1][0])
        
        self.chosenPool.addAgent(self)
        if len(self.my_choices)>0 and self.chosenPool.name != self.my_choices[len(self.my_choices)-1]:
            self.my_switches += 1

        self.my_choices.append(self.chosenPool.name)

class BandwagonAgent(Agent):

    def __init__(self, a_id):
        self.my_payoffs = []
        self.my_choices = []
        self.my_switches = 0
        self.strat_type = "bandwagon"
        self.a_id = a_id
    
    def choosePool(self):
        if len(self.my_choices) == 0:
            self.chosenPool = np.random.choice(pool_choices)
        else:
            values = []
            i = 1
            for pool in pool_choices:
                values.append((i, pool.hist_payoff[len(pool.hist_payoff)-1], pool.hist_n_agents[len(pool.hist_n_agents)-1]))
                i += 1
            temp_a = np.array(values, dtype=pool_dtype)
            sorted_pools = np.sort(temp_a, order='hist_n_agents')
            self.chosenPool = getPool(sorted_pools[len(sorted_pools)-1][0])
        
        self.chosenPool.addAgent(self)
        if len(self.my_choices)>0 and self.chosenPool.name != self.my_choices[len(self.my_choices)-1]:
            self.my_switches += 1

        self.my_choices.append(self.chosenPool.name)

def runExperiment(runs, n_agents, strategy_choices, strategy_p):
    agents = []

    n_per_strat = {
        "stable" : 0,
        "sticky" : 0,
        "random" : 0,
        "safe" : 0,
        "alwaysnew": 0,
        "frost": 0,
        "highroller": 0,
        "bandwagon": 0
    }

    for i in range(n_agents):
        new_agent = np.random.choice(strategy_choices, p=strategy_p)(int(i))
        n_per_strat[new_agent.strat_type] += 1
        agents.append(new_agent)

    print(n_per_strat)

    for r in range(runs):
        # All agents choose a pool
        for agent in agents:
            agent.choosePool()
            
        # Pools start payoff
        stable_pool.payAgents()
        low_pool.payAgents()
        high_pool.payAgents()

def getPool(index):
    if index == 1:
        return stable_pool
    elif index == 2:
        return low_pool
    elif index == 3:
        return high_pool

# Global settings
tau = np.random.uniform(0, 1)

# Define pools
stable_pool = Pool("stable", 1)
low_pool = UnstablePool("low", [0, int(40)], [0.50, 0.50])
high_pool = UnstablePool("high", [0, 80], [0.75, 0.25])

pool_choices = [stable_pool, low_pool, high_pool]
pool_dtype = [('pool', int), ('hist_payoffs', int), ('hist_n_agents', int)]

# Experiments
runExperiment(3, 50, [FrostAgent, StickyAgent], [.05, .95])