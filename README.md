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
- Frost - Always choose the least chosen pool (based on average number of agents that have previously chosen it). Inspired by the poem _The Road not Taken_, hence the name.

**Looks at payoffs**
- High Roller - Always choose a pool with the highest payoff in the previous time step
- Opportunistic - Always choose a pool with the highest average payoff

## Environment Setup and Experiments
For my challenge solution, each experiment has 100 agents and run for 100 timesteps. Because there is randomness in the behavior of some agent strategies, each experiment is repeated 5 times (trials) and the average total wealth is used for analysis.

There are 3 pools: _stable_, _low_ and _high_. The _stable_ pool always give a payoff of 1 to all agents in it. The _low_ pool gives a payoff of 0 or 40 with equal probabilities. The _high_ pool has 75% chance of giving 0 payoff and 25% of giving 80 payoffs. Both _low_ and _high_ pools divide the payoff among the agents in them. If agents transfer pools, _tau_ is deducted from their wealth, which has a value of 1. All agents cannot know the wealth of other agents and where they will go next.

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

From _Table 1_, we can see that the experiment with 100 `stable` agents got the highest average total wealth because none of the agents were changing pools. The next highest are the `safe` agents mainly because all of them eventually stayed in the _stable_ pool after some timestep, causing no more transfers. `Sticky` agents also got a high average total wealth because they weren't moving pools at all. So even though some of them might not get payoffs on some timesteps, the total wealth never dipped because they stayed on the same pool since the beginning. And although the `bandwagon` agents have high tendencies of moving, only a few of them transfer pools at one time.

**Low Wealth**

The lowest total wealth among the strategies was from the `frost` agents because large numbers of agents move at a time, hence the large drop and almost zero wealth. The `alwaysnew` agents also had very low total wealth because all agents move every timestep. `Random` agents fared relatively better because they might not move at all, reducing _tau_ deductions. `Highroller` agents also had low wealth because they are easily attracted to pools that give high payoffs in the previous timestep. In that case, they have a tendency to move often even though they aren't getting the payoff they expected from their choices (i.e. moving to a pool that previously paid 10 but gave 0 in the current timestep). `Opportunistic` agents almost behave the same but they have the advantage of better hindsight. These agents wouldn't easily go to a pool that previously gave a high payoff because of a low average payoff.

### Wealth Over Time

![alt text][1combi]

**Figure 1.** Average total wealth over time of experiments with only 1 strategy.

From _Figure 1_, we can see that the experiments with pure `stable`, `sticky`, `safe` and `bandwagon` agents had a steady increase in total wealth over time, with no dips. The all-`random` and all-`opportunistic` agent experiments show very minimal increases in total wealth over time. Although the `highroller`, `alwasynew` and `frost` agents had momentary increases in wealth at a hadnful of timesteps, they never really sustained an upward trend. From the figure, we can even see them having slow and steady decreases in weatlh over time.

### Influence of Diversity of Strategies

![alt text][dist]

**Figure 2.** Distribution of average total wealth from experiments with at least 2 strategies.

As mentioned, I played around with different combinations of agent strategies. I will use the highest average total wealth from the 1-strategy experiments as basis of comparison. We can say that a combination performed well if they had an average total wealth above 10,000. 

_Figure 2_ shows the Gaussian distribution of the average total wealth. Most of the combinations had average total wealth between 2,379 to 8,379. In the following sections, I will discuss which groups of agent strategies contributed to the high and low average total wealth from the experiments.

#### Best Performers

**Table 2.** The best performing combinations compared to the average total wealth of the all-stable experiment.

| Best Performing Combinations                      | Average Total Wealth |
| :------------------------------------------------ | -------------------: |
| sticky & safe                                     |            11,184.00 |
| stable & sticky                                   |            10,481.00 |
| stable, sticky & bandwagon                        | 	         12,062.40 |
| stable, sticky & safe                             |  	         11,616.60 | 
| sticky, safe & bandwagon                          | 	         10,376.00 | 
| stable, safe & bandwagon                          | 	         10,007.20 | 
| stable, sticky, safe & bandwagon                  | 	         11,683.60 | 
| stable, random, safe & bandwagon                  | 	         10,445.20 | 
| stable, safe, alwaysnew & bandwagon               | 	         10,013.80 | 
| stable, sticky, safe, bandwagon & opportunistic   | 	         11,010.80 | 
| stable, sticky, safe, highroller & bandwagon      | 	         10,161.20 | 
| stable, sticky, safe, frost & bandwagon           | 	         10,105.80 | 

