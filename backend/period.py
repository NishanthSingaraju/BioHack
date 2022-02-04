import random
import pandas as pd
from collections import defaultdict
from datetime import datetime, timedelta
from constants import PERIOD_CYCLE, ACTIVITY_TYPE, TOTAL_DAYS

def get_stage(count):
    for stage, metadata in PERIOD_CYCLE.items():
        date_range = metadata["date"]
        if (date_range[0] <= count) and (count <= date_range[1]):
            return stage

def predict_period(df):
    day = datetime.today()
    day_str = day.strftime('%Y-%m-%d')
    count = 0
    while df[day_str] != 1:
        count += 1
        day = day - timedelta(days=1)
        day_str = day.strftime('%Y-%m-%d')
    stages = []
    for i in range(0,10):
        c = count % 30
        stages.append(get_stage(c))
        count+=1
    return stages

def get_suggestions(stages):
    d = defaultdict(list)
    for i in range(10):
        stage = stages[i]
        valid_activity = PERIOD_CYCLE[stage]["activity"]
        activity = random.choice(ACTIVITY_TYPE[valid_activity])
        d[i].append(activity)
    return d

def read_period_file(file):
    df = pd.read_csv(file, header=0)
    dict_from_csv = df.applymap(str).groupby('day')['period'].apply(int).to_dict()
    return {k: v for k, v in enumerate(predict_period(dict_from_csv))}

def suggestion_pipeline(file):
    stages = read_period_file(file)
    return get_suggestions(stages)

if __name__ == '__main__':
    pass