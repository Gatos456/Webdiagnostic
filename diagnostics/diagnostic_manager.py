from .system_check import analizar_sistema



def realizar_diagnostico():

    resultado = {}


    resultado["Sistema"] = analizar_sistema()


    return resultado