Out of the 502 experiments with more than 1 agent strategy involved, only 12 combinations had an average total wealth over 10,000. Certainly, the presence of risk-averse agents like `stable`, `safe` and `sticky` are keeping the total wealth high which gives risk-taking agent strategies enough leg room to gamble with higher payoffs. However, this is only true if they are majority of the agents in the experiment. If we look at _Table 2_ for example, even though the combination `stable, sticky, safe, frost & bandwagon` has the worst performer `frost` agents, they still managed to amass a lot of wealth because the `frost` agents never had a chance to drag everyone and cause dips in total wealth value. 5,703 is the lowest average total wealth when majority of the agent strategies are from those three.

#### Worst Performers

**Table 3.** The worst performing combinations compared to the average total wealth of the all-stable experiment.

| Worst Performing Combinations                     | Average Total Wealth |
| :------------------------------------------------ | -------------------: |
| random & alwaysnew                                |               805.00 |
| alwaysnew & highroller                            |               379.00 |
| random, alwaysnew & highroller                    | 	            706.00 |

At the bottom of the rankings (_Table 3_), combinations with majority of `random`, `alwaysnew` and `highroller` agents usually yield low average total wealth. This is mainly due to their randomness and high attraction to good immediate past payoffs. We can say that they represent a sample of the population who are less pragmatic and impulsive.

#### Balanced Wildcards

After looking at all the experiments, I noticed that the `bandwagon` and `opportunistic` strategies amplifies the effect of the best and worst performing combinations of agent strategies. For example, 9 out of 12 best performing combinations had `bandwagon` agents along with best performing `stable`, `safe` and `sticky` agents. If they are not yet the majority, `bandwagon` agents has helped pull up the total wealth for them. However, I also saw `bandwagon` and `opportunistic` agents exacerbating the negative effects of `random`, `alwaysnew` and `highroller` agents.

## Limitations

These experiments were run with just a _tau_ of 1 and the agents never really a threshold for the least amount of wealth they should maintain before taking _tau_ deductions.

## Conclusion

From these experiments, I saw how the major presence of `stable`, `safe` and or `sticky` agents can outperform any combination of agent strategies because of their conservative nature. I also saw how the impulsiveness of the `random`, `alwaysnew` and `highroller` agents definitely dragged their performance, with most of their combinations never reaching a wealth of 1,000. There are also the balanced `bandwagon` and `opportunistic` strategies that can amplify the effects of whichever class of strategies holds the majority. In a way, we can see that these two strategies promoted cooperation even though the individual wealth of other agents were not known. 

## Code & Dataset

The agent-based model is implemented in Python 3.6.6 and the code are written in `main.py`. 

All experiment outputs like total wealth and population per pool per timestep are saved in CSVs and can be found in the `/experiments` folder. 

## Appendix

**Total wealth over time for experiments with 2 different agent strategies**

![alt text][2combi]

**Total wealth over time for experiments with 3 different agent strategies**

![alt text][3combi]

**Total wealth over time for experiments with 4 different agent strategies**

![alt text][4combi]

**Total wealth over time for experiments with 5 different agent strategies**

![alt text][5combi]

**Total wealth over time for experiments with 6 different agent strategies**

![alt text][6combi]

**Total wealth over time for experiments with 7 different agent strategies**

![alt text][7combi]

**Total wealth over time for experiments with 8 different agent strategies**

![alt text][8combi]

**Total wealth over time for experiments with 9 different agent strategies**

![alt text][9combi]

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
[dist]: /outputs/distribution.png "Distribution of average total wealth from experiments with at least 2 strategies."