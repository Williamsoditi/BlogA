import unittest
from app.models import Comment, User
from app import db

class CommentTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Comments class
    '''
    def setUp(self):
        self.user_Mwikali = User(password = '5443', email = 'mwikali119@gmail.com')
        self.new_comment = Comment(id=1,comment='Nice blog')

    def tearDown(self):
        Comment.query.delete()
        User.query.delete()
        
    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.id,1)
        self.assertEquals(self.new_comment.comment,'Nice blog')
        
    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)
        
    def test_get_comment_by_id(self):
        self.new_comment.save_comment()
        got_comments = Comment.get_comments(1)
        self.assertFalse(len(got_comments) == 1)