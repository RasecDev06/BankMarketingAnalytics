## Descripción del proyecto

Este proyecto consiste en el desarrollo de una aplicación interactiva en
Streamlit para explorar y analizar el dataset Bank Marketing, correspondiente
a una campaña realizada por una institución financiera.

La aplicación fue diseñada para recorrer el análisis de manera progresiva,
desde la carga y revisión inicial de los datos hasta la identificación de
hallazgos relacionados con la aceptación de la campaña. Para ello se estudian
variables numéricas y categóricas, valores faltantes y registros identificados
como `unknown`, distribuciones, frecuencias y relaciones entre las
características de los clientes y la variable objetivo `y`.

El análisis también permite comparar grupos de clientes según su respuesta a
la campaña y explorar aspectos como la duración de las llamadas, el tipo de
contacto, los resultados de campañas anteriores y el comportamiento de la
aceptación según el mes de contacto.

La aplicación incorpora controles interactivos que permiten seleccionar
variables y modificar determinados parámetros del análisis, haciendo posible
explorar el dataset desde diferentes perspectivas sin modificar directamente
el código.

## Tecnologías utilizadas:

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit


## Funcionalidades principales

La aplicación está organizada en diferentes secciones que permiten desarrollar
el análisis de forma progresiva:

- Carga de un dataset en formato CSV mediante Streamlit.
- Visualización inicial de los registros cargados.
- Identificación de las dimensiones del dataset.
- Clasificación automática de variables numéricas y categóricas.
- Revisión de los tipos de datos de cada variable.
- Cálculo de estadísticas descriptivas.
- Análisis de valores nulos (`NaN`) y valores desconocidos (`unknown`).
- Análisis de distribuciones de variables numéricas mediante histogramas.
- Análisis de frecuencias, proporciones y moda de variables categóricas.
- Comparación de variables numéricas con el resultado de la campaña mediante boxplots.
- Comparación de variables categóricas con la variable objetivo `y`.
- Selección dinámica de variables y parámetros de análisis.
- Presentación de hallazgos clave obtenidos durante el EDA.
- Generación de conclusiones basadas en los resultados observados.


## Estructura del proyecto

El proyecto está organizado de la siguiente manera:

```text
BankMarketing/
│
├── app.py
├── BankMarketing.csv
├── requirements.txt
└── README.md
```

## Instrucciones de ejecución

Para ejecutar la aplicación de manera local es necesario tener Python instalado
en el equipo.

### 1. Descargar el proyecto

Descargar o clonar el repositorio y acceder a la carpeta del proyecto.

### 2. Instalar las dependencias

Abrir una terminal dentro de la carpeta del proyecto y ejecutar:

```bash
pip install -r requirements.txt
```

Este comando instalará las librerías necesarias definidas en el archivo
`requirements.txt`.

### 3. Ejecutar la aplicación

Desde la misma terminal ejecutar:

```bash
streamlit run app.py
```

Streamlit iniciará la aplicación y permitirá acceder a ella desde el navegador.

### 4. Cargar el dataset

Una vez iniciada la aplicación, ingresar a la sección **Carga de datos** y
seleccionar el archivo `BankMarketing.csv`.

Después de cargar el dataset estarán disponibles las diferentes secciones del
análisis exploratorio.


## Links relevantes

- Repositorio GitHub: https://github.com/RasecDev06/BankMarketingAnalytics
- https://bank-marketing-analytics-rasecdev06.streamlit.app/
