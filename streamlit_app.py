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
import time

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

def extract_sheet_and_gid_from_url(url):
    """Extrai sheet_id e gid da URL do Google Sheets"""
    try:
        # Extrai o sheet_id
        if '/d/' in url:
            sheet_id = url.split('/d/')[1].split('/')[0]
        else:
            st.error("❌ URL inválida. Use uma URL do Google Sheets.")
            return None, None
            
        # Extrai o gid se presente
        gid = '0'  # valor padrão
        if 'gid=' in url:
            gid = url.split('gid=')[1].split('&')[0].split('#')[0]
        elif '#gid=' in url:
            gid = url.split('#gid=')[1].split('&')[0]
            
        return sheet_id, gid
    except Exception as e:
        st.error(f"❌ Erro ao processar URL: {str(e)}")
        return None, None

@st.cache_data(ttl=60, show_spinner=True)  # Cache mais curto para testes
def load_google_sheets_data(sheet_url):
    """Carrega dados do Google Sheets com melhor tratamento de erros"""
    if not sheet_url or sheet_url.strip() == "":
        st.warning("⚠️ URL do Google Sheets não fornecida")
        return create_sample_data()
    
    try:
        sheet_id, gid = extract_sheet_and_gid_from_url(sheet_url)
        if not sheet_id:
            return create_sample_data()
            
        # Tenta diferentes formatos de URL
        urls_to_try = [
            f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}",
            f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv",
            f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&gid={gid}"
        ]
        
        for i, csv_url in enumerate(urls_to_try):
            try:
                st.info(f"🔄 Tentativa {i+1}: Carregando dados da planilha...")
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                response = requests.get(csv_url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    # Verifica se a resposta não está vazia
                    if len(response.text.strip()) == 0:
                        st.warning(f"⚠️ Resposta vazia da URL {i+1}")
                        continue
                    
                    # Tenta decodificar diferentes encodings
                    try:
                        content = response.content.decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            content = response.content.decode('latin-1')
                        except UnicodeDecodeError:
                            content = response.content.decode('utf-8', errors='ignore')
                    
                    df = pd.read_csv(StringIO(content))
                    
                    # Verifica se o DataFrame não está vazio
                    if df.empty:
                        st.warning(f"⚠️ Planilha vazia na tentativa {i+1}")
                        continue
                    
                    # Verifica se tem as colunas esperadas
                    expected_columns = ['CONCURSO'] + [f'BOLA {j}' for j in range(1, 16)]
                    missing_columns = [col for col in expected_columns if col not in df.columns]
                    
                    if missing_columns:
                        st.warning(f"⚠️ Colunas faltando: {missing_columns}")
                        # Tenta usar as primeiras colunas disponíveis
                        if len(df.columns) >= 16:
                            st.info("🔄 Tentando usar as primeiras 16 colunas...")
                            df.columns = expected_columns[:len(df.columns)]
                    
                    st.success(f"✅ Dados carregados com sucesso! {len(df)} registros encontrados")
                    st.info(f"📊 Colunas encontradas: {list(df.columns)}")
                    
                    # Mostra uma prévia dos dados
                    if len(df) > 0:
                        st.info(f"🎯 Último concurso: {df.iloc[-1]['CONCURSO'] if 'CONCURSO' in df.columns else 'N/A'}")
                    
                    return df
                else:
                    st.warning(f"⚠️ Status HTTP {response.status_code} na tentativa {i+1}")
                    
            except requests.exceptions.Timeout:
                st.error(f"⏱️ Timeout na tentativa {i+1}")
            except requests.exceptions.RequestException as e:
                st.error(f"🌐 Erro de conexão na tentativa {i+1}: {str(e)}")
            except Exception as e:
                st.error(f"❌ Erro inesperado na tentativa {i+1}: {str(e)}")
        
        # Se todas as tentativas falharam
        st.error("❌ Não foi possível carregar os dados de nenhuma URL")
        st.info("📝 Verifique se:")
        st.info("1. A planilha está compartilhada publicamente")
        st.info("2. A URL está correta")
        st.info("3. A planilha não está vazia")
        st.info("4. Você tem conexão com a internet")
        
        return create_sample_data()
        
    except Exception as e:
        st.error(f"❌ Erro geral ao carregar dados: {str(e)}")
        return create_sample_data()

def create_sample_data():
    """Cria dados de exemplo baseados no CSV fornecido"""
    st.info("📋 Usando dados de exemplo")
    data = {
        'CONCURSO': [3470, 3471, 3472],
        'BOLA 1': [1, 2, 3], 'BOLA 2': [4, 5, 6], 'BOLA 3': [5, 7, 8], 'BOLA 4': [7, 9, 10], 'BOLA 5': [8, 11, 12],
        'BOLA 6': [10, 13, 14], 'BOLA 7': [12, 15, 16], 'BOLA 8': [13, 17, 18], 'BOLA 9': [14, 19, 20], 'BOLA 10': [18, 21, 22],
        'BOLA 11': [20, 23, 24], 'BOLA 12': [21, 25, 1], 'BOLA 13': [22, 2, 3], 'BOLA 14': [23, 4, 5], 'BOLA 15': [24, 6, 7]
    }
    return pd.DataFrame(data)

def create_sample_historical_data():
    """Cria dados históricos dos últimos 10 concursos para análise"""
    historical_data = [
        {'CONCURSO': 3470, 'NUMEROS': [1, 4, 5, 7, 8, 10, 12, 13, 14, 18, 20, 21, 22, 23, 24]},
        {'CONCURSO': 3469, 'NUMEROS': [2, 3, 6, 9, 11, 12, 15, 16, 17, 19, 20, 21, 22, 24, 25]},
        {'CONCURSO': 3468, 'NUMEROS': [1, 3, 5, 8, 10, 11, 13, 14, 16, 18, 19, 21, 23, 24, 25]},
        {'CONCURSO': 3467, 'NUMEROS': [2, 4, 6, 7, 9, 12, 13, 15, 17, 18, 20, 21, 22, 23, 25]},
        {'CONCURSO': 3466, 'NUMEROS': [1, 2, 5, 7, 9, 11, 14, 15, 16, 18, 19, 20, 22, 24, 25]},
        {'CONCURSO': 3465, 'NUMEROS': [3, 4, 6, 8, 10, 12, 13, 14, 17, 19, 20, 21, 23, 24, 25]},
        {'CONCURSO': 3464, 'NUMEROS': [1, 2, 4, 7, 8, 11, 13, 15, 16, 18, 19, 21, 22, 24, 25]},
        {'CONCURSO': 3463, 'NUMEROS': [3, 5, 6, 9, 10, 12, 14, 15, 17, 18, 20, 21, 22, 23, 24]},
        {'CONCURSO': 3462, 'NUMEROS': [1, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 20, 23, 24, 25]},
        {'CONCURSO': 3461, 'NUMEROS': [2, 3, 6, 8, 10, 11, 13, 15, 18, 19, 20, 21, 22, 24, 25]}
    ]
    return pd.DataFrame(historical_data)

def create_sample_games():
    """Cria jogos de exemplo"""
    games = [
        {'JOGO': 1, 'NUMEROS': [1,2,4,7,11,12,13,14,15,17,20,21,22,23,24], 'ACERTOS': 11},
        {'JOGO': 2, 'NUMEROS': [1,2,6,7,11,12,14,15,17,19,20,21,22,23,25], 'ACERTOS': 8},
        {'JOGO': 3, 'NUMEROS': [1,2,4,6,7,12,13,14,19,20,21,22,23,24,25], 'ACERTOS': 11},
        {'JOGO': 4, 'NUMEROS': [1,2,4,6,11,12,13,14,15,17,19,20,21,24,25], 'ACERTOS': 8},
        {'JOGO': 5, 'NUMEROS': [1,4,6,7,11,13,14,15,17,19,21,22,23,24,25], 'ACERTOS': 9},
        {'JOGO': 6, 'NUMEROS': [2,4,6,7,11,12,13,15,17,19,20,22,23,24,25], 'ACERTOS': 8},
    ]
    return pd.DataFrame(games)

def get_conjunto_18_dezenas():
    """Retorna o conjunto das 18 dezenas (desdobramento)"""
    return [1, 2, 4, 6, 7, 11, 12, 13, 14, 15, 17, 19, 20, 21, 22, 23, 24, 25]

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

def process_sheet_data(df):
    """Processa os dados da planilha para extrair o último sorteio"""
    try:
        if df is None or df.empty:
            return None
        
        # Pega a última linha (último sorteio)
        last_row = df.iloc[-1]
        
        # Extrai os números das colunas BOLA 1 a BOLA 15
        numbers = []
        for i in range(1, 16):
            col_name = f'BOLA {i}'
            if col_name in df.columns:
                num = last_row[col_name]
                if pd.notna(num):
                    numbers.append(int(num))
        
        concurso = last_row.get('CONCURSO', 'N/A')
        
        return {
            'concurso': concurso,
            'numeros': sorted(numbers)
        }
    except Exception as e:
        st.error(f"❌ Erro ao processar dados da planilha: {str(e)}")
        return None

def main():
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
        
        # Status da conexão
        st.markdown("### 🔗 STATUS DA PLANILHA")
        
        sheet_url = st.text_input(
            "URL do Google Sheets:",
            value="https://docs.google.com/spreadsheets/d/1tJynBjtlHAEiytXug9HdbRS8rKsKYxopqQSjFXNE9Y0/edit?gid=674877581#gid=674877581",
            help="Cole aqui a URL da sua planilha do Google Sheets"
        )
        
        # Botões de controle
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Atualizar", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        with col2:
            if st.button("🧹 Limpar Cache", use_container_width=True):
                st.cache_data.clear()
                st.success("Cache limpo!")
        
        # Configurações de debug
        st.markdown("---")
        debug_mode = st.checkbox("🐛 Modo Debug", help="Mostra informações detalhadas de carregamento")
        auto_refresh = st.selectbox(
            "🔄 Auto-atualização:",
            ["Manual", "30 segundos", "1 minuto", "5 minutos"],
            help="Atualização automática dos dados"
        )
        
        st.markdown("---")
        
        # Filtros modernos
        st.markdown("### 📊 NAVEGAÇÃO")
        view_mode = st.selectbox(
            "Selecione a visualização:",
            ["🏠 Dashboard Principal", "📈 Estatísticas dos Sorteios", "📋 Histórico & Relatórios"]
        )
        
        # Informações da planilha
        st.markdown("---")
        st.markdown("### ℹ️ INFORMAÇÕES")
        st.info("📝 **Dicas para resolver problemas:**")
        st.info("1. Verifique se a planilha está pública")
        st.info("2. Teste a URL no navegador")
        st.info("3. Use 'Limpar Cache' se necessário")
        st.info("4. Ative o 'Modo Debug' para mais detalhes")
    
    # Auto-refresh logic
    if auto_refresh != "Manual":
        refresh_intervals = {
            "30 segundos": 30,
            "1 minuto": 60,
            "5 minutos": 300
        }
        time.sleep(refresh_intervals.get(auto_refresh, 60))
        st.rerun()
    
    # Carregamento de dados com debug
    if debug_mode:
        st.markdown("### 🐛 DEBUG MODE")
        with st.expander("Informações de Debug", expanded=True):
            st.write(f"**URL fornecida:** {sheet_url}")
            if sheet_url:
                sheet_id, gid = extract_sheet_and_gid_from_url(sheet_url)
                st.write(f"**Sheet ID:** {sheet_id}")
                st.write(f"**GID:** {gid}")
                st.write(f"**Timestamp:** {datetime.datetime.now()}")
    
    # Carregamento dos dados
    with st.spinner("🔄 Carregando dados da planilha..."):
        df = load_google_sheets_data(sheet_url) if sheet_url else create_sample_data()
    
    # Processa os dados da planilha
    sheet_data = process_sheet_data(df)
    
    # Define os números do último sorteio
    if sheet_data and sheet_data['numeros']:
        winning_numbers = sheet_data['numeros']
        ultimo_concurso = sheet_data['concurso']
        st.success(f"✅ Dados atualizados! Último concurso: {ultimo_concurso}")
    else:
        winning_numbers = [1, 4, 5, 7, 8, 10, 12, 13, 14, 18, 20, 21, 22, 23, 24]
        ultimo_concurso = 3470
        st.warning("⚠️ Usando dados de exemplo")
    
    # Dados auxiliares
    games_df = create_sample_games()
    historical_df = create_sample_historical_data()
    conjunto_18 = get_conjunto_18_dezenas()
    
    if df is not None:
        if view_mode == "🏠 Dashboard Principal":
            # Métricas principais com design moderno
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🎮 JOGOS REALIZADOS</h3>
                    <h1 style="font-size: 2.5rem; margin: 0.5rem 0; color: #ffffff; text-shadow: 1px 1px 4px rgba(0,0,0,0.5);">{len(games_df)}</h1>
                    <p style="opacity: 0.8;">Total de apostas</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                total_acertos = games_df['ACERTOS'].sum()
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🎯 ACERTOS TOTAIS</h3>
                    <h1 style="font-size: 2.5rem; margin: 0.5rem 0; color: #ffffff; text-shadow: 1px 1px 4px rgba(0,0,0,0.5);">{total_acertos}</h1>
                    <p style="opacity: 0.8;">Números acertados</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                media_acertos = games_df['ACERTOS'].mean()
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📊 MÉDIA DE ACERTOS</h3>
                    <h1 style="font-size: 2.5rem; margin: 0.5rem 0; color: #ffffff; text-shadow: 1px 1px 4px rgba(0,0,0,0.5);">{media_acertos:.1f}</h1>
                    <p style="opacity: 0.8;">Por jogo</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                max_acertos = games_df['ACERTOS'].max()
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
            
            # Mostrar dados brutos se em modo debug
            if debug_mode and sheet_data:
                st.markdown("**Debug - Dados processados:**")
                st.json(sheet_data)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Análise detalhada dos jogos
            st.markdown("---")
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### 🎮 ANÁLISE DETALHADA DOS JOGOS")
            
            for _, game in games_df.iterrows():
                with st.expander(f"🎯 Jogo #{game['JOGO']} - {len([n for n in game['NUMEROS'] if n in winning_numbers])} acertos", expanded=False):
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
                        acertos_reais = len([n for n in game['NUMEROS'] if n in winning_numbers])
                        st.metric("Acertos", acertos_reais)
                        st.metric("Taxa", f"{(acertos_reais/15)*100:.1f}%")
                        
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
                # Gráfico de acertos por jogo (recalculado com dados reais)
                games_display = games_df.copy()
                games_display['ACERTOS_REAIS'] = games_display['NUMEROS'].apply(
                    lambda x: len([n for n in x if n in winning_numbers])
                )
                
                fig_acertos = px.bar(
                    games_display,
                    x='JOGO',
                    y='ACERTOS_REAIS',
                    title='🎯 Acertos por Jogo (Dados Atualizados)',
                    color='ACERTOS_REAIS',
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
                acertos_dist = games_display['ACERTOS_REAIS'].value_counts().sort_index()
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
            
            # Mostrar dados da planilha se disponível
            if not df.empty:
                st.markdown("### 📊 DADOS DA PLANILHA")
                st.dataframe(df.head(10), use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Estatísticas históricas
            historical_stats = calculate_historical_stats(historical_df)
            
            # Métricas dos últimos 10 sorteios
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
                    <p>nos últimos 10 sorteios</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🎯 ÍMPARES TOTAL</h3>
                    <h2>{historical_stats['impares_total']}</h2>
                    <p>nos últimos 10 sorteios</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Frequência dos números
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### 🔢 FREQUÊNCIA DOS NÚMEROS NOS ÚLTIMOS 10 SORTEIOS")
            
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
            st.markdown('</div>', unsafe_allow_html=True)
        
        elif view_mode == "📋 Histórico & Relatórios":
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("## 📋 HISTÓRICO DE RESULTADOS E RELATÓRIOS")
            
            # Mostrar dados brutos da planilha
            if not df.empty:
                st.markdown("### 📈 DADOS BRUTOS DA PLANILHA")
                st.dataframe(df, use_container_width=True, height=300)
                
                # Estatísticas da planilha
                st.markdown("### 📊 ESTATÍSTICAS DA PLANILHA")
                st.write(f"**Total de registros:** {len(df)}")
                st.write(f"**Colunas:** {list(df.columns)}")
                if 'CONCURSO' in df.columns:
                    st.write(f"**Concursos:** {df['CONCURSO'].min()} a {df['CONCURSO'].max()}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Rodapé moderno
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(102, 51, 153, 0.1) 0%, rgba(255, 215, 0, 0.1) 100%); border-radius: 20px; margin: 2rem 0;">
        <h3 style="color: #ffd700; margin-bottom: 1rem;">🎯 LOTOFÁCIL DASHBOARD</h3>
        <p style="color: #9966cc; margin-bottom: 0.5rem;">Desenvolvido com tecnologia avançada • Streamlit & Plotly</p>
        <p style="color: rgba(255,255,255,0.7);">Última atualização: {datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")}</p>
        <div style="width: 100px; height: 2px; background: linear-gradient(90deg, #ffd700, #663399); margin: 15px auto; border-radius: 1px;"></div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
