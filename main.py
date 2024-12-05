import os
from PIL import Image
import sys


def compress_images(input_folder):
    # Obtener la ruta absoluta de la carpeta de entrada
    input_folder = os.path.abspath(input_folder)

    # Crear el nombre de la carpeta de salida añadiendo 'compress' al nombre original
    base_folder_name = os.path.basename(input_folder)
    output_folder_name = base_folder_name + 'c'
    output_folder = os.path.join(
        os.path.dirname(input_folder), output_folder_name)

    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Recorrer todos los archivos en la carpeta de entrada
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                input_file_path = os.path.join(root, file)
                # Calcular la ruta relativa para mantener la estructura de directorios
                relative_path = os.path.relpath(root, input_folder)
                # Determinar el directorio de salida para este archivo
                output_dir = os.path.join(output_folder, relative_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                # Crear la ruta de salida con el mismo nombre pero extensión .webp
                output_file_path = os.path.join(
                    output_dir, os.path.splitext(file)[0] + '.webp')

                # Obtener el tamaño original del archivo
                original_size = os.path.getsize(input_file_path)

                # Abrir la imagen y guardar como WebP con compresión con pérdida
                with Image.open(input_file_path) as img:
                    img.save(output_file_path, 'WEBP', quality=10, method=6)

                # Obtener el tamaño del archivo comprimido
                compressed_size = os.path.getsize(output_file_path)

                # Calcular el porcentaje de reducción
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
