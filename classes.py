class Literal:
    def __init__(self, name, sign):
        self.name = name  # integer
        self.sign = sign  # boolean

    def __repr__(self):
        return ("-" if not self.sign else "") + self.name

    def __eq__(self, other):
        if type(other) != Literal:
            return False
        return self.name == other.name and self.sign == other.sign

    def __hash__(self):
      return hash((self.name, self.sign))

class Clause:
    def __init__(self, id, literal_set):
        self.id = id
        self.literal_set = literal_set

    def __repr__(self):
        return f"{self.id}: {str(self.literal_set)}"

    def __eq__(self, other):
        if type(other) != Clause:
            return False
        return self.id == other.id
