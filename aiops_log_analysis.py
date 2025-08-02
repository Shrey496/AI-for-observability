import pandas as pd
import numpy as np
import re
from sklearn.ensemble import IsolationForest

#Read log file
log_file_path = "logs.txt"
with open(log_file_path, "r") as file:
    logs = file.readlines()

#Parse logs into a structured DataFrame
data = []
for log in logs:
    parts = log.strip().split(" ", 3)
    if len(parts) < 4:
        continue
    timestamp = parts[0] + " " + parts[1]
    level = parts[2]
    message = parts[3]
    data.append([timestamp, level, message])

df = pd.DataFrame(data, columns=["timestamp", "level", "message"])

#Convert timestamp to datetime format for sorting
df["timestamp"] = pd.to_datetime(df["timestamp"])

#Assign numeric scores to log levels and 
level_mapping = {"INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
df["level_score"] = df["level"].map(level_mapping)

#Add message length as a new feature
df["message_length"] = df["message"].apply(len)

# AI Model for Anomaly Detection using ML algorithm: IsolationForest
model = IsolationForest(contamination=0.1, random_state=42)
df["anomaly"] = model.fit_predict(df[["level_score", "message_length"]])

# Mark anomalies in a readable format
df["is_anomaly"] = df["anomaly"].apply(lambda x: "❌ Anomaly" if x == -1 else "✅ Normal")

# Print only detected anomalies
anomalies = df[df["is_anomaly"] == "❌ Anomaly"]
print("\n🔍 **Detected Anomalies:**\n", anomalies)