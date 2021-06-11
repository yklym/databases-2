from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(self):
        self.driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))

    def close(self):
        self.__driver.close()

    def sign_in(self, redis_id):
        with self.__driver.session() as session:
            session.run("MATCH (u:user {redis_id: $redis_id}) SET u.online = true", redis_id=redis_id)

    def sign_out(self, redis_id):
        with self.__driver.session() as session:
            session.run("MATCH (u:user {redis_id: $redis_id}) SET u.online = false", redis_id=redis_id)

    def register_user(self, username):
        with self.driver.session() as session:
            session.write_transaction(self.__register_user, username)

            existing_users = tx.run('MATCH (user:User {username: $username}) RETURN user', username=username)

            for val in existing_users:
                existing_username = val['user']['username']
                print(f'REGISTER USER: {existing_username}, {username}')

                if existing_username == username:
                    print(f'USERNAME {username} already exists')
                    return

            session.run(
                "MERGE (user:User {username: $username})",
                username=username
            )

    def add_message(self, message_dict):
        with self.driver.session() as session:
            tags = message_dict['tags'].split(',')
            query = "CREATE (msg:Message {id: $id})\n"

            for idx, tag in enumerate(tags):
                if tag != '' and tag is not None:
                    query += f"MERGE (tag{idx}:Tag {{ name: '{tag}' }})\n" + f"CREATE (msg)-[:HAS_TAG]->(tag{idx})"

            after_query = "MERGE (sender:User {username: $senderName})\n" + \
                          "MERGE (receiver:User {username: $receiverName})\n" + \
                          "MERGE (sender)-[:SENT {to: $receiverName}]->(msg)\n" + \
                          "MERGE (msg)-[:TO {from: $senderName}]->(receiver)\n"

            print('EXCECUTING QUERY:\n' + query + after_query + '\n')

            session.run(
                query + after_query,
                id=message_dict['id'],
                senderName=message_dict['sender-name'],
                receiverName=message_dict['receiver-name']
            )

    def create_message(self, sender_id, consumer_id, message: dict):
        with self.__driver.session() as session:
            try:
                messages_id = session.write_transaction(self.__create_message_as_relation, int(sender_id),
                                                        int(consumer_id), message["id"])
                for tag in message["tags"]:
                    session.write_transaction(self.add_tag, messages_id, tag)
            except Exception as e:
                print(str(e))

    def add_tag(self, tx, messages_id, tag):
        tx.run("MATCH ()-[r]-() where ID(r) = $messages_id "
               "FOREACH(x in CASE WHEN $tag in r.tags THEN [] ELSE [1] END | "
               "SET r.tags = coalesce(r.tags,[]) + $tag)", messages_id=messages_id, tag=tag)

    def deliver_message(self, redis_id):
        with self.__driver.session() as session:
            session.run("MATCH (m:messages {redis_id: $redis_id }) SET m.delivered = true", redis_id=redis_id)

    def mark_as_spam(self, redis_id):
        with self.__driver.session() as session:
            session.run("MATCH (u1:user)-[r:messages]->(u2:user) "
                        "WHERE $redis_id IN r.all AND NOT $redis_id IN r.spam "
                        "SET r.spam = r.spam + $redis_id", redis_id=redis_id)

    def get_users_by_tag(self, tags):
        return self.__record_to_list(self.__get_users_by_tag(tags), 'name')

    def users_with_tagged_unrelated(self, tags):
        list_of_names = self.__record_to_list(self.__get_users_by_tag(tags), 'name')
        unrelated_users = []
        for name1 in list_of_names:
            group = [name1]
            for name2 in list_of_names:
                if name1 != name2:
                    res = self.__check_relation_between_users(name1, name2)
                    if not res and name1 not in group:
                        group.append(name2)
            unrelated_users.append(group)
        return unrelated_users

    def __get_users_by_tag(self, tags):
        with self.__driver.session() as session:
            tags = tags.split(", ")
            for tag in tags:
                if not Tag.has_member(tag):
                    raise ValueError(f"Tag: {tag} doesnt exist")
            query = "MATCH (u:user)-[r:messages]-() WHERE"
            for tag in tags:
                query += f" \'{tag}\' IN r.tags AND"
            # removing last AND
            query = query[:-3] + "RETURN u"
            return session.run(query)

    def __check_relation_between_users(self, first_user, second_user):
        with self.__driver.session() as session:
            res = session.run("MATCH  (u1:user {name: $first_user}), (u2:user {name: $second_user}) "
                              "RETURN EXISTS((u1)-[:messages]-(u2))", first_user=first_user, second_user=second_user)
            return res.single()[0]

    def way_by_users(self, first_user, second_user):
        users = self.get_users()
        if first_user not in users or second_user not in users:
            raise ValueError('Invalid users names')
        with self.__driver.session() as session:
            shortest_path = session.run("MATCH p = shortestPath((u1:user)-[*..10]-(u2:user)) "
                                        "WHERE u1.name = $first_user AND u2.name = $second_user "
                                        "RETURN p", first_user=first_user, second_user=second_user)
            if shortest_path.peek() is None:
                raise Exception(f"Way between {first_user} and {second_user} doesnt exist")
            for record in shortest_path:
                nodes = record[0].nodes
                path = []
                for node in nodes:
                    path.append(node._properties['name'])
                return path

    def users_by_relation(self, n):
        with self.__driver.session() as session:
            res = session.run(f"MATCH p = (u1:user)-[*]-(u2:user)"
                              f"WHERE u1 <> u2 AND "
                              f"reduce(total_len = 0, r IN relationships(p)| total_len + size(r.all)) = {n} "
                              f"RETURN u1, u2")
            return self.__pair_record_to_list(res, 'name')

    def get_users_by_spam(self):
        with self.__driver.session() as session:
            res = session.run("MATCH p = (u1:user)-[]-(u2:user)"
                              "WHERE u1 <> u2 AND all(x in relationships(p) WHERE x.all = x.spam)"
                              "RETURN u1, u2")
            return self.__pair_record_to_list(res, 'name')

    def __pair_record_to_list(self, res, pull_out_value):
        my_list = list(res)
        my_list = list(dict.fromkeys(my_list))
        new_list = []
        for el in my_list:
            list_el = list(el)
            if list_el not in new_list and list_el[::-1] not in new_list:
                new_list.append(el)
        return [[el[0]._properties[pull_out_value], el[1]._properties[pull_out_value]] for el in new_list]

    def get_users(self):
        with self.__driver.session() as session:
            res = session.run("MATCH (u:user) RETURN u")
            return self.__record_to_list(res, 'name')

    def __record_to_list(self, res, pull_out_value):
        my_list = list(res)
        my_list = list(dict.fromkeys(my_list))
        return [el[0]._properties[pull_out_value] for el in my_list]


neo = Neo4jConnection()
