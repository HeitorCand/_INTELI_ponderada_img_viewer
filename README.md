# Visualizador de Imagens com Filtros

Este é um aplicativo de visualização de imagens desenvolvido em Python usando PySimpleGUI e Pillow (PIL). O aplicativo permite aos usuários visualizar imagens, aplicar diversos filtros e transformações e salvar o resultado.

## Funcionalidades

- **Carregamento automático de imagens**: As imagens são carregadas automaticamente assim que selecionadas no navegador de arquivos.
- **Visualização lado a lado**: Exibe a imagem original e modificada lado a lado para comparação.
- **Filtros disponíveis**:
  - Escala de cinza
  - Inversão de cores
  - Aumento de contraste
  - Desfoque
  - Nitidez
  - Detecção de bordas
- **Transformações**:
  - Rotação (com controle de ângulo de -180° a 180°)
- **Salvar imagens**: Permite salvar a imagem modificada em um arquivo novo.
- **Resetar modificações**: Restaura a imagem ao seu estado original.

## Requisitos

- Python 3.x
- PySimpleGUI
- Pillow (PIL)
- NumPy

## Instalação

1. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

2. Para usuários de macOS, pode ser necessário instalar o tkinter:

```bash
brew install python-tk@3.13
```

## Como usar

1. Execute o script:

```bash
python main.py
```

2. Na interface do aplicativo:
   - Clique em "Browse" para selecionar uma imagem (a imagem será carregada automaticamente)
   - Selecione os filtros desejados marcando as caixas correspondentes
   - Para rotacionar, marque "Rotacionar" e ajuste o ângulo usando o controle deslizante
   - Clique em "Aplicar" para processar a imagem com os filtros e transformações selecionados
   - Use "Resetar" para voltar à imagem original
   - Clique em "Salvar Imagem" para salvar a imagem modificada em um novo arquivo

## Estrutura do código

- **FILTERS**: Dicionário contendo os diferentes filtros disponíveis e suas implementações
- **TRANSFORMATIONS**: Dicionário com as transformações disponíveis
- **convert_to_bytes**: Converte imagens PIL para bytes para exibição no PySimpleGUI
- **apply_filters**: Aplica os filtros selecionados à imagem
- **apply_transformation**: Aplica transformações à imagem
- **main**: Função principal que configura a interface e gerencia eventos

## Exemplos de uso

1. **Converter uma imagem para escala de cinza**:
   - Selecione a imagem
   - Marque "Escala de cinza"
   - Clique em "Aplicar"
   - Salve o resultado

2. **Detectar bordas e rotacionar**:
   - Selecione a imagem
   - Marque "Detecção de bordas"
   - Marque "Rotacionar" e ajuste o ângulo para 90°
   - Clique em "Aplicar"
   - Salve o resultado

## Personalização

Para adicionar novos filtros, basta adicionar novas entradas ao dicionário `FILTERS` com a implementação correspondente:

```python
FILTERS = {
    # ... filtros existentes ...
    "Novo Filtro": lambda img: # implementação do filtro
}
```

Da mesma forma, novas transformações podem ser adicionadas ao dicionário `TRANSFORMATIONS`:

```python
TRANSFORMATIONS = {
    # ... transformações existentes ...
    "Nova Transformação": lambda img, val: # implementação da transformação
}
```

## Detalhes técnicos

### Processamento de imagem

O aplicativo utiliza a biblioteca Pillow para manipular as imagens. Cada filtro é implementado como uma função lambda que recebe uma imagem e retorna uma imagem processada.

As transformações são implementadas como funções lambda que recebem uma imagem e um valor (por exemplo, o ângulo de rotação) e retornam uma imagem transformada.

### Interface do usuário

A interface do usuário é construída usando PySimpleGUI, que fornece uma maneira simples e rápida de criar interfaces gráficas em Python. A interface é dividida em duas colunas:

- **Coluna esquerda**: Contém os controles para seleção de filtros, transformações e ações (aplicar, salvar, resetar).
- **Coluna direita**: Exibe a imagem original e a imagem modificada lado a lado.

A interface foi projetada para ser intuitiva e fácil de usar, permitindo que os usuários vejam imediatamente o resultado das suas modificações.