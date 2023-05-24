from DataLineageAPI import app
from DataLineageAPI.routes import *
from flask_restful import Api
from flask_cors import CORS
from DataLineageAPI.database.models import *

api = Api(app)
cors = CORS(app)

api.add_resource(Test, "/addTest")
api.add_resource(Query, "/query")
api.add_resource(GraphData, "/graphData")
api.add_resource(ColumnData, "/columns")
api.add_resource(ColumnLineage, "/columnLineage")
""" 

api.add_resource(Testing, "/test/<string:name>") """

if __name__ == "__main__":
    app.run(debug=True)
