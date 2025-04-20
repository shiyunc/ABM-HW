*Code adapted from Mesa Examples project*

# Schelling Segregation Model With Relational Mobility

## Summary

The Schelling segregation model is a classic agent-based model, demonstrating how even a mild preference for similar neighbors can lead to a much higher degree of segregation than we would intuitively expect. The model consists of agents on a square grid, where each grid cell can contain at most one agent. Agents come in two colors: red and blue. They are happy if a certain share of their eight possible neighbors are of the same color, and unhappy otherwise. Unhappy agents will pick a random empty cell to move to each step, until they are happy. The model keeps running until there are no unhappy agents.

Even in runs where the agents would be perfectly happy with a majority of their neighbors being of a different color (e.g. a Blue agent would be happy with five Red neighbors and three Blue ones), the model consistently leads to a high degree of segregation, with most agents ending up with no neighbors of a different color.

## Improvement on the original model

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
