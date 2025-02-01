import os
import json
import ctypes
from pathlib import Path

DISK_PATHS: list = ["D:\\"]


def get_disk_usage(disk_path: str) -> dict:
    """Obtiene la información de uso del disco para una ruta."""
    free_bytes = ctypes.c_ulonglong(0)
    total_bytes = ctypes.c_ulonglong(0)
    total_free_bytes = ctypes.c_ulonglong(0)

    if ctypes.windll.kernel32.GetDiskFreeSpaceExW(
        disk_path,
        ctypes.byref(free_bytes),
        ctypes.byref(total_bytes),
        ctypes.byref(total_free_bytes),
    ):
        total_gb = total_bytes.value / (1024**3)
        free_gb = free_bytes.value / (1024**3)
        used_gb = total_gb - free_gb
        percent_used = (used_gb / total_gb) * 100

        # Obtener el nombre del disco y la etiqueta del volumen
        volume_label, drive_name = get_volume_label_and_drive(disk_path)

        disk_info = {
            "disk_path": disk_path,
            "total": f"{total_gb:.0f} GB",
            "used": f"{used_gb:.0f} GB",
            "free": f"{free_gb:.0f} GB",
            "percent_used": f"{percent_used:.0f}%",
            "volume_label": volume_label,
            "drive_name": drive_name,
        }
        return disk_info
    else:
        return {"error": "No se pudo obtener la información del disco"}


def get_volume_label_and_drive(disk_path: str) -> tuple:
    """Obtiene la etiqueta del volumen y el nombre del disco."""
    volume_label = ctypes.create_unicode_buffer(255)
    file_system_name = ctypes.create_unicode_buffer(255)

    # Llamar a GetVolumeInformation
    result = ctypes.windll.kernel32.GetVolumeInformationW(
        disk_path,
        volume_label,
        len(volume_label),
        None,
        None,
        None,
        file_system_name,
        len(file_system_name),
    )

    # Obtener la etiqueta y el nombre del disco
    if result != 0:
        volume_label_str = volume_label.value if volume_label.value else "No label"
    else:
        volume_label_str = "No label"

    # El nombre del disco es la letra del disco, e.g., "C:", "D:"
    drive_name = os.path.splitdrive(disk_path)[0]

    return volume_label_str, drive_name


def save_to_json(data: dict, output_file: Path) -> None:
    """Guarda la información obtenida en un archivo JSON."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    disk_data = []
    for disk_path in DISK_PATHS:
        disk_data.append(get_disk_usage(disk_path))

    # Guardar la información en un archivo JSON
    desktop = Path.home() / "Downloads"
    output_file = desktop / "disk_usage.json"
    save_to_json(disk_data, output_file)
    print(f"Disk usage data saved to: {output_file}")


if __name__ == "__main__":
    main()
