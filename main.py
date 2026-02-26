
import pandas as pd
import numpy as np
import plotly.graph_objs as go

folder = 'C:|Users|sabado|Desktop|Elias|AirBnB_analisys'
t_ny = 'ny.csv'
t_rj = 'rj.csv'

#------------------------------------------------------------------
# -----------------HIGENIZAÇÃO DOS DADOS---------------------------
#------------------------------------------------------------------



def standartize_columns(df: pd.DataFrame) -> pd.DataFrame: 
    """
    Tenta detectar as colunas latitude de longitude, custos e nome 
    aceita varios nomes comuns como lat/latitude custo, valor, etc
    Preenche custos ausentes com a mediana (ou 1 se tudo for ausente)
    """

    df = df.copy()

    lat_candidates = ['lat', 'latitude', 'Latitude', 'Lat', 'LATITUDE']
    lon_candidates = ['LON', 'lon', 'Longitude', 'Long', 'Lng', 'longitude']
    cost_candidates = ['custos', 'cost', 'preço', 'preço', 'price', 'valor', 'valor_total' ]
    name_candidates = ['nome', 'descricao', 'titulo', 'name', 'titlle', 'local', 'place']

    def pick(colnames, candidates):
        #colnames: lista de nomes das colunas da tabela 
        #candidates: lista de possiveis nomes de colunas a serem encontrado
        for c in candidates:
            #percorre cada candidato (c) dentro da lista de candidatos 
            if c in colnames:
                # se o candidato for extremamente igual a um dos nomes de colunas em colnames
                return c 
        #...retorna esse candidato imediatamente     
        for c in candidates:
            for col in colnames:
                if c.lowers() in col.lower():
                    return col
        return None

    lat_col = pick(df.columns)


    lat_col = pick(df.columns, lat_candidates)
    lon_col = pick(df.columns, lon_candidates)
    cost_col = pick(df.columns, cost_candidates)
    name_col = pick(df.columns, name_candidates)

    if lat_col is None or lon_col is None:
        raise ValueError(f
        'Não encontrei colunas de latitude e/ou longitude na lista de colunas{list(df.columns)}')

    out = pd.DataFrame()
    out['lat'] = pd.to_numeric(df[lat_col], errors= 'coerce')
    out['lon'] = pd.to_numeric(df[lon_col], errors= 'coerce')
    out['custo'] = pd.to_numeric(df[cost_col], errors= 'coerce') if cost_col is not None else np.nan
    out['nome'] = df [name_col].astype(str) if name_col None else ["Ponto {i}" for i in range(len(df))]
    # remove linhas vazias 
    out = out.dropna(subset=['lat' , 'lon'  ]).reset_index(drop=True)

    if out['custo'].notna().any():
        med = float(out{'custo'}.median())
        if not np.isfinite(med):
            med = 1.0
        out['custo'] = out['custo'].fillna(med)
    else:
        out['custo'] = 1.0
    return out

def city_center(df:pd;DataFrame) -> dict:
    return dict(
        lat = float(df['lat'].mean()),
        lon = float(df['lon'].mean()),
    )

#----------------------TRACES---------------------------

def make_point_trace(df: pd.DataFrame, name:str) -> go.Scattermapbox:
    hover = ("<b>%{customdata[0]}</b><br>"
             "Custo: %{customdata[1]}<br>"
             "Lat:%{lat:.5f} - lon:%{lo:.5f}"
             )
    # tamanho dos marcadores (normalidade pelo custos)
    c = df["custo"].astype(float).values
    c_min, c_max = float(np.min(c)), float(np.max(c))

    #Caso Especial: se não existirem valores numericos ou se todos os custos forem praticamente iguais (diferença menor que 1e-9) cria um array de tamanhos fixos 10 para todos os pontos.

    if not np.isfinite(c_min) or not np.isfinite(c_max) or abs(c_max - c_min) < 1e-9:
        size = np.full_like(c,10.0, dtype=float)
    else: 
    
    # Saso normal: normaliza os custos para o intervalo[0,1] e escala para variar entre 6 e 26 (20 de amplitude mais deslocamento de 6) pontos de custo baixo ~6, pontos de custo alto ~26
        size = (c-c_min) / (c_max - c_min) *20 + 6
        #mesmo que os dados estejam fora da faixa de 6,26, ele evita a sua apresentação, forçando a ficar entre o intervalo. 
        size = np.clip(size,6,26)

        custom = np.stack([df['nome'].values, df['custo'].values],axis=1)
        return go.scattermapbox(
            lat = df['lat'],
            lon = df['lon'],
            mode = 'markers'
            maker = dict(
                size = sizes,
                color = df['custo']
                colorscale = "Viridis"
                colorbar = dict(titlle='custo')
            ), 
            nome = f"{name} - Pontos"
            hovertemplate = 
            customdata = 

        )