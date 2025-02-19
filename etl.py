import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, table_count_queries


def load_staging_tables(cur, conn):
    
    for query in copy_table_queries:
        print(query, '\n')
        cur.execute(query)
        conn.commit()
        print("done")

def insert_tables(cur, conn):
    for i, query in enumerate(insert_table_queries):
        cur.execute(query)
        conn.commit()

        # Fetch row count after insert
        count_query = table_count_queries[i]
        cur.execute(count_query)
        count = cur.fetchone()[0]
        print(f"Rows in table after insert: {count}\n")


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
