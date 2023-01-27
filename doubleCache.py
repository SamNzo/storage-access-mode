from fileSystemLRU import DirectoryLRU
from linkedList import LinkedList
from dotenv import load_dotenv
from memLRU import MemLRU
from aws import AWSS3
import os

class doubleCache:
    """
    Represents a 3 levels cache system.
    [Memcache] - [File system] - [Cloud AWS S3]
    """
    def __init__(self, dirname: str, n1: int, m1: int, n2: int, m2: int, accessKey: str, secretKey: str, hostname: str, bucketname: str):
        if not n2 > n1 > m2 > m1:
            print("Invalid set of parameters.\nPlease re-arrange it so n2 > n1 > m2 > m1")
            return
        self.dirLRU = DirectoryLRU(dirname, n2, m2)
        self.memLRU = MemLRU(n1, m1)
        self.aws = AWSS3(accessKey, secretKey, hostname, bucketname)

    def create(self, data, filename: str, keyname: str):
        """
        Add data to cache & directory & aws
        """
        self.dirLRU.createFile(filename, data)
        self.memLRU.create(keyname, data)
        self.aws.create(keyname, data)

    def read(self, filename: str, keyname: str, displayImage: bool=False):
        """
        Read file from cache.
        If error, read from directory.
        If error, read from cloud.
        When the data is found it is put in the levels missing it.
        """
        try:
            data = self.memLRU.readCache(keyname, displayImage)
            if data == None:
                print("An error occurred while reading data from cache")
                data = self.dirLRU.readFile(filename, displayImage)
                if data != None:
                    print("Data was successfully read from cache")
                    self.memLRU.create(keyname, data)
                    return data
                else:
                    print("An error occurred while reading data from directory")
                    data = self.aws.readBucket(keyname, displayImage)
                    if data == None:
                        print("An error occurred while reading data from aws bucket")
                    else:
                        print("Data was successfully read from aws bucket")
                        self.memLRU.create(keyname, data)
                        self.dirLRU.createFile(filename, data)
                    return data
            print("Data was successfully read from cache")
            return data
        except Exception as e:
            print(e)
            return None

    def delete(self, filename: str, keyname: str):
        """
        Delete data from directory & aws
        """
        self.dirLRU.deleteFile(filename)
        self.memLRU.delete(keyname)
        self.aws.delete(keyname)


if __name__ == "__main__":
    
    # Get environment variables
    load_dotenv()
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_HOST = os.getenv("AWS_HOST")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

    double_cache = doubleCache("myDoubleCacheDir", 8, 2, 12, 4, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_HOST, AWS_BUCKET_NAME)

    # Add a file in cache
    data_cache = double_cache.memLRU.readFile("Images/pepe.png", displayImage=True)
    double_cache.memLRU.create("mykey", data_cache)
    # Read file and display image
    data_aws = double_cache.aws.read("Images/Nautilus.jpg", displayImage=True)
    # Add previous data to bucket
    double_cache.aws.create("le_nautilus_de_alexis", data_aws)
    # Try with error to check if read method works (test.png does not exit in the directory)
    data_from_bucket = double_cache.read("test.png", "le_nautilus_de_alexis", displayImage=True)
    # Try again with error but this time for a file only in cache
    data_from_bucket = double_cache.read("test2.png", "mykey", displayImage=True)





