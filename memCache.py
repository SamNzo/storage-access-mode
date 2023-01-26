from pymemcache.client.base import Client
from PIL import Image
import io
import os

class Mem:
    def __init__(self):
        print("Dont forget to run `memcached` in your terminal")
        self.client = Client("localhost")

    def create(self, key: str, data: bytearray):
        """
        Add data to cache
        """
        try:
            success = self.client.set(key, bytes(data), noreply=False)
            if success:
                print("Data was successfully added to the cache (key={})".format(key))
            else:
                print("Data was not added to the cache (key={})".format(key))
        except Exception as e:
            print(e)

    def readFile(self, path: str, displayImage: int=0) -> bytearray:
        """
        Read file and write its data in a byte array.
        To display byte data as image make displayImage argument equal 1
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

    def readCache(self, key: str, displayImage: int=0):
        """
        Read value from cache
        """
        data = self.client.get(key)
        if data == None:
            print("Key {} not found in cache".format(key))
        else:
            print("Key {} found in cache".format(key))
            if displayImage:
                image = Image.open(io.BytesIO(data))
                image.show()
        return data


    def delete(self, key: str):
        """
        Remove data from cache
        """
        success = self.client.delete(key, noreply=False)
        if success:
            print("Data was successfully removed from the cache (key={})".format(key))
        else:
            print("The given key does not match any of the cache's keys")

if __name__ == '__main__':

    ### MEMCACHE ###
    memory = Mem()
    # Read image file and display image with bytes
    data = memory.readFile("Images/pepe.png", 1)
    # Add data to the cache
    memory.create("pepe", data)
    # Read data from the cache and display image
    memory.readCache("pepe", 1)
    # Delete data from cache
    memory.delete("pepe")