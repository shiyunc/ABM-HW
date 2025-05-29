# Horizontal Social Learning Outperforms Vertical Learning in Volatile Societies

## Summary

This model aims to explore whether certain social environments favor horizontal learners or vertical learners in terms of individual gain and global wealth accumulation. Horizontal social learning means learning from peers. Vertical social learning means learning from seniors (typically parents, but we have used a broader definition here). 

In this study, we assume that in a rapidly changing (volatile) society, horizontal learners have an advantage over vertical learners. In a stable society, vertical learners outperform horizontal learners. We simulate the extent of social change by adjusting the "key to success" in diffrent generations. Within each generation, an agent have 5 rounds to learn from either their successful peers or their senior role models, based on their social learning type. Their goal is to change their strategy toward to "key to success". The more similar their strategy is to key, the higher gain they earn. We will examine which type of learners earn the higher average gain to decide which social learning strategy is more adaptive in a certain society. 

The study found that in societies with moderate to high volatility, horizontal learning is more adaptive in terms of both individual gain and global wealth accumulation. The more volatile the society is, the more it benefits and benefits from horizontal learners. Vertical learning only has an advantage in highly stable societies where the key to success barely changes. Second, horizontal learning is a general adaptive approach, which produces steady individual gains despite the social volatility level. Third, although horizontal learners are favored in volatile societies, stable societies have a higher global wealth accumulation despite the proportion of different learners.


## How to Run

To run the model interactively once you have a complete agents file, run the following code in this directory:

```
    $ solara run app.py
```

## Files

* ``agents.py``: Contains the agent class (some functions are still under development).
* ``model.py``: Contains the model class (some functions are still under development).
* ``app.py``: Defines classes for visualizing the model in the browser via Solara, and instantiates a visualization server.

