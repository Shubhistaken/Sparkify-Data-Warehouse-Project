import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, table_count_queries


def load_staging_tables(cur, conn):
    """
    Loads data from S3 into the staging tables on Redshift using the COPY commands.

    Parameters:
        cur: A cursor object for executing SQL commands.
        conn: A connection object to the Redshift cluster.
    """
    for query in copy_table_queries:
        print(query, '\n')
        cur.execute(query)
        conn.commit()
        print("Staging table load complete.")


def insert_tables(cur, conn):
    """
    Inserts data from staging tables into the final analytics tables and prints row counts.

    Parameters:
        cur: A cursor object for executing SQL commands.
        conn: A connection object to the Redshift cluster.
    """
    for i, query in enumerate(insert_table_queries):
        cur.execute(query)
        conn.commit()

        # Fetch row count after insert
        count_query = table_count_queries[i]
        cur.execute(count_query)
        count = cur.fetchone()[0]
        print(f"Rows in table after insert: {count}\n")


def main():
    """
    Connects to the Redshift cluster using configuration details from dwh.cfg,
    loads data into staging tables, transforms the data by inserting into final tables,
    and then closes the connection.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values())
    )
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
