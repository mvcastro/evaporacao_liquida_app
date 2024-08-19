import pandas as pd
import streamlit as st
from sqlalchemy import Engine, create_engine

from charts import get_plotly_fig
from db_access import (
    retorna_esp_cds,
    retorna_evapo_liquida_novo_por_esp_cd,
    retorna_dados_tabelas_por_esp_cd
)

st.set_page_config(layout="wide")

st.header("Resultados de Evaporação Líquida Média Mensal")
st.divider()

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(sep=";").encode("utf-8")

@st.cache_resource
def create_connection() -> Engine:
    engine = create_engine("sqlite:///database.db")
    return engine

@st.cache_data
def get_esp_cds(_engine: Engine) -> list[str]:
    return retorna_esp_cds(engine=_engine)

@st.cache_data
def get_data_by_esp_cd(_engine: Engine, esp_cd: int) -> pd.DataFrame:
    return retorna_evapo_liquida_novo_por_esp_cd(engine=_engine, esp_cd=esp_cd)

@st.cache_data
def get_data_comp_by_esp_cd(_engine: Engine, esp_cd: int) -> pd.DataFrame:
    return retorna_dados_tabelas_por_esp_cd(engine=_engine, esp_cd=esp_cd)

engine = create_connection()
esp_cds = get_esp_cds(engine)

with st.sidebar:
    esp_cd = st.selectbox(
        label="Esp-cd do Reservatório:",
        options=esp_cds
    )
    
    if esp_cd:
        esp_cd_int = int(esp_cd.split("-")[0].strip())
        df_evp_liq = get_data_by_esp_cd(_engine=engine, esp_cd=esp_cd_int)
        df_comp = get_data_comp_by_esp_cd(_engine=engine, esp_cd=esp_cd_int)
        csv_data = convert_df(df_comp)
        
        st.divider()
        st.info('Clique no botão para baixar os dados do Reservatório:', icon="ℹ️")
        st.download_button(
            label="Download data as CSV",
            data=csv_data,
            file_name=f"dados_evap_liq_esp_cd_{esp_cd_int}.csv",
            mime="text/csv",
    )
    
if esp_cd:

    
    st.plotly_chart(get_plotly_fig(
        df_evp_liq[['evp_lago_mm', 'etr_mm', 'evp_liq_mm']],
        title="Resultado Evaporação [MM]:"
        ),
        use_container_width=True
    )
    
    st.plotly_chart(get_plotly_fig(
        df_evp_liq[['evp_liq_m3_s']],
        title="Resultado Evaporação [M³/S]:"
        ),
        use_container_width=True
    )
    
    st.header("Comparação do Resultado Atual com Anterior:")
    st.divider()
    
    st.plotly_chart(get_plotly_fig(
        df_comp[['el_mm_2021', 'el_mm_2024']],
        title="Evaporação Líquida [MM]:"
        ),
        use_container_width=True
    )
        
    st.plotly_chart(get_plotly_fig(
        df_comp[['area_2021', 'area_2024',]],
        title="Área [KM²]:"
        ),
        use_container_width=True
    )
        
    st.plotly_chart(get_plotly_fig(
        df_comp[['el_m3_s_2021', 'el_m3_s_2024']],
        title="Evaporação Líquida [M³/S]:"
        ),
        use_container_width=True
    )
    