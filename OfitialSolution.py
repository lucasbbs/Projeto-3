# Projeto 3 - APC 2020/2

# Funcões
def imprime_lista(lista, ordenada):
    """ TODO """
    if ordenada:
        lista.sort()
    for item in lista:
        print(item)
        

def calc_distancia(lista1, lista2):
    """ TODO """
    dist = 0
    for i in range(len(lista1)):
        dist += abs(lista1[i] - lista2[i])
    return dist


def build_etapa_1(nomes, amostras, distancias):
    """ TODO """
    qtd_imgs = len(nomes)  
    # Percorre a triangulacão superior da matriz
    for i in range(qtd_imgs):
        for j in range(i + 1, qtd_imgs):
            distancias[i][j] = calc_distancia(amostras.get(nomes[i]),
                                              amostras.get(nomes[j]))
            distancias[j][i] = distancias[i][j] # Espelha os resultados na matriz
                
    # Calcula a soma das distâncias
    min_soma = float("inf")
    indice = 0
    for i in range(qtd_imgs):
        soma = 0
        for j in range(qtd_imgs):
            soma += distancias[i][j]
        if soma < min_soma:
            min_soma = soma
            indice = i
    
    # Retorna nomes_S e nomes_U
    medoid = nomes[indice]
    nomes_U = nomes.copy()
    nomes_U.remove(medoid)
    return [medoid], nomes_U         


def build_etapa_2(k, nomes_S, nomes_U, nomes, distancias):
    """ TODO """
    # Para k = 2...K
    for _ in range(k - 1):
        ganho = [0 for i in range(len(nomes))]
        # Para cada amostra i do conjunto U
        for img_i in nomes_U:
            # Para cada amostra j do conjunto U − {i}
            for img_j in [x for x in nomes_U if x != img_i]:            
                d_j = float("inf")
                # Computa Dj
                for amostra in nomes_S:
                    dist = distancias[nomes.index(img_j)][nomes.index(amostra)]
                    if dist < d_j:
                        d_j = dist
                # Se Dj > d(i,j)
                dist_ij = distancias[nomes.index(img_i)][nomes.index(img_j)]        
                if d_j > dist_ij:
                    ganho[nomes.index(img_i)] += d_j - dist_ij
        
        # Escolha a amostra i que maximize gi
        g = -1
        #img_sel = ''
        for img in nomes_U:
            if ganho[nomes.index(img)] > g:
                img_sel = img
                g = ganho[nomes.index(img)]

        # Remova i do conjunto U e adicione-a ao conjunto S
        nomes_U.remove(img_sel)
        nomes_S.append(img_sel)


def tarefa_3(nomes_S, nomes_U, nomes, distancias):
    """ TODO """
    grupos = {}
    for img in nomes_S:
        grupos[img] = []
        
    for amostra in nomes_U:
        min_dist = float("inf")
        medoid = ''
        for img in nomes_S:
            dist = distancias[nomes.index(amostra)][nomes.index(img)]
            if dist < min_dist:
                medoid = img
                min_dist = dist
        grupos[medoid].append(amostra)
    # Imprime
    for medoid in sorted(grupos):
        print(medoid)
        for amostra in sorted(grupos[medoid]):
            print(f'  {amostra}')
    
    
# Constantes
ARQ = 'vectors.txt'

# Variáveis
nomes_imagens = [] # Contém os nomes das imagens
amostras = {} # Contém os vetores das imagens
distancias = [] # Contém as distâncias entre as imagens
nomes_imagens_S = [] # Contém os nomes das imagens selecionadas
nomes_imagens_U = [] # Contém os nomes das imagens não selecionadas

# Lê os dados de entrada
tarefa, qtd_imgs, k = map(int, input().split())

for _ in range(qtd_imgs):
    nome_img = input()
    amostras[nome_img] = []

# Guarda os nomes das imagens em ordem alfabética
nomes_imagens = list(amostras.keys())
nomes_imagens.sort()

# Lê os dados do arquivo e armazena apenas os dados
# das imagens de interesse.
with open(ARQ) as arq:
    for linha in arq:
        vetor = linha.split()
        nome = vetor[0]
        if nome in amostras:
            amostras[nome] = list(map(float, vetor[1:]))

# Inicializa matriz de distâncias
distancias = [[0 for i in range(qtd_imgs)] for j in range(qtd_imgs)]

# Executa a tarefa
if tarefa == 1:
    nomes_imagens_S, nomes_imagens_U = build_etapa_1(nomes_imagens, amostras, distancias)
    imprime_lista(nomes_imagens_S, False)
elif tarefa == 2:
    nomes_imagens_S, nomes_imagens_U = build_etapa_1(nomes_imagens, amostras, distancias)
    build_etapa_2(k, nomes_imagens_S, nomes_imagens_U, nomes_imagens, distancias)
    imprime_lista(nomes_imagens_S, True)
elif tarefa == 3:
    nomes_imagens_S, nomes_imagens_U = build_etapa_1(nomes_imagens, amostras, distancias)
    build_etapa_2(k, nomes_imagens_S, nomes_imagens_U, nomes_imagens, distancias)
    tarefa_3(nomes_imagens_S, nomes_imagens_U, nomes_imagens, distancias)
elif tarefa == 4:
    pass
