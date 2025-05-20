import reflex as rx
from app.states.experiment_state import (
    ExperimentState,
    Experiment,
)


def experiment_row(exp: Experiment) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            exp["id"],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            exp["name"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
        ),
        rx.el.td(
            exp["date"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
        ),
        on_click=lambda: ExperimentState.select_experiment(
            exp["id"]
        ),
        class_name=rx.cond(
            (
                ExperimentState.selected_experiment_id_1
                == exp["id"]
            )
            | (
                ExperimentState.selected_experiment_id_2
                == exp["id"]
            ),
            "cursor-pointer bg-green-200 hover:bg-green-300",
            "cursor-pointer hover:bg-green-100",
        ),
    )


def experiment_table() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Experiments",
            class_name="text-2xl font-semibold text-green-800 mb-4",
        ),
        rx.el.div(
            rx.cond(
                ExperimentState.is_table_collapsed,
                rx.el.button(
                    rx.icon(
                        tag="chevron_left",
                        class_name="text-white",
                    ),
                    on_click=ExperimentState.expand_table,
                    class_name="mb-4 mr-2 p-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors flex items-center justify-center",
                    title="Show All Experiments / Reset",
                ),
                rx.fragment(),
            ),
            rx.el.div(class_name="flex-grow"),
            rx.cond(
                (
                    ExperimentState.selected_experiment_id_1
                    != None
                )
                & (
                    ExperimentState.selected_experiment_id_2
                    == None
                )
                & ~ExperimentState.is_comparing
                & ExperimentState.is_table_collapsed,
                rx.el.button(
                    rx.hstack(
                        "Compare ",
                        rx.icon(
                            tag="chevron_right",
                            class_name="text-white",
                        ),
                    ),
                    on_click=ExperimentState.start_comparison_mode,
                    class_name="mb-4 px-4 py-2 bg-teal-500 text-white rounded hover:bg-teal-600 transition-colors",
                ),
                rx.fragment(),
            ),
            class_name="flex flex-wrap items-center",
        ),
        rx.cond(
            ExperimentState.is_comparing,
            rx.el.p(
                "Select a second experiment from the table below to compare.",
                class_name="my-2 p-2 bg-yellow-100 text-yellow-800 border border-yellow-300 rounded-md",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "ID",
                            class_name="px-6 py-3 text-left text-xs font-medium text-green-700 uppercase tracking-wider bg-green-100",
                        ),
                        rx.el.th(
                            "Name",
                            class_name="px-6 py-3 text-left text-xs font-medium text-green-700 uppercase tracking-wider bg-green-100",
                        ),
                        rx.el.th(
                            "Date",
                            class_name="px-6 py-3 text-left text-xs font-medium text-green-700 uppercase tracking-wider bg-green-100",
                        ),
                        class_name="border-b border-green-300",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        ExperimentState.displayed_experiments,
                        experiment_row,
                    ),
                    class_name="bg-white divide-y divide-green-200",
                ),
                class_name="min-w-full divide-y divide-green-200 shadow-lg overflow-hidden border border-green-300 sm:rounded-lg",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="p-4 bg-green-100 rounded-lg shadow-xl sticky top-0 z-10",
    )