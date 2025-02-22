import streamlit as st
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def app():
    st.write('Análise Histórica')
    st.subheader('Retorno Mensal')
    with st.expander('...', expanded=True):
        opcao = st.radio('Selecione', ['Índices', 'Ações', 'Commodities'])

        if opcao == 'Índices':
            indices = {'IBOV': '^BVSP',
                        'S&P500': '^GSPC',     
                        'NASDAQ': '^IXIC',
                        'FTSE100':'^FTSE',
                        'DAX':'^GDAXI',
                        'CAC40':'^FCHI',
                        'SSE Composite':'000001.SS',
                        'Nikkei225':'^N225',
                        'Merval':'^MERV'}
            with st.form(key='form_indice'):
                escolha = st.selectbox('Índice', list(indices.keys()))
                analisar = st.form_submit_button('Analisar')
                ticker = indices[escolha]

        elif opcao == 'Commodities':
            commodities = {'Ouro': 'GC=F',
                        'Prata': 'SI=F',
                        'Platinum': 'PL=F',     
                        'Cobre': 'HG=F',
                        'WTI Oil':'CL=F',
                        'Brent Oil':'BZ=F',
                        'Milho':'ZC=F',
                        'Soja':'ZS=F',
                        'Café':'KC=F'}    
            with st.form(key='form_commodities'):
                escolha = st.selectbox('Commodities', list(commodities.keys()))
                analisar = st.form_submit_button('Analisar')
                ticker = commodities[escolha]

        elif opcao == 'Ações':
            acoes = ['ALOS3', 'ABEV3', 'ASAI3', 'AURE3', 'AMOB3', 'AZUL4', 'AZZA3', 'B3SA3', 'BBSE3', 'BBDC3', 'BBDC4', 
                    'BRAP4', 'BBAS3', 'BRKM5', 'BRAV3', 'BRFS3', 'BPAC11', 'CXSE3', 'CRFB3', 'CCRO3', 'CMIG4', 'COGN3', 
                    'CPLE6', 'CSAN3', 'CPFE3', 'CMIN3', 'CVCB3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENGI11', 'ENEV3', 
                    'EGIE3', 'EQTL3', 'FLRY3', 'GGBR4', 'GOAU4', 'NTCO3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ISAE4', 
                    'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'RENT3', 'LREN3', 'LWSA3', 'MGLU3', 'POMO4', 'MRFG3', 'BEEF3', 
                    'MRVE3', 'MULT3', 'PCAR3', 'PETR3', 'PETR4', 'RECV3', 'PRIO3', 'PETZ3', 'PSSA3', 'RADL3', 'RAIZ4', 
                    'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'STBP3', 'SMTO3', 'CSNA3', 'SLCE3', 'SUZB3', 'TAEE11', 'VIVT3', 
                    'TIMS3', 'TOTS3', 'UGPA3', 'USIM5', 'VALE3', 'VAMO3', 'VBBR3', 'VIVA3', 'WEGE3', 'YDUQ3']

            # Criando um dicionário com chave como o nome da ação e valor como o nome da ação com '.SA'
            acoes_dict = {acao: acao + '.SA' for acao in acoes}

            with st.form(key='form_acoes'):
                escolha = st.selectbox('Ações', list(acoes_dict.keys()))
                analisar = st.form_submit_button('Analisar')
                ticker = acoes_dict[escolha]

    if analisar:
        data_inicial = ('1999-12-01')
        data_final = ('2030-12-31')

        # Baixa os dados do Yahoo Finance
        dados = yf.download(ticker, start=data_inicial, end=data_final, interval="1mo")

        if not dados.empty:
            retornos = dados['Close'].pct_change().dropna()
            # Adiciona colunas de ano e mês para organização
            retornos = retornos.reset_index()
            retornos['Year'] = retornos['Date'].dt.year
            retornos['Month'] = retornos['Date'].dt.month

            # Criar a tabela pivot sem média, apenas reorganizando os dados
            tabela_retornos = retornos.pivot(index='Year', columns='Month', values=ticker)
            tabela_retornos.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                                        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

            # Criando Heatmap
            fig, ax = plt.subplots(figsize=(12, 9))
            cmap = sns.color_palette('RdYlGn', 15)
            sns.heatmap(tabela_retornos, cmap=cmap, annot=True, fmt='.2%', center=0, vmax=0.025, vmin=-0.025, cbar=False,
                        linewidths=0.5, xticklabels=True, yticklabels=True, ax=ax)
            ax.set_title(f'Heatmap Retorno Mensal - {escolha}', fontsize=18)
            ax.set_yticklabels(ax.get_yticklabels(), rotation=0, verticalalignment='center', fontsize='12')
            ax.set_xticklabels(ax.get_xticklabels(), fontsize='12')
            plt.ylabel('')
            st.pyplot(fig)

            # Estatísticas
            stats = pd.DataFrame(tabela_retornos.mean(), columns=['Média'])
            stats['Mediana'] = tabela_retornos.median()
            stats['Maior'] = tabela_retornos.max()
            stats['Menor'] = tabela_retornos.min()
            stats['Positivos'] = tabela_retornos.gt(0).sum() / tabela_retornos.count() # .gt(greater than) = Contagem de números maior que zero
            stats['Negativos'] = tabela_retornos.le(0).sum() / tabela_retornos.count() # .le(less than) = Contagem de números menor que zero

            # Stats_A
            stats_a = stats[['Média', 'Mediana', 'Maior', 'Menor']].transpose()

            fig, ax = plt.subplots(figsize=(12, 2))
            sns.heatmap(stats_a, cmap=cmap, annot=True, fmt='.2%', center=0, vmax=0.025, vmin=-0.025, cbar=False,
                        linewidths=0.5, xticklabels=True, yticklabels=True, ax=ax)
            st.pyplot(fig)

            # Stats_B
            stats_b = stats[['Positivos', 'Negativos']].transpose()

            fig, ax = plt.subplots(figsize=(12, 1))
            sns.heatmap(stats_b, cmap=sns.color_palette("magma", as_cmap=True), annot=True, fmt='.2%', center=0, vmax=0.025, vmin=-0.025, cbar=False,
                        linewidths=0.5, xticklabels=True, yticklabels=True, ax=ax)
            st.pyplot(fig)

        else:
            st.error("Erro ao buscar os dados. Verifique o ticker ou tente novamente mais tarde.")

