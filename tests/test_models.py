from unittest import TestCase
from models import db, Podcast, User, WatchList

from app import app


db.create_all()

 
class PodcastModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        
        db.drop_all()
        db.create_all()

        db.session.commit() 

        cls.client = app.test_client()
    
    @classmethod
    def tearDownClass(cls):
        db.session.rollback()

    def test_podcast_add(self):
        podcast = Podcast.add_podcast("JRE", "Joe Rogan Exp", "Great time JRE", "https://i.scdn.co/image/9af79fd06e34dea3cd27c4e1cd6ec7343ce20af4",
                                      "4rOoJ6Egrf8K2IrywzwOMk")
        db.session.commit()
        
        self.assertEqual(podcast.host, "JRE")

    def test_get_by_id(self):
        podcast = Podcast.add_podcast("JRE", "Joe Rogan Exp", "Great time JRE", "https://i.scdn.co/image/9af79fd06e34dea3cd27c4e1cd6ec7343ce20af4",
                                      "4rOoJ6Egrf8K2IrywzwOMk")
        
        db.session.commit()

        #checking if podcast was added correctly
        self.assertEqual(podcast.host, "JRE")
        
        test_podcast = Podcast.get_by_id(podcast.id)
        
        self.assertEqual(test_podcast.host, "JRE")

    def test_delete_podcast(self):
        podcast = Podcast.add_podcast("JRE", "Joe Rogan Exp", "Great time JRE", "https://i.scdn.co/image/9af79fd06e34dea3cd27c4e1cd6ec7343ce20af4",
                                      "4rOoJ6Egrf8K2IrywzwOMk")
        
        db.session.commit()

        #checking if podcast was added correctly
        self.assertEqual(podcast.host, "JRE")

        deleted_podcast = Podcast.delete_podcast(podcast.id)
        
        db.session.commit()

        self.assertIsNone(deleted_podcast)

        deleted_podcast_query = Podcast.get_by_id(podcast.id)
        self.assertIsNone(deleted_podcast_query)

class UserModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        
        db.drop_all()
        db.create_all()

        cls.uid = 100
        u = User.register(username="Someguy",password="Password1" ,email="email@email.com")
        u.id = cls.uid
        cls.u = User.get_by_id(cls.uid)
        
        db.session.commit() 

        cls.client = app.test_client()
    
    @classmethod
    def tearDownClass(cls):
        db.session.rollback()   

    def test_register(self):
        user = User.register(username="testUser", password="Password123", email="Email@Email.com")

        db.session.commit()

        self.assertEqual(user.username, "testUser")
    
    def test_get_by_id(self):
        user = User.get_by_id(self.uid)
        self.assertEqual(user.id, self.uid)

    def test_get_by_username(self):
        user = User.get_by_username(self.u.username)
        self.assertEqual(user.username, self.u.username)
    
    def test_make_admin_by_id(self):
        user = User.make_admin_by_id(self.uid)
        self.assertTrue(user.admin)

class WatchListTests(TestCase):
    @classmethod
    def setUpClass(cls):
    
        db.drop_all()
        db.create_all()

        cls.uid = 100
        cls.u = User.register(username="Someguy",password="Password1" ,email="email@email.com")
        cls.u.id = cls.uid
  
        cls.podcast = Podcast.add_podcast("JRE", "Joe Rogan Exp", "Great time JRE", 
                                  "https://i.scdn.co/image/9af79fd06e34dea3cd27c4e1cd6ec7343ce20af4",
                                  "4rOoJ6Egrf8K2IrywzwOMk")
        db.session.commit()
        WatchList.add_item(user_id=cls.uid, podcast_id=cls.podcast.id)
        db.session.commit() 
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.rollback()   
    def test_get_watchlist(self):
        watchlist = WatchList.get_watchlist(user_id=self.uid)
       
        self.assertEqual(watchlist[0].podcasts, self.podcast)
    def test_add_item(self):
        podcast = Podcast.add_podcast("TRT", "Red  Thread", "Great time TRT",
                                      "https://i.scdn.co/image/9af79fd06e34dea3cd27c4e1cd6ec7343ce20af4",
                                      "0ebffb9b25e748ff")
        db.session.commit()

        WatchList.add_item(self.uid, podcast.id)

        watchlist = WatchList.get_watchlist(user_id=self.uid)

        self.assertEqual(watchlist[1].podcasts, podcast)

    def test_remove_item(self):
        WatchList.remove_item(self.uid, self.podcast.id);
        watchlist = WatchList.get_watchlist(user_id=self.uid)
        self.assertNotIn(self.podcast, watchlist)
        
        

            

    


    
