import streamlit as st

def app():
    st.title("📊 Bem-vindo ao MarketView!")

    # Descrição do app
    st.write('---')
    st.write("""  
        O **MarketView** é a sua plataforma para acompanhar indicadores financeiros e econômicos, 
        trazendo informações cruciais para a tomada de decisões inteligentes e embasadas. 
        Explore as diversas funcionalidades do sistema utilizando o menu lateral:

        ### Funcionalidades:
        
        - **Calendário Econômico**  
        Acompanhe eventos importantes e datas chave para o mercado financeiro.

        &nbsp;

        - **Panorama do Mercado**  
        Obtenha uma visão geral dos principais indicadores econômicos e financeiros globais.

        &nbsp;

        - **Análise Histórica**  
        Ferramentas para comparar o desempenho de ativos ao longo do tempo:
            - **Retorno Mensal**  
            Analise os retornos mensais dos ativos selecionados.
            - **Desempenho Relativo**  
            Compare o desempenho de diferentes ativos de forma relativa.

        &nbsp;

        - **Política Monetária**  
        Mantenha-se informado sobre as principais políticas monetárias:
            - **Selic**  
            Acompanhe a taxa de juros básica da economia brasileira.
            - **IPCA**  
            Acompanhe o Índice de Preços ao Consumidor Amplo (IPCA), o principal indicador da inflação no Brasil.

        &nbsp;

        - **Fundamentos de Ações**  
        Avalie a saúde financeira das empresas:
            - **Dados de Balanço Patrimonial**  
            Acesse os dados financeiros das empresas.
            - **Demonstrações de Resultados**  
            Consulte as demonstrações financeiras das empresas.
            - **Indicadores Fundamentalistas**  
            Obtenha indicadores como P/L, ROE, e outros.
            - **Performance entre Ações**  
            Compare o desempenho histórico entre diferentes ações.

        &nbsp;

        Explore agora e aproveite ao máximo todas as funcionalidades do **MarketView**!
    """)
