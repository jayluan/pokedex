
import os
from PIL import Image
import Image

def crop(Path,input,height,width,i,k,page,area):
    im = Image.open(input)
    imgwidth, imgheight = im.size
    for i in range(0,imgheight,height):
        for j in range(0,imgwidth,width):
            box = (j, i, j+width, i+height)
            a = im.crop(box)
            try:
                o = a.crop(area)
                o.save(os.path.join(Path,"%s" % page,"pokemon-%s.png" % k))
            except:
                pass
            k +=1



if __name__ == "__main__":
    crop('./', '151.png', 96, 96, 0, 1, '', (0,0,96,96))
