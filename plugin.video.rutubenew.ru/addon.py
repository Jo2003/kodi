import requests
from urlparse import parse_qsl
import sys
import json
import xbmcgui
import xbmcplugin

__rutube_api__ = "http://rutube.ru/api/"
__format__     = "json"

base_url     = sys.argv[0]
addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'movies')


def rutube_get(function, search = None, an_id = None):
    url    = __rutube_api__ + function + "/"
    params = {}
    ret    = {}

    if an_id is not None:
        url += an_id + "/"

    if search is not None:
        params["query"] = search

    params["format"] = __format__

    r = requests.get(url, data = params)

    if (r.status_code == 200):
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

def searchDlg(caption, function):
    ret           = { "function" : str(function) }
    ret["search"] = xbmcgui.Dialog().input(caption)
    return ret

def list_categories():

    # Get video categories
    categories = rutube_get("tags")

    # Create a list for our items.
    listing = []

    # Iterate through categories
    for category in categories["results"]:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category["name"], thumbnailImage=category["picture"])
        # Set a fanart image for the list item.
        # Here we use the same image as the thumbnail for simplicity's sake.
        # list_item.setProperty('fanart_image', VIDEOS[category][0]['thumb'])
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': category["name"], 'genre': category["name"], 'plot' : category["description"]})
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

def list_videos(tagis):
    return None

def play_video(url):
    return None

##
## @brief      parse parameter string and route into correct direction
##
## @param      paramstring  The paramstring
##
##
def router(paramstring):

    params = dict(parse_qsl(paramstring))

    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()

## program entry ...
if __name__ == '__main__':
    router(sys.argv[2][1:])
