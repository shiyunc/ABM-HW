from model import StrategyModel
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)
# Horizontal agents are red. Vertical agents are blue. Role models are black (inactive). 
# The intensity of color reflects how much gain an agent has. The more intense, the higher gain.  
def agent_portrayal(agent):
    max_gain = 25
    norm_gain = min(agent.gain / max_gain, 1.0)
    alpha = 0.2 + 0.8 * norm_gain # give a base color degree of 20%, or we can't tell the agent type.

    if agent.is_role_model:
        color = (0, 0, 0, alpha)  # black
    elif agent.learner_type == "horizontal":
        color = (1, 0, 0, alpha)  # red
    else:
        color = (0, 0, 1, alpha)  # blue

    return {
        "color": color,
        "marker": "s",
        "size": 40,
    }
# setting up default values. 
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "width": Slider("Grid Width", value=20, min=10, max=50, step=1),
    "height": Slider("Grid Height", value=20, min=10, max=50, step=1),
    "key_change": Slider("Proportion of Key Change", value=0.8, min=0, max=1, step=0.01),
    "horizontal_ratio": Slider("Proportion of Horizontal Learners", value=0.5, min=0, max=1, step=0.01),
    "role_model_ratio": Slider("Proportion of Role Models", value=0.3, min=0, max=1, step=0.01),
}

# Setting up facets that enable visualization. 
SpaceGraph = make_space_component(agent_portrayal=agent_portrayal)
GainPlot = make_plot_component(["Horizontal_Avg_Gain", "Vertical_Avg_Gain"])
AccumulatedPlot = make_plot_component("Accumulated_Gain")

strategy_model = StrategyModel()

page = SolaraViz(
    model=strategy_model,
    components=[SpaceGraph, GainPlot, AccumulatedPlot],
    model_params=model_params,
    name="Social Learning Simulation",
)

page
