import sys
import os
import pandas as pd
from cleverminer import cleverminer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataPump import prepareData

df = prepareData.get_traffic_violations()

df = df[['accident', 'belts', 'personal_injury', 'property_damage', 'gender', 'race', 'subagency', 'cityIncomeCategory', 
         'time_of_stop_category', 'vehicle_type', 'alcohol', 'violation_type']]


clm = cleverminer(df=df,target='race',proc='CFMiner',
               quantifiers= {'RelMax':0.5, 'Base':50},
               cond ={
                    'attributes':[
                        {'name': 'time_of_stop_category', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                        {'name': 'subagency', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                        {'name': 'violation_type', 'type': 'lcut', 'minlen': 1, 'maxlen': 1},
                        {'name': 'cityIncomeCategory', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                        {'name': 'gender', 'type': 'subset', 'minlen': 1, 'maxlen': 1},

                    ], 'minlen':1, 'maxlen':3, 'type':'con'}
               )

clm.print_summary()
clm.print_rulelist()
clm.print_rule(1)
