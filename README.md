# ML Sales Forecasting

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](Dockerfile)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Análise de dados e previsão de preços de imóveis no Reino Unido usando machine learning

## Destaques

- Análise exploratória de 30M+ transações imobiliárias (1995-2025)
- Amostragem estratificada para representatividade temporal
- Visualizações e correlações de preços
- Preparação de dados para modelos preditivos
- Notebooks documentados passo-a-passo
- Containerização com Docker

## Funcionalidades

- Análise exploratória do dataset UK Property Sales
- Amostragem sistemática de 100k linhas distribuídas temporalmente
- Limpeza e transformação de dados
- Análise de correlação com encoding de variáveis categóricas
- Visualizações de evolução temporal e distribuição geográfica
- Identificação de outliers e padrões de mercado

## Stack Tecnológica

- **Python**: 3.11+
- **Data Science**: pandas, numpy, matplotlib, seaborn
- **Machine Learning**: scikit-learn
- **Notebooks**: Jupyter Lab
- **Containerization**: Docker
- **Testing**: pytest

## Quick Start

### Instalação Local

```bash
# Clone do repositório
git clone https://github.com/LucasBiason/ml-sales-forecasting.git
cd ml-sales-forecasting

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r notebooks/requirements.txt

# Iniciar Jupyter Lab
jupyter lab
```

### Notebooks

- `etl.ipynb` - Análise exploratória e preparação de dados
- `download_data.py` - Script para baixar dataset do Kaggle

## Dataset

### UK Property Sales (Price Paid Data)

- **Fonte**: [Kaggle - UK Price Paid Data](https://www.kaggle.com/datasets/lorentzyeung/price-paid-data-202304)
- **Tamanho**: ~30.5 milhões de transações
- **Período**: 1995 a 2025
- **Licença**: Open Government Licence v3.0

### Colunas Principais

- price: Preço da transação em £
- transfer_date: Data da venda
- postcode: Código postal
- property_type: Tipo (D=Detached, S=Semi, T=Terraced, F=Flat)
- county: Condado
- old_new: Y=Nova construção, N=Existente
- duration: F=Freehold, L=Leasehold

## Análise Realizada

### 1. Amostragem Estratificada

Para trabalhar com um dataset de 30M+ linhas, implementei amostragem sistemática que garante representatividade temporal:

```python
# Pega 1 linha a cada 305 linhas (~100k total)
skip_rate = total_rows // sample_size
skip_rows = lambda i: i % skip_rate != 0
```

Isso evita o problema de carregar apenas dados antigos (1995).

### 2. Limpeza e Transformação

- Remoção de duplicatas e dados inválidos
- Conversão de tipos (datetime, numeric, category)
- Criação de features temporais (year, month, quarter)
- Encoding de variáveis categóricas

### 3. Análise Exploratória

- Evolução de preços ao longo de 30 anos
- Distribuição por tipo de propriedade
- Análise geográfica (condados mais caros)
- Identificação de outliers (mercado de luxo)
- Correlações entre variáveis

### 4. Insights Principais

- Preços cresceram consistentemente de 1995 a 2025
- Greater London domina volume e preço médio
- Detached properties são ~40% mais caras que Terraced
- Cerca de 6-7% dos dados são outliers (propriedades > £137k em 1995)
- Propriedades novas tendem a ser mais caras

## Estrutura do Projeto

```
ml-sales-forecasting/
├── notebooks/
│   ├── etl.ipynb            # Análise exploratória completa
│   ├── download_data.py     # Download do dataset do Kaggle
│   ├── requirements.txt     # Dependências Python
│   └── data/               # Dados baixados
├── CHANGELOG.md            # Histórico de mudanças
├── README.md              # Este arquivo
└── LICENSE               # MIT License
```

## Próximos Passos

- [ ] Feature engineering avançado (extrair região do postcode)
- [ ] Modelagem preditiva de preços
- [ ] Análise de sazonalidade (melhor época para comprar/vender)
- [ ] Segmentação de mercado por faixa de preço
- [ ] Dashboard interativo com visualizações

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autor

**Lucas Biason**
- GitHub: [@LucasBiason](https://github.com/LucasBiason)
- LinkedIn: [lucasbiason](https://linkedin.com/in/lucasbiason)

---

**Versão:** 0.0.0  
**Última Atualização:** Janeiro 2025
