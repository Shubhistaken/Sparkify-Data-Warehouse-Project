import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops each table in the Redshift cluster using the DROP TABLE queries.

    Parameters:
        cur: A cursor object for executing SQL commands.
        conn: A connection object to the Redshift cluster.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates tables in the Redshift cluster using the CREATE TABLE queries.

    Parameters:
        cur: A cursor object for executing SQL commands.
        conn: A connection object to the Redshift cluster.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Connects to the Redshift cluster using configuration details in dwh.cfg,
    drops existing tables, creates new tables, and then closes the connection.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values())
    )
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
