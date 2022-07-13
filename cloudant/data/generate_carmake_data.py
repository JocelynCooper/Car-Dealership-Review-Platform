import json
import random

reviews = json.load(open(""))

carMakeList = set()
for review in reviews["reviews"]:
    carMakeList.add(review["car_make"])

descriptions = ["Tangible product differentiation is both critical to success and difficult to maintain on a sustained basis. \
    A key focus of the marketing function should be to rigorously understand consumers’ preferences, unmet needs, and willingness \
        to pay, in order to maximize the “hit rate” on innovative products.",
                "Minimizing cost of ownership (both up-front acquisition cost and long-term ownership cost) within the segment boundary is \
            critical. The marketing function must take an active role in balancing the drive toward lower cost of ownership with the \
                consumer value created through innovative features and options.",
                "For mass-market vehicles, incentives are a symptom of a weak brand — not the cause. In the absence of a strong brand, price is \
                    the only plausible way to affect near-term demand. Hence, curtailing incentives in an effort to “build brand” is not likely \
                        an economically viable option.",
                "A successful automotive brand benefits from its brand core values, which have grown over a period of decades, and transport its specific character from the inside to the outside. It is recharged continuously with peak performances, much like a battery, which transmits its brand energy to the customer. Audi's peak performances, for example, include the Audi quattro technology, which earned the company a number of triumphant victories in motor sports. It still supports the brand to this day.",
                "Apart from their peak performances, strong (automotive) brands are characterized by high agility paired with stability. This combination is called resilience. If you look at the positions of the leading auto makers on the BrandTrust Resilience Index, the significance of resilience becomes clear: In 2017, Audi defied the Diesel scandal and even passed Tesla (top position in the 2015 index). Apparently, consumers respond not only to the proselytizing powers of founder Elon Musk, but care about real experiences with the brand. Solid automotive brands, built over the course of many years, cannot be destroyed over night, because their customers are willing to forgive mistakes."]

carMake = []
i = 1
for make in carMakeList:
    curr = {}
    curr["id"] = i
    curr["name"] = make
    curr["description"] = random.choice(list(descriptions))
    curr["establish_date"] = str(random.choice(list(range(1970, 2022)))) + "-" +str(random.choice(list(range(1, 13)))) + "-" + str(random.choice(list(range(1, 32)))) 
    carMake.append(curr)
    i += 1

with open('carmake.json', 'w') as fp:
    json.dump(carMake, fp)
