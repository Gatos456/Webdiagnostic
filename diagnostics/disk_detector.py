import subprocess


def detectar_discos():
    discos = []

    try:
        resultado = subprocess.run(
            ["wmic", "diskdrive", "get", "Model,Size"],
            capture_output=True,
            text=True
        )

        lineas = resultado.stdout.splitlines()

        for linea in lineas[1:]:
            linea = linea.strip()

            if not linea:
                continue

            partes = linea.rsplit(maxsplit=1)

            if len(partes) != 2:
                continue

            modelo = partes[0]
            size = partes[1]

            try:
                gb = round(int(size) / (1024**3))
                capacidad = f"{gb} GB"
            except:
                capacidad = "-"

            discos.append({
                "modelo": modelo,
                "capacidad": capacidad
            })

    except Exception as e:
        print(e)

    return discos