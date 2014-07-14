#!/usr/bin/env python
#-*- coding: utf-8 -*-

from base64 import b64encode
import unittest
import server
import shutil
import string
import random
import json
import sys
import os

from server import _API_PREFIX

TEST_DIRECTORY = "test_users_dirs/"
TEST_USER_DATA = "test_user_data.json"

DEMO_USER = "i_am_an_user@rawbox.it"
DEMO_PSW = "very_secret_password"
DEMO_FAKE_USER = "fake_usr"
DEMO_CLIENT = None

SHARE_CLIENTS = []

DEMO_FILE = "somefile.txt"
DEMO_CONTENT = "Hello my dear,\nit's a beautiful day here in Compiobbi."
DEMO_DEST_COPY_PATH = "new_cp"
DEMO_DEST_MOVE_PATH = "new_mv"
NO_SERVER_PATH = "marcoRegna"


def make_headers(user, psw):
    return {
        "Authorization": "Basic "
        + b64encode("{0}:{1}".format(user, psw))
    }


# def transfer(path, flag=True, test=True):
#     client_path, server_path = set_tmp_params(path)
#     if flag:
#         func = "copy"
#         new_path = "{}/{}".format(DEMO_DEST_COPY_PATH, path)
#     else:
#         func = "move"
#         new_path = "{}/{}".format(DEMO_DEST_MOVE_PATH, path)

#     if test:
#         data = {
#             "file_src": client_path,
#             "file_dest": os.path.join(new_path, DEMO_FILE)
#         }
#         rv = DEMO_CLIENT.call("post", "actions/" + func, data)
#     else:
#         data = {
#             "file_src": NO_SERVER_PATH,
#             "file_dest": os.path.join(new_path, DEMO_FILE)
#         }
#         rv = DEMO_CLIENT.call("post", "actions/" + func, data)

#     return rv, client_path, server_path


# def set_tmp_params(father_dir):
#     ''' Add a file in user's directory, in the path passed in argument
#     Please, use path here with only a word (not "dir/subdir") '''
#     client_path = os.path.join(father_dir, DEMO_FILE)
#     server_path = os.path.join(TEST_DIRECTORY, DEMO_USER, client_path)
#     os.makedirs(os.path.dirname(server_path))
#     shutil.copy(DEMO_FILE, server_path)

#     server_father_path = os.path.join(TEST_DIRECTORY, DEMO_USER, father_dir)
#     u = server.User.users[DEMO_USER]
#     u.paths[father_dir] = [server_father_path, 0, False]
#     u.paths[client_path] = [server_path, 0, 0]

#     return client_path, server_path


# class TestClient(object):

#     def __init__(self, user, psw):
#         self.user = user
#         self.psw = psw
#         self.headers = {
#             "Authorization": "Basic "
#             + b64encode("{0}:{1}".format(user, psw))
#         }
#         self.tc = server.app.test_client()
#         self.VERBS = {
#             "post": self.tc.post,
#             "get": self.tc.get,
#             "put": self.tc.put,
#             "delete": self.tc.delete
#         }

#     def call(self, HTTP_verb, url, data=None, auth=True):
#         return self.VERBS[HTTP_verb](server._API_PREFIX + url,
#                                      data=data,
#                                      headers=self.headers if auth else None)

#     def create_demo_user(self, flag=False):
#         usr = "user"
#         psw = "psw"
#         if flag:
#             usr = "fake_usr"
#             psw = "fake_psw"

#         data = {
#             usr: self.user,
#             psw: self.psw
#         }
#         return self.call("post", "create_user", data, auth=False)

#     def set_fake_usr(self, flag=False):
#         self.headers["Authorization"] = "".join((
#             "Basic ",
#             b64encode("{0}:{1}".format(
#                 DEMO_FAKE_USER if flag else self.user,
#                 self.psw
#             ))
#         ))


# class TestSequenceFunctions(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         # set a test "USERS_DIRECTORIES"
#         try:
#             os.mkdir(TEST_DIRECTORY)
#         except OSError:
#             shutil.rmtree(TEST_DIRECTORY)
#             os.mkdir(TEST_DIRECTORY)

