from fastapi import APIRouter, HTTPException
from models import User, UserLogin, LinkID, UserDetails
from database import db
from helpers import hash_password, verify_password

router = APIRouter()

# Registration endpoint
@router.post("/register")
def register(user: User):
    existing_user = db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    db.users.insert_one(user_dict)
    return {"message": "User registered successfully"}

# Login endpoint
@router.post("/login")
def login(user: UserLogin):
    db_user = db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"message": "Login successful"}

# Linking ID endpoint
@router.post("/link_id")
def link_id(linked_id: LinkID):
    us = db.users.find_one({"email": linked_id.email})
    if us:
        result = db.users.update_one(
            {"email": linked_id.email},
            {"$set": {"linked_id": linked_id.linked_id}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="User not found or ID not updated")
    else:
        raise HTTPException(status_code=400, detail="User not found")
    return {"message": "ID linked successfully"}

# Function to update user details in 'user_details' collection
@router.post("/update_user_details/{link_id}")
def update_user_details(link_id: str, user_details: UserDetails):
    # Check if the user exists in 'users' collection
    existing_user = db.users.find_one({"linked_id": link_id})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert user_id to ObjectId for storing in 'user_details' collection
    user_details_dict = user_details.dict()

    # Upsert (update or insert) user details in 'user_details' collection
    result = db.user_details.update_one(
        {"linked_id": link_id},
        {"$set": user_details_dict},
        upsert=True
    )

    if result.modified_count == 0 and result.upserted_id is None:
        raise HTTPException(status_code=500, detail="Failed to update user details")

    # Update the users collection to store the user_details ID
    db.users.update_one(
        {"linked_id": link_id},
        {"$set": {"user_details_id": str(result.upserted_id) if result.upserted_id else str(db.user_details.find_one({"linked_id": link_id})["_id"])}}
    )

    return {"message": "User details updated successfully"}

# Function to join data from multiple collections
@router.get("/user_with_details/{email}")
def get_user_with_details(email: str):
    # Fetch user details from the 'users' collection
    user = db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Perform an aggregation pipeline to join 'users' and 'user_details'
    pipeline = [
        {
            "$match": {"email": email}
        },
        {
            "$lookup": {
                "from": "user_details",
                "localField": "linked_id",
                "foreignField": "linked_id",
                "as": "user_details"
            }
        },
        {
            "$unwind": "$user_details"  # If 'user_details' is an array, unwind to get individual documents
        },
        {
            "$project": {
                "_id": 0,  # Exclude '_id' field from the output
                "username": 1,
                "email": 1,
                "linked_id": 1,
                "full_name": "$user_details.full_name",
                "age": "$user_details.age",
                "address": "$user_details.address"
            }
        }
    ]

    # Execute the aggregation pipeline
    result = list(db.users.aggregate(pipeline))
    if not result:
        raise HTTPException(status_code=404, detail="User details not found")

    return result[0]  # Return the first (and only) result as a dictionary

# Chain delete endpoint
@router.delete("/delete_user/{email}")
def delete_user(email: str):
    user = db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.user_details.delete_many({"linked_id": user["linked_id"]})
    db.users.delete_one({"email": email})
    return {"message": "User and all associated data deleted successfully"}
