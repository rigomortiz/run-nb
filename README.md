# run-nb
Proyecto en python para ejecutar notebooks de jupyter de forma automática.

## Requerimientos
- Python 3.9 o superior
- Librerias de python:

      pyspark==3.1.1  
      pytest==7.1.2  
      pytest-spark==0.6.0  
      nbclient==0.5.13  
      nbconvert==7.0.0  
      nbformat==5.4.0  
      numpy==1.22.4  
      pandas==1.5.2  
      ipykernel==6.13.0  
      ipython==8.3.0  
      jupyter-client==7.3.1  
      jupyter-core==4.10.0  


## Descarga de proyecto
Descargar el proyecto de drive y subirlo al Workspace de Sandbox. Colocarlo dentro de la carpeta "/artifacts/python/run-nb".

Abrir Jupyter y ejecutar en la consola los siguientes comandos:
```
cd /var/sds/homes/{XP}/workspace/artifacts/python/run-nb
unzip run-nb.zip
```
**Estructura de la carpeta "run-nb"**
```
run-nb
├── main.py
├── requirements.txt
├── README.md
├── pytest.ini
├── src
    ├── __init__.py
    ├── ConfigFile.py
    ├── Constants.py
    ├── Notebook.py
    ├── Scheduler.py
    ├── TestMagic.py
    └── Utils.py
```

## Instalación de dependencias
En el Workspace de Sandbox ya se entran instaladas las dependencias necesarias para ejecutar el proyecto. En caso de que no se encuentren instaladas, ejecutar en la consola los siguientes comandos:
```
cd /var/sds/homes/{XP}/workspace/artifacts/python/run-nb
pip3 install -r requirements.txt
```

## Proyectos de ejemplo
Descargar la carpeta "example.zip" de drive y subirla al Workspace de Sandbox.

Ejecutar en la consola los siguientes comandos (Colocar tu XP en lugar de {XP}):
```
cd /var/sds/homes/{XP}/workspace/
unzip example.zip
```
**Estructura de la carpeta "example"**
```
example
├── notebooks
│   ├── demo.ipynb
│   ├── demo_1.ipynb
│   ├── demo_2.ipynb
│   └── demo_3.ipynb
├── parametros
│   ├── counts.csv
│   └── dates.csv
├── project-1.conf
└── project-2.conf
```

Editar los archivos project-1.conf y project-2.conf para que apunten a la ruta correcta de los archivos.

Ejemplo: 

**project-1.conf**
Colocar tu XP en lugar de {XP}
```
[demo]
notebooks = /var/sds/homes/{XP}/workspace/example/notebooks/demo.ipynb

[demo_2]
params.file = /var/sds/homes/{XP}/workspace/example/parametros/dates.csv
notebooks = /var/sds/homes/{XP}/workspace/example/notebooks/demo_2.ipynb
```

**project-2.conf**
Colocar tu XP en lugar de {XP}
``` 
[demo_1]
params.file = /var/sds/homes/{XP}/workspace/example/parametros/counts.csv
notebooks = /var/sds/homes/{XP}/workspace/example/notebooks/demo_1.ipynb

[demo_3]
params = a,b,x,y,z
notebooks = /var/sds/homes/{XP}/workspace/example/notebooks/demo_3.ipynb
```

## Ejecución

Ejecutar en consola los siguientes comandos (Colocar tu XP en lugar de {XP}):
```
cd /var/sds/homes/{XP}/workspace/artifacts/python/run-nb
python3 main.py /var/sds/homes/{XP}/workspace/example/project-2.conf  /var/sds/homes/{XP}/workspace/example/project-1.conf
```

Al finalizar la ejecución, dentro de la carpeta **/var/sds/homes/{XP}/workspace/example/output** se creará una carpeta por cada proyecto ejecutado. Dentro de cada carpeta se encontrarán los resultados de la ejecución de cada notebook.

## Especificaciones de los archivos a utilizar

### Archivos **.conf**
Archivos que se pasan como parametros al ejecutar **main.py**, los cuales contienen la configuración de los notebooks a ejecutar.

Los proyectos se configuran en archivos **.conf**. Cada archivo **.conf** puede contener uno o más notebooks. Cada notebook se define en una sección con el nombre del notebook entre corchetes. Dentro de cada sección se pueden definir los siguientes parámetros:
* **params.file**: Ubicación absoluta del archivo csv que contiene los parametros a pasar al notebook.
* **params**: Los parametros se separan por coma.
* **notebooks**: La ubicación absoluta del notebook a ejecutar.

