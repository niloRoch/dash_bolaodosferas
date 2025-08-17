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

@st.cache_data(ttl=300)
def load_google_sheets_data(sheet_url):
    """Carrega dados do Google Sheets"""
    try:
        sheet_id = sheet_url.split('/d/')[1].split('/')[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=674877581"
        
        response = requests.get(csv_url)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            return df
        else:
            st.error(f"Erro ao carregar dados: Status {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro ao conectar com Google Sheets: {str(e)}")
        return create_sample_data()

def create_sample_data():
    """Cria dados de exemplo baseados no CSV fornecido"""
    data = {
        'CONCURSO': [3470],
        'BOLA 1': [1], 'BOLA 2': [4], 'BOLA 3': [5], 'BOLA 4': [7], 'BOLA 5': [8],
        'BOLA 6': [10], 'BOLA 7': [12], 'BOLA 8': [13], 'BOLA 9': [14], 'BOLA 10': [18],
        'BOLA 11': [20], 'BOLA 12': [21], 'BOLA 13': [22], 'BOLA 14': [23], 'BOLA 15': [24]
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
    
    # Carregamento de dados
    df = load_google_sheets_data(sheet_url) if sheet_url else create_sample_data()
    games_df = create_sample_games()
    historical_df = create_sample_historical_data()
    conjunto_18 = get_conjunto_18_dezenas()
    winning_numbers = [1, 4, 5, 7, 8, 10, 12, 13, 14, 18, 20, 21, 22, 23, 24]
    
    if df is not None:
        if view_mode == "🏠 Dashboard Principal":
            # Métricas principais com design 
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🎮 JOGOS REALIZADOS</h3>
                    <h1 style=""font-size: 2.5rem; margin: 0.5rem 0; color: #ffffff; text-shadow: 1px 1px 4px rgba(0,0,0,0.5);">{len(games_df)}</h1>
                    <p style="opacity: 0.8;">Total de apostas</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                total_acertos = games_df['ACERTOS'].sum()
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🎯 ACERTOS TOTAIS</h3>
                    <h1 style=""font-size: 2.5rem; margin: 0.5rem 0; color: #ffffff; text-shadow: 1px 1px 4px rgba(0,0,0,0.5);">{total_acertos}</h1>
                    <p style="opacity: 0.8;">Números acertados</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                media_acertos = games_df['ACERTOS'].mean()
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📊 MÉDIA DE ACERTOS</h3>
                    <h1 style=""font-size: 2.5rem; margin: 0.5rem 0; color: #ffffff; text-shadow: 1px 1px 4px rgba(0,0,0,0.5);">{media_acertos:.1f}</h1>
                    <p style="opacity: 0.8;">Por jogo</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                max_acertos = games_df['ACERTOS'].max()
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🏆 MELHOR RESULTADO</h3>
                    <h1 style=""font-size: 2.5rem; margin: 0.5rem 0; color: #ffffff; text-shadow: 1px 1px 4px rgba(0,0,0,0.5);">{max_acertos}</h1>
                    <p style="opacity: 0.8;">Máximo de acertos</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Último sorteio destacado
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### 🎲 ÚLTIMO SORTEIO - CONCURSO 3470")
            st.markdown(display_numbers_as_balls(winning_numbers, title="Números Sorteados"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Análise detalhada dos jogos
            st.markdown("---")
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### 🎮 ANÁLISE DETALHADA DOS JOGOS")
            
            for _, game in games_df.iterrows():
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
                    games_df,
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
                acertos_dist = games_df['ACERTOS'].value_counts().sort_index()
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
            
            # Tabela detalhada
            st.markdown("### 📊 TABELA COMPLETA DE JOGOS")
            
            # Preparar dados para exibição
            games_display = games_df.copy()
            games_display['NUMEROS_STR'] = games_display['NUMEROS'].apply(
                lambda x: ' - '.join([f"{n:02d}" for n in sorted(x)])
            )
            games_display['ACERTOS_COM_SORTEIO'] = games_display['NUMEROS'].apply(
                lambda x: len([n for n in x if n in winning_numbers])
            )
            games_display['TAXA_ACERTO'] = (games_display['ACERTOS_COM_SORTEIO'] / 15 * 100).round(1)
            
            # Status baseado nos acertos
            def get_status(acertos):
                if acertos >= 11:
                    return "🏆 Premiado"
                elif acertos >= 8:
                    return "🎯 Regular"
                else:
                    return "⭐ Baixo"
            
            games_display['STATUS'] = games_display['ACERTOS_COM_SORTEIO'].apply(get_status)
            
            st.dataframe(
                games_display[['JOGO', 'NUMEROS_STR', 'ACERTOS_COM_SORTEIO', 'TAXA_ACERTO', 'STATUS']].rename(columns={
                    'JOGO': '🎮 Jogo',
                    'NUMEROS_STR': '🔢 Números',
                    'ACERTOS_COM_SORTEIO': '🎯 Acertos',
                    'TAXA_ACERTO': '📊 Taxa (%)',
                    'STATUS': '🏆 Status'
                }),
                use_container_width=True,
                height=400
            )
            
            # Análise temporal (simulada)
            st.markdown("---")
            st.markdown("### 📈 EVOLUÇÃO DOS RESULTADOS")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de linha dos acertos
                fig_evolucao = px.line(
                    games_df,
                    x='JOGO',
                    y='ACERTOS',
                    title='Evolução dos Acertos por Jogo',
                    markers=True,
                    color_discrete_sequence=['#ffd700']
                )
                fig_evolucao.add_hline(y=games_df['ACERTOS'].mean(), line_dash="dash", 
                                      line_color="#663399", annotation_text="Média")
                fig_evolucao.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    title_font=dict(color='white')
                )
                st.plotly_chart(fig_evolucao, use_container_width=True)
            
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
            insights.append(f"🏆 **Melhor jogo:** #{melhor_jogo['JOGO']} com {melhor_jogo['ACERTOS']} acertos")
            
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
            
            # Comparação com estatísticas dos sorteios
            stats = calculate_advanced_stats(games_df, winning_numbers)
            if 'pares_sorteio' in stats:
                insights.append(f"⚖️ **Último sorteio:** {stats['pares_sorteio']} pares e {stats['impares_sorteio']} ímpares")
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
        <p style="color: #9966cc; margin-bottom: 0.5rem;">Desenvolvido com tecnologia avançada • Streamlit & Plotly</p>
        <p style="color: rgba(255,255,255,0.7);">Última atualização: {}</p>
        <div style="width: 100px; height: 2px; background: linear-gradient(90deg, #ffd700, #663399); margin: 15px auto; border-radius: 1px;"></div>
    </div>
    """.format(datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()





















