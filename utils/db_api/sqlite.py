import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int primary key,
            Name varchar(255) NOT NULL,
            profil varchar(255) NOT NULL,
            block INTEGER default 0
            );
"""
        self.execute(sql, commit=True)

    def __create_table_yotube(self):
        sql = """
            CREATE TABLE Youtube (
                id int NOT NULL,
                url varchar(255) NOT NULL,
                fps varchar(5) NOT NULL,
                typ varchar(50) NOT NULL,
                date varchar(50) NOT NULL
                );
    """
        self.execute(sql, commit=True)

    def __create_table_instagram(self):
        sql = """
            CREATE TABLE Instagram (
                id int NOT NULL,
                url varchar(255) NOT NULL,
                date varchar(50) NOT NULL
                );
    """
        self.execute(sql, commit=True)

    def add_yotube(self, id: int, url: str, fps: str, typ: str, date: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"
        try:
            self.__create_table_yotube()
        except Exception as e:
            print(e)
        sql = """
        INSERT INTO Youtube(id, url, fps, typ, date) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, url, fps, typ, date), commit=True)

    def add_instagram(self, id: int, url: str, date: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"
        try:
            self.__create_table_instagram()
        except Exception as e:
            print(e)
        sql = """
           INSERT INTO Instagram(id, url, date) VALUES(?, ?, ?)
           """
        self.execute(sql, parameters=(id, url, date), commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, profil: str, block: int = 0):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, Name, profil, block) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, profil, block), commit=True)

    def __add_admin(self, name: str, per: int = 0):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(name, per) VALUES(?, ?)
        """
        self.execute(sql, parameters=(name, per), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def __select_users(self,ID):
        sql = f"SELECT * FROM Users WHERE id = {ID}"
        return self.execute(sql, fetchall=True)

    def block_test(self,ID) -> bool:
        sql = self.__select_users(ID)
        for i in sql:
            print(i[0])
            print(len(sql))
            if i[0]==ID:
                if i[3]==1:
                    return True
                else:
                    return False
        return False

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)
    
    def count_Instagram(self):
        return self.execute("SELECT COUNT(*) FROM Instagram;", fetchone=True)
    
    def count_Youtube(self):
        return self.execute("SELECT COUNT(*) FROM Youtube;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def updata_user(self, id, val):
        print('updata')
        self.execute(f"UPDATE Users SET block={val} WHERE id={id};", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")
