# Trace Feature

![PyPI - Python Version](https://img.shields.io/badge/python-3-blue.svg?longCache=true&style=flat-square)
![License](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)
![DSW](https://img.shields.io/badge/Desenho-2018.1-red.svg?Cache=true&style=flat-square)


Neste repositório se encontra a ferramenta de geração de _traces_ a partir da execução de cada feature BDD. 

## Instalação

### Virtualenv

##### **1. Instale o Pip**
Para visualizar se você possui o pip instalado, use:
```python
pip --version
```

Caso não tenha o pip instalado, use:
```python
sudo apt-get install python3-pip
```


##### **2. Instale o Virtualenv**
Para visualizar se você possui o virtualenv instalado, use:
```python
virtualenv --version
```

Caso não tenha o pip instalado, use:   
```python
sudo pip3 install virtualenv
```


##### **3. Crie um Virtualenv com Python3**
```python
virtualenv -p python3 env
```


##### **4. Entre no Virtualenv**
Entre na pasta que contém seu virtualenv e use:  

```python 
source env/bin/activate
```

---

Após criar um _virtualenv_, navegue até o diretório `trace_feature` e execute o seguinte comando:   

```python
$ pip install .
```

### Navegue até o projeto que deseja analisar e execute:
```python
$ python 
> import trace_feature as t
> t.trace_feature()
```

---
Para efeitos de teste, foi disponibilizado um projeto _rails_, que pode ser acessado no seguinte link: 