#         server.USERS_DIRECTORIES = TEST_DIRECTORY
#         # set a test "USER_DATA" json
#         open(TEST_USER_DATA, "w").close()
#         server.USERS_DATA = TEST_USER_DATA

#         # demo user configuration
#         global DEMO_CLIENT
#         DEMO_CLIENT = TestClient(DEMO_USER, DEMO_PSW)
#         DEMO_CLIENT.create_demo_user()
#         with open(DEMO_FILE, "w") as f:
#             f.write(DEMO_CONTENT)

#         # create some clients for share tests
#         for i in range(5):
#             random.seed(i)
#             user = "".join(random.sample(string.letters, 7) +
#                            ["@"] + random.sample(string.letters, 3)
#                            + [".com"])
#             random.seed(i + 40)
#             psw = "".join(random.sample(string.letters, 10))
#             u = TestClient(user, psw)
#             u.create_demo_user()
#             SHARE_CLIENTS.append(u)

#     @classmethod
#     def tearDownClass(cls):
#         # restore previous status
#         try:
#             os.remove(DEMO_FILE)
#             os.remove(TEST_USER_DATA)
#             shutil.rmtree(TEST_DIRECTORY)
#         except OSError:
#             pass

#     def setUp(self):
#         server.app.config.update(TESTING=True)
#         server.app.testing = True

#     def test_create_user(self):
#         # check if a new user is correctly created
#         dirs_counter = len(os.listdir(server.USERS_DIRECTORIES))

#         user = "Gianni"
#         psw = "IloveJava"
#         client = TestClient(user, psw)
#         rv = client.create_demo_user(True)
#         self.assertEqual(rv.status_code, server.HTTP_BAD_REQUEST)

#         rv = client.create_demo_user()
#         self.assertEqual(rv.status_code, server.HTTP_CREATED)
#         # check if a directory is created
#         new_counter = len(os.listdir(server.USERS_DIRECTORIES))
#         self.assertEqual(dirs_counter + 1, new_counter)

#         # check if, when the user already exists, 'create_user' returns an
#         # error
#         rv = client.create_demo_user()
#         self.assertEqual(rv.status_code, server.HTTP_CONFLICT)

#         user = "Gianni"
#         psw = "zappa"
#         client = TestClient(user, psw)

#         rv = client.create_demo_user()
#         self.assertEqual(rv.status_code, server.HTTP_CONFLICT)

#     def test_to_md5(self):
#         # check if two files with the same content have the same md5
#         second_file = "second_file.txt"
#         with open(second_file, "w") as f:
#             f.write(DEMO_CONTENT)

#         first_md5 = server.to_md5(DEMO_FILE)
#         second_md5 = server.to_md5(second_file)
#         self.assertEqual(first_md5, second_md5)

#         os.remove(second_file)

#         # check if, for a directory, returns False
#         tmp_dir = "aloha"
#         os.mkdir(tmp_dir)
#         self.assertFalse(server.to_md5(tmp_dir))

#         os.rmdir(tmp_dir)

#     def test_create_server_path(self):
#         # check if aborts when you pass invalid paths:
#         invalid_paths = [
#             "../file.txt",
#             "folder/../file.txt"
#         ]

#         for p in invalid_paths:
#             f = open(DEMO_FILE, "r")
#             data = {"file_content": f}
#             rv = DEMO_CLIENT.call("post", "files/" + p, data)
#             f.close()

#             self.assertEqual(rv.status_code, 400)
#         # TODO: other tests here?

#     def test_files_post(self):
#         demo_path = "somepath/somefile.txt"
#         DEMO_CLIENT.set_fake_usr(True)
#         f = open(DEMO_FILE, "r")
#         data = {"file_content": f}
#         rv = DEMO_CLIENT.call("post", "files/" + demo_path, data)
#         f.close()
#         self.assertEqual(rv.status_code, 401)

