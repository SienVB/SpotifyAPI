import requests
from prettytable import PrettyTable


auth_url = "https://accounts.spotify.com/api/token"

#Enter client credentials
client_id = input("Client ID: ")
client_secret = input("Client secret: ")

payload = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'grant_type': 'client_credentials',
}
res = requests.post(auth_url, auth=(client_id, client_secret), data=payload)
res_data = res.json()

#Generate access token
access_token = res_data.get('access_token')

#Search for artists until 'q' to quit
while True:
    artist = input("Search artist, q to quit: ")
    if artist == "q":
        break

    url = "https://api.spotify.com/v1/search?q=" + artist + "&type=artist"
    #max results to keep overview clean
    max_results = int(input("Set the maximum amount of results you want to display: "))

    payload = {}
    headers = {
    'Authorization': 'Bearer ' + access_token
    }

    #Get results with auth token
    response = requests.request("GET", url, headers=headers, data = payload)

    #Errorhandle: if not enough results
    if(max_results > len(response.json()['artists']['items'])):
        max_results = len(response.json()['artists']['items'])


    #Table header
    t = PrettyTable(['Name','Followers', 'Popularity', 'Genres'])
    #Loop over json and print results in table
    n = 0
    while n < max_results:
        name = (response.json()['artists']['items'][n]['name'])
        followers = (response.json()['artists']['items'][n]['followers']['total'])
        pop = str((response.json()['artists']['items'][n]['popularity']))

        #Only show first 3 genres
        #Errorhandle: if less than 3 genres, show only those
        if len(response.json()['artists']['items'][n]['genres']) > 3:
            genres = (response.json()['artists']['items'][n]['genres'][0-2])
        else:
            genres = (response.json()['artists']['items'][n]['genres'])
        
        t.add_row([name, followers, pop, genres])
        n += 1

    print(t)
        
