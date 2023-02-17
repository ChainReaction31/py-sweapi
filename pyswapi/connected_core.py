class SystemPropertiesCore:

    def __init__(self, definition, uid, name, description):
        """
            :param definition: URI for the ontological definition for system
            :param uid: the unique ID of the system
            :param name: the human-readable name of the system
            :param description: a brief description of the system
        """

        self.definition = "www.test.org/test/plyfile"
        self.uid = "urn:test:plyfilereader"
        self.name = "Test Ply File Reader"
        self.description = "A Test Ply File Reader"

        self.definition = definition
        self.uid = uid
        self.name = name
        self.description = description
        self.type = self.definition

    def get_dict(self):
        return dict([
            ('definition', self.definition),
            ('name', self.name),
            ('uid', self.uid),
            ('type', self.definition),
            ('description', self.description)
        ])