#         DEMO_CLIENT.set_fake_usr(False)
#         f = open(DEMO_FILE, "r")
#         data = {"file_content": f}
#         rv = DEMO_CLIENT.call("post", "files/" + demo_path, data)
#         f.close()
#         self.assertEqual(rv.status_code, 201)
#         with open("{}{}/{}".format(TEST_DIRECTORY, DEMO_USER, demo_path)) as f:
#             uploaded_content = f.read()
#             self.assertEqual(DEMO_CONTENT, uploaded_content)

#         f = open(DEMO_FILE, "r")
#         data = {"file_content": f}
#         rv = DEMO_CLIENT.call("post", "files/" + demo_path, data)
#         f.close()
#         self.assertEqual(rv.status_code, 409)

#     def test_files_get(self):
#         client_path, server_path = set_tmp_params("dwn")
#         DEMO_CLIENT.set_fake_usr(True)
#         rv = DEMO_CLIENT.call("get", "files/" + client_path)
#         self.assertEqual(rv.status_code, 401)

#         DEMO_CLIENT.set_fake_usr(False)
#         rv = DEMO_CLIENT.call("get", "files/" + client_path)
#         self.assertEqual(rv.status_code, 200)

#         with open(server_path) as f:
#             got_content = f.read()
#             self.assertEqual(DEMO_CONTENT, got_content)

#         rv = DEMO_CLIENT.call("get", "files/" + NO_SERVER_PATH)
#         self.assertEqual(rv.status_code, 404)

#     def test_files_put(self):
#         demo_path = "somepath/somefile.txt"

#         client_path, server_path = set_tmp_params("pt")
#         if not server_path in server.User.users[DEMO_USER].paths[client_path]:
#             return

#         f = open(DEMO_FILE, "r")
#         data = {"file_content": f}
#         DEMO_CLIENT.set_fake_usr(True)
#         rv = DEMO_CLIENT.call("put", "files/" + demo_path, data)
#         f.close()
#         self.assertEqual(rv.status_code, 401)
#         DEMO_CLIENT.set_fake_usr(False)
#         f = open(DEMO_FILE, "r")
#         data = {"file_content": f}
#         rv = DEMO_CLIENT.call("put", "files/" + demo_path, data)
#         f.close()
#         self.assertEqual(rv.status_code, 201)

#         with open("{}{}/{}".format(TEST_DIRECTORY, DEMO_USER, demo_path)) as f:
#             put_content = f.read()
#             self.assertEqual(DEMO_CONTENT, put_content)

#         rv = DEMO_CLIENT.call("put", "files/" + NO_SERVER_PATH)
#         self.assertEqual(rv.status_code, 404)

#     def test_actions_delete(self):
#         client_path, server_path = set_tmp_params("dlt")
#         full_server_path = os.path.join(server_path, DEMO_FILE)

#         data = {"path": client_path}
#         DEMO_CLIENT.set_fake_usr(True)
#         rv = DEMO_CLIENT.call("post", "actions/delete", data)
#         self.assertEqual(rv.status_code, 401)

#         DEMO_CLIENT.set_fake_usr(False)
#         rv = DEMO_CLIENT.call("post", "actions/delete", data)
#         self.assertEqual(rv.status_code, 200)
#         self.assertFalse(os.path.isfile(full_server_path))
#         #check if the file is correctly removed from the dictionary
#         self.assertFalse(server_path in server.User.users[DEMO_USER].paths)

#         data = {"path": NO_SERVER_PATH}
#         rv = DEMO_CLIENT.call("post", "actions/delete", data)
#         self.assertEqual(rv.status_code, 404)

#         rv = DEMO_CLIENT.call("post", "actions/destroy", data)
#         self.assertEqual(rv.status_code, 404)

#     def test_last_file_delete_in_root(self):
#         # create a demo user
#         user = "emilio"
#         client = TestClient(user, "passw")
#         client.create_demo_user()

#         # upload a file
#         path = "filename.txt"
#         f = open(DEMO_FILE, "r")
#         data = {"file_content": f}
#         rv = client.call("post", "files/" + path, data)
#         f.close()
#         self.assertEqual(rv.status_code, 201)

#         # delete the file
#         data = {"path": path}
#         rv = client.call("post", "actions/delete", data)
#         self.assertEqual(rv.status_code, 200)

