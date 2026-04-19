# TP 2: Calculadora de índices GINI

## Descripción
Aplicación multicapa que consulta el índice GINI de Argentina
desde la API del Banco Mundial, y procesa los datos a través
de una librería escrita en C.


## Ejecución
Para ejecutarlo, usar los siguientes comandos:

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests
gcc -g -O0 -shared -fPIC -o libgini.so gini_calc.c
python3 gini_fetch.py
```