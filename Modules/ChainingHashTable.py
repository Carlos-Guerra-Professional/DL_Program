#Chaining Hash Table Data Structure
class ChainingHashTable:
    def __init__(self, table_size=41):
        self.table = []
        for i in range(table_size):
            self.table.append([])

    # Chaining Hash Table places objects into bucket(s) respectively using a key value system and handles collisions by
    # appending values (items) to buckets.
    # Time is O(1), Worst Case Space Complexity is O(n).
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Search can be done by finding the bucket represented by the correct key matching
    # the hashkey calculation using the items own key and if more than 1 item in the bucket, will search each item 1 by 1
    # till item is found inside that bucket.
    #Best time complexity is O(1), worst is O(n).
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]
            return None

    def __str__(self):
        index = 0
        s = ""                # s
        for bucket in self.table:
            s += "%2d: %s\n" % (index, bucket)
            index += 1
        return s

    def display_hash_table(hash_table):
        for i in range(hash_table):
            print(i, ": ")
            for j in hash_table[i]:
                print(j)


