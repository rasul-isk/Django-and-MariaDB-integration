from flask import request
from datetime import datetime


def test_up(client):
    """ Test to see of the server is up. """
    assert client.get("/").status_code == 200
    assert client.get("/aboutme").status_code == 200
    assert client.get("/CV").status_code == 200
    assert client.get("/hobbies").status_code == 200
    assert client.get("/feedback").status_code == 200
    assert client.get("/computing").status_code == 200
    assert client.get("/computing/softdev").status_code == 200
    assert client.get("/computing/VR").status_code == 200
    assert client.get("/computing/IT").status_code == 200
    assert client.get("/recent").status_code == 200


def test_missing(client):
    """ Test to see an appropriate response for a missing URL. """
    assert client.get("/missing").status_code == 404


def test_correct_form(client):
    """ Grab the home page, check for 200 code (all ok), then check to
        see if we have received the correct form and that the response is
        a HTML page.
    """
    response = client.get("/feedback")
    assert response.status_code == 200
    # Remember: response.data is a binary text version of the HTML page.
    assert (
        bytes('<form action="/savedata" method="post">', encoding="utf-8")
        in response.data
    )
    assert "<!DOCTYPE html>" in response.get_data(True)


def test_form_operation(client, clean_up_db):
    """ Create some test/sample data, then POST the data to the server.  Ensure
        the request is using POST, then look for a 200 (all ok) status code.  Get the 
        response, check for a valid HTML page, then check that the submitted form data
        was received then send back to the browser in the response.
    """
    form_data = {
        "name": "Tester Abc",
        "email": "tester@abc.com",
        "message": "This is test message.",
    }
    response = client.post("/savedata", data=form_data)
    assert request.method == "POST"
    assert response.status_code == 200
    assert "<html>" in response.get_data(True)
    assert form_data["name"] in response.get_data(True)
    assert form_data["message"] in response.get_data(True)
