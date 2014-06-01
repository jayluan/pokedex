from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys
import re

#The reason we have to scrape like this is because the true URL of the pokemon image contains different unpredictable paths 
#even though the file name is predictable
def scape_pokemon(url, out_folder="/test/", pokemon_id=1):
    """Downloads all the images at 'url' to /test/"""

    #first we want to make sure that we know what the title of the pictures contain, which is part of the URL
    target_file = re.search(r"(\w+).png", url)
    target_fname = target_file.group(0)
    generation = re.search(r"Spr_(\w+)_\d+",  target_fname).group(1)
    soup = bs(urlopen(url))
    parsed = list(urlparse.urlparse(url))

    scraped_list = []
    for image in soup.findAll("img"):
        
        filename = image["src"].split("/")[-1]

        #make sure we got the file that we actually want on the page
        if( filename != target_fname):
            continue
        parsed[2] = image["src"]
        outname = "pokemon-" + str(pokemon_id) + "-" + generation + ".png"
        outpath = os.path.join(out_folder, outname)
        
        #make sure we're not downloading duplicates from the page        
        if(filename in scraped_list):
            continue

        if image["src"].lower().startswith("http"):
            urlretrieve(image["src"], outpath)
        else:
            urlretrieve(urlparse.urlunparse(parsed), outpath)

        print "Scraped Image: %(src)s" % image
        scraped_list.append(filename);

def _usage():
    print "usage: python dumpimages.py http://example.com [outpath]"

if __name__ == "__main__":
    # url = sys.argv[-1]
    # out_folder = "/test/"
    # if not url.lower().startswith("http"):
    #     out_folder = sys.argv[-1]
    #     url = sys.argv[-2]
    #     if not url.lower().startswith("http"):
    #         _usage()
    #         sys.exit(-1)

    #assemble URLs and do for loop
    url = "http://bulbapedia.bulbagarden.net/wiki/File:Spr_3r_150.png"
    pokemon_id = 150
    url_head = "http://bulbapedia.bulbagarden.net/wiki/File:Spr_"
    sprite_types = ['2g', '2s', '1b', '3r', '4d', '5b', '4p', '1y']
    for generation in sprite_types:
        for i in range(1,152):
            url = url_head + generation + "_" + '%03d'%i + '.png'
            scape_pokemon(url, '', i)

