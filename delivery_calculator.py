from flask import Flask, jsonify, request
from datetime import datetime
import math

app = Flask(__name__)


@app.route('/', methods=['POST'])
def delivery_calculator():
    cart_value = request.json['cart_value']  # getting delivery information from the request payload
    delivery_distance = request.json['delivery_distance']
    number_of_items = request.json['number_of_items']
    time = request.json['time']
    time_obj = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")  # converting to datetime object

    final_fee = 0

    if cart_value < 10000:  # checking if cart value is more or equal to 100e, because then final fee stays 0e

        if cart_value < 1000:  # adding surcharge is cart value is less than 10e
            final_fee += 1000 - cart_value

        if delivery_distance <= 1000:  # if distance less than or equal to 1km, adding extra 2e to delivery fee
            final_fee += 200
        else:  # otherwise adding 1e for every 500m
            additional_delivery = math.ceil(((delivery_distance - 1000) / 500.0)) * 100
            final_fee += 200 + additional_delivery

        if number_of_items > 4:  # if number of items is more than 4, adding 50 cents to delivery fee for each piece
            final_fee += (number_of_items - 4) * 50

        if time_obj.weekday() == 4 and 15 <= time_obj.hour <= 19:  # if it's friday rush time, multiplying by 1.1
            final_fee *= 1.1

        if final_fee > 1500:  # checking the final fee as it cannot be bigger than 15e
            final_fee = 1500

    return jsonify({'delivery_fee': int(final_fee)})  # returning final fee as a response payload


if __name__ == '__main__':
    app.run(debug=True)
