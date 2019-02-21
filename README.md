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
- Robert Frost - Always choose the least chosen pool (based on average number of agents that have previously chosen it). Inspired by the poem _The Road not Taken_, hence the name.

**Looks at payoffs**
- High Roller - Always choose a pool with the highest payoff in the previous time step
- Opportunistic - Always choose a pool with the highest average payoff

## Environment Setup and Experiments
For my challenge solution, each experiment has 100 agents and run for 100 timesteps. Because there is randomness in the behavior of some agent strategies, each experiment is repeated 5 times (trials) and the average total wealth is used for analysis.

Since there are 9 different agent strategies, I played around with different combinations. Aside from running experiments where all agents follow the same strategy, I also run experiments that had 2 to 9 combinations of strategies deployed, with equal distributions. For example, there are experiments with 50-50 random and safe agents, and 33-33-34 random, sticky and safe agents. Overall, there are 511 experiments and in the following sections, we will look at some of the significant behaviors that emerged.

## Results & Analysis

### General Behaviors

**Table 1.** Average total wealth of experiments with only 1 strategy.

| Strategy      | Average Total Wealth |
| :------------ | -------------------: |
| stable        |            10,000.00 |
| safe          |             9,662.40 |
| sticky        |             7,328.60 | 
| bandwagon     |             5,287.40 | 
| opportunistic |             1,139.40 |
| random        |             1,015.60 |
| highroller    |               348.80 |
| alwaysnew     |               167.20 |
| frost         |               140.40 |

**High Wealth**

From Table 1, we can see that the experiment with 100 **stable** agents got the highest average total wealth because none of the agents were changing pools. The next highest are the **safe** agents mainly because all of them eventually stayed in the _stable_ pool after some timestep, causing no more transfers. **Sticky** agents also got a high average total wealth because they weren't moving pools at all. So even though some of them might not get payoffs on some timesteps, the total wealth never dipped because they stayed on the same pool since the beginning. And although the **bandwagon** agents have high tendencies of moving, only a few of them transfer pools at one time.

**Low Wealth**
The lowest total wealth among the strategies was from the **frost** agents because large numbers of agents move at a time, hence the large drop and almost zero wealth. The **alwaysnew** agents also had very low total wealth because all agents move for all timesteps. 

### Wealth Over Time

![alt text][1combi]

**Figure 1.** Average total wealth over time of experiments with only 1 strategy.

### Influence of Diversity of Strategies

Are there generally classes of agent behavior (say, based on what data they use, how they process it, or the agent's overall sophistication) that lead to better performance?

<!-- Images -->
[1combi]: /outputs/total_wealth_1-combi.png "Total wealth over time for experiments with agents that use 1 strategy."
[2combi]: /outputs/total_wealth_2-combi.png "Total wealth over time for experiments with 2 different agent strategies."
[3combi]: /outputs/total_wealth_3-combi.png "Total wealth over time for experiments with 3 different agent strategies."
[4combi]: /outputs/total_wealth_4-combi.png "Total wealth over time for experiments with 4 different agent strategies."
[5combi]: /outputs/total_wealth_5-combi.png "Total wealth over time for experiments with 5 different agent strategies."
[6combi]: /outputs/total_wealth_6-combi.png "Total wealth over time for experiments with 6 different agent strategies."
[7combi]: /outputs/total_wealth_7-combi.png "Total wealth over time for experiments with 7 different agent strategies."
[8combi]: /outputs/total_wealth_8-combi.png "Total wealth over time for experiments with 8 different agent strategies."
[9combi]: /outputs/total_wealth_9-combi.png "Total wealth over time for experiments with 9 different agent strategies."