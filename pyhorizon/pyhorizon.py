"""
horizon
~~~~~~~~~~~~
This module is a thin wrapper for the NASA API.
https://api.nasa.gov/index.html

:copyright: (c) 2016 by Eric Dalrymple.
:license: The MIT License (MIT), see LICENSE for more details.
"""
import requests
import os


class HorizonException(Exception):

    def __init__(self, error, response):
        self.error = error
        self.response = response
        self.headers = response.headers

    def __str__(self):
        return self.error

    def __eq__(self, other):
        if isinstance(other, "".__class__):
            return self.error == other
        elif isinstance(other, self.__class__):
            return self.error == other.error and self.headers == other.headers
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return super(HorizonException).__hash__()


def raise_status(response):
    """Raise an exception if the request did not return a status code of 200.

    :param response: Request response body
    """
    if response.status_code != 200:
        if response.status_code == 401:
            raise HorizonException('Unauthorized', response)
        elif response.status_code == 403:
            raise HorizonException('Forbidden', response)
        elif response.status_code == 404:
            raise HorizonException('Not Found', response)
        else:
            response.raise_for_status()


def find_in_response(obj, condition, path=[]):
    """Recursively search through a dict to find full paths.

    The search will return all paths that fit the criteria, whether they are keys or values. An empty list will be
    returned if there are not matches.

    :param obj: Dictionary response object
    :param condition: Key or value
    :param path: The path being built by looking through the dictionary
    :return: Generator of paths
    """
    if isinstance(obj, list):
        for index, value in enumerate(obj):
            new_path = list(path)
            new_path.append(index)
            for result in find_in_response(value, condition, path=new_path):
                yield result

    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = list(path)
            new_path.append(key)
            for result in find_in_response(value, condition, path=new_path):
                yield result

            if condition == key:
                new_path = list(path)
                new_path.append(key)
                yield new_path

            elif condition == value:
                new_path = list(path)
                new_path.append(key)
                new_path.append(value)
                yield new_path


