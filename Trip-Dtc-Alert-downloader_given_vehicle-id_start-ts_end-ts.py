import requests 
import csv
import json
import pandas as pd
from datetime import datetime, timezone
import os
from pathlib import Path

# declaring the output path
output_path = "D:/products/ECT_time_series/ECT_TRIPS_ALERT_19JAN_2024"


# internal functions being used
def trip_data_download(vehicle_id, start_ts, end_ts):
    trip_url = 'http://internal-apis.intangles.com/trips/' + str(vehicle_id) + '/gettripsintime/' + str(start_ts) + '/' + str(end_ts) + '?proj=_id,start_time,end_time'
    # getting the trip-data
    trip_response = requests.get(trip_url, json=trip_url)
    if trip_response.status_code == 200:
        # Parse the JSON response
        trip_json_data = trip_response.json()
        return trip_json_data['result']
    return []


def fetch_alert_dtc_data(start_ts, end_ts):
       

        headers = {
            'Content-Type': 'application/json',
        }


        vehicle_alert_data = {
            "report": "dafault",
            "filter": [
                {
                    "alert_algo_output.timestamp": {
                        "gt": start_ts,
                        "lt": end_ts
                    }
                }
               
    
            ],
            "select": {
                "alert_algo_output.account_id": {
                    "value": True,
                    "as": "account_id"
                },
                "alert_algo_output.vehicle_id": {
                    "value": True,
                    "as": "vehicle_id"
                },
                "alert_algo_output.severity": {
                    "value": True,
                    "as": "severity"
                },
                "alert_algo_output.alerts": {
                    "value": True,
                    "as": "alert_name"
                },
                "alert_algo_output.timestamp": {
                    "value": True,
                    "as": "time"
                },
                "vehicle.spec_id":{
                    "value":True,
                    "as":"spec_id"
                },
                "spec.model":{
                    "value":True,
                    "as":"model"
                },
                "spec.manufacturer":{
                    "value":True,
                    "as":"manufacturer"
                },
                "spec.max_load_capacity":{
                    "value":True,
                    "as":"max_load_capacity"
                }
            }
        }

        vehicle_dtc_data = {"report": "default",
        "filter":[
            {
                "fault_log.timestamp":{
                    "gt": start_ts,
                    "lt": end_ts
                }
            },
            {
                "fault_log.status": "active"
            }
        ],
        "select":{
            "fault_log.status":{
                "value":True,
                "as":"status"
            },
            "fault_log.code":{
                "value":True,
                "as":"code"
            },
            "fault_code.severity":{
                "value":True,
                "as":"severity"
            },
            "fault_log.vehicle_id":{
                "value":True,
                "as":"vehicle_id"
            },
            "vehicle.account_id": {
                "value": True,
                "as": "account_id"
            },
            "vehicle.tag":{
                "value":True,
                "as":"vehicle_plate"
            },
            "fault_log.timestamp":{
                "value":True,
                "as":"time"
            },
            "spec.manufacturer":{
                "value":True
            },
            "fault_code.manufacturer":{
                "value":True
            },
            "fault_code.description":{
                "value":True,
                "as":"description"
            }
        }
        }
    


        alert_url = 'http://internal-apis.intangles.com/dashboard_apis/fetch'

        # getting the alert-data
        alert_response = requests.post(alert_url, json=vehicle_alert_data, headers=headers)
        alert_csv_filename = 'alert.csv'
        if alert_response.status_code == 200:
            # Parse the JSON response
            json_data = alert_response.json()
            alert_headers = json_data['result']['fields']
            with open(alert_csv_filename, 'w', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames = alert_headers)
                
                # Write headers to the CSV file
                csv_writer.writeheader()
                
                # Write each JSON item as a row in the CSV file
                csv_writer.writerows(json_data['result']['output'])
        else:
            print(f"Failed to fetch the alert data. Status code: {alert_response.status_code}")
        df_alert = pd.read_csv(alert_csv_filename, encoding='unicode_escape') 
        


        dtc_url = 'http://internal-apis.intangles.com/dashboard_apis/fetch'
        dtc_response = requests.post(dtc_url, json=vehicle_dtc_data, headers=headers)
        print(dtc_response)
        dtc_csv_filename = 'dtc.csv'
        if dtc_response.status_code == 200:
            # Parse the JSON response
            dtc_json_data = dtc_response.json()
            dtc_headers = dtc_json_data['result']['fields']
            with open(dtc_csv_filename, 'w', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=dtc_headers)
                
                # Write headers to the CSV file
                csv_writer.writeheader()
                
                # Write each JSON item as a row in the CSV file
                csv_writer.writerows(dtc_json_data['result']['output'])
        else:
            print(f"Failed to fetch the dtc data. Status code: {alert_response.status_code}")
        df_dtc = pd.read_csv(dtc_csv_filename, encoding='unicode_escape') 

        return df_alert, df_dtc

