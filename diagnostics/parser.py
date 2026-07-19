import re


def parsear_smart(texto):
    datos = {
        "salud": "Desconocida",
        "temperatura": "-",
        "horas": "-",
        "encendidos": "-",
        "vida": "-"
    }

    # Estado SMART
    salud = re.search(
        r"SMART overall-health self-assessment test result:\s+(\w+)",
        texto
    )

    if salud:
        datos["salud"] = salud.group(1)

    # Temperatura
    temp = re.search(
        r"Temperature_Celsius.*?(\d+)\s+\(",
        texto
    )

    if temp:
        datos["temperatura"] = int(temp.group(1))

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