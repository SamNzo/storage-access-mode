from pymemcache.client.base import Client
from PIL import Image
from linkedList import LinkedList
import io

class MemLRU:
    def __init__(self, n: int, m: int):
        print("Dont forget to run `memcached` in your terminal")
        self.client = Client("localhost")
        self.link = LinkedList(n, m)

    def create(self, key: str, data: bytearray):
        """
        Add data to cache
        """
        try:
            success = self.client.set(key, bytes(data), noreply=False)
            if success:
                print("Data was successfully added to the cache (key={})".format(key))
                deleted_keys = self.link.create(key)
                # If keys were removed from the linked list: remove them from cache
                # This happens if the list size exceeds <n>
                if (deleted_keys):
                    for key in deleted_keys:
                        self.delete(key, deletefromlist=False)
            else:
                print("Data was not added to the cache (key={})".format(key))
        except Exception as e:
            print(e)

    def readFile(self, path: str, displayImage: bool=False) -> bytearray:
        """
        Read file and write its data in a byte array.
        To display byte data as image make displayImage True
        """
        try:
            f = open("{}".format(path), 'rb')
            data = f.read()
            f.close()
            byte_array = bytearray(data)
        except Exception as e:
            print(e)
            return

        if displayImage:
            image = Image.open(io.BytesIO(byte_array))
            image.show()

        return byte_array

    def readCache(self, key: str, displayImage: bool=False):
        """
        Read value from cache
        """
        data = self.client.get(key)
        if data == None:
            print("Key {} not found in cache".format(key))
        else:
            print("Key {} found in cache".format(key))
            self.link.delete(key, makehead=True)
            if displayImage:
                image = Image.open(io.BytesIO(data))
                image.show()
        return data


    def delete(self, key: str, deletefromlist: bool=True):
        """
        Remove data from cache
        """
        success = self.client.delete(key, noreply=False)
        if success:
            print("Data was successfully removed from the cache (key={})".format(key))
            if deletefromlist:
                self.link.delete(key)
        else:
            print("The given key does not match any of the cache's keys")

if __name__ == '__main__':

    ### MEMCACHE ###
    memory = MemLRU(7, 3)
    # Read image file and display image with bytes
    data = memory.readFile("Images/pepe.png", displayImage=True)
    # Add data to the cache
    memory.create("pepe", data)
    # Read data from the cache and display image
    memory.readCache("pepe", displayImage=True)
    # Delete data from cache
    memory.delete("pepe")