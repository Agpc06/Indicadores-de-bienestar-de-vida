# 📊 Análisis del Impacto Urbano en la Esperanza de Vida y la Sostenibilidad Ambiental de Latinoamérica

   En las últimas décadas, la humanidad ha comprendido que el verdadero éxito de una nación no se mide solo por su riqueza material, sino por su capacidad para ofrecer una vida digna y saludable a sus ciudadanos sin comprometer los recursos naturales del futuro. Ahora, el desarrollo es un equilibrio entre economía, sociedad y medio ambiente.

   En este panorama, Latinoamérica se presenta como una región de cambios. Representando aproximadamente el 8% de la población mundial según CEPAL (Comisión Económica para América Latina y el Caribe), la región enfrenta el reto de gestionar procesos en la urbanización mientras intenta preservar una de las biodiversidades más ricas del planeta. Sin embargo, los indicadores de desarrollo tradicionales suelen ocultar las tensiones que existen entre el crecimiento de las ciudades y el bienestar real.

   Para profundizar en esta realidad, este estudio utiliza los Indicadores del Desarrollo Mundial del Banco Mundial como un lente analítico. Al procesar datos que abarcan desde 1990 hasta 2023, buscamos transformar cifras globales en conocimiento estratégico, permitiendo identificar si el avance de la región es realmente sostenible o si los logros en calidad de vida están generando una deuda ambiental irreversible.

#  🎯 Objetivo General

Analizar el impacto del desarrollo urbano sobre la esperanza de vida y la sostenibilidad ambiental en Latinoamérica desde 1963 hasta 2023.

##  🎯 Objetivos especificos 
Para desglosar este análisis, la investigación se fundamenta en tres pilares:

- Caracterizar la evolución histórica de la mortalidad infantil y la esperanza de vida, en contraste con la cobertura forestal de la región.
   
- Analizar el impacto de la variación poblacional sobre la conservación de los ecosistemas forestales, tomando en cuenta el porcentaje de dicha población que reside en zonas rurales de la región
   
- Evaluar el impacto de las emisiones de CO2 sobre la esperanza de vida al nacer en los paises de la región

# 🔍 Marco Teórico

   Para evaluar cómo el crecimiento urbano afecta la calidad de vida y el entorno en Latinoamérica, es fundamental establecer las bases de las dimensiones sugeridas en los objetivos:

### Banco Mundial 🏦
   El Banco Mundial (BM) es una organización internacional y una de las principales fuentes de financiamiento y conocimiento para países en desarrollo. Su misión principal es reducir la pobreza y fomentar la prosperidad compartida, ofreciendo asistencia financiera (préstamos), técnica e investigación en áreas como salud, educación e infraestructura.

### ¿Que es un indicador mundial? 🌐
   Un indicador mundial es una herramienta estadística o cualitativa diseñada por organismos internacionales para medir, comparar y monitorear el progreso de fenómenos globales (sociales, económicos o ambientales) entre diferentes países.

### Sostenibilidad ambiental y superficie forestal 🌎
La superficie boscosa es el principal medidor de salud ambiental. En Latinoamérica, el crecimiento urbano compite directamente con el suelo natural; por lo tanto, la pérdida de bosques es el costo inmediato que paga la región para expandir sus ciudades y su economía.
   
### Emisiones de dioxido de carbono y la esperanza de vida al nacer 💨📈
Aunque el desarrollo industrial ligado al CO2 elevó inicialmente la longevidad, hoy la crisis climática y la contaminación actúan como un freno directo: el aumento de emisiones degrada la salud pública y reduce la esperanza de vida global al intensificar riesgos ambientales y enfermedades respiratorias.

### Curva de kuznets 〽️
La curva de Kuznets es una representación gráfica en forma de "U invertida" que postula que, durante el desarrollo económico, la desigualdad de ingresos aumenta inicialmente y luego disminuye. Propuesta por Simon Kuznets, sugiere que el crecimiento económico corrige automáticamente la desigualdad a largo plazo, pasando de economías rurales a industriales y avanzadas.

