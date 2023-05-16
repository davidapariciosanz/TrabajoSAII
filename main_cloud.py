import os
from google.cloud import bigquery
import streamlit as st
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'famous-team-364023-97f7dbe208f3.json'

# Función para conectarse a la base de datos y ejecutar una consulta
def ejecutar_consulta(page, sql_query):

    client = bigquery.Client()

    query_job = client.query(sql_query)

    if page == 'Q1':
        # Definir listas vacías para cada columna del DataFrame
        nombreEmpresa = []
        enlaceEmpresa = []

        # Iterar sobre los elementos que deseas agregar a cada columna
        for row in query_job.result():
            nombreEmpresa.append(row.nombreEmpresa)
            enlaceEmpresa.append(row.enlaceEmpresa)

        # Crear el DataFrame utilizando el constructor de DataFrame de pandas
        df = pd.DataFrame({'Empresa': nombreEmpresa,
                           'Enlace a la página web': enlaceEmpresa})

    elif page == 'Q2':
        # Definir listas vacías para cada columna del DataFrame
        nombreEmpresa = []
        fechaConsultaPolitica = []
        fechaUltimaActualizacion = []

        # Iterar sobre los elementos que deseas agregar a cada columna
        for row in query_job.result():
            nombreEmpresa.append(row.nombreEmpresa)
            fechaConsultaPolitica.append(row.fechaConsultaPolitica)
            fechaUltimaActualizacion.append(row.fechaUltimaActualizacion)

        # Crear el DataFrame utilizando el constructor de DataFrame de pandas
        df = pd.DataFrame({'Empresa': nombreEmpresa,
                           'Fecha de consulta': fechaConsultaPolitica,
                           'Fecha de última actualización': fechaUltimaActualizacion})

    elif page == 'Q3':
        # Definir listas vacías para cada columna del DataFrame
        nombreEmpresa = []
        descripcionPolitica = []
        minutosLectura = []
        numeroPalabras = []

        # Iterar sobre los elementos que deseas agregar a cada columna
        for row in query_job.result():
            nombreEmpresa.append(row.nombreEmpresa)
            descripcionPolitica.append(row.descripcionPolitica)
            minutosLectura.append(row.minutosLectura)
            numeroPalabras.append(row.numeroPalabras)

        # Crear el DataFrame utilizando el constructor de DataFrame de pandas
        df = pd.DataFrame({'Empresa': nombreEmpresa,
                           'Descripción de la política': descripcionPolitica,
                           'Minutos de lectura de los ToS': minutosLectura,
                           'Número de palabras de los ToS': numeroPalabras})

    return df


# Aplicación Streamlit
def main():

    st.sidebar.header('Trabajo SAII: Grupo 2')
    st.sidebar.text('David Aparicio Sanz \nEmma Hernández Paz \nJaime Ojosnegros Arranz')


    # Función para ejecutar el primer tipo de consulta
    def queryOne():
        st.header('Consulta 1')
        st.text('Enlace a la página web de la empresa seleccionada.')

        empresasQ1 = ['Amazon', 'Apple', 'Blizzard', 'CNN', 'DuckDuckGo', 'Facebook', 'Google', 'Instagram',
                      'Khan Academy', 'LinkedIn', 'Microsoft', 'Netflix', 'PayPal', 'Pinterest', 'Pornhub', 'Quora',
                      'Reddit', 'Spotify', 'Startpage', 'Twitter', 'WikiHow', 'Wikipedia', 'YouTube']
        nombreEmpresa = st.sidebar.selectbox('Selecciona la empresa', empresasQ1)

        query = """
        SELECT DISTINCT nombreEmpresa, enlaceEmpresa 
        FROM `famous-team-364023.Mediador.Empresa`
        WHERE nombreEmpresa = '""" + nombreEmpresa + """' 
        AND enlaceEmpresa IS NOT NULL
        """

        st.table(ejecutar_consulta(page, query))

    # Función para ejecutar el segundo tipo de consulta
    def queryTwo():
        st.header('Consulta 2')
        st.text('Fechas de consulta y de última actualización de las política de la empresa \nseleccionada con determinado identificador.')

        empresasQ2 = ['Allrecipes', 'Amazon', 'AOL', 'Bank of America', 'Bing', 'Blogger', 'CNET', 'ESPN', 'Google',
                      'IMDb', 'Instagram', 'MSN', 'Reddit', 'The Huffington Post', 'The NY Times', 'The Walt Disney Company', 'Walmart',
                      'Washington Post', 'Yahoo!', 'YouTube']
        nombreEmpresaIdPolitica = {"Allrecipes": [70], "Amazon": [105], "AOL": [1034], "Bank of America": [1300],
                                   "Bing": [1582], "Blogger": [591], "CNET": [641], "ESPN": [186], "Google": [591],
                                   "IMDb": [21], "Instagram": [135], "MSN": [1582], "Reddit": [303],
                                   "The Huffington Post": [1034], "The NY Times": [26],
                                   "The Walt Disney Company": [186], "Walmart": [348], "Washington Post": [200],
                                   "Yahoo!": [1361], "YouTube": [591]}

        nombreEmpresa = st.sidebar.selectbox('Selecciona la empresa', empresasQ2)
        idPolitica = st.sidebar.selectbox('Selecciona el id de la política de privacidad', nombreEmpresaIdPolitica[nombreEmpresa])

        query = """
        SELECT DISTINCT nombreEmpresa, fechaConsultaPolitica, fechaUltimaActualizacion 
        FROM `famous-team-364023.Mediador.Actualizacion`
        WHERE nombreEmpresa = '""" + nombreEmpresa + """' 
        AND idPolitica = """ + str(idPolitica)

        st.table(ejecutar_consulta(page, query))

    # Función para ejecutar el tercer tipo de consulta
    def queryThree():
        st.header('Consulta 3')
        st.text('Descripción de las políticas y minutos de lectura de los términos de servicio \nde las empresas cuyos términos de servicio tengan 300 o más palabras.')
        st.text('Extra: Se permite seleccionar el número mínimo de minutos de lectura.')

        numeroPalabras = str(st.sidebar.slider('Selecciona el número mínimo de palabras', min_value=0, max_value=8600))
        minutosLectura = str(st.sidebar.slider('Selecciona el número mínimo de minutos de lectura', min_value=0, max_value=36))

        query = """
        SELECT DISTINCT Politica.nombreEmpresa, Politica.descripcionPolitica, Empresa.minutosLectura, Empresa.numeroPalabras 
        FROM famous-team-364023.Mediador.Empresa INNER JOIN famous-team-364023.Mediador.Politica ON Empresa.nombreEmpresa = Politica.nombreEmpresa 
        WHERE Empresa.numeroPalabras >= """ + numeroPalabras + """
        AND Empresa.minutosLectura >= """ + minutosLectura

        st.table(ejecutar_consulta(page, query))

    # Selector para el cambio de página
    page = st.sidebar.selectbox('Selecciona la consulta', ['Q1', 'Q2', 'Q3'])

    # Invocador del cambio de página
    if page == 'Q1':
        queryOne()
    elif page == 'Q2':
        queryTwo()
    elif page == 'Q3':
        queryThree()

# Ejecutar la aplicación
if __name__ == '__main__':
    main()
