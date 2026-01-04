import os
import sys
import subprocess
from PIL import Image


def compress_images(input_folder):
    input_folder = os.path.abspath(input_folder)

    # Preguntar nombre base para renombrar
    base_name = input(
        "Ingresa un nombre base para renombrar todos los archivos "
        "(presiona Enter para conservar nombres originales): "
    ).strip()
    rename_files = bool(base_name)
    counter = 1  # contador global para numerar archivos cuando se renombren

    # Selección de formato de salida para IMÁGENES
    print("\nElige el formato de salida para las imágenes:")
    print("1. WEBP (default)")
    print("2. PNG")
    print("3. JPG")
    print("4. JPEG")
    output_format = input("Opción: ").strip()

    format_options = {"1": "WEBP", "2": "PNG", "3": "JPEG", "4": "JPEG"}
    chosen_format = format_options.get(output_format, "WEBP")

    # Carpeta de salida
    base_folder_name = os.path.basename(input_folder)
    output_folder_name = base_folder_name + "c"
    output_folder = os.path.join(os.path.dirname(input_folder), output_folder_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_files = 0
    files_compressed = 0
    total_original_size = 0
    total_compressed_size = 0

    image_exts = (".jpg", ".jpeg", ".png", ".webp")
    video_exts = (".mp4", ".mov", ".avi", ".mkv", ".webm")

    for root, _, files in os.walk(input_folder):
        for file in files:
            if not file.lower().endswith(image_exts + video_exts):
                continue

            total_files += 1
            input_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, input_folder)
            output_dir = os.path.join(output_folder, relative_path)

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            original_size = os.path.getsize(input_file_path)
            total_original_size += original_size

            # Proceso para IMÁGENES
            if file.lower().endswith(image_exts):
                ext = chosen_format.lower()
                if rename_files:
                    output_file_name = f"{base_name}{counter}.{ext}"
                else:
                    output_file_name = os.path.splitext(file)[0] + f".{ext}"
                output_file_path = os.path.join(output_dir, output_file_name)

                try:
                    with Image.open(input_file_path) as img:
                        if chosen_format == "PNG":
                            # Mantener transparencia si existe
                            if img.mode in ("RGBA", "LA") or (
                                img.mode == "P" and "transparency" in img.info
                            ):
                                img.save(
                                    output_file_path,
                                    format="PNG",
                                    optimize=True,
                                    compression_level=9,
                                )
                            else:
                                img = img.convert("RGB")
                                img.save(
                                    output_file_path,
                                    format="JPEG",
                                    quality=85,
                                    optimize=True,
                                )
                        elif chosen_format in ["JPEG"]:
                            if img.mode in ("RGBA", "LA", "P"):
                                img = img.convert("RGB")
                            img.save(
                                output_file_path,
                                format=chosen_format,
                                quality=85,
                                optimize=True,
                            )
                        else:  # WEBP
                            img.save(
                                output_file_path,
                                format=chosen_format,
                                quality=50,
                                method=6,
                            )

                    compressed_size = os.path.getsize(output_file_path)
                    total_compressed_size += compressed_size
                    files_compressed += 1

                    reduction = (
                        (original_size - compressed_size) / original_size * 100
                        if original_size
                        else 0
                    )

                    print(f"Comprimido {input_file_path} → {output_file_path}")
                    print(f"Tamaño original:   {original_size / 1024:.2f} KB")
                    print(f"Tamaño comprimido: {compressed_size / 1024:.2f} KB")
                    print(f"Reducción:         {reduction:.2f}%\n")

                except Exception as e:
                    print(f"Error al comprimir {input_file_path}: {e}")

            # Proceso para VIDEOS
            else:
                # Siempre guardamos como MP4 (H.264 + AAC)
                ext = "mp4"
                if rename_files:
                    output_file_name = f"{base_name}{counter}.{ext}"
                else:
                    output_file_name = os.path.splitext(file)[0] + f".{ext}"
                output_file_path = os.path.join(output_dir, output_file_name)

                try:
                    # ffmpeg debe estar instalado en el sistema
                    cmd = [
                        "ffmpeg",
                        "-i",
                        input_file_path,
                        "-vcodec",
                        "libx264",
                        "-crf",
                        "28",
                        "-preset",
                        "slow",
                        "-acodec",
                        "aac",
                        "-b:a",
                        "128k",
                        "-movflags",
                        "+faststart",
                        "-y",  # sobrescribir sin preguntar
                        output_file_path,
                    ]
                    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                    compressed_size = os.path.getsize(output_file_path)
                    total_compressed_size += compressed_size
                    files_compressed += 1

                    reduction = (
                        (original_size - compressed_size) / original_size * 100
                        if original_size
                        else 0
                    )
                    print(f"Comprimido {input_file_path} → {output_file_path}")
                    print(f"Tamaño original:   {original_size / 1024:.2f} KB")
                    print(f"Tamaño comprimido: {compressed_size / 1024:.2f} KB")
                    print(f"Reducción:         {reduction:.2f}%\n")

                except subprocess.CalledProcessError as e:
                    print(f"Error al comprimir {input_file_path}: {e}")

            # Incrementar contador si se renombró
            if rename_files:
                counter += 1

    # Resumen
    print("\nResumen:")
    print(f"Total de archivos encontrados: {total_files}")
    print(f"Total de archivos comprimidos: {files_compressed}")
    print(f"Tamaño total original:   {total_original_size / 1024:.2f} KB")
    print(f"Tamaño total comprimido: {total_compressed_size / 1024:.2f} KB")

    if total_original_size > 0:
        overall_reduction = (
            (total_original_size - total_compressed_size)
            / total_original_size
            * 100
        )
        print(f"Reducción total: {overall_reduction:.2f}%")
    else:
        print("No se encontraron archivos para comprimir.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python compress_images.py <ruta_de_la_carpeta>")
    else:
        compress_images(sys.argv[1])