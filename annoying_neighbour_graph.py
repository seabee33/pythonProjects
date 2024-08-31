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
    times = [datetime.datetime.strftime(time[0], "%H:%M") for time in times_r]  # Data is a list of times in HH:MM format
    time_counts = Counter(times)

    # Get all unique times and their counts
    times_sorted = sorted(time_counts.keys())
    counts = [time_counts[time] for time in times_sorted]

    # Determine the full time range from min to max time
    min_time = min(times)
    max_time = max(times)

    min_time_formatted = datetime.datetime.strptime(min_time, "%H:%M")
    max_time_formatted = datetime.datetime.strptime(max_time, "%H:%M")

    full_time_range = []
    current_time = min_time_formatted

    while current_time <= max_time_formatted:
        full_time_range.append(current_time.strftime("%H:%M"))
        current_time += datetime.timedelta(minutes=1)

    counts = [time_counts.get(time, 0) for time in full_time_range]

    # Generate the chart
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_ylim(0, max(counts) + 1)
    ax.set_xlabel("Times")
    ax.set_ylabel("Frequency")
    ax.set_title("Time annoying neighbour annoys me every morning")

    # Plot the bars and set x-ticks to include every minute
    bars = ax.bar(full_time_range, counts, color='blue', edgecolor='black')
    
    # Set x-ticks for every minute
    ax.set_xticks(range(len(full_time_range)))
    ax.set_xticklabels(full_time_range, rotation=45, fontsize=9)
    
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Prepare data for animation
    times_with_count = [(i, count) for i, count in enumerate(counts) if count >= 1]
    
    def animate(i):
        index, count = times_with_count[i]
        bars[index].set_height(count)
    
    ani = FuncAnimation(fig, animate, frames=len(times_with_count), interval=1000, repeat=False)

    plt.tight_layout()
    plt.show()

    plt.tight_layout()
    plt.show()
