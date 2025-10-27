# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.0.0] - 2025-01-27

### Adicionado
- Notebook de análise exploratória de dados (etl.ipynb)
- Script de download de dados do Kaggle
- Estrutura inicial do projeto
- README com documentação básica
- Dockerfile e docker-compose para containerização
- Makefile com comandos úteis

### Mudado
- Refatoração completa do notebook ETL
- Implementação de amostragem estratificada para análise temporal
- Atualização da documentação

### Corrigido
- Problema de amostragem que carregava apenas dados de 1995
- Análise de correlação com encoding de variáveis categóricas

