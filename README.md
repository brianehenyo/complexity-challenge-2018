# Complexity Challenge 2018
by [Briane Paul Samson](https://brianesamson.com)

This is my submission for [Complexity Explorer](https://www.complexityexplorer.org/)'s Complexity Challenge 2018.

## Agent Strategies
For this challenge, I created 9 agent strategies, grouped into 3 categories. 

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

## Environment Setup and Experiments
For my challenge solution, each experiment has 100 agents and run for 100 timesteps. Because there is randomness in the behavior of some agent strategies, each experiment is repeated 5 times and the average total wealth is used for analysis.

Since there are 9 different agent strategies, I played around with different combinations. Aside from running experiments where all agents follow the same strategy, I also run experiments that had 2 to 9 combinations of strategies deployed, with equal distributions. For example, there are experiments with 50-50 random and safe agents, and 33-33-34 random, sticky and safe agents. Overall, there are 511 experiments and in the following sections, we will look at some of the significant behaviors that emerged.

## Results & Analysis

### General Behaviors

**Table 1.** Average Total Wealth of Experiments with Only 1 Strategy.
| Strategy      | Average Total Wealth |
|------------|-------------------|
| stable        |            10,000.00 |
| safe          |             9,662.40 |
| sticky        |             7,328.60 | 
| bandwagon     |             5,287.40 | 
| opportunistic |            1,139.40  |
| random        |            1,015.60  |
| highroller    |              348.80  |
| alwaysnew     |              167.20  |
| frost         |              140.40  |


| Priority apples | Second priority | Third priority |
|-------|--------|---------|
| ambrosia | gala | red delicious |
| pink lady | jazz | macintosh |
| honeycrisp | granny smith | fuji |


### Wealth Over Time


### Influence of Diversity of Strategies

Are there generally classes of agent behavior (say, based on what data they use, how they process it, or the agent's overall sophistication) that lead to better performance?
