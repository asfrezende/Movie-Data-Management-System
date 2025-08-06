import csv
import pandas as pd
import math
import time

# Hash Table to map movies and users
class TH_filmes:
    def __init__(self, tam=10, max=0.8):
        self.tam = tam
        self.tabela = [[] for a in range(tam)]
        self.quant = 0
        self.max = max

    # Given a new table size and a flag, resizes table
    def th_redimensionar(self, novo_tam, flag):
        th_antiga = self.tabela
        self.tam = novo_tam
        self.tabela = [[] for a in range(novo_tam)]
        self.quant = 0 
        if flag == 0:
            for filme in th_antiga:
                for item in filme:
                    self.th_insere_filme(item[0], item[1], item[2], item[3], item[4], item[5])
        else:
            for user in th_antiga:
                for item in user:
                    self.th_insere_usuario(item[0], item[1])
        return

    # Given a Hash Table (TH_filmes), checks if the ratio between the amount of movies and table size is appropriate based on the max occupation rate
    def th_confere_tam(self, flag):
        proporcao = self.quant/self.tam
        if proporcao > self.max:
            novo_tam = self.tam*2
            self.th_redimensionar(novo_tam, flag)
        return

    def func_hash(self, chave):
        return sum(ord(c) for c in str(chave))%10

    # Given an user and a list of the movies, inserts it on the table
    def th_insere_usuario(self, id_user, filmes):
        self.th_confere_tam(1)
        index = self.func_hash(id_user)
        novo_user = [id_user, filmes]
        for i, item in enumerate(self.tabela[index]): 
            if item[0] == id_user:
                self.tabela[index][i] = novo_user
                return
        self.tabela[index].append(novo_user)
        self.quant += 1
        return

    # Given an user ID, returns his info
    def th_busca_user(self,id_user):
        index = self.func_hash(id_user)
        for user in self.tabela(index):
            if user[0] == id_user:
                return user
        return None

    # Given a movie (ID, title, genre, year, number of ratings and average rating), inserts it on the table
    def th_insere_filme(self, id_f, titulo, generos, ano, quant_av, media_av):
        self.th_confere_tam(0)
        index = self.func_hash(id_f) 
        novo_filme = [id_f, titulo, generos, ano, quant_av, media_av]
        for i, item in enumerate(self.tabela[index]): 
            if item[0] == id_f:
                self.tabela[index][i] = novo_filme 
                return
        self.tabela[index].append(novo_filme)
        self.quant += 1
        return

    # Given a movie ID, returns the movie
    def th_busca_filme(self, id_f):
        index = self.func_hash(id_f)
        for filme in self.tabela[index]:
            if filme[0] == id_f:
                return filme
        return None

    # Given an array, loads its components into the Hash Table
    def th_carrega_filmes(self, matriz):
        for l in matriz:
            id_f = l[0]
            nome = l[1]
            generos = l[2]
            ano = l[3]
            quant_av = l[4]
            media_av = l[5]
            self.th_insere_filme(id_f, nome, generos, ano, quant_av, media_av) 
        return

# Trie nodes
class NodoTrieFilmes:
    def __init__(self):
        self.filhos = [None] * 256
        self.idf = None
        self.fim = False
# Trie to map the movies' names
class ArvoreTrieFilmes:
    def __init__(self):
        self.raiz = NodoTrieFilmes()

