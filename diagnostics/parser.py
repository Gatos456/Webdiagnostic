import re


def parsear_smart(texto):

    datos = {

        "modelo": "-",
        "serie": "-",
        "firmware": "-",

        "salud": "Desconocida",
        "temperatura": "-",
        "horas": "-",
        "encendidos": "-",
        "vida": "-"
    }


    # Modelo

    modelo = re.search(
        r"Device Model:\s+(.+)",
        texto
    )

    if modelo:
        datos["modelo"] = modelo.group(1).strip()


    # Número de serie

    serie = re.search(
        r"Serial Number:\s+(.+)",
        texto
    )

    if serie:
        datos["serie"] = serie.group(1).strip()


    # Firmware

    firmware = re.search(
        r"Firmware Version:\s+(.+)",
        texto
    )

    if firmware:
        datos["firmware"] = firmware.group(1).strip()



    # Salud SMART

    salud = re.search(
        r"SMART overall-health self-assessment test result:\s+(\w+)",
        texto
    )

    if salud:
        datos["salud"] = salud.group(1)



    # Temperatura

    temperatura = re.search(
        r"Temperature_Celsius.*?(\d+)\s+\(",
        texto
    )

    if temperatura:
        datos["temperatura"] = int(temperatura.group(1))



    # Horas

    horas = re.search(
        r"Power_On_Hours.*?(\d+)$",
        texto,
        re.MULTILINE
    )

    if horas:
        datos["horas"] = int(horas.group(1))



    # Encendidos

    encendidos = re.search(
        r"Power_Cycle_Count.*?(\d+)$",
        texto,
        re.MULTILINE
    )

    if encendidos:
        datos["encendidos"] = int(encendidos.group(1))



    # Vida SSD

    vida = re.search(
        r"SSD_Life_Left.*?(\d+)$",
        texto,
        re.MULTILINE
    )

    if vida:
        datos["vida"] = int(vida.group(1))


    return datos