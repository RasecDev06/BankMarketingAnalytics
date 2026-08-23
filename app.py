import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Configuracion de la pagina
st.set_page_config(
    page_title="Bank Marketing Analytics",
    page_icon=":bank:",
    layout="wide")

# Inicializamos el DataFrame dentro de la sesion
if "df" not in st.session_state:
    st.session_state.df = None


# Clase encargada de realizar operaciones de analisis
# sobre el dataset Bank Marketing
class AnalizadorBankMarketing:
    # El constructor recibe el DataFrame que sera analizado
    def __init__(self, df):
        self.df = df

    # Clasificamos las columnas del DataFrame
    # con variables numericas y categoricas
    def clasificar_variables(self):
        numericas = (
            self.df
            .select_dtypes(include="number")
            .columns
            .tolist()
        )
        categoricas = (
            self.df
            .select_dtypes(include="object")
            .columns
            .tolist()
        )
        return numericas, categoricas

    # Analizamos los valores nulos presentes en el DataFrame
    # y calculamos su cantidad y porcentaje por variable
    def analizar_nulos(self):
        # Contamos los valores nulos de cada variable
        nulos = self.df.isnull().sum()

        # Calculamos el porcentaje de valores nulos
        porcentajes_nulos = (nulos / len(self.df)) * 100

        # Creamos un DataFrame con los resultados obtenidos
        resumen_nulos = pd.DataFrame({
            "Valores nulos": nulos,
            "Porcentaje (%)": porcentajes_nulos
        })
        # Devolvemos la tabla con el resumen de valores nulos
        return resumen_nulos

    # Generamos las estadisticas descriptivas de las variables numericas del DataFrame
    def obtener_estadisticas(self):
        # Utilizamos describe() para calcular las principales
        # medidas estadisticas de las variables numericas
        estadisticas = self.df.describe()

        # Devolvemos la tabla con los resultados
        return estadisticas


# Sidebar
st.sidebar.title("Bank Marketing")

# Variable menu donde se almacenara el valor seleccionado por el usuario
menu = st.sidebar.radio(
    "Navegacion",
    ["Home", "Carga de datos", "Analisis EDA", "Conclusiones"])

if menu == "Home":
    st.title("Bienvenido a Bank Marketing")
    st.subheader("Análisis Exploratorio de Datos de Campañas Bancarias")
    st.write(
        """
        Este proyecto tiene como objetivo realizar un Análisis Exploratorio
        de Datos (EDA) sobre una campaña de marketing de una institución
        financiera, con la finalidad de identificar patrones y relaciones
        relevantes asociados a la aceptación de la campaña por parte
        de los clientes.
        """
    )
    st.divider()

    st.subheader("Informacion del Proyecto")
    st.write("Autor: Cesar Ospiño Salas")
    st.write("Especializacion: Python for Analytics")
    st.write("Año: 2026")

    st.divider()

    st.subheader("Dataset")
    st.write(
        """
        El dataset BankMarketing contiene información relacionada con
        clientes de una institución financiera y las interacciones realizadas
        durante una campaña de marketing.

        La variable `y` representa el resultado de la campaña e indica
        si el cliente aceptó ("yes") o no aceptó ("no") la propuesta.
        """
    )

    st.divider()

    st.subheader("Tecnologias utilizadas")
    st.write(
        """
        - Python
        - Pandas
        - Numpy
        - Matplotlib
        - Seaborn
        - Streamlit
        """
    )

elif menu == "Carga de datos":
    st.title("Carga del Dataset")

    st.write(
        """
       En esta sección puedes cargar el dataset BankMarketing
       que será utilizado para realizar el análisis exploratorio de datos.
       """
    )
    # Muestra un boton para subir el archivo
    archivo = st.file_uploader(
        "Selecciona el archivo BankMarketing.csv",
        type=["csv"]
    )
    # Lee el csv con pandas
    if archivo is not None:
        # Crea el dataframe
        df = pd.read_csv(archivo, sep=";")
        st.session_state.df = df
        st.success("Dataset cargado correctamente")

        # Obtenemos cantidad de filas y columnas
        filas, columnas = df.shape
        # Creamos dos columnas para mostrar las metricas
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Filas", filas)

        with col2:
            st.metric("Columnas", columnas)

        # Mostramos las primeras 5 filas del dataset
        st.subheader("Vista previa del Dataset")
        st.dataframe(df.head())
    else:
        st.info("Carga el archivo BankMarketing.csv para continuar.")

