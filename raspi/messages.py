class Messages(list):
    def __init__(self, capacity=10):
        self.capacity = capacity
        
    def append(self, item):
        if len(self) >= self.capacity:
            del self[0]
        super(Messages, self).append(item)
