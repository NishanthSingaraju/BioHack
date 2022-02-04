from datetime import datetime, timedelta
import csv
from io import BytesIO
from api import app

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

def test_file_upload():
    client = app.test_client() # you will need your flask app to create the test_client
    filepath = "data/period.csv"
    csv_data = open(filepath, "rb")
    data = {
        'file': (csv_data, filepath),
    }
    # note in that in the previous line you can use 'file' or whatever you want.
    # flask client checks for the tuple (<FileObject>, <String>)
    res = client.post('/api/upload', data=data)
    assert res.status_code == 200

if __name__ == '__main__':
    create_test_csv()
    test_file_upload()