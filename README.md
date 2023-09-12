# Davibot

En este repositorio se almacenará el código fuente de el Bot de Davivienda (DaviBot). 

## Objetivo
El bot tiene como objetivo brindar una herramienta que permita la comunicación automatizada con la plataforma de cobranza del banco Davivienda (Mila que se encuentra en fase Beta). Link: https://mila.cobranzasbeta.com.co/

## Anotación
Mila-Beta es un chatbot que valida la información personal de los clientes Davivienda y permite conectar con un asesor para lograr acuerdos de pago o refinanciaciones de obligaciones financieras de clientes morosos.

# Metodología 

## Retos y problemáticas:
El funcionamiento básico del DaviBot consiste en el envio de informacion a traves del chatbot de Mila beta. A partir de ciertas entradas (La preguntas que realiza Mila) poder elegir la respuesta más apropiada.

Las preguntas que realiza Mila son pseudo-estandarizadas (Se sigue un mismo orden y misma estructura de pregunta pero puede deferir en su formulación. Sin embargo el significado semántico se mantiene).
### 1.  Lógica y algorítmica.
Para dar solución se plantea un flujo de información que permite dar una respuesta a paritr de una entrada.
**Respuesta contextual:**   A partir de una entrada de texto que contiene ciertas palabras o expresiones clave comunes en preguntas con un mismo significado semántico se otorgará una respuesta escrita o acción establecida.
Eg: 
Mila:
>Buen día soy ****** de Promociones y Cobranzas Beta aliado del Banco Davivienda. ¿Con quién hablo? 

 (En este caso el mensaje pide el nombre completo del cliente. Sin embargo, el asesor asociado puede cambiar por lo que el mensaje en si puede ser diferente con cada contacto). En este caso la expresion clave es *¿Con quién hablo?*. Por lo tanto cando la entrada de texto incluya esta expresión clave, la respuesta debe ser el nombre del cliente.
Davibot:

> Nombre del cliente

**Flujo de trabajo:** El flujo consiste en la sucesión de pasos que debería realizar DaviBot para un correcto funcionamiento. Se presenta en la siguiente imagen.