######   Analisis EDA   #########
elif menu == "Analisis EDA":
    st.title("Analisis exploratorio de datos")
    if st.session_state.df is None:
        st.warning("Primero debes cargar el dataset en la sección Carga de datos")
    else:
        # Recuperamos el DataFrame guardado en la sesion
        df = st.session_state.df

        # Creamos un objeto de la clase AnalizadorBankMarketing
        # y le entregamos el DataFrame que sera analizado
        analizador = AnalizadorBankMarketing(df)

        # Clasificamos las variables utilizando
        # un metodo del objeto analizador
        numericas, categoricas = analizador.clasificar_variables()

        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
            "Informacion General",
            "Variables",
            "Estadisticas",
            "Valores faltantes",
            "Distribucion numerica",
            "Variables categoricas",
            "Analisis bivariado",
            "Categoricas vs resultado",
            "Analisis personalizado",
            "Hallazgos clave"
        ])

        with tab1:
            st.subheader("Informacion General del Dataset")

            # Obtenemos las dimensiones del DataFrame
            filas, columnas = df.shape

            # Creamos dos columnas visuales para mostrar las dimensiones
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Numero de Filas", filas)
            with col2:
                st.metric("Numero de Columnas", columnas)

            st.divider()

            # Resumen tecnico del dataset mediante df.info()
            st.subheader("Resumen tecnico del Dataset")

            buffer = io.StringIO()
            df.info(buf=buffer)
            info = buffer.getvalue()

            st.code(info)

            st.divider()

            # Mostramos el tipo de dato de cada variable
            st.subheader("Tipos de datos")
            tipos = (
                df.dtypes
                .astype(str)
                .reset_index()
                .rename(columns={
                    "index": "Variable",
                    0: "Tipo de dato"
                })
            )
            st.dataframe(tipos)

            # Contamos los valores nulos de cada variable
            st.divider()

            st.subheader("Valores nulos")

            nulos = (
                df.isnull()
                .sum()
                .reset_index()
                .rename(
                    columns={"index": "Variable", 0: "valores nulos"
                             })
            )
            st.dataframe(nulos)

        with tab2:

            # Clasificamos las variables usando la función personalizada
            st.subheader("Clasificacion de variables")

            # Mostramos cuántas variables hay de cada tipo
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Variables numericas", len(numericas))
            with col2:
                st.metric("Variables categoricas", len(categoricas))

            st.divider()

            # Mostramos las variables numericas y categoricas
            st.subheader("Variables numericas")
            df_numericas = pd.DataFrame(
                numericas,
                columns=["Variable"]
            )
            st.dataframe(df_numericas)

            st.subheader("Variables Categoricas")
            df_categoricas = pd.DataFrame(
                categoricas,
                columns=["Variable"]
            )

            st.dataframe(df_categoricas)

        with tab3:
            st.subheader("Estadisticas descriptivas")

            # Generamos las estadisticas descriptivas utilizando
            # el metodo definido en la clase AnalizadorBankMarketing
            estadisticas = analizador.obtener_estadisticas()

            # Mostramos las estadísticas en Streamlit
            st.dataframe(estadisticas)

            st.divider()

            st.subheader("Medidas descriptivas de variables numericas")

            # Calculamos la media de cada variable numerica
            medias = df[numericas].mean()

            # Calculamos la mediana de cada variable numerica
            medianas = df[numericas].median()

            # Calculamos la desviacion estandar de cada variable numerica
            desviaciones = df[numericas].std()

            # Creamos un DataFrame para comparar ambas medidas
            resumen = pd.DataFrame({
                "Media": medias,
                "Mediana": medianas,
                "Desviacion estandar": desviaciones
            })
            # Mostramos la comparación
            st.dataframe(resumen)

        with tab4:
            st.subheader("Analisis de valores faltantes")

            # Analizamos los valores nulos utilizando el metodo definido
            # en la clase AnalizadorBankMarketing
            resumen_nulos = analizador.analizar_nulos()

            # Mostramos los resultados
            st.dataframe(resumen_nulos)

            st.divider()

            # Titulo de la seccion del grafico
            st.subheader("Valores desconocidos (unknown)")

            # Contamos cuantas veces aparece "unknown" en cada variable
            unknown = (df == "unknown").sum()

            # Calculamos el porcentaje de valores unknown
            porcentaje_unknown = (unknown / len(df)) * 100

            # Creamos una tabla con cantidad y porcentaje
            resumen_unknown = pd.DataFrame({
                "Valores unknown": unknown,
                "Porcentaje (%)": porcentaje_unknown
            })

            # Mostramos solamente las variables que contienen valores "unknown"
            # El filtro > 0 elimina de la tabla las variables que no tienen valores desconocidos
            resumen_unknown = resumen_unknown[
                resumen_unknown["Valores unknown"] > 0
                ]

            # Mostramos en Streamlit la tabla filtrada
            st.dataframe(resumen_unknown)

            # Titulo de la seccion donde mostraremos el grafico
            st.subheader("Visualizacion de valores unknown")

            # Creamos la figura y el area donde se dibujara el grafico
            # figsize=(9, 5) establece el ancho y alto de la figura
            fig, ax = plt.subplots(figsize=(9, 5))

            # Creamos un grafico de barras
            # Eje X: variables que contienen valores "unknown"
            # Eje Y: porcentaje de valores "unknown" de cada variable
            ax.bar(
                resumen_unknown.index,
                resumen_unknown["Porcentaje (%)"],
                color="red"
            )

            # Colocamos un nombre al eje horizontal
            ax.set_xlabel("Variables")
            # Colocamos un nombre al eje vertical
            ax.set_ylabel("Porcentaje (%)")
            # Colocamos un titulo al grafico
            ax.set_title("Porcentaje de valores unknown por variable")

            # Rotamos 45 grados los nombres de las variables
            # para facilitar su lectura
            plt.xticks(rotation=45)

            # Ajustamos automaticamente los margenes del grafico
            # para evitar que el titulo o las etiquetas queden cortados
            plt.tight_layout()

            # Mostramos en Streamlit el grafico creado con Matplotlib
            st.pyplot(fig)

            st.info(
                """
                El dataset no presenta valores nulos (NaN). Sin embargo, algunas variables
                categoricas contienen el valor "unknown". Se decidio conservar estos registros
                como una categoria independiente, ya que representan informacion desconocida 
                y su eliminacion podria provocar perdidas de informacion, especialmente en 
                la variable default.
                """
            )

        with tab5:
            st.subheader("Distribucion de variables numericas")

            # Agregamos un selector con las variables numericas disponibles
            variable_numerica = st.selectbox(
                "Selecciona una variable numerica",
                numericas
            )

            # Creamos la figura donde se dibujara el histograma
            fig, ax = plt.subplots(figsize=(9, 5))

            # Creamos el histograma de la variable seleccionada
            ax.hist(
                df[variable_numerica],
                bins=30,
                edgecolor="black"
            )

            # Colocamos los nombres en los ejes
            ax.set_xlabel(variable_numerica)
            ax.set_ylabel("Frecuencia")

            # Colocamos un titulo dinamico usando la variable seleccionada
            ax.set_title(f"Distribucion de {variable_numerica}")

            # Ajustamos los margenes para evitar elementos cortados
            plt.tight_layout()

            # Mostramos el grafico en Streamlit
            st.pyplot(fig)

            # Calculamos las principales medidas descriptivas
            # de la variable seleccionada por el usuario
            media_variable = df[variable_numerica].mean()
            mediana_variable = df[variable_numerica].median()
            desviacion_variable = df[variable_numerica].std()

            # Calculamos el primer y tercer quartil utilizando numpy
            q1 = np.percentile(
                df[variable_numerica],
                25
            )

            q3 = np.percentile(
                df[variable_numerica],
                75
            )

            # Calculamos el rango intercuartilico
            iqr = q3 - q1

            # Creamos 3 columnas para mostrar las medidas principales
            col1, col2, col3 = st.columns(3)

            # Mostramos la media de la variable seleccionada
            with col1:
                st.metric(
                    "Media",
                    f"{media_variable:.2f}"
                )
            # Mostramos la mediana de la variable seleccionada
            with col2:
                st.metric(
                    "Mediana",
                    f"{mediana_variable:.2f}"
                )
            # Mostramos la desviacion estandar de la variable seleccionada
            with col3:
                st.metric(
                    "Desviacion estandar",
                    f"{desviacion_variable:.2f}"
                )

            # Creamos tres columnas para mostrar los valores de los cuartiles
            col1, col2, col3 = st.columns(3)

            # Mostramos el primer cuartil
            with col1:
                st.metric(
                    "Q1 - Percentil 25",
                    f"{q1:.2f}"
                )
            # Mostramos el tercer cuartil
            with col2:
                st.metric(
                    "Q3 - Percentil 75",
                    f"{q3:.2f}"
                )

            # Mostramos el rango intercuartilico
            with col3:
                st.metric(
                    "Rango intercuartilico (IQR)",
                    f"{iqr:.2f}"
                )

        with tab6:
            st.subheader("Analisis de variables categoricas")

            # Creamos un selector con las variables categoricas disponibles
            # La variable elegida por el usuario se guardara en variable_categorica
            variable_categorica = st.selectbox(
                "Selecciona una variable categorica",
                categoricas
            )

            # Contamos cuantas veces aparece cada categoria
            frecuencias = df[variable_categorica].value_counts()

            # Obtenemos la moda de la variable categorica seleccionada
            # la moda representa la categoria que mas se repite
            moda_variable = df[variable_categorica].mode().iloc[0]

            # Obtenemos cuantas veces aparece la categoria que corresponde a la moda
            frecuencia_moda = frecuencias.iloc[0]

            # Mostramos la moda y su frecuencia
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Moda", moda_variable)

            with col2:
                st.metric("Frecuencia de la moda", frecuencia_moda)

            st.divider()

            # Convertimos las frecuencias en un Dataframe
            # para mostrarlas de manera ordenada
            tabla_frecuencias = frecuencias.reset_index()

            # Cambiamos los nombres de las columnas
            tabla_frecuencias.columns = [
                "Categoria",
                "Frecuencia"
            ]

            # Calculamos el porcentaje de cada categoria
            tabla_frecuencias["Porcentaje (%)"] = (
                    tabla_frecuencias["Frecuencia"] / len(df) * 100
            ).round(2)

            # Mostramos la tabla de frecuencias en Streamlit
            st.dataframe(tabla_frecuencias)

            # Creamos la figura donde se dibujara el grafico
            fig, ax = plt.subplots(figsize=(9, 5))

            # Creamos un grafico de barras con las frecuencias
            ax.bar(
                frecuencias.index,
                frecuencias.values,
                color="blue"
            )

            # Colocamos los nombres a los ejes
            ax.set_xlabel(variable_categorica)
            ax.set_ylabel("Frecuencia")

            # Creamos un titulo dinamico con la variable seleccionada
            ax.set_title(f"Frecuencia de {variable_categorica}")

            # Rotamos las categorias para mejorar su lectura
            plt.xticks(rotation=45)

            # Ajustamos automaticamente los margenes del grafico
            plt.tight_layout()

            # Mostramos el grafico en Streamlit
            st.pyplot(fig)

        with tab7:
            st.subheader("Analisis bivariado: variable numerica vs resultado")

            # Creamos un selector para elegir la variable numerica
            # que sera comparada con la variable objetivo "y"
            variable_bivariada = st.selectbox(
                "Selecciona una variable numerica para comparar con y",
                numericas,
                key="bivariado_numerico"
            )

            # Separamos los valores de la variable numerica segun el resultado
            # de la campaña
            datos_no = df[df["y"] == "no"][variable_bivariada]
            datos_yes = df[df["y"] == "yes"][variable_bivariada]

            # Creamos la figura donde se dibujara el boxplot
            fig, ax = plt.subplots(figsize=(9, 5))

            # Creamos un boxplot con Seaborn para comparar
            # la variable numerica segun el resultado de la campaña
            sns.boxplot(
                data=df,
                x="y",
                y=variable_bivariada,
                ax=ax
            )

            # Colocamos los nombres de los ejes
            ax.set_xlabel("Resultado de la campaña (y)")
            ax.set_ylabel(variable_bivariada)

            # Creamos un titulo dinamico con la variable seleccionada
            ax.set_title(
                f"Distribucion de {variable_bivariada} segun el resultado de la campaña")

            # Ajustamos automaticamente los margenes del grafico
            plt.tight_layout()

            # Mostramos el grafico en Streamlit
            st.pyplot(fig)

            # Calculamos la media de la variable seleccionada
            # para los clientes que no aceptaron y los que si aceptaron
            media_no = datos_no.mean()
            media_yes = datos_yes.mean()

            # Calculamos la mediana de ambos grupos
            mediana_no = datos_no.median()
            mediana_yes = datos_yes.median()

            # Creamos una tabla para comparar la estadisticas
            # de los clientes que aceptaron y los que no
            comparacion = pd.DataFrame({
                "Resultado": ["No", "Yes"],
                "Media": [media_no, media_yes],
                "Mediana": [mediana_no, mediana_yes]
            })

            # Redondeamos los valores numericos a dos decimales
            # Para facilitar su lectura
            comparacion[["Media", "Mediana"]] = (
                comparacion[["Media", "Mediana"]].round(2)
            )

            # Mostramos un titulo para la tabla comparativa
            st.subheader("Comparacion estadistica")

            # Mostramos la tabla en Streamlit
            st.dataframe(comparacion)

        with tab8:
            st.subheader("Analisis bivariado: variable categorica vs resultado")

            # Creamos una lista de variables categoricas excluyendo la variable objetivo "y"
            categoricas_sin_y = [
                columna for columna in categoricas if columna != "y"
            ]

            # Creamos un selector para elegir la variable categorica
            # que sera comparada con la variable objetivo "y"
            variable_categorica_bivariada = st.selectbox(
                "Selecciona una variable categorica para comparar con y",
                categoricas_sin_y,
                key="bivariado_categoria"
            )

            # Creamos una tabla cruzada entre la variable categorica
            # seleccionada y la variable objetivo "y"
            tabla_cruzada = pd.crosstab(
                df[variable_categorica_bivariada],
                df["y"]
            )

            # Mostramos la tabla cruzada en streamlit
            st.dataframe(tabla_cruzada)

            # Calculamos el porcentaje de respuesta dentro de cada categoria
            tabla_porcentajes = pd.crosstab(
                df[variable_categorica_bivariada],
                df["y"],
                normalize="index"
            ) * 100

            # Redondeamos los porcentajes a dos decimales
            tabla_porcentajes = tabla_porcentajes.round(2)

            # Mostramos la tabla de porcentajes en Streamlit
            st.subheader("Porcentaje por categoria")
            st.dataframe(tabla_porcentajes)

            st.divider()

            # Mostramos un titulo para la visualizacion
            st.subheader("Visualizacion por resultado de la campaña")

            # Creamos la figura donde se dibujara el grafico
            fig, ax = plt.subplots(figsize=(9, 5))

            # Creamos un grafico de barras agrupadas utilizando
            # los porcentajes calculados para las respuestas "no" y "yes"
            tabla_porcentajes.plot(
                kind="bar",
                ax=ax
            )

            # Colocamos los nombres de los ejes
            ax.set_xlabel(variable_categorica_bivariada)
            ax.set_ylabel("Porcentaje (%)")

            # Creamos un titulo dinamico utilizando la variable seleccionada
            ax.set_title(
                f"Resultado de la campaña segun {variable_categorica_bivariada}"
            )

            # Colocamos un titulo a la leyenda
            # La leyenda permite identificar las barras correspondientes a "no" y "yes"
            ax.legend(title="Resultado (y)")

            # Rotamos las categorias para facilitar su lectura
            plt.xticks(rotation=45)

            # Ajustamos automaticamente los margenes del grafico
            plt.tight_layout()

            # Mostramos el grafico en Streamlit
            st.pyplot(fig)

        with tab9:
            st.subheader("Analisis basado en parametros seleccionados")

            st.write(
                """
                Selecciona las variables que deseas incluir en el analisis.
                La tabla se actualizara automaticamente segun las columnas elegidas.
                """
            )

            # Creamos un selector multiple que permite elegir
            # una o varias columnas del dataset
            columnas_seleccionadas = st.multiselect(
                "Selecciona las variables que deseas analizar",
                options=df.columns.tolist()
            )

            # Verificamos que el usuario haya seleccionado por lo menos una variable
            if columnas_seleccionadas:

                # Creamos un nuevo Dataframe utilizando solamente
                # las columnas seleccionadas por el usuario
                df_seleccionado = df[columnas_seleccionadas]

                # Mostramos una vista previa de los datos seleccionados
                st.subheader("Vista de variables seleccionadas")

                # Creamos un slider para que el usuario pueda pueda elegir
                # cuantas filas desea visualizar
                cantidad_filas = st.slider(
                    "Cantidad de filas a mostrar",
                    min_value=5,
                    max_value=50,
                    value=10,
                    step=5
                )

                # Mostramos la cantidad de filas seleccionada por el usuario
                st.dataframe(
                    df_seleccionado.head(cantidad_filas)
                )

                st.divider()

                # Creamos un selector para que el usuario decida
                # que tipo de analisis desea realizar
                tipo_analisis = st.selectbox(
                    "Selecciona el tipo de analisis",
                    ["Tipos de datos",
                     "Valores unicos"
                     ],
                    key="tipo_analisis"
                )

                # Si el usuario selecciona "Tipos de datos",
                # Mostramos el tipo de dato de cada variable seleccionada
                if tipo_analisis == "Tipos de datos":
                    tipos_seleccionados = (
                        df_seleccionado.dtypes
                        .astype(str)
                        .reset_index()
                    )
                    # Cambiamos los nombres de las columnas
                    # para que la tabla sea mas facil de interpretar
                    tipos_seleccionados.columns = [
                        "Variable",
                        "Tipo de dato"
                    ]
                    # Mostramos la tabla en Streamlit
                    st.dataframe(tipos_seleccionados)

                # Si el usuario selecciona "valores unicos",
                # contamos cuantos valores diferentes tiene cada variable
                elif tipo_analisis == "Valores unicos":
                    valores_unicos = (
                        df_seleccionado.nunique()
                        .reset_index()
                    )

                    # Cambiamos los nombres de las columnas
                    # para facilitar su lectura
                    valores_unicos.columns = [
                        "Variable",
                        "Valores unicos"
                    ]
                    # Mostramos la tabla en Streamlit
                    st.dataframe(valores_unicos)

                # Creamos un checkbox para permitir al usuario
                # mostrar estadisticas descriptivas
                mostrar_estadisticas = st.checkbox(
                    "Mostrar estadisticas descriptivas"
                )

                # Verificar si el usuario activo el checkbox
                if mostrar_estadisticas:

                    # Seleccionamos solamente las variables numericas
                    # dentro de las columnas elegidas por el usuario
                    columnas_numericas = df_seleccionado.select_dtypes(
                        include="number"
                    )

                    # Verificamos que exista por lo menos una variable numerica
                    if not columnas_numericas.empty:
                        st.dataframe(
                            columnas_numericas.describe()
                        )
                    else:
                        st.info("Las variables seleccionadas no tienen datos numericos")

            else:
                # Mostramos un mensaje mientras no se seleccione ninguna variable
                st.info("Selecciona al menos una variable para realizar el analisis")

        with tab10:
            st.subheader("Hallazgos clave del analisis")

            # Contamos cuantos clientes aceptaron y no aceptaron la campaña
            resultados_campaña = df["y"].value_counts()

            # Calculamos el porcentaje de clientes que aceptaron la campaña
            tasa_aceptacion = (
                    (df["y"] == "yes").mean() * 100
            )

            # Calculamos el porcentaje de clientes que no aceptaron la campaña
            tasa_rechazo = (
                    (df["y"] == "no").mean() * 100
            )

            # Creamos tres columnas para mostrar
            # los principales indicadores de la campaña
            col1, col2, col3 = st.columns(3)

            with col1:
                # Mostramos la cantidad total de clientes analizados
                st.metric(
                    "Total clientes",
                    len(df)
                )

            with col2:
                # Mostramos el porcentaje de clientes
                # que aceptaron la campaña
                st.metric(
                    "Tasa de aceptacion",
                    f"{tasa_aceptacion:.2f}%"
                )

            with col3:
                # Mostramos el porcentaje de clientes
                # que no aceptaron la campaña
                st.metric(
                    "Tasa de rechazo",
                    f"{tasa_rechazo:.2f}%"
                )

            st.divider()

            st.subheader("Resultado general de la campaña")

            # Creamos la figura donde se mostrara
            # la cantidad de respuestas "no" y "yes"
            fig, ax = plt.subplots(figsize=(7, 4))

            # Creamos un grafico de barras con los resultados de la campaña
            ax.bar(
                resultados_campaña.index,
                resultados_campaña.values
            )

            # Colocamos los nombres de los ejes
            ax.set_xlabel("Resultado")
            ax.set_ylabel("Cantidad de clientes")

            # Colocamos un titulo al grafico
            ax.set_title("Distribucion del resultado de la campaña")

            # Ajustamos los margenes del grafico
            plt.tight_layout()

            # Mostramos el grafico en Streamlit
            st.pyplot(fig)

            st.divider()

            # Mostramos el segundo hallazgo del analisis
            st.subheader("Duracion de las llamadas y aceptacion")

            # Calculamos la duracion promedio de las llamadas
            # agrupando los clientes segun el resultado de la campaña
            duracion_promedio = (
                df.groupby("y")["duration"]
                .mean()
                .round(2)
            )

            # Creamos dos columnas para mostrar la duracion promedio
            # de los clientes que no aceptaron y los que si aceptaron
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Duracion promedio - No",
                    f"{duracion_promedio['no']:.2f} segundos"
                )

            with col2:
                st.metric(
                    "Duracion promedio - Yes",
                    f"{duracion_promedio['yes']:.2f} segundos"
                )

            st.divider()

            # Mostramos el tercer hallazgo del analisis
            st.subheader("Resultado de campañas anteriores")

            # Creamos una tabla cruzada entre el resultado
            # de la campaña anterior y el resultado de la campaña actual
            poutcome_resultado = pd.crosstab(
                df["poutcome"],
                df["y"],
                normalize="index"
            ) * 100

            # Redondeamos los porcentajes a dos decimales
            poutcome_resultado = poutcome_resultado.round(2)

            # Mostramos la tabla de porcentajes
            st.dataframe(poutcome_resultado)

            # Creamos la figura donde se mostrara
            # el porcentaje de aceptacion segun el resultado de la campaña anterior
            fig, ax = plt.subplots(figsize=(7, 4))

            # Graficamos solamente el porcentaje correspondiente a los clientes
            # que respondieron "yes"
            ax.bar(
                poutcome_resultado.index,
                poutcome_resultado["yes"]
            )

            # Colocamos los nombres de los ejes
            ax.set_xlabel("Resultado de campaña anterior")
            ax.set_ylabel("Porcentaje de aceptacion (%)")

            # Colocamos el titulo al grafico
            ax.set_title("Tasa de aceptacion segun resultado de campaña anterior")

            # Ajustamos automaticamente los margenes del grafico
            plt.tight_layout()

            # Mostramos el grafico en Streamlit
            st.pyplot(fig)

            st.divider()

            # Mostramos el cuarto hallazgo del analisis
            st.subheader("Tipo de contacto y aceptacion")

            # Creamos una tabla cruzada entre el tipo de contacto
            # y el resultado de la campaña
            contacto_resultado = pd.crosstab(
                df["contact"],
                df["y"],
                normalize="index"
            ) * 100

            # Redondeamos los porcentajes a dos decimales
            contacto_resultado = contacto_resultado.round(2)

            # Mostramos la tabla de porcentajes
            st.dataframe(contacto_resultado)

            # Creamos la figura donde se mostrara
            # la tasa de aceptacion segun el tipo de contacto
            fig, ax = plt.subplots(figsize=(7, 4))

            # Graficamos solamente el porcentaje de clientes
            # que respondieron "yes"
            ax.bar(
                contacto_resultado.index,
                contacto_resultado["yes"]
            )

            # Colocamos los nombres de los ejes
            ax.set_xlabel("Tipo de contacto")
            ax.set_ylabel("Porcentaje de aceptacion (%)")

            # Colocamos el titulo al grafico
            ax.set_title("Tasa de aceptacion segun tipo de contacto")

            # Ajustamos automaticamente los margenes del grafico
            plt.tight_layout()

            # Mostramos el grafico en Streamlit
            st.pyplot(fig)

            st.divider()

            # Mostramos el quinto hallazgo del analisis
            st.subheader("Mes de contacto y aceptacion")

            # Creamos una tabla cruzada entre el mes de contacto y el
            # resultado de la campaña
            mes_resultado = pd.crosstab(
                df["month"],
                df["y"],
                normalize="index"
            ) * 100

            # Redondeamos los porcentajes a dos decimales
            mes_resultado = mes_resultado.round(2)

            # Ordenamos los meses de mayor a menor segun el
            # porcentaje de clientes que respondieron "yes"
            mes_resultado = mes_resultado.sort_values(
                by="yes",
                ascending=False
            )

            # Mostramos la tabla con los porcentajes
            st.dataframe(mes_resultado)

            # Creamos la figura donde se mostrara la tasa de
            # aceptacion de cada mes
            fig, ax = plt.subplots(figsize=(7, 4))

            # Graficamos solamente el porcentaje correspondiente a los clientes
            # que respondieron "yes"
            ax.bar(
                mes_resultado.index,
                mes_resultado["yes"]
            )

            # Colocamos los nombres a los ejes
            ax.set_xlabel("Mes")
            ax.set_ylabel("Porcentaje de aceptacion (%)")

            # Colocamos el titulo al grafico
            ax.set_title("Tasa de aceptacion segun mes de contacto")

            # Ajustamos automaticamente los margenes del grafico
            plt.tight_layout()

            # Mostramos el grafico en streamlit
            st.pyplot(fig)

            st.divider()

            # Mostramos el sexto hallazgo del analisis
            st.subheader("Volumen de contactos por mes")

            # Contamos cuantos clientes fueron contactados en cada mes
            contactos_mes = df["month"].value_counts()

            # Convertimos los resultados a un DataFrame
            tabla_contactos_mes = contactos_mes.reset_index()

            # Cambiamos los nombres de las columnas
            # para facilitar la interpretacion de la tabla
            tabla_contactos_mes.columns = [
                "Mes",
                "Cantidad de contactos"
            ]

            # Agregamos a la tabla de contactos una nueva columna
            # con la tasa de aceptacion correspondiente a cada mes
            tabla_contactos_mes["Tasa de aceptacion (%)"] = (
                tabla_contactos_mes["Mes"].map(
                    mes_resultado["yes"]
                )
            )

            # Redondeamos la tasa de aceptacion a dos decimales
            # para facilitar la lectura de los resultados
            tabla_contactos_mes["Tasa de aceptacion (%)"] = (
                tabla_contactos_mes["Tasa de aceptacion (%)"].round(2)
            )

            # Mostramos un titulo para la tabla comparativa
            st.subheader("Volumen y tasa de aceptacion por mes")

            # Mostramos la tabla final en streamlit
            st.dataframe(tabla_contactos_mes)