#         user_root = os.path.join(server.USERS_DIRECTORIES, user)
#         self.assertTrue(os.path.isdir(user_root))

#     def test_actions_copy(self):
#         DEMO_CLIENT.set_fake_usr(True)
#         data = {"file_src": "src", "file_dest": "dest"}
#         rv = DEMO_CLIENT.call("post", "actions/copy", data)
#         self.assertEqual(rv.status_code, 401)
#         DEMO_CLIENT.set_fake_usr(False)
#         rv, client_path, server_path = transfer("cp", True)
#         self.assertEqual(rv.status_code, 201)

#         full_dest_path = os.path.join(TEST_DIRECTORY,
#                                       DEMO_USER,
#                                       DEMO_DEST_COPY_PATH,
#                                       client_path)
#         self.assertEqual(os.path.isfile(server_path), True)

#         u = server.User.users[DEMO_USER]
#         self.assertEqual("cp/{}".format(DEMO_FILE) in u.paths, True)
#         self.assertEqual(os.path.isfile(full_dest_path), True)
#         self.assertEqual("{}/cp/{}".format(DEMO_DEST_COPY_PATH,
#                                            DEMO_FILE) in u.paths, True)
#         client_path, server_path = set_tmp_params("prova")
#         data = {"file_src": client_path, "file_dest": client_path}
#         rv = DEMO_CLIENT.call("post", "actions/copy", data)
#         self.assertEqual(rv.status_code, 409)

#     def test_actions_move(self):
#         DEMO_CLIENT.set_fake_usr(True)
#         data = {"file_src": "src", "file_dest": "dest"}
#         rv = DEMO_CLIENT.call("post", "actions/move", data)
#         self.assertEqual(rv.status_code, 401)
#         DEMO_CLIENT.set_fake_usr(False)
#         rv, client_path, server_path = transfer("mv", False)
#         self.assertEqual(rv.status_code, 201)

#         full_dest_path = os.path.join(TEST_DIRECTORY,
#                                       DEMO_USER,
#                                       DEMO_DEST_MOVE_PATH,
#                                       client_path)
#         self.assertEqual(os.path.isfile(server_path), False)

#         u = server.User.users[DEMO_USER]
#         self.assertEqual("mv/{}".format(DEMO_FILE) in u.paths, False)
#         self.assertEqual(os.path.isfile(full_dest_path), True)
#         self.assertEqual("{}/mv/{}".format(DEMO_DEST_MOVE_PATH,
#                                            DEMO_FILE) in u.paths, True)
#         rv, client_path, server_path = transfer("mv", False, False)
#         self.assertEqual(rv.status_code, 404)

#     def test_files_differences(self):
#         client = TestClient(
#             user="complex_user@gmail.com",
#             psw="complex_password"
#         )
#         client.create_demo_user()

#         # first check: user created just now
#         rv = client.call("get", "files/")
#         self.assertEqual(rv.status_code, 200)
#         snapshot1 = json.loads(rv.data)
#         self.assertFalse(snapshot1["snapshot"])

#         # second check: insert some files
#         some_paths = [
#             "path1/cool_filename.txt",
#             "path2/path3/yo.jpg"
#         ]
#         for p in some_paths:
#             f = open(DEMO_FILE, "r")
#             data = {"file_content": f}
#             rv = client.call("post", "files/" + p, data)
#             f.close()
#             self.assertEqual(rv.status_code, 201)

#         rv = client.call("get", "files/")
#         self.assertEqual(rv.status_code, 200)
#         snapshot2 = json.loads(rv.data)
#         self.assertGreater(snapshot2["timestamp"], snapshot1["timestamp"])
#         self.assertEqual(len(snapshot2["snapshot"]), 1)
#         for s in snapshot2["snapshot"].values():
#             self.assertEqual(len(s), 2)

#         # third check: delete a file
#         data = {"path": some_paths[1]}
#         rv = client.call("post", "actions/delete", data)
#         self.assertEqual(rv.status_code, 200)

#         rv = client.call("get", "files/")
#         self.assertEqual(rv.status_code, 200)

