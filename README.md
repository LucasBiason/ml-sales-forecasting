# ML Sales Forecasting

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Latest-orange.svg)](https://scikit-learn.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Ready-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](Dockerfile)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Sistema completo de previsao de precos de imoveis no Reino Unido usando Random Forest

## Destaques

- Modelo Random Forest com R² = 11.16% (geral) e 27% (imoveis ate £1M)
- Pipeline completo: EDA → Model Selection → Tuning → Production
- Feature engineering com postcode_region (2,253 regioes)
- 4 notebooks Jupyter documentados passo-a-passo
- Modelo exportado e pronto para API FastAPI
- 99,831 amostras de treinamento

## Funcionalidades

- Analise exploratoria de 30M+ transacoes imobiliarias (1995-2025)
- Amostragem estratificada para representatividade temporal
- Feature engineering avancado (postcode_region, target encoding)
- Comparacao de 5 modelos ML (Ridge, Random Forest, XGBoost, LightGBM)
- Hyperparameter tuning com RandomizedSearchCV
- Exportacao de modelo para producao
- Cross-validation para validacao robusta

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

Pipeline completo de ML em 4 notebooks:

1. **01_exploratory_analysis.ipynb** - EDA, amostragem, limpeza
2. **02_model_selection.ipynb** - Feature engineering, comparacao de 5 modelos
3. **03_hyperparameter_tuning.ipynb** - Otimizacao com RandomizedSearchCV
4. **04_pipeline.ipynb** - Treino final e exportacao para producao

Utilitarios:
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

## Resultados do Modelo

### Performance

- **R² Geral**: 11.16% (todos os imoveis)
- **R² <£1M**: 27% (98.6% dos casos)
- **MAE**: £86,796
- **Modelo**: Random Forest (100 estimators)
- **Features**: 6 (property_type, county, postcode_region, old_new, duration, year)

### Feature Importance

As features mais importantes para o modelo:
1. postcode_region_enc (localizacao granular)
2. county_enc (condado)
3. year (epoca da venda)
4. property_type_enc (tipo do imovel)

## Proximos Passos

- [ ] Implementar API FastAPI com endpoints de predicao
- [ ] Criar frontend React para interface de usuario
- [ ] Dockerizar aplicacao completa
- [ ] Deploy em producao (Render/Railway)
- [ ] Adicionar mais features (area, numero de quartos)
- [ ] Dashboard interativo com Streamlit

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autor

**Lucas Biason**
- GitHub: [@LucasBiason](https://github.com/LucasBiason)
- LinkedIn: [lucasbiason](https://linkedin.com/in/lucasbiason)

---

**Versão:** 1.0.0 - Notebooks Completos  
**Última Atualização:** 28 de Outubro de 2025
