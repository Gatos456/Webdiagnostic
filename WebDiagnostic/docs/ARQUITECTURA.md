# Arquitectura

## Componentes

Web Diagnostic está dividido en varios módulos independientes.

### Interfaz (UI)

Se encarga de mostrar toda la información al usuario.

### Diagnostic Engine

Motor principal encargado de analizar los archivos de diagnóstico.

### Base de datos

Contiene errores conocidos, causas y soluciones.

### Parser

Lee el archivo .wdiag y convierte la información para que pueda analizarse.

### Analizador

Compara los datos con la base de datos y genera un diagnóstico.

### Módulo Wii

Recopila e interpreta la información específica de Nintendo Wii.

## Flujo de funcionamiento

Nintendo Wii

↓

WD Loader

↓

Archivo .wdiag

↓

Web Diagnostic

↓

Parser

↓

Diagnostic Engine

↓

Resultado

↓

Informe para el usuario