#         snapshot3 = json.loads(rv.data)
#         self.assertGreater(snapshot3["timestamp"], snapshot2["timestamp"])
#         self.assertEqual(len(snapshot3["snapshot"]), 1)

#         for s in snapshot3["snapshot"].values():
#             self.assertEqual(len(s), 1)

#     def test_user_class_init(self):
#         # create a temporary directory and work on it
#         working_directory = os.getcwd()

#         test_dir = "tmptmp"
#         try:
#             os.mkdir(test_dir)
#         except OSError:
#             shutil.rmtree(test_dir)
#             os.mkdir(test_dir)

#         os.chdir(test_dir)

#         # check 1: if the folder is empty, nothing is modified
#         previous_users = server.User.users
#         server.User.user_class_init()
#         self.assertEqual(server.User.users, previous_users)

#         # check 2: if there is a json, upload the users from it
#         username = "UserName"
#         tmp_dict = {
#             "users": {
#                 username: {
#                     "paths": {
#                         "": [
#                             "user_dirs/{}".format(username),
#                             False,
#                             1403512334.247553
#                         ],
#                         "hello.txt": [
#                             "user_dirs/{}/hello.txt".format(username),
#                             "6186badadb5fbb0416cd29a04e2d92d7",
#                             1403606130.356392
#                         ]
#                     },
#                     "psw": "encrypted password",
#                     "timestamp": 1403606130.356392
#                 },
#             }
#         }
#         with open(server.USERS_DATA, "w") as f:
#             json.dump(tmp_dict, f)
#         server.User.user_class_init()
#         self.assertIn(username, server.User.users)

#         # restore the previous situation
#         os.chdir(working_directory)
#         shutil.rmtree(test_dir)

#     # SHARE TESTS
#     def test_add_share(self):
#         DEMO_CLIENT.set_fake_usr(True)
#         rv = DEMO_CLIENT.call("post", "shares/dir/usr")
#         self.assertEqual(rv.status_code, 401)

#         DEMO_CLIENT.set_fake_usr(False)

#         f = open(DEMO_FILE, "r")
#         data = {"file_content": f}
#         rv = DEMO_CLIENT.call("post", "files/" + DEMO_FILE, data)
#         f.close()
#         self.assertEqual(rv.status_code, 201)

#         rv = DEMO_CLIENT.call("post", "shares/{}/{}".format(
#             DEMO_FILE, SHARE_CLIENTS[1].user)
#         )
#         self.assertEqual(rv.status_code, 200)

#         # upload a file
#         f = open(DEMO_FILE, "r")
#         data = {"file_content": f}
#         rv = DEMO_CLIENT.call("post", "files/path_to_share/" + DEMO_FILE, data)
#         f.close()
#         self.assertEqual(rv.status_code, 201)

#         with open("{}{}/{}/{}".format(TEST_DIRECTORY, DEMO_USER,
#                                       "path_to_share", DEMO_FILE)) as f:
#             uploaded_content = f.read()
#             self.assertEqual(DEMO_CONTENT, uploaded_content)

#         # share the folder
#         rv = DEMO_CLIENT.call("post", "shares/path_to_share/{}".format(
#             SHARE_CLIENTS[2].user)
#         )
#         self.assertEqual(rv.status_code, 200)

#         self.assertEqual("shares/{}/path_to_share".format(DEMO_CLIENT.user) in
#                          server.User.users[SHARE_CLIENTS[2].user].paths, True)

#     def test_can_write(self):
#         DEMO_CLIENT.set_fake_usr(True)
#         rv = DEMO_CLIENT.call("post", "shares/dir/usr")
#         self.assertEqual(rv.status_code, 401)

#         DEMO_CLIENT.set_fake_usr(False)

#         f = open(DEMO_FILE, "r")
#         data = {"file_content": f}
#         rv = DEMO_CLIENT.call("post", "files/try_to_modify/" + DEMO_FILE, data)
#         f.close()
#         self.assertEqual(rv.status_code, 201)

#         rv = DEMO_CLIENT.call("post",
#                               "shares/try_to_modify/{}".format(SHARE_CLIENTS[3]
#                                                                .user))
#         self.assertEqual(rv.status_code, 200)

