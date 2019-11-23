# Diego & Glot Frames Bot
DyG Frames es un bot creado en Python3 para Facebook.

## Dependencias 
* Python 3.6 O Superior
* Pip
* facebook-sdk

## Estado del Código
De momento este código es privado/limitado a ciertas personas y no existen intenciones de volverlo público en un corto plazo.

## ¿Qué hace?
En un principio quería que python obtuviera un frame en base a una marca de tiempo, **pero**, subir videos con resoluciones muy grandes costaria mucho espacio de disco virtual y python no tiene librerias muy poderosas para procesar ese video cada 10 minutos.

Se cambió esa idea para extraer los frames desde cada video utilizando `ffmpeg`. (Puedes utilizar cualquier herramienta mientras sigas el orden los path a contiuación) y el nombre de archivo `0001.jpg` donde 0001 será cada episodios `0002, 0003, ..., 0134`.`jpg`

### Organización de los archivos de carpetas.
```
VID_FOLDER
├── SEASON_FOLDER
│   ├── EPISODE_FOLDER
│   └── EPISODE_FOLDER
└── SEASON_FOLDER
    ├── EPISODE_FOLDER
    └── EPISODE_FOLDER
```

* `VID_FOLDER`: Carpeta donde se encuentras las temporadas
  * Contiene las temporadas en forma de carpetas enumaradas desde 1 a n temporadas
* `SEASON_FOLDER`: Corresponde a una temporada.
  * Contiene los episodios en forma de carpetas enumaradas desde 1 a n.
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
La forma más facil y comoda de almacenar datos que yo conozo es utilizando archivos `.json`.

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
| episode | Ultimo episodio  |
| frame | Ultimo frame  |

## Instalación
Actualmente `dyg_frames` no funciona en un proceso de fondo, asi, poder ahorrar recursos de una maquina virtual. Sin embargo se puede crear un `crontab` para ejecutarlo en el tiempo que fuera necesario.

> Es importante añadir que para algunas instancias de linux es necesario utilizar UTF8

```shell
$ PYTHONIOENCODING=UTF-8 python main.py
```

1. Crear un `virtualenv` de python 3.6+
2. `source env/bin/activate`
3. `pip install facebook-sdk`
   1. facebook-sdk en producción se encuentra en una version inferior a la requerida para el sdk 4.0. Recomendacion, instalar desde el [source](https://facebook-sdk.readthedocs.io/en/latest/install.html).
4. configurar `.env` según `.env-example`
   1. `FACEBOOK_TOKEN`: Token app requerida para publicar en facebook
   2. `PAGE_ID`: _deprecada para esta app_
   3. `VID_FOLDER`: Nombre del directorio donde se encuentran los frames de las imagenes

### Utilizando crontab 
1. `# crontab -e`
2. `*/10 * * * * cd /path/to/dyg/ && /path/to/dyg/env/bin/python main.py >> logs.txt` .. se ejecutará cada 10 minutos y guardara el estado en un log.