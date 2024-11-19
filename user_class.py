import random
import json

used_ids = []


def random_id() -> int:
    # with open('data.json', 'r+') as file:
    #     data = json.load(file)
    #implement adding values to a dictoinary inside json file so they cant repeat id numbers
    random_number = random.randint(0, 156)

    return random_number


def save_data(person) -> bool:
    #person is an object, of class Profile [person.name, person.id, person.level, person.get_cookie_clicks]
    with open('data.json', 'r') as file:
        data = json.load(file)
    for profile in data:
        if profile.get("name") == person.name:
            index = data.index(profile)
            profile["attributes"]["id"] = person.id
            profile["attributes"]["level"] = person.level
            profile["attributes"]["cookies"] = person.get_cookie_clicks
            data[index] = profile
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Saved user profile {person.name}")
            return True
    return False


class Profile:
    def __init__(self, name: str, id: int, level: int, cookies: int):
        self.name = name
        self.id = id
        self.level = level
        self._cookies = cookies

    def __str__(self):
        return f"Name: {self.name}, ID: {self.id}, Level: {self.level}, Cookies: {self._cookies}"

    def get_random_id(self):
        self.id = random_id()
        return self.id

    @property
    def get_cookie_clicks(self):
        return self._cookies

    def increment_cookie_clicks(self):
        self._cookies += 1

    def set_cookie_clicks(self, value):
        self._cookies += value

    def level_up(self):
        self.level += 1
        self._cookies = 0
        return f"New level is {self.level}"
