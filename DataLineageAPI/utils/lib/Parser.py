""" import json
from dataclasses import dataclass
from DataLineageAPI.database.models import Lineage, Project
from abc import ABC, abstractmethod


@dataclass
class DataLineage:
    src_db: str
    trgt_db: str
    src_tables: list[dict]
    trgt_tables: list[dict]
    query: str


class FileHanlder(ABC):

    @abstractmethod
    def handle_file():
        pass


class DataHandler:

    def __init__(self, lineage_objects: list[DataLineage]):
        self.lineage_objects = lineage_objects

    @staticmethod
    def project_DB_obj(project_name: str):
        project = Project(project_name=project_name)
        project.save()
        return project

    def feed_mongo(self, project_name: str):
        project = DataHandler.project_DB_obj(project_name)
        for lineage_obj in self.lineage_objects:
            Lineage(project=project, src_db_name=lineage_obj.src_db, trgt_db_name=lineage_obj.trgt_db,
                    src_tables=lineage_obj.src_tables, trgt_tables=lineage_obj.trgt_tables, query=lineage_obj.query).save()


class Parser(FileHanlder):

    def __init__(self):
        self.lineage_objects = []
        self.data = None

    def handle_file(self):
        with open("D:\\Data Lineage\\DataLineage\\src\\lineage.json", "r") as f:
            self.data = json.load(f)

    def get_data_objects(self):
        self.parse()

        return self.lineage_objects

    def parse(self, file_location: str = ""):
        self.handle_file()

        lineages = self.data["lineages"]
        for lineage in lineages:
            src_db = lineage["src_path"][0]["database"]
            src_tables = lineage["src_path"][1]["table"]

            trgt_db = lineage["trg_path"][0]["database"]
            trgt_tables = [
                {
                    "name": lineage["trg_path"][1]["table"],
                    "column":lineage["trg_path"][1]["column"]
                }
            ]

            query = lineage["source_code"]

            obj = DataLineage(src_db, trgt_db, src_tables, trgt_tables, query)

            self.lineage_objects.append(obj)
 """
