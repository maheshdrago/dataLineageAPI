from DataLineageAPI.database.models import *
from typing import TypeVar, Generic, List

T = TypeVar("T")


class LineageData(Generic[T]):

    project_name: str

    def __init__(self, project_name: str) -> None:
        self.project_name = project_name

    def generate_tables_json(self):
        tables = {}
        tablesDB = Schema_Details.query.all()
        for i in tablesDB:
            table_name = str(i.table_name)
            if tables.get(table_name, False):
                tables[table_name].append(i.column_name)
            else:
                tables[table_name] = [i.column_name]

        return tables

    def get_leftout_cols(self, lineages):
        data = {}
        schema_details = self.generate_tables_json()
        for table_name, columns in schema_details.items():
            if lineages.get(table_name, False):
                lineages_data = lineages[table_name]
                lineage_cols = list(
                    map(lambda lineage: lineage["source_col"], lineages_data))
                leftout_cols = [
                    column for column in columns if column not in lineage_cols]

                data[table_name] = leftout_cols

            else:
                target_cols = [lineage["target_col"] for table, lineage_arr in lineages.items(
                ) for lineage in lineage_arr if lineage["target_table"] == table_name]

                leftout_cols = [
                    column for column in columns if column not in target_cols]
                data[table_name] = leftout_cols

        return data

    def fetch_table_lineages(self) -> List[T]:
        table_lineages = Table_Lineage.query.all()
        lineages = {}

        for lineage in table_lineages:
            target_name = str(lineage.target_table)

            if not lineages.get(target_name, False):
                lineages[target_name] = {
                    "source": [lineage.source_table],
                    "query": lineage.join_condition
                }
            else:
                lineages.get(target_name)[
                    "source"].append(lineage.source_table)

        return lineages

    def fetch_column_lineages(self) -> List[T]:
        column_lineages = Column_Lineage.query.all()
        lineages = {}
        src_tables = []
        trgt_tables = set()
        for lineage in column_lineages:
            src_table = lineage.source_table.capitalize()
            src_col = lineage.source_column
            trgt_table = lineage.target_table
            trgt_col = lineage.target_column
            transformation = lineage.transformation

            if lineages.get(src_table, False):
                lineages[src_table].append({
                    "target_table": trgt_table,
                    "target_col": trgt_col,
                    "source_col": src_col,
                    "transformation": transformation
                })
            else:
                lineages[src_table] = [{
                    "target_table": trgt_table,
                    "target_col": trgt_col,
                    "source_col": src_col,
                    "transformation": transformation
                }]

                src_tables.append(src_table.capitalize())

            trgt_tables.add(trgt_table.capitalize())

        schema_details = self.get_leftout_cols(lineages)

        lineages["src_tables"] = src_tables
        lineages["trgt_tables"] = list(trgt_tables)
        lineages["schema_details"] = schema_details

        return lineages

    def fetch_columns(self, table_name: str) -> List:
        tableCols = Schema_Details.query.filter_by(
            table_name=table_name.capitalize())
        columns = [str(row.column_name) for row in tableCols]
        return columns
