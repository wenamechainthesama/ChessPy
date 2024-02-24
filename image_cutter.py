from os import mkdir
from PIL import Image
from os.path import abspath, dirname

PIECE_IMAGE_RESOLUTION = 333
PIECE_TYPES_AMOUNT = 6
ASSETS_PATH = f"{abspath(dirname(__file__))}\PiecesImages"

# Load, crop and save images of pieces
filepath = abspath(dirname(__file__))
image = Image.open(f"{filepath}\pieces.png")
images = []
box = None
for row in range(2):
    for column in range(PIECE_TYPES_AMOUNT):
        box = (
            PIECE_IMAGE_RESOLUTION * column,
            PIECE_IMAGE_RESOLUTION * row,
            PIECE_IMAGE_RESOLUTION * (column + 1),
            PIECE_IMAGE_RESOLUTION * (row + 1),
        )
        piece_image = image.crop(box)
        images.append(piece_image)

"""
Making new directory called "PiecesImages" where images of all pieces are stored while game is running
When game ends file automatically will be deleted
Filenames of saved images are following this pattern: filename = {color}{type}.png
"""
new_dir = "PiecesImages"
mkdir(ASSETS_PATH)
for index, image in enumerate(images):
    image.save(
        f"{ASSETS_PATH}\{index // PIECE_TYPES_AMOUNT}{index % PIECE_TYPES_AMOUNT + 1}.png"
    )