Ejemplo 1: **project-1.conf** 

En este caso el nombre del proyecto es "project-1", el cual contiene dos notebooks: "demo" y "demo_2". El notebook "demo" no recibe parametros, mientras que el notebook "demo_2" recibe parametros desde el archivo "dates.csv" ubicado en la carpeta "parametros".
```
# Seccion 1
# Nombre del notebook: demo
[demo]
# notebooks: La ubicación absoluta del notebook a ejecutar.
notebooks = /var/sds/homes/{XP}/workspace/example/notebooks/demo.ipynb
# Este notebook no recibe parametros

# Seccion 2
# Nombre del notebook: demo_2
[demo_2]
# params.file: Ubicación absoluta del archivo csv que contiene los parametros a pasar al notebook.
params.file = /var/sds/homes/{XP}/workspace/example/parametros/dates.csv
# notebooks: La ubicación absoluta del notebook a ejecutar.
notebooks = /var/sds/homes/{XP}/workspace/example/notebooks/demo_2.ipynb
```

Ejemplo 2: **project-2.conf**   

En este caso el nombre del proyecto es "project-2", el cual contiene dos notebooks: "demo_1" y "demo_3". El notebook "demo_1" recibe parametros desde el archivo "counts.csv" ubicado en la carpeta "parametros". El notebook "demo_3" recibe parametros directamente desde el archivo de configuración.
```
# Seccion 1
# Nombre del notebook: demo_1
[demo_1]
# params.file: Ubicación absoluta del archivo csv que contiene los parametros a pasar al notebook.
params.file = /var/sds/homes/{XP}/workspace/example/parametros/counts.csv
# notebooks: La ubicación absoluta del notebook a ejecutar.
notebooks = /var/sds/homes/{XP}/workspace/example/notebooks/demo_1.ipynb

# Seccion 2
# Nombre del notebook: demo_3
[demo_3] 
# params: Los parametros se separan por coma
params = a,b,x,y,z 
# notebooks: La ubicación absoluta del notebook a ejecutar.
notebooks = /var/sds/homes/{XP}/workspace/example/notebooks/demo_3.ipynb
```
### Archivos **.csv**
Ejemplo de los archivos **.csv** que contienen los parametros:

**dates.csv**

Este archivo contiene los parametros para el notebook "demo_2". El notebook "demo_2" recibe 3 parametros: DATE_HOLDING, DATE_CDD, DATE_NDOD. El archivo "dates.csv" contiene 3 filas, cada fila contiene los valores de los parametros para cada ejecución del notebook.

El campo "CARPETA" es el nombre de la carpeta donde se guardará el resultado de la ejecución del notebook. El campo "DATE_HOLDING" es el valor del parametro DATE_HOLDING, el campo "DATE_CDD" es el valor del parametro DATE_CDD y el campo "DATE_NDOD" es el valor del parametro DATE_NDOD.

```csv
CARPETA,DATE_HOLDING,DATE_CDD,DATE_NDOD
2018-01-31,2018-01-31,2018-01-31,2018-01-31
2018-02-28,2018-02-28,2018-02-28,2018-02-28
2018-03-31,2018-03-31,2018-03-28,2018-03-28
```

**counts.csv**  

Este archivo contiene los parametros para el notebook "demo_1". El notebook "demo_1" recibe 1 parametro: COUNT. El archivo "counts.csv" contiene 2 filas, cada fila contiene el valor del parametro para cada ejecución del notebook.
Este archivo no contiene el campo "CARPETA" ya que el nombre de la carpeta donde se guardará el resultado de la ejecución será el valor del parametro COUNT.
```csv
COUNT
4
5
```

**Estructura final de la carpeta con los resultados**
```
example
├── notebooks
│   ├── demo.ipynb
│   ├── demo_1.ipynb
│   ├── demo_2.ipynb
│   └── demo_3.ipynb
├── parametros
│   ├── counts.csv
│   └── dates.csv
├── project-1.conf
|── project-2.conf
├── output
│   ├── project-1
│   │   ├── demo
│   │   │   ├── demo.ipynb
│   │   ├── demo_2
│   │   │   ├── 2018-01-31
│   │   │   │   ├── demo_2.ipynb
│   │   │   ├── 2018-02-28
│   │   │   │   ├── demo_2.ipynb
│   │   │   ├── 2018-03-31
│   │   │   │   ├── demo_2.ipynb
│   ├── project-2
│   │   ├── demo_1
│   │   │   ├── 4
│   │   │   │   ├── demo_1.ipynb
│   │   │   ├── 5
│   │   │   │   ├── demo_1.ipynb
│   │   ├── demo_3
│   │   │   ├── a
│   │   │   │   ├── demo_3.ipynb
│   │   │   ├── b
│   │   │   │   ├── demo_3.ipynb
│   │   │   ├── x
│   │   │   │   ├── demo_3.ipynb
│   │   │   ├── y
│   │   │   │   ├── demo_3.ipynb
│   │   │   ├── z
│   │   │   │   ├── demo_3.ipynb
``` 

