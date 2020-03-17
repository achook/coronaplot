import matplotlib.pyplot as plt
import numpy as np
from requests import get
from datetime import datetime

COUNTRY = "PL"

WIDTH = 10
HEIGHT = 5
DPI = 250
OUTPUT = "plot.png"

GR = 0.52

r = get(f"https://thevirustracker.com/free-api?countryTimeline={COUNTRY}")
data = r.json()["timelineitems"][0]

dates = []
cases = []
deaths = []
recovered = []
exp = []

started = False
index = 1

for element in data:
    try:
        daily_cases = data[element]["total_cases"]

        if daily_cases == 0 and not started:
            continue

        cases.append(daily_cases)

        daily_deaths = data[element]["total_deaths"]
        deaths.append(daily_deaths)

        daily_recovered = data[element]["total_recoveries"]
        recovered.append(daily_recovered)

        day = datetime.strptime(element, "%m/%d/%Y")
        dates.append(day.strftime("%d.%m"))

        exp.append((1+GR) ** index)
        index += 1

        started = True

    except TypeError as err:
        pass

fig, ax = plt.subplots(figsize=[WIDTH,HEIGHT], dpi=DPI)

ax.plot(dates, cases, label="cases", color="orange", linewidth=2)
ax.plot(dates, deaths, label="deaths", color="red", linewidth=2) 
ax.plot(dates, recovered, label="recovered", color="green", linewidth=2)
ax.plot(dates, exp, label="exponential growth", color="black", linewidth=2, linestyle=':')

now = datetime.now().strftime("%d.%m.%Y")
ax.set_title(f"Infected in {COUNTRY} for {now}")

ax.legend()
plt.xticks(rotation=45)

fig.tight_layout()
plt.savefig(OUTPUT)