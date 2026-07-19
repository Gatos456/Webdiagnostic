import subprocess


def leer_smart(dispositivo, tipo="ata"):
    """
    Lee la información SMART de un disco mediante Smartmontools.

    Args:
        dispositivo (str): Ejemplo "/dev/sda"
        tipo (str): Tipo de dispositivo ("ata", "nvme", etc.)

    Returns:
        str: Salida completa de smartctl.
    """

    try:
        resultado = subprocess.run(
            [
                "smartctl",
                "-a",
                "-d",
                tipo,
                dispositivo
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        salida = resultado.stdout

        if resultado.stderr:
            salida += "\n" + resultado.stderr

        return salida

    except FileNotFoundError:
        return "ERROR: Smartmontools no está instalado o no está en el PATH."

    except Exception as e:
        return f"ERROR: {e}"