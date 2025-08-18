import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from io import StringIO
import datetime
from collections import Counter
import math
import re

# lista global para acumular mensagens de carregamento
load_logs = []  

# Configuração da página
st.set_page_config(
    page_title="Dashboard Lotofácil - Bolão dos Feras",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado moderno com paleta Lotofácil
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 75%, #000000 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: transparent;
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2d1b69 0%, #663399 50%, #4a0080 100%);
    }
    
    .css-1lcbmhc {
        background: linear-gradient(180deg, #2d1b69 0%, #663399 50%, #4a0080 100%);
    }
    
    /* Cards modernos */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(102, 51, 153, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102, 51, 153, 0.4);
    }
    
    /* Bolinhas dos números */
    .number-ball {
        background: linear-gradient(135deg, #663399 0%, #9966cc 100%);
        color: white;
        border-radius: 50%;
        width: 45px;
        height: 45px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin: 3px;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(102, 51, 153, 0.4);
        transition: all 0.3s ease;
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .number-ball:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(102, 51, 153, 0.6);
    }
    
    .winning-ball {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4a 100%);
        color: #2d1b69;
        animation: pulse 2s infinite;
        border: 2px solid #fff;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4); }
        50% { transform: scale(1.05); box-shadow: 0 8px 25px rgba(255, 215, 0, 0.6); }
        100% { transform: scale(1); box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4); }
    }
    
    /* Cards de conteúdo */
    .content-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 2rem;
        border-radius: 25px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        color: white;
    }
    
    .game-card {
        background: linear-gradient(135deg, rgba(102, 51, 153, 0.1) 0%, rgba(153, 102, 204, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(102, 51, 153, 0.3);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(102, 51, 153, 0.2);
        border-left: 4px solid #663399;
    }
    
    /* Títulos */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
    }
    
    h1 {
        background: linear-gradient(135deg, #ffd700 0%, #663399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: transparent;
        text-align: center;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    /* Fallback para mobile */
    @media (max-width: 768px) {
        h1 {
            background: none;
            -webkit-background-clip: initial;
            -webkit-text-fill-color: initial;
            background-clip: initial;
            color: #ffffff;
        }
    }

    
    /* Seletores e inputs */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        color: white;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        color: white;
    }
    
    /* Destaques */
    .highlight-number {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4a 100%);
        color: #2d1b69;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        margin: 0 3px;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
    }
    
    /* Estatísticas especiais */
    .stat-item {
        background: linear-gradient(135deg, rgba(102, 51, 153, 0.2) 0%, rgba(153, 102, 204, 0.1) 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 3px solid #ffd700;
        color: white;
        backdrop-filter: blur(5px);
    }
    
    /* Melhorias nos gráficos */
    .js-plotly-plot {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* Texto geral */
    .stMarkdown, .stText, p, span {
        color: white;
    }
    
    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, #663399 0%, #9966cc 100%);
        color: white;
        border-radius: 15px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 51, 153, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 51, 153, 0.4);
    }
    
    /* Container principal */
    .main-container {
        padding: 0 1rem;
    }
    
    /* Animações suaves */
    * {
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Funções de utilidade
def is_prime(n):
    """Verifica se um número é primo"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_fibonacci(n):
    """Verifica se um número é de Fibonacci"""
    fibonacci_numbers = [1, 1, 2, 3, 5, 8, 13, 21]
    return n in fibonacci_numbers

def get_moldura_numbers():
    """Retorna os números da moldura (bordas do cartão)"""
    return [1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25]

def get_centro_numbers():
    """Retorna os números do centro do cartão"""
    return [7, 8, 9, 12, 13, 14, 17, 18, 19]

def extract_sheet_id(url):
    """Extrai o ID da planilha da URL do Google Sheets"""
    try:
        if '/d/' in url:
            sheet_id = url.split('/d/')[1].split('/')[0]
            return sheet_id
        return None
    except:
        return None

@st.cache_data(ttl=300)
def load_google_sheets_data(sheet_url):
    global load_logs
    sheet_id = extract_sheet_id(sheet_url)
    if not sheet_id:
        st.error("URL inválida do Google Sheets")
        return None, None, None, None
    
    try:
        # Mapear as abas baseado nos nomes dos arquivos CSV fornecidos
        sheets_data = {}
        
        # Tentar diferentes GIDs para encontrar as abas
        gids = {
            'resultados': '1617489375',  # Vamos tentar encontrar automaticamente
            'api': '1272948934',  # GID fornecido no código original
            'conj_num_escolhidos': '1096273873',
            'jogos_concursos': '40804589',
            'lf_acompanhamento': '674877581'
        }
        
        # Carregar aba 'resultados' diretamente pelo GID correto
        try:
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1617489375"
            response = requests.get(csv_url, timeout=10)
        
            if response.status_code == 200:
                df = pd.read_csv(StringIO(response.text))
                df.columns = df.columns.str.strip()  # limpar espaços
                if all(f'Bola{i}' in df.columns for i in range(1, 16)):
                    sheets_data['resultados'] = df
                    load_logs.append("✅ Aba 'resultados' carregada com sucesso!")
                else:
                    load_logs.append("⚠️ Estrutura da aba 'resultados' inválida")
            else:
                load_logs.append("⚠️ Não foi possível carregar a aba 'resultados'")
        except Exception as e:
            st.error(f"Erro ao carregar aba 'resultados': {str(e)}")

        
        # Carregar outras abas conhecidas
        for name, gid in gids.items():
            if gid and name != 'resultados':  # Já tentamos a 'resultados'
                try:
                    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
                    response = requests.get(csv_url, timeout=10)
                    
                    if response.status_code == 200:
                        df = pd.read_csv(StringIO(response.text))
                        # Limpar espaços em branco dos nomes das colunas
                        df.columns = df.columns.str.strip()
                        sheets_data[name] = df
                        load_logs.append(f"✅ Aba '{name}' carregada com sucesso!")
                    else:
                        load_logs.append(f"⚠️ Não foi possível carregar a aba '{name}' (GID: {gid})")
                except Exception as e:
                    load_logs.append(f"⚠️ Erro ao carregar aba '{name}': {str(e)}")
        
        # Se não conseguiu carregar dados, usar dados de exemplo
        if not sheets_data:
            load_logs.append("📁 Usando dados de exemplo. Verifique a URL da planilha.")
            return load_sample_data()
        
        return process_sheets_data(sheets_data)
        
    except Exception as e:
        st.error(f"Erro geral ao carregar dados: {str(e)}")
        return load_sample_data()

def process_sheets_data(sheets_data):
    global load_logs
    try:
        # Processar dados dos resultados/API
        if 'api' in sheets_data:
            api_df = sheets_data['api']
            
            # Extrair último resultado
            if len(api_df) > 0:
                ultimo_concurso = None
                winning_numbers = []
                
                for idx, row in api_df.iterrows():
                    if pd.notna(row.get('Concurso', None)) and str(row['Concurso']).isdigit():
                        ultimo_concurso = int(row['Concurso'])
                        numeros = []
                        for i in range(1, 16):
                            col_name = f'Bola{i}'
                            if col_name in row and pd.notna(row[col_name]):
                                try:
                                    numeros.append(int(row[col_name]))
                                except:
                                    pass
                        if len(numeros) == 15:
                            winning_numbers = sorted(numeros)
                            break
        
        if not winning_numbers:
            winning_numbers = [1, 2, 3, 5, 6, 11, 13, 16, 17, 19, 21, 22, 23, 24, 25]
            ultimo_concurso = 3471
        
        # Processar dados históricos
        if 'resultados' in sheets_data:
            df_res = sheets_data['resultados'].copy()
            df_res.columns = df_res.columns.str.strip()
            df_res['NUMEROS'] = df_res[[f'Bola{i}' for i in range(1, 15+1)]].values.tolist()
            
            if 'Concurso' in df_res.columns:
                df_res.rename(columns={'Concurso': 'CONCURSO'}, inplace=True)
            elif 'concurso' in df_res.columns:
                df_res.rename(columns={'concurso': 'CONCURSO'}, inplace=True)

            if 'Data' in df_res.columns:
                df_res.rename(columns={'Data': 'DATA'}, inplace=True)
            elif 'DATA' not in df_res.columns:
                df_res['DATA'] = None
                
            historical_df = df_res[['CONCURSO','DATA','NUMEROS']].copy()
            historical_df = historical_df.sort_values('CONCURSO', ascending=False).reset_index(drop=True)
        else:
            historical_df = create_sample_historical_data()
                    
        # Processar jogos da aba lf_acompanhamento
        if 'lf_acompanhamento' in sheets_data:
            df_jogos = sheets_data['lf_acompanhamento'].copy()
            jogos_area = df_jogos.iloc[10:80, 2:17]
            
            jogos = []
            for i, row in enumerate(jogos_area.values.tolist(), start=1):
                numeros = []
                for x in row:
                    try:
                        if pd.notna(x):
                            numeros.append(int(float(str(x).strip())))
                    except:
                        continue
                jogos.append({
                    'CONCURSO': ultimo_concurso,
                    'JOGO': i,
                    'NUMEROS': numeros,
                    'ACERTOS': sum(n in winning_numbers for n in numeros)
                })
            
            games_df = pd.DataFrame(jogos)
        else:
            load_logs.append("⚠️ Aba 'lf_acompanhamento' não encontrada. Usando jogos de exemplo.")
            games_df = create_games_from_csv_data()
        
        # Conjunto de 18 dezenas
        conjunto_18 = []
        if 'conj_num_escolhidos' in sheets_data:
            df_conj = sheets_data['conj_num_escolhidos']
            ultima_linha = df_conj.dropna(how='all').iloc[-1]
            conjunto_18 = [int(v) for v in ultima_linha.values[1:] if pd.notna(v) and str(v).isdigit()]
        else:
            load_logs.append("⚠️ Aba 'conj_num_escolhidos' não encontrada. Usando conjunto padrão.")
            conjunto_18 = [1, 2, 4, 6, 7, 11, 12, 13, 14, 15, 17, 19, 20, 21, 22, 23, 24, 25]

        # Processar jogos da aba jogos/concursos (para Histórico & Relatórios)
        if 'jogos_concursos' in sheets_data:
            df_jogos_concursos = sheets_data['jogos_concursos'].copy()
            df_jogos_concursos.columns = df_jogos_concursos.columns.str.strip().str.upper()
            
            if 'CONCURSO' not in df_jogos_concursos.columns:
                for col in df_jogos_concursos.columns:
                    if "CONCURSO" in col.upper():
                        df_jogos_concursos.rename(columns={col: "CONCURSO"}, inplace=True)
                        break
            
            jogos_concursos = []
            for idx, row in df_jogos_concursos.iterrows():
                numeros = []
                for col, x in row.items():
                    if col in ["CONCURSO", "ACERTOS"]:
                        continue
                    try:
                        if pd.notna(x) and str(x).isdigit():
                            numeros.append(int(x))
                    except:
                        continue

                if numeros:
                    # usa valor da planilha se existir
                    acertos_val = None
                    if "ACERTOS" in df_jogos_concursos.columns and pd.notna(row.get("ACERTOS", None)):
                        try:
                            acertos_val = int(row["ACERTOS"])
                        except:
                            acertos_val = None

                    if acertos_val is None:
                        acertos_val = sum(n in winning_numbers for n in numeros)

                    jogos_concursos.append({
                        'CONCURSO': int(row["CONCURSO"]) if "CONCURSO" in row and pd.notna(row["CONCURSO"]) else ultimo_concurso,
                        'JOGO': idx + 1,
                        'NUMEROS': numeros,
                        'ACERTOS': acertos_val
                    })
            
            jogos_concursos_df = pd.DataFrame(jogos_concursos)
        else:
            jogos_concursos_df = pd.DataFrame()
         
        return {
            'ultimo_concurso': ultimo_concurso,
            'winning_numbers': winning_numbers,
            'games_df': games_df,
            'games_concursos_df': jogos_concursos_df,
            'historical_df': historical_df,
            'conjunto_18': conjunto_18
        }
        
    except Exception as e:
        st.error(f"Erro ao processar dados: {str(e)}")
        return load_sample_data()


def load_sample_data():
    """Carrega dados de exemplo baseados nos CSVs fornecidos"""
    try:
        # Dados do último sorteio (baseado no CSV API)
        ultimo_concurso = 3471
        winning_numbers = [1, 2, 3, 5, 6, 11, 13, 16, 17, 19, 21, 22, 23, 24, 25]
        
        # Jogos baseados no CSV jogos_concursos
        games_df = create_games_from_csv_data()
        
        # Dados históricos
        historical_df = create_sample_historical_data()
        
        # Conjunto de 18 dezenas
        conjunto_18 = [1, 2, 4, 6, 7, 11, 12, 13, 14, 15, 17, 19, 20, 21, 22, 23, 24, 25]
        
        return {
            'ultimo_concurso': ultimo_concurso,
            'winning_numbers': winning_numbers,
            'games_df': games_df,
            'historical_df': historical_df,
            'conjunto_18': conjunto_18
        }
    except Exception as e:
        st.error(f"Erro ao carregar dados de exemplo: {str(e)}")
        return None

def create_games_from_csv_data():
    """Cria DataFrame dos jogos baseado no CSV jogos_concursos"""
    # Dados do concurso 3470
    jogos_3470 = [
        {'CONCURSO': 3470, 'JOGO': 1, 'NUMEROS': [1,2,4,7,11,12,13,14,15,17,20,21,22,23,24], 'ACERTOS': 11},
        {'CONCURSO': 3470, 'JOGO': 2, 'NUMEROS': [1,2,6,7,11,12,14,15,17,19,20,21,22,23,25], 'ACERTOS': 8},
        {'CONCURSO': 3470, 'JOGO': 3, 'NUMEROS': [1,2,4,6,7,12,13,14,19,20,21,22,23,24,25], 'ACERTOS': 11},
        {'CONCURSO': 3470, 'JOGO': 4, 'NUMEROS': [1,2,4,6,11,12,13,14,15,17,19,20,21,24,25], 'ACERTOS': 8},
        {'CONCURSO': 3470, 'JOGO': 5, 'NUMEROS': [1,4,6,7,11,13,14,15,17,19,21,22,23,24,25], 'ACERTOS': 9},
        {'CONCURSO': 3470, 'JOGO': 6, 'NUMEROS': [2,4,6,7,11,12,13,15,17,19,20,22,23,24,25], 'ACERTOS': 8},
    ]
    
    # Dados do concurso 3471 
    jogos_3471 = [
        {'CONCURSO': 3471, 'JOGO': 1, 'NUMEROS': [1,3,4,6,7,9,11,12,14,15,17,18,20,22,25], 'ACERTOS': 7},
        {'CONCURSO': 3471, 'JOGO': 2, 'NUMEROS': [1,2,3,4,7,9,12,13,15,17,18,19,20,22,25], 'ACERTOS': 8},
        {'CONCURSO': 3471, 'JOGO': 3, 'NUMEROS': [1,2,4,6,7,11,12,13,14,17,18,19,20,22,25], 'ACERTOS': 9},
        {'CONCURSO': 3471, 'JOGO': 4, 'NUMEROS': [1,2,3,4,6,7,9,11,12,13,14,15,19,20,25], 'ACERTOS': 8},
        {'CONCURSO': 3471, 'JOGO': 5, 'NUMEROS': [1,2,3,4,6,9,11,12,13,14,15,17,18,19,22], 'ACERTOS': 9},
        {'CONCURSO': 3471, 'JOGO': 6, 'NUMEROS': [2,3,6,7,9,11,13,14,15,17,18,19,20,22,25], 'ACERTOS': 9},
    ]
    
    # Recalcular acertos baseado no resultado do concurso 3471
    winning_3471 = [1, 2, 3, 5, 6, 11, 13, 16, 17, 19, 21, 22, 23, 24, 25]
    
    for jogo in jogos_3471:
        acertos = len([n for n in jogo['NUMEROS'] if n in winning_3471])
        jogo['ACERTOS'] = acertos
    
    # Combinar todos os jogos
    all_games = jogos_3470 + jogos_3471
    
    return pd.DataFrame(all_games)

def create_sample_historical_data():
    """Cria dados históricos baseados no CSV resultados"""
    historical_data = [
        {'CONCURSO': 3471, 'DATA': '16/08/2025', 'NUMEROS': [1, 2, 3, 5, 6, 11, 13, 16, 17, 19, 21, 22, 23, 24, 25]},
        {'CONCURSO': 13, 'DATA': '22/12/2003', 'NUMEROS': [3, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19, 23]},
        {'CONCURSO': 12, 'DATA': '15/12/2003', 'NUMEROS': [1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 14, 16, 17, 24, 25]},
        {'CONCURSO': 11, 'DATA': '08/12/2003', 'NUMEROS': [2, 6, 7, 8, 9, 10, 11, 12, 16, 19, 20, 22, 23, 24, 25]},
        {'CONCURSO': 10, 'DATA': '01/12/2003', 'NUMEROS': [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 14, 19, 20, 23, 24]},
        {'CONCURSO': 9, 'DATA': '24/11/2003', 'NUMEROS': [3, 4, 5, 9, 10, 11, 13, 15, 16, 17, 19, 20, 21, 24, 25]},
        {'CONCURSO': 8, 'DATA': '17/11/2003', 'NUMEROS': [1, 5, 6, 8, 9, 10, 13, 15, 16, 17, 18, 19, 20, 22, 25]},
        {'CONCURSO': 7, 'DATA': '10/11/2003', 'NUMEROS': [1, 4, 7, 8, 10, 12, 14, 15, 16, 18, 19, 21, 22, 23, 25]},
        {'CONCURSO': 6, 'DATA': '03/11/2003', 'NUMEROS': [1, 2, 4, 5, 6, 7, 10, 12, 15, 16, 17, 19, 21, 23, 25]},
        {'CONCURSO': 5, 'DATA': '27/10/2003', 'NUMEROS': [1, 2, 4, 8, 9, 11, 12, 13, 15, 16, 19, 20, 23, 24, 25]},
    ]
    return pd.DataFrame(historical_data)

def display_numbers_as_balls(numbers, winning_numbers=None, title=""):
    """Exibe números como bolinhas modernas da lotofácil"""
    html = f'<div style="margin: 20px 0;"><h4 style="color: #ffd700; margin-bottom: 15px;">{title}</h4>'
    html += '<div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 15px; backdrop-filter: blur(10px);">'
    
    for num in sorted(numbers):
        if winning_numbers and num in winning_numbers:
            html += f'<div class="number-ball winning-ball">{num:02d}</div>'
        else:
            html += f'<div class="number-ball">{num:02d}</div>'
    
    html += '</div></div>'
    return html

def calculate_advanced_stats(games_df, winning_numbers):
    """Calcula estatísticas avançadas dos jogos"""
    stats = {}
    
    # Análise dos jogos
    total_games = len(games_df)
    all_numbers = []
    
    for _, game in games_df.iterrows():
        all_numbers.extend(game['NUMEROS'])
    
    # Estatísticas dos números jogados
    stats['pares'] = len([n for n in all_numbers if n % 2 == 0])
    stats['impares'] = len([n for n in all_numbers if n % 2 != 0])
    stats['primos'] = len([n for n in all_numbers if is_prime(n)])
    stats['fibonacci'] = len([n for n in all_numbers if is_fibonacci(n)])
    stats['moldura'] = len([n for n in all_numbers if n in get_moldura_numbers()])
    stats['centro'] = len([n for n in all_numbers if n in get_centro_numbers()])
    stats['soma_total'] = sum(all_numbers)
    stats['media'] = stats['soma_total'] / len(all_numbers) if all_numbers else 0
    
    # Estatísticas do último sorteio
    if winning_numbers:
        stats['pares_sorteio'] = len([n for n in winning_numbers if n % 2 == 0])
        stats['impares_sorteio'] = len([n for n in winning_numbers if n % 2 != 0])
        stats['primos_sorteio'] = len([n for n in winning_numbers if is_prime(n)])
        stats['fibonacci_sorteio'] = len([n for n in winning_numbers if is_fibonacci(n)])
        stats['moldura_sorteio'] = len([n for n in winning_numbers if n in get_moldura_numbers()])
        stats['centro_sorteio'] = len([n for n in winning_numbers if n in get_centro_numbers()])
        stats['soma_sorteio'] = sum(winning_numbers)
    
    return stats

def calculate_historical_stats(historical_df):
    """Calcula estatísticas dos sorteios históricos"""
    stats = {}
    all_historical_numbers = []
    
    for _, row in historical_df.iterrows():
        all_historical_numbers.extend(row['NUMEROS'])
    
    # Frequência geral dos últimos sorteios
    frequency = Counter(all_historical_numbers)
    
    # Estatísticas por concurso
    concurso_stats = []
    for _, row in historical_df.iterrows():
        numeros = row['NUMEROS']
        concurso_stat = {
            'CONCURSO': row['CONCURSO'],
            'PARES': len([n for n in numeros if n % 2 == 0]),
            'IMPARES': len([n for n in numeros if n % 2 != 0]),
            'PRIMOS': len([n for n in numeros if is_prime(n)]),
            'FIBONACCI': len([n for n in numeros if is_fibonacci(n)]),
            'MOLDURA': len([n for n in numeros if n in get_moldura_numbers()]),
            'CENTRO': len([n for n in numeros if n in get_centro_numbers()]),
            'SOMA': sum(numeros),
            'MENOR': min(numeros),
            'MAIOR': max(numeros),
            'AMPLITUDE': max(numeros) - min(numeros),
            'NUMEROS': numeros
        }
        concurso_stats.append(concurso_stat)
    
    stats['concursos'] = pd.DataFrame(concurso_stats)
    stats['frequency'] = frequency
    
    # Estatísticas gerais
    stats['pares_total'] = sum([c['PARES'] for c in concurso_stats])
    stats['impares_total'] = sum([c['IMPARES'] for c in concurso_stats])
    stats['soma_media'] = np.mean([c['SOMA'] for c in concurso_stats])
    stats['amplitude_media'] = np.mean([c['AMPLITUDE'] for c in concurso_stats])
    
    return stats

def create_modern_chart(data, chart_type, title, color_scheme=None):
    """Cria gráficos com estilo moderno"""
    if color_scheme is None:
        color_scheme = ['#663399', '#9966cc', '#ffd700', '#cc99ff', '#b366d9']
    
    if chart_type == 'bar':
        fig = px.bar(data, color_discrete_sequence=color_scheme, title=title)
    elif chart_type == 'pie':
        fig = px.pie(data, color_discrete_sequence=color_scheme, title=title)
    elif chart_type == 'line':
        fig = px.line(data, color_discrete_sequence=color_scheme, title=title)
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Inter'),
        title_font=dict(size=20, color='white'),
        legend=dict(font=dict(color='white')),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white')
    )
    
    return fig

def main():
    # Lista para armazenar logs de carregamento
    global load_logs
    load_logs = []
    
    # Cabeçalho moderno
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0; margin-bottom: 2rem;">
        <h1>🎯 DASHBOARD LOTOFÁCIL</h1>
        <p style="color: #9966cc; font-size: 1.6rem; font-weight: 500;">BOLÃO DOS FERAS</p>
        <div style="width: 100px; height: 4px; background: linear-gradient(90deg, #ffd700, #663399); margin: 20px auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar moderna
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 1rem; margin-bottom: 2rem;">
            <h2 style="color: white; margin-bottom: 0.5rem;">⚙️ CONFIGURAÇÕES</h2>
            <div style="width: 50px; height: 2px; background: #ffd700; margin: 10px auto;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        sheet_url = st.text_input(
            "🔗 URL do Google Sheets:",
            value="https://docs.google.com/spreadsheets/d/1tJynBjtlHAEiytXug9HdbRS8rKsKYxopqQSjFXNE9Y0/edit?gid=674877581#gid=674877581",
            help="Cole aqui a URL da sua planilha do Google Sheets"
        )
        
        if st.button("🔄 Atualizar Dados"):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Filtros modernos
        st.markdown("### 📊 NAVEGAÇÃO")
        view_mode = st.selectbox(
            "Selecione a visualização:",
            ["🏠 Dashboard Principal", "📈 Estatísticas dos Sorteios", "📋 Histórico & Relatórios"]
        )
        
        # Status de conexão
        st.markdown("---")
        st.markdown("### 📡 STATUS DA CONEXÃO")
        if sheet_url and extract_sheet_id(sheet_url):
            load_logs.append("✅ Planilha conectada")
        else:
            load_logs.append("⚠️ URL inválida")
    
    # Carregamento de dados com indicador de progresso
    with st.spinner("🔄 Carregando dados da planilha..."):
        data = load_google_sheets_data(sheet_url) if sheet_url else load_sample_data()
    
    if data is None:
        st.error("❌ Erro ao carregar dados. Verifique a URL da planilha.")
        return
    
    # Extrair dados
    ultimo_concurso = data['ultimo_concurso']
    winning_numbers = data['winning_numbers']
    games_df = data['games_df']
    historical_df = data['historical_df']
    conjunto_18 = data['conjunto_18']
    
    # Filtrar jogos por concurso se necessário
    if view_mode == "🏠 Dashboard Principal":
        # Usar dados do último concurso
        current_games = games_df[games_df['CONCURSO'] == ultimo_concurso].copy()
        if len(current_games) == 0:
            current_games = games_df.tail(6).copy()  # Pegar últimos 6 jogos
    else:
        current_games = games_df.copy()
    
    if view_mode == "🏠 Dashboard Principal":
        # Métricas principais com design 
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎮 JOGOS REALIZADOS</h3>
                <h1 style="font-size: 2.5rem; margin: 0.5rem 0; color: #ffffff; text-shadow: 1px 1px 4px rgba(0,0,0,0.5);">{len(current_games)}</h1>
                <p style="opacity: 0.8;">Total de apostas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_acertos = current_games['ACERTOS'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎯 ACERTOS TOTAIS</h3>
                <h1 style="font-size: 2.5rem; margin: 0.5rem 0; color: #ffffff; text-shadow: 1px 1px 4px rgba(0,0,0,0.5);">{total_acertos}</h1>
                <p style="opacity: 0.8;">Números acertados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            media_acertos = current_games['ACERTOS'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊 MÉDIA DE ACERTOS</h3>
                <h1 style="font-size: 2.5rem; margin: 0.5rem 0; color: #ffffff; text-shadow: 1px 1px 4px rgba(0,0,0,0.5);">{media_acertos:.1f}</h1>
                <p style="opacity: 0.8;">Por jogo</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            max_acertos = current_games['ACERTOS'].max()
            st.markdown(f"""
            <div class="metric-card">
                <h3>🏆 MELHOR RESULTADO</h3>
                <h1 style="font-size: 2.5rem; margin: 0.5rem 0; color: #ffffff; text-shadow: 1px 1px 4px rgba(0,0,0,0.5);">{max_acertos}</h1>
                <p style="opacity: 0.8;">Máximo de acertos</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Último sorteio destacado
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(f"### 🎲 ÚLTIMO SORTEIO - CONCURSO {ultimo_concurso}")
        st.markdown(display_numbers_as_balls(winning_numbers, title="Números Sorteados"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Análise detalhada dos jogos
        st.markdown("---")
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🎮 ANÁLISE DETALHADA DOS JOGOS")
        
        for _, game in current_games.iterrows():
            with st.expander(f"🎯 Jogo #{game['JOGO']} - {game['ACERTOS']} acertos", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown("**🎲 Números jogados:**")
                    st.markdown(display_numbers_as_balls(game['NUMEROS'], winning_numbers), unsafe_allow_html=True)
                    
                    # Análise do jogo
                    acertos = [n for n in game['NUMEROS'] if n in winning_numbers]
                    
                    if acertos:
                        st.markdown(f"**✅ Números acertados ({len(acertos)}):**")
                        acertos_html = ' '.join([f'<span class="highlight-number">{n:02d}</span>' for n in acertos])
                        st.markdown(acertos_html, unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="metric-card" style="margin: 0;">', unsafe_allow_html=True)
                    st.metric("Acertos", game['ACERTOS'])
                    st.metric("Taxa", f"{(game['ACERTOS']/15)*100:.1f}%")
                    
                    # Estatísticas do jogo
                    pares = len([n for n in game['NUMEROS'] if n % 2 == 0])
                    impares = len([n for n in game['NUMEROS'] if n % 2 != 0])
                    primos = len([n for n in game['NUMEROS'] if is_prime(n)])
                    fibonacci = len([n for n in game['NUMEROS'] if is_fibonacci(n)])
                    st.metric("Pares", pares)
                    st.metric("Ímpares", impares)
                    st.metric("Primos", primos)
                    st.metric("Fibonacci", fibonacci)
                    st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Conjunto de 18 dezenas
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🔢 CONJUNTO DAS 18 DEZENAS (DESDOBRAMENTO)")
        st.markdown(display_numbers_as_balls(conjunto_18, winning_numbers, "Suas dezenas escolhidas"), unsafe_allow_html=True)
        
        # Análise rápida do conjunto
        acertos_conjunto = len([n for n in conjunto_18 if n in winning_numbers])
        st.markdown(f"""
        <div class="stat-item">
            <h4>📈 Análise do Conjunto</h4>
            <p><strong>Acertos no último sorteio:</strong> {acertos_conjunto} de 18 números</p>
            <p><strong>Taxa de acerto:</strong> {(acertos_conjunto/18)*100:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Gráficos lado a lado
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de acertos por jogo
            fig_acertos = px.bar(
                current_games,
                x='JOGO',
                y='ACERTOS',
                title='🎯 Acertos por Jogo',
                color='ACERTOS',
                color_continuous_scale=['#663399', '#9966cc', '#ffd700']
            )
            fig_acertos.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Inter'),
                title_font=dict(color='white')
            )
            st.plotly_chart(fig_acertos, use_container_width=True)
        
        with col2:
            # Distribuição de acertos
            acertos_dist = current_games['ACERTOS'].value_counts().sort_index()
            fig_dist = px.pie(
                values=acertos_dist.values,
                names=acertos_dist.index,
                title='📊 Distribuição de Acertos',
                color_discrete_sequence=['#663399', '#9966cc', '#ffd700', '#cc99ff', '#b366d9']
            )
            fig_dist.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Inter'),
                title_font=dict(color='white')
            )
            st.plotly_chart(fig_dist, use_container_width=True)
    
    elif view_mode == "📈 Estatísticas dos Sorteios":
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("## 📈 ESTATÍSTICAS DOS SORTEIOS HISTÓRICOS")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Estatísticas históricas
        historical_stats = calculate_historical_stats(historical_df)
        
        # Métricas dos últimos sorteios
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊 MÉDIA SOMA</h3>
                <h2>{historical_stats['soma_media']:.0f}</h2>
                <p>nos últimos sorteios</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📐 AMPLITUDE MÉDIA</h3>
                <h2>{historical_stats['amplitude_media']:.0f}</h2>
                <p>diferença maior-menor</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎲 PARES TOTAL</h3>
                <h2>{historical_stats['pares_total']}</h2>
                <p>nos últimos sorteios</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎯 ÍMPARES TOTAL</h3>
                <h2>{historical_stats['impares_total']}</h2>
                <p>nos últimos sorteios</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Frequência dos números
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🔢 FREQUÊNCIA DOS NÚMEROS NOS ÚLTIMOS SORTEIOS")
        
        # Criar DataFrame para frequência
        freq_data = pd.DataFrame.from_dict(historical_stats['frequency'], orient='index', columns=['Frequencia'])
        freq_data = freq_data.reset_index().rename(columns={'index': 'Numero'})
        freq_data = freq_data.sort_values('Numero')
        
        # Gráfico de frequência
        fig_freq = px.bar(
            freq_data,
            x='Numero',
            y='Frequencia',
            title='Frequência de Cada Número',
            color='Frequencia',
            color_continuous_scale=['#663399', '#9966cc', '#ffd700']
        )
        fig_freq.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Inter'),
            title_font=dict(color='white')
        )
        st.plotly_chart(fig_freq, use_container_width=True)
        
        # Top números mais e menos sorteados
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔥 NÚMEROS MAIS SORTEADOS")
            top_numeros = freq_data.nlargest(5, 'Frequencia')
            for _, row in top_numeros.iterrows():
                st.markdown(f"""
                <div class="stat-item">
                    <span class="highlight-number">{int(row['Numero']):02d}</span> 
                    <strong>{int(row['Frequencia'])} vezes</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### ❄️ NÚMEROS MENOS SORTEADOS")
            bottom_numeros = freq_data.nsmallest(5, 'Frequencia')
            for _, row in bottom_numeros.iterrows():
                st.markdown(f"""
                <div class="stat-item">
                    <span class="highlight-number">{int(row['Numero']):02d}</span> 
                    <strong>{int(row['Frequencia'])} vezes</strong>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Estatísticas por concurso
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 📊 ANÁLISE DETALHADA POR CONCURSO")
        
        # Mostrar tabela dos últimos concursos
        concursos_display = historical_stats['concursos'].copy()
        st.dataframe(
            concursos_display[['CONCURSO', 'PARES', 'IMPARES', 'PRIMOS', 'FIBONACCI', 'MOLDURA', 'CENTRO', 'SOMA', 'AMPLITUDE']],
            use_container_width=True,
            height=400
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Gráficos de tendências
        col1, col2 = st.columns(2)
        
        with col1:
            # Evolução da soma
            fig_soma = px.line(
                concursos_display,
                x='CONCURSO',
                y='SOMA',
                title='Evolução da Soma por Concurso',
                markers=True,
                color_discrete_sequence=['#ffd700']
            )
            fig_soma.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                title_font=dict(color='white')
            )
            st.plotly_chart(fig_soma, use_container_width=True)
        
        with col2:
            # Comparação Pares vs Ímpares
            fig_par_impar = px.bar(
                concursos_display,
                x='CONCURSO',
                y=['PARES', 'IMPARES'],
                title='Pares vs Ímpares por Concurso',
                color_discrete_sequence=['#663399', '#ffd700']
            )
            fig_par_impar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                title_font=dict(color='white')
            )
            st.plotly_chart(fig_par_impar, use_container_width=True)
    
    elif view_mode == "📋 Histórico & Relatórios":
        games_df = data.get('games_concursos_df', data['games_df'])
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("## 📋 HISTÓRICO DE RESULTADOS E RELATÓRIOS")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Resumo executivo
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            jogos_11_mais = len(games_df[games_df['ACERTOS'] >= 11])
            st.markdown(f"""
            <div class="metric-card">
                <h3>🏆 11+ ACERTOS</h3>
                <h2>{jogos_11_mais}</h2>
                <p>jogos premiados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            jogos_8_10 = len(games_df[(games_df['ACERTOS'] >= 8) & (games_df['ACERTOS'] <= 10)])
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎯 8-10 ACERTOS</h3>
                <h2>{jogos_8_10}</h2>
                <p>jogos regulares</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            jogos_baixo = len(games_df[games_df['ACERTOS'] < 8])
            st.markdown(f"""
            <div class="metric-card">
                <h3>⭐ <8 ACERTOS</h3>
                <h2>{jogos_baixo}</h2>
                <p>jogos baixos</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            taxa_sucesso = (jogos_11_mais / len(games_df)) * 100 if len(games_df) > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <h3>📈 TAXA SUCESSO</h3>
                <h2>{taxa_sucesso:.1f}%</h2>
                <p>jogos 11+</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Seletor de concurso
        st.markdown("### 📊 FILTRAR POR CONCURSO")
        concursos_disponiveis = sorted(games_df['CONCURSO'].unique(), reverse=True)
        concurso_selecionado = st.selectbox(
            "Selecione o concurso:",
            options=['Todos'] + concursos_disponiveis,
            index=0
        )
        
        # Filtrar dados
        if concurso_selecionado != 'Todos':
            games_display = games_df[games_df['CONCURSO'] == concurso_selecionado].copy()
            titulo_tabela = f"JOGOS DO CONCURSO {concurso_selecionado}"
        else:
            games_display = games_df.copy()
            titulo_tabela = "TODOS OS JOGOS"
        
        # Tabela detalhada
        st.markdown(f"### 📊 {titulo_tabela}")
        
        # Preparar dados para exibição
        games_display['NUMEROS_STR'] = games_display['NUMEROS'].apply(
            lambda x: ' - '.join([f"{n:02d}" for n in sorted(x)])
        )
        games_display['TAXA_ACERTO'] = (games_display['ACERTOS'] / 15 * 100).round(1)
        
        # Status baseado nos acertos
        def get_status(acertos):
            if acertos >= 11:
                return "🏆 Premiado"
            elif acertos >= 8:
                return "🎯 Regular"
            else:
                return "⭐ Baixo"
        
        games_display['STATUS'] = games_display['ACERTOS'].apply(get_status)
        
        st.dataframe(
            games_display[['CONCURSO', 'JOGO', 'NUMEROS_STR', 'ACERTOS', 'TAXA_ACERTO', 'STATUS']].rename(columns={
                'CONCURSO': '🎲 Concurso',
                'JOGO': '🎮 Jogo',
                'NUMEROS_STR': '🔢 Números',
                'ACERTOS': '🎯 Acertos',
                'TAXA_ACERTO': '📊 Taxa (%)',
                'STATUS': '🏆 Status'
            }),
            use_container_width=True,
            height=400
        )
        
        # Análise temporal
        st.markdown("---")
        st.markdown("### 📈 EVOLUÇÃO DOS RESULTADOS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de linha dos acertos por concurso
            if len(games_df['CONCURSO'].unique()) > 1:
                acertos_por_concurso = games_df.groupby('CONCURSO')['ACERTOS'].mean().reset_index()
                fig_evolucao = px.line(
                    acertos_por_concurso,
                    x='CONCURSO',
                    y='ACERTOS',
                    title='Média de Acertos por Concurso',
                    markers=True,
                    color_discrete_sequence=['#ffd700']
                )
                fig_evolucao.add_hline(y=games_df['ACERTOS'].mean(), line_dash="dash", 
                                      line_color="#663399", annotation_text="Média Geral")
                fig_evolucao.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    title_font=dict(color='white')
                )
                st.plotly_chart(fig_evolucao, use_container_width=True)
            else:
                st.info("📊 Dados de apenas um concurso disponível")
        
        with col2:
            # Distribuição por faixas de acerto
            faixas = ['0-7', '8-10', '11-15']
            valores = [
                len(games_df[games_df['ACERTOS'] <= 7]),
                len(games_df[(games_df['ACERTOS'] >= 8) & (games_df['ACERTOS'] <= 10)]),
                len(games_df[games_df['ACERTOS'] >= 11])
            ]
            
            fig_faixas = px.bar(
                x=faixas,
                y=valores,
                title='Distribuição por Faixas de Acerto',
                color=valores,
                color_continuous_scale=['#663399', '#9966cc', '#ffd700']
            )
            fig_faixas.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                title_font=dict(color='white')
            )
            st.plotly_chart(fig_faixas, use_container_width=True)
        
        # Relatório de insights
        st.markdown("---")
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.markdown("### 🧠 INSIGHTS E RECOMENDAÇÕES")
        
        insights = []
        
        # Análise da estratégia atual
        melhor_jogo = games_df.loc[games_df['ACERTOS'].idxmax()]
        insights.append(f"🏆 **Melhor jogo:** Concurso {melhor_jogo['CONCURSO']} - Jogo #{melhor_jogo['JOGO']} com {melhor_jogo['ACERTOS']} acertos")
        
        # Análise de números mais/menos jogados
        all_numbers = []
        for _, game in games_df.iterrows():
            all_numbers.extend(game['NUMEROS'])
        frequency = Counter(all_numbers)
        mais_jogado = max(frequency, key=frequency.get)
        menos_jogado = min(frequency, key=frequency.get)
        insights.append(f"🔥 **Número mais jogado:** {mais_jogado:02d} ({frequency[mais_jogado]} vezes)")
        insights.append(f"❄️ **Número menos jogado:** {menos_jogado:02d} ({frequency[menos_jogado]} vezes)")
        
        # Taxa de sucesso
        taxa_11_mais = (len(games_df[games_df['ACERTOS'] >= 11]) / len(games_df)) * 100
        insights.append(f"📊 **Taxa de jogos premiados (11+):** {taxa_11_mais:.1f}%")
        
        # Análise por concurso
        if len(games_df['CONCURSO'].unique()) > 1:
            melhor_concurso = games_df.groupby('CONCURSO')['ACERTOS'].mean().idxmax()
            insights.append(f"🎯 **Melhor concurso:** {melhor_concurso} (maior média de acertos)")
        
        # Comparação com estatísticas dos sorteios
        stats = calculate_advanced_stats(games_df, winning_numbers)
        insights.append(f"⚖️ **Último sorteio:** {stats.get('pares_sorteio', 0)} pares e {stats.get('impares_sorteio', 0)} ímpares")
        insights.append(f"🔢 **Seus jogos tendem a:** {stats['pares']/len(all_numbers)*100:.1f}% pares")
        
        for insight in insights:
            st.markdown(f"<div class='stat-item'>{insight}</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Estatísticas comparativas
        st.markdown("---")
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 📊 ESTATÍSTICAS COMPARATIVAS")
        
        stats = calculate_advanced_stats(games_df, winning_numbers)
        
        # Comparação entre jogos e último sorteio
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎮 Estatísticas dos Seus Jogos")
            st.markdown(f"""
            <div class="stat-item">📊 <strong>Pares:</strong> {stats['pares']} | <strong>Ímpares:</strong> {stats['impares']}</div>
            <div class="stat-item">🔢 <strong>Primos:</strong> {stats['primos']} | <strong>Fibonacci:</strong> {stats['fibonacci']}</div>
            <div class="stat-item">🖼️ <strong>Moldura:</strong> {stats['moldura']} | <strong>Centro:</strong> {stats['centro']}</div>
            <div class="stat-item">➕ <strong>Soma Total:</strong> {stats['soma_total']} | <strong>Média:</strong> {stats['media']:.1f}</div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🎲 Estatísticas do Último Sorteio")
            if 'pares_sorteio' in stats:
                st.markdown(f"""
                <div class="stat-item">📊 <strong>Pares:</strong> {stats['pares_sorteio']} | <strong>Ímpares:</strong> {stats['impares_sorteio']}</div>
                <div class="stat-item">🔢 <strong>Primos:</strong> {stats['primos_sorteio']} | <strong>Fibonacci:</strong> {stats['fibonacci_sorteio']}</div>
                <div class="stat-item">🖼️ <strong>Moldura:</strong> {stats['moldura_sorteio']} | <strong>Centro:</strong> {stats['centro_sorteio']}</div>
                <div class="stat-item">➕ <strong>Soma:</strong> {stats['soma_sorteio']}</div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Rodapé moderno
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(102, 51, 153, 0.1) 0%, rgba(255, 215, 0, 0.1) 100%); border-radius: 20px; margin: 2rem 0;">
        <h3 style="color: #ffd700; margin-bottom: 1rem;">🎯 LOTOFÁCIL DASHBOARD</h3>
        <p style="color: #9966cc; margin-bottom: 0.5rem;"> • Streamlit & Plotly  •</p>
        <p style="color: rgba(255,255,255,0.7);">Última atualização: {}</p>
        <div style="width: 100px; height: 2px; background: linear-gradient(90deg, #ffd700, #663399); margin: 15px auto; border-radius: 1px;"></div>
        <p style="color: rgba(255,255,255,0.5); font-size: 0.9rem;">📊 Dados carregados: {} jogos • {} sorteios históricos</p>
    </div>
    """.format(
        datetime.datetime.now().strftime("%d/%m/%Y às %H:%M"),
        len(games_df) if games_df is not None else 0,
        len(historical_df) if historical_df is not None else 0
    ), unsafe_allow_html=True)

    # Mostrar logs no final do dashboard
    if load_logs:
        st.markdown("---")
        st.markdown("### 📡 STATUS DO CARREGAMENTO DAS ABAS")
        for msg in load_logs:
            if "✅" in msg:
                st.success(msg)
            elif "⚠️" in msg:
                st.warning(msg)
            elif "❌" in msg or "Erro" in msg:
                st.error(msg)
            else:
                st.info(msg)

if __name__ == "__main__":
    main()
