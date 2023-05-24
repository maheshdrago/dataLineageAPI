from flask_restful import Resource
from flask import jsonify, request
from DataLineageAPI.database.models import *
from .utils.lib.graphData import LineageData


class GraphData(Resource):
    def get(self):
        lineageData = LineageData("test")
        data = lineageData.fetch_table_lineages()
        return jsonify({"data": data})


class ColumnData(Resource):
    def get(self):
        table_name = request.args.get("table_name")
        lineageData = LineageData("test")
        columns = lineageData.fetch_columns(table_name)

        return jsonify({"data": columns})


class ColumnLineage(Resource):
    def get(self):
        lineageData = LineageData("test")
        column_lineages = lineageData.fetch_column_lineages()
        return jsonify({"col_lineages": column_lineages})


class Test(Resource):
    def get(self):
        try:
            """ db.session.add(Schema_Details(
                table_name="Student", column_name="StudentID"))
            db.session.add(Schema_Details(
                table_name="Student", column_name="StudentName"))
            db.session.add(Schema_Details(
                table_name="Student", column_name="DepartmentID"))
            db.session.add(Schema_Details(
                table_name="Department", column_name="DepartmentName"))
            db.session.add(Schema_Details(
                table_name="Department", column_name="DepartmentID"))
            db.session.add(Schema_Details(
                table_name="Report", column_name="StudentName"))
            db.session.add(Schema_Details(
                table_name="Report", column_name="DepartmentName"))

            db.session.commit() """

            """ db.session.add(Table_Lineage(target_table="Report", source_table="Student",
                           join_condition="student.id=department.id", join_type="inner"))
            db.session.add(Table_Lineage(target_table="Report", source_table="Department",
                           join_condition="student.id=department.id", join_type="inner"))

            db.session.commit() """

            """ db.session.add(Column_Lineage(target_table="Report", target_column="StudentName",
                           transformation="", source_table="student", source_column="StudentName"))
            db.session.add(Column_Lineage(target_table="Report", target_column="DepartmentName",
                           transformation="", source_table="Department", source_column="DepartmentName"))

            db.session.commit() """
            db.session.add(Column_Lineage(target_table="Report", target_column="DepartmentId",
                           transformation="", source_table="Department", source_column="DepartmentID"))
            db.session.commit()
            return {"data": "created"}
        except Exception as e:
            print(e)
            return {"Data": "false"}


class Query(Resource):
    def get(self):
        databaseName = request.args.get("dbName")

        if databaseName == "column_lineage":
            json_data = []
            data = Column_Lineage.query.all()
            for i in data:
                json_data.append({
                    "target_table": i.target_table,
                    "target_column": i.target_column,
                    "transformation": i.transformation,
                    "source_table": i.source_table,
                    "source_column": i.source_column
                })

            return jsonify({"data": json_data})

        elif databaseName == "table_lineage":
            json_data = []
            data = Table_Lineage.query.all()

            for i in data:
                json_data.append({
                    "target_table": i.target_table,
                    "source_table": i.source_table,
                    "join_condition": i.join_condition,
                    "join_type": i.join_type
                })

            return jsonify({"data": json_data})

        elif databaseName == "schema_details":
            json_data = []
            data = Schema_Details.query.all()

            for i in data:
                json_data.append({
                    "table_name": i.table_name,
                    "column_name": i.column_name,
                })

            return jsonify({"data": json_data})
