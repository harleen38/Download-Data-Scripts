import requests

# veichle_ID = str(int(1187730441440854016))

# Start_TS = str(int(1704091435456))
# End_TS   = str(int(1706608051399))

#C:\Users\Harleen.Kaur\Downloads\Download_TH_data (3).py

veichle_ID = str(int(1225921672096251904))

Start_TS = str(int(1704047400000))
End_TS   = str(int(1708176998000))


local_filename = "D:/products/Temp/" + veichle_ID +".json"

# for Indian vehicles use the API 'http://data-download.intangles.com:1883/download/'
# for US vehicles use the API http://algo-internal-apis.intangles-aws-us-east-1.intangles.us:1883/download/
URL = 'http://data-download.intangles.com:1883/download/' + veichle_ID +  "/" +Start_TS + "/" + End_TS 


print(URL)

r = requests.get(URL,stream=True)

with open(local_filename, 'wb') as f:
	for chunk in r.iter_content(chunk_size=1024):
		if chunk:
			print("WRITING...........")
			f.write(chunk)


