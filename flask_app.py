from flask import Flask, render_template, request, url_for
import numpy as np

app = Flask(__name__)
app.secret_key = 'flask'


@app.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html') 

@app.route('/incerteza', methods=['get','post'])
def incerteza():
    return render_template('incerteza.html')

@app.route('/risco', methods=['get','post'])
def risco():
    return render_template('risco.html')


@app.route('/maxmin', methods=['get','post'])
def maxmin():
    num_investimentos = request.form['num_investimentos']
    num_cenarios = request.form['num_cenarios']

    print(num_investimentos,num_cenarios)
    return render_template('risco.html', num_cenarios=int(num_cenarios), num_investimentos=int(num_investimentos))


@app.route('/maxmin_input', methods=['get','post'])
def maxmin_input():
    x = request.form['num_investimentos']
    y = request.form['num_cenarios']
    vetor = []
    risco_cenario = []
    for i in range(int(y)):
        aux = float(request.form['risco_cenario{}'.format(i)])
        risco_cenario.append(aux)

    for i in range(int(x)):
        investimentos = []
        for j in range(int(y)):
            aux = float(request.form['investimentos{}{}'.format(i,j)])
            investimentos += [aux]
        #print(investimentos)
        vetor += [investimentos]
        
    #print(vetor)
    
    #cria uma matriz
    matriz = np.array(vetor)

    #Maiores valores de cada linha
    maxInRows = np.amax(matriz, axis=1)
    #Menores valores de cada linha
    minInRows = np.amin(matriz, axis=1)
    #Maiores valores de cada coluna
    maxInColumns = np.amax(matriz, axis=0)

    laplace = []
    hurwicz = []
    for i in range(int(x)):
        aux1 = 0
        aux2 = 0
        for j in range(int(y)):
            aux1 += (matriz[i][j])
            aux2 += (matriz[i][j] * risco_cenario[j])
        laplace.append(aux1/int(y))
        hurwicz.append(aux2)

    vetorMAIORES = []
    for i in range(int(x)):
        investimentos = []
        for j in range(int(y)):
            investimentos += [ maxInColumns[j] - matriz[i][j] ]
        #print(investimentos)
        vetorMAIORES += [investimentos]

    lista_maiores = []
    for i in range(int(x)):
        vetorAUX = []
        for j in range(int(y)):
            vetorAUX.append(vetorMAIORES[i][j])
            maior = max(vetorAUX)
        lista_maiores.append(maior)

    menor_lista_maior = min(lista_maiores)

    return render_template('maxmin.html', matriz=matriz, risco_cenario=risco_cenario, num_investimentos=int(x), num_cenarios=int(y), maxInRows=maxInRows, minInRows=minInRows, laplace=laplace, hurwicz=hurwicz, lista_maiores=lista_maiores, menor_lista_maior=menor_lista_maior, vetorMAIORES=vetorMAIORES)


@app.route('/vme', methods=['get','post'])
def vme():
    num_investimentos = request.form['num_investimentos']
    num_cenarios = request.form['num_cenarios']

    print(num_investimentos,num_cenarios)
    return render_template('incerteza.html', num_cenarios=int(num_cenarios), num_investimentos=int(num_investimentos))


@app.route('/vme_input', methods=['get','post'])
def vme_input():
    x = request.form['num_investimentos']
    y = request.form['num_cenarios']
    vetor = []
    risco_cenario = []
    for i in range(int(y)):
        aux = float(request.form['risco_cenario{}'.format(i)])
        risco_cenario.append(aux)

    for i in range(int(x)):
        investimentos = []
        for j in range(int(y)):
            aux = float(request.form['investimentos{}{}'.format(i,j)])
            investimentos += [aux]
        #print(investimentos)
        vetor += [investimentos]
        
    #print(vetor)
    
    matriz = np.array(vetor)

    print(matriz)
    print(risco_cenario)
    
    inv = []
    for i in range(int(x)):
        total = 0
        for j in range(int(y)):
            total += (matriz[i][j] * risco_cenario[j])
        inv.append(total)

    print(inv)

    melhor_investimento = max(inv)
    indece_melhor_investimento = inv.index(melhor_investimento)+1

    print(melhor_investimento, indece_melhor_investimento)

    maxInColumns = np.amax(matriz, axis=0)

    vetorPOE = []
    for i in range(int(x)):
        investimentos = []
        for j in range(int(y)):
            investimentos += [ maxInColumns[j] - matriz[i][j] ]
        #print(investimentos)
        vetorPOE += [investimentos]

    matrizPOE = vetorPOE

    perdas_ponderadas = []
    for i in range(int(x)):
        total = 0
        for j in range(int(y)):
            total += (vetorPOE[i][j] * risco_cenario[j])
        perdas_ponderadas.append(total)

    menor_perda_ponderada = min(perdas_ponderadas)

    investimento_perfeito = maxInColumns
    investimento_perfeito_ponderado = []

    for i in range(int(y)):
        investimento_perfeito_ponderado.append( investimento_perfeito[i] * risco_cenario[i] )

    total_investimentos_perfeito_ponderado = sum(investimento_perfeito_ponderado)

    VEIP = total_investimentos_perfeito_ponderado - melhor_investimento 

    return render_template('vme.html',matriz=matriz, risco_cenario=risco_cenario, melhor_investimento=melhor_investimento, indece_melhor_investimento=indece_melhor_investimento, num_investimentos=int(x), num_cenarios=int(y), inv=inv, max=maxInColumns, POE=vetorPOE, perdas_ponderadas=perdas_ponderadas, menor_perda_ponderada=menor_perda_ponderada, investimento_perfeito=investimento_perfeito, investimento_perfeito_ponderado=investimento_perfeito_ponderado ,total_investimentos_perfeito_ponderado=total_investimentos_perfeito_ponderado, VEIP=VEIP)

app.run(debug=True)