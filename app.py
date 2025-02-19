import streamlit as st
from pages import home, calendario_economico, panorama_do_mercado, retorno_mensal, politica_monetaria, fundamentos, criptos

# Configuração global do Streamlit
st.set_page_config(
    page_title="MarketView",  # Título que aparecerá na aba do navegador
    page_icon="📈",           # Ícone na aba do navegador
    layout="wide"             # Layout em tela cheia
)

# Inicializar o estado da página
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Barra lateral com navegação usando radio
st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Escolha uma página", 
    ["Home", "Calendário Econômico", "Panorama do Mercado", "Retorno Mensal", "Política Monetária", "Fundamentos", "Criptos"]
)

# Redirecionar para as páginas conforme a escolha do usuário
if pagina == "Home":
    home.app()
elif pagina == "Calendário Econômico":
    calendario_economico.app()
elif pagina == "Panorama do Mercado":
    panorama_do_mercado.app()
elif pagina == "Retorno Mensal":
    retorno_mensal.app()
elif pagina == "Política Monetária":
    politica_monetaria.app()
elif pagina == "Fundamentos":
    fundamentos.app()
elif pagina == "Criptos":
    criptos.app()
