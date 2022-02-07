import DBcm

from appconfig import config


def test_running_locally():
    """ Check to ensure the config is running for the local settings."""
    assert config["host"] == "127.0.0.1"


def get_db_count():
    """ Connect to the database and return number of rows in the addrs table."""
    with DBcm.UseDatabase(config) as db:
        SQL = "select count(*) from feedbacks"
        db.execute(SQL)
        results = db.fetchall()
    return results[0][0]  # Remember: we get back a list of tuples from fetchall.


def test_count_increase(client, clean_up_db):
    """ Check to ensure the number of rows in the database incremented by 1."""
    initial_count = get_db_count()
    form_data = {
        "name": "Tester Abc 1",
        "email": "tester@abc1.com",
        "message": "1 This is test message.",
    }
    # Send the data to webapp using the FORM's URL.
    client.post("/savedata", data=form_data)
    new_count = get_db_count()
    assert new_count == initial_count + 1


def test_last_row(client, clean_up_db):
    """ Is the last row of data equal to what was submitted via the form? """
    form_data = {
        "name": "Tester Abc 2",
        "email": "tester@abc2.com",
        "message": "2 This is test message.",
    }
    # Send the data to webapp using the FORM's URL.
    client.post("/savedata", data=form_data)
    with DBcm.UseDatabase(config) as db:
        SQL = """
            select name, email, message
            from feedbacks
            order by id desc
            limit 1
        """
        db.execute(SQL)
        results = db.fetchall()
    assert results[0][0] == (form_data["name"])
    assert results[0][1] == form_data["email"]
    assert results[0][2] == form_data["message"]
