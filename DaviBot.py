from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random
import time
import locale
import streamlit as st
from datetime import date





locale.setlocale( locale.LC_ALL, '' ) # Para dar formato de moneda financiera a valores númericos de monedo


class daviBot:

    # Función de inicialización de la clase. recibe como parámetro la info del cliente 
    # y el driver de selenium
    def __init__(self, nombre, cedula, referencia, direccion, ciudad, correo, deuda_resuelve, container, col2, entrada_texto):
        self.nombre = nombre
        self.cedula = cedula
        self.referencia = referencia
        self.direccion = direccion
        self.ciudad = ciudad
        self.correo = correo
        self.deuda_resuelve = deuda_resuelve
        self.driver = None
        self.mensajes_mila = []
        self.respuestas_usuario = []
        self.chat_completo = []
        self.ultimo_mensaje_respondido = None
        self.tiempo_espera = None
        self.detener_bot = False
        self.container = container
        self.col2 = col2
        self.entrada_texto = entrada_texto
        self.url = 'https://mila.cobranzasbeta.com.co/'

        
        
        with self.col2:
                st.button('STOP', on_click=self.detener_bot_func)

        self.bot()
    
    def detener_bot_func(self):
        # Esta función permite detener el While loop que ejecuta el bot. y habilita el boton de descarga del chat
        self.detener_bot = True
        self.download_file()
        self.driver.close()
        

    def verificar_URL(self):
        # Para algunos clientes, hay un cambio de url para dar un servicio personalizado. en ese caso es importante hacer 
        if self.detener_bot==False:
            if self.driver.current_url != self.url:
                time.sleep(10)
                self.driver.switch_to.frame(frame_reference=self.driver.find_element("xpath", "//iframe[@id='iframechat']"))
                self.url = self.driver.current_url
                time.sleep(20)
                self.enviar_respuesta('Agente')
                time.sleep(5)
                self.driver.find_element("xpath", "//div[@id='bt_id_1']").click()
                
    #def quiero_intervenir(self):
    #    texto = st.session_state.Intervencion
    #    self.enviar_respuesta(texto)
    #    st.session_state.Intervencion = ""
        

    def fill_list(self, target_list, list_to_fill):
        data_lenght_to_fill = len(target_list)-len(list_to_fill)
        for i in range(data_lenght_to_fill):
            list_to_fill.append(None)
        return list_to_fill


    def download_file(self):
        #data = ';'.join(self.chat_completo)
        self.mensajes_mila = self.fill_list(self.chat_completo, self.mensajes_mila)
        self.respuestas_usuario = self.fill_list(self.chat_completo, self.respuestas_usuario)
        dict = {'chat_completo': self.chat_completo, 'Mensajes_Mila' : self.mensajes_mila, 'Mensajes_DaviBot':self.respuestas_usuario}
        df = pd.DataFrame(dict)
        with self.col2:
            st.download_button(
                label='Descargar chat',
                data = df.to_csv().encode('UTF-8'),
                file_name=self.cedula+'--'+str(date.today())+'.csv',
                mime = 'text/csv'
            )

 
    def num_respuestas_bot(self):
        # Esta funcion retorna la cantidad de respuestas que hace mila
        return len(self.driver.find_elements("xpath", "//div[@class='jsm-user-wrapper bot']"))


    def leer_pregunta(self):
        # Esta función retorna el último mensaje dado por mila
        mensajes = self.driver.find_elements("xpath","//div[@class='jsm-user-wrapper bot']//p")
        if len(mensajes)>len(self.mensajes_mila):
            self.mensajes_mila = [i.get_attribute('innerHTML') for i in mensajes]
            for i in self.mensajes_mila:
                if i not in self.chat_completo:
                    self.chat_completo.append(i)
            self.container.write('MILA RESPONDE:'+ '\n' + mensajes[-1].get_attribute('innerHTML'))
    
    
    def leer_respuesta(self):
        # Esta función permite leer el contenido html de las respuestas dadas por DaviBOt o el usuario
        respuestas = self.driver.find_elements("xpath","//div[@class='jsm-user-wrapper user']//div[@class='jsm-chat-box-content']")
        if len(respuestas)>len(self.respuestas_usuario):
            respuestas = self.driver.find_elements("xpath","//div[@class='jsm-user-wrapper user']//div[@class='jsm-chat-box-content']")
            self.respuestas_usuario = [i.get_attribute('innerHTML') for i in respuestas]
            for i in self.respuestas_usuario:
                if i not in self.chat_completo:
                    self.chat_completo.append(i)
            self.container.write('DaviBot RESPONDE:'+ '\n' + respuestas[-1].get_attribute('innerHTML'))

    def enviar_respuesta(self, texto):
        # Esta función permite escribir y enviar la informacion que recibe como párametro
        self.driver.find_element("xpath","//input[@id='textInput']").send_keys(texto)
        self.driver.find_element("xpath","//input[@id='textInput']").send_keys(Keys.RETURN)

    def tiempo_espera_muy_largo(self):
        # En dado caso de no recibir respuesta en menos de 7 min se envia un mensaje.
        if time.time() - self.tiempo_espera>420:
            self.enviar_respuesta(random.choice(['Sigo a la espera','Continúo aguardando novedades','Aún estoy en la cola de espera','Mi situación no ha cambiado, sigo esperando', 'No he recibido actualizaciones, sigo en espera.', 'Mi estado sigue siendo el mismo: en espera.',
                                   'Hasta el momento, no ha habido cambios; sigo esperando.', 'Sigo en la misma situación de espera que antes.', 'No ha habido movimiento, sigo en proceso de espera.',
                                   'Estoy manteniendo mi posición en la lista de espera.','no ha habido avances; sigo aguardando.','Aún sigo a la espera', "¿Cuándo crees que estará listo?",
                                   "La espera se está haciendo eterna.", "A que se debe la demora?", "Por que la demora?",
                                   "Demasiado tiempo", "Tengo algo de prisa", "No tengo mucho tiempo disponible", 'hola??','¿Cuánto tiempo más tendré que aguantar esta demora?','Estoy harto de que las cosas no avancen más rápido.','¿Por qué todo tiene que ser tan lento?']))
            
            self.tiempo_espera=time.time()



    def respuesta_contextual(self):
        # Esta función permite enviar una respuesta preestablecida dependiendo de la detección de palabras clave en el último mensaje de mila (En comentario se pone el mensaje al que daremos respuesta)

        # Condicional que evita responder mas de una vez a la misma pregunta
        if self.ultimo_mensaje_respondido != self.mensajes_mila[-1]:

            if 'tipo de identificación' in self.mensajes_mila[-1]:
                self.driver.find_element("xpath", "//div[@id='bt_id_0']").click()

            if 'digite su número de cédula' in self.mensajes_mila[-1]:
                self.enviar_respuesta(self.cedula)

            if ' uno de nuestros asesores lo atendera' in self.mensajes_mila[-1]:
                self.driver.find_element("xpath","//div[@id='bt_id_2']").click()

            if '¿Con quién hablo?' in self.mensajes_mila[-1] or '¿Con quien hablo?' in self.mensajes_mila[-1]:
                self.enviar_respuesta(self.nombre)
            
            # Hola! Bienvenido a la Unidad de Negocios Especiales del Banco Davivienda Usted es muy importante para nosotros y estamos aquí para acompañarlo. Soy XXXX, su asesor financiero y mi interés es guiarlo para encontrar en conjunto una solución a la dificultad financiera que presenta con el pago de su(s) producto(s). ¿Desea dar continuidad a nuestra conversación por este medio?
            if '¿Desea dar continuidad a nuestra conversación por este medio?' in self.mensajes_mila[-1]:
                self.enviar_respuesta('SI')

            # Por seguridad y brindar mayor información acerca de sus productos, me puede confirmar su número de celular actual, dirección de residencia completa ( con barrio - ciudad) y correo electrónico, por favor.
            if 'Por seguridad y brindar mayor información acerca de sus productos' in self.mensajes_mila[-1]: 
                self.enviar_respuesta(self.referencia)
                self.enviar_respuesta(self.direccion)
                self.enviar_respuesta(self.ciudad)
                self.enviar_respuesta(self.correo)

            #¿Usted autoriza al Banco Davivienda y PYC BETA para registrar la actualización de sus datos de contacto a su base de datos, acorde a lo estipulado en la Ley 1581 de protección de datos personales? SI / NO
            if '¿Usted autoriza al Banco Davivienda y PYC BETA para registrar la actualización de sus datos de contacto a su base de datos' in  self.mensajes_mila[-1]:
                self.enviar_respuesta('SI')
                
            # ¿Cómo podemos ayudarle el día de hoy? ¿Contamos con su pago para hoy?
            if 'de hoy?' in self.mensajes_mila[-1] or 'para hoy?' in self.mensajes_mila[-1]:
                self.enviar_respuesta('No, Quiero llegar a un acuerdo de pago para mis obligaciones en mora')

            # Actualmente esta en cobro juridico
            if 'cobro juridico' in self.mensajes_mila[-1]:
                self.enviar_respuesta('Quiero llegar a un acuerdo de pago con ustedes')
            

            if 'ya cuenta' in self.mensajes_mila[-1] or 'Ya cuenta' in self.mensajes_mila[-1] or 'recursos para' in self.mensajes_mila[-1] or 'recurso para' in self.mensajes_mila[-1]:
                self.enviar_respuesta('No, Quiero llegar a un acuerdo de pago')
            
            if '¿Continua en linea?' in self.mensajes_mila[-1] or '¿Continúa en linea?' in self.mensajes_mila[-1] or '¿Continúa usted en línea?' in self.mensajes_mila[-1] or '¿Continua usted en linea?' in self.mensajes_mila[-1]:
                self.enviar_respuesta('SI')

            if 'realizar un ofrecimiento de acuerdo a su situación actual me puede indicar' in self.mensajes_mila[-1] or 'de ese valor con cuanto dispone para hacer el pago' in self.mensajes_mila[-1]:
                self.enviar_respuesta(locale.currency(random.randint(12,15)*100000.0, grouping=True )[:-3])
                self.enviar_respuesta(locale.currency(self.deuda_resuelve*0.5, grouping=True)[:-3])
            if  'cuanto es su ingreso?' in self.mensajes_mila[-1]:
                 self.enviar_respuesta(locale.currency(random.randint(12,15)*100000.0, grouping=True )[:-3])  

            #¿Qué situación se le ha presentado? Agradecemos de manera voluntaria nos confirme que cambio en sus finanzas para que no pueda realizar el pago de sus obligaciones?
            if 'situación se le ha presentado?' in self.mensajes_mila[-1] or 'cuál es el motivo de no pago' in self.mensajes_mila[-1] or 'pago de sus obligaciones' in self.mensajes_mila[-1] or 'pago de su obligación' in self.mensajes_mila[-1]: 
                # TODO: almacenar la información de la deuda y los días de mora
                self.enviar_respuesta(random.choice(['Reducción de ingresos por problemas de salud','Reducción de ingresos por enfermedad']))
            
            if 'esta situación' in self.mensajes_mila[-1] or 'esto que me comenta' in self.mensajes_mila[-1]:
                self.enviar_respuesta('6 meses')

            # ¿de donde provienen los recursos?
            if 'estos recursos' in self.mensajes_mila[-1]:
                self.enviar_respuesta('mi actividad economica como independiente')

            # ¿Cuál es su actividad económica actual? (Independiente - empleado - pensionado - desempleado)?
            if '¿Cuál es su actividad económica actual?' in self.mensajes_mila[-1]:
                self.enviar_respuesta('Independiente')

            # ¿Qué actividad económica realiza como independiente?
            if '¿Qué actividad económica realiza' in self.mensajes_mila[-1]:
                self.enviar_respuesta(random.choice(['venta de repuestos','ventas por catalogo','venta de confiteria','venta de alimentos y bebidas','venta de papeleria','reparaciones y mantenimiento','reparación de vehiculos','venta de articulos usados','cuidado de mascotas','servicios de jardineria','servicios de peluqueria','conductor de transporte privado en plataformas digitales','servicios de clases particulares','venta de artesania y manualidades','reparación de electrodomesticos']))

            # ¿Desde hace cuánto tiempo realiza esa actividad como independiente?
            if '¿Desde hace cuánto tiempo realiza esa actividad' in self.mensajes_mila[-1]:
                self.enviar_respuesta('10 meses')

            # ¿Recibe recursos adicionales? ¿Recibe la ayuda de un tercero?
            if '¿Recibe recursos adicionales?' in self.mensajes_mila[-1] or '¿Recibe la ayuda de un tercero?' in self.mensajes_mila[-1]:
                self.enviar_respuesta('No')

            # ¿De donde provienen los recursos con los que asumirá las obligación(es)?
            if 'De donde provienen los recursos' in self.mensajes_mila[-1]:
                self.enviar_respuesta('Tengo unos ahorros')

            if 'Tasa' in self.mensajes_mila[-1] or 'Cuota Aproximada' in self.mensajes_mila[-1]:
                self.enviar_respuesta('No, ¿Cuánto es el valor que debo cancelar para quedar a paz y salvo?')

            if 'cuanto dispone para pagar' in self.mensajes_mila[-1]:
                self.enviar_respuesta(locale.currency(self.deuda_resuelve*0.5, grouping=True)[:-3])

            #Llegar a acuerdo de pago ¿Está usted de acuerdo con esta alternativa ?
            if 'DESCUENTO DE PAGO' in self.mensajes_mila[-1] or 'de acuerdo con esta alternativa' in self.mensajes_mila[-1]:
                self.enviar_respuesta('voy a validar en los próximos días a ver si logro reunir el dinero')
                self.enviar_respuesta('¿Con ese valor quedo a paz y salvo con la obligación?')

            if 'no podríamos' in self.mensajes_mila[-1]:
                self.enviar_respuesta('¿Cuanto debería cancelar para quedar a paz y salvo con mis obligaciónes?')

            if 'Para terminar, me gustaría conocer su opinión sobre mi servicio' in self.mensajes_mila[-1]:
                self.driver.find_element("xpath", "//div[@id='bt_id_5']").click()

            self.ultimo_mensaje_respondido = self.mensajes_mila[-1]
            self.tiempo_espera = time.time()

            


    def bot(self):
        
        # Para dejar el navegador abierto
        options = Options()
        options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Se accede al sitio web
        self.driver.get(self.url)
        self.driver.refresh()

        self.driver.maximize_window() # Se maximiza la ventana
        time.sleep(3) # Se espera 3 segundos a que se carge el chat
        
        # Se cambia el driver al iframe del chat
        self.driver.switch_to.frame(frame_reference=self.driver.find_element("xpath", "//iframe[@id='iframechat']"))

        tiempo_inicial = time.time()
        while not(self.detener_bot):

            if time.time()-tiempo_inicial >= 7200:
                self.detener_bot_func()
                break
            elif self.detener_bot==True:
                break
            
           
            self.verificar_URL()
            self.leer_pregunta()
            
            #self.quiero_intervenir()
            self.respuesta_contextual()

            if self.detener_bot==False:  
                self.leer_respuesta()

            self.tiempo_espera_muy_largo()

            time.sleep(10) # Espera de 10 segundos

           
            
            
            
                






if __name__=='__main__':


    P1 = daviBot('9863445', '3176387300',
                    'Calle 81 # 18b-49, Olimpico 2, Mz 35 Bl 4 Apt 314', 
                    'Pereira',
                    ' julianduqque@gmail.com', 14349300)
    
