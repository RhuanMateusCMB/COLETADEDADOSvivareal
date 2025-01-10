import streamlit as st
import pandas as pd
from supabase import create_client
import plotly.express as px
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Teste de Gráficos - CMB Capital",
    page_icon="📊",
    layout="wide"
)

# Classe para gerenciar conexão com Supabase
class SupabaseManager:
    def __init__(self):
        self.url = st.secrets["SUPABASE_URL"]
        self.key = st.secrets["SUPABASE_KEY"]
        self.supabase = create_client(self.url, self.key)

    def obter_dados(self):
        try:
            response = self.supabase.table('teste').select("*").execute()
            if response.data:
                st.success("Dados carregados com sucesso!")  # Debug
                return pd.DataFrame(response.data)
            else:
                st.warning("Nenhum dado encontrado na tabela")  # Debug
                return None
        except Exception as e:
            st.error(f"Erro ao obter dados do Supabase: {str(e)}")
            return None

def main():
    # Título e descrição
    st.title("📊 Teste de Gráficos")
    
    # Inicializar conexão com Supabase
    db = SupabaseManager()
    df = db.obter_dados()

    # Debug: Mostra as primeiras linhas do DataFrame
    st.write("Preview dos dados:")
    st.write(df.head())

    if df is not None and not df.empty:
        # Convertendo a coluna de data
        df['data_coleta'] = pd.to_datetime(df['data_coleta'])
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Registros", len(df))
        with col2:
            preco_medio = df['preco_real'].mean()
            st.metric("Preço Médio", f"R$ {preco_medio:,.2f}")
        with col3:
            area_media = df['area_m2'].mean()
            st.metric("Área Média", f"{area_media:,.2f} m²")
        with col4:
            preco_m2_medio = df['preco_m2'].mean()
            st.metric("Preço/m² Médio", f"R$ {preco_m2_medio:,.2f}")

        # Visualizações
        st.markdown("### 📈 Visualizações")
        
        try:
            # Gráfico de dispersão: Preço x Área
            st.write("Tentando criar o gráfico de dispersão...")  # Debug
            fig_scatter = px.scatter(
                df,
                x='area_m2',
                y='preco_real',
                title='Relação entre Área e Preço',
                labels={'area_m2': 'Área (m²)', 'preco_real': 'Preço (R$)'},
                hover_data=['endereco', 'preco_m2']
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.success("Gráfico de dispersão criado com sucesso!")  # Debug

            # Distribuição de preços por m²
            st.write("Tentando criar o histograma...")  # Debug
            fig_hist = px.histogram(
                df,
                x='preco_m2',
                title='Distribuição de Preços por m²',
                labels={'preco_m2': 'Preço por m² (R$)', 'count': 'Quantidade'},
                nbins=30
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            st.success("Histograma criado com sucesso!")  # Debug

        except Exception as e:
            st.error(f"Erro ao criar os gráficos: {str(e)}")
            st.write("Estrutura do DataFrame:")
            st.write(df.dtypes)

    else:
        st.warning("Não há dados disponíveis para visualização.")

if __name__ == "__main__":
    main()
