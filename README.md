# Complexity Challenge 2018
by [Briane Paul Samson](https://brianesamson.com)

This is my submission for [Complexity Explorer's](https://www.complexityexplorer.org/) Complexity Challenge 2018.

## Agent Strategies

**No Heuristics**
- Stable - Always on the stable pool. Risk averse
- Sticky - Stay in the same pool as the initial
- Random - Doesn’t look at prior payoffs
- Always new - Always change pool

**Looks at the # of agents**
- Bandwagon - Always choose a pool that has the most number of agents in the previous time step
- Safe - Always choose a pool that had the most agents with payoffs in the previous time step
- Robert Frost - Always choose the least chosen pool (based on average number of agents that have previously chosen it)

**Looks at payoffs**
- High Roller - Always choose a pool with the highest payoff in the previous time step
- Opportunistic - Always choose a pool with the highest average payoff

## Analysis
- What general behaviors arise in the system? 
- How does the wealth of the agents change over time? 
- How does the diversity of strategies influence the dynamics of the system?
- Are there generally classes of agent behavior (say, based on what data they use, how they process it, or the agent's overall sophistication) that lead to better performance?
