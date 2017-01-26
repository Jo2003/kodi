import requests
from urlparse import parse_qsl
import sys
import json
import xbmcgui
import xbmc
import xbmcplugin

__rutube_api__ = "http://rutube.ru/api/"
__format__     = "json"
__traces__     = "yes"

base_url     = sys.argv[0]
addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'movies')

def myLog(what):
    if (__traces__ == "yes"):
        print "RutubeNew: {0}".format(what)

def rutube_get(function, search = None, an_id = None, page = 1, per_page = 20):
    url    = __rutube_api__ + function + "/"
    params = {}
    ret    = {}

    if an_id is not None:
        url += str(an_id) + "/"

    if search is not None:
        params["query"] = search

    params["format"]   = __format__
    params["limit"]    = per_page

    r = requests.get(url, params = params)

    myLog(r.url)

    if (r.status_code == 200):
        if search:
            myLog(r.content)
        ret = json.loads(r.content)
    else:
        ret = None
    return ret

def rutube_simple_get(url):
    ret = {}
    r   = requests.get(url)

    if (r.status_code == 200):
        ret = json.loads(r.content)
    else:
        ret = None
    return ret

def searchDlg(caption):
    return xbmcgui.Dialog().input(caption)

def list_categories(search = None, page = 1):

    categories = []

    # Get video categories
    if search is None:
        categories = rutube_get("tags")
    else:
        categories = rutube_get("search/tags", search = search)

    # Create a list for our items.
    listing = []

    # Iterate through categories
    for category in categories["results"]:

        # image ...
        image = ""
        plot  = ""

        if "picture" in category:
            image = category["picture"]
        elif "image" in category:
            image = category["image"]

        if "description" in category:
            plot = category["description"]

        list_item = xbmcgui.ListItem(label=category["name"], thumbnailImage=image)

        list_item.setInfo('video', {'title': category["name"], 'genre': category["name"], 'plot' : plot})
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = '{0}?action=listing&category={1}'.format(base_url, category["id"])
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))

    # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(addon_handle)

def create_root():
    # we need list items Tags, Videos, Channels and Search

    # Create a list for our items.
    listing = []

    list_item = xbmcgui.ListItem(label="Tags")
    url       = '{0}?action=tags'.format(base_url)
    is_folder = True
    listing.append((url, list_item, is_folder))

    list_item = xbmcgui.ListItem(label="TV")
    url       = '{0}?action=tv'.format(base_url)
    is_folder = True
    listing.append((url, list_item, is_folder))

    list_item = xbmcgui.ListItem(label="Search")
    url       = '{0}?action=searchmenu'.format(base_url)
    is_folder = True
    listing.append((url, list_item, is_folder))

    list_item = xbmcgui.ListItem(label="Stupid")
    url       = '{0}?action=stupid'.format(base_url)
    is_folder = False
    listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(addon_handle)

def list_searches():
    # we need list items Search Tags, Search Videos, Search Channels

    # Create a list for our items.
    listing = []

    list_item = xbmcgui.ListItem(label="Search Tags", iconImage='DefaultVideo.png')
    url       = '{0}?action=searchtagsform'.format(base_url)
    is_folder = True
    listing.append((url, list_item, is_folder))

    list_item = xbmcgui.ListItem(label="Search Videos", iconImage='DefaultVideo.png')
    url       = '{0}?action=searchvideosform'.format(base_url)
    is_folder = True
    listing.append((url, list_item, is_folder))

    list_item = xbmcgui.ListItem(label="Search Channels", iconImage='DefaultVideo.png')
    url       = '{0}?action=searchchannelsform'.format(base_url)
    is_folder = True
    listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(addon_handle)


def list_videos(search = None):
    return None

def list_tv(search = None):
    tvShows = []

    # Get video categories
    if search is None:
        tvShows = rutube_get("metainfo/tv")
    else:
        tvShows = rutube_get("search/video", search = search)

    # Create a list for our items.
    listing = []

    # Iterate through categories
    for show in tvShows["results"]:

        # image ...
        image = ""
        plot  = ""

        if "picture" in show:
            image = show["picture"]
        elif "image" in show:
            image = show["image"]

        if "description" in show:
            plot = show["description"]

        list_item = xbmcgui.ListItem(label=show["name"], thumbnailImage=image)

        list_item.setInfo('video', {'title': show["name"], 'genre': show["name"], 'plot' : plot})
        list_item.setArt({'poster' : show['poster_url']})
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = '{0}?action=listtv&tvid={1}'.format(base_url, show["id"])
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))

    # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(addon_handle)


def play_video(vid):

    title   = ""
    genre   = ""
    videoId = 0

    if isinstance(vid, dict):
        if "id" in vid:
            videoId = int(vid["id"])

        if "title" in vid:
            title = vid["title"]

        if "genre" in vid:
            genre = vid["genre"]

    else:
        videoId = int(vid)

    if not title:
        title = "RuTube Video #{0}".format(videoId)

    if not genre:
        genre = "RuTube Video"

    list_item = xbmcgui.ListItem(title)
    list_item.setInfo('video', {'Title': title, 'Genre': genre})

    resp = rutube_get("play/options", an_id = vid)
    xbmc.Player().play(resp["video_balancer"]["m3u8"], list_item)

def search_tags():
    query  = searchDlg("Search Tags")
    search = None
    if query:
        search = query
        print "Searching for " + search

    list_categories(search)

def stupid():
    play_video(6089719)


##
## @brief      parse parameter string and route into correct direction
##
## @param      paramstring  The paramstring
##
##
def router(paramstring):

    params = dict(parse_qsl(paramstring))
    search = None

    # Check the parameters passed to the plugin
    if 'action' in params:
        if params['action'] == 'tags':
            search = None
            if 'search' in params:
                search = params['search']
            list_categories(search)
        elif params['action'] == 'videos':
            search = None
            if 'search' in params:
                search = params['search']
            list_videos(search)
        elif params['action'] == 'tv':
            search = None
            if 'search' in params:
                search = params['search']
            list_tv(search)
        elif params['action'] == 'searchtagsform':
            search_tags()
        elif params['action'] == 'searchmenu':
            list_searches()
        elif params['action'] == 'stupid':
            stupid()
        else:
            create_root()
    else:
        create_root()

## program entry ...
if __name__ == '__main__':
    router(sys.argv[2][1:])