#         f = open(DEMO_FILE, "r")
#         data = {"file_content": f}
#         rv = SHARE_CLIENTS[3].call("post",
#                                    "files/shares/{}/try_to_modify/"
#                                    .format(DEMO_CLIENT.user) + DEMO_FILE, data)
#         f.close()
#         self.assertEqual(rv.status_code, 403)

#         f = open(DEMO_FILE, "r")
#         data = {"file_content": f}
#         rv = SHARE_CLIENTS[3].call("put", "files/shares/{}/try_to_modify/"
#                                    .format(DEMO_CLIENT.user) + DEMO_FILE, data)
#         f.close()
#         self.assertEqual(rv.status_code, 403)

#         data = {"path": "shares/{}/try_to_modify/".format(DEMO_CLIENT.user) +
#                 DEMO_FILE}
#         rv = SHARE_CLIENTS[3].call("post", "actions/delete", data)
#         self.assertEqual(rv.status_code, 403)

#         data = {"path": "shares/{}/try_to_modify/".format(DEMO_CLIENT.user) +
#                 DEMO_FILE}
#         rv = SHARE_CLIENTS[3].call("post", "actions/delete", data)
#         self.assertEqual(rv.status_code, 403)

#         f = open(DEMO_FILE, "r")
#         data = {"file_content": f}
#         rv = SHARE_CLIENTS[3].call("post", "files/a_path/" + DEMO_FILE, data)
#         f.close()
#         self.assertEqual(rv.status_code, 201)

#         data = {"file_src": "a_path/" + DEMO_FILE,
#                 "file_dest": "shares/{}/try_to_modify/"
#                 .format(DEMO_CLIENT.user)}
#         rv = SHARE_CLIENTS[3].call("post", "actions/copy", data)
#         self.assertEqual(rv.status_code, 403)

#         rv = SHARE_CLIENTS[3].call("post", "actions/move", data)
#         self.assertEqual(rv.status_code, 403)

#     def test_remove_beneficiary(self):
#         owner = SHARE_CLIENTS[0].user
#         user1 = SHARE_CLIENTS[1].user
#         user2 = SHARE_CLIENTS[2].user

#         # test if aborts when the file is not on the server
#         received = SHARE_CLIENTS[0].call(
#             "delete",
#             "/".join(["shares", "somefile.txt", "beneficiary@oijoid.it"])
#         )
#         self.assertEqual(received.status_code, 400)
#         self.assertEqual(received.data,
#                          '"The specified file or directory is not present"')

#         # test if aborts when the resource is not shared with the beneficiary
#         with open(DEMO_FILE, "r") as f:
#             data = {"file_content": f}
#             rv = SHARE_CLIENTS[0].call("post", "files/" + DEMO_FILE, data)
#             self.assertEqual(rv.status_code, 201)

#         received = SHARE_CLIENTS[0].call(
#             "delete",
#             "/".join(["shares", DEMO_FILE, user1])
#         )
#         self.assertEqual(received.status_code, 400)

#         # share a file with a couple of users
#         for usern in [user1, user2]:
#             received = SHARE_CLIENTS[0].call(
#                 "post",
#                 "/".join(["shares", DEMO_FILE, usern])
#             )
#             self.assertEqual(received.status_code, 200)

#         # remove the first user
#         received = SHARE_CLIENTS[0].call(
#             "delete",
#             "/".join(["shares", DEMO_FILE, user1])
#         )
#         self.assertEqual(received.status_code, 200)

#         server_path = os.path.join(
#             server.USERS_DIRECTORIES,
#             owner,
#             DEMO_FILE
#         )
#         self.assertIn(server_path, server.User.shared_resources)
#         self.assertEqual(
#             server.User.shared_resources[server_path],
#             [owner, user2]
#         )

#         # remove the second user
#         received = SHARE_CLIENTS[0].call(
#             "delete",
#             "/".join(["shares", DEMO_FILE, user2])
#         )
#         self.assertEqual(received.status_code, 200)
#         self.assertNotIn(server_path, server.User.shared_resources)

