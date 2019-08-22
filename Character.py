class Character:
    def __init__(self, name, level, realm, realm_class, race):
        self.name = name
        self.level = level
        self.realm = realm
        self.realm_class = realm_class
        self.race = race
        self.items = []

    def __repr__(self):
        return "Name: {}, Level: {}, Realm: {}, Class: {}, Race: {}".format(
            self.name, self.level, self.realm, self.realm_class, self.race)