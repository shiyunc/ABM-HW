*Code adapted from Mesa Examples project*

# Horizontal vs. Vertical Social Learning in a Volatile Society

## Summary

This model aims to explore whether certain social environments favor horizontal learners or vertical learners. Horizontal social learning means learning from peers. Vertical social learning means learning from seniors (typically parents). In this study, we assume that in a rapidly changing (volatile) society, horizontal learners have an advantage over vertical learners. In a stable society, vertical learners outperform horizontal learners. We simulate the extent of social change by adjusting the "key to success" in successive generations. 


## Improvements on the Original Model

Despite its significance, the original model overlooks the societal frictions that restrict individuals from moving freely. In this study, I introduced relational mobility to the model and explored how it influenced the agents’ behavioral pattern and the segregation outcome. Relational mobility represents how much flexibility a society affords individuals to create and dispose of social relationships based on personal preference. I added a parameter called "friction". High friction represents low relational mobility. For each agent in each round, a random number is generated to represent the circumstances of the agent. Only when the circumstances are good enough to overcome the friction can the agent move. This design makes the model more realistic and increases the interaction between the individual behavior and the social environment. 

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively once you have a complete agents file, run the following code in this directory:

```
    $ solara run app.py
```

## Files

* ``agents.py``: Contains the agent class, currently incomplete
* ``model.py``: Contains the model class
* ``app.py``: Defines classes for visualizing the model in the browser via Solara, and instantiates a visualization server.

## Further Reading

Schelling's original paper describing the model:

[Schelling, Thomas C. Dynamic Models of Segregation. Journal of Mathematical Sociology. 1971, Vol. 1, pp 143-186.](https://www.stat.berkeley.edu/~aldous/157/Papers/Schelling_Seg_Models.pdf)

An interactive, browser-based explanation and implementation:

[Parable of the Polygons](http://ncase.me/polygons/), by Vi Hart and Nicky Case.