#     def test_remove_share(self):
#         owner = SHARE_CLIENTS[0].user
#         user1 = SHARE_CLIENTS[1].user
#         user2 = SHARE_CLIENTS[2].user

#         # upload a file
#         with open(DEMO_FILE, "r") as f:
#             data = {"file_content": f}
#             rv = SHARE_CLIENTS[0].call("post", "files/shared_file", data)
#             self.assertEqual(rv.status_code, 201)

#         # test if aborts when the resource is not shared
#         received = SHARE_CLIENTS[0].call(
#             "delete",
#             "/".join(["shares", "shared_file"])
#         )
#         self.assertEqual(received.status_code, 400)

#         # share a file with a couple of users
#         for usern in [user1, user2]:
#             received = SHARE_CLIENTS[0].call(
#                 "post",
#                 "/".join(["shares", "shared_file", usern])
#             )
#             self.assertEqual(received.status_code, 200)

#         # remove the share on the resource and check
#         received = SHARE_CLIENTS[0].call("delete",
#                                          "/".join(["shares", "shared_file"]))
#         self.assertEqual(received.status_code, 200)
#         self.assertNotIn(
#             os.path.join(
#                 server.USERS_DIRECTORIES,
#                 owner,
#                 "shared_file"
#             ),
#             server.User.shared_resources
#         )

#     def test_changes_in_shared_directory(self):
#         owner = SHARE_CLIENTS[3].user
#         beneficiary = SHARE_CLIENTS[4].user
#         subdir = "pappalabaisa"

#         # upload a file
#         with open(DEMO_FILE, "r") as f:
#             data = {"file_content": f}
#             rv = SHARE_CLIENTS[3].call(
#                 "post",
#                 "".join(["files/", subdir, "/", DEMO_FILE]),
#                 data
#             )
#         self.assertEqual(rv.status_code, 201)

#         # share subdir with beneficiary
#         rv = SHARE_CLIENTS[3].call(
#             "post",
#             "shares/{}/{}".format(subdir, beneficiary)
#         )
#         self.assertEqual(rv.status_code, 200)

#         # update a shared file and check if it's ok
#         owner_timestamp = server.User.users[owner].timestamp
#         with open("modified_file", "w") as f:
#             f.write("ps, scordavo di dirti ciao.")
#         with open("modified_file", "r") as f:
#             data = {"file_content": f}
#             rv = SHARE_CLIENTS[3].call(
#                 "put",
#                 "".join(["files/", subdir, "/", DEMO_FILE]),
#                 data
#             )
#         self.assertEqual(rv.status_code, 201)
#         os.remove("modified_file")

#         owner_new_timestamp = server.User.users[owner].timestamp
#         self.assertGreater(owner_new_timestamp, owner_timestamp)

#         ben_timestamp = server.User.users[beneficiary].timestamp
#         self.assertEqual(owner_new_timestamp, ben_timestamp)

#         # upload a new file in shared directory and check
#         with open(DEMO_FILE, "r") as f:
#             data = {"file_content": f}
#             rv = SHARE_CLIENTS[3].call(
#                 "post",
#                 "".join(["files/", subdir, "/other_subdir/new_file"]),
#                 data
#             )
#         self.assertEqual(rv.status_code, 201)
#         self.assertEqual(
#             server.User.users[owner].timestamp,
#             server.User.users[beneficiary].timestamp
#         )
#         self.assertIn(
#             "/".join(["shares", owner, subdir, "other_subdir/new_file"]),
#             server.User.users[beneficiary].paths
#         )

#         # remove a file and check
#         data = {"path": "".join([subdir, "/other_subdir/new_file"])}
#         rv = SHARE_CLIENTS[3].call("post", "actions/delete", data)
#         self.assertEqual(rv.status_code, 200)

#         self.assertEqual(
#             server.User.users[owner].timestamp,
#             server.User.users[beneficiary].timestamp
#         )
#         self.assertNotIn(
#             "/".join(["shares", owner, subdir, "other_subdir"]),
#             server.User.users[beneficiary].paths
#         )
#         self.assertNotIn(
#             "/".join(["shares", owner, subdir, "other_subdir/new_file"]),
#             server.User.users[beneficiary].paths
#         )

