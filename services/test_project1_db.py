import pytest
import psycopg2
from database.PROJECT1_db import *

@pytest.fixture
def db_cursor():
    conn = psycopg2.connect(
        dbname="project1",
        user="postgres",
        password="6068",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    yield cur, conn
    cur.close()
    conn.close()

def test_assign_user(db_cursor):
    db_cursor.cursor()
    assign_user("pytest_user2", "pytest_pass")
    db_cursor.commit()

    result = return_user_id("pytest_user2")
    assert result is not None


def test_add_balance_db(db_cursor):
    cur, conn = db_cursor

    assign_user("pytest_user2", "Password@123")
    conn.commit()

    update_balance("pytest_user2", 1000)
    conn.commit()

    user_id = return_user_id("pytest_user2")
    cur.execute("SELECT balance FROM USERS WHERE user_id = %s", (user_id,))
    balance = cur.fetchone()[0]
    assert balance == 1000