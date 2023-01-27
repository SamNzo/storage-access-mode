# Storage access modes - ENSTA 2023

The goal of this repository is to understand different access modes of data storage. This goes from RAM memory, to the cloud, to the file system. Each of the different types of storage offering different characteristics and constraints in terms of latency, bandwidth, robustness, security and cost.

## Usage
Clone repository
```
git clone https://github.com/SamNzo/storage-access-mode.git
```

Install python & pip
```
sudo apt update
sudo apt install python3
sudo apt install python3-pip
```

### Cache
Install [memcached](https://memcached.org/) & [pymemcached](https://pypi.org/project/pymemcache/) library.
```
sudo apt install memcached
pip install pymemcache
```

### AWS
Install [boto](https://pypi.org/project/boto/)
```
pip install boto
```

To connect to AWS an access & secret key are needed.
To keep those private, use [dotenv](https://pypi.org/project/python-dotenv/)
```
pip install python-dotenv
```

Create a **.env** file with the following content
```
AWS_ACCESS_KEY = "your aws access key"
AWS_SECRET_KEY = "your aws secret key"
AWS_HOST = "your aws host link"
AWS_BUCKET_NAME = "your bucket name"`
```