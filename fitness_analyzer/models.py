"""
here is the oop area, this should have an optimal and shrunked down version of A1
this module represents a single sensor reading
"""
from validation import validate_participant_id, validate_session_id


class Participant:
    """
    this class acsesses and stores Personal information from the user
    """
    def __init__(self,participant_id, name, baseline_hr, baseline_skin, baseline_temp):
            

        self._participant_id = validate_participant_id(participant_id)
        self._name = name
        self._baseline_hr = baseline_hr
        self._baseline_skin = baseline_skin
        self._baseline_temp = baseline_temp

       
    @classmethod
    def instanciate_row(cls, row):
        return cls(
            participant_id=row["participant_id"],
            name= row.get("name",""),
            baseline_hr=float(row["baseline_heart_rate"]),
            baseline_skin=float(row["baseline_skin_response"]),
            baseline_temp=float(row["baseline_temp"])
        )
    

    @property
    def ID(self):
        return self._participant_id

    @property
    def Name(self):
        return self._name

    @property
    def Baseline_HR(self):
        return self._baseline_hr


    @property
    def Baseline_Skin(self):
        return self._baseline_skin


    @property
    def Baseline_Temp(self):

        return self._baseline_temp


class Observation:
    def __init__(self, timestamp, heart_rate, skin_response,
                 temperature, activity_level, signal_quality):
        self._timestamp = timestamp
        self._heart_rate = heart_rate
        self._skin_response = skin_response
        self._temperature = temperature
        self._activty_level = activity_level
        self._signal_quality = signal_quality

    @classmethod
    def from_row(cls, validated_row):
        return cls(
            timestamp = validated_row["timestamp"],
            heart_rate = validated_row["heart_rate"],
            skin_response = validated_row["skin_response"],
            temperature = validated_row["temperature"],
            activity_level = validated_row["activity_level"],
            signal_quality = validated_row["signal_quality"]
        )

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def heart_rate(self):
        return self._heart_rate

    @property
    def skin_response(self):
        return self._skin_response

    @property
    def temperature(self):
        return self._temperature

    @property
    def activity_level(self):
        return self._activty_level

    @property
    def signal_quality(self):
        return self._signal_quality




class fitnessSession:
    def __init__(self, session_id, participant):
        self._session_id=validate_session_id(session_id)
        self._participant=participant
        self._observation=list()

    def add_obs(self, observation):
        if not isinstance(observation, Observation):
            raise TypeError(
                f"expectied an Observation, got {type(observation).__name__}"
            )
        self._observations.append(observation)


    @property
    def session_id(self):
        return self._session_id

    @property
    def participant(self):
        return self._participant

    @property
    def observation(self):
        return sorted(self._observation, key=lambda obs: obs.timestamp)
    
    @property
    def obsCount(self):
        return len(self._observation)

    @property
    def isEmpty(self):
        return self.obsCount==0

    def values(self, metric_name):
        return[getattr(obs, metric_name) for obs in self._observation]




