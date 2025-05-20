import reflex as rx
from app.states.experiment_state import (
    ExperimentState,
    DataPoint,
)
from typing import List, Dict, Optional


def attribute_graph_component(
    attribute_name: str,
    data_source: rx.Var[List[DataPoint]],
) -> rx.Component:
    return rx.el.div(
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                class_name="opacity-50 stroke-green-200",
            ),
            rx.recharts.graphing_tooltip(
                content_style={
                    "background_color": "rgba(255, 255, 255, 0.8)",
                    "border_radius": "0.5rem",
                }
            ),
            rx.recharts.x_axis(
                data_key="step",
                name="Step",
                stroke="#34D399",
            ),
            rx.recharts.y_axis(
                name="Value", stroke="#34D399"
            ),
            rx.recharts.area(
                type="monotone",
                data_key="value",
                stroke="#10B981",
                fill="#34D399",
                fill_opacity=0.6,
            ),
            data=data_source,
            height=300,
            width="100%",
            margin={
                "top": 5,
                "right": 30,
                "left": 20,
                "bottom": 5,
            },
        ),
        class_name="p-4 bg-white rounded-lg shadow-md border border-green-200",
    )


def single_attribute_display(
    attribute_name: str,
    data_dict: rx.Var[Dict[str, List[DataPoint]]],
    exp_id: rx.Var[Optional[int]],
    is_loading: rx.Var[bool],
) -> rx.Component:
    return rx.cond(
        is_loading,
        rx.el.div(
            rx.spinner(class_name="text-green-500"),
            class_name="h-[300px] flex items-center justify-center bg-white rounded-lg shadow-md border border-green-200",
        ),
        rx.cond(
            data_dict.contains(attribute_name),
            attribute_graph_component(
                attribute_name, data_dict[attribute_name]
            ),
            rx.el.div(
                rx.el.p(
                    "No data for attribute '",
                    attribute_name,
                    "' in Experiment ",
                    rx.el.span(exp_id.to_string()),
                ),
                class_name="p-4 text-green-700 h-full flex items-center justify-center bg-green-50 rounded-lg shadow-md border border-green-200 min-h-[300px]",
            ),
        ),
    )


def attribute_graphs_section() -> rx.Component:
    return rx.cond(
        ExperimentState.selected_experiment_id_1 != None,
        rx.el.div(
            rx.el.h2(
                rx.cond(
                    ExperimentState.selected_experiment_id_2
                    != None,
                    "Experiment Comparison",
                    "Experiment Data",
                ),
                class_name="text-2xl font-semibold text-green-800 mt-8 mb-4",
            ),
            rx.foreach(
                ExperimentState.all_attribute_names,
                lambda attr_name: rx.el.div(
                    rx.el.h3(
                        f"Attribute: {attr_name}",
                        class_name="text-xl font-semibold text-green-700 my-4 md:col-span-2",
                    ),
                    rx.el.div(
                        rx.cond(
                            ExperimentState.selected_experiment_id_2
                            != None,
                            rx.el.h4(
                                "Experiment ",
                                rx.el.span(
                                    ExperimentState.selected_experiment_id_1.to_string()
                                ),
                                class_name="text-lg font-medium text-green-600 text-center mb-2",
                            ),
                            rx.fragment(),
                        ),
                        single_attribute_display(
                            attr_name,
                            ExperimentState.experiment_attributes_data_1,
                            ExperimentState.selected_experiment_id_1,
                            ExperimentState.is_loading_data_1,
                        ),
                    ),
                    rx.cond(
                        ExperimentState.selected_experiment_id_2
                        != None,
                        rx.el.div(
                            rx.el.h4(
                                "Experiment ",
                                rx.el.span(
                                    ExperimentState.selected_experiment_id_2.to_string()
                                ),
                                class_name="text-lg font-medium text-green-600 text-center mb-2",
                            ),
                            single_attribute_display(
                                attr_name,
                                ExperimentState.experiment_attributes_data_2,
                                ExperimentState.selected_experiment_id_2,
                                ExperimentState.is_loading_data_2,
                            ),
                        ),
                        rx.fragment(),
                    ),
                    class_name=rx.cond(
                        ExperimentState.selected_experiment_id_2
                        != None,
                        "grid grid-cols-1 md:grid-cols-2 gap-4 items-start border-t border-green-200 pt-4 mt-4",
                        "grid grid-cols-1 gap-4 items-start border-t border-green-200 pt-4 mt-4",
                    ),
                ),
            ),
            class_name="mt-6",
        ),
        rx.fragment(),
    )