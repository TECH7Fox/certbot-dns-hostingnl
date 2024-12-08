import requests



# url = f"https://api.hosting.nl/domains"

# response = requests.get(
#     url,
#     headers={
#         "API-TOKEN": "ea37265aa6ac5e7cc113bebae51d83af576cb55d08e9a7a6259918249129d974",
#         "Content-Type": "application/json"
#     },
# )

# print(response.status_code)
# print(response.text)
# response.raise_for_status()


url = f"https://api.hosting.nl/domains/tech7fox.nl/dns"
data = [
    {
        'name': "tech7fox.nl",
        'type': 'TXT',
        'content': '"test"',
        'ttl': "3600",
        'prio': "0",
    }
]
print(data)

response = requests.post(
    url,
    headers={"API-TOKEN": "ea37265aa6ac5e7cc113bebae51d83af576cb55d08e9a7a6259918249129d974"},
    json=data,
)
print(response.status_code)
print(response.text)
response.raise_for_status()
