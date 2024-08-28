# My annoying neighbour yells at his dog every morning as they leave their house
# I noticed it seems to always be around certain times, so I decided to log the times
# So I could then display the data on a graph because I like graphs

import mysql.connector, matplotlib.pyplot as plt, datetime
from collections import Counter
from matplotlib.ticker import MaxNLocator

conn = mysql.connector.connect(host="192.168.4.222", database="seabee", user="readonly", password="readonly")

with conn.cursor() as cursor:
    cursor.execute("SELECT time FROM dog ORDER BY time ASC") 
    times_r = cursor.fetchall()
    times = [datetime.datetime.strftime(time[0], "%H:%M") for time in times_r] # Data is a list of times in HH:MM format
    time_counts = Counter(times)

    times_sorted = sorted(time_counts.keys())
    counts = [time_counts[time] for time in times_sorted]

    plt.figure(figsize=(10,6))
    plt.bar(times_sorted, counts, color='blue', edgecolor='black')
    plt.xticks(rotation=45)

    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))  # Fixed typo here

    plt.tight_layout()
    plt.show()

