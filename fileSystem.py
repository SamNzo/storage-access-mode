from PIL import Image
import shutil
import io
import os

class Directory:
    def __init__(self, name: str):
        self.name = name
        self.path = "{}/{}".format(os.getcwd(), self.name)
        try:
            os.mkdir(self.path)
        except FileExistsError:
            print("An existing directory already has this name")
        except Exception as e:
            print(e)


    def listFiles(self):
        """
        List files in directory
        """
        files = os.listdir("{}".format(self.path))
        print("Files in directory {}:".format(self.name))
        for file in files:
            print(file)
        return files

    def createFile(self, filename: str, data):
        """
        Create file in directory with given data
        """
        try:
            f = open("{}/{}".format(self.path, filename), 'wb')
            f.write(data)
            print("File {} was successfully created".format(filename))
        except FileExistsError:
            print("An existing file already has this name")
        except Exception as e:
            print("haha")
            print(e)
        

    def readFile(self, filename: str, displayImage: bool=False):
        """
        Read file and write its data in a byte array.
        To display byte data as image make displayImage True
        """
        try:
            f = open("{}/{}".format(self.path, filename), 'rb')
            data = f.read()
            f.close()
            print("Data was successfully read from file " + filename)
        except Exception as e:
            print(e)
            return None

        if displayImage:
            image = Image.open(io.BytesIO(data))
            image.show()

        return data

    def deleteFile(self, filename: str):
        """
        Delete file from directory
        """
        try:
            os.remove("{}/{}".format(self.path, filename))
            print("File {} was successfully removed".format(filename))
        except Exception as e:
            print(e)

    def copyFile(self, sourcePath: str):
        """
        Copy file from source to directory
        """
        try:
            shutil.copy(sourcePath, "{}".format(self.path))
            print("File {} was successfully copied")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    
    ### FILE SYSTEM ###
    # Create directory
    directory = Directory("myDir")
    # Copy images into directory
    directory.copyFile("Images/mario.png")
    directory.copyFile("Images/yoshi.png")
    directory.copyFile("Images/peach.png")
    # List directory files
    directory.listFiles()
    # Read data from image and display it (0 for no display)
    bytes1 = directory.readFile("mario.png", displayImage=True)
    bytes2 = directory.readFile("yoshi.png", displayImage=True)
    bytes3 = directory.readFile("peach.png", displayImage=True)
    # Write data collected from previous readings into files
    directory.createFile("new_mario", bytes1)
    directory.createFile("new_yoshi", bytes2)
    directory.createFile("new_peach", bytes3)

