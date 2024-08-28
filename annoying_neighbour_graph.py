# My annoying neighbour yells at his dog every morning as they leave their house
# I noticed it seems to always be around certain times, so I decided to log the times
# So I could then display the data on a graph because I like graphs

import mysql.connector, matplotlib.pyplot as plt, datetime
from collections import Counter
from matplotlib.ticker import MaxNLocator
from matplotlib.animation import FuncAnimation

conn = mysql.connector.connect(host="192.168.4.222", database="seabee", user="readonly", password="readonly")

with conn.cursor() as cursor:
    cursor.execute("SELECT time FROM dog ORDER BY time ASC") 
    times_r = cursor.fetchall()
    times = [datetime.datetime.strftime(time[0], "%H:%M") for time in times_r] #data is a list of times HH:MM format
    time_counts = Counter(times)

    times_sorted = sorted(time_counts.keys())
    counts = [time_counts[time] for time in times_sorted]

    # Get min and max times
    min_time = min(times)
    max_time = max(times)

    # Format min and max time
    min_time_formatted = datetime.datetime.strptime(min_time, "%H:%M")
    max_time_formatted = datetime.datetime.strptime(max_time, "%H:%M")
    full_time_range = []

    current_time = min_time_formatted
    while current_time <= max_time_formatted:
        full_time_range.append(current_time.strftime("%H:%M"))
        current_time += datetime.timedelta(minutes=1)

    counts = [time_counts.get(time, 0) for time in full_time_range]

    # Generate the chart
    plt.figure(figsize=(14,8))
    plt.bar(full_time_range, counts, color='blue', edgecolor='black')
    plt.xticks(rotation=45, fontsize=9)

    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.xlabel("Times")
    plt.ylabel("Frequency")
    plt.title("Time annoying neighbour annoys me every morning")

    plt.tight_layout()
    plt.show()
