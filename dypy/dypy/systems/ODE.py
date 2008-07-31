class ODE():   
    def __init__(self, name, description=''):
        self.name = name
        self.description = description
    
    def iterate(self, state, parameters, dt=0.01):
        return self.integrate(state, parameters, dt)
    
    def derivative(self, state, parameters):
        assert 0, "must be defined"
    
    def get_parameter_names(self):
        assert 0, "must be defined"
  
    def get_state_names(self):
        assert 0, "must be defined"

    def integrate_euler(self, state, parameters, dt=0.01):
        return state + dt * self.derivative(state, parameters)
    
    def integrate(self, state, parameters, dt=0.01):
        k1 = dt * self.derivative(state, parameters)
        k2 = dt * self.derivative(state + k1/2.0, parameters)
        k3 = dt * self.derivative(state + k2/2.0, parameters)
        k4 = dt * self.derivative(state + k3, parameters)
        
        return state + (k1 + 2.0*k2 + 2.0*k3 + k4)/6.0