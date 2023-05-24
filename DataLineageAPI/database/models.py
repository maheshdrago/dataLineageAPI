from DataLineageAPI import db


class Table_Lineage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_table = db.Column(db.String(50), unique=False)
    source_table = db.Column(db.String(50), unique=False)
    join_condition = db.Column(db.String(230))
    join_type = db.Column(db.String(50))


class Column_Lineage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_table = db.Column(db.String(50), unique=False)
    target_column = db.Column(db.String(50), unique=False)
    transformation = db.Column(db.String(50), unique=False)
    source_table = db.Column(db.String(50), unique=False)
    source_column = db.Column(db.String(50), unique=False)


class Schema_Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(50), unique=False)
    column_name = db.Column(db.String(50), unique=False)
