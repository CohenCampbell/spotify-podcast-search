from unittest import TestCase
from models import db, User, Podcast
from forms import RegisterForm, LoginForm, SpotifyPodcastSearchForm, SpotifyPodcastInfoForm, KeywordForm
from flask import session
from app import app
import os

db.create_all()
app.config['WTF_CSRF_ENABLED'] = False

TEST_CODE = os.getenv("TEST_CODE")

class RegisterFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        
        db.drop_all()
        db.create_all()

        db.session.commit() 

        cls.client = app.test_client()
    
    @classmethod
    def tearDownClass(cls):
        db.session.rollback()
    
    def test_RegisterForm_render(self):
        with app.test_client() as client:
            resp = client.get("/register")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form action="/register" method="post">', html)
    
    def test_RegisterForm_submission(self):
         with app.test_client() as client:
            data = {"username":"User1", 
                    "password":"Password1", 
                    "email": "Email@Email.com"}
            reg = client.post("/register", data=data)

            res = User.get_by_username("User1")
            self.assertEqual(res.username, "User1")
            self.assertEqual(res.email, "Email@Email.com")

class LoginFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        
        db.drop_all()
        db.create_all()

        db.session.commit() 

        cls.client = app.test_client()
    
    @classmethod
    def tearDownClass(cls):
        db.session.rollback()
    
    def test_LoginForm_render(self):
        with app.test_client() as client:
            resp = client.get("/login")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form action="/login" method="post">', html)

    def test_LoginForm_submission(self):
         user = User.register("User1", "Password1", "Email@Email.com");
         db.session.commit() 
         with app.test_client() as client:
            data = {"username": "User1", "password": "Password1"}
            log = client.post("/login", data=data)

            self.assertEqual(session["user_id"], user.id)
    
class SpotifyPodcastSearchFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        
        db.drop_all()
        db.create_all()

        db.session.commit() 

        cls.client = app.test_client()
        
    @classmethod
    def tearDownClass(cls):
        db.session.rollback()

    def test_SpotifyPodcastSearchForm_render_not_admin(self):
        with app.test_client() as client:
            resp = client.get("/podcastAPI", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            #Checks for login form because of redirect
            self.assertIn('<form action="/login" method="post">', html)

    def test_SpotifyPodcastSearchForm_render(self):
        admin = User.register("Admin1", "Password1", "Email@Email.com");
        db.session.commit()
        User.make_admin_by_id(admin.id)
        with app.test_client() as client:
            d = {"username": "Admin1", "password": "Password1"}
            log = client.post("/login", data=d)

            resp = client.get("/podcastAPI", follow_redirects=True)
            html = resp.get_data(as_text=True)
           
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form action="/podcastAPI" method="post">', html)
    
    def test_SpotifyPodcastSearchForm_submission(self):
        #!This test will fail if TEST_CODE isn't updated
        with app.test_client() as client:
            admin = User.register("Admin2", "Password2", "Email@Email.com");
            db.session.commit()
            User.make_admin_by_id(admin.id)

            log_d = {"username": "Admin2", "password": "Password2"}
            client.post("/login", data=log_d)

            
            with client.session_transaction() as sess:
                sess["code"] = TEST_CODE

            #RedThread podcast id, if the podcast gets deleted this won't work
            data = {"search": "1AuEfikQoC5MTezIAiance"}
            podcast_res = client.post("/podcastAPI", data=data, follow_redirects=True)
            html =  podcast_res.get_data(as_text=True)
            
            self.assertIn('<button type="submit" class="btn btn-success">Add to database!</button>', html)

class KeywordFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        
        db.drop_all()
        db.create_all()

        User.register("User1", "Password1", "Email@Email.com");
        User.register("User2", "Password2", "Email@Email.com");
        db.session.commit() 

        cls.client = app.test_client()
    
    @classmethod
    def tearDownClass(cls):
        db.session.rollback()

    def test_KeywordForm_render(self):
        podcast = Podcast.add_podcast("TRT", "Red  Thread", "Great time TRT",
                                      "https://i.scdn.co/image/9af79fd06e34dea3cd27c4e1cd6ec7343ce20af4",
                                      "0ebffb9b25e748ff")
        db.session.commit()
        
        with app.test_client() as client:
            data = {"username": "User1", "password": "Password1"}
            log = client.post("/login", data=data)

            resp = client.get(f"/podcast/{podcast.id}", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<form action="/search/{podcast.id}" method="post">', html)

    def test_KeywordForm_submission(self):
        podcast = Podcast.add_podcast("JRE", "Joe Rogan Exp", "Great time JRE", "https://i.scdn.co/image/9af79fd06e34dea3cd27c4e1cd6ec7343ce20af4",
                                      "4rOoJ6Egrf8K2IrywzwOMk")
        db.session.commit()
        with app.test_client() as client:
            log_data = {"username": "User2", "password": "Password2"}
            log = client.post("/login", data=log_data)

            #!This test will fail if TEST_CODE isn't updated
            with client.session_transaction() as sess:
                sess["code"] = TEST_CODE

            data = {"keyword": "asdf;lasdkjf3%Lj2034)-_sdflk"}
            resp = client.post(f"/search/{podcast.id}",data=data ,follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn(f'<p class="text-danger">No episodes were found using the word {data["keyword"]}!</p>', html)



             
 