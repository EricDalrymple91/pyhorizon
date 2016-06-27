# Pyhorizon v0.2

Pyhorizon is a thin Python wrapper for the [NASA API](https://api.nasa.gov/index.html). As of 6/28/2016, APOD, Asteroids-NeoWs, Earth, Mars rover photos, patents and sounds are supported in full. After sending a 
request, you can check your rate limit by calling a built in attribute to see how many requests you have left. Pyhorizon allows you to easily search NASA data and have a great time doing so.

# Table of Contents

+ [Obtaining Pyhorizon](#obtaining-pyhorizon)
+ [Using Pyhorizon](#using-pyhorizon)
	+ [Astronomy Picture of the Day](#astronomy-picture-of-the-day)
	+ [Asteroids](#asteroids)
	+ [Earth](#earth)
	+ [Mars Rovers Photos](#mars-rovers-photos)
	+ [Patents](#patents)
	+ [Sounds](#sounds)
	+ [Save Image URLs](#save-image-urls)
+ [Changelog](#changelog)
+ [Attribution](#attribution)
+ [License](#license)

# Obtaining Pyhorizon

You can get Pyhorizon using pip install:

	pip install pyhorizon
	
OR:

Going [here](https://github.com/EricDalrymple91/pyhorizon) :octocat:, downloading the zip file and running the setup file:

	python setup.py install

# Using Pyhorizon

To start, you need to import *pyhorizon* and create an instance from it. By default, the API key used will be *DEMO_KEY*. However, I would suggest going [here](https://api.nasa.gov/index.html#apply-for-an-api-key) and applying for a NASA API key. With your own API key, you can make far more [requests](https://api.nasa.gov/api.html#web-service-rate-limits). 

All standard methods will return the response body JSON object as a dictionary.

Examples:

```python
from pyhorizon import Horizon

apollo = Horizon()

# Or if you have your own api key
apollo = Horizon(key='YOUR_API_KEY')

# Return the amount of requests left
print(apollo.rate_limit_remaining)
```

### Astronomy Picture of the Day

Return information for NASA's APOD imagery. You can query by date and hd images.

[NASA API documentation link](https://api.nasa.gov/api.html#apod)

Method:

* apod(**kwargs)

Examples:

```python
# Return APOD dictionary object for current date
print(apollo.apod())

# Lookup a particular date
print(apollo.apod(date='205-8-27'))

# Lookup a particular date and return hd imagery if possible
print(apollo.apod(date='2015-01-04', hd=True))
```

### Asteroids

Return near earth asteroid information. You can find asteroids by their id, get feeds from dates, browse or get stats.

[NASA API documentation link](https://api.nasa.gov/api.html#NeoWS)

Methods:

* neo_feed(start_date, end_date)
* neo_feed_today()
* neo_lookup(asteroid_id)
* neo_browse(**kwargs)
* neo_stats()

Examples:
```python
# Lookup a particular asteroid
print(apollo.neo_lookup(3542519))

# Lookup today's feed
print(apollo.neo_feed_today())

# Lookup a particular date range
print(apollo.neo_feed('2015-09-07', '2015-09-08'))

# Browse NEOs
print(apollo.neo_browse())

# Lookup all asteroids from a browse request
neos = apollo.neo_browse(page=1, size=20)
for neo in neos['near_earth_objects']:
	print(apollo.neo_lookup(n['neo_reference_id']))
```

### Earth

Return landsat 8 imagery and information regarding the last time imagery was taken for a location.

[NASA API documentation link](https://api.nasa.gov/api.html#earth)

Methods:

* imagery(**kwargs)
* assets(**kwargs)

Examples:
```python
print(apollo.imagery())

# Find imagery for a particular location and date
print(apollo.imagery(lat=1.5, lon=100.75, date='2015-8-27', cloud_score=True))

# Find assets
print(apollo.assets())
print(apollo.assets(lat=1.5, lon=100.75, begin='2014-02-01', end='2014-02-05'))
```

### Mars Rover Photos

Return photos by either martian sol or earth date given a mars rover. You can further query by 
camera.

[NASA API documentation link](https://api.nasa.gov/api.html#MarsPhotos)

Attributes:

* rovers
* cameras

Methods:

* martian_sol(rover, sol, **kwargs)
* earth_date(rover, date, **kwargs)

Examples
```python
# View available mars rovers as a list
print(apollo.rovers)

# View cameras and their rover availability as a dictionary
print(apollo.cameras)

# Find images for all cameras based on martian sol
print(apollo.martian_sol('opportunity', 1000))

# Find images for a particular camera and page-set
print(apollo.martian_sol('opportunity', 1000, camera='NAVCAM', page=1))

# Find images for all cameras based on earth date
print(apollo.earth_date('curiosity', '2015-8-27'))
```

### Patents

Return NASA patent information.

[NASA API documentation link](https://api.nasa.gov/api.html#patents)

Methods:

* patents(**kwargs)

Examples
```python
print(apollo.patents())

# Lookup particular patents
print(apollo.patents(query='temperature'))

# Return a particular threshold of patents
print(apollo.patents(limit=3))
```

### Sounds

Return space sounds with sound cloud links.

[NASA API documentation link](https://api.nasa.gov/api.html#sounds)

Methods:

* sounds(**kwargs)

Examples
```python
print(apollo.sounds())

# Search for particular sounds
print(apollo.sounds(q='apollo'))

# Return limited sounds
print(apollo.sounds(limit=2))
```

### Save Image URLs

Extra methods are included in Horizon to save and search for images in the request response objects.

Methods:

* save_img(img, directory, name)
* image_walk(response_body, directory, name)

Examples
```python
response = apollo.earth_date('curiosity', '2015-6-27')

# Default directory is the current working directory, and default name is image
# Save an image url from a response body
apollo.save_img(response['photos'][0]['img_src'], directory='C:\Users\TestUser\Photos', name='big mars')

# Save all images in a response body. Scans for 'img_src' keys and then 'url' or 'hd_url' keys
apollo.image_walk(response, directory='C:\Users\TestUser\Photos', name='mars bar')
```

# Changelog

### 0.2 (2016-6-26)

- General reformatting

### 0.1 (2016-6-23)

- Initial release.

# Attribution

Horizion isn't endorsed by [NASA](https://www.nasa.gov/) and doesn't reflect the views or opinions of NASA or anyone officially involved in producing or managing NASA or the NASA API. 

# License

The MIT License (MIT)
