from django.shortcuts import render
from .models import Song , Album ,Artist
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials 
import unicodedata

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="55264f7f45324bee82ccd9f0c03b31a4",  client_secret="079db58f7cfd4373ab30378566a15938"))

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
		Song.objects.all().delete()
		Album.objects.all().delete()
		Artist.objects.all().delete()
		if 'r' in request.GET:
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
		if 'p' in request.GET:
			try:
				results = sp.search(q=searchname, limit=10, type='album')
				print(results)
				for i,t in enumerate(results['albums']['items']):
					theTitle = t['name']
					if not t['images']:
						theImage = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
					else:
						theImage = t['images'][0]['url']
					theId = t['id']
					someting = sp.album(theId)
					releaseDate = someting['release_date']
					popularity = float(someting['popularity'])
					theType = someting['album_type']
					theExternal = t['external_urls']['spotify']
					theURI = t['uri']
					theMainArtist = t['artists'][0]['name']
					somelist = [x['name'] for x in t['artists']]
					theArtists = ', '.join(somelist)
					thatList = [str(x) for x in t['available_markets']]
					theMarkets = ', '.join(thatList)
					stringDate = unicodedata.normalize('NFKD', releaseDate).encode('ascii','ignore')
					theYear = stringDate[:4]
					print(11)
					theAlbum = Album.objects.create(year=theYear,title=theTitle,theType=theType,popularity=popularity,releaseDate=releaseDate,query=searchname,image=theImage,albumId=theId,external=theExternal,uri=theURI,mainArtist=theMainArtist,artists=theArtists,artistId='no')
					musicData = Album.objects.filter(query=searchname)
			except:
				musicData = "there is a album error"
		if 'yo' in request.GET:
			try:
				results = sp.search(q=searchname, limit=10, type='album')
				for i,t in enumerate(results['albums']['items']):
					theTitle = t['name']
					#print t['name']
					if not t['images']:
						theImage = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
					else:
						theImage = t['images'][0]['url']
					theId = t['id']
					someting = sp.album(theId)
					releaseDate = someting['release_date']
					popularity = float(someting['popularity'])
					theType = someting['album_type']
					theExternal = t['external_urls']['spotify']
					theURI = t['uri']
					theMainArtist = t['artists'][0]['name']
					somelist = [x['name'] for x in t['artists']]
					theArtists = ', '.join(somelist)
					thatList = [str(x) for x in t['available_markets']]
					theMarkets = ', '.join(thatList)
					stringDate = unicodedata.normalize('NFKD', releaseDate).encode('ascii','ignore')
					theYear = stringDate[:4]
					theAlbum = Album.objects.create(year=theYear,title=theTitle,theType=theType,popularity=popularity,releaseDate=releaseDate,query=searchname,image=theImage,albumId=theId,external=theExternal,uri=theURI,mainArtist=theMainArtist,artists=theArtists,artistId='no')
					musicData = Album.objects.filter(query=searchname).order_by('-popularity')
			except:
				musicData = "there is a album error"
		if 'n' in request.GET:
			try:
				results = sp.search(q=searchname, limit=50, type='artist')
				for i,t in enumerate(results['artists']['items']):
					name = t['name']
					artistId = t['id']
					genres = [x for x in t['genres']]
					theGenres = ', '.join(genres)
					external = t['external_urls']['spotify']
					uri = t['uri']
					if not t['images']:
						image = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
					else:
						image = t['images'][0]['url']
					popularity = float(t['popularity'])
					numOfFollowers = t['followers']
					theArtist = Artist.objects.create(name=name,query=searchname,artistId=artistId,genres=theGenres,external=external,uri=uri,image=image,popularity=popularity,numOfFollowers=numOfFollowers,songId="None",albumId="None")
					musicData = Artist.objects.filter(query=searchname)
			except:
				musicData = "there is a artist error"
		if 'b' in request.GET:
			try:
				results = sp.search(q=searchname, limit=50, type='artist')
				for i,t in enumerate(results['artists']['items']):
					name = t['name']
					artistId = t['id']
					genres = [x for x in t['genres']]
					theGenres = ', '.join(genres)
					external = t['external_urls']['spotify']
					uri = t['uri']
					if not t['images']:
						image = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
					else:
						image = t['images'][0]['url']
					popularity = float(t['popularity'])
					numOfFollowers = t['followeres']
					theArtist = Artist.objects.create(name=name,query=searchname,artistId=artistId,genres=theGenres,external=external,uri=uri,image=image,popularity=popularity,numOfFollowers=numOfFollowers,songId="None",albumId="None")
					musicData = Artist.objects.filter(query=searchname).order_by('-popularity')
			except:
				musicData = "there is a artist error"
		print(musicData)
		return render(request, 'search.html',{'musicData': musicData, 'search': True})
	else:
		return render(request, 'search.html')  
