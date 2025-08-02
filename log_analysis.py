import pandas as pd
from collections import Counter
import re

#Read the log file
log_file = "logs.txt"

#Append the log entries to an array ONLY if it matches the provided pattern. Ex: 2025-03-27 10:00:00 INFO Suspicious IP access blocked
log_entries = []
with open(log_file, "r") as file:
    for line in file:
        match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)", line.strip())
        if match:
            timestamp, level, message = match.groups()
            log_entries.append([timestamp, level, message])

#Use pandas library to convert the log array to a DataFrame, essentially timestamp, level, message would be columns which will have data within them grouped in rows
df = pd.DataFrame(log_entries, columns=["timestamp", "level", "message"])
df["timestamp"] = pd.to_datetime(df["timestamp"])      #Convert to a datetime object to enable performing math operations based on timestamp, like sort, filter..

#Count errors in the last 30 seconds
error_counts = Counter(df[df["level"] == "ERROR"]["timestamp"].dt.floor("30s"))

#Set threshold (Number of allowed error messages within a 30 second window before an alert is fired)
threshold = 3

anamoly_windows = []

#Detect error spikes
for time, count in error_counts.items():
    if count > threshold:
        anamoly_windows.append(time)
        print(f"Anamoly detected! {count} ERROR logs within 30 seconds of: {time}")



#Print logs with anamolies
anamolies = df[(df["level"] == "ERROR") & (df["timestamp"].dt.floor("30s").isin(anamoly_windows))]

#Sorted log lines that represent anamolies by timestamp and print them
print("\nLogs with Anamolies:")
anamolies_sorted = anamolies.sort_values(by="timestamp")
print(anamolies_sorted.to_string(index=False))





