"""
here is the oop area, this should have an optimal and shrunked down version of A1
this module represents a single sensor reading
"""

class Observation:
    pass

class Participant:
    def __init__(self):
        pass

    def participant_id(self):
        pass

    def baseline_hr(self):
        pass

    def baseline_sr(self):
        pass

    def baseline_temp(self):
        pass


class fitnessSession:
    def __init__(self):
        self._observation=list()
        pass

    def add_obs(self, observation: Observation):
        if not isinstance(observation, Observation):
            raise TypeError
        self._observations.append(observation)
        
    def observations(self):
        pass
    def obs_count(self):
        pass

    def isEmpty(self):
        pass

