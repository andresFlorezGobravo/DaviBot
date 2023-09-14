
import streamlit as st
from DaviBot import daviBot
from PIL import Image





class interfaz_streamlit():
    def __init__(self):

        logo = Image.open('images/logo.png')
        st.image(logo)
        st.title("DaviBot")

        self.col1, self.col2 = st.columns(2)
        
        self.container = st.container()
        self.container.title('Chat:')
        self.Entrada_texto = None #self.container.text_input("Quiero Intervenir:", key='Intervencion')

        with self.col1:
            st.text_input("Nombre", key="nombre")
            st.text_input("Cédula", key="cedula")
            st.text_input("Referencia", key="referencia")
            st.text_input("Dirección", key="direccion")

        with self.col2:
            st.text_input("Ciudad", key = "ciudad")
            st.text_input("Correo electrónico", key = "correo")
            st.number_input("Deuda resuelve", min_value=0 ,key = "deuda_resuelve")


        with self.col1:
            button = st.button("Iniciar Bot", type = "primary", on_click=self.iniciar_bot)
            #button2 = st.button("STOP BOT")

       

    def iniciar_bot(self):
        daviBot(    st.session_state.nombre,
                    st.session_state.cedula,
                    st.session_state.referencia,
                    st.session_state.direccion,
                    st.session_state.ciudad,
                    st.session_state.correo,
                    st.session_state.deuda_resuelve,
                    self.container,
                    self.col2,
                    self.Entrada_texto
                    )


interfaz_streamlit()












    

