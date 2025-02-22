import streamlit as st

def app():
    st.title("Home")


    # Título da página
    st.title("📊 Bem-vindo ao MarketView!")

    # Descrição do app
    st.write('')
    st.write('')
    st.write("""
        O **MarketView** é a sua plataforma para acompanhar indicadores financeiros e econômicos.  
        Utilize o menu lateral para explorar as diversas páginas e funcionalidades do sistema, como:
        - **Calendário Econômico**
             
        - **Panorama do Mercado**
             
        - **Análise Histórica**
             - Retorno Mensal
             - Desempenho Relativo

        - **Política Monetária**
             - Selic
             - IPCA

        - **Fundamentos de Ações**
             - Dados Balanço Patrimonial
             - Dados Domonstrativos de Resultados
             - Indicadores Fundamentalista
             - Performace entre ações

        
    """)


