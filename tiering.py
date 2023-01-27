from fileSystem import Directory
from dotenv import load_dotenv
from memCache import Mem
from aws import AWSS3
import os

class Tiering:
    def __init__(self, dirName: str, accessKey: str, secretKey: str, hostname: str, bucketname: str):
        self.dir = Directory(dirName)
        self.aws = AWSS3(accessKey, secretKey, hostname, bucketname)
        self.mem = Mem()

    def create(self, cost: int, data, filename: str, AWSKeyname: str, cacheKey: str):
        """
        Add data to directory, aws bucket or cache depending on the cost parameter
        """
        if cost < 100:
            # Create on aws bucket
            self.aws.create(AWSKeyname, data)
        elif 100 <= cost < 1000:
            # Create in directory
            self.dir.createFile(filename, data)
        else:
            # Create in cache
            self.mem.create(cacheKey, data)

    def read(self, filename: str, AWSKeyname: str, cacheKey: str, displayImage: bool=False):
        """
        Read data from directory
        If error, try in cache
        If error, try in aws bucket
        """
        # Try in directory
        data = self.dir.readFile(filename, displayImage)
        if (data == None):
            # Try in cache
            print("An error occured while reading in directory")
            data = self.mem.readCache(cacheKey, displayImage)
            if (data == None):
                # Try in aws bucket
                print("An error occured while reading in cache")
                data = self.aws.readBucket(AWSKeyname, displayImage)
                if (data == None):
                    print("An error occured while reading in aws bucket")
        return data


    def delete(self, filename: str, AWSKeyname: str, cacheKey: str):
        """
        Delete data from directory, aws bucket & cache
        """
        self.aws.delete(AWSKeyname)
        self.dir.deleteFile(filename)
        self.mem.delete(cacheKey)

if __name__ == '__main__':

    # Get environment variables
    load_dotenv()
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_HOST = os.getenv("AWS_HOST")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")


    tiering = Tiering("myTieringDir", AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_HOST, AWS_BUCKET_NAME)
    # Copy image into directory
    tiering.dir.copyFile("Images/rick_roll.jpeg")
    # Get bytes
    data = tiering.dir.readFile("rick_roll.jpeg")
    # Add images to directory, cache & aws bucket
    tiering.create(500, data, "new_rick_roll.jpeg", "rick_roll_aws", "rick_roll") # dir
    tiering.create(2000, data, "new_rick_roll.jpeg", "rick_roll_aws", "rick_roll") # cache
    tiering.create(0, data, "new_rick_roll.jpeg", "rick_roll_aws", "rick_roll") # aws
    # Read data in directory
    tiering.read("rick_roll.jpeg", "rick_roll_aws", "rick_roll", displayImage=True)
    # Read data in cache
    tiering.read("test1.png", "rick_roll_aws", "rick_roll", displayImage=True)
    # Read data from aws bucket
    tiering.read("test2.png", "rick_roll_aws", "rick_roll_aws", displayImage=True)
    # Delete
    tiering.delete("new_rick_roll.jpeg", "rick_roll_aws", "rick_roll")