# This is a script to get an artists singles and albums and print the links

import requests, os, time

client_id = "your_client_id_here"
client_secret = "your_client_secret_here"
artist_id = input("Artist ID: ")


headers = {
	"Content-Type": "application/x-www-form-urlencoded"
}


def keys():
	data = {
		"grant_type": "client_credentials",
		"client_id": client_id,
		"client_secret": client_secret
		}
	file_path = "key.txt"
	current_time = time.time()

	if os.path.exists(file_path):
		print("file exists")
		file_mod_time = os.path.getmtime(file_path)
		if current_time - file_mod_time <= 3600:
			print("edited in last 60 mins")
			with open(file_path, "r") as f:
				file_key = f.read()
			print(f"data: {file_key}")
			return file_key
			
		else:
			print("file edited more then 60 mins ago")
			response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

			if response.status_code == 200:
				response_data = response.json()
				access_token = response_data["access_token"]
				with open("key.txt","w") as f:
					print("writing token to file")
					f.write(access_token)
				return(access_token)
			else:
				print(f"Status code: {response.status_code}")
	else:
		print("file not exist")
		response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

		if response.status_code == 200:
			response_data = response.json()
			access_token = response_data["access_token"]
			with open("key.txt","w") as f:
				print("writing token to file")
				f.write(access_token)
			return(access_token)
		else:
			print(f"Status code: {response.status_code}")
	
bkey = keys()

	
print("getting albums")
new_response = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=single,album", headers={"Authorization": f"Bearer {bkey}"})
if new_response.status_code == 200:
	items = ""
	raw_data = new_response.json()
	for album in raw_data["items"]:
		items += str(f"https://open.spotify.com/album/{album['id']} ")
	print(items)
	
else:
	print(f"response status code: {new_response.status_code}")
