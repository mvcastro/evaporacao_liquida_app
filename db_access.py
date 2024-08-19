import pandas as pd
from sqlalchemy import Engine, text


def retorna_esp_cds(engine: Engine) -> list[str]:
    
    sql = "SELECT esp_cd, nome FROM inventario ORDER BY esp_cd"
    
    with engine.connect() as conn:
        resposta = conn.execute(text(sql))
        esp_cds = [f"{i[0]} - {i[1]}" for i in resposta]
    
    return esp_cds


def retorna_evapo_liquida_novo_por_esp_cd(engine: Engine, esp_cd: int) -> pd.DataFrame:

    sql = """SELECT esp_cd,
                    cod_sar,
                    ano,
                    mes,
                    evp_lago_mm,
                    etr_mm,
                    evp_liq_mm,
                    evp_liq_m3_s,
                    area_km2,
                    fonte_area
            FROM evap_liquida_novo
             WHERE esp_cd = :esp_cd
             ORDER BY ano, mes"""
    df = pd.read_sql(sql=text(sql), con=engine, params={'esp_cd': esp_cd})
    period = pd.PeriodIndex.from_fields(year=df.ano, month=df.mes, day=15, freq='D').to_timestamp()  # type: ignore
    df.set_index(period, inplace=True, drop=True)

    return df


def retorna_evapo_liquida_anterior_por_esp_cd(engine: Engine, esp_cd: int) -> pd.DataFrame:

    sql = """SELECT esp_cd,
                    cod_sar, 
                    ano,
                    mes,
                    evp_liq_mm,
                    area_km2,
                    vazao_m3_s,
                    fonte_area
	         FROM evap_liquida_anterior
             WHERE esp_cd = :esp_cdc
             ORDER BY ano, mes"""
    df = pd.read_sql(sql=text(sql), con=engine, params={'esp_cd': esp_cd},
    )
    period = pd.PeriodIndex.from_fields(year=df.ano, month=df.mes, day=15, freq='D').to_timestamp()  # type: ignore
    df.set_index(period, inplace=True, drop=True)

    return df


def retorna_dados_tabelas_por_esp_cd(engine: Engine, esp_cd: int) -> pd.DataFrame:

    sql = """SELECT esp_cd,
                    ano,
                    mes,
                    a.evp_liq_mm AS el_mm_2021,
                    b.evp_liq_mm AS el_mm_2024,
                    a.area_km2 AS area_2021,
                    b.area_km2 AS area_2024,
                    a.vazao_m3_s AS el_m3_s_2021,
                    b.evp_liq_m3_s AS el_m3_s_2024
	         FROM evap_liquida_novo b
             LEFT JOIN evap_liquida_anterior a USING (esp_cd, ano, mes)
             WHERE esp_cd = :esp_cd
             ORDER BY ano, mes"""
    df = pd.read_sql(sql=text(sql), con=engine, params={'esp_cd': esp_cd})
    period = pd.PeriodIndex.from_fields(year=df.ano, month=df.mes, day=15, freq='D').to_timestamp()  # type: ignore
    df.set_index(period, inplace=True, drop=True)

    return df

