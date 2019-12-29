# Diego & Glot Frames Bot
DyG Frames es un bot en Python3 para Facebook. El código principal publica un frame por cada ejecución.

## Requerimientos
* Python 3.6+
* Pip
* [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)
* facebook-sdk
* [ffmpeg](https://www.ffmpeg.org/)

## Estado del Código
De momento este código es privado/limitado a ciertas personas y no existen intenciones de volverlo público en un corto plazo.

## ¿Qué hace?
En un principio quería que python obtuviera un frame en base a una marca de tiempo, **pero**, subir videos con resoluciones muy grandes costaría mucho espacio de almacenamiento y python no tiene librerías muy amigables para extracción de frames.

Se cambió esa idea para extraer los frames desde cada video utilizando `ffmpeg` (_Una colección de software libre que nos permitirá extraer los frames_). **Puedes utilizar cualquier herramienta mientras sigas la organización a continuación**

### Organización de los archivos de carpetas.
```bash
# los archivos se deben llamar de la siguiente forma
0001.jpg , donde 0001 corresponde al frame.
El limite de frames es 9999 x episodio/video, etc.
# organización de carpetas
VID_FOLDER
├── SEASON_FOLDER
│   ├── EPISODE_FOLDER
│   └── EPISODE_FOLDER
└── SEASON_FOLDER
    ├── EPISODE_FOLDER
    └── EPISODE_FOLDER
```

* `VID_FOLDER`: Carpeta donde se encuentras las temporadas
  * Contiene las temporadas en forma de carpetas enumeradas desde 1 a n temporadas
* `SEASON_FOLDER`: Corresponde a una temporada.
  * Contiene los episodios en forma de carpetas enumeradas desde 1 a n.
* `EPISODE_FOLDER`: Corresponde a un episodio de la temporada
  * Contiene los fotogramas de cada capitulo enumerados desde 0001 a n.
  * Los episodios deben estar en formato `.jpg` (En una futura actualización se podrá configurar desde el `.env`)

### Ejemplo
```
vid
├── 1
│   ├── 1
│   │   └── 0001.jpg
│   └── 2
└── 2
    ├── 1
    │   └── 0001.jpg
    └── 2
```

## Data.json
La forma más fácil y cómoda de almacenar datos que **yo** conozco es utilizando archivos `.json`.

`data.json` es el archivo primordial de esta app, puesto que es donde se almacenan los datos de las temporadas, disponibilidad, episodios, nombres, etc.

Ejemplo
```json
{
    "name": "Diego & Glot",
    "disponible": true,
    "seasons": [
        {
            "number": 1,
            "episodes": 1,
            "episode": [
                "Glot el Kiltro",
            ]
        }
    ],
    "save_data": {
        "season": 2,
        "episode": 1,
        "frame": 5
    }
}
```
### Explicación
#### Objeto Principal
| Nombre | Nota |
|---   | ---   |
| name | Nombre de la serie |
| disponible | Indica si la serie está disponible, se utiliza como flag para indicarle al bot que se puede continuar posteando. Se cambia este valor cuando el bot detecta que no existen mas seasons en este archivo. |
| seasons | Arreglo de Objetos, en este caso, temporadas  |
| save_data | Marcas donde se guardan el último estado del bot  |
#### Season
| seasons.objeto | Nota |
|---   | ---   |
| number | Número de la temporada (debe estar en orden 1..2..3...)|
| episodes  | La cantidad de episodios |
| episode | Arreglo de Strings, contiene los nombres de cada episodio. Deberá ser la misma cantidad que la indicada en la variable anterior |

#### save_data
| save_data.objeto | Nota |
|---   | ---   |
| season | Season actual del bot |
| episode | Último episodio  |
| frame | Último frame  |

## Instalación
Actualmente `dyg_frames` no funciona en un proceso de fondo, asi, poder ahorrar recursos de una maquina virtual. Sin embargo se puede crear un `crontab` para ejecutarlo en el tiempo que fuera necesario.

> * Es importante añadir que para algunas instancias de linux es necesario utilizar UTF8
> * En otras ocasiones influye demasiado el idioma del **LOCALE** en el que se encuentra tu distro. 
> * [Este link puede ser de utilidad](https://askubuntu.com/a/89983) para cambiar los LOCALES

```bash
# Otra forma de forzar el utf-8
# No siempre funciona ...
$ PYTHONIOENCODING=UTF-8 python main.py
```

1. Crear un `virtualenv` de python 3.6+
2. `source env/bin/activate`
3. `pip install facebook-sdk`
   1. facebook-sdk en producción se encuentra en una version inferior a la requerida para el sdk 4.0. Recomendación, instalar desde el [source](https://facebook-sdk.readthedocs.io/en/latest/install.html).
4. configurar `.env` según `.env-example`
   1. `FACEBOOK_TOKEN`: Token app requerida para publicar en facebook
   2. `PAGE_ID`: _deprecada para esta app_
   3. `VID_FOLDER`: Nombre del directorio donde se encuentran los frames de las imágenes


### Utilizando crontab 
En lo personal recomiendo utilizar [crontab de unix](https://es.wikipedia.org/wiki/Cron_(Unix)), es una forma ordenada de manejar los tiempos en que se ejecutan ciertas tareas. Además nos permite manejar el tiempo con mayor flexibilidad. 

Ejecutamos `crontab -e` en nuestra `terminal`, luego, seleccionamos nuestro editor preferido y añadimos la siguiente linea al final del archivo.

```bash
*/10 * * * * cd /path/to/dyg/ && /path/to/dyg/env/bin/python main.py >> logs.txt
```
Lo anterior ejecutará el script cada 10 minutos en segundo plano sin la necesidad tener abierto un proceso durmiendo (sleep). 
```bash
   ______ Se ejecutará cada 10 minutos
  |
  |  ___________Todos los días
  |  | | | |
*/10 * * * * cd /path/to/dyg/ && /path/to/dyg/env/bin/python main.py >> logs.txt
```
* Se dirige a la ubicación donde está el script.
* Ejecuta la versión de python que se instaló junto al virtualenv
* Y guarda los resultados en un log
 