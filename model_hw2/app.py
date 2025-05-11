from model import StrategyModel
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)
# Horizontal agents are red. Vertical agents are blue. Role models are black (inactive).
def agent_portrayal(agent):
    if agent.is_role_model:
        color = "black"
    elif agent.learner_type == "horizontal":
        color = "red"
    else:
        color = "blue"
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
    "key_change": Slider("Proportion of Key Change", value=0.5, min=0, max=1, step=0.01),
    "horizontal_ratio": Slider("Proportion of Horizontal Learners", value=0.5, min=0, max=1, step=0.01),
    "role_model_ratio": Slider("Proportion of Role Models", value=0.3, min=0, max=1, step=0.01),
}
# Setting up facets that enable visualization. 
SpaceGraph = make_space_component(agent_portrayal=agent_portrayal)
HorizontalPlot = make_plot_component("Horizontal_Avg_Gain")
VerticalPlot = make_plot_component("Vertical_Avg_Gain")
TotalPlot = make_plot_component("Total_Gain")

strategy_model = StrategyModel()

page = SolaraViz(
    model=strategy_model,
    components=[SpaceGraph, HorizontalPlot, VerticalPlot, TotalPlot],
    model_params=model_params,
    name="Social Learning Simulation",
)

page
