import streamlit as st
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def app():
    st.title('Análise Histórica')
    st.subheader('Retorno Mensal')
   



    # Formulário principal
    with st.form(key='form_ativo'):
        opcao = st.radio('', ['Índices', 'Ações', 'Commodities'])

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
            
            escolha = st.selectbox('Selecione o Ativo:', list(indices.keys()))
            analisar = st.form_submit_button('Analisar')
            ticker = indices[escolha]

        elif opcao == 'Commodities':
            commodities = {'Ouro': 'GC=F',
                        'Prata': 'SI=F',
                        'Platinum': 'PL=F',     
                        'Cobre': 'HG=F',
                        
                        'WTI Oil':'CL=F',
                        'Brent Oil':'BZ=F',
                        'Gasolina':'RB=F',
                        'Gás Natural':'NG=F',
                        
                        'Gado Vivo':'LE=F',
                        'Porcos Magros':'LE=F',

                        'Milho':'ZC=F',
                        'Soja':'ZS=F',
                        'Cacau':'CC=F',
                        'Café':'KC=F'}    
            
            escolha = st.selectbox('Selecione o Ativo:', list(commodities.keys()))
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

            escolha = st.selectbox('Selecione o Ativo:', list(acoes_dict.keys()))
            analisar = st.form_submit_button('Analisar')
            ticker = acoes_dict[escolha]
            if analisar:
                st.write(f'Você selecionou a ação: {escolha}')
                st.write(f'Ticker: {ticker}')

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
    @st.cache_data(ttl=600)  # Cache atualizado a cada 10 min
    def carregar_dados(tickers, data_inicio, data_fim):
        if not tickers:
            return pd.DataFrame()
        
        dados = {}
        for ticker in tickers:
            hist = yf.Ticker(ticker).history(start=data_inicio, end=data_fim)['Close']
            dados[ticker] = hist
        
        return pd.DataFrame(dados).dropna()  # Remove valores NaN

    def calcular_performance(dados):
        if not dados.empty:
            return (dados / dados.iloc[0] - 1) * 100
        return dados

    def criar_grafico(ativos_selecionados, dados, normalizado=True, legenda_dict=None):
        fig = go.Figure()
        for ativo in ativos_selecionados:
            nome_ativo = legenda_dict.get(ativo, ativo)  # Usa a chave do dicionário para o nome
            # Dados normalizados ou brutos
            y_data = calcular_performance(dados)[ativo] if normalizado else dados[ativo]
            
            # Adicionando linha do gráfico
            fig.add_trace(go.Scatter(
                x=dados.index,
                y=y_data,
                name=nome_ativo,  # Utiliza a chave do dicionário na legenda
                mode='lines',  # Apenas a linha
                line=dict(width=1)
            ))
            
            # Adicionando bolinha no último ponto
            fig.add_trace(go.Scatter(
                x=[dados.index[-1]],  # Último ponto do gráfico
                y=[y_data.iloc[-1]],  # Último valor
                mode='markers',
                marker=dict(size=5, color='red', symbol='circle'),
                name=f'{nome_ativo} - Último Preço',
                showlegend=False
            ))

        # Ajustando a data do eixo X para intervalo de 1 ano
        fig.update_layout(
            title=f"{'Desempenho Relativo (%)' if normalizado else 'Preço dos Ativos'}",
            xaxis_title='Data',
            yaxis_title='Performance (%)' if normalizado else 'Preço',
            xaxis=dict(
                tickformat='%Y',  # Exibe o ano
                tickmode='array',  # Define um modo de marcação personalizada
                tickvals=dados.index[::252],  # Marca um ponto a cada 252 dias (aproximadamente 1 ano de pregão)
            ),
            legend_title='Ativos',
            legend_orientation='h',
            plot_bgcolor='rgba(211, 211, 211, 0.15)',
            height=600,
            margin=dict(r=10)  # Ajusta a margem à direita
        )
        fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot')

        return fig

    st.subheader('Desempenho Relativo')

    with st.form(key='formulario_dados'):
        opcao1 = st.selectbox('Selecione:', ['Índices', 'Ações', 'Commodities'])

        indices = {'IBOV': '^BVSP','EWZ':'EWZ', 'S&P500': '^GSPC', 'NASDAQ': '^IXIC', 'FTSE100': '^FTSE', 'DAX': '^GDAXI', 
                'CAC40': '^FCHI', 'SSE Composite': '000001.SS', 'Nikkei225': '^N225', 'Merval': '^MERV'}

        commodities = {'Ouro': 'GC=F',
                        'Prata': 'SI=F',
                        'Platinum': 'PL=F',     
                        'Cobre': 'HG=F',
                        
                        'WTI Oil':'CL=F',
                        'Brent Oil':'BZ=F',
                        'Gasolina':'RB=F',
                        'Gás Natural':'NG=F',
                        
                        'Gado Vivo':'LE=F',
                        'Porcos Magros':'LE=F',

                        'Milho':'ZC=F',
                        'Soja':'ZS=F',
                        'Cacau':'CC=F',
                        'Café':'KC=F'}    

        acoes = ["PETR4", "VALE3","ITUB4", "BBAS3", "BBDC4",
                "RAIZ4","PRIO3", "VBBR3", "CSAN3", "UGPA3",  
                "BPAC11", "SANB11", "GGBR4", "CSNA3", "USIM5",  
                "JBSS3", "ABEV3", "MRFG3", "BRFS3", "BEEF3",  
                "ELET3", "NEOE3", "CPFE3", "ENGI11", "EQTL3",  
                "SUZB3", "KLBN11", "DTEX3", "RANI3", "MRFG3", 
                "CYRE3", "MRVE3", "EZTC3", "CVCB3", "TRIS3", 
                "WEGE3", "B3SA3"]

        acoes_dict = {acao: acao + '.SA' for acao in acoes}

        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            if opcao1 == '':
                escolha = st.multiselect('Índice', list(indices.keys()), placeholder='Ativos')
                ticker = [indices[indice] for indice in escolha]
                legenda_dict = {v: k for k, v in indices.items()}  # Inverte o dicionário para a legenda

            elif opcao1 == '':
                escolha = st.multiselect('Commodities', list(commodities.keys()), placeholder='Ativos')
                ticker = [commodities[commodity] for commodity in escolha]
                legenda_dict = {v: k for k, v in commodities.items()}  # Inverte o dicionário para a legenda

            elif opcao1 == '':
                escolha = st.multiselect('Ações', list(acoes_dict.keys()), placeholder='Ativos')
                ticker = [acoes_dict[acao] for acao in escolha]
                legenda_dict = {v: k for k, v in acoes_dict.items()}  # Inverte o dicionário para a legenda

        with col2:
            data_inicio = st.date_input('Data de início', pd.to_datetime('2020-01-01').date(), format='DD/MM/YYYY')
        with col3:
            data_fim = st.date_input('Data de término', pd.to_datetime('today').date(), format='DD/MM/YYYY')

        submit_button = st.form_submit_button(label='Carregar Dados')

    # Verificar se nenhum ativo foi selecionado
    if submit_button:
        if not ticker:
            st.error("Por favor, selecione pelo menos um ativo antes de continuar.")  # Exibe erro se nenhum ativo for selecionado
        else:
            # Opção para visualizar valores normalizados ou brutos
            normalizado = st.checkbox("Exibir desempenho percentual", value=True)

            # Carregar os dados reais
            dados = carregar_dados(ticker, data_inicio, data_fim)
            if not dados.empty:
                fig = criar_grafico(ticker, dados, normalizado, legenda_dict)
                st.plotly_chart(fig)
            else:
                st.warning("Nenhum dado disponível para os tickers selecionados.")


