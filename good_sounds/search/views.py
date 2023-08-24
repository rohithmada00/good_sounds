from django.shortcuts import render
from .models import Song 
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials 

def convertMillis(millis):
	mill = float(millis)
	seconds=(mill/1000)%60
	seconds = str(seconds)
	minutes=(mill/(1000*60))%60
	minutes = str(minutes)
	return minutes + ":" + seconds

def search(request):
	if request.GET:
		searchname = request.GET.get('q')
		if 'r' in request.GET:
			Song.objects.all().delete()
			sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="55264f7f45324bee82ccd9f0c03b31a4",  client_secret="079db58f7cfd4373ab30378566a15938"))
			results = sp.search(q=searchname, limit=50, type='track')
			for i,t in enumerate(results['tracks']['items']):
				theTitle = t['name']
				theAlbum = t['album']['name']
				theId = t['id']
				thePreview = t['preview_url']
				theExternal = t['external_urls']['spotify']
				theURI = t['uri']
				theDuration = convertMillis(t['duration_ms'])
				theMainArtist = t['artists'][0]['name']
				somelist = [x['name'] for x in t['artists']]
				theArtists = ', '.join(somelist)
				thePopularity = t['popularity']
				thatList = [str(x) for x in t['available_markets']]
				theMarkets = ', '.join(thatList)
				#print theTitle
				theImage = t['album']['images'][0]['url']
				theSong = Song.objects.create(title=theTitle,query=searchname,album=theAlbum,songId=theId,preview=thePreview,external=theExternal,uri=theURI,duration=theDuration,mainArtist=theMainArtist,artists=theArtists,popularity=thePopularity,markets=theMarkets, image=theImage)
				musicData = Song.objects.filter(query=searchname)
		if 'j' in request.GET:
			Song.objects.all().delete()
			results = sp.search(q=searchname, limit=50, type='track')
			for i,t in enumerate(results['tracks']['items']):
				theTitle = t['name']
				theAlbum = t['album']['name']
				theId = t['id']
				thePreview = t['preview_url']
				theExternal = t['external_urls']['spotify']
				theURI = t['uri']
				theDuration = convertMillis(t['duration_ms'])
				theMainArtist = t['artists'][0]['name']
				somelist = [x['name'] for x in t['artists']]
				theArtists = ', '.join(somelist)
				thePopularity = t['popularity']
				thatList = [str(x) for x in t['available_markets']]
				theMarkets = ', '.join(thatList)
				theImage = t['album']['images'][0]['url']
				#print theTitle
				theSong = Song.objects.create(title=theTitle,query=searchname,album=theAlbum,songId=theId,preview=thePreview,external=theExternal,uri=theURI,duration=theDuration,mainArtist=theMainArtist,artists=theArtists,popularity=thePopularity,markets=theMarkets, image=theImage)
				musicData = Song.objects.filter(query=searchname).order_by('-popularity')
		return render(request, 'search.html',{'musicData': musicData, 'search': True})
	else:
		return render(request, 'search.html')  
