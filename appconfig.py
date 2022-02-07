import platform

where = platform.uname().release.find("aws")

if where == -1:
    # Local.
    config = {
        "host": "127.0.0.1",
        "database": "feedbackDB",
        "user": "developer",
        "password": "leaderpasswd",
    }
else:
    # Not on PA.
    config = {
        "host": "C00246498.mysql.pythonanywhere-services.com",
        "database": "********", #hidden account details
        "user": "********",
        "password": "********", 
    }  # pragma: no cover
