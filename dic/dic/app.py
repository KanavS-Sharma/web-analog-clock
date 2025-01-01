from flask import Flask, render_template
from datetime import datetime, timezone
import pytz
import ephem

app = Flask(__name__)

def get_moon_phase():
    """Calculate the current moon phase using PyEphem."""
    moon = ephem.Moon()
    today = ephem.now()
    moon.compute(today)
    phase = moon.phase
    return phase

def is_leap_year(year):
    """Check if a year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

@app.route('/')
def home():
    now = datetime.now()
    utc_now = datetime.now(timezone.utc)
    local_tz = pytz.timezone('Asia/Kolkata')  # Change to your preferred timezone
    local_time = utc_now.astimezone(local_tz)

    data = {
        "local_time": local_time.strftime("%Y-%m-%d %H:%M:%S"),
        "utc_time": utc_now.strftime("%Y-%m-%d %H:%M:%S"),
        "day": local_time.strftime("%A"),
        "month": local_time.strftime("%B"),
        "year": local_time.year,
        "is_leap_year": is_leap_year(local_time.year),
        "week_of_year": local_time.strftime("%U"),
        "timezone": {
            "name": local_tz.zone,
            "utc_offset": local_time.strftime("%z"),
        },
        "moon_phase": get_moon_phase(),
    }

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)