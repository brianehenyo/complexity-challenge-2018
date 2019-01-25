import numpy as np
import datetime
import json
from itertools import combinations
from decimal import Decimal

expDir = "experiments/"
date_today = datetime.datetime.now()

per_strat = ("stable", "sticky", "random", "safe", "alwaysnew", "frost", "highroller", "bandwagon", "opportunistic")

wealth_per_strat = dict.fromkeys(per_strat, 0)

class Pool:

    def __init__(self, name, payoff):
        self.in_agents = []
        self.hist_payoff = []
        self.hist_n_agents = []
        self.name = name
        self.payoff = payoff
        self.n_per_strat = dict.fromkeys(per_strat, 0)

    def reset(self):
        self.in_agents = []
        self.n_per_strat = dict.fromkeys(per_strat, 0)

    def addAgent(self, new_agent):
        self.in_agents.append(new_agent)

    def payAgents(self):
        self.hist_n_agents.append(len(self.in_agents))
        # print(self.name + " is paying " + str(len(self.in_agents)) + ", hist -" + str(self.hist_payoff) + " " + str(self.hist_n_agents))
        
        if len(self.in_agents) > 0:
            for a in self.in_agents:
                a.getPayoff(self.payoff)
                self.n_per_strat[a.strat_type] += 1
                wealth_per_strat[a.strat_type] += a.wealth

        self.hist_payoff.append(self.payoff)

    def __str__(self):
        return "This pool has a payoff of {}".format(self.payoff)

class UnstablePool(Pool):

    def __init__(self, name, payoff, p):
        super().__init__(name, payoff)
        self.p = p

    def payAgents(self):
        self.hist_n_agents.append(len(self.in_agents))
        # print(self.name + " is paying " + str(len(self.in_agents)) + ", hist -" + str(self.hist_payoff) + " " + str(self.hist_n_agents))

        curr_payoff = np.random.choice(self.payoff, p=self.p)
        # print(curr_payoff)
        if len(self.in_agents) > 0:
            curr_payoff = round(curr_payoff/len(self.in_agents), 2)
            for a in self.in_agents:
                a.getPayoff(round(curr_payoff, 2))
                self.n_per_strat[a.strat_type] += 1
                wealth_per_strat[a.strat_type] += round(curr_payoff, 2)

        self.hist_payoff.append(round(curr_payoff, 2))

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
        self.my_payoffs.append(round(payoff, 2))
        self.wealth += round(payoff, 2)
        if len(self.my_choices) > 1 and self.my_choices[len(self.my_choices)-1] != self.my_choices[len(self.my_choices)-2]:
            self.wealth -= tau

    def __str__(self):
        return "I'm #{}:{}, have {} = {} and made {} switches".format(self.a_id, self.strat_type, self.my_payoffs, self.wealth, self.my_switches)

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
        if len(self.my_choices) == 0:
            self.chosenPool = np.random.choice(pool_choices)
        elif len(self.my_choices) > 0 and self.wealth > tau:
            new_pool_choices = []
            for pool in pool_choices:
                if pool.name != self.my_choices[len(self.my_choices)-1]:
                    new_pool_choices.append(pool)
            self.chosenPool = np.random.choice(new_pool_choices)
        
        self.chosenPool.addAgent(self)
        if len(self.my_choices)>0 and self.chosenPool.name != self.my_choices[len(self.my_choices)-1]:
            self.my_switches += 1

        self.my_choices.append(self.chosenPool.name)

class RandomAgent(Agent):

    def __init__(self, a_id):
        super().__init__(a_id)
        self.strat_type = "random"
    
    def choosePool(self):
        if len(self.my_choices) == 0 or self.wealth > tau:
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
        elif len(self.my_choices) > 0 and self.wealth > tau:
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
        elif len(self.my_choices) > 0 and self.wealth > tau:
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
        super().__init__(a_id)
        self.strat_type = "bandwagon"
    
    def choosePool(self):
        if len(self.my_choices) == 0:
            self.chosenPool = np.random.choice(pool_choices)
        elif len(self.my_choices) > 0 and self.wealth > tau:
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

