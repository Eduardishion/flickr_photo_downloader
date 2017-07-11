import flickrapi
import argparse
import os
import sys
import uuid
import time

from __init__ import api_secret
from __init__ import api_key

flickr = flickrapi.FlickrAPI(api_key,api_secret,cache=True)

def flickr_walk(keyward, limit):
    photos = flickr.walk(text=keyward,
                         tag_mode='all',
                         tags=keyward,
                         extras='url_c',
                         per_page=limit,
                         sort="relevance",
                         privacy_filter=1)
    print("### ")
    for photo in photos:
        try:
            url=photo.get('url_c')
            if url:
                # print(url)
                urls.append(url)
            if len(urls) >= limit:
                break
        except Exception as e:
            print('failed to download image')

def download_image(url,i):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:     #If the Current Version of Python is 3.0 or above
        import urllib.request    #urllib library for Extracting web pages
        try:
            urllib.request.urlretrieve(url, dest + prename + str(i) + ".jpg")
        except Exception as e:
            print(str(e))
    else:                        #If the Current Version of Python is 2.x
        import urllib2
        try:
            urllib.urlretrieve(url, dest + prename + str(i) + ".jpg")
        except:
            return"Page Not found"

if __name__ == "__main__":
    # parse command line options
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", help="the keyword to search")
    parser.add_argument("--limit", help="the limit for downloading image",
            type=int, default=50)
    args = parser.parse_args()
    print("Connecting to flickr to get {:d} photos with tag '{:s}'".format(args.limit, args.keyword))
    urls = []
    prename = uuid.uuid4().hex
    flickr_walk(args.keyword, args.limit)
    dest = "dl_images/" + args.keyword
    if not os.path.isdir(dest):
        os.makedirs(dest)
    dest += "/"
    i = 0
    for url in urls:
        i+=1
        sys.stdout.write("\r[{:d} / {:d}]  Getting:   {: <80}\r".format(i, args.limit, url))
        sys.stdout.flush()
        download_image(url,i)
    print("\r{: <100}\nDONE\n")
