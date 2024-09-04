# EscapeRoom

El juego consiste en escapar de una sala generada de forma aleatoria, donde el jugador deberá resolver acertijos para poder escapar. El mismo será hecho con código de Python y utilizando los temas vistos en la materia de Programación I de la carrera de Lic. en Gestión IT.

## Integrantes
* Claribel Pereyra
* Lucas Vitale
* Joaquin Fernandes

## Fechas Importantes
* Primera entrega: **24-09**
* Segunda entrega: **19-11**
* Entrega final: **03-12**

## Temas a Utilizar

### Para la Primera Entrega:
* Listas
* Matrices
* Funciones Lambda
* Regex
* Diccionarios
* Tuplas
* Excepciones

### Para la Segunda Entrega:
* Unit Test
* Archivos
* Recursividad

## Posibles Escenarios
* **Temática 'La casa de papel'**: Basado en la serie reconocida de Netflix "La casa de papel"

## Getting Started

Las siguientes instrucciones permiten obtener una copia del proyecto, configurar el entorno y poder correrlo localmente.

### Prerequisitos

#### Python
* Descargar [Python](https://www.python.org/downloads/).
* Instalar Python y configurar las variables de entorno.
* Puedes verificar que lo hayas hecho correctamente ejecutando `python --version` desde cualquier consola o terminal en tu computadora.

#### Python Virtual Environment
Los entornos virtuales de Python son útiles para evitar conflictos entre diferentes proyectos que puedan usar diferentes versiones de bibliotecas.

* Desde una consola en la raíz del proyecto, ejecuta el siguiente comando:
  ```bash
  python -m venv .venv
```

* Después de completar, se debería crear una carpeta llamada `.venv` en la raíz del proyecto.
* Para activar el entorno virtual, ejecuta:
  ```bash
  $ source .venv/bin/activate
  ```

### Instalación

#### Python Libraries
* Es necesario instalar los módulos/bibliotecas utilizados como dependencias desde el archivo `requirements.txt` en el proyecto. Después de activar el entorno virtual, ejecuta el siguiente comando:
  ```bash
  (.venv) PS C:\Users\your_user\your_workspace> pip install -r requirements.txt
  ```

* Una vez completada la instalación, puedes verificar los módulos instalados con el comando `pip freeze`. Deberías ver algo como lo siguiente:
  ```bash
  (.venv) PS C:\Users\your_user\your_workspace> pip freeze
  
  allure-pytest-bdd==2.8.22
  allure-python-commons==2.8.13
  pytest==5.4.1
  selenium==3.141.0
 ```