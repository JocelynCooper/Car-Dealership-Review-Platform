import json
import random

reviews = json.load(open(""))

typeList = ['Sedan', 'SUV', 'WAGON']
carModel = []

i = 1
for review in reviews["reviews"]:
    curr = {}
    curr["id"] = i
    curr["carMakeId"] = 1
    i += 1
    curr["carMakeName"] = review["car_make"]
    curr["dealer_id"] = review["dealership"]
    curr["name"] = review["car_model"]
    curr["type"] = random.choice(typeList)
    curr["year"] = review["car_year"]
    carModel.append(curr)
    

with open('carmodel.json', 'w') as fp:
    json.dump(carModel, fp)
