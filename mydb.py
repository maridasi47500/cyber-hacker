from user import User
from country import Country
from video import Video
from comment import Comment
class Mydb():
  def __init__(self):
    self.hey="hello"
    self.Video=Video()
    self.Comment=Comment()
    self.User=User()
    self.Country=Country()