#         # remove every file in shared subdir and check if the shared_resource
#         # has been removed
#         data = {"path": "/".join([subdir, DEMO_FILE])}
#         rv = SHARE_CLIENTS[3].call("post", "actions/delete", data)
#         self.assertEqual(rv.status_code, 200)

#         self.assertNotIn(
#             os.path.join(
#                 server.USERS_DIRECTORIES,
#                 owner,
#                 subdir
#             ),
#             server.User.shared_resources
#         )


class TestServerInternalErrors(unittest.TestCase):
    root = os.path.join(
        os.path.dirname(
            os.path.abspath(
                sys.argv[0])
        ),
        "demo_test/internal_errors"
    )

    def setUp(self):
        server.app.config.update(TESTING=True)
        server.app.testing = True
        # Note: it's possible to make assertRaises on internal server
        # exceptions from the test_client only if app testing is True.

        self.root = TestServerInternalErrors.root
        server.SERVER_ROOT = self.root
        server.server_setup()

        self.user_data = os.path.join(self.root, "user_data.json")
        self.user_dirs = os.path.join(self.root, "user_dirs")
        self.tc = server.app.test_client()

    def tearDown(self):
        try:
            shutil.rmtree(self.user_dirs)
        except OSError:
            pass
        try:
            os.remove(self.user_data)
        except OSError:
            pass

    def test_corrupted_users_data_json(self):
        """
        If the user data file is corrupted, it will be raised a ValueError.
        """
        shutil.copy(
            os.path.join(self.root, "corrupted_user_data.json"),
            self.user_data
        )
        with self.assertRaises(ValueError):
            server.server_setup()

    def test_directory_already_present(self):
        """
        If, creating a new user, after checking his username, a directory with
        his/her name is already present, it will be raised an OSError and
        it will be returned a status code 500.
        """
        username = "papplamoose@500.com"
        try:
            os.makedirs(os.path.join(self.user_dirs, username))
        except OSError:
            shutil.rmtree(self.user_dirs)
            os.makedirs(os.path.join(self.user_dirs, username))

        def try_to_create_user():
            return self.tc.post(
                _API_PREFIX + "create_user",
                data={
                    "user": username,
                    "psw": "omg_it_will_be_raised_an_error!"
                }
            )

        # check if OSError is raised
        with self.assertRaises(OSError):
            try_to_create_user()

        # check if returns 500
        server.app.testing = False
        received = try_to_create_user()
        self.assertEqual(received.status_code, 500)

    def test_access_to_non_existent_server_path(self):
        """
        If a path exists in some user's paths dictionary, but it's not in the
        filesystem, when somebody will try to access it, it will be raised an
        IOError and it will be returned a status code 500.
        """
        owner = "Emilio@me.it"
        owner_headers = make_headers(owner, "password")
        owner_filepath = "ciao.txt"

        # setup
        shutil.copy(
            os.path.join(self.root, "demo_user_data.json"),
            self.user_data
        )
        server.server_setup()

        # 1. case download
        def try_to_download():
            return self.tc.get(
                "{}files/{}".format(_API_PREFIX, owner_filepath),
                headers=owner_headers
            )
        # check IOError
        with self.assertRaises(IOError):
            try_to_download()
        # check service code
        server.app.testing = False
        received = try_to_download()
        self.assertEqual(received.status_code, 500)
        server.app.testing = True

        # 2. case move or copy
        def try_to_transfer(action):
            return self.tc.post(
                "{}actions/{}".format(_API_PREFIX, action),
                data={
                    "file_src": owner_filepath,
                    "file_dest": "transferred.file"
                },
                headers=owner_headers
            )
        # check IOError
        for action in ["move", "copy"]:
            with self.assertRaises(IOError):
                try_to_transfer(action)
        # check service code
        server.app.testing = False
        for action in ["move", "copy"]:
            try_to_transfer(action)
        self.assertEqual(received.status_code, 500)
        server.app.testing = True


if __name__ == '__main__':
    # make tests!
    unittest.main()