# Marco Metodológico 📑
Este apartado detalla el camino técnico seguido para procesar los datos del World Development Indicators (WDI).

### Enfoque y diseño 📐
- Enfoque: Cuantitativo, dado que se basa en el análisis de variables numéricas y el uso de la estadística para probar relaciones.
- Diseño: No experimental, de tipo longitudinal y correlacional. Se observan los fenómenos en su contexto natural a través del tiempo sin manipular las variables.

### Universo Estadístico 📉
   Todos los países que forman parte de la región latinoamericana del dataset World Development Indicators (W.D.I.).
   
### Muestra 📊
   Selección no probabilística de los países de la región previamente mencoionada que cuentan con registros completos para todas las variables de estudio durante el periodo 1963 – 2023.

# 👨‍💻 Aspectos Técnicos 
En esta sección se detallan las herramientas tecnológicas y metodologías aplicadas para el desarrollo del proyecto.

### Herramientas utilizadas 🔧
Se utilizaron distintas herramientas para el manejo y análisis de datos

•⁠  ⁠Supabase: Es una herramienta que te da alojamiento de la base de datos en la nube y conectividad remota.

•⁠  ⁠SQLite: Almacenamiento local y estructuración de los indicadores para el manejo de las consultas.

•⁠  ⁠Power BI: Modelado  y diseño de dashboards.

•⁠  ⁠Streamlit: Creación de una interfaz web interactiva para la exploración rápida de datos.

•⁠  Python: limpieza y procesamiento de datos.

### Estructura del Repositorio 📁
Nos ayudará a entender cada carpeta del repositorio de este proyecto

```text
Indicadores-de-bienestar-de-vida/
├── .streamlit/
│   └── config.toml                # Configuración de la app de Streamlit
│
├── inputs/                        # Scripts para obtención y procesamiento de datos
│   ├── interpolación.py           # Métodos de interpolación de datos
│   ├── owid_co2.py                # Datos de CO2 (Our World in Data)
│   ├── owid_enrolment.py          # Datos de educación
│   └── wbgapi.py                  # Conexión a API del Banco Mundial
│
├── pages/                         # Páginas de la aplicación
│   ├── 01_Introducción.py         # Introducción del proyecto
│   ├── 02_Objetivos.py            # Objetivos
│   ├── 03_Planteamiento_Del_Problema.py  # Problema de investigación
│   ├── 05_Manejo_De_Datos.py      # Procesamiento de datos
│   ├── 06_Evolución_Histórica.py  # Análisis temporal
│   ├── 07_Impacto_Poblacional.py  # Impacto en la población
│   └── Queries.py                 # Consultas SQL
│
├── utils/                         # Funciones auxiliares (helpers)
│
├── app.py                         # Aplicación principal de Streamlit
├── requirements.txt               # Dependencias del proyecto
├── README.md                      # Documentación
├── .gitignore                     # Archivos ignorados por Git
├── evaluacion_sql_indicadores.docx # Documento de evaluación
```
# Colaboradores del proyecto 🫂

Este proyecto fue desarrollado por los siguientes colaboradores:

- Vicente Díaz
- Laurys Alvarez
- Angel Pastrano
- Angel Reina

# Dashboards Interactivos 📈
En esta parte de la investigación observamos los datos mediante dashboards interactivos diseñado en Streamlit y Power BI para el análisis de los objetivos del proyecto

### Links
**📊[Dashboard Interactivo - Power BI](https://app.powerbi.com/view?r=eyJrIjoiOWI2ZDc0OGItMDhkNy00ZmY3LWIxY2YtZWEzNzc0MGUwNjZjIiwidCI6IjRjODE4Zjc5LWFiODQtNDU1Mi05YjdjLTJmZTcxNWIwZDBkNSIsImMiOjR9)**

**📊[Dashboard Interactivo - Streamlit]

