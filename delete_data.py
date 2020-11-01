import redis
server = redis.Redis(host='localhost', port=6379, db=0)


def delete_post(post_id):
    post_id = str(post_id)
    all_posts = server.smembers("POST_IDS")

    if post_id.encode() not in all_posts:
        print("Post does not exist")
        return

    # Atjauno index set
    server.srem("POST_IDS", post_id)

    # Autoram nonem -1 postu
    author_id = server.hget("post:" + post_id, "author_ID")

    server.hincrby("author:" + str(author_id.decode()), "total_posts", -1)

    # Izdzes post
    server.delete("post:" + post_id)

def delete_author(author_id, delete_posts=True):
    author_id = str(author_id)
    all_authors = server.smembers("AUTHOR_IDS")

    if author_id.encode() not in all_authors:
        print("Author does not exist")
        return

    # Atjauno index set
    server.srem("AUTHOR_IDS", author_id)

    if delete_posts:
        # Izdes author posts
        all_posts = server.smembers("POST_IDS")
        post_counter = 0
        for posts in all_posts:
            posts = posts.decode()

            post_author = server.hget("post:" + str(posts), "author_ID")

            if post_author.decode() == author_id:
                server.delete("post:" + str(posts))
                post_counter += 1


        print("Deleted ", post_counter, " user posts.")

    # Izdesh person data
    person_id = server.hget("author:" + author_id, "person_ID").decode()
    server.delete("person:" + str(person_id))

    # Izdesh author data
    server.delete("author:" + str(author_id))


def delete_topic(topic):

    # Check if topic exists first
    topics = server.smembers("topics")
    exists = False
    # Check if topic exists
    for element in topics:
        if element.decode() == topic:
            exists = True
            break

    if exists == False:
        print("Topic does not exist!")
        return

    post_ids = server.smembers("POST_IDS")

    delete_counter = 0
    # Delete posts that contain the topic
    for id in post_ids:
        if server.hget("post:" + str(id.decode()), "topic").decode() == topic:

            # Author total_post count -1
            post_author = server.hget("post:" + str(id.decode()), "author_ID")
            server.hincrby("author:" + str(post_author.decode()), "total_posts", -1)

            # Izdesh post
            server.delete("post:" + str(id.decode()))

            delete_counter += 1

    print("Deleted ", delete_counter, " posts on topic: ", topic)

    # Delete topic
    server.srem("topics", topic)


# delete_post(1)
# delete_author(3, delete_posts=True)
delete_topic("Sports")
