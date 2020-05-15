import math
import re
from PIL import Image

from staticfiles_processor import StaticfileProcessor

arguments_pattern = re.compile(r'[\w/]+.image\[(\S+)\].?\w*')
image_pattern = re.compile(r'[\w/]+(.image\[\S+\]).?\w*')


def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


def create_gradient(size, outer_color, inner_color):
    imgsize = size
    image = Image.new('RGB', imgsize)  # Create the image

    for y in range(imgsize[1]):
        for x in range(imgsize[0]):

            #Find the distance to the center
            distanceToCenter = math.sqrt((x - imgsize[0]/2) ** 2 + (y - imgsize[1]/2) ** 2)

            #Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCenter) / (math.sqrt(2) * imgsize[0]/2)

            #Calculate r, g, and b values
            r = outer_color[0] * distanceToCenter + inner_color[0] * (1 - distanceToCenter)
            g = outer_color[1] * distanceToCenter + inner_color[1] * (1 - distanceToCenter)
            b = outer_color[2] * distanceToCenter + inner_color[2] * (1 - distanceToCenter)

            #Place the pixel        
            image.putpixel((x, y), (int(r), int(g), int(b)))
    return image


def get_arguments(match):
    return {a[0]: a[1] for a in [m.split('=') for m in match.split('|')]}


class ImageProcessor(StaticfileProcessor):
    def check_match(self, path, match):
        return re.match(arguments_pattern, path)

    def process(self, destination, origin):
        arguments = get_arguments(re.search(arguments_pattern, destination).group(1))
        pat = r'[\w/\-_]+(.image\[\S+\]).?\w*'
        clean = re.match(pat, origin)
        source = origin.replace(clean.group(1), '')
        img = Image.open(source)
        if 'size' in arguments:
            new_size = tuple(int(s) for s in arguments['size'].split('x'))
            img = img.resize(new_size, Image.ANTIALIAS)
        if 'background' in arguments:
            background = tuple(c for c in arguments['background'].split('x'))
            if len(background) > 1:
                img_bg = create_gradient(img.size, hex_to_rgb(background[0]), hex_to_rgb(background[1]))
            else:
                img_bg = Image.new('RGB', img.size, '#{}'.format(background[0]))
            img_bg.paste(img, (0, 0), img)
            img = img_bg
        img.save(destination)
        pass
