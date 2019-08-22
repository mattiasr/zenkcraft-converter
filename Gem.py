class Gem:
    def __init__(self):
        self.bonus_type = ''
        self.bonus_attribute = ''
        self.bonus_amount = ''

    def __repr__(self):
        return "Type: '{}', Attribute: '{}', Amount: '{}'".format(self.bonus_type, self.bonus_attribute, self.bonus_amount)