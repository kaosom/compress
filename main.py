import os
from PIL import Image
import sys


def compress_images(input_folder):
    input_folder = os.path.abspath(input_folder)

    base_folder_name = os.path.basename(input_folder)
    output_folder_name = base_folder_name + 'c'
    output_folder = os.path.join(
        os.path.dirname(input_folder), output_folder_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                input_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_file_path = os.path.join(
                    output_dir, os.path.splitext(file)[0] + '.webp')

                original_size = os.path.getsize(input_file_path)

                with Image.open(input_file_path) as img:
                    img.save(output_file_path, 'WEBP', quality=10, method=6)

                compressed_size = os.path.getsize(output_file_path)

                reduction = (original_size - compressed_size) / \
                    original_size * 100

                print(f"Comprimido {input_file_path} a {output_file_path}")
                print(f"Tamaño original: {original_size / 1024:.2f} KB")
                print(f"Tamaño comprimido: {compressed_size / 1024:.2f} KB")
                print(f"Reducción: {reduction:.2f}%\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python compress_images.py <ruta_de_la_carpeta>")
    else:
        compress_images(sys.argv[1])
