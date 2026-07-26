class DetectionResults:

    def __init__(self):
        self.objects = []

    def update(self, detections):
        self.objects = detections

    def get(self):
        return self.objects

    def clear(self):
        self.objects = []


results = DetectionResults()
