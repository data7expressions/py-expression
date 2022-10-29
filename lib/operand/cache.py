from lib.contract.base import ICache
# https://www.geeksforgeeks.org/hash-map-in-python/

class MemoryCache(ICache):
  
    # Create empty bucket list of given size
    def __init__(self, size):
        self.size = size
        self.hash_table = [[] for _ in range(self.size)]
      
    def set(self, key, val):
        hashed_key = hash(key) % self.size          
        bucket = self.hash_table[hashed_key]  
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket[index] = (key, val)
        else:
            bucket.append((key, val))
  
    def get(self, key):
        hashed_key = hash(key) % self.size
        bucket = self.hash_table[hashed_key]  
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            if record_key == key:
                found_key = True
                break
        if found_key:
            return None
  
    def delete(self, key):
        hashed_key = hash(key) % self.size
        bucket = self.hash_table[hashed_key]  
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket.pop(index)
        return
    
    def __str__(self):
        return "".join(str(item) for item in self.hash_table)