import redis
server = redis.Redis(host='localhost', port=6379, db=0)


def select_author(author_id, formatted=True):
    person_id = server.hget("author:" + str(author_id), "person")
    print(person_id)




select_author(10)
