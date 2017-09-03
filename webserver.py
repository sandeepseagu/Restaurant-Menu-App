from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem

engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message+= "<html><body>"
            message+="Hello!"
            message+="""<form method='POST' enctype='multipart/form-data' action='/hello'>
            <h2>what would you like me to say?</h2><input name='message' type='text'>
            <input type='submit' value='Submit'></form> """
            message+="</body></html>"

            self.wfile.write(message)
            print message
            return
        try:
            if self.path.endswith("/hola"):
              self.send_response(200)
              self.send_header('Content-type', 'text/html')
              self.end_headers()
              message = ""
              message += "<html><body>&#161Hola</body></html>"
              self.wfile.write(message)
              print message
              return

        except:
            self.send_error(404, 'File Not Found: %s' % self.path)

        restaurants = session.query(Restaurant).all()
        try:
            if self.path.endswith("/edit"):
                restaurantIDPath=self.path.split("/")[2]
                restaurantQuery=session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                if restaurantIDPath!=[]:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()
                    output=""
                    output+="<html><body>"
                    output+=restaurantQuery.name
                    output+="<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit>"% restaurantQuery.id
                    output+=
            if self.path.endswith("/restaurant"):

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output +="<a href='#'>Edit</a></br>"
                    output +="<a href='#'>Delete</a></br>"
                    output +="</br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
             #pass
                self.send_error(404, 'File Not Found: %s' % self.path)




        try:

            if self.path.endswith("/restaurant/new"):

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output+="""<form method='POST' enctype='multipart/form-data' action='/restaurant/new'>
                <h2>Add a New Restaurant</h2><input name='newRestaurant' type='text' placeholder='New Restaurant name'>
                <input type='submit' value='Submit'></form> """

                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
             #pass
                self.send_error(404, 'File Not Found: %s' % self.path)



    def do_POST(self):
         #try:
          #  self.send_response(301)
           # self.end_headers()

            #ctype,pdict=cgi.parse_header(self.headers.getheader('content-type'))
            #if ctype=='multipart/form-data':
             #   fields=cgi.parse_multipart(self.rfile,pdict)
              #  messagecontent=fields.get('message')

            #output=""
            #output+="<html><body>"
            #output+="<h2>Okay, how about this:</h2>"
            #output+="<h2>%s</h2>" % messagecontent[0]

            #output+="""<form method='POST' enctype='multipart/form-data' action='/hello'>
            #<h2>what would you like me to say?</h2><input name='message' type='text'>
            #<input type='submit' value='Submit'></form> """
            #output+="</html></body>"
            #self.wfile.write(output)


         #except:
          #  pass


         try:
            if self.path.endswith("/restaurant/new"):
                ctype,pdict=cgi.parse_header(self.headers.getheader('content-type'))
                if ctype=='multipart/form-data':
                  fields=cgi.parse_multipart(self.rfile,pdict)
                messagecontent=fields.get('newRestaurant')

                #newRestaurant=Restaurant(name=messagecontent[0])

                newRestaurantName = Restaurant(name=messagecontent[0])
                session.add(newRestaurantName)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()

         except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
      main()