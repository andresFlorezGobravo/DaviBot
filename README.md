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
