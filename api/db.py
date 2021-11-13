import psycopg2
from psycopg2 import sql
from sql_scripts import get_price_by_id_period

DB_CONN = 'postgresql://wb:password@82.148.28.184:5432/test'


def get_price(ecom_id, start_date, end_date):
    conn = psycopg2.connect(DB_CONN)

    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) FROM ecom")
    # cur.execute(sql.SQL("SELECT COUNT(1) FROM {}").format(sql.Identifier('ecom')))
    # cur.execute(get_price_by_id_period, (ecom_id, start_date, end_date))
    rows = cur.fetchall()

    print(rows)
    cur.close()
    conn.close()

