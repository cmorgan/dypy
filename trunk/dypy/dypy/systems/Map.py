class Map:
    def __init__(self, name, description=''):
        self.name = name
        self.description = description
    
    def iterate(self, state, parameters):
        assert 0, "must be defined"
    
    def derivative(self, state, parameters):
        assert 0, "must be defined"

    def get_parameter_names(self):
        assert 0, "must be defined"

    def get_state_names(self):
        assert 0, "must be defined"