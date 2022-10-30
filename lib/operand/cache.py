from lib.contract.base import ICache
# Revisar e implementar: https://realpython.com/lru-cache-python/

class MemoryCache(ICache):
  
    def __init__(self):
        self.__cache = {}
      
    def set(self, key, val):
        self.__cache[str(key)] = val        
  
    def get(self, key):
        if str(key) in self.__cache:
            return self.__cache[str(key)]
        return None
  
    def delete(self, key):
        if str(key) in self.__cache:
            del self.__cache[str(key)]
