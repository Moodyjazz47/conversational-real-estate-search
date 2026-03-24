import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor

from pydantic import BaseModel, field_validator


# ------Pydantic Validation Class------

class DBConfig(BaseModel):
    """

    Enforces pydantic type validation and custom field validators
    """
    host: str
    port: int
    db_name: str
    username: str
    password: str
    min_conn: int = 1
    max_conn: int = 5

    @field_validator('host','db_name','username','password')
    @classmethod
    def str_validation(cls, value):
        if not value.strip():
            raise ValueError('must be a non empty string')
        return value


    @field_validator('port')
    @classmethod
    def port_validation(cls, value:int):
        if value<=0 or value>65535:
            raise ValueError('value is an invalid port type')
        return value


    @field_validator('max_conn')
    @classmethod
    def poolsize_validation(cls, maxconn:int, info ): #maxpool is just variable name instead of 'value'

        minconn = info.data.get('min_conn', 1) #info is the dict where already validated values are stored by Pydantic
        if maxconn < minconn:  # info.data are those actual values, .get() will fetch a certain value (minpool) '1' is
            raise ValueError('maxpool cannot be lesser than minpool') #default value is not fetched, we need minpool to compare with maxpool
        return maxconn



# ------Query Executor Class------


class QueryExecutor:

    def __init__(self, config: DBConfig):
        if not isinstance(config, DBConfig):
            raise TypeError('config must be a DBConfig instance')

        self.config = config
        self.pool = self._createpool()



    def _createpool(self):
        """
        Create and return a psycopg2 connection pool.
        """
        try:
            return SimpleConnectionPool(minconn=self.config.min_conn,
                                        maxconn=self.config.max_conn,
                                        host= self.config.host,
                                        port= self.config.port,
                                        dbname= self.config.db_name,
                                        user= self.config.username,
                                        password=self.config.password,
                                        )
        except psycopg2.Error as e:
            raise RuntimeError('Failed to establish connection to Database') from e


    def _validate_readonly(self, sql:str):
        """
        Ensure the SQL query is read-only.
        Only SELECT queries are allowed.
        """
        if not sql or not isinstance(sql, str):
            raise ValueError('SQL must be a non-empty string')

        normalized_sql = sql.strip().lower()

        if not normalized_sql.startswith('select'):
            raise ValueError('only read-only SELECT queries are allowed')


    def _get_connection(self):
        """
        Borrow a connection from the already established connection pool.
        """
        if not self.pool:
            raise RuntimeError('Connection pool has not been initialized')

        try:
            return self.pool.getconn()

        except psycopg2.Error as e:
            raise RuntimeError('Failed to get db connection from the pool') from e


    def _release_connection(self, conn):
        """
        Return a connection back to the connection pool.
        """
        try:
            self.pool.putconn(conn)
        except psycopg2.Error as e:
            raise RuntimeError('Failed to release connection back to pool') from e



    # -----MAIN PUBLIC API-----

    def execute(self, query: str, params: list | tuple = None) -> list[dict]:
        """
        Execute a read-only SQL query and return results as a list of dicts.
        """

        self._validate_readonly(query)

        conn = None

        try:
            conn = self._get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:

                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                results = cursor.fetchall()

            return results

        except psycopg2.Error as e:
            raise RuntimeError("Database query execution failed") from e

        finally:
            if conn:
                self._release_connection(conn)




