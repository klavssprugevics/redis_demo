import redis
import random


# Savienojas ar DB
server = redis.Redis(host='localhost', port=6379, db=0)

# =-=-=-=-=-=-= Izmaina post nosaukumu =-=-=-=-=-=-=
def change_post_title(count):

    # Izvelas nejausus postus
    posts_ID = server.srandmember("POST_IDS", count)

    print("=====================================================")
    print("EDIT#1: CHANGE POST TITLE")
    print("Titles before: ")
    print("=====================================================")

    # Postu nosaukumus uzliek visus ar lielo burtu.
    for post in posts_ID:

        # Iegust pasreizejo nosaukumu
        title = server.hget("post:" + str(post.decode()), "title")

        # Paskatas vai post eksiste
        if title == None:
            continue
        else:
            title = title.decode()
            print(title)

            # Nomaina nosaukumu
            server.hset("post:" + str(post), "title", title.upper())

            # Atjauno timestamp
            server.hset("post:" + str(post), "timestamp", server.time()[0])

    print("=====================================================")
    print("Post IDs: ", end="")
    print([id for id in posts_ID])
    print("Titles after: ")
    print("=====================================================")

    # Parbauda vai izmainiti nosaukumi
    for post in posts_ID:
        print(server.hget("post:" + str(post), "title").decode())


# =-=-=-=-=-=-= Izmaina autora username =-=-=-=-=-=-=
def change_author_username(count):

    # Izvelas nejausus autorus
    authors_ID = server.srandmember("AUTHOR_IDS", count)

    print("=====================================================")
    print("EDIT#2: CHANGE USERNAME")
    print("Usernames before: ")
    print("=====================================================")

    for author in authors_ID:

        # Panem pasreizejo username
        username = server.hget("author:" + str(author.decode()), "username")

        # Parbauda vai autors eksiste
        if username == None:
            continue
        else:
            username = username.decode()
            print(username)

            # Izmaina username
            server.hset("author:" + str(author), "username", username.upper())

    print("=====================================================")
    print("Author IDs: ", end="")
    print([id for id in authors_ID])
    print("Usernames after: ")
    print("=====================================================")

    # Check if username changed.
    for author in authors_ID:
        print(server.hget("author:" + str(author), "username").decode())


# =-=-=-=-=-=-= Izmaina topic nosaukumu un visus postus, kas pieder sim topic =-=-=-=-=-=-=
def change_topic_name(old_topic, new_topic):

    print("=====================================================")
    print("EDIT#3: CHANGE Topic name")
    print("Old topic name:", old_topic)
    print("=====================================================")

    # Parbauda vai topic eksiste
    if server.sismember("topics", old_topic):

        # Izdzes veco
        server.srem("topics", old_topic)

        # Pievieno jauno
        server.sadd("topics", new_topic)

        post_ids = server.smembers("POST_IDS")

        # Apskata visus post un nomaina topic, kuriem bija vecais topic
        for id in post_ids:
            if server.hget("post:" + str(id.decode()), "topic").decode() == old_topic:
                server.hset("post:" + str(id.decode()), "topic", new_topic)

    else:
        print("Topic doesn't exist")


change_post_title(10)
change_author_username(10)
change_topic_name("Sports", "Sports and Fitness")
