Link directo: https://emilywellnessapp-cj2kh5s3ouwsfwzkyuaax6.streamlit.app/

# ⚡ Emily's Wellness Dashboard

## 📋 Descripción General

Este proyecto es un panel de control interactivo (Dashboard) de bienestar físico y mental desarrollado en Python con Streamlit. La aplicación procesa registros históricos personales de salud y telemetría diaria para transformarlos en métricas visuales intuitivas. Su objetivo principal es centralizar datos que suelen estar dispersos (sueño, pasos, ejercicio, alimentación y estado de ánimo) para facilitar un análisis integral de hábitos y comparar el rendimiento contra los estándares de salud de referencia en EE. UU. (_US National Trend Benchmarks_).

---

## 💻 Explicaciones Varias (Para Nuevos Miembros)

Si eres nuevo en este proyecto, ¡bienvenido! Aquí tienes un desglose sencillo para entender rápidamente qué es este sistema, cómo funciona y qué valor aporta:

### ¿Qué es esto y qué problema resuelve?

El registro de hábitos saludables suele ser caótico: usamos un reloj para los pasos, una app para el sueño y notas para la comida. Este proyecto actúa como un **unificador central**. Toma un conjunto de datos crudos (un archivo `.csv`), limpia la información y la convierte en un portal web interactivo con análisis automatizados (_Auto-Insights_) que explican con palabras sencillas lo que los números intentan decirte.

### Estructura de la Aplicación (Pestañas)

El sistema divide la información en seis grandes módulos para que sea fácil de digerir:

1. **Overview (Vista General):** Muestra el resumen de la última semana, el semáforo de alertas según el estrés, consejos de un entrenador inteligente y la tabla comparativa con los percentiles de referencia de EE. UU.
2. **Workout Routine (Rutina de Entrenamiento):** Sugiere una planificación semanal balanceada basada en el nivel de fatiga.
3. **Nutrition (Nutrición):** Evalúa el balance calórico acumulado semanal (déficit o superávit).
4. **Sleep (Sueño):** Muestra la arquitectura del descanso y propone reglas de higiene del sueño.
5. **Stress (Estrés):** Es el corazón analítico del proyecto. Presenta una cuadrícula uniforme de 4 gráficos que analizan científicamente las correlaciones del estrés frente al sueño, el estado de ánimo, los minutos de ejercicio y la frecuencia cardíaca en reposo (RHR).
6. **History (Historial Mensual):** Un módulo robusto para aislar cualquier mes del historial, desplegar una base de datos tabular interactiva y generar 6 gráficos independientes para evaluar tendencias macro a largo plazo.

---

## 🛠️ Requisitos para la Instalación

Antes de comenzar, asegúrate de tener instalado en tu equipo lo siguiente:

- **Lenguaje Base:** Python 3.9 o superior.
- **Gestor de Paquetes:** `pip` (incluido por defecto al instalar Python).
- **Archivo de Datos:** Se requiere el archivo fuente de datos estructurados llamado `sic_wellness_emily_park.csv` dentro de la carpeta raíz del proyecto.
- **Navegador Web:** Google Chrome, Safari, Firefox o Edge para interactuar con la interfaz.

---

## 📥 Cómo Instalar

Sigue estos pasos en tu terminal para descargar el proyecto y configurar el entorno con las librerías necesarias:

1. **Clona este repositorio en tu máquina local:**

```bash
git clone https://github.com/vpolletv/emily_wellnes_app.git
```

2. **Navega al directorio raíz del proyecto:**

```bash
cd emily_wellnes_app/
```

3. **Instala las dependencias del proyecto de forma directa:**

```bash
pip install streamlit pandas numpy matplotlib
```

---

## 🚀 Cómo Ejecutar

Una vez que la instalación de las librerías finalice con éxito, puedes iniciar el servidor web de la aplicación ejecutando el siguiente comando:

```bash
streamlit run app.py
```

_(Nota: Si guardaste tu archivo de código con otro nombre, como `dashboard.py` o `main.py`, reemplaza `app.py` por el nombre exacto de tu script)._

Inmediatamente después, el terminal te indicará que el servidor está corriendo y se abrirá de forma automática una pestaña en tu navegador web con la dirección local `http://localhost:8501`.

---

## 💡 Cómo Usar

Interactuar con el panel de control es sumamente sencillo:

1. **Navegación:** Utiliza la barra de navegación horizontal ubicada en la parte superior para saltar entre los diferentes módulos (`Overview`, `Stress`, `History`, etc.).
2. **Interpretación Visual:** En la pestaña **Overview** y **Stress**, presta atención a los códigos de color (Verde = Óptimo, Amarillo = Moderado, Rojo = Alerta) para identificar rápidamente qué hábitos requieren atención.
3. **Lectura de Gráficos:** Los gráficos de la sección de Estrés están sincronizados en tamaño para que puedas comparar visualmente el mismo día en diferentes variables.
4. **Uso del Historial:** Ve a la pestaña **History**, haz clic en el selector desplegable `📅 Choose Month:` y selecciona el año y mes que deseas auditar. La tabla y los 6 gráficos inferiores se actualizarán dinámicamente para ese período.

---

## 🗑️ Cómo Borrar (Desinstalación)

Si deseas remover por completo el proyecto y limpiar tu equipo para no dejar archivos residuales, sigue estos pasos:

1. **Detener el servidor:** Ve a la terminal donde se está ejecutando la aplicación y presiona la combinación de teclas `Ctrl + C`. Esto cerrará el portal web de Streamlit.
2. **Cerrar el navegador:** Puedes cerrar la pestaña del navegador donde visualizabas el dashboard.
3. **Eliminar los archivos del proyecto:** En tu terminal, retrocede una carpeta y elimina el directorio completo de la aplicación:

```bash
cd ..
rm -rf NOMBRE_DE_LA_CARPETA
```

_(Si estás en Windows y no usas una terminal Bash, simplemente haz clic derecho sobre la carpeta del proyecto desde el Explorador de Archivos y selecciona **Eliminar**)._

---

## 🤝 Contribuciones

Si deseas colaborar optimizando las fórmulas de correlación, mejorando los estilos CSS de las tarjetas o añadiendo nuevas fuentes de datos, eres bienvenido. Por favor, abre un **Pull Request** detallando tus cambios o reporta anomalías en la sección de **Issues**.
