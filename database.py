import sqlite3
from sqlite3 import Error

userid = 12453
vchan = 389689235


# добавление бд и подключение к ней
class DB:
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection

    def create_query(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred")

    def add_channel(self, connection, vchan, user):
        add_chan = f"""
        INSERT INTO
          channels (vchannel, userid)
        VALUES
          ({vchan}, {user})
        """
        cursor = connection.cursor()
        try:
            cursor.execute(add_chan)
            connection.commit()
            print(1)
        except Error as e:
            print(f"The error '{e}' occurred")

    def delete_Channel(self, connection, vchan):
        delete_Chan = f"DELETE FROM channels WHERE vchannel = {vchan}"
        cursor = connection.cursor()
        try:
            cursor.execute(delete_Chan)
            connection.commit()
            print(2)
        except Error as e:
            print(f"The error '{e}' occurred")

    def find_vchannel(self, connection):
        find_Chan = "SELECT vchannel FROM channels"
        channs = []
        cursor = connection.cursor()
        try:
            cursor.execute(find_Chan)
            res = cursor.fetchall()
            connection.commit()
            for i in res:
                for j in i:
                    channs.append(int(j))
            return channs
        except Error as e:
            print(f"The error '{e}' occurred")

    def find_tchannel(self, connection, vchan):
        find_Chan = f"SELECT tchannel FROM channels WHERE vchannel = {vchan}"
        channs = 0
        cursor = connection.cursor()
        try:
            cursor.execute(find_Chan)
            res = cursor.fetchall()
            connection.commit()
            for i in res:
                for j in i:
                    channs = (int(j))
            return channs
        except Error as e:
            print(f"The error '{e}' occurred")

    def find_users_vchan(self, connection, user):
        find_Chan = f"SELECT vchannel FROM channels WHERE userid = {user}"
        channs = 0
        cursor = connection.cursor()
        try:
            cursor.execute(find_Chan)
            res = cursor.fetchall()
            connection.commit()
            for i in res:
                for j in i:
                    channs = (int(j))
            return channs
        except Error as e:
            print(f"The error '{e}' occurred")
        else:
            print("it not")


create_users_table = """
CREATE TABLE IF NOT EXISTS channels (
  vchannel INTEGER PRIMARY KEY,
  tchannel INTEGER NOT NULL
);
"""

if __name__ == '__main__':
    dan = DB()
    connection = dan.create_connection("urVChan.sqlite")
    print(dan.find_channel(connection))