class OpportunisticAgent(Agent):

    def __init__(self, a_id):
        super().__init__(a_id)
        self.strat_type = "opportunistic"
    
    def choosePool(self):
        if len(self.my_choices) == 0:
            self.chosenPool = np.random.choice(pool_choices)
        elif len(self.my_choices) > 0 and self.wealth > tau:
            values = []
            i = 1
            for pool in pool_choices:
                values.append((i, np.sum(pool.hist_payoff)/len(pool.hist_payoff), pool.hist_n_agents[len(pool.hist_n_agents)-1]))
                i += 1
            temp_a = np.array(values, dtype=pool_dtype)
            sorted_pools = np.sort(temp_a, order='hist_payoffs')
            self.chosenPool = getPool(sorted_pools[len(sorted_pools)-1][0])
        
        self.chosenPool.addAgent(self)
        if len(self.my_choices)>0 and self.chosenPool.name != self.my_choices[len(self.my_choices)-1]:
            self.my_switches += 1

        self.my_choices.append(self.chosenPool.name)

def runExperiment(n, runs, n_agents, strategy_choices, strategy_p):
    global wealth_per_strat
    repetitions = 5

    # n_per_strat = dict.fromkeys(per_strat, 0)

    # agent_num = 1
    # for i in range(len(strategy_choices)):
    #     for j in range(strategy_p[i]):
    #         new_agent = strategy_choices[i](int(agent_num))
    #         n_per_strat[new_agent.strat_type] += 1
    #         agents.append(new_agent)
    #         agent_num += 1

    # # for i in range(n_agents):
    # #     new_agent = np.random.choice(strategy_choices, p=strategy_p)(int(i))
    # #     n_per_strat[new_agent.strat_type] += 1
    # #     agents.append(new_agent)

    # experiments.append({
    #     "exp_num": n,
    #     "runs": runs,
    #     "n_agents": n_agents,
    #     "n_per_strat": n_per_strat,
    #     "tau": tau
    # })

    for rep in range(repetitions):
        agents = []
        n_per_strat = dict.fromkeys(per_strat, 0)

        print(strategy_choices)

        agent_num = 1
        for i in range(len(strategy_choices)):
            for j in range(strategy_p[i]):
                new_agent = strategy_choices[i](int(agent_num))
                n_per_strat[new_agent.strat_type] += 1
                agents.append(new_agent)
                agent_num += 1

        # for i in range(n_agents):
        #     new_agent = np.random.choice(strategy_choices, p=strategy_p)(int(i))
        #     n_per_strat[new_agent.strat_type] += 1
        #     agents.append(new_agent)

        experiments.append({
            "exp_num": n,
            "rep": rep,
            "runs": runs,
            "n_agents": n_agents,
            "n_per_strat": n_per_strat,
            "tau": tau
        })

        for r in range(runs):
            # All agents choose a pool
            for agent in agents:
                agent.choosePool()
                
            # Pools start payoff
            stable_pool.payAgents()
            low_pool.payAgents()
            high_pool.payAgents()

            # Compute for total wealth in this timestep
            total_wealth = 0
            for agent in agents:
                total_wealth += agent.wealth

            row = {
                "exp_num": int(n),
                "rep": int(rep),
                "timestep": int(r),
                "stable_payoff": int(stable_pool.hist_payoff[len(stable_pool.hist_payoff)-1]),
                "low_payoff": int(low_pool.hist_payoff[len(low_pool.hist_payoff)-1]),
                "high_payoff": int(high_pool.hist_payoff[len(high_pool.hist_payoff)-1]),
                "stable_n_agents": int(stable_pool.hist_n_agents[len(stable_pool.hist_n_agents)-1]),
                "low_n_agents": int(low_pool.hist_n_agents[len(low_pool.hist_n_agents)-1]),
                "high_n_agents": int(high_pool.hist_n_agents[len(high_pool.hist_n_agents)-1]),
                "total_wealth": int(total_wealth)
            }

            for key in n_per_strat.keys():
                row.update({"n_agent_" + str(key) : int(n_per_strat[key])})

            for key in wealth_per_strat.keys():
                row.update({"wealth_" + str(key) : int(wealth_per_strat[key])})

            for key in stable_pool.n_per_strat.keys():
                row.update({"stable_n_" + str(key) : int(stable_pool.n_per_strat[key])})
            
            for key in low_pool.n_per_strat.keys():
                row.update({"low_n_" + str(key) : int(low_pool.n_per_strat[key])})

            for key in high_pool.n_per_strat.keys():
                row.update({"low_n_" + str(key) : int(high_pool.n_per_strat[key])})

            exp_runs.append(row)

            stable_pool.reset()
            low_pool.reset()
            high_pool.reset()
            wealth_per_strat = dict.fromkeys(per_strat, 0)
    
    # saveExperimentsToCSV(n, runs, n_agents, n_per_strat, exp_runs)

