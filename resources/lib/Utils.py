# -*- coding: utf8 -*-

# Copyright (C) 2016- Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcgui
import xbmcvfs
import xbmcplugin
import requests
import os
import sys
import time
import simplejson as json

from kodi65 import addon


def get_http(url=None, headers=False):
    """
    fetches data from *url, returns it as a string
    """
    succeed = 0
    if not headers:
        headers = {'User-agent': 'XBMC/16.0 ( phil65@kodi.tv )'}
    while (succeed < 2) and (not xbmc.abortRequested):
        try:
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                raise Exception
            return r.text
        except Exception:
            log("get_http: could not get data from %s" % url)
            xbmc.sleep(1000)
            succeed += 1
    return None


def log(txt):
    if isinstance(txt, str):
        txt = txt.decode("utf-8", 'ignore')
    message = u'%s: %s' % (addon.ID, txt)
    xbmc.log(msg=message.encode("utf-8", 'ignore'),
             level=xbmc.LOGDEBUG)


def save_to_file(content, filename, path=""):
    """
    dump json and save to *filename in *path
    """
    if not path:
        return None
    else:
        if not xbmcvfs.exists(path):
            xbmcvfs.mkdirs(path)
        text_file_path = os.path.join(path, filename + ".txt")
    now = time.time()
    text_file = xbmcvfs.File(text_file_path, "w")
    json.dump(content, text_file)
    text_file.close()
    log("saved textfile %s. Time: %f" % (text_file_path, time.time() - now))
    return True

def read_from_file(path="", raw=False):
    """
    return data from file with *path
    """
    if not path:
        return None
    if not xbmcvfs.exists(path):
        return False
    try:
        with open(path) as f:
            log("opened textfile %s." % (path))
            if not raw:
                result = json.load(f)
            else:
                result = f.read()
        return result
    except:
        log("failed to load textfile: " + path)
        return False

def add_image(item, total=0):
    liz = xbmcgui.ListItem(str(item["index"]),
                           iconImage="DefaultImage.png",
                           thumbnailImage=item["thumb"])
    liz.setInfo(type="image",
                infoLabels={"Id": item["label"]})
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                       url=item["thumb"],
                                       listitem=liz,
                                       isFolder=False,
                                       totalItems=total)
