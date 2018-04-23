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
        Makes sure that there exists this username and password combination in the User table
        Inputs:
            Username the user entered and the hashed string of the password the user inputted
        Returns:
            True if there is a match in the db
            False otherwise
    """
    def verifyLogin(self, username, hashPass):
        # SQL statement to execute
        sql = "SELECT Username, Password from User WHERE Username = %s AND Password = %s;"

        # User input to check for in SQL statement
        userin = (username, hashPass)

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
                return True
            else:
                # No match
                return False
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getUserType:
        Gets the user type of the current user
        Only call this after a username is verified
        Inputs:
            The current users username
        Returns:
            The type of user the user is
    """
    def getUserType(self, username):
        # SQL statement to execute
        sql = "SELECT UserType from User WHERE Username = %s;"

        # User input to check for in SQL statement
        userin = (username)

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
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
            getEmail:
                Gets the email of the current user
                Only call this after a username is verified
                Inputs:
                    The current users username
                Returns:
                    The email of this user
            """
    def getEmail(self, username):
        # SQL statement to execute
        sql = "SELECT Email from User WHERE Username = %s;"

        # User input to check for in SQL statement
        userin = (username)

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
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
        checkEmail:
            Checks if email is already taken in the User table
            Inputs:
                Email to check for
            Returns:
                True if the email already exists
                False if not
        """
    def checkEmail(self, email):
        # SQL statement to execute
        sql = "SELECT * FROM User WHERE Email = %s;"

        # User input to check for in SQL statement
        userin = (email)

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, userin)

            # Get result
            result = cursor.fetchall()

            if len(result) > 0:
                # Email already exists in User table
                return True
            else:
                # Email doesn't exist
                return False

        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    checkUsername:
        Checks if username is already taken in the User table
        Inputs:
            Username to check for
        Returns:
            True if the username already exists
            False if not
    """
    def checkUsername(self, username):
        # SQL statement to execute
        sql = "SELECT * FROM User WHERE Username = %s;"

        # User input to check for in SQL statement
        userin = (username)

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, userin)

            # Get result
            result = cursor.fetchall()

            if len(result) > 0:
                # Username already exists in User table
                return True
            else:
                # Username doesn't exist
                return False
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    registerNewUser:
        Adds new user to the User table
        Inputs:
            email, username, already hashed password, and the type of user
        Returns:
            true if the insert was successful
            (should always be successful if checkEmail and checkUsername are called before this)
    """
    def registerNewUser(self, email, username, hashPass, usertype):
        # SQL statement to execute
        sql = "INSERT INTO User (Email, Username, Password, UserType) " \
              "VALUES (%s, %s, %s, %s); " \

        # User input to check for in SQL statement
        userin = (email, username, hashPass, usertype)

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            rowsAffected = cursor.execute(sql, userin)

            # Commit changes to db
            conn.commit()

            # Check that the query was successful
            if rowsAffected > 0:
                return True
            else:
                return False
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
        checkPropertyNmae:
            Checks if property name is already taken in the Property table
            Inputs:
                Property name to check for
            Returns:
                True if the property name already exists
                False if not
    """
    def checkPropertyName(self, name):
        # SQL statement to execute
        sql = "SELECT * FROM Property WHERE Name = %s;"

        # User input to check for in SQL statement
        userin = (name)

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, userin)

            # Get result
            result = cursor.fetchall()

            if len(result) > 0:
                # Property name already exists in User table
                return True
            else:
                # Property name doesn't exist
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
        sql = "INSERT INTO Property (Name, Size, IsCommercial, IsPublic, Street, City, Zip, PropertyType, Owner)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"

        # User input to check for in SQL statement
        userin = (name, float(size), commercial, public, address, city, addyZip, propType, owner)

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            rowsAffected = cursor.execute(sql, userin)

            # Commit changes to db
            conn.commit()

            # Check that the query was successful
            if rowsAffected > 0:
                return True
            else:
                return False
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getMaxPropID:
        Returns the current max ID in Property table so we can create a new
    """
    def getMaxPropID(self):
        # SQL statement to execute
        sql = "SELECT MAX(ID) FROM Property"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql)

            # Get result
            result = cursor.fetchone()

            if result is None:
                return 1
            else:
                return result

        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getPropertyID:
        Gets the property ID associated with the property name
        Inputs:
            The property name
        Returns:
            The property ID
    """
    def getPropertyID(self, propName):
        # SQL statement to execute
        sql = "SELECT ID from Property WHERE Name = %s;"

        # User input to check for in SQL statement
        userin = (propName)

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
            print(logging.exception("error happened"))
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
            rowsAffected = cursor.execute(sql, userin)

            # Commit changes to db
            conn.commit()

            # Check that the query was successful
            if rowsAffected > 0:
                return True
            else:
                return False
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getApprovedVegetables:
        Returns a list of approved vegetables
    """
    def getApprovedVegetables(self):
        # SQL statement to execute
        sql = "SELECT Name FROM FarmItem WHERE IsApproved = 1 AND Type = %s"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, "VEGETABLE")

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item[0] for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getApprovedFruits:
       Returns a list of approved friuts
    """
    def getApprovedFruits(self):
        # SQL statement to execute
        sql = "SELECT Name FROM FarmItem WHERE IsApproved = 1 AND Type = %s"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, "FRUIT")

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item[0] for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getApprovedFlowers:
         Returns a list of approved flowers
    """
    def getApprovedFlowers(self):
        # SQL statement to execute
        sql = "SELECT Name FROM FarmItem WHERE IsApproved = 1 AND Type = %s"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, "FLOWER")

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item[0] for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getApprovedNuts:
        Returns a list of approved nuts
    """
    def getApprovedNuts(self):
        # SQL statement to execute
        sql = "SELECT Name FROM FarmItem WHERE IsApproved = 1 AND Type = %s"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, "NUT")

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item[0] for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getApprovedAnimals:
        Returns a list of approved animals
    """
    def getApprovedAnimals(self):
        # SQL statement to execute
        sql = "SELECT Name FROM FarmItem WHERE IsApproved = 1 AND Type = %s"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, "ANIMAL")

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item[0] for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getApprovedVegetables:
        Returns a list of approved vegetables
    """
    def getApprovedVegetables(self):
        # SQL statement to execute
        sql = "SELECT Name FROM FarmItem WHERE IsApproved = 1 AND Type = %s"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, "VEGETABLE")

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item[0] for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    ####UNAPPROVED STARTS HERE


    """
    getApprovedVegetables:
        Returns a list of approved vegetables
    """
    def getUnapprovedVegetables(self):
        # SQL statement to execute
        sql = "SELECT Name FROM FarmItem WHERE IsApproved = 0 AND Type = %s"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, "VEGETABLE")

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item[0] for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getUnapprovedFruits:
       Returns a list of unapproved friuts
    """
    def getUnapprovedFruits(self):
        # SQL statement to execute
        sql = "SELECT Name FROM FarmItem WHERE IsApproved = 0 AND Type = %s"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, "FRUIT")

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item[0] for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getUnapprovedFlowers:
         Returns a list of unapproved flowers
    """
    def getUnapprovedFlowers(self):
        # SQL statement to execute
        sql = "SELECT Name FROM FarmItem WHERE IsApproved = 0 AND Type = %s"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, "FLOWER")

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item[0] for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getUnapprovedNuts:
        Returns a list of unapproved nuts
    """
    def getUnapprovedNuts(self):
        # SQL statement to execute
        sql = "SELECT Name FROM FarmItem WHERE IsApproved = 0 AND Type = %s"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, "NUT")

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item[0] for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getUnapprovedAnimals:
        Returns a list of approved animals
    """
    def getUnapprovedAnimals(self):
        # SQL statement to execute
        sql = "SELECT Name FROM FarmItem WHERE IsApproved = 0 AND Type = %s"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, "ANIMAL")

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item[0] for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getOwnerProperties:
        Gets all of the properties owned by an owner
        Inputs:
            The username of the owner
        Return:
            A list of the properties
    """
    def getOwnerProperties(self, username):
        # SQL statement to execute
        sql = "SELECT * FROM Property WHERE Owner = %s;"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, username)

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    def getPropertyDetails(self, propID):
        # SQL statement to execute
        sql = "SELECT * FROM Property WHERE ID = %s;"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, propID)

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:

            conn.close()

    def getPublicProperties(self):
        # SQL statement to execute
        sql = "SELECT * FROM Property WHERE IsPublic = %s AND ApprovedBy <> %s ;"

        userin = (1, 'NULL')

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, userin)

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:

            conn.close()

    def getPropertyDetails(self, propID):
        # SQL statement to execute
        sql = "SELECT * FROM Property WHERE ID = %s;"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
        # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, propID)

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    def getVisitHistory(self, username):
        # SQL statement to execute
        sql = "SELECT Name, VisitDate, Rating FROM Visit JOIN Property ON ID = PropertyID AND Username = %s"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, username)

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:

            conn.close()

    def getOwners(self):
        # SQL statement to execute
        sql = "SELECT Email, Username, COUNT(Owner) AS NumProp FROM User JOIN Property ON Username = Owner GROUP BY Owner"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql)

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    def getVisitors(self):
        # SQL statement to execute
        sql = "SELECT User.Email, User.Username, COUNT(Visit.Username) as LoggedVisits FROM User JOIN Visit ON Visit.Username = User.Username GROUP BY Visit.Username"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql)

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:

            conn.close()

    def getConfirmedProps(self):
        # SQL statement to execute
        sql = "SELECT Property.Name, Property.Street as Address, Property.City, Property.Zip, Property.Size, Property.PropertyType AS Type, Property.IsPublic as Public, Property.IsCommercial as Commercial, Property.ID, Property.ApprovedBy as VerifiedBy,  AVG(Visit.Rating) AS AvgRating FROM Property LEFT JOIN Visit ON Property.ID = Visit.PropertyID WHERE ApprovedBy IS NOT NULL GROUP BY Property.ID"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql)

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:

            conn.close()

    def getUnconfirmedProps(self):
        # SQL statement to execute
        sql = "SELECT Property.Name, Property.Street as Address, Property.City, Property.Zip, Property.Size, Property.PropertyType AS Type, Property.IsPublic as Public, Property.IsCommercial as Commercial, Property.ID, Property.Owner FROM Property WHERE ApprovedBy IS NULL"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql)

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:

            conn.close()

    """
        getOtherOwnerProperties:
            Gets all the confirmed properties owned by other owners; ordered by name asc
            Inputs:
                Current owners username
            Returns:
                A list of all the other properties
        """
    def getOtherOwnerProperties(self, username):
        # SQL statement to execute
        sql = "SELECT * FROM Property WHERE Owner <> %s AND ApprovedBy <> %s ORDER BY Name ASC;"

        # Format user input to add to sql statement
        userin = (username, 'NULL')

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, userin)

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    """
    getPropertyCrops:
        Gets the list of crops for a property
        Inputs:
            The property ID
        Returns:
            A list of crops associated with this property
    """
    def getPropertyCrops(self, propID):
        # SQL statement to execute
        sql = "SELECT ItemName FROM Has WHERE PropertyID = %s"

        # Create connection
        conn = DBManager.getConnection(self)

        try:
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, propID)

            # Get result
            result = cursor.fetchall()

            # Put it in a list
            resultList = [item[0] for item in result]

            return resultList
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()

    #approve crops
    def approveCrop(self, name):
        # SQL statement to execute
        print (name, "here")
        sql = " UPDATE FarmItem SET IsApproved = 1 WHERE Name = %s"

        # Create connection
        conn = DBManager.getConnection(self)
        cropin = (name)
        try:
            # Execute query
            cursor = conn.cursor()

            rowsAffected = cursor.execute(sql, cropin)

            # Commit changes to db
            conn.commit()

            # Check that the query was successful
            if rowsAffected > 0:
                print('done')
                return True

            else:
                print('not done')
                return False
        except Exception as e:
            print("ERROR: {}".format(e))
            print(logging.exception("error happened"))
        finally:
            conn.close()