# Utility for getting a pool based on index
def getPool(index):
    if index == 1:
        return stable_pool
    elif index == 2:
        return low_pool
    elif index == 3:
        return high_pool

# Save experiment results to CSVs
def saveExperimentsToCSV(exp_num, runs, n_agents, n_per_strat, exp_runs):
    fileName = "runs_" + str(date_today.month) + str(date_today.day) + "-" +str(date_today.hour) + str(date_today.minute) + ".json"

    with open(expDir + fileName, "w+") as jsonFile:
        json.dump(exp_runs, jsonFile)

# Global settings
n_agents = 50
runs = 100
# tau = round(np.random.uniform(0, 10), 2)
tau = 1
experiments = []
exp_runs = []

# Define pools
stable_pool = Pool("stable", 1)
low_pool = UnstablePool("low", [0, 40], [0.50, 0.50])
high_pool = UnstablePool("high", [0, 80], [0.75, 0.25])

pool_choices = [stable_pool, low_pool, high_pool]
pool_dtype = [('pool', int), ('hist_payoffs', int), ('hist_n_agents', int)]

# Experiments
strat_list = [StableAgent, StickyAgent, RandomAgent, AlwaysNewAgent, BandwagonAgent, SafeAgent, FrostAgent, HighRollerAgent, OpportunisticAgent]
experiment_settings = []

# for s in strat_list:
#     experiment_settings.append({"agent_types": [s], "agent_p": [100]})

# combi = combinations(strat_list, 2)
# for c in list(combi):
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [50, 50]})
    # experiment_settings.append({"agent_types": np.array(c), "agent_p": [.25, .75]})
    # experiment_settings.append({"agent_types": np.array(c), "agent_p": [.75, .25]})

# combi = combinations(strat_list, 3)
# for c in list(combi):
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [33, 33, 34]})
    # experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5, .25, .25]})
    # experiment_settings.append({"agent_types": np.array(c), "agent_p": [.25, .5, .25]})
    # experiment_settings.append({"agent_types": np.array(c), "agent_p": [.25, .25, .5]})

# combi = combinations(strat_list, 4)
# for c in list(combi):
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [25, 25, 25, 25]})
    # experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5, .5/3, .5/3, .5/3]})
    # experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/3, .5, .5/3, .5/3]})
    # experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/3, .5/3, .5, .5/3]})
    # experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/3, .5/3, .5/3, .5]})

combi = combinations(strat_list, 5)
for c in list(combi):
    experiment_settings.append({"agent_types": np.array(c), "agent_p": [20, 20, 20, 20, 20]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5, .5/4, .5/4, .5/4, .5/4]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/4, .5, .5/4, .5/4, .5/4]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/4, .5/4, .5, .5/4, .5/4]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/4, .5/4, .5/4, .5, .5/4]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/4, .5/4, .5/4, .5/4, .5]})

