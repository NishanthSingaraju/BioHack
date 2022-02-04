import random
from collections import defaultdict
from datetime import datetime, timedelta
from constants import PERIOD_CYCLE, ACTIVITY_TYPE

def get_stage(count):
    for stage, metadata in PERIOD_CYCLE.items():
        date_range = metadata["date"]
        if (date_range[0] <= count) and (count <= date_range[1]):
            return stage

def predict_period(df):
    today = datetime.today().strftime('%Y-%m-%d')
    day = today
    count = 0
    while df[day] != 1:
        count += 1
        day = day - timedelta(days=1)

    stages = []
    for i in range(0,10):
        c = count % 30
        stages.append(get_stage(c))
        count+=1
    return stages

def get_suggestions(df):
    stages = predict_period(df)
    d = defaultdict(list)
    for i,stage in enumerate(stages):
        activity = random.choice(ACTIVITY_TYPE["stage"])
        d[i].append(activity)
    return d

if __name__ == '__main__':
    pass