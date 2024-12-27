import sys
import os
import pandas as pd
from cleverminer import cleverminer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataPump import prepareData

df = prepareData.get_traffic_violations()

df = df[['accident', 'belts', 'personal_injury', 'property_damage', 'gender', 
         'race', 'subagency', 'cityIncomeCategory', 'time_of_stop_category', 'vehicle_type', 'alcohol', 'violation_type','make']]


clm = cleverminer(df=df, proc='SD4ftMiner',
                  quantifiers= {'Base1':100, 'Base2':100, 'Ratioconf' : 1.5},
               ante ={
                    'attributes':[
                        {'name': 'subagency', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                        {'name': 'cityIncomeCategory', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                    ], 'minlen':1, 'maxlen':2, 'type':'con'},
               succ ={
                    'attributes':[
                        {'name': 'violation_type', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                    ], 'minlen':1, 'maxlen':1, 'type':'con'},
               frst ={
                    'attributes':[
                        {'name': 'time_of_stop_category', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                    ], 'minlen':1, 'maxlen':1, 'type':'con'},   
               scnd ={
                    'attributes':[
                        {'name': 'time_of_stop_category', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                    ], 'minlen':1, 'maxlen':1, 'type':'con'},
               )

clm.print_summary()
clm.print_rulelist()
clm.print_rule(1) 