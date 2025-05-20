import reflex as rx
import pandas as pd
from typing import TypedDict, List, Dict, Optional
from app.utils.databricks_utils import async_query_df


class Experiment(TypedDict):
    id: int
    name: str
    date: str


class DataPoint(TypedDict):
    step: int
    value: float


class ExperimentState(rx.State):
    experiments_data: List[Experiment] = []
    selected_experiment_id_1: Optional[int] = None
    experiment_attributes_data_1: Dict[
        str, List[DataPoint]
    ] = {}
    is_loading_data_1: bool = False
    selected_experiment_id_2: Optional[int] = None
    experiment_attributes_data_2: Dict[
        str, List[DataPoint]
    ] = {}
    is_loading_data_2: bool = False
    is_table_collapsed: bool = False
    is_comparing: bool = False

    @rx.event(background=True)
    async def initial_load(self):
        async with self:
            df = await async_query_df(
                "SELECT id, name, CAST(date AS STRING) as date FROM experiments ORDER BY date DESC;"
            )
            if not df.empty:
                self.experiments_data = df.to_dict(
                    orient="records"
                )
            else:
                self.experiments_data = []
        yield

    @rx.event
    def select_experiment(self, experiment_id: int):
        if self.is_comparing:
            self.selected_experiment_id_2 = experiment_id
            self.is_comparing = False
            self.is_table_collapsed = True
            yield ExperimentState.fetch_attribute_data_2
        else:
            self.selected_experiment_id_1 = experiment_id
            self.selected_experiment_id_2 = None
            self.experiment_attributes_data_2 = {}
            self.is_loading_data_2 = False
            self.is_table_collapsed = True
            yield ExperimentState.fetch_attribute_data_1

    async def _fetch_data_for_experiment(
        self, experiment_id: Optional[int]
    ) -> Dict[str, List[DataPoint]]:
        if experiment_id is None:
            return {}
        query = "\n            SELECT\n                dp.step,\n                dp.value,\n                dt.type_name\n            FROM data_points dp\n            JOIN data_types dt ON dp.data_type_id = dt.id\n            WHERE dp.experiment_id = %(exp_id)s\n            ORDER BY dt.type_name, dp.step;\n            "
        df = await async_query_df(
            query, parameters={"exp_id": experiment_id}
        )
        new_attributes_data: Dict[str, List[DataPoint]] = {}
        if not df.empty:
            for type_name, group_df in df.groupby(
                "type_name"
            ):
                new_attributes_data[type_name] = group_df[
                    ["step", "value"]
                ].to_dict(orient="records")
        return new_attributes_data

    @rx.event(background=True)
    async def fetch_attribute_data_1(self):
        async with self:
            self.is_loading_data_1 = True
            self.experiment_attributes_data_1 = {}
        yield
        attributes_data = (
            await self._fetch_data_for_experiment(
                self.selected_experiment_id_1
            )
        )
        async with self:
            self.experiment_attributes_data_1 = (
                attributes_data
            )
            self.is_loading_data_1 = False
        yield

    @rx.event(background=True)
    async def fetch_attribute_data_2(self):
        async with self:
            self.is_loading_data_2 = True
            self.experiment_attributes_data_2 = {}
        yield
        attributes_data = (
            await self._fetch_data_for_experiment(
                self.selected_experiment_id_2
            )
        )
        async with self:
            self.experiment_attributes_data_2 = (
                attributes_data
            )
            self.is_loading_data_2 = False
        yield

    @rx.event
    def expand_table(self):
        self.is_table_collapsed = False
        self.is_comparing = False
        self.selected_experiment_id_1 = None
        self.experiment_attributes_data_1 = {}
        self.is_loading_data_1 = False
        self.selected_experiment_id_2 = None
        self.experiment_attributes_data_2 = {}
        self.is_loading_data_2 = False

    @rx.event
    def start_comparison_mode(self):
        self.is_comparing = True
        self.is_table_collapsed = False
        self.selected_experiment_id_2 = None
        self.experiment_attributes_data_2 = {}
        self.is_loading_data_2 = False

    @rx.var
    def displayed_experiments(self) -> List[Experiment]:
        if self.is_table_collapsed:
            if (
                self.selected_experiment_id_1 is not None
                and self.selected_experiment_id_2
                is not None
            ):
                ids_to_show = {
                    self.selected_experiment_id_1,
                    self.selected_experiment_id_2,
                }
                return [
                    exp
                    for exp in self.experiments_data
                    if exp["id"] in ids_to_show
                ]
            elif self.selected_experiment_id_1 is not None:
                return [
                    exp
                    for exp in self.experiments_data
                    if exp["id"]
                    == self.selected_experiment_id_1
                ]
            return []
        return self.experiments_data

    @rx.var
    def all_attribute_names(self) -> List[str]:
        keys1 = set(
            self.experiment_attributes_data_1.keys()
        )
        keys2 = set(
            self.experiment_attributes_data_2.keys()
        )
        return sorted(list(keys1.union(keys2)))