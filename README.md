## Teclado Virtual con Control por Gestos
## Descripción
Este proyecto implementa un teclado virtual controlado por gestos de la mano utilizando OpenCV, MediaPipe y Pygame. Permite escribir texto moviendo el dedo índice sobre las teclas virtuales y borrar palabras mediante el gesto de puño cerrado. Además, incluye un sistema de autocompletado basado en un modelo LSTM entrenado con un dataset personalizable, y utiliza NLTK como respaldo para sugerencias adicionales.

## Tecnologías utilizadas
- Python versión 3.11+
- OpenCV
- MediaPipe
- Pygame
- TensorFlow/Keras
- NLTK
  
## Estructura del proyecto
PROYECTO-IA/
- `main.py`: Ciclo principal, integración de cámara, gestos y teclado.
- `detector_manos.py`: Detección de mano y reconocimiento de gestos (puño cerrado).
- `interfaz_teclado.py`: Interfaz gráfica del teclado virtual y área de sugerencias.
- `logica_teclado.py`: Lógica de entrada de texto, sugerencias y procesamiento de teclas.
- `config.py`: Configuración de tamaños, colores, fuentes y cámara.
- `modelo_palabras/`: Modelos y dataset de palabras para el LSTM.
    - `sugeridor_palabras.py`: Entrenamiento y uso del modelo LSTM.
    - `palabras.txt`: Dataset de palabras para entrenar el modelo.
    - `lstm_suggester.pkl`: Modelo LSTM entrenado.
- `sounds/click.wav`: Sonido de retroalimentación al presionar teclas.

## Instalación y configuración

### 1. Crear estructura del proyecto

1. Crea una carpeta principal para el proyecto, por ejemplo: `PROYECTO-IA`.
2. Dentro de ella, crea dos subcarpetas:
   - `modelo_palabras`: Agrega `sugeridor_palabras.py` y `palabras.txt`.
   - `sounds`: Agrega el archivo `click.wav`.
3. Coloca el resto de los archivos (`main.py`, `detector_manos.py`, `interfaz_teclado.py`, `logica_teclado.py`, `config.py`) directamente en la carpeta principal.

### 2. Crear y activar ambiente virtual
Abre la terminal en la carpeta del proyecto y ejecuta: **python -m venv venv**, luego actívalo con **.\venv\Scripts\activate**

*Nota: En Linux/Mac usa: source venv/bin/activate*

## 3. Instalar dependencias 
Con el ambiente virtual activo, instala las librerías necesarias con: **pip install opencv-python mediapipe pygame tensorflow nltk joblib** seguido de un enter para comience la instalación.

## 4. Descargar corpus de NLTK (solo una vez)
Con el entorno aún activo, abre una terminal de Python escribiendo **python** seguido de **Enter** y ejecuta estos comandos:  

**import nltk**

**nltk.download('cess_esp')**

Deberás ver un mensaje indicando que el corpus se descargó correctamente, si es así cierra la terminal de Python con **exit()**

## 5. Entrenamiento del modelo LSTM
Nota: Debe estar activo tu ambiente virtual 

Ejecuta en consola el script de entrenamiento **python modelo_palabras/sugeridor_palabras.py** seguido de enter, esto generará un nuevo archivo llamado `lstm_suggester.pkl` en la carpeta "modelo_palabras".

## 6. Ejecución del teclado virtual 
1. Para iniciar el sistema, activa tu ambiente virtual y posteriormente ejecuta *python main.py* seguido de enter.
   ![Captura de pantalla 2025-06-12 000435](https://github.com/user-attachments/assets/230bd6ea-d74d-4b2f-ae50-20c6404a086b)

2. Aparecerá la cámara y el teclado virtual en pantalla.
   
   
   ![image](https://github.com/user-attachments/assets/7568e1a8-2dad-4528-abff-6876064ec848)


## 7. Uso
- **Selecciona teclas** moviendo el dedo índice frente a la cámara.
  
![image](https://github.com/user-attachments/assets/9a809e4f-70a0-43c8-8a72-73b64685d931)


  
- **Borra palabras** haciendo el gesto de puño cerrado para borrar la palabra completa o bien si deseas borrar sólo una letra posiciona tu dedo índice en la tecla "BORRAR".
- **Selecciona sugerencias** manteniendo el dedo sobre la sugerencia durante 1.6 segundos. El sistema sugiere palabras automáticamente mientras escribes.
- **Para salir** da un clic en la X del teclado virtual o presiona la tecla esc. 


## Créditos
Desarrollado por Estefanía Oaxaca. 

---

¿Tienes dudas o problemas? Revisa los comentarios en el código fuente o no dudes en escribirme: sz22004526@estudiantes.uv.mx



