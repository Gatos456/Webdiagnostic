import subprocess


def leer_smart(disco):
    try:
        resultado = subprocess.run(
            [
                "smartctl",
                "-a",
                disco
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        return resultado.stdout

    except Exception as e:
        return str(e)