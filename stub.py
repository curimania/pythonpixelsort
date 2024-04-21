from PIL import Image
from tqdm import tqdm
import argparse
from random import randint

parser = argparse.ArgumentParser(description="Pixelsortiert das Input-Image")
parser.add_argument('image', metavar='I', type=str, help='das zu sortierende Bild')
parser.add_argument('-minInterval', type=int, required=False, help='minimale Interval Laenge', default=10)
parser.add_argument('-maxInterval', type=int, required=False, help='maximale Interval Laenge', default=100)
parser.add_argument('-output', type=str, default='newImage.png', help='name des erzeugten Bildes')
parser.add_argument('-direction', type=str, choices=['right', 'left', 'down', 'up'], required=False, default='right', help='welche Richtung sortiert werden soll')
args = parser.parse_args()

rotationen = { 'right': 0,'down': 90,'left': 180, 'up': 270}

originalJPG = Image.open(args.image).rotate(rotationen[args.direction], expand=1)
breite, hoehe = originalJPG.size
newImage = originalJPG.copy()

for y in tqdm(range(hoehe)):
    row = [originalJPG.getpixel((x, y)) for x in range(breite)]

    links = 0
    while links < breite:
        intervalBreite = randint(args.minInterval, args.maxInterval)
        rechts = min(links + intervalBreite, breite)
        row[links:rechts] = sorted(row[links:rechts], key=lambda pixel: sum(pixel) / len(pixel))
        links = links + intervalBreite

    for x, pixel in enumerate(row):
            newImage.putpixel((x, y), pixel)

newImage.rotate(-rotationen[args.direction], expand=1).save(args.output)