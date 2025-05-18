from sys import maxsize


class Group:
    def __init__(self, name=None, header=None, id=None):
        self.name = name
        self.header = header
        self.id = id


    def __repr__(self):
        return "%s:%s" % (self.id, self.name)


    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    @classmethod
    def id_or_max(cls, obj):
        return int(obj.id) if obj.id is not None else maxsize