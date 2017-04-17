#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
from PIL import Image
import PIL.ImageOps as ImageOps
import argparse

ASCII_CHARS = [ str(unichr(x)) for x in range(33,63)]


def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image

def map_pixels_to_ascii_chars(image):
    """Maps each pixel to an ascii char based on the range
    in which it lies.
    0-255 is mapped into ASCII_CHARS.
    """

    pixels_in_image = list(image.getdata())
    pixels_to_chars = []
    for pixel_value in pixels_in_image:
        if pixel_value == 0:
            pixels_to_chars.append(args.black)
        elif pixel_value == 255:
            pixels_to_chars.append(args.white)
        else:
            pixels_to_chars.append(ASCII_CHARS[pixel_value%len(ASCII_CHARS)])

    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, new_width=100):
    image = scale_image(image, new_width)
    # convert to grayscale
    image = image.convert('L')
    #invertion 
    if args.doInvert:
        image = ImageOps.invert(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in
            xrange(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath, size):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception, e:
        print "Unable to open image file {image_filepath}.".format(image_filepath=image_filepath)
        print e
        return

    if args.image_rotate:
        image = image.rotate(args.image_rotate)

    image_ascii = convert_image_to_ascii(image, size)
    return image_ascii

if __name__=='__main__':

    parser = argparse.ArgumentParser(prog='cowFactory.py', description='Convert image to cow files(*.cow)')
    parser.add_argument('-i', action='store_true', dest='doInvert', default=False, help='invert image') 
    parser.add_argument('-r', action='store', dest='image_rotate', type=int, help='rotate image by angle')
    parser.add_argument('-s', action='store', dest='ascii_size', type=int, default=100, help='ascii image size, defualt is 100')
    parser.add_argument('-w', action='store', dest='white', default=' ', help='character for white color, defualt is " "')
    parser.add_argument('-b', action='store', dest='black', default='#', help='character for black color, defualt is "#"')
    parser.add_argument('-a', action='store', dest='ascii_charts', help="specific characters for image, ex: '!#$`' or 'foo' ")
    parser.add_argument("image_file", help='Image file path')
    args = parser.parse_args()

    if args.ascii_charts:
        # override ascii table
        ASCII_CHARS = [ c for c in args.ascii_charts ]

    ascii_img = []
    ascii_img.extend("#\n# This is created by cowFactory.py\n#\n$the_cow = <<EOC;".splitlines())
    ascii_img.extend("    $thoughts\n     $thoughts\n".splitlines())
    ascii_img.append(handle_image_conversion(args.image_file, args.ascii_size))
    ascii_img.append("EOC")
    for line in ascii_img:
        print line

    sys.exit()