# combi = combinations(strat_list, 6)
# for c in list(combi):
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [17, 17, 17, 17, 16, 16]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5, .1, .1, .1, .1, .1]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.1, .5, .1, .1, .1, .1]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.1, .1, .5, .1, .1, .1]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.1, .1, .1, .5, .1, .1]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.1, .1, .1, .1, .5, .1]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.1, .1, .1, .1, .1, .5]})

# combi = combinations(strat_list, 7)
# for c in list(combi):
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [15, 15, 14, 14, 14, 14, 14]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5, .5/6, .5/6, .5/6, .5/6, .5/6, .5/6]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/6, .5, .5/6, .5/6, .5/6, .5/6, .5/6]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/6, .5/6, .5, .5/6, .5/6, .5/6, .5/6]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/6, .5/6, .5/6, .5, .5/6, .5/6, .5/6]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/6, .5/6, .5/6, .5/6, .5, .5/6, .5/6]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/6, .5/6, .5/6, .5/6, .5/6, .5, .5/6]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/6, .5/6, .5/6, .5/6, .5/6, .5/6, .5]})

# combi = combinations(strat_list, 8)
# for c in list(combi):
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [13, 13, 13, 13, 12, 12, 12, 12]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5, .5/7, .5/7, .5/7, .5/7, .5/7, .5/7, .5/7]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/7, .5, .5/7, .5/7, .5/7, .5/7, .5/7, .5/7]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/7, .5/7, .5, .5/7, .5/7, .5/7, .5/7, .5/7]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/7, .5/7, .5/7, .5, .5/7, .5/7, .5/7, .5/7]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/7, .5/7, .5/7, .5/7, .5, .5/7, .5/7, .5/7]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/7, .5/7, .5/7, .5/7, .5/7, .5, .5/7, .5/7]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/7, .5/7, .5/7, .5/7, .5/7, .5/7, .5, .5/7]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/7, .5/7, .5/7, .5/7, .5/7, .5/7, .5/7, .5]})

# combi = combinations(strat_list, 9)
# for c in list(combi):
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [12, 11, 11, 11, 11, 11, 11, 11, 11]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5, .5/8, .5/8, .5/8, .5/8, .5/8, .5/8, .5/8, .5/8]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/8, .5, .5/8, .5/8, .5/8, .5/8, .5/8, .5/8, .5/8]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/8, .5/8, .5, .5/8, .5/8, .5/8, .5/8, .5/8, .5/8]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/8, .5/8, .5/8, .5, .5/8, .5/8, .5/8, .5/8, .5/8]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/8, .5/8, .5/8, .5/8, .5, .5/8, .5/8, .5/8, .5/8]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/8, .5/8, .5/8, .5/8, .5/8, .5, .5/8, .5/8, .5/8]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/8, .5/8, .5/8, .5/8, .5/8, .5/8, .5, .5/8, .5/8]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/8, .5/8, .5/8, .5/8, .5/8, .5/8, .5/8, .5, .5/8]})
#     experiment_settings.append({"agent_types": np.array(c), "agent_p": [.5/8, .5/8, .5/8, .5/8, .5/8, .5/8, .5/8, .5/8, .5]})

exp_num = 1
for exp in experiment_settings:
    runExperiment(exp_num, runs, n_agents, exp["agent_types"], exp["agent_p"])
    exp_num += 1

expListFileName = "experiments_" + str(date_today.month) + str(date_today.day) + "-" +str(date_today.hour) + str(date_today.minute) + ".json"
with open(expDir + expListFileName, "w+") as jsonFile:
    json.dump(experiments, jsonFile)

runsFileName = "runs_" + str(date_today.month) + str(date_today.day) + "-" +str(date_today.hour) + str(date_today.minute) + ".json"

with open(expDir + runsFileName, "w+") as jsonFile:
    json.dump(exp_runs, jsonFile)