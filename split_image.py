from PIL import Image
import os

def split_save_image(ruta_imagen, carp_destino, splits_columns):
    # Create the destination folder
    os.makedirs(carp_destino, exist_ok=True)

    # Open and process the image
    with Image.open(ruta_imagen) as img:
        width, height = img.size

        # Calculate size of each tile
        size_square = width // splits_columns
        splits_rows = height // size_square

        # Split and save each tile
        cont = 0
        for i in range(splits_rows):
            for j in range(splits_columns):
                left = j * size_square
                top = i * size_square
                right = left + size_square
                bottom = top + size_square

                square = img.crop((left, top, right, bottom))
                name_file = f"tile ({cont + 1}).png"
                square.save(os.path.join(carp_destino, name_file))
                cont += 1

# Ejecutar la función
split_save_image("assets/images/tiles/Wall_tiles.png", "assets/images/tiles", 20)