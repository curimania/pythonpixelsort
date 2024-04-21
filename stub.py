from PIL import Image
from tqdm import tqdm
import argparse
from random import randint

parser = argparse.ArgumentParser(description="Pixelsortiert das Input-Image")
parser.add_argument('image', metavar='I', type=str, help='das zu sortierende Bild')
parser.add_argument('-minInterval', type=int, required=False, help='minimale Interval Laenge', default=10)
parser.add_argument('-maxInterval', type=int, required=False, help='maximale Interval Laenge', default=100)
parser.add_argument('-output', type=str, default='newImage.png', help='name des erzeugten Bildes')
args = parser.parse_args()

originalJPG = Image.open(args.image)
breite, hoehe = originalJPG.size
newImage = originalJPG.copy()

minRng = args.minInterval
maxRng = args.maxInterval

for y in tqdm(range(hoehe)):
    row = [originalJPG.getpixel((x, y)) for x in range(breite)]

    links = 0
    while links < breite:
        intervalBreite = randint(minRng, maxRng)
        rechts = min(links + intervalBreite, breite)
        row[links:rechts] = sorted(row[links:rechts], key=lambda pixel: sum(pixel) / len(pixel))
        links = links + intervalBreite

    for x, pixel in enumerate(row):
            newImage.putpixel((x, y), pixel)

newImage.save(args.output)