def miliseconds_to_utc(time_ms):
    time_seconds = time_ms / 1000.0
    # Create a UTC datetime object
    trip_time_utc = datetime.utcfromtimestamp(time_seconds).replace(tzinfo=timezone.utc)
    formatted_trip_time_utc = trip_time_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    return formatted_trip_time_utc



# Declare an empty DataFrame outside the loop
df_trip_all_alerts = pd.DataFrame()
df_trip_all_dtcs = pd.DataFrame()


# enter the start time and end time between which you want the trips for vehicles
start_ts = 1704047400000
end_ts = 1705482021000
# downloading the alerts and dtcs for all the vehicle_id between the start and end time-stamp
df_alert, df_dtc = fetch_alert_dtc_data(start_ts, end_ts)

# enter the vehicle_id of the vehicle for which you want the trips 
vehicle_id = 940957370228408320
# downloading all the trips of the vehicle_id between the start and end time-stamp
trip_json_data = trip_data_download(vehicle_id, start_ts, end_ts)



df_vehicle_alert = df_alert[(df_alert.vehicle_id == vehicle_id)]
df_vehicle_dtc = df_dtc[(df_dtc.vehicle_id == vehicle_id)]


# sperating the trip-data from the all alert and dtc data
for i in range(len(trip_json_data)):
    trip_start_time = trip_json_data[i]['start_time']
    trip_start_time_utc = miliseconds_to_utc(trip_start_time)
    trip_end_time = trip_json_data[i]['end_time']
    trip_end_time_utc = miliseconds_to_utc(trip_end_time)
    #print(trip_start_time_utc)
    df_vehicle_trip_alert = df_vehicle_alert[(df_vehicle_alert.vehicle_id == vehicle_id) & (df_vehicle_alert.time>=trip_start_time_utc) & (df_vehicle_alert.time<=trip_end_time_utc)]
    df_vehicle_trip_dtc = df_vehicle_dtc[(df_vehicle_dtc.vehicle_id == vehicle_id) & (df_vehicle_dtc.time>=trip_start_time_utc) & (df_vehicle_dtc.time<=trip_end_time_utc)]
    if df_vehicle_trip_alert.shape[0] > 0:
        df_vehicle_trip_alert['trip_id'] = trip_json_data[i]['_id']
        df_vehicle_trip_alert['trip_start_time'] = trip_start_time_utc
        df_vehicle_trip_alert['trip_end_time'] = trip_end_time_utc
        df_trip_all_alerts = pd.concat([df_trip_all_alerts, df_vehicle_trip_alert], ignore_index=True)
    if  df_vehicle_trip_dtc.shape[0] > 0: 
         df_vehicle_trip_dtc['trip_id'] = trip_json_data[i]['_id']
         df_vehicle_trip_dtc['trip_start_time'] = trip_start_time_utc
         df_vehicle_trip_dtc['trip_end_time'] = trip_end_time_utc 
         df_trip_all_dtcs = pd.concat([df_trip_all_dtcs, df_vehicle_trip_dtc], ignore_index=True)

trip_directory = Path(os.path.join(output_path, "trip_data"))

if not trip_directory.exists():
    # Create the directory
    trip_directory.mkdir(parents=True, exist_ok=True)
df_trip_all_alerts.to_csv(os.path.join(trip_directory ,str("trip_alerts_" + str(vehicle_id) + "-" + str(start_ts) + "to" + str(end_ts) + ".csv")))

dtc_directory = Path(os.path.join(output_path, "dtc_data"))
if not dtc_directory.exists():
    # Create the directory
    dtc_directory.mkdir(parents=True, exist_ok=True)
df_trip_all_dtcs.to_csv(os.path.join(dtc_directory ,str("dtc_alerts_" + str(vehicle_id) + "-" + str(start_ts) + "to" + str(end_ts) + ".csv")))