###########################################################################################################
############################################## SORTING ####################################################
# Modified counting sort
def counting_sort(arr, val):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        index = int((arr[i] * (10**6)) // val) % 10
        count[index] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        index = int((arr[i] * (10**6)) // val) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    return output

def lsd_radix_sort(arr):
    max_val = int(max(arr)*(10**6))
    exp = 1
    while max_val // exp > 0:
        arr = counting_sort(arr, exp)
        exp *= 10
    return arr

# Modified selection sort with two priorities: user rating (first) and average global rating
def selection_sort_1(filmes):
    n = len(filmes)
    for i in range(n):
        max = i
        for j in range(i+1, n):
            if filmes[j][6] > filmes[max][6]:
                max = j
            elif filmes[j][6]==filmes[max][6] and filmes[j][5] > filmes[max][5]:
                max = j
        filmes[i], filmes[max] = filmes[max], filmes[i]
    return filmes

# Modified selection sort
def selection_sort(filmes):
    n = len(filmes)
    for i in range(n):
        max = i
        for j in range(i+1, n):
            if filmes[j][5] > filmes[max][5]:
                max = j
            elif filmes[j][5]==filmes[max][5] and filmes[j][4]>filmes[max][4]:
                max = j
        filmes[i], filmes[max] = filmes[max], filmes[i]
    return filmes
###########################################################################################################
###########################################################################################################

# Given an user, an array of users and a hash table, returns an array with all movies rated by the user
def busca_user_csv(id_user, matriz_user, th_filmes):
    resultados = []
    for user in matriz_user:
        if user[0] == id_user:
            for filme_info in user[1]:
                id_filme = filme_info[0]
                filme_dados = th_filmes.th_busca_filme(id_filme)
                if filme_dados:
                    resultados.append({filme_dados[1], filme_info[1]})
            return resultados
    return None

# Given a CSV file with ratings, organizes its data on an array in the format:
# [[user ID, [movie ID, movie rating, movie date]], ...., []]
def le_users_csv(nome):
    df = pd.read_csv(nome, encoding='utf-8')
    return [[user, 
             group[['movieId', 'rating', 'date']].values.tolist()]
            for user, group in df.groupby('userId')]


# Given a CSV file with movie ratings and an array of movies, inserts the ratings in the array
def le_ratings_csv(matriz, nome):
    arquivo = pd.read_csv(nome, encoding='utf-8')
    conteudo_ratings = arquivo.groupby('movieId')['rating'].agg(['count', 'sum']).reset_index()
    filmes_df = pd.DataFrame(matriz, columns=['title', 'movieId', 'genres', 'year', 'quant_av', 'media_av'])
    filmes_df = filmes_df.merge(conteudo_ratings, on='movieId', how='left')
    filmes_df['count'] = filmes_df['count'].fillna(0)
    filmes_df['sum'] = filmes_df['sum'].fillna(0.0)

    filmes_df['quant_av'] = filmes_df['count'].astype(int)
    filmes_df['media_av'] = filmes_df.apply(lambda row: math.floor((row['sum']/row['count'])*10**6)/10**6 if row['count']>0 else 0.0, axis=1)
    filmes_df = filmes_df.drop(['count', 'sum'], axis=1)
    matriz = filmes_df.values.tolist()
    return matriz

# Given an CSV file with movies' infos, organizes them in an array
def le_filmes_csv(nome):
    df = pd.read_csv(nome, encoding='utf-8')
    df['genres'] = df['genres'].str.split('|')
    df = df[['title', 'movieId', 'genres', 'year']]
    matriz = df.values.tolist()
    for linha in matriz:
        linha.extend([0, 0])
    return matriz

# Given the root of a Trie, a word and a movie ID, iserts it on the given Trie
def insere_nodo_trie(raiz, palavra, chave):
    atual = raiz
    for letra in palavra:
        i = ord(letra) % 256
        if atual.filhos[i] is None:
            atual.filhos[i] = NodoTrieFilmes()
        atual = atual.filhos[i]
    atual.idf = chave
    atual.fim = True

# Given the root of a Trie and a list of IDs, searches the tree and returns all IDs found
def trie_busca_prefixo_aux(raiz, ids):
    if raiz.fim:
        ids.append(raiz.idf)
    for i in range(256):
        if raiz.filhos[i] is not None:
            trie_busca_prefixo_aux(raiz.filhos[i], ids)
    return

# Given the root of a Trie and a prefix, searches for the movies with the prefix and returns a list of their IDs
def trie_busca_prefixo(raiz, prefix):
    atual = raiz
    for letra in prefix:
        i = ord(letra) % 256
        if atual.filhos[i] is None:
            return None
        atual = atual.filhos[i]
    ids = []
    trie_busca_prefixo_aux(atual, ids) 
    if ids:
        return ids
    return None

# Given a movie prefix, the root of a Trie and a Hash Table, searches for all movies with the given prefix on the hash table and returns an array with their info
def busca_por_prefixo(prefix, trie, th):
    filmes_encontrados = trie_busca_prefixo(trie, prefix)
    res = []
    if filmes_encontrados is not None:
        for filme in filmes_encontrados:
            if th.th_busca_filme(filme.idf) is not None:
                res.append(th.th_busca_filme(filme.idf)) # coloca na matriz as informações de cada filme
        return res
    return None

# Given a Hash Table and a Trie, map the data from two CSV files into these structures
# This function also tracks its execution time
def leitura_de_arq(th, trie_f):
    tempo_ini = time.time()

    dados_filmes_movies = le_filmes_csv("movies.csv")
    if dados_filmes_movies:
        for titulo, id_f, generos, ano, quant_av, media_av in dados_filmes_movies:
            insere_nodo_trie(trie_f.raiz, titulo, id_f)
    dados_filmes_movies = le_ratings_csv(dados_filmes_movies, "ratings.csv")
    for filme in dados_filmes_movies:
        th.th_insere_filme(filme[1], filme[0], filme[2], filme[3], filme[4], filme[5])
    dados_usuarios_ratings = le_users_csv("ratings.csv")

    tempo_fim = time.time()
    tempo_exec = tempo_fim - tempo_ini
    print(f"Running time: {tempo_exec} seconds \n")

    return dados_usuarios_ratings, th, trie_f

# Given a prefix, the root of a Trie and a Hash table, searches for all movies with given prefix and prints out a list sorted by their average rating in the format:
# movie ID, movie title, genres, release year, global average rating and number of ratings
def busca_por_prefixo(prefixo, trie, th):
    ids_filmes = trie_busca_prefixo(trie.raiz, prefixo)
    if not ids_filmes:
        print(f"No movie found.\n")
        return
    
    filmes_info = []
    medias = []
    for id_filme in ids_filmes:
        filme = th.th_busca_filme(id_filme)
        if filme:
            filmes_info.append(filme)
            medias.append(filme[5])
    
    medias_ordenadas = lsd_radix_sort(medias)
    filmes_ordenados = []
    for media in reversed(medias_ordenadas):
        for i, filme in enumerate(filmes_info):
            if abs(filme[5] - media) < 1e-6:
                filmes_ordenados.append(filme)
                filmes_info.pop(i)

    print("\n{:<10} {:<50} {:<30} {:<8} {:<15} {:<10}".format("movieId", "title", "genres", "year", "rating", "count"))
    print("")

    for filme in filmes_ordenados:
        movieId = filme[0]
        title = filme[1][:47] + "..." if len(filme[1]) > 50 else filme[1]
        genres = ('|'.join(filme[2]) if isinstance(filme[2], list) else filme[2])[:47] + "..." if len('|'.join(filme[2]) if isinstance(filme[2], list) else filme[2]) > 50 else ('|'.join(filme[2]) if isinstance(filme[2], list) else filme[2])
        year = filme[3]
        count = filme[4]
        rating = filme[5]
        print("{:<10} {:<50} {:<50} {:<6} {:<10.6f} {:<10}".format(movieId, title, genres, year, rating, count))
    print("\n")
    return

# Given an user ID, a Hash Table and an array, prints out the info of up to 20 movies rated by the given user sorted in the format:
# movie ID, movie title, genres, number of ratings, global average rating, user rating
def filmes_por_user(userid, th, dados_user):
    user_avs = None
    for user in dados_user:
        if user[0] == userid:
            user_avs = user[1]
    if not user_avs:
        print(f"User not found.\n")
        return

    filmes_user = []
    for avaliacoes in user_avs:
        movieId = avaliacoes[0]
        user_av = avaliacoes[1]
        filme = th.th_busca_filme(movieId)
        if filme:
            filmes_user.append([filme[0], filme[1], filme[2], filme[3], filme[4], filme[5], user_av])

    filmes_user = (selection_sort_1(filmes_user))[:20]

    if filmes_user:
        print("\n{:<10} {:<50} {:<30} {:<6} {:<10} {:<10} {:<10}".format("movieId", "title", "genres", "year", "count", "global", "user"))
        print(" ")
        
        for filme in filmes_user:
            movieId = filme[0]
            title = filme[1][:47] + "..." if len(filme[1]) > 50 else filme[1]
            genres = ('|'.join(filme[2]) if isinstance(filme[2], list) else filme[2])[:27] + "..." if len('|'.join(filme[2]) if isinstance(filme[2], list) else filme[2]) > 30 else ('|'.join(filme[2]) if isinstance(filme[2], list) else filme[2])
            year = filme[3]
            count = filme[4]
            global_rating = filme[5]
            user_rating = "{0:.1f}".format(filme[6])
            print("{:<10} {:<50} {:<30} {:<6} {:<10} {:<10} {:<10}".format(movieId, title, genres, year, count, global_rating, user_rating))
        print("\n")
        return
    else:
        print(f"No movie rated.\n")
        return

# Given an int, a movie genre and a Hash Table, prints out a list of the top N movies of said genre sorted in the format:
# movie ID, movie title, genres, release year, global average rating, number of ratings
def melhores_por_genero(N, genero, th):
    filmes_genero = []
    for item in th.tabela:
        for filme in item:
            if genero in filme[2] and filme[4] >= 1000:
                filmes_genero.append([filme[0], filme[1], filme[2], filme[3], filme[4], filme[5]])

    filmes_genero = filmes_genero[:N] if N <= len(filmes_genero) else filmes_genero
    res = selection_sort(filmes_genero)
    
    if res:
        print("\n{:<10} {:<50} {:<50} {:<6} {:<10} {:<10}".format("movieId", "title", "genres", "year", "rating", "count"))
        print("")

        for filme in res:
            movieId = filme[0]
            title = filme[1][:47] + "..." if len(filme[1]) > 50 else filme[1]
            genres = ('|'.join(filme[2]) if isinstance(filme[2], list) else filme[2])[:47] + "..." if len('|'.join(filme[2]) if isinstance(filme[2], list) else filme[2]) > 50 else ('|'.join(filme[2]) if isinstance(filme[2], list) else filme[2])
            year = filme[3]
            count = filme[4]
            rating = filme[5]
            print("{:<10} {:<50} {:<50} {:<6} {:<10} {:<10}".format(movieId, title, genres, year, rating, count))
        print("\n")
        return
    else:
        print("No movie found.\n")
        return

def main():
    # Initializing data structures, reading files and mapping their data
    trie_filmes = ArvoreTrieFilmes()
    th_filmes = TH_filmes(tam=10) 
    dados_usuarios_ratings, th_filmes, trie_filmes= leitura_de_arq(th_filmes, trie_filmes)

    while True:
        comando = input("- prefix [movie prefix]: list of movies with given prefix.\n"
        "- user [user ID]: list of movies rated by given user.\n"
        "- top [N] [movie genre]: list of the N top movies of given genre.\n"
        "- esc to exit.\n"
        "Run: ").strip()
        if comando.upper() == "ESC" :
            break
        partes = comando.split()
        if not partes:
            continue 
        if partes[0].lower() == "prefix" and len(partes) >= 2:
            prefixo = ' '.join(partes[1:])
            busca_por_prefixo(prefixo, trie_filmes, th_filmes)   
        elif partes[0].lower() == "user" and len(partes) == 2:
            try:
                userid = int(partes[1])
                filmes_por_user(userid, th_filmes, dados_usuarios_ratings)
            except ValueError:
                print("Error.\n")         
        elif partes[0].lower() == "top" and len(partes) >= 3:
            try:
                N = int(partes[1])
                genero = ' '.join(partes[2:])
                melhores_por_genero(N, genero, th_filmes)
            except ValueError:
                print("Error.\n")
        else:
            print("Invalid.\n")

if __name__ == "__main__":
    main()