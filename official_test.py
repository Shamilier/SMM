import requests
access_token = 'EAALNj3P9lggBO81OrlZBWKgROwUy5iggWIm8TMCkEhUqcPXLQjxaZBAetwt9lhIhc3D2m6imEVZC5UqNbqPrmSd9fP8xG8D8HTYaJIMmZCZBM6nZAr1Pp1GtbhUPvCe8ZBIaJpNhrW5dCBj1sg0NdZBTO4ULWqKvZCzJHUf6N7bzVbhOzkDv4DzDssxJkLwVubGFYUGAzNdqpgd8CCWJfLal8AnJTldBHL65P9YVeGDZCeH5BdIdLSyRCaasZCZCxmhSPwZDZD'
user_id = '506146865101740'  # ID пользователя Instagram
url = f"https://graph.facebook.com/{user_id}?fields=id&access_token={access_token}"

response = requests.get(url)
print(response)
data = response.json()
print(data)