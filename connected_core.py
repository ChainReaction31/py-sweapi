class AbstractSystemPropertiesCore:
    definition: str
    uid: str
    name: str
    description: str
    type: str

    def __init__(self):
        self.definition = "www.test.org/test/plyfile"
        self.uid = "urn:test:plyfilereader"
        self.name = "Test Ply File Reader"
        self.description = "A Test Ply File Reader"

    def get_dict(self):
        return dict([
            ('defintion', self.definition),
            ('name', self.name),
            ('uid', self.uid),
            ('type', self.definition),
            ('description', self.description)
        ])
