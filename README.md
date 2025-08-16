# Dashboard Lotofácil 🎯

Um dashboard interativo desenvolvido em Streamlit para análise completa de jogos da Lotofácil, com integração ao Google Sheets.
<div align="center">


<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**🔗 [Acesse o Dashboard Online](https://bolaodosferas.streamlit.app/)** 

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bolaodosferas.streamlit.app/)

</div>

---

## ✨ Funcionalidades

### 🏠 Dashboard Geral
- **Métricas principais**: Total de jogos, acertos, médias
- **Último sorteio**: Visualização dos números sorteados
- **Gráficos interativos**: Acertos por jogo e distribuição

### 🎮 Análise de Jogos
- **Comparação detalhada**: Seus números vs números sorteados
- **Destaque visual**: Números acertados em destaque
- **Taxa de acerto**: Percentual de acerto por jogo

### 📈 Histórico
- **Tabela completa**: Todos os jogos organizados
- **Estatísticas resumo**: Distribuição por faixas de acerto

## 🎨 Design
- **Responsivo**: Funciona em desktop e mobile
- **Interativo**: Gráficos e animações
- **Moderno**: Interface limpa e intuitiva

## 🚀 Instalação

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar o dashboard
```bash
streamlit run dashboard_lotofacil.py
```

### 3. Acessar no navegador
O dashboard estará disponível em: `http://localhost:8501`

## 📋 Configuração do Google Sheets

### 1. Preparar a planilha
- Certifique-se de que a planilha está pública para leitura
- URL deve estar no formato: `https://docs.google.com/spreadsheets/d/ID_DA_PLANILHA/edit`

### 2. Estrutura esperada
```
| CONCURSO | BOLA 1 | BOLA 2 | ... | BOLA 15 |
|----------|--------|--------|-----|---------|
| 3470     | 1      | 4      | ... | 24      |
```

### 3. Configurar no dashboard
- Cole a URL da sua planilha na sidebar
- Clique em "🔄 Atualizar Dados"

## 🎯 Recursos Técnicos

### Cache Inteligente
- Dados são atualizados automaticamente a cada 5 minutos
- Botão manual para atualização imediata

### Visualizações
- **Plotly**: Gráficos interativos e responsivos
- **Bolinhas numeradas**: Simulam as bolinhas da Lotofácil
- **Animações**: Efeitos visuais suaves

### Performance
- Cache de dados para carregamento rápido
- Otimização de memória
- Interface responsiva

## 📊 Exemplos de Análise

### Frequência de Números
Identifica quais números você costuma jogar mais, ajudando a:
- Diversificar suas apostas
- Identificar padrões pessoais
- Comparar com estatísticas oficiais

### Taxa de Acerto
Analisa a performance dos seus jogos:
- Jogos com 11+ acertos (quadra na Lotofácil)
- Jogos intermediários (8-10 acertos)
- Jogos com poucos acertos (<8)

### Comparação Visual
- Números seus vs números sorteados
- Destaque dos acertos
- Visualização intuitiva

## 🔧 Personalização

### Cores
As cores podem ser ajustadas no CSS do arquivo principal:
- `#667eea`: Azul principal
- `#764ba2`: Roxo complementar
- `#ffd700`: Dourado para destaques

### Layout
- Sidebar expansível com configurações
- Grid responsivo
- Cards informativos

## 📱 Compatibilidade

- **Navegadores**: Chrome, Firefox, Safari, Edge
- **Dispositivos**: Desktop, tablet, mobile
- **Python**: 3.8+
- **Streamlit**: 1.28+

## 🆘 Solução de Problemas

### Erro de conexão com Google Sheets
1. Verifique se a URL está correta
2. Confirme que a planilha está pública
3. Teste a URL diretamente no navegador

### Dados não carregando
1. Clique em "🔄 Atualizar Dados"
2. Verifique sua conexão com internet
3. Confirme a estrutura da planilha

### Performance lenta
1. Reduza o número de jogos na planilha
2. Limpe o cache do navegador
3. Reinicie o Streamlit

## 📈 Próximas Melhorias

- [ ] Integração com API oficial da Caixa
- [ ] Exportação de relatórios em PDF
- [ ] Sistema de notificações
- [ ] Análise preditiva
- [ ] Comparação com outros jogadores
- [ ] Histórico de múltiplos concursos

## 👨‍💻 Desenvolvimento

### Estrutura do projeto
```
lotofacil-dashboard/
├── dashboard_lotofacil.py  # Aplicação principal
├── requirements.txt        # Dependências
└── README.md              # Este arquivo
```

### Tecnologias utilizadas
- **Streamlit**: Framework web para Python
- **Pandas**: Manipulação de dados
- **Plotly**: Gráficos interativos
- **NumPy**: Computação numérica
- **Requests**: Requisições HTTP

## 📄 Licença

Este projeto é de código aberto. Sinta-se livre para usar, modificar e distribuir.

---
## **Contato**

[![Website](https://img.shields.io/badge/Website-4c1d95?style=for-the-badge&logo=firefox&logoColor=a855f7)](https://www.nilorocha.tech)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nilo-rocha-/)
[![Email](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:nilo.roch4@gmail.com)

---

## 📈 **Analytics do Projeto**

![GitHub stars](https://img.shields.io/github/stars/seu-usuario/employee-attrition-analytics?style=social)
![GitHub forks](https://img.shields.io/github/forks/seu-usuario/employee-attrition-analytics?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/seu-usuario/employee-attrition-analytics?style=social)



**Dashboard Lotofácil** - Transforme seus dados em insights!
