- Download_2_months_data_from_mongo : This script download the OBD-Data for a given vehicle-id, start-timestamp and end-timestamp for the two month-period (including present)
                                      The API being called over here is 'http://data-download.intangles.com:1883/download/'


- Download_2_months_data_from_mongo : This script download the OBD-Data for a given vehicle-id, start-timestamp and end-timestamp for the older period (before the 2 month-period)
                                      The API being called over here is 'https://apis.intangles.com/vehicle/'

- Dtc_Alert_given_period_all_vehicles : This jupyer notebook helps to download DTC and Alert raised in a given period in all the vehicles
                                        URL for Trip-Download is :  'http://internal-apis.intangles.com/trips/' + str(vehicle_id) + '/gettripsintime/' + str(start_ts) + '/' + str(end_ts) + '?proj=_id,start_time,end_time'
                                        URL for DTC & Alert Fetching : 'http://internal-apis.intangles.com/dashboard_apis/fetch"

- Trip-Dtc-Alert-downloader_given_vehicle-id_start-ts_end-ts : This script enables to download all DTC and Alerts for a vehicle-id in a specific time-period
                   URL for Trip-Download is :  'http://internal-apis.intangles.com/trips/' + str(vehicle_id) + '/gettripsintime/' + str(start_ts) + '/' + str(end_ts) + '?proj=_id,start_time,end_time'
                                        URL for DTC & Alert Fetching : 'http://internal-apis.intangles.com/dashboard_apis/fetch"



 