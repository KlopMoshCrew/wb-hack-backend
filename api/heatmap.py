from flask_restful import Resource, reqparse
from datetime import datetime, timedelta
from cluster import get_cluster_for_ecom
from api.db import get_price

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
        self.colors = ["#0000FF", "#0000FF", "#800080", "#800080", "#008000", "#008000", "#FFC0CB", "#FFC0CB", "#FF0000", "#FF0000" ]

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
        ecom_ids_for_one_date = get_cluster_for_ecom(ecom_id)
        prices = self.get_prices(ecom_ids_for_one_date, start_date, end_date)
        
        print(prices)
        for n in range(int((end_date - start_date).days + 1)):
            date = start_date + timedelta(n)
            filtered_prices = self.extract_prices_for_date(prices, date)
            print("filtered dates", filtered_prices)
            print("date ", date)

            if len(filtered_prices) == 0:
                continue
            disrib_colors, min_price, max_price = self.get_disrib_colors(filtered_prices.values()) # могло бы быть написано лучше
            
            for ecom_id in ecom_ids_for_one_date:
                info = self.get_info_for_ecom(date, ecom_id, filtered_prices, disrib_colors, min_price, max_price)
                if info is not None:
                    result.append(info)
        #print("result ", result)
        return result

    def extract_prices_for_date(self, raw_prices, date):
        prices = {}
        for key, prices_with_date in raw_prices.items():
            for elem in prices_with_date:
                if elem[0] == date.date():
                    prices[key] = elem[1]
                    break
                    
        return prices

    def get_info_for_ecom(self, date, ecom_id, prices, disrib_colors, min_price, max_price):
        if ecom_id not in prices:
            return None
        price = prices[ecom_id]
        return {"date" : date.strftime('%Y-%m-%d'),
                "color" : disrib_colors,
                "min" : min_price,
                "max" : max_price
                }
   
    def get_prices(self, ecom_ids, start_date, end_date):
        prices = {}
        for ecom_id in ecom_ids:
            price = get_price(ecom_id, start_date, end_date)
            if len(price):
                prices[ecom_id] = price
        return prices
    
    def get_disrib_colors(self, prices):
        max_price = max(prices)
        min_price = min(prices)
        distrib = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for price in prices:
            pos = self.get_position_in_interval(price, min_price, max_price)
            distrib[pos] = distrib[pos] + 1
        
        elements_less_or_equal = []
        for value in distrib:
            elements_less_or_equal.append(self.count_less_or_equal_in_array(value, elements_less_or_equal))

        count_elements = 1.0 * len(prices)
        # доля элементов меньше
        
        distrib_colors = []
        for value in elements_less_or_equal:
            distrib_colors.append(self.count_elements_less_value_to_color(value, count_elements))
        print(distrib_colors)
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

    def count_elements_less_value_to_color(self, count_elements_less_value, count_elements):
        color_index = int(count_elements_less_value * 1.0 /(count_elements / 10) * 10)
        if color_index < 0:
            color_index = 0
        if color_index > 9 :
            color_index = 9

        return self.colors[color_index]