#________________________________________________________________________________________________________________________________________________________
    st.markdown('---')
    # Função para carregar os dados usando yfinance
    @st.cache_data
    def carregar_dados(tickers, data_inicio, data_fim):
        dados = {}
        for ticker in tickers:
            hist = yf.Ticker(ticker).history(start=data_inicio, end=data_fim)['Close']
            dados[ticker] = hist
        return pd.DataFrame(dados)

    def calcular_performance(dados):
        # Função para calcular a performance em percentual
        if not dados.empty:
            return (dados / dados.iloc[0] - 1) * 100
        return dados

    def criar_grafico(ativos_selecionados, dados):
        fig = go.Figure()
        for ativo in ativos_selecionados:
            fig.add_trace(go.Scatter(
                x=dados.index,
                y=dados[ativo],
                name=ativo,
                line=dict(width=1)
            ))

        fig.update_layout(
            title='Desempenho Relativo dos Ativos (%)',
            xaxis_title='Data',
            yaxis_title='Performance (%)',
            xaxis=dict(tickformat='%m/%Y'),
            legend_title='Ativo',
            legend_orientation='h',
            plot_bgcolor='rgba(211, 211, 211, 0.15)'  # Cor de fundo cinza claro   
        )
        fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot')

        return fig

    st.subheader('Desempenho Relativo')

    opcao1 = st.radio('Selecione', ['Índices', 'Ações', 'Commodities'])

    indices = {'IBOV': '^BVSP', 'S&P500': '^GSPC', 'NASDAQ': '^IXIC', 'FTSE100': '^FTSE', 'DAX': '^GDAXI', 
            'CAC40': '^FCHI', 'SSE Composite': '000001.SS', 'Nikkei225': '^N225', 'Merval': '^MERV'}

    commodities = {'Ouro': 'GC=F', 'Prata': 'SI=F', 'Platina': 'PL=F', 'Cobre': 'HG=F', 'WTI Oil': 'CL=F', 
                'Brent Oil': 'BZ=F', 'Milho': 'ZC=F', 'Soja': 'ZS=F', 'Café': 'KC=F'}

    acoes = ['ALOS3', 'ABEV3', 'ASAI3', 'AURE3', 'AMOB3', 'AZUL4', 'AZZA3', 'B3SA3', 'BBSE3', 'BBDC3', 'BBDC4', 
            'BRAP4', 'BBAS3', 'BRKM5', 'BRAV3', 'BRFS3', 'BPAC11', 'CXSE3', 'CRFB3', 'CCRO3', 'CMIG4', 'COGN3', 
            'CPLE6', 'CSAN3', 'CPFE3', 'CMIN3', 'CVCB3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENGI11', 'ENEV3', 
            'EGIE3', 'EQTL3', 'FLRY3', 'GGBR4', 'GOAU4', 'NTCO3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ISAE4', 
            'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'RENT3', 'LREN3', 'LWSA3', 'MGLU3', 'POMO4', 'MRFG3', 'BEEF3', 
            'MRVE3', 'MULT3', 'PCAR3', 'PETR3', 'PETR4', 'RECV3', 'PRIO3', 'PETZ3', 'PSSA3', 'RADL3', 'RAIZ4', 
            'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'STBP3', 'SMTO3', 'CSNA3', 'SLCE3', 'SUZB3', 'TAEE11', 'VIVT3', 
            'TIMS3', 'TOTS3', 'UGPA3', 'USIM5', 'VALE3', 'VAMO3', 'VBBR3', 'VIVA3', 'WEGE3', 'YDUQ3']

    acoes_dict = {acao: acao + '.SA' for acao in acoes}
    col1,col2,col3=st.columns([4,1,1])

    with col1:
        if opcao1 == 'Índices':
            escolha = st.multiselect('Índice', list(indices.keys()), placeholder='Ativos')
            ticker = [indices[indice] for indice in escolha]

        elif opcao1 == 'Commodities':
            escolha = st.multiselect('Commodities', list(commodities.keys()), placeholder='Ativos')
            ticker = [commodities[commodity] for commodity in escolha]

        elif opcao1 == 'Ações':
            escolha = st.multiselect('Ações', list(acoes_dict.keys()), placeholder='Ativos')
            ticker = [acoes_dict[acao] for acao in escolha]

    with col2:
        data_inicio = st.date_input('Data de início', pd.to_datetime('2015-01-01').date(), format='DD/MM/YYYY')
    with col3:
        data_fim = st.date_input('Data de término', pd.to_datetime('today').date(), format='DD/MM/YYYY')

    # Carregar os dados reais
    dados = carregar_dados(ticker, data_inicio, data_fim)
    if not dados.empty:
        fig = criar_grafico(ticker, calcular_performance(dados))
        st.plotly_chart(fig)
    else:
        st.write("Nenhum dado disponível para os tickers selecionados.")

