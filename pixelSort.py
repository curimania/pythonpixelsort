from PIL import Image
from tqdm import tqdm
import argparse
from random import randint

# minimal usage: python3 pixelSort.py "newImage.png" 

# Erstellen eines Argument Parsers für die Konsole

parser = argparse.ArgumentParser(description="Pixelsortiert das Input-Image")
parser.add_argument('image', metavar='I', type=str, help='das zu sortierende Bild')
parser.add_argument('-direction', type=str, choices=['right', 'left', 'down', 'up'], required=False, default='right', help='welche Richtung sortiert werden soll')
parser.add_argument('-minInterval', type=int, required=False, help='minimale Interval Laenge', default=10)
parser.add_argument('-maxInterval', type=int, required=False, help='maximale Interval Laenge', default=100)
parser.add_argument('-output', type=str, default='newImage.png', help='name des erzeugten Bildes')
args = parser.parse_args()

print("### START Pixel Sorter ###")

# Da wir von links nach rechts sortieren hier alle weiteren Richtungen
rotationen = { 'right': 0,
               'down': 90,
               'left': 180,
               'up': 270}


# unsere erste Sortierfunktion nach der Pixelhelligkeit
def helligkeit(pixel):
    return sum(pixel) / len(pixel)


# die eigentliche Sortier-Funktion
def sortiere(originalJPG, minRng, maxRng):
    # zwischenspeichern der Masse
    breite, hoehe = originalJPG.size
    # erstellen einer Kopie, die wir sortieren werden
    newImage = originalJPG.copy()
    # wir iterieren von oben nach unten durch die Reihen des Bildes
    for y in tqdm(range(hoehe)):
        # Zwischenspeichern der aktuellen Pixelreihe
        row = [originalJPG.getpixel((x, y)) for x in range(breite)]
        currentStart = 0
        # iterieren durch die Reihe
        while True:
            # abbrechen der Random Intervalle
            if currentStart >= breite - 1:
                break
            else:
                # Random Laenge des zu sortierenden Intervalls
                i = randint(minRng, maxRng)
                left = currentStart
                right = min(currentStart + i, breite)
                # hier passiert das eigentliche Pixel-Sortieren
                row[left:right] = sorted(row[left:right], key=helligkeit)
                currentStart = currentStart + i
        
        # die sortierten Pixel werden in das neue Bild geschrieben
        for x, pixel in enumerate(row):
            newImage.putpixel((x, y), pixel)
    
    return newImage

# Einlesen der eventuellen Drehung je nach Richtung --> Gradzahl in 90 Grad Schritten
rotieren = rotationen[args.direction]

# Einlesen des Input-Bildes und gleichzeitiges Rotieren
originalJPG = Image.open(args.image).rotate(rotieren, expand=1)

# Erstellen des sortierten Resultat Bildes
newImage = sortiere(originalJPG, minRng=args.minInterval, maxRng=args.maxInterval)

# zurueck drehen des Bildes und Speichern im Filesystem
newImage.rotate(-1 * rotieren, expand=1).save(args.output)

print("### ENDE ###")