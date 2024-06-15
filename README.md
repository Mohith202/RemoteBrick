Create virtal environment : **python3 -m venv envi**
Activate it: **envi\Scripts\activate**

In Virtual environment install required packages using cmd:** pip install fastapi uvicorn pymongo pydantic bcrypt
**
Pull all files from repository:

**In database.py change username, password and URI of you mongodb atlas.**

Start the application: Uvicorn main:app --reload
1.	Post- http://127.0.0.1:8000/register
JSON -{
     "username": "john_doe",
    "email": "john.doe@exampl2e.com",
    "password": "securepassword"
}

2.	POST- http://127.0.0.1:8000/login
JSON-{
    "email": "john.doe@exampl2e.com",
    "password": "securepassword"
}
3.	POST-http://127.0.0.1:8000/link_id
JSON-
{
    "email":"john@example3.com",
    "password":"securepassword",
    "linked_id":"12345"
}

4.	POST -http://127.0.0.1:8000/update_user_details/12345
JSON-{
    "linked_id":"12345",
    "full_name": "Mohith",
    "age": 45,
    "address": "Hyderabad"
}

5.	GET-http://127.0.0.1:8000/user_with_details/john@example3.com
6.	Delete -http://127.0.0.1:8000/delete_user/ john@example3.com