![Flujo](https://github.com/andresFlorezGobravo/DaviBot/blob/main/images/Funcionamiento_bot.png)



## 2. Interacción:

**Lenguaje de programación:** Para realizar el proyecto se optó por la utilización del lenguaje de programación Python debido a la versatilidad de sus librerías y a la fácil comprensión de su sintaxis para el seguimiento y desarrollo del proyecto.

**WEB:** Dado que la plataforma Mila es un portal web, se debe tener una capa de interacción con la pagina de forma automatizada. Para esto se utilizarán técnicas de web scraping para inspeccionar e interactuar con el contenido de la pagina web. En este caso se hará uso de la librería *Selenium*.
(Aquí dejo un pequeño tutorial para aprender el funcionamiento básico de esta librería https://www.youtube.com/watch?v=SPM1tm2ZdK4).
*Nota: El el chatbot se encuentra embebido en un iframe dentro de la pagina de cobranza. por lo que es necesario hacer un switch del driver de selenium al iframe del chatbot.*
Para identificar el contenido apropiado dentro del chatbot se deben identificar las etiquetas apropiadas dentro del código html del iframe del chatbot a través del speudolenguaje XPATH (Aquí dejo un tutorial https://www.w3schools.com/xml/xpath_intro.asp).
*Consejo: Usar la herramienta de inspeccionar pagina web. Al dar **CTRL + F** en la ventana que muestra el código HTML de la página podrán probar el lenguaje XPATH y así facilitar el proceso de programación.*

El contenido de los mensajes de Mila se encuentran alojados en la etiqueta DIV con clase 'jsm-user-wrapper bot' los mensajes del usuario se alojaran en etiquetas DIV de clase 'jsm-user-wrapper user'.

## 3. Interfaz:
Dada la necesidad de proveer de datos de los clientes al bot se creo una interfaz temporal haciendo uso de la librería de STREAMLIT *(Esta es una solución temporal de interfaz para la validación de funcionamiento y no debería ser considerado como el front-end de la aplicación web es necesario diseñar una interfaz apropiada.)* (Aquí dejo un tutorial para aprender a usar streamlit https://www.youtube.com/watch?v=_Syn5SpWgZ0)

Para correr la aplicación es necesario abrir el CMD en la ruta donde se encuentren guardados los archivos python.
```
streamlit run Interfaz.py
```

Al correr el comando por primera vez pedira un crreo electronico (Pueden dejar el campo vacío al dar enter directamente). Si no es la primera vez que corren el comando, lo unico que sucedera será la apertura de la interfaz en el LocalHost. Y en la ventana de comandos CMD aparecerá la dirección URL para compartir el aplicativo con otras personas en que esten en la misma red local.

Para usar multiples veces el Davibot se debe usar el segundo URL (Network URL) [La que se muestra en la imagen] Pueden copiar y pegar la URL y correr el bot cuands veces quieran siempre y cuando se use este segundo link.

![CMD](https://github.com/andresFlorezGobravo/DaviBot/blob/main/images/cmd.PNG)
La URL no será la misma que la mostrada en la imagen !!!!

La interfaz es la siguiente:

![Interfaz](https://github.com/andresFlorezGobravo/DaviBot/blob/main/images/interfaz.png)

Aquí es donde se digita la información del cliente. Y el botón iniciar Bot permite correr el funcionamiento completo.


Duarante el funcionamiento del DaviBot se puede detener en cualquier momento haciendo click en el boton STOP. Despues de unos segundos aparecera un botón de descarga que permitirá bajar un archivo CSV nombrado con la cédula del cliente y el día en que se realizó el funcionamiento del bot.


**Archivo Python:** El archivo asociado a la interfaz se llama Interfaz.py



## Backend:

Toda la programación y lógica se realizo mediante Python. Su archivo asociado se llama DaviBot.py y cada ejecucion del bot a travez de la interfaz llama un objeto denominado *daviBot*.
Este objeto (Clase generada en python) que se inicializa con la siguiente información del cliente: nombre, cedula, referencia, direccion, ciudad, correo, deuda_resuelve. (Esta información se digita desde la interfaz)

Este objeto cuenta con varias funciones asociadas. La principal es la llamada *bot()* donde se establece la conexión con el portal de Mila-Beta e inicia un While Loop para registrar todas las acciones del bot y de mila.
Durante la ejecución de este While loop se ejecutan subrutinas de la clase daviBot. Las sub rutinas son:
- *leer_pregunta():* Almacena las preguntas que realiza Mila.
- *leer_respuesta():* Almacena las respuesta que brinda Davibot
- *enviar_respuesta():* Envia la respuesta que ingrese como parámetro.
- *tiempo_espera_muy_largo():* En dado caso que el tiempo de espera sea muy largo, envia un mensaje de "Sigo esperando".
- *respuesta_contextual():* A partir del ultimo mensaje de Mila se evaluan las condiciones de contenido para enviar un mensaje predetermiando.


# Proximos Pasos:

## 1. Variedad de respuesta contextual:
Incrementar las condiciones de y expresiones clave en las respuestas contextuales.

## 2. Diseñar una interfaz apropiada:
La interfaz deberia ser diseñada con herramientas para tal efecto. Diseñar un fron-end con HTML, CSS, JS y usando Angular como framework Frontend dado que es la tecnología usada por la empresa.

## 3. Conectar con la base de datos:
Evitar el ingreso de datos manuales a partir de la interfaz y cambiarlo por el ingreso de datos automaticas a partir de la lectura de una base de datos. 

## 4. Backend formal:
Dado que todo esta programado en Python. Sería ideal formalizar el backend usando Django como framework.

## 5. Alojar la solución resultante en la nube:
Una ves el frontend y Backend sean concretados deberia ser alojado en la nube AWS en servicions de contenedores como KUBERNETES.

## 6. Almacenamiento de la conversación:
Es necesario almacenar los archivos generados de la conversacion en una base de datos.

## 7. Opcional: ChatGPT
Añadir una funcionalidad para el procesamiento de lenguaje natural para pregurtas que no sean procesables por la función de respuesta contextual.