import Image as img
import os, sys

def resize_dir(in_dir, out_dir, width, height):
    #get png files in the input directory
    files = [f for f in os.listdir(in_dir) if os.path.splitext(f)[1] == '.png']

    #if output directory doesn't exist, create it
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    #resize and write them
    for image in files:
        im = img.open(os.path.join(in_dir,image))
        im_out = im.resize( (width, height), img.BICUBIC)
        outpath = os.path.join(out_dir, image)
        im_out.save(outpath)

if __name__ == "__main__":
    width = 192
    height = 192
    
    resize_dir('./bulbapedia/', './bulbapedia_resized/', width, height)




















