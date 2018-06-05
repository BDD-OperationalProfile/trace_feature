# trace_feature
Neste repositório se encontra a ferramenta de geração de traces a partir da execução de cada feature BDD. 

## Instalação

### Após criar um virtualenv, navegue até o diretório trace_feature e execute o seguinte comando:
```
$ pip install -e .
```
### Navegue até o projeto que deseja analisar (myrottenpotatoes) e execute:
```
$ python 
> import trace_feature as t
> t.trace_feature()
```
