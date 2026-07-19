def analizar_disco(datos):
    resultado = {
        "estado": "OK",
        "avisos": []
    }

    # Comprobar salud SMART
    salud = datos.get("salud", "")

    if "PASSED" not in salud and "OK" not in salud:
        resultado["estado"] = "CRITICO"
        resultado["avisos"].append(
            "El disco ha reportado un fallo SMART"
        )


    # Comprobar temperatura
    try:
        temperatura = int(
            ''.join(
                filter(str.isdigit, datos.get("temperatura", ""))
            )
        )

        if temperatura >= 60:
            resultado["estado"] = "CRITICO"
            resultado["avisos"].append(
                "Temperatura demasiado alta"
            )

        elif temperatura >= 50:
            if resultado["estado"] == "OK":
                resultado["estado"] = "ADVERTENCIA"

            resultado["avisos"].append(
                "Temperatura elevada"
            )

    except:
        pass


    # Comprobar sectores dañados
    try:
        sectores = int(datos.get("sectores", 0))

        if sectores > 0:
            if resultado["estado"] == "OK":
                resultado["estado"] = "ADVERTENCIA"

            resultado["avisos"].append(
                "Hay sectores reasignados en el disco"
            )

    except:
        pass


    return resultado
if __name__ == "__main__":
    disco_prueba = {
        "salud": "FAILED",
        "temperatura": "65",
        "sectores": "3"
    }

    resultado = analizar_disco(disco_prueba)

    print(resultado)
    