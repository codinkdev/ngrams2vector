import string
import math
import re

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
 


####################### MAIN ################################
### Un ejemplo

t1 = Ngram("Julio Raffo, Lautaro Matas",2)
t2 = Ngram("Julio Raffo, Rodriguez Lautaro",2)
print (t1.compare(t2))
