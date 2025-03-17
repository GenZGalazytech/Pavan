from fastapi import  HTTPException
from models.models import  Message, User,Userlogin
from connect import get_users_collection,get_image_collection
from Controllers.modelcontroller import get_text_embedding
from utils.jwt_utils import create_access_token
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np




users=get_users_collection()
image_collection=get_image_collection()


def register(user: User):
    if(users.find_one({"email": user.email})):
        raise HTTPException(status_code=400, detail="Email already registered")
    result = users.insert_one(dict(user))
    if(result):
        return {"status_code":200, "message": "User created..."}
    else:
        return {"status_code":400, "message": "Registration Failed"}

def login(user:Userlogin):
    data=users.find_one({"email": user.email})
    if(data):
        if(data["password"]==user.password):
            access_token = create_access_token({"sub": user.email})
            # print(access_token)
            return {"status_code": 200, "message": "Login successful", "access_token": access_token, "token_type": "bearer"}
        else:
            return {"status_code":401, "message": "Email/Password is incorrect"}
    else:
        return {"status_code":404, "message": "No User Found"}
# def login(user: Userlogin):
#     data = users.find_one({"email": user.email})
    
#     if not data:
#         raise HTTPException(status_code=404, detail="No User Found")

#     if user.password != data["password"]:
#         raise HTTPException(status_code=401, detail="Email/Password is incorrect")

#     access_token = create_access_token({"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}


def get_all_users():
    data=users.find()
    if(data):
        for d in data:
            print(d)
        return {"status_code":200, "message": "data"}
    else:
        return {"status_code":400, "message":"no data"}
       
def search_images(message : Message):
    query_embedding = get_text_embedding(message.message).reshape(1, -1)

    matches = []
    for user in image_collection.find({"username":message.username}):
        image_url = user["image_url"]
        stored_embedding = np.array(user["embeddings"]).reshape(1, -1)  # Convert back to array

        similarity = cosine_similarity(query_embedding, stored_embedding)[0][0]
        print(similarity)
        if similarity >= 0.26:
            matches.append(image_url)  # Include similarity
        # matches.sort(key=lambda x: x["similarity"], reverse=True)  
        # image_results = [match["image_url"] for match in matches]
        # for image in matches:
        #     print(image)
    return {"reply": "Results", "images": matches}
