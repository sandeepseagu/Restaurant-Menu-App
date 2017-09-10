# "Database code" for the DB Forum.

import datetime
import psycopg2
import bleach

POSTS = [("This is the first post.", datetime.datetime.now())]

def get_posts():
  """Return all posts from the 'database', most recent first."""
  DB=psycopg2.connect("dbname=forum")
  c=DB.cursor()
  c.execute("SELECT time,content FROM posts ORDER BY time DESC")
  posts=({'content': str(row[1]), 'time': str(row[0])} for row in c.fetchall())
  DB.close()
  return (posts) 

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  DB=psycopg2.connect("dbname=forum")
  c=DB.cursor()
  text=bleach.clean( str(content))
  c.execute("INSERT INTO posts(content) VALUES (%s)", (text,))
  DB.commit()
  DB.close()
  #POSTS.append((content, datetime.datetime.now()))

