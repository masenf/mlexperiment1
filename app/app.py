import reflex as rx
import reflex_enterprise as rxe
from app.states.experiment_state import ExperimentState
from app.components.experiment_table import experiment_table
from app.components.attribute_graphs import (
    attribute_graphs_section,
)
from rxconfig import config


def index() -> rx.Component:
    return rx.el.div(
        experiment_table(),
        attribute_graphs_section(),
        class_name="container mx-auto p-4",
        on_mount=ExperimentState.initial_load,
    )


app = rxe.App(theme=rx.theme(appearance="light"))
app.add_page(index)