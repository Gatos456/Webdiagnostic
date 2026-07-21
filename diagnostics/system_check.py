import psutil
import platform


def analizar_sistema():

    datos = {}


    # Sistema operativo
    datos["Sistema operativo"] = platform.system()

    datos["Versión"] = platform.version()



    # Procesador
    datos["Procesador"] = platform.processor()



    # Memoria RAM
    ram = psutil.virtual_memory().total / (1024 ** 3)

    datos["RAM"] = str(round(ram, 2)) + " GB"



    # Uso del disco principal
    disco = psutil.disk_usage("C:\\")

    datos["Disco usado"] = str(disco.percent) + "%"



    # Espacio libre
    libre = disco.free / (1024 ** 3)

    datos["Espacio libre"] = str(round(libre, 2)) + " GB"



    return datos
