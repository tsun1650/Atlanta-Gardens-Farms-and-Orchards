import pymysql.cursors
import logging


class DBManager:

    def __init__(self):
        self._db = "idk"

    """
    getConnection:
        Returns the connection to the database
        only called within this class!! (don't need to call from main code)
    """
    def getConnection(self):
        # create connection
        conn = pymysql.connect(
            host='academic-mysql.cc.gatech.edu',
            user='cs4400_team_68',
            password='JQasN9vs',
            db='cs4400_team_68'
        )
        return conn

    """
    verifyLogin:
        Makes sure that there exists this email and password combination in the User table
        Inputs:
            Email the user entered and the hashed string of the password the user inputted
        Returns:
            True if there is a match in the db
            False otherwise
    """
    def verifyLogin(self, email, hashPass):
        # SQL statement to execute
        sql = "SELECT Email, Password from User WHERE Email = %s AND Password = %s;"

        # User input to check for in SQL statement
        userin = (email, hashPass)

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, userin)

            # Get result
            result = cursor.fetchone()

            if result is not None:
                # Found match
                conn.close()
                return True
            else:
                # No match
                conn.close()
                return False
        except Exception as e:
            print("ERROR: {}".format(e))
        finally:
            conn.close()

    """
    getUserType:
        Gets the user type of the current user
        Only call this after a user is verified through verifyLogin
        Inputs:
            The current users email
        Returns:
            The type of user the user is
    """
    def getUserType(self, email):
        # SQL statement to execute
        sql = "SELECT UserType from User WHERE Email = %s;"

        # User input to check for in SQL statement
        userin = (email)

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, userin)

            # Get result
            result = cursor.fetchone()

            return result
        except Exception as e:
            print("ERROR: {}".format(e))
        finally:
            conn.close()

    """
    registerNewUser:
        Adds new user to the User table
        Inputs:
            email, username, already hashed password, and the type of user
        Returns:
            true if the insert was successful
            false otherwise (aka email and username not unique)
    """
    def registerNewUser(self, email, username, hashPass, usertype):
        # SQL statement to execute
        sql = "INSERT INTO User (Email, Username, Password, UserType) " \
              "VALUES (%s, %s, %s, %s) " \
              "WHERE NOT EXISTS " \
              "(SELECT Email, Username FROM User WHERE Email = %s AND Username = %s);"

        # User input to check for in SQL statement
        userin = (email, username, hashPass, usertype, email, username)

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, userin)

            # Commit changes to db
            conn.commit()

            # Get result
            result = cursor.fetchall()

            if len(result) > 0:
                # Insert was a success
                conn.close()
                return True
            else:
                # Insert failed
                conn.close()
                return False

        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    addProperty:
        Adds a property to the Property table; only if the name is unique
        Property is not approved by admin yet
        Inputs:
            name, address, city, zip, public, commercial, type, owner name, and size of the new property
        Returns: 
            True if the insert was successful
            False if the name of the property already exists in the Property table
    """
    def addProperty(self, name, address, city, addyZip, public, commercial, propType, owner, size):
        # SQL statement to execute
        sql = "INSERT INTO Property (Name, Address, City, ZIP, " \
              "isPublic, isCommercial, PropertyType, OwnedBy, NumVisits, AvgRating, Size) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0, 0.0, %s) " \
              "WHERE NOT EXISTS " \
              "(SELECT Name FROM Property WHERE Name = %s);"

        # User input to check for in SQL statement
        userin = (name, address, city, addyZip, public, commercial, propType, owner, size, name)

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, userin)

            # Commit changes to db
            conn.commit()

            # Get result
            result = cursor.fetchall()

            if len(result) > 0:
                # Insert was a success
                conn.close()
                return True
            else:
                # Insert failed
                conn.close()
                return False

        except Exception as e:
            print("ERROR: {}".format(e))
        finally:
            conn.close()

    """
    addItem:
        Adds an item into to the Has table
        Inputs:
            the property ID the item belongs to, and the items name
        Returns:
            True if the insert was successful
            False otherwise
    """
    def addItem(self, propID, name):
        # SQL statement to execute
        sql = "INSERT INTO Has (PropertyID, ItemName) " \
              "VALUES (%s, %s);"

        # User input to check for in SQL statement
        userin = (propID, name)

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, userin)

            # Commit changes to db
            conn.commit()

            # Get result
            result = cursor.fetchall()

            if len(result) > 0:
                # Insert was a success
                conn.close()
                return True
            else:
                # Insert failed
                conn.close()
                return False

        except Exception as e:
            print("ERROR: {}".format(e))
        finally:
            conn.close()