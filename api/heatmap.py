from flask_restful import Resource, reqparse
from datetime import datetime, timedelta
from cluster import get_cluster_for_ecom
import random
import numpy as np
import json
#from datetime import date, timedelta


class Heatmap(Resource):

    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument("ecom_id", type=str, required=True, location="args")
        self.get_parser.add_argument("start_date", type=str, required=True, location="args")
        self.get_parser.add_argument("end_date", type=str, required=True, location="args")
        self.colors = ["blue", "blue", "green", "green", "red", "red", "green", "green", "blue", "blue" ]

    def get(self):
        args = self.get_parser.parse_args()
        ecom_id = args["ecom_id"]

        try:
            start_date = datetime.strptime(str(args["start_date"]), '%Y-%m-%d')
            end_date = datetime.strptime(args["end_date"], '%Y-%m-%d')
        except Exception as e:
            print(str(e))
            return {"message": "invalid params"}, 400
        
        heatmap = self.get_heatmap(start_date, end_date, ecom_id)
        return {"heatmap": heatmap}, 200

    
    def get_heatmap(self, start_date, end_date, ecom_id):
        result = []
        for n in range(int((end_date - start_date).days)):
            date = start_date + timedelta(n)
            ecom_ids_for_one_date = get_cluster_for_ecom(ecom_id)
            prices = self.get_prices(ecom_ids_for_one_date)
            disrib_colors, min_price, max_price = self.get_disrib_colors(prices.values()) # могло бы быть написано лучше
            
            for ecom_id in ecom_ids_for_one_date:
                result.append(self.get_info_for_ecom(date, ecom_id, prices, disrib_colors, min_price, max_price))
        return result
        
    def get_info_for_ecom(self, date, ecom_id, prices, disrib_colors, min_price, max_price):
        price = prices[ecom_id]
        return {"ecom_id": ecom_id, 
                "price": price,
                "date" : date.strftime('%Y-%m-%d'),
                "color" : self.get_color(price, disrib_colors, min_price, max_price)
                }
   
    def get_color(self, price, disrib_colors, min_price, max_price):
        pos = self.get_position_in_interval(price, min_price, max_price)
        return disrib_colors[pos]

    def get_prices(self, ecom_ids, start_date, end_date):
        prices = {}
        for ecom_id in ecom_ids:
            prices[ecom_id] = self.get_price(ecom_id)
        return prices

    #mock
    def get_price(self, ecom_id, start_date, end_date):
        return ecom_id + 1
    
    def get_disrib_colors(self, prices):
        max_price = max(prices)
        min_price = min(prices)
        distrib = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for price in prices:
            pos = self.get_position_in_interval(price, min_price, max_price)
            distrib[pos] = distrib[pos] + 1
        
        elements_less_or_equal = []
        for value in prices:
            elements_less_or_equal.append(self.count_less_or_equal_in_array(value, prices))
        distrib_colors = []
        for value in elements_less_or_equal:
            distrib_colors.append(self.value_to_color(value))
        return distrib_colors, min_price, max_price

    def get_position_in_interval(self, price, min_price, max_price):
        if(min_price > max_price):
            max_price, min_price = min_price, max_price
        step = 0
        temp_price = min_price
        interval_step = (max_price - min_price) / 10.0
       
        while (temp_price < max_price and price>=temp_price):
            temp_price = temp_price + interval_step
            step = step + 1
        if step > 9:
            step = 9 # на случай проблем с округлением 
        return step

    def count_less_or_equal_in_array(self, value, array):
        result = 0
        for elem in array:
            if elem >= value: # забиваем на эквал
                result = result + 1
        return result

    def value_to_color(self, value):
        if value < 0:
            value = 0
        if value > 9 :
            value = 9

        return self.colors[value]