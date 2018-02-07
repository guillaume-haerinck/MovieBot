
import socket
import random

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 12000))
print ("server launched, listening on port 12000")

while True:
        socket.listen(5)
        client, address = socket.accept()
        print ("{} connected".format( address ))

        response = client.recv(255)
        if response.decode("utf-8") == "getMovie":
            print ("Check the Database for movies")
            movies = open('dbMovies.txt').read().splitlines()
            movie = random.choice(movies)
            print (movie)
            client.send(movie.encode("utf-8"))

print ("Close")
client.close()
stock.close()