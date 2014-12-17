import time

class Statechart(object):
    """
    Base class for statecharts.
    
    Example:
        
        class StatechartChild(Statechart):
            # ...
        
        wm = connect()
        statechart = StatechartChild(wm)
        statechart.run()
    """
    class State(object):
        def __init__(self):
            self.should_exit = False  # exit after completing iteration
    
    class Inputs(object):
        """
        This class is for gathering the input data from the sensors.
        
        update_state() uses this to modify the State object.
        """
        pass
            
        
    def __init__(self, cycle=0.2):
        self.state = self.State()
        self.inputs = self.Inputs()
        
        self.cycle = cycle 
        self.should_exit = False  # exit immediately
    
    def run(self):
        while not self.iterate():
            time.sleep(self.cycle)
        
    def iterate(self):
        self.iteration_starting()
        if self.should_exit: return self.should_exit
        
        self.read_inputs()
        if self.should_exit: return self.should_exit
            
        self.update_state()
        if self.should_exit: return self.should_exit
            
        self.perform_actions()
        if self.should_exit: return self.should_exit
        
        self.iteration_finishing()
        
        return self.state.should_exit or self.should_exit
    
    def read_inputs(self):
        """
        Collect input data to self.inputs.
        """
        pass
        
    def update_state(self):
        """
        Read self.inputs and update self.state.
        """
        pass
    
    def perform_actions(self):
        """
        Control actuators.
        """
        pass
    
    def iteration_starting(self):
        """
        For UI output. Called before update_state().
        """
        pass

    def iteration_finishing(self):
        """
        For UI output. Called after perform_actions().
        """
        pass

class Messages(list):
    def __init__(self, capacity=10):
        self.capacity = capacity
        
    def append(self, item):
        if len(self) > self.capacity:
            del self[0]
        super(Messages, self).append(item)
        
