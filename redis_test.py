import redis
server = redis.Redis(host='localhost', port=6379, db=0)

# print(server.get("server:name").decode())

# Generate n number of random person and authors
# Generate topics
# Generator 500-1000 blog posts


print(server.hset("blog:1", "title", "hello"))
for id in range(0, 200):

    server.hset("author:"  + str(id), "name", "Janis")
    server.hset("author:"  + str(id), "surname", "Razna")
    server.hset("author:"  + str(id), "posts", 0)
