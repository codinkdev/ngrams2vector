import string
import math
import re
import numpy as np


class Trigram:
           
    #self.ABC  = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    #self.TRIGRAMS = [ x + y + z for x in abc for y in abc for z in abc]
    
    # Inicializacion 
    def __init__(self,word):
        trigs = self._word2trigs( self._cleanword(word) )
        self.dvalues = {}
        for tri in trigs:
            self._set(tri)
            
    """ Operaciones """
    # Producto Interno
    def iproduct(self, other):
        sum = 0
        list = self._getlist(other)
        for i in list:
            sum = sum + self.dvalues.get(i,0)*other.dvalues.get(i,0)    
        return sum
        
    # Norma del vector
    def norm(self):
        return math.sqrt( len(self.dvalues.keys()))
    
    # Comparacion de dos trigramas
    def compare(self, other):
        return self.iproduct(other)/(self.norm()*other.norm())


    """ Getters y Setters Privados  """
    # Marca el valor de un trigrama
    def _set(self, tri):
        self.dvalues[self._tri2int(tri)] = 1

    # Obtiene el valor de un trigrama
    def _get(self, tri):
        tvalue = self._tri2int(tri)
        if self.dvalues.has_key(tvalue):
            return self.dvalues[tvalue]
        else:
            return 0
        
    """ Funciones Auxiliares """
    def _cleanword(self, word: str, pattern: str = "[^A-Z\s]+") -> str:
        return re.sub(pattern, "", word.upper())

    # Obtiene los trigramas correspondientes a una palabra
    def _word2trigs(self, word):
        trigs = []
        word = ' ' + word + ' '
        for i in range(0, len(word) - 2):
            trigs.append(word[i:i+3])
        return trigs
    
    # obtiene el valor entero de un char
    def _charvalue(self, c):
        if c.isalpha():
            return ord(c)-ord('A')+1
        else:
            return 0
        
    # convierte un trigrama en su representacion entera
    def _tri2int(self, tri):
        return self._charvalue(tri[2]) + self._charvalue(tri[1])*27 + self._charvalue(tri[0])*27*27
    
  
    # Obtiene una lista ordernada y sin duplicados de los trigramas 
    def _getlist(self, other):
        l = list(self.dvalues.keys()) + list(other.dvalues.keys())
        l.sort()
        l = self._cleanduplicates(l)
        return l
    
    # limpia duplicados de una lista ordenada
    def _cleanduplicates(self, sortedlist):
        cleanedlist = []
        old = None    
        for e in sortedlist:
            if e != old:
                cleanedlist.append(e)
                old = e
        return cleanedlist
 

class Ngram:
        
    # Inicializacion 
    def __init__(self,word, n=3):
        self.n = n
        trigs = self._word2trigs( self._cleanword(word) )
        self.dvalues = {}
        for tri in trigs:
            self._set(tri)
            
    """ Operaciones """
    # Producto Interno
    def iproduct(self, other):
        sum = 0
        list = self._getlist(other)
        for i in list:
            sum = sum + self.dvalues.get(i,0)*other.dvalues.get(i,0)    
        return sum
        
    # Norma del vector
    def norm(self):
        return math.sqrt( len(self.dvalues.keys()))
    
    # Comparacion de dos trigramas
    def compare(self, other):
        return self.iproduct(other)/(self.norm()*other.norm())


    """ Getters y Setters Privados  """
    # Marca el valor de un trigrama
    def _set(self, tri):
        self.dvalues[self._tri2int(tri)] = 1

    # Obtiene el valor de un trigrama
    def _get(self, tri):
        tvalue = self._tri2int(tri)
        if self.dvalues.has_key(tvalue):
            return self.dvalues[tvalue]
        else:
            return 0
        
    """ Funciones Auxiliares """
    def _cleanword(self, word: str, pattern: str = "[^A-Z\s]+") -> str:
        return re.sub(pattern, "", word.upper())

    # Obtiene los trigramas correspondientes a una palabra
    def _word2trigs(self, word):
        trigs = []
        word = ' ' + word + ' '

        for i in range(0, len(word) - self.n + 1):
            trigs.append(word[i:i+self.n])

        return trigs
    

    
    # obtiene el valor entero de un char
    def _charvalue(self, c):
        if c.isalpha():
            return ord(c)-ord('A')+1
        else:
            return 0
        
    # convierte un trigrama en su representacion entera
    def _tri2int(self, tri):
        result = 0
        for i in range(0, self.n):
            result = result + self._charvalue(tri[i])*27**i
        return result
    
  
    # Obtiene una lista ordernada y sin duplicados de los trigramas 
    def _getlist(self, other):
        l = list(self.dvalues.keys()) + list(other.dvalues.keys())
        l.sort()
        l = self._cleanduplicates(l)
        return l
    
    # limpia duplicados de una lista ordenada
    def _cleanduplicates(self, sortedlist):
        cleanedlist = []
        old = None    
        for e in sortedlist:
            if e != old:
                cleanedlist.append(e)
                old = e
        return cleanedlist
 

def generate_normalized_vector(sparse_sequence, m, n):
    # obtener la longitud de la secuencia
    sequence_length = m

    vector_length = 1 + (sequence_length // n)
    print(vector_length)

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

import re

def generate_ngrams(text, n):
    # filtrar los caracteres no deseados de la cadena de entrada y convertir a mayúsculas
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.upper()

    # obtener la longitud del texto
    text_length = len(text)

    # generar el set de n-gramas únicos
    ngrams = set()
    symbol_count = 27 # letras mayúsculas más espacio
    for i in range(text_length - n + 1):
        ngram = text[i:i+n]
        ngram_value = 0
        for j, symbol in enumerate(ngram):
            symbol_value = ord(symbol) - ord('A') + 1 if symbol != ' ' else 0
            ngram_value += symbol_value * (symbol_count ** (n - j - 1))
        ngrams.add(ngram_value)

    return ngrams


if __name__ == "__main__":

    t1 = Ngram("Julio Raffo, Lautaro Matas",2)
    t2 = Ngram("Julio Raffo, Rodriguez Lautaro",2)
    print (t1.compare(t2))

    print(generate_normalized_vector([1,2,3,10,12], 16,2))
