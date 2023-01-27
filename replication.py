from fileSystem import Directory
from dotenv import load_dotenv
from aws import AWSS3
import os

class Replication:
    def __init__(self, dirName: str, accessKey: str, secretKey: str, hostname: str, bucketname: str):
        self.dir = Directory(dirName)
        self.aws = AWSS3(accessKey, secretKey, hostname, bucketname)

    def create(self, data, filename: str, keyname: str):
        """
        Add data to directory & aws
        """
        self.dir.createFile(filename, data)
        self.aws.create(keyname, data)

    def read(self, filename: str, keyname: str, displayImage: bool=False):
        """
        Read file from directory
        If error, read from aws and put data in directory
        """
        try:
            data = self.dir.readFile(filename, displayImage)
            if data == None:
                print("An error occurred while reading directory data")
                data_from_bucket = self.aws.readBucket(keyname, displayImage)
                if data_from_bucket != None:
                    print("Data was successfully fetched from aws bucket")
                    self.dir.createFile(filename, data_from_bucket)
                    return data_from_bucket
                print("An error occured while reading bucket data")
                return
            print("Data was successfully read from directory")
        except Exception as e:
            print(e)
        return data
            

    def delete(self, filename: str, keyname: str):
        """
        Delete data from directory & aws
        """
        self.dir.deleteFile(filename)
        self.aws.delete(keyname)

if __name__ == '__main__':

    # Get environment variables
    load_dotenv()
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_HOST = os.getenv("AWS_HOST")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

    # Connection
    replication = Replication("myReplicaDir", AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_HOST, AWS_BUCKET_NAME)

    # Copy image in new directory
    replication.dir.copyFile("Images/toed.png")
    # Read file from directory (or bucket if error)
    data = replication.read("toed.png", "toed de Delphine", displayImage=True)
    # Try with error to check if read method works (blabla does not exit in the directory and sousou.png is a key in the bucket)
    data_from_bucket = replication.read("test.png", "sousou.png", displayImage=True)
    # Display the data copied from aws bucket into directory
    replication.dir.readFile("test.png", displayImage=True)
    # Add previous data to directory & aws bucket
    replication.create(data, "myNewToed.png", "2e toed de Delphine")
    # Display all keys
    print(replication.aws.list())
    # Remove data from directory & aws bucket
    replication.delete("myNewToed.png", "2e toed de Delphine")