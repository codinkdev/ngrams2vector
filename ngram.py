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
        self.ngrams = self.ngrams()
        
        self.dvalues = {}
        for ngram in self.ngrams:
            self.dvalues[ngram] = 1
            
    """ Operaciones """
    # Producto Interno
    def iproduct(self, other):
        sum = 0
        keylist = self._getlist(other)
        for key in keylist:
            sum = sum + self.dvalues.get(key,0)*other.dvalues.get(key,0)    
        return sum
        
    # Norma del vector
    def norm(self):
        return math.sqrt( len(self.dvalues.keys()))
    
    # Comparacion de dos trigramas
    def compare(self, other):
        return self.iproduct(other)/(self.norm()*other.norm())
        
    """ Funciones Auxiliares """
    
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
    
    
    # Obtiene una lista ordernada y sin duplicados de los trigramas 
    def _getlist(self, other):

        keyset = set(self.dvalues.keys())
        keyset.update(other.dvalues.keys())
        keylist = list(keyset)
        keylist.sort()
        return keylist
 

    def as_vector(self, n):
        # obtener la longitud de la secuencia
        sequence_length = self.symbol_count ** self.n
        sparse_sequence = self.ngrams

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

