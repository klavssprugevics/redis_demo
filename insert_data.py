import redis
import csv
import random
import datetime
server = redis.Redis(host='localhost', port=6379, db=0)

# Izdesh visu
server.flushall()

# Izveido un ievieto "Person" hashus
# Nolasa vardu/uzvardu no .csv
with open("data//names.csv") as names_file:
    id = 1
    names = csv.reader(names_file, delimiter=',')
    for person in names:
        age = random.randint(13, 99)

        # Uzgenere random telefona numuru
        phone = [random.randint(0, 9) for i in range(8)]
        phone[0] = 2
        phone = ''.join(str(digit) for digit in phone)

        server.hset("person:"  + str(id), "name", person[0])
        server.hset("person:"  + str(id), "surname", person[1])
        server.hset("person:"  + str(id), "age", age)
        server.hset("person:"  + str(id), "phone", phone)

        id += 1

# Katrai personai izveidos random author hash
author_ids = [i for i in range(1, 51)]
random.shuffle(author_ids)

# Izveido "Author" hashus
for i in range(0, len(author_ids)):

    person_ID = author_ids[i]
    # Panem vardu no Person
    name = server.hget("person:" + str(person_ID), "name")

    # Izveido random username
    username = name.decode() + str(random.randint(1, 999))

    # Izveido random paroles, parveidojot random int uz ASCII
    sequence = [random.randint(65, 120) for i in range(8)]
    password = ''.join(chr(letter) for letter in sequence)

    server.hset("author:"  + str(i + 1), "author_ID", str(i + 1))
    server.hset("author:"  + str(i + 1), "person_ID", person_ID)
    server.hset("author:"  + str(i + 1), "username", username)
    server.hset("author:"  + str(i + 1), "password", password)
    server.hset("author:"  + str(i + 1), "total_posts", 0)

    # Ievieto Autora ID seta, kas uzglabas eksistejosos autorus
    server.sadd("AUTHOR_IDS", str(i + 1))

# Izveido "Topics" kopu
server.sadd("topics", "Technology")
server.sadd("topics", "Data structures")
server.sadd("topics", "Politics")
server.sadd("topics", "Environment")
server.sadd("topics", "News")
server.sadd("topics", "Sports")

# Atlasa random elementu no lista
# print(server.srandmember("topics", 1)[0].decode())

# Nolasa title nosaukumus no faila
title_list = []
with open("data//titles.csv") as titles_file:
    titles = csv.reader(titles_file, delimiter=',')
    for item in titles:
        title_list.append(item[0])

# Sajauc title sarakstu
random.shuffle(title_list)

# Inicialize date objektu
x = datetime.datetime.now()


# Nolasa dummy tekstus no faila
with open("data//text.csv") as text_file:
    id = 1
    text = csv.reader(text_file, delimiter=',')

    for item in text:

        # Izvelas random author
        author_ID = random.randint(1, 50)

        server.hset("post:" + str(id), "post_ID", str(id))
        server.hset("post:" + str(id), "author_ID", str(author_ID))
        server.hset("post:" + str(id), "title", title_list[id - 1])
        server.hset("post:" + str(id), "text", item[0])

        # Panem random topic no saraksta
        server.hset("post:" + str(id), "topic", server.srandmember("topics", 1)[0].decode())
        server.hset("post:" + str(id), "date", x.strftime("%c"))
        server.hset("post:" + str(id), "timestamp", server.time()[0])

        # Palielina author total posts par vienu
        server.hincrby("author:" + str(author_ID), "total_posts", 1)

        # Ievieto post ID seta, kas uzglabas eksistejosos postus
        server.sadd("POST_IDS", str(id))
        id += 1
