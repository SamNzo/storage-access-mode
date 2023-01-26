from pymemcache.client.base import Client
import random
import json
import time

# Don't forget to run `memcached' before running this next line:
client = Client(('localhost', 11211))

# Once the client is instantiated, you can access the cache:
client.set(json.dumps(5), 6)

def f(x: int) -> int:
    time.sleep(0.5)
    return x+1

def fc(x: int):
    print(x)
    res = client.get(json.dumps(x))
    if res == None:
        print("Key {} not found in cache".format(str(x)))
        value = f(x)
        client.set(json.dumps(x), value)
        print("key: {}, value: {} was added to cache".format(str(x), str(value)))
        return value
    else:
        print("Key {} found in cache".format(str(x)))
        return json.loads(res)


if __name__ == '__main__':

    n = input("How many requests do you want?")
    for i in range(int(n)):
        rand = random.randint(0, 100)
        t1 = time.time()
        fc(int(rand))
        t2= time.time()
        print("Execution time: {}".format(str(t2 - t1)))
