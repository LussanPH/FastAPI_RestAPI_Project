import requests

header = {
    "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzgwMjQwNDM5fQ.aCeNrU9zsLeMN23k8lQeH5xb2qd7PWeFov_v52dxH7Y"
}

response = requests.get("http://127.0.0.1:8000/auth/refresh", headers=header)
print(response.json())