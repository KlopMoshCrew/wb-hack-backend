from flask_restful import Resource, reqparse
from datetime import datetime, timedelta
from cluster import get_cluster_for_ecom
#from datetime import date, timedelta


class Heatmap(Resource):

    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument("ecom_id", type=str, required=True, location="args")
        self.get_parser.add_argument("start_date", type=str, required=True, location="args")
        self.get_parser.add_argument("end_date", type=str, required=True, location="args")

    def get(self):
        args = self.get_parser.parse_args()
        ecom_id= args["ecom_id"]

        try:
            start_date = datetime.strptime(str(args["start_date"]), '%Y-%m-%d')
            end_date = datetime.strptime(args["end_date"], '%Y-%m-%d')
        except Exception as e:
            print(str(e))
            return {"message": "invalid params"}, 400
        
        self.get_heatmap(start_date, end_date, ecom_id)
        return {"message": "ok"}, 200
    
    def get_heatmap(self, start_date, end_date, ecom_id):
        result = []
        for n in range(int((end_date - start_date).days)):
            result_for_one_date = get_cluster_for_ecom(start_date + timedelta(n), ecom_id)
            result.append(result_for_one_date)
        print(result)
        #result = get_cluster_for_ecom(start_date, end_date, ecom_id)

