import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import Person, Post, Comment

tested_app.config.from_object(TestConfig)


class Test(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Person(id=1, name="Alice"))
        self.db.session.add(Person(id=2, name="Bob"))
        self.db.session.add(Post(user_id=1, content="You suck!"))
        self.db.session.add(Post(user_id=2, content="What time will you be there?"))
        self.db.session.add(Comment(post_id=1, commenter_id=2, comment="No, you suck!"))
        # self.db.session.commit()
        # self.app = tested_app.test_client()
        try:
            self.db.session.commit()
        except:
            self.db.session.close()
        finally:
            self.app = tested_app.test_client()

    def testA_put_person_without_id(self):
        # do we really need to check counts?
        initial_count = Person.query.filter_by(name="Manuel").count()

        # send the request and check the response status code
        response = self.app.put("/person", data={"name": "Manuel"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Person.query.filter_by(name="Manuel").count()
        self.assertEqual(updated_count, initial_count+1)

    def testB_get_all_person(self):
        # send the request and check the response status code
        response = self.app.get("/person")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        person_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(person_list), list)
        self.assertDictEqual(person_list[0], {"id": "1", "name": "Alice"})
        self.assertDictEqual(person_list[1], {"id": "2", "name": "Bob"})
        self.assertDictEqual(person_list[2], {"id": "3", "name": "Manuel"})

    def testC_get_person_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/person/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        person = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(person, {"id": "1", "name": "Alice"})

    def testD_get_person_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/person/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this person id."})

    def testE_new_post_valid_user_id(self):
        response = self.app.post("/post", data={"user_id": "3", "content": "Hello World!"})
        self.assertEqual(response.status_code, 200)
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

    def testF_new_post_invalid_user_id(self):
        response = self.app.post("/post", data={"user_id": "5", "content": "Blablabla"})
        self.assertEqual(response.status_code, 403)
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 403, "msg": "Cannot put post. User does not exist."})

    def testG_get_post_by_id(self):
        response = self.app.get("/post/3")
        self.assertEqual(response.status_code, 200)
        post = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(post, {"post_id": "3", "user_id": "3", "content": "Hello World!"})

    def testH_add_comment_valid_id(self):
        response = self.app.post("/comment", data={"post_id": "2", "commenter_id": "3", "comment": "I'll be there at 8."})
        self.assertEqual(response.status_code, 200)
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

    def testI_add_comment_invalid_post(self):
        response = self.app.post("comment", data={"post_id": "4", "commenter_id": "2", "comment": "ABCDEFG"})
        self.assertEqual(response.status_code, 403)
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 403, "msg": "Cannot comment on post. Post does not exist."})

    def testJ_delete_post_valid_id(self):
        response = self.app.delete("/post/1")
        self.assertEqual(response.status_code, 200)
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

    def testK_get_all_post(self):
        response = self.app.get("/post")
        self.assertEqual(response.status_code, 200)
        post_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(post_list), list)
        self.assertDictEqual(post_list[0], {"post_id": "2", "user_id": "2", "content": "What time will you be there?"})
        self.assertDictEqual(post_list[1], {"post_id": "3", "user_id": "3", "content": "Hello World!"})

    def testL_delete_post_invalid_id(self):
        response = self.app.delete("post/4")
        self.assertEqual(response.status_code, 403)
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 403, "msg": "Post does not exist."})
