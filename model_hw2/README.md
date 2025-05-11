*Code adapted from Mesa Examples project*

# Horizontal vs. Vertical Social Learning in a Volatile Society

## Summary

This model aims to explore whether certain social environments favor horizontal learners or vertical learners. Horizontal social learning means learning from peers. Vertical social learning means learning from seniors (typically parents, but we used a broader definition here). 

In this study, we assume that in a rapidly changing (volatile) society, horizontal learners have an advantage over vertical learners. In a stable society, vertical learners outperform horizontal learners. We simulate the extent of social change by adjusting the "key to success" in diffrent generations. Within each generation, an agent have 5 rounds to learn from either their successful peers or their senior role models, based on their social learning type. Their goal is to change their strategy toward to "key to success". The more similar their strategy is to key, the higher gain they earn. We will examine which type of learner earn the higher gain to decide which social learning strategy is more adaptive in a certain society. 


## How to Run

To run the model interactively once you have a complete agents file, run the following code in this directory:

```
    $ solara run app.py
```

## Files

* ``agents.py``: Contains the agent class (some functions are still under development).
* ``model.py``: Contains the model class (some functions are still under development).
* ``app.py``: Defines classes for visualizing the model in the browser via Solara, and instantiates a visualization server.
