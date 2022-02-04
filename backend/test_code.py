from datetime import datetime, timedelta
import csv

def create_test_csv():
    today = datetime.today()
    past_month = today - timedelta(days=35)
    next_month = today + timedelta(days=35)
    day, count = past_month, 0
    period_tracker = []
    while day < next_month:
        if count % 28 == 0:
            track = {"day": day.strftime('%Y-%m-%d'), "period": 1}
        else:
            track = {"day": day.strftime('%Y-%m-%d'), "period": 0}
        period_tracker.append(track)
        day += timedelta(days=1)
        count+=1

    field_names = ["day", "period"]
    with open('data/period.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(period_tracker)

if __name__ == '__main__':
    create_test_csv()