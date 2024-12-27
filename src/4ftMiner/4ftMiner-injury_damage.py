import sys
import os
import pandas as pd
from cleverminer import cleverminer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataPump import prepareData

df = prepareData.get_traffic_violations()

df = df[['accident', 'belts', 'personal_injury', 'property_damage', 'gender', 'race', 'subagency', 'cityIncomeCategory', 'time_of_stop_category', 'vehicle_type', 'alcohol', 'violation_type','wasRaining', 'wind_type', 'temperature_type']]
df = df[df['accident'] == 'Yes']

clm = cleverminer(
    df=df,
    proc='4ftMiner',
    quantifiers={'Base': 10, 'aad': 0.2, 'conf': 0.3},
    ante={
        'attributes': [
            {'name': 'gender', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
            {'name': 'race', 'type': 'subset','minlen': 1, 'maxlen': 1},
            {'name': 'wasRaining', 'type': 'rcut','minlen': 1, 'maxlen': 1},
            {'name': 'wind_type', 'type': 'rcut','minlen': 1, 'maxlen': 1},
            {'name': 'temperature_type', 'type': 'rcut','minlen': 1, 'maxlen': 1},
            {'name': 'time_of_stop_category', 'type': 'subset','minlen': 1, 'maxlen': 1}
        ],
        'minlen': 1,
        'maxlen': 3,
        'type': 'con'
    },
    succ={
        'attributes': [
            
            {'name': 'personal_injury', 'type': 'rcut', 'minlen': 1, 'maxlen': 1},
            {'name': 'property_damage', 'type': 'rcut', 'minlen': 1, 'maxlen': 1}
        ],
        'minlen': 1,
        'maxlen': 1,
        'type': 'con'
    }
)

clm.print_summary()
clm.print_rulelist()
clm.print_rule(1)