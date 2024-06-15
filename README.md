Create virtal environment : **python3 -m venv envi**
Activate it: **envi\Scripts\activate**

In Virtual environment install required packages using cmd:**pip install fastapi uvicorn pymongo pydantic bcrypt**

Pull all files from the repository.

**In database.py change username, password and URI of you mongodb atlas.**

Start the application: **uvicorn main:app --reload**

**For better experience use Postman**

1.	Post request- http://127.0.0.1:8000/register
JSON -{
     "username": "john_doe",
    "email": "john.doe@exampl2e.com",
    "password": "securepassword"
}

2.	POST request - http://127.0.0.1:8000/login
JSON-{
    "email": "john.doe@exampl2e.com",
    "password": "securepassword"
}
3.	POST request -http://127.0.0.1:8000/link_id
JSON-
{
    "email":"john@example3.com",
    "password":"securepassword",
    "linked_id":"12345"
}

4.	POST request -http://127.0.0.1:8000/update_user_details/12345
JSON-{
    "linked_id":"12345",
    "full_name": "Mohith",
    "age": 45,
    "address": "Hyderabad"
}

5.	GET request-http://127.0.0.1:8000/user_with_details/john@example3.com
6.	Delete  request -http://127.0.0.1:8000/delete_user/ john@example3.com

