import string
import math
import re
import numpy as np

from unidecode import unidecode

class Ngram:
        
    # Inicializacion 
    def __init__(self,word, n=3, symbol_count=27):
        self.n = n
        self.word = word
        self.symbol_count = symbol_count
        self.ngrams_values = self.ngrams()
        
            
    """ Operaciones """
    # Producto Interno calculado sobre los conjuntos de valores enteros (indices) de los ngramas
    # Esto se basa en que los valores ngramas son unicos y que el producto interno es la cantidad de elementos en la interseccion
    # a = (1,0,0,1) es representad como el conjunto {0,3}
    # b = (0,1,0,1) es representado como el conjunto {1,3}
    # a.b = 2 (longitud interseccion de los conjuntos)
    def iproduct(self, other):
        intersection = set(self.ngrams_values).intersection(set(other.ngrams_values))
        return len(intersection)
        
    # Norma del vector
    # La norma del vector es la raiz cuadrada de la suma de los cuadrados de sus elementos
    # asumiendo vectores binarios, la norma es la raiz cuadrada de la cantidad de elementos del vector distintos de cero
    # en la representacion de los ngramas, un elemento distinto de cero es un indice de un ngrama en el conjunto ngram_values
    # a = (1,0,0,1) es representad como el conjunto {0,3} y su norma es sqrt(2)
    def norm(self):
        return math.sqrt( len(self.ngrams_values))
    
    # Comparacion de dos trigramas basada en el producto interno y la norma (distancia coseno)
    def compare(self, other):
        return self.iproduct(other)/(self.norm()*other.norm())
        
    """ Funciones Auxiliares """
    
    # Genera el conjunto de ngramas de la palabra limpia de acentos y normalizada (sin repeticiones de ngramas) 
    # El conjunto es representado como un conjunto de valores enteros (indices) de los ngramas
    # El indice de un ngrama es calculado como la suma de los valores de los simbolos que 
    # lo componen multiplicados por la base (cantidad de simbolos) elevado a la posicion del simbolo en el ngrama
    def ngrams(self, as_value=True):

        n = self.n
        symbol_count = self.symbol_count

        # reemplazar caracteres acentuados por sus equivalentes sin acento
        text = unidecode(self.word)
        
        # filtrar los caracteres no deseados de la cadena de entrada y convertir a mayúsculas
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = text.upper()

        # obtener la longitud del texto
        text_length = len(text)

        # generar el set de n-gramas únicos
        ngrams = set()
        for i in range(text_length - n + 1):
            ngram = text[i:i+n]
            ngram_value = 0
            for j, symbol in enumerate(ngram):
                symbol_value = ord(symbol) - ord('A') + 1 if symbol != ' ' else 0
                ngram_value += symbol_value * (symbol_count ** (n - j - 1))
            
            if as_value:
                ngrams.add(ngram_value)
            else:
                ngrams.add(ngram)

        return ngrams
    
    # Genera el vector de valores flotantes de la secuencia de valores de ngramas
    # cada valor del vector es la representacion de un bloque de n bits del vector binario 
    # reconstruido a partir de el conjunto de valores de valores de ngramas (ngrams_values)
    def as_vector(self, n):
        # obtener la longitud de la secuencia
        sequence_length = self.symbol_count ** self.n
        sparse_sequence = self.ngrams_values

        vector_length = 1 + (sequence_length // n)
        # imprimir la longitud del vector
        print('vector length:', vector_length)

        # crear un array numpy de ceros del tamaño adecuado
        double_vector = np.zeros(vector_length, dtype=np.float64)

        # agregar cada bloque al vector de salida
        current_block = ''
        for i in range(sequence_length):
            if i in sparse_sequence:
                current_block += '1'
            else:
                current_block += '0'
            if (i+1) % n == 0:
                double_vector[(i+1)//n-1] = float(int(current_block, 2))
                current_block = ''

        # si la última secuencia no tiene n bits, agregar ceros para completar el último bloque y agregar el último bloque al vector de salida
        if current_block:
            current_block += '0' * (n - len(current_block))
            double_vector[(sequence_length//n)] = float(int(current_block, 2))

        # normalizar el vector
        norm = np.linalg.norm(double_vector)
        if norm == 0:
            return double_vector
        return double_vector / norm





if __name__ == "__main__":

    t1 = Ngram("Julio Raffo, Lautaro Matas",2)
    t2 = Ngram("Julio Raffo, Matas Lautaro",2)
    print (t1.compare(t2))
    print (t1.as_vector(4))

