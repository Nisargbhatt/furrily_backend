from mongoengine import connect

from constants import connection

connect("furrily", host=connection)
