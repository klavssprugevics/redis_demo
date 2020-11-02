import redis


# Savienojas ar DB
server = redis.Redis(host='localhost', port=6379, db=0)

# =-=-=-=-=-=-= Dzes post pec id =-=-=-=-=-=-=
def delete_post(post_id):

    post_id = str(post_id)
    all_posts = server.smembers("POST_IDS")

    if post_id.encode() not in all_posts:
        print("Post does not exist")
        return

    # Atjauno index set
    server.srem("POST_IDS", post_id)

    # Autoram nonem -1 total_posts
    author_id = server.hget("post:" + post_id, "author_ID")
    server.hincrby("author:" + str(author_id.decode()), "total_posts", -1)

    # Izdzes post
    server.delete("post:" + post_id)


# =-=-=-=-=-=-= Dzes autoru pec id =-=-=-=-=-=-=
def delete_author(author_id, delete_posts=True):

    author_id = str(author_id)
    all_authors = server.smembers("AUTHOR_IDS")

    if author_id.encode() not in all_authors:
        print("Author does not exist")
        return

    # Atjauno index set
    server.srem("AUTHOR_IDS", author_id)

    # Dzes autora postus
    if delete_posts:

        all_posts = server.smembers("POST_IDS")
        post_counter = 0
        for posts in all_posts:

            posts = posts.decode()
            post_author = server.hget("post:" + str(posts), "author_ID")

            if post_author.decode() == author_id:
                server.delete("post:" + str(posts))
                post_counter += 1

        print("Deleted ", post_counter, " user posts.")

    # Dzes personas datus
    person_id = server.hget("author:" + author_id, "person_ID").decode()
    server.delete("person:" + str(person_id))

    # Dzes autoru datus
    server.delete("author:" + str(author_id))

# =-=-=-=-=-=-= Dzes topic =-=-=-=-=-=-=
def delete_topic(topic):

    # Parbauda vai eksiste
    topics = server.smembers("topics")
    exists = False

    for element in topics:
        if element.decode() == topic:
            exists = True
            break

    if exists == False:
        print("Topic does not exist!")
        return


    post_ids = server.smembers("POST_IDS")

    # Dzes postus, kas pieder pie topic
    delete_counter = 0
    for id in post_ids:
        if server.hget("post:" + str(id.decode()), "topic").decode() == topic:

            # Autora total_post  -1
            post_author = server.hget("post:" + str(id.decode()), "author_ID")
            server.hincrby("author:" + str(post_author.decode()), "total_posts", -1)

            # Dzes post
            server.delete("post:" + str(id.decode()))
            delete_counter += 1

    print("Deleted ", delete_counter, " posts on topic: ", topic)

    # Dzes topic
    server.srem("topics", topic)


delete_post(50)
# delete_author(3, delete_posts=True)
# delete_topic("Sports")
