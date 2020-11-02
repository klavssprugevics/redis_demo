import redis


# Savienojas ar DB
server = redis.Redis(host='localhost', port=6379, db=0)

# =-=-=-=-=-=-= Atlasa autoru un vina postus =-=-=-=-=-=-=
def select_author_by_id(author_id, show_posts=False):

    author_id = str(author_id)
    author_ids = server.smembers("AUTHOR_IDS")

    # Parbauda vai autors eksiste
    if author_id.encode() not in author_ids:
        print("Author does not exist")
        return

    # Panem info no "author" hash
    author_username = server.hget("author:" + str(author_id), "username").decode()
    total_posts = server.hget("author:" + str(author_id), "total_posts").decode()

    # Panem info no "person" hash
    person_id = server.hget("author:" + str(author_id), "person_ID").decode()
    person_name = server.hget("person:" + str(person_id), "name").decode()
    person_surname = server.hget("person:" + str(person_id), "surname").decode()
    person_age = server.hget("person:" + str(person_id), "age").decode()

    # Attelo datus par author
    print("=====================================================")
    print("Author     :  ", person_name, " ", person_surname)
    print("Username   : ", author_username)
    print("Age        : ", person_age)
    print("Total posts: ", total_posts)
    print("=====================================================")

    # Ja grib attelot ari autora postus
    if show_posts:

        post_ids = server.smembers("POST_IDS")

        for id in post_ids:
            if server.hget("post:" + str(id.decode()), "author_ID").decode() == author_id:
                post_title = server.hget("post:" + str(id.decode()), "title").decode()
                post_topic = server.hget("post:" + str(id.decode()), "topic").decode()

                print("Title: ", post_title)
                print("Topic: ", post_topic)
                print("=====================================================")


# =-=-=-=-=-=-= Atlasa postus pie konkreta topic =-=-=-=-=-=-=
def select_posts_by_topic(topic):

    post_ids = server.smembers("POST_IDS")
    topics = server.smembers("topics")

    # Parbauda vai topic eksiste
    exists = False
    for element in topics:
        if element.decode() == topic:
            exists = True
            break

    if exists == False:
        print("Topic does not exist!")
        return

    # Atrod postus, kuriem sakrit topic un atlasa informaciju par tiem
    for id in post_ids:
        if server.hget("post:" + str(id.decode()), "topic").decode() == topic:

            post_title = server.hget("post:" + str(id.decode()), "title").decode()
            post_topic = server.hget("post:" + str(id.decode()), "topic").decode()
            post_text = server.hget("post:" + str(id.decode()), "text").decode()
            post_date = server.hget("post:" + str(id.decode()), "date").decode()
            post_author = server.hget("post:" + str(id.decode()), "author_ID").decode()

            # Atlasa personas info
            person_id = server.hget("author:" + str(post_author), "person_ID").decode()
            person_name = server.hget("person:" + str(person_id), "name").decode()
            person_surname = server.hget("person:" + str(person_id), "surname").decode()

            print("Title  : ", post_title)
            print("Author : ", person_name, " ", person_surname)
            print("Topic  : ", post_topic)
            print("Created: ", post_date)
            print("------------------------------------------------------")
            print(post_text)
            print("------------------------------------------------------")
            print("=====================================================")


# =-=-=-=-=-=-= Atlasa konkretu skaitu postus, sakartotus pec izveides laika =-=-=-=-=-=-=
def sort_posts_by_creation(count, newest=True):

    # Atlasa visus postus
    post_ids = server.smembers("POST_IDS")

    # Iegust visu postu timestamps
    timestamps = [int(server.hget("post:" + str(i.decode()), "timestamp").decode()) for i in post_ids]

    # Sakarto postus pec timestamps
    creation_order = [i for _, i in sorted(zip(timestamps, post_ids))]

    # Jo lielaks timestamp, jo velak izveidots -> Vajag dilstosa seciba
    if newest == True:
        creation_order = creation_order[::-1]

    # Izprinte jaunakos/vecakos postus
    for i in range(0, count):
        id = creation_order[i].decode()

        post_title = server.hget("post:" + str(id), "title").decode()
        post_topic = server.hget("post:" + str(id), "topic").decode()
        post_date = server.hget("post:" + str(id), "date").decode()
        post_author = server.hget("post:" + str(id), "author_ID").decode()

        # Atlasa personas info
        person_id = server.hget("author:" + str(post_author), "person_ID").decode()
        person_name = server.hget("person:" + str(person_id), "name").decode()
        person_surname = server.hget("person:" + str(person_id), "surname").decode()

        print("Title  : ", post_title)
        print("Topic  : ", post_topic)
        print("Author : ", person_name, " ", person_surname)
        print("Created: ", post_date)
        print("=====================================================")


# =-=-=-=-=-=-= Izvada autorus pec to "total_posts" skaita =-=-=-=-=-=-=
def sort_authors_by_posts(count):

    author_ids = server.smembers("AUTHOR_IDS")

    # Iegust visu visu autoru "total_posts"
    total_posts = [int(server.hget("author:" + str(i.decode()), "total_posts").decode()) for i in author_ids]

    # Sakarto autorus pec total_posts
    top_authors = [i for _, i in sorted(zip(total_posts, author_ids))]

    # Apmaina sarakstu, lai butu dilstosa seciba
    top_authors = top_authors[::-1]

    # Izdruka autorus
    for i in range(0, count):
        select_author_by_id(top_authors[i].decode())


select_author_by_id(3, show_posts=True)
# select_posts_by_topic("Sports")
# sort_posts_by_creation(3, True)
# sort_authors_by_posts(10)
