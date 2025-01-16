
import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(
    page_title="Detector de Textos Suicidas",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stTextArea textarea {
            border-radius: 10px;
            border: 1px solid #ddd;
            padding: 10px;
        }
        .stButton>button {
            border-radius: 20px;
            padding: 0.5rem 2rem;
            background-color: #FF4B4B;
            color: white;
            font-weight: bold;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #FF3333;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .header-container {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(to right, #FF4B4B, #FF8080);
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
        }
        /* Ocultar visualmente la etiqueta pero mantenerla accesible para lectores de pantalla */
        .visually-hidden {
            position: absolute !important;
            width: 1px !important;
            height: 1px !important;
            padding: 0 !important;
            margin: -1px !important;
            overflow: hidden !important;
            clip: rect(0,0,0,0) !important;
            white-space: nowrap !important;
            border: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Header con diseño mejorado
st.markdown("""
    <div class="header-container">
        <h1>🤖 Detector de Textos Suicidas</h1>
        <p style='font-size: 1.2rem;'>Una herramienta de IA para identificar contenido potencialmente suicida</p>
    </div>
    """, unsafe_allow_html=True)

# Crear dos columnas
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Ingrese el texto a analizar")
    # Usar label_visibility="collapsed" para mantener la accesibilidad sin mostrar visualmente la etiqueta
    text_input = st.text_area(
        label="Texto para análisis",  # Etiqueta significativa para accesibilidad
        label_visibility="collapsed",  # Ocultar visualmente pero mantener para lectores de pantalla
        height=200,
        placeholder="Escriba o pegue aquí el texto que desea analizar..."
    )

    if st.button("🔍 Analizar Texto"):
        if text_input.strip() != "":
            with st.spinner('Analizando el texto...'):
                try:
                    response = requests.post(
                        "http://localhost:8000/predict",
                        json={"text": text_input}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Contenedor para resultados
                        st.markdown("### 📊 Resultados del Análisis")
                        results_container = st.container()
                        
                        with results_container:
                            # Mostrar predicción con diseño mejorado
                            if result["is_suicidal"]:
                                st.error("⚠️ ALERTA: Se ha detectado contenido suicida")
                                st.markdown("""
                                    <div style='background-color: #ffe6e6; padding: 1rem; border-radius: 10px; border-left: 5px solid #ff4b4b;'>
                                        <h4 style='color: #ff4b4b;'>Recursos de Ayuda:</h4>
                                        <ul>
                                            <li>Línea Salud Mental Responde: 0800-333-1665</li>
                                        </ul>
                                    </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.success("✅ No se ha detectado contenido suicida")
                            
                            # Mostrar confianza con una barra de progreso
                            confidence = result['confidence']
                            st.markdown("#### Nivel de Confianza")
                            st.progress(confidence)
                            st.markdown(f"<p style='text-align: center; font-size: 1.2rem;'>{confidence:.1%}</p>", unsafe_allow_html=True)
                    
                    else:
                        st.error("❌ Error al procesar la solicitud")
                
                except Exception as e:
                    st.error(f"❌ Error de conexión: {str(e)}")
        else:
            st.warning("⚠️ Por favor, ingrese un texto para analizar")

with col2:
    # Información adicional
    st.markdown("""
    ### ℹ️ Acerca de esta herramienta
    
    Esta aplicación utiliza inteligencia artificial para analizar textos y detectar posible contenido suicida. 
    
    **¿Cómo funciona?**
    1. Ingrese el texto que desea analizar
    2. Presione el botón "Analizar"
    3. Reciba resultados instantáneos
    
    **Importante:**
    - Esta herramienta es solo para ayuda
    - No reemplaza el juicio profesional
    - En caso de emergencia, busque ayuda profesional
    
    ---
    ### 🆘 Recursos de Ayuda
    - Línea Salud Mental Responde
    - Disponible 24/7
    - Llame al 0800-333-1665
    """)

# Footer
st.markdown("""
    ---
    <p style='text-align: center; color: #666;'>
        Desarrollado con ❤️ para ayudar a salvar vidas
    </p>
    """, unsafe_allow_html=True)