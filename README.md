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

La interfaz es la siguiente:

![Interfaz](https://github.com/andresFlorezGobravo/DaviBot/blob/main/images/interfaz.png)
