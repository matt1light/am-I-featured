import requests
import base64
import json


CLIENT_ID = '35ccc8fd28124f2798578803c3be3822';
CLIENT_SECRET= 'e0d23146812a4de7bf10d0f3f37c4e9b';

def getToken():
    authKey = 'Basic ' + base64.b64encode(CLIENT_ID + ':' + CLIENT_SECRET)
    r = requests.post('https://accounts.spotify.com/api/token', headers = {'Authorization': authKey}, data = {'grant_type': 'client_credentials' })
    return r.json()['access_token']

def getPlaylists(token):
    r = requests.get('https://api.spotify.com/v1/browse/featured-playlists', headers = {'Authorization': 'Bearer ' + token}, data = {'country': 'CA'})
    return r.json()['playlists']['items']

def getTracks(playlist, token):
    r = requests.get('https://api.spotify.com/v1/users/spotify/playlists/' + playlist['id']  + '/tracks', headers = {'Authorization': 'Bearer ' + token})
    return r.json()['items']

def matchArtist(track, artist, token):
    for track_artist in track['artists']:
        if track_artist['name'] == artist:
            return True
    return False

def getAllMatches(artist):
    token = getToken()
    playlists = getPlaylists(token)
    playlistcount = 0
    trackcount = 0
    for playlist in playlists:
        playlistcount += 1
        tracks = getTracks(playlist, token)
        for track in tracks:
            trackcount += 1
            if matchArtist(track['track'], artist, token):
                try:
                    print 'Playlist: ' + playlist['name'] + ' Track: ' + track['track']['name'] + ' Artist: ' +  artist
                except:
                    next
    print trackcount
    print playlistcount

def run():
    while True:
        name = raw_input('What is the name of the artist you would like to search for: ')
        if name == "":
            break
        getAllMatches(name)

run()
