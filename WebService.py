import pymysql.cursors


class DBManager:

    # Returns the connection to the database
    def getConnection(self):
        # create connection
        conn = pymysql.connect(
            host='academic-mysql.cc.gatech.edu',
            user='cs4400_team_68',
            password='JQasN9vs'
        )

        return conn

    # Takes the user inputted email and the user inputted password that has already been hashed as params
    # Makes sure that there exists this email and password combination in the database
    # Returns true if there is a match, False otherwise
    def verifyLogin(self, email, hashPass):
        # SQL statement to execute
        sql = "SELECT Email, Password from User WHERE Email = %s AND Password = %s"

        # User input to check for in SQL statement
        userin = (email, hashPass)

        # Create connection
        conn = self.getConnection()

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
        finally:
            conn.close()