class Horizon(object):

    version = '0.0.1'
    asteroids_neows_version = '1'
    mars_rovers_photos_version = '1'
    rovers = ['Curiosity', 'Opportunity', 'Spirit']
    cameras = {'FHAZ': {'full_name': 'Front Hazard Avoidance Camera',
                        'rovers': ['Curiosity', 'Opportunity', 'Spirit']},
               'RHAZ': {'full_name': 'Rear Hazard Avoidance Camera',
                        'rovers': ['Curiosity', 'Opportunity', 'Spirit']},
               'MAST': {'full_name': 'Mast Camera',
                        'rovers': ['Curiosity']},
               'CHEMCAM': {'full_name': 'Chemistry and Camera Complex',
                           'rovers': ['Curiosity']},
               'MAHLI': {'full_name': 'Mars Hand Lens Imager',
                         'rovers': ['Curiosity']},
               'MARDI': {'full_name': 'Mars Descent Imager',
                         'rovers': ['Curiosity']},
               'NAVCAM': {'full_name': 'Navigation Camera',
                          'rovers': ['Curiosity', 'Opportunity', 'Spirit']},
               'PANCAM': {'full_name': 'Panoramic Camera',
                          'rovers': ['Opportunity', 'Spirit']},
               'MINITES': {'full_name': 'Miniature Thermal Emission Spectrometer (Mini-TES)',
                           'rovers': ['Opportunity', 'Spirit']}}

    def __init__(self, key='DEMO_KEY'):
        self.key = key
        self.rate_limit_remaining = 'Unknown'

    def base_request(self, url, **kwargs):
        args = {'api_key': self.key}
        for k in kwargs:
            if kwargs[k] is not None:
                args[k] = kwargs[k]
        r = requests.get('https://api.nasa.gov/{url}'.format(
            url=url
            ),
            params=args
        )
        raise_status(r)
        self.rate_limit_remaining = r.headers['X-RateLimit-Remaining']
        return r.json()

    def apod(self, **kwargs):
        """Retrieve information and the image url for NASA's astronomy picture of the day.

        Example Query: https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY

        Link: https://api.nasa.gov/api.html#apod

        :param **kwargs: Optional arguments that 'request' takes (date, hd).
        :return: Apod request response body.
        """
        return self.base_request('planetary/apod', **kwargs)

    def martian_sol(self, rover, sol, **kwargs):
        """Retrieve image urls and information for data gathered by NASA's Curiosity, Opportunity, and Spirit
        rovers on mars based on the entered rover and martian sol.

        Example Query: https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=fhaz&api_key=DEMO_KEY

        Link: https://api.nasa.gov/api.html#MarsPhotos

        :param rover: Mars rover.
        :param sol: Martian sol.
        :param **kwargs: Optional arguments that 'request' takes (camera, page).
        :return: Mars rover photos and information request response body.
        """
        return self.base_request('/mars-photos/api/v{version}/rovers/{rover}/photos'.format(
            version=self.mars_rovers_photos_version,
            rover=rover
            ),
            sol=sol,
            **kwargs
        )

    def earth_date(self, rover, date, **kwargs):
        """Retrieve image urls and information for data gathered by NASA's Curiosity, Opportunity, and Spirit
        rovers on mars based on the entered rover and earth date.

        Example Query: https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date=2015-6-3&api_key=DEMO_KEY

        Link: https://api.nasa.gov/api.html#MarsPhotos

        :param rover: Mars rover.
        :param date: Date on earth.
        :param **kwargs: Optional arguments that 'request' takes (camera, page).
        :return: Mars rover photos and information request response body.
        """
        return self.base_request('/mars-photos/api/v{version}/rovers/{rover}/photos'.format(
            version=self.mars_rovers_photos_version,
            rover=rover
            ),
            earth_date=date,
            **kwargs
        )

    def imagery(self, **kwargs):
        """Retrieve the landsat 8 image for the entered location and date.

        Example Query: https://api.nasa.gov/planetary/earth/imagery?lon=100.75&lat=1.5&date=2014-02-01&cloud_score=True&api_key=DEMO_KEY

        Link: https://api.nasa.gov/api.html#imagery

        :param **kwargs: Optional arguments that 'request' takes (lat, lon, dim, date, cloud score).
        :return: Earth imagery request response body.
        """
        return self.base_request('planetary/earth/imagery', **kwargs)

    def assets(self, **kwargs):
        """Retrieves the date-times and asset names for available NASA landsat 8 imagery for the entered location.

        Example Query: https://api.nasa.gov/planetary/earth/assets?lon=100.75&lat=1.5&begin=2014-02-01&api_key=DEMO_KEY

        Link: https://api.nasa.gov/api.html#assets

        :param **kwargs: Optional arguments that 'request' takes (lat, lon, begin, end).
        :return: Earth assets request response body.
        """
        return self.base_request('planetary/earth/assets', **kwargs)

    def neo_feed(self, start_date, end_date):
        """Retrieve a list of asteroids based on their closest approach date to earth.

        Example Query: https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key=DEMO_KEY

        Link: https://api.nasa.gov/api.html#neows-feed

        :param start_date: Starting date for asteroid search
        :param end_date: Ending date for asteroid search
        :return: Neo feed request response body.
        """
        return self.base_request('/neo/rest/v{version}/feed'.format(
            version=self.asteroids_neows_version
            ),
            start_date=start_date,
            end_date=end_date
        )

    def neo_feed_today(self):
        """Retrieve a list of asteroids based on how close they are to earth on the day ran.

        Example Query: https://api.nasa.gov/neo/rest/v1/feed/today?api_key=DEMO_KEY

        Link: https://api.nasa.gov/neo/?api_key=DEMO_KEY

        :return: Neo feed today request response body.
        """
        return self.base_request('neo/rest/v{version}/feed/today'.format(version=self.asteroids_neows_version))

    def neo_lookup(self, asteroid_id):
        """Lookup a specific asteroid.

        Example Query: https://api.nasa.gov/neo/rest/v1/neo/3542519?api_key=DEMO_KEY

        Link: https://api.nasa.gov/api.html#neows-lookup

        :param asteroid_id: Identification number of an asteroid
        :return: Neo lookup request response body.
        """
        return self.base_request('neo/rest/v{version}/neo/{asteroid_id}'.format(
            version=self.asteroids_neows_version,
            asteroid_id=asteroid_id
            )
        )

    def neo_browse(self, **kwargs):
        """Browse the overall asteroid data-set.

        Example Query: https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=DEMO_KEY

        Link: https://api.nasa.gov/api.html#neows-lookup

        :param **kwargs: Optional arguments that 'request' takes (page, size).
        :return: Neo browse request response body.
        """
        return self.base_request('neo/rest/v{version}/neo/browse/'.format(
            version=self.asteroids_neows_version
            ),
            **kwargs
        )

    def neo_stats(self):
        """Browse asteroid stats.

        Example Query: https://api.nasa.gov/neo/rest/v1/stats?api_key=DEMO_KEY

        Link: https://api.nasa.gov/neo/?api_key=DEMO_KEY

        :return: Neo stats request response body.
        """
        return self.base_request('neo/rest/v{version}/stats'.format(version=self.asteroids_neows_version))

    def patents(self, **kwargs):
        """Retrieve a list of NASA patents.

        Example Query: https://api.nasa.gov/patents/content?query=temperature&limit=5&api_key=DEMO_KEY

        Link: https://api.nasa.gov/api.html#patents

        :param **kwargs: Optional arguments that 'request' takes (query, concept_tags, limit).
        :return: Patents request response body.
        """
        return self.base_request('/patents/content', **kwargs)

    def sounds(self, **kwargs):
        """Return a dictionary of NASA recorded sounds from space. Hosted via sound cloud.

        Example Query: https://api.nasa.gov/planetary/sounds?q=apollo&api_key=DEMO_KEY

        Link: https://api.nasa.gov/api.html#sounds

        :param **kwargs: Optional arguments that 'request' takes (q, limit).
        :return: Sounds information and links request response body.
        """
        return self.base_request('planetary/sounds', **kwargs)

    @staticmethod
    def save_image(img, directory=os.getcwd(), name='image'):
        """Save an image from a URL.

        :param img: Image URL
        :param directory: Image save location
        :param name: Name that will be given to output image
        """
        ext = os.path.splitext(img)[1].lower()
        if not ext:
            ext = '.jpg'
        with open(os.path.join(directory, '{name}{ext}'.format(name=name, ext=ext)), 'wb') as i:
            i.write(requests.get(img).content)

    def image_walk(self, response_body, directory=os.getcwd(), name='image'):
        """Save all images in a response body by searching through it.

        :param response_body: Request response body
        :param directory: Image(s) save location
        :param name: Name that will be given to output image(s)
        """
        finds = list(find_in_response(response_body, 'img_src'))
        if len(finds) == 0:
            finds = list(find_in_response(response_body, 'url')) + list(find_in_response(response_body, 'hdurl'))
        for i, find in enumerate(finds):
            image = response_body
            for value in find:
                image = image[value]
            self.save_image(image, directory, name='{name}{count}'.format(name=name, count=i+1))

