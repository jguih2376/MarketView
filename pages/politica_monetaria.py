import streamlit as st
import matplotlib.pyplot as plt
from bcb import sgs

@st.cache_data
def get_data():
    selic = sgs.get({'Selic': 432}, start='2000-01-01')
    selic_atual = selic.iloc[-1].values[0]
    ipca = sgs.get({'IPCA': 13522}, start='2000-01-01')
    ipca_atual = ipca.iloc[-1].values[0]
    return selic, selic_atual, ipca, ipca_atual

def app():
    st.title("Política Monetária")
    st.write("Atualizações sobre a política monetária.")

    # Obtendo dados com cache
    selic, selic_atual, ipca, ipca_atual = get_data()


    col1, col2 = st.columns([3, 1])
    with col1:
        # Plotando a série histórica da Selic com grelha
        fig, ax = plt.subplots(figsize=(8, 4))
        selic['Selic'].plot(ax=ax, kind='line', title='Taxa de Juros SELIC')
        ax.spines[['top', 'right']].set_visible(False)
        ax.set_ylabel('Taxa de Juros (%)')
        ax.grid(True, axis='y', linestyle='--', linewidth=0.5, color='gray')
        ax.scatter(selic.index[-1], selic_atual, color='red', zorder=5, label=f'Atual: {selic_atual:.2f}%')
        ax.legend()
        st.pyplot(fig)

        st.write('')
        st.write('')

        # Plotando Gráfico IPCA
        fig, ax = plt.subplots(figsize=(8, 4))
        ipca['IPCA'].plot(ax=ax, kind='line', title='IPCA Acumulado 12M')
        ax.spines[['top', 'right']].set_visible(False)
        ax.set_ylabel('IPCA acumulado (%)')
        ax.grid(True, axis='y', linestyle='--', linewidth=0.5, color='gray')
        ax.scatter(ipca.index[-1], ipca_atual, color='red', zorder=5, label=f'Atual: {ipca_atual:.2f}%')
        ax.legend()
        st.pyplot(fig)

    with col2:
        st.write('')
        st.write('')

        # Exibindo o iframe com alinhamento ajustado
        iframe_code = """
        <div style="text-align: center; padding: 10px; font-family: sans-serif;">
            <span style="font-size: 16px; font-weight: bold; display: block; margin-bottom: 8px; color: white;">Mundo</span>
            <iframe frameborder="0" scrolling="no" height="146" width="108" allowtransparency="true" marginwidth="0" marginheight="0" 
            src="https://sslirates.investing.com/index.php?rows=1&bg1=FFFFFF&bg2=F1F5F8&text_color=333333&enable_border=hide&border_color=0452A1&
            header_bg=ffffff&header_text=FFFFFF&force_lang=12" align="center"></iframe>
        </div>
        """

        st.components.v1.html(iframe_code, height=180)