## Ejemplo de un Notebook

### Parametros en el notebook

Existen 2 formas de pasar parametros a un notebook:
1. Pasar parametros desde un archivo csv.
2. Pasar parametros desde el archivo de configuración.

Para hacer uso de los paramétros en el notebook solo basta con agregar en el notebook el nombre de la variable a pasar


Ejemplo del notebook **demo_1.ipynb**, la variable **COUNT** es el nombre del parametro a pasar.
```python
%%test

def inc(x):
    return x + 1

def test_answer():
    # Parametro COUNT
    assert inc(3) == {COUNT}
```


```python
%%save_test

def test_spark_session_dataframe_2(spark_session):
    test_df = spark_session_dataframe(spark_session)
    # Parametro COUNT
    assert test_df.count() == {COUNT}
```


Ejemplo del notebook **demo_2.ipynb**, **DATE_HOLDING**, **DATE_CDD** y **DATE_NDOD** son los nombres de los parametros a pasar.
```python
# Parametros DATE_HOLDING, DATE_CDD, DATE_NDOD
print(DATE_HOLDING)
print(DATE_CDD)
print(DATE_NDOD)
``` 

Ejemplo del notebook **demo_3.ipynb**, el nombre de la variable **PARAM** es el nombre del parametro a pasar. Por defecto el nombre de la variable es PARAM cuando se pasa el parametro desde el archivo de configuración.
```python
%%test

import pytest

@pytest.fixture
def first_entry():
    # Parametro PARAM
    return '{PARAM}'
```

### Uso de pytest en el notebook

Para hacer uso de [pytest](https://pytest.org) en el notebook solo basta con agregar en el notebook la siguiente el siguiente [magic command](https://ipython.readthedocs.io/en/stable/interactive/magics.html) **%%run_test**. Esto permite ejecutar las pruebas unitarias que se encuentran en la celda.

Cada celda es independiente, por lo que se puede ejecutar una prueba unitaria en una celda y otra prueba unitaria en otra celda.


Ejemplo del notebook **demo_1.ipynb**

**Celda 1**

Aquí se ejecutan la función **inc** y la prueba unitaria **test_answer**.
```python
%%run_test

def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == {COUNT}
```

Celda 2

Aquí se ejecuta la prueba unitaria **test_print_dataframe** y **test_count_dataframe**. Se usa el plugin [pytest-spark](https://pypi.org/project/pytest-spark/) para ejecutar las pruebas unitarias que hacen uso de spark.
```python
%%run_test

from IPython.display import display, HTML

def spark_session_dataframe(spark_session):
    test_df = spark_session.createDataFrame([[1,3],[2,4],[1,2],[1,0]], "a: int, b: int")
    
    return test_df

def test_print_dataframe(spark_session):
    test_df = spark_session_dataframe(spark_session)
    display(HTML(test_df.limit(10).toPandas().to_html()))
    
def test_count_dataframe(spark_session):
    test_df = spark_session_dataframe(spark_session)
```

Ejemplo del notebook **demo_2.ipynb**

Celda 6

Aquí se ejecuta la prueba unitaria **test_rule_1**, **test_rule_2** y **test_rule_3**.
```python
%%run_test

def test_rule_1():
    assert '2018-01-31' == '{DATE_HOLDING}'
    
def test_rule_2():
    assert '2018-02-28' == '{DATE_HOLDING}'  
    
def test_rule_3():
    assert '2018-03-31' == '{DATE_HOLDING}'
```

Ejemplo del notebook **demo_3.ipynb**

Celda 1

```python
%%run_test

import pytest

@pytest.fixture
def first_entry():
    return '{PARAM}'

@pytest.fixture
def order(first_entry):
    return []

@pytest.fixture(autouse=True)
def append_first(order, first_entry):
    return order.append(first_entry)

def test_string_only(order, first_entry):
    assert order == [first_entry]

def test_string_and_int(order, first_entry):
    order.append(2)
    assert order == [first_entry, 2]
```
