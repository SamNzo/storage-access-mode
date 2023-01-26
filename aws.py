from boto.s3.connection import S3Connection
from dotenv import load_dotenv
from boto.s3.key import Key
from PIL import Image
import io
import os


class AWSS3:
    def __init__(self, accessKey: str, secretKey: str, hostname: str, bucketname: str):
        conn = S3Connection(accessKey, secretKey, host=hostname)
        self.bucket = conn.get_bucket(bucketname)
        self.S3Key = Key(self.bucket)
        
    def list(self):
        """
        List all keys from bucket
        """
        keys = self.bucket.get_all_keys()
        return keys

    def create(self, keyName: str, data):
        """
        Add data to bucket
        """
        self.S3Key.key = keyName
        obj = self.S3Key.set_contents_from_string(data, encrypt_key=True)
        return obj

    def read(self, filename: str, displayImage: int=0):
        """
        Read file and write its data in a byte array.
        To display byte data as image make displayImage argument equal 1
        """
        try:
            f = open("{}".format(filename), 'rb')
            data = f.read()
            f.close()
        except Exception as e:
            print(e)
            return

        if displayImage:
            image = Image.open(io.BytesIO(data))
            image.show()

        return data

    def readBucket(self, keyName: str, displayImage: int=0):
        """
        Read bucket key and write its data in a byte array.
        To display byte data as image make displayImage argument equal 1
        """
        try:
            self.S3Key.key = keyName
            obj = self.S3Key.get_contents_as_string()
            print("Data was successfully read from bucket " + self.bucket.name + " with key " + keyName)
        except Exception as e:
            print(e)
            return None

        if displayImage:
            image = Image.open(io.BytesIO(obj))
            image.show()

        return obj

    def delete(self, keyName: str):
        """
        Delete data from bucket
        """
        self.bucket.delete_key(keyName)

if __name__ == '__main__':

    # Get environment variables
    load_dotenv()
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_HOST = os.getenv("AWS_HOST")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

    # Connection
    aws = AWSS3(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_HOST, AWS_BUCKET_NAME)

    # List all bucket keys
    print("Keys from bucket " + aws.bucket.name + ":\n", aws.list())
    # Read file and display image
    data = aws.read("Images/Nautilus.jpg", 1)
    # Add previous data to bucket
    aws.create("le nautilus de alexis", data)
    # List all bucket keys again
    print("Keys from bucket " + aws.bucket.name + ":\n", aws.list())
    # Read from bucket
    aws.readBucket("le nautilus de alexis", 1)
    # Delete from bucket
    aws.delete("le nautilus de alexis")


    