elif menu == "Conclusiones":
    st.title("Conclusiones del analisis")

    # Verificamos que exista un dataset cargado
    if st.session_state.df is None:
        st.warning("Primero debes cargar el Dataset en la seccion Carga de datos"
                   )
    else:
        # Recuperamos el Dataframe almacenado en la sesion
        df = st.session_state.df

        # Calculamos la tasa general de aceptacion
        tasa_aceptacion = (
                (df["y"] == "yes").mean() * 100
        )

        # Calculamos la tasa general de rechazo
        tasa_rechazo = (
                (df["y"] == "no").mean() * 100
        )

        # Calculamos la duracion promedio de las llamadas
        # segun el resultado de la campaña
        duracion_promedio = (
            df.groupby("y")["duration"]
            .mean()
            .round(2)
        )

        st.write(
            """
            A partir del analisis exploratorio realizado sobre el dataset
            Bank Marketing, se identificaron diferentes patrones asociados
            al resultado de la campaña de marketing.
            """
        )

        st.divider()

        # Mostramos la conclusion general relacionada
        # con el resultado de la campaña
        st.subheader("Resultado general de la campaña")

        st.write(
            f"""
            La campaña presenta una tasa de aceptacion de aproximadamente {tasa_aceptacion:.2f}%,
            mientras que el {tasa_rechazo:.2f}% de los clientes no aceptaron la propuesta.
            
            Esto demuestra que la aceptacion de la campaña fue considerablemente
            menor que el rechazo y permite establecer un punto de referencia para
            comparar el comportamiento de las demas variables analizadas.
            """
        )

        st.divider()

        # Mostramos la segunda conclusion relacionada con la duracion de las llamadas
        st.subheader("Duracion de las llamadas")

        st.write(
            f"""
            Los clientes que aceptaron la campaña presentaron una duracion
            promedio de llamada considerablemente mayor que aquellos que
            no aceptaron la propuesta.
        
            La duracion promedio fue de aproximadamente {duracion_promedio['yes']:.2f} segundos
            para los clientes que respondieron "yes", frente a 
            {duracion_promedio['no']:.2f} segundos para los clientes que respondieron "no".
        
            Este resultado muestra una asociacion entre una mayor duracion
            de la llamada y la aceptacion de la campaña.
            """
        )

        # Calculamos la tasa de aceptacion segun el resultado de la campaña anterior
        poutcome_resultado = pd.crosstab(
            df["poutcome"],
            df["y"],
            normalize="index"
        ) * 100

        # Redondeamos los porcentajes a dos decimales
        poutcome_resultado = poutcome_resultado.round(2)

        st.divider()

        # Mostramos la tercera conclusion relacionada con el resultado
        # de campañas anteriores
        st.subheader("Resultado de campañas anteriores")

        st.write(
            f"""
            Los clientes cuyo resultado en una campaña anterior fue 'success' 
            presentaron una tasa de aceptacion de {poutcome_resultado.loc['success', 'yes']:.2f}% 
            en la campaña actual.
            
            Esta tasa fue considerablemente mayor que la observada en los clientes cuyo resultado
            anterior fue "failure" ({poutcome_resultado.loc['failure', 'yes']:.2f}%) o "nonexistent"
            ({poutcome_resultado.loc['nonexistent', 'yes']:.2f}%).
            
            Esto indica una fuerte asociacion entre un resultado positivo previo y una mayor tasa
            observada de aceptacion en la campaña actual.
            """
        )

        # Calculamos la tasa de aceptacion segun el tipo de contacto
        contacto_resultado = pd.crosstab(
            df["contact"],
            df["y"],
            normalize="index"
        ) * 100

        # Redondeamos los porcentajes a dos decimales
        contacto_resultado = contacto_resultado.round(2)

        st.divider()

        # Mostramos la cuarta conclusion relacionada con el tipo de contacto
        st.subheader("Tipo de contacto")

        st.write(
            f"""
            El tipo de contacto utilizado tambien presenta diferencias importantes
            en la tasa de aceptacion de la campaña.

            Los clientes contactados mediante "cellular" registraron una tasa de
            aceptacion de {contacto_resultado.loc['cellular', 'yes']:.2f}%,
            mientras que los contactados mediante "telephone" alcanzaron una tasa
            de {contacto_resultado.loc['telephone', 'yes']:.2f}%.

            Por lo tanto, en los datos analizados, el contacto mediante cellular
            estuvo asociado con una mayor tasa observada de aceptacion que el
            contacto mediante telephone.
            """
        )

        # Calculamos la tasa de aceptacion segun el mes de contacto
        mes_resultado = pd.crosstab(
            df["month"],
            df["y"],
            normalize="index"
        ) * 100

        # Redondeamos los porcentajes a dos decimales
        mes_resultado = mes_resultado.round(2)

        # Ordenamos los meses de mayor a menor segun su tasa de aceptacion
        mes_resultado = mes_resultado.sort_values(
            by="yes",
            ascending=False
        )

        # Obtenemos el mes con la mayor tasa de aceptacion
        # idxmax() devuelve la etiqueta del indice donde se encuentra el valor maximo
        mes_mayor_aceptacion = mes_resultado["yes"].idxmax()

        # Obtenemos la tasa de aceptacion de ese mes
        tasa_mes_mayor = mes_resultado.loc[
            mes_mayor_aceptacion,
            "yes"
        ]

        # Contamos cuantos clientes fueron contactados en cada mes
        contactos_mes = df["month"].value_counts()

        # Obtenemos la cantidad de contactos del mes con la mayor tasa de aceptacion
        volumen_mes_mayor = contactos_mes[
            mes_mayor_aceptacion
        ]

        # Obtenemos el mes con mayor volumen de contactos
        mes_mayor_volumen = contactos_mes.idxmax()

        # Obtenemos la cantidad de contactos de ese mes
        cantidad_mayor_volumen = contactos_mes.max()

        # Obtenemos su tasa de aceptacion
        tasa_mes_mayor_volumen = mes_resultado.loc[
            mes_mayor_volumen,
            "yes"
        ]

        st.divider()

        # Mostramos la quinta conclusion relacionada con el volumen de contactos por mes
        st.subheader("Volumen de contactos por mes")

        st.write(
            f"""
            La tasa de aceptacion tambien presenta diferencias importantes segun
            el mes en que se realizo el contacto.
            
            El mes con la mayor tasa de aceptacion fue el mes de "{mes_mayor_aceptacion}",
            con {tasa_mes_mayor:.2f}% de respuestas positivas y {volumen_mes_mayor} contactos
            registrados.
            
            Sin embargo, el mes con mayor volumen de contactos fue el mes de "{mes_mayor_volumen}",
            con {cantidad_mayor_volumen} contactos, pero una tasa de aceptacion de solamente 
            {tasa_mes_mayor_volumen:.2f}%.
            
            Esto demuestra la importancia de analizar conjuntamente la tasa de
            aceptacion y el volumen de contactos, ya que un porcentaje elevado
            puede corresponder a un grupo considerablemente menor de clientes.
            """
        )
