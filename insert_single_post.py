import redis
import datetime

# Ievieto vienu postu, lai parbauditu, ka post kartosana pec ievietosanas laika strada

# Savienojas ar DB
server = redis.Redis(host='localhost', port=6379, db=0)

author_ID = server.srandmember("AUTHOR_IDS").decode()

id = 9999

# Inicialize date objektu
x = datetime.datetime.now()

# Ievieto info "post" hash
server.hset("post:" + str(id), "post_ID", str(id))
server.hset("post:" + str(id), "author_ID", str(author_ID))
server.hset("post:" + str(id), "title", "TEST TITLE")
server.hset("post:" + str(id), "text", "TEST TEXT")

# Panem random topic no saraksta
server.hset("post:" + str(id), "topic", server.srandmember("topics", 1)[0].decode())
server.hset("post:" + str(id), "date", x.strftime("%c"))
server.hset("post:" + str(id), "timestamp", server.time()[0])

# Palielina autora "total_posts" par vienu
server.hincrby("author:" + str(author_ID), "total_posts", 1)

# Ievieto post ID kopa, kas uzglaba eksistejosos postus
server.sadd("POST_IDS", str(id))
