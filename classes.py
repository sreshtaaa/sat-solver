class Literal:
    def __init__(self, name, sign):
        self.name = name  # integer
        self.sign = sign  # boolean

    def __repr__(self):
        return ("-" if not self.sign else "") + str(self.name)
        
    def __eq__(self, other):
        if type(other) != Literal:
            return False
        return self.name == other.name and self.sign == other.sign

    def __hash__(self):
      return hash((self.name, self.sign))

class Clause:
    def __init__(self, cid, literal_set):
        self.cid = cid
        self.literal_set = literal_set

    def __repr__(self):
        return f"{self.cid}: {str(self.literal_set)}"

    def __eq__(self, other):
        if type(other) != Clause:
            return False
        return self.cid == other.cid
    
    def __hash__(self): 
        return hash((self.cid))
