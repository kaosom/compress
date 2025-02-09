import os
from PIL import Image
import sys


def compress_images(input_folder):
    input_folder = os.path.abspath(input_folder)

    print("Elige el formato de salida:")
    print("1. WEBP (default)")
    print("2. PNG")
    print("3. JPG")
    print("4. JPEG")
    output_format = input("Opción: ").strip()

    format_options = {"1": "WEBP", "2": "PNG", "3": "JPEG", "4": "JPEG"}
    chosen_format = format_options.get(output_format, "WEBP")

    base_folder_name = os.path.basename(input_folder)
    output_folder_name = base_folder_name + 'c'
    output_folder = os.path.join(os.path.dirname(input_folder), output_folder_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_files = 0
    files_compressed = 0
    total_original_size = 0
    total_compressed_size = 0

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                total_files += 1
                input_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                output_file_path = os.path.join(output_dir, os.path.splitext(file)[0] + f'.{chosen_format.lower()}')

                original_size = os.path.getsize(input_file_path)
                total_original_size += original_size

                try:
                    with Image.open(input_file_path) as img:
                        if chosen_format == "PNG":
                            # Si la imagen original es PNG, intentamos mantener la transparencia
                            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                                # Optimizar PNG manteniendo el canal alfa
                                img.save(output_file_path, format="PNG", optimize=True, compression_level=9)
                            else:
                                # Si no tiene transparencia, convertimos a RGB para mejor compresión
                                img = img.convert("RGB")
                                # Guardar como JPG para mejor compresión
                                jpg_path = output_file_path.rsplit('.', 1)[0] + '.jpg'
                                img.save(jpg_path, format="JPEG", quality=85, optimize=True)
                                # Renombrar a PNG si es necesario
                                if output_file_path.endswith('.png'):
                                    os.rename(jpg_path, output_file_path)
                        elif chosen_format in ["JPEG"]:
                            if img.mode in ("RGBA", "LA", "P"):
                                img = img.convert("RGB")
                            img.save(output_file_path, format=chosen_format, quality=85, optimize=True)
                        else:  # WEBP
                            img.save(output_file_path, format=chosen_format, quality=50, method=6)

                        compressed_size = os.path.getsize(output_file_path)
                        total_compressed_size += compressed_size
                        files_compressed += 1

                        reduction = (original_size - compressed_size) / original_size * 100

                        print(f"Comprimido {input_file_path} a {output_file_path}")
                        print(f"Tamaño original: {original_size / 1024:.2f} KB")
                        print(f"Tamaño comprimido: {compressed_size / 1024:.2f} KB")
                        print(f"Reducción: {reduction:.2f}%\n")
                except Exception as e:
                    print(f"Error al comprimir {input_file_path}: {e}")

    print("\nResumen:")
    print(f"Total de archivos encontrados: {total_files}")
    print(f"Total de archivos comprimidos: {files_compressed}")
    print(f"Tamaño total original: {total_original_size / 1024:.2f} KB")
    print(f"Tamaño total comprimido: {total_compressed_size / 1024:.2f} KB")

    if total_original_size > 0:
        overall_reduction = (total_original_size - total_compressed_size) / total_original_size * 100
        print(f"Reducción total: {overall_reduction:.2f}%")
    else:
        print("No se encontraron archivos para comprimir.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python compress_images.py <ruta_de_la_carpeta>")
    else:
        compress_images(sys.argv[1])