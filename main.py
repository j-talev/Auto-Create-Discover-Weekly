import json
import requests
from secret import spotify_user_id, discover_weekly_id
from refresh import Refresh
from datetime import date



class SaveSongs:
    
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = "spotify_token"
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.new_playlist_id = ""
    
    
        
    def find_songs(self):
        print("Finding songs in discover weekly...")
        # loop through playlist tracks and add them to list
        
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(discover_weekly_id)
        
        response = requests.get(query,
                                headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})
        
        response_json = response.json()
        
        print(response)
        
        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]
        
        self.add_to_playlist()
        
    def create_playlist(self):
        print("Trying to create playlist...")
        # create a new playlist
        
        today = date.today()
        
        todayFormatted = today.strftime("%d/%m/%Y")
        
        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
        
        request_body = json.dumps({
            "name": todayFormatted + " discover weekly",
            "description": "Discover weekly tracks for week starting {}".format(todayFormatted),
            "public": False
        })
        
        response = requests.post(query, data=request_body, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})
        
        response_json = response.json()
        
        return response_json["id"]
        
    def add_to_playlist(self):
        print("Adding songs...")
        # add all songs to new playlist
        
        self.new_playlist_id = self.create_playlist()
        
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id,self.tracks)
        
        response = requests.post(query, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})
        
        print(response.json)
        
    def call_refresh(self):
        
        print("Refreshing token...")
        
        refreshCaller = Refresh()
        
        self.spotify_token = refreshCaller.refresh()
        
        self.find_songs()
        
        
a = SaveSongs()
a.call_refresh()