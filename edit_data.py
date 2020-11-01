import redis
import random

server = redis.Redis(host='localhost', port=6379, db=0)


# =-=-=-=-=-=-= Change post title =-=-=-=-=-=-=
# Select 15 random post id to change title.
posts_ID = [random.randint(1, 1500) for i in range(15)]


print("=====================================================")
print("EDIT#1: CHANGE POST TITLE")
print("Titles before: ")
print("=====================================================")

# Set title name to all caps.
for post in posts_ID:

    title = server.hget("post:" + str(post), "title")
    print(title)
    # Check if post exists first.
    if title == None:
        continue
    else:
        title = title.decode()
        server.hset("post:" + str(post), "title", title.upper())

        # Update timestamp
        server.hset("post:" + str(post), "timestamp", server.time()[0])

print("=====================================================")
print("Post IDs: ", end="")
print([id for id in posts_ID])
print("Titles after: ")
print("=====================================================")

# Check if title changed.
for post in posts_ID:
    print(server.hget("post:" + str(post), "title"))


# =-=-=-=-=-=-= Change username =-=-=-=-=-=-=
# Select 15 random author ids to change username.
authors_ID = [random.randint(1, 100) for i in range(15)]

print("=====================================================")
print("EDIT#2: CHANGE USERNAME")
print("Usernames before: ")
print("=====================================================")
for author in authors_ID:

    username = server.hget("author:" + str(author), "username")
    print(username)
    # Check if user exists first.
    if username == None:
        continue
    else:
        username = username.decode()
        server.hset("author:" + str(author), "username", username.upper())

print("=====================================================")
print("Author IDs: ", end="")
print([id for id in authors_ID])
print("usernames after: ")
print("=====================================================")

# Check if username changed.
for author in authors_ID:
    print(server.hget("author:" + str(author), "username"))


# =-=-=-=-=-=-= Change topic name and corresponding post titles =-=-=-=-=-=-=

old_topic = "Sports"
print("=====================================================")
print("EDIT3: CHANGE Topic name")
print("Old topic name:", old_topic)
print("=====================================================")

# Check if topic exists
if server.sismember("topics", old_topic):
    new_topic = old_topic + " and Fitness"

    # Delete old topic
    server.srem("topics", old_topic)

    # Add new topic
    server.sadd("topics", new_topic)

    post_ids = server.smembers("POST_IDS")
    
    # Iterate all posts and update topic
    for id in post_ids:
        if server.hget("post:" + str(id.decode()), "topic").decode() == old_topic:
            server.hset("post:" + str(id.decode()), "topic", new_topic)

else:
    print("Topic doesn't exist")
