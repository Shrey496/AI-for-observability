# AI-for-observability
 A Python script used to detect anamolies in system logs using **ML algorithm: IsolationForest** to ensure a predictive approach to observability.

# log_analysis.py:
* Read the file
* Serialize the data (using pandas)
* Go through each line of the log
* Get the count of error logs
* If the count exceeds the threshold limit within a specified time range/window, print a message alerting user about this occurence
* Detect error spikes within a 30 second window
* Print logs with anamolies

# aiops_log_analysis.py:
* Read the file
* Serialize the data (using pandas)
* Go through each line of the log
* Assign numeric scores to log levels
* AI Model for Anomaly Detection using ML algorithm: IsolationForest
* Mark anomalies in a readable format and print
