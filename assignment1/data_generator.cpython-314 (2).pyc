"""
code
"""

#functions


def majority(l1, target):
    if l1.count(target) >= len(l1)/2:
        return True
    else:
        return False


def Downward_trend(valid_dataset, metric_key, thresheold=0.85):

    trend_results = []

    for session in valid_dataset:
        # 1. Extract valid numerical values for the metric from this session
        data = [
            reading[metric_key]
            for reading in session
            if isinstance(reading, dict) and reading.get(metric_key) is not None
        ]

        total_pairs = 0
        reduction_pairs = 0

        # 2. Count pairwise reductions within the session
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                total_pairs += 1
                if data[j] < data[i]:
                    reduction_pairs += 1

        # 3. Determine if session meets the threshold ratio
        if total_pairs == 0:
            trend_results.append(False)
        else:
            is_downward = (reduction_pairs / total_pairs) > thresheold
            trend_results.append(is_downward)

    return trend_results


def matching_lists(*truthy_lists):

 #   return [all(element == items[0] for element in items) for items in zip(*truthy_lists)]
    return [all(items) for items in zip(*truthy_lists)]


#text functions*

def suportive_messages(assign1):
    messages=["rest is important!",
              "Good job!",
              "great!",
              "a good rest is good for the soul!",
              "recorded data is insufficient :("
              ]
    possible_assign=["resting", "moderate activity", "high activity", "recovery", "poor_quality"]
    if assign1 in possible_assign:
        if assign1==possible_assign[0]:
            return messages[0]
        elif assign1==possible_assign[1]:
            return messages[1]
        elif assign1==possible_assign[2]:
            return messages[2]
        elif assign1==possible_assign[3]:
            return messages[3]
        elif assign1==possible_assign[4]:
            return messages[4]
    else:
        return "hello, your activety class has eluded me"





#classes

class Participant:
    """
    this class acsesses and stores Personal information from the user
    """
    def __init__(self,profile_data=None):
            
        self.personal_data=profile_data

        self._participant_id = None
        self._baseline_hr = None
        self._baseline_skin = None
        self._baseline_temp = None

        if isinstance(self.personal_data,dict):
            self._participant_id = self.personal_data.get("participant_id")
            self._baseline_hr = self.personal_data.get("baseline_heart_rate")
            self._baseline_skin = self.personal_data.get("baseline_skin_response")
            self._baseline_temp = self.personal_data.get("baseline_temperature")
    @classmethod
    def instanciate_profile(cls, profile_dict):
        return cls(profile_dict)
    

    @property
    def ID(self):
        return self._participant_id


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

    def __init__(self, raw_data = None):
        self.raw_data=raw_data

        self.inValid=list()
        self.Valid=list()


        self.heart_rate = list()
        self.skin_response = list()
        self.temperature = list()
        self.activity_level = list()
        self.signal_quality=list()

    def isValid(self, Signal_threshold=0.8):
        """ check if the raw data is valid, within realistic limits and meets quality standards"""

        try:
            if isinstance(self.raw_data,list):
                for x in self.raw_data:
                    if isinstance(x,dict):
                        if x.get("signal_quality") < Signal_threshold:
                            self.inValid.append(x)
                        elif None in x.values():
                            self.inValid.append(x)
                        else:
                            self.Valid.append(x)
                    else:
                        return " the content of your raw_data list is not dictionaries (line 145)", " the content of your raw_data list is not dictionaries (line 145)"
            else:
                return "the raw data you provided is not formated correctly (line 145)", "the raw data you provided is not formated correctly (line 145)"
            return self.inValid, self.Valid
        
        except Exception as e:
            return "something went wrong in Observation, isValid (line 155)", str(e)


    @property
    def ValidValues(self):
        return self.Valid

    @property
    def InValidCount(self):
        return len(self.inValid)


    def ValidDataContainerAllocation(self):
        try:
            if self.Valid:
                self.heart_rate = [x.get("heart_rate") for x in self.Valid if 0 < x["heart_rate"] <220]
                self.skin_response = [x.get("skin_response") for x in self.Valid if 0 < x["skin_response"] <3.5]
                self.temperature = [x.get("temperature") for x in self.Valid if 30 < x["temperature"] <38]
                self.activity_level = [x.get("activity_level") for x in self.Valid if 0 <= x["activity_level"] <= 1]
                self.signal_quality = [x.get("signal_quality") for x in self.Valid if 0 <= x["signal_quality"] <= 1]
                return self.heart_rate, self.skin_response, self.temperature, self.activity_level, self.signal_quality
            else:
                return "the data container is empty","the data container is empty", "the data container is empty","the data container is empty","the data container is empty"
        except Exception as e:
            return "something went wrong on Observation, ValidDataContainerAllocation (line 177)", str(e)
  
    def ValidateType(self):
            try:

                _check_heart = all(type(x) in (int,float) for x in self.heart_rate)
                _check_skin = all(type(x) in (int,float) for x in self.skin_response)
                _check_temp = all(type(x) in (int,float) for x in self.temperature)
                _check_activity = all(type(x) in (int,float) for x in self.activity_level)
                _check_signal = all(type(x) in (int,float) for x in self.signal_quality)
                if all([_check_heart, _check_skin, _check_temp, _check_activity, _check_signal]) and all([self.heart_rate, self.skin_response, self.temperature, self.activity_level, self.signal_quality]):
                    return True #, [_check_heart,_check_skin,_check_temp,_check_activity,_check_signal],[self.heart_rate, self.skin_response, self.temperature, self.activity_level, self.signal_quality]
                else:
                    return False #, [_check_heart,_check_skin,_check_temp,_check_activity,_check_signal], [self.heart_rate, self.skin_response, self.temperature, self.activity_level, self.signal_quality]
            except Exception as e:
                return "something went wrong on Observation, ValidateType (line 201)", str(e)



class SessionsStorage:
    def __init__(self, *raw_datasets: list):
        self.collection_raw_dataset=raw_datasets
        self.raw=list()
        self.all_valid_record=list()
        self.all_invalid_record=list()

    def ValidateAll(self):
        for entry in self.collection_raw_dataset:
            obs_instance=Observation(entry)
            invalid, valid = obs_instance.isValid()
            

            obs_instance.ValidDataContainerAllocation()
            self.raw.append(obs_instance)
            
            if valid:
                self.all_valid_record.append(valid)
            if invalid:
                self.all_invalid_record.append(invalid)
        return self.all_invalid_record, self. all_valid_record



class sessionMath(SessionsStorage):
    def __init__(self, profile_data=None, *raw_datasets):
        super().__init__(*raw_datasets)
        self.participant = Participant.instanciate_profile(profile_data)
#        self.participant.SetProfileData()
        self.summary_data = dict()
        
        # self.inv,self.v=self.ValidateAll()
        self.invalid_records= None
        self.valid_records = None
        self.total_unusable_observations=None
        self.total_usable_observations=None

        # self.all_hr=list()

    @staticmethod
    def format_text(string, value, width=55):
        if isinstance(value, (float)):
            value=round(value, 2)
        return f"{string.ljust(width, ".")} {value}"




    def recoveryTracker(self):
        "this function checks for a restitution period based on the last 3 session timestamps"
        " and compare it to avg, max and mid-time values"
        # data=self.all_valid_record
        # sorted_data=sort_dict_list(self.all_valid_record, "heart_rate")

        checking_hr = Downward_trend(self.all_valid_record, "heart_rate")
        checking_sr= Downward_trend(self.all_valid_record, "skin_response")
        checking_temp= Downward_trend(self.all_valid_record, "temperature")
        checking_al= Downward_trend(self.all_valid_record, "activity_level")

        isRecovery=matching_lists(checking_hr,checking_sr, checking_temp, checking_al)
        recovery_msg=[]
        recovery_check=False
        count=1
        for count,x in enumerate(isRecovery,start=1):
            if x is True:
                recovery_msg.append((f"data from session {count} is  a recovery session",count))
                recovery_check=True
            elif x is False:
                continue
            else:
                recovery_msg.append("something went wrong")
        return  recovery_check, recovery_msg #checking_hr,checking_sr, checking_temp, checking_al ,isRecovery #, recovery_msg

    def ValidateAll(self):
        # Call parent's ValidateAll method first
        self.invalid_records, self.valid_records = super().ValidateAll()

        # 2. Add child-specific tracking logic (usable vs unusable count summary)
        self.total_usable_observations = sum(len(session) for session in self.valid_records)
        self.total_unusable_observations = sum(len(session) for session in self.invalid_records)
        
        return self.invalid_records, self.valid_records 

    
    def hr_info(self, recovery_msg=None):
        try:
            data_capsule=list(self.raw)

            #step 1 in filtering out recovery data as it polutes maximum, and average readings
            recovery_idx=list()
            if recovery_msg is not None:
                for msg in recovery_msg:
                    if isinstance(msg,tuple):
                        recovery_idx.append(msg[1]-1)


                filtered_data=list()
                for idx, data in enumerate(data_capsule):
                    if idx not in recovery_idx:
                        filtered_data.append(data)
                data_capsule=filtered_data
            all_hr=list()
             ###############################3   
            if not all_hr and self.raw:
                for values in self.raw:
                    if values.heart_rate and isinstance(values.heart_rate, list):
                         all_hr.extend(values.heart_rate)
            ##############################################3

            for values in data_capsule:
                if values.heart_rate and isinstance(values.heart_rate,list):
                    all_hr.extend(values.heart_rate)
            if all_hr:
                self.summary_data["heart_rate"] = {
                    "reference": self.participant.Baseline_HR,
                    "max": max(all_hr),
                    "avg": round(sum(all_hr) / len(all_hr),1),
                    "min": min(all_hr)
                }

            elif not all_hr:
                self.summary_data["heart_rate"] = {
                    "reference": self.participant.Baseline_HR,
                    "max": 0,
                    "avg": 0,
                    "min": 0
                }
            else:
                return "something went wrong(line183)"
            return self.summary_data["heart_rate"]
        except Exception as e:
            return f"something went wrong in sessionMath, hr_info (line 292)", str(e)


    def sr_info(self,recovery_msg=None):
        try:
            data_capsule=list(self.raw)
            #step 1 in filtering out recovery data as it polutes maximum, and average readings
            recovery_idx=list()
            if recovery_msg is not None:
                for msg in recovery_msg:
                    if isinstance(msg,tuple):
                        recovery_idx.append(msg[1]-1)


                filtered_data=list()
                for idx, data in enumerate(data_capsule):
                    if idx not in recovery_idx:
                        filtered_data.append(data)
                data_capsule=filtered_data  
            all_sr=list()

             ###############################3   
            if not all_sr and self.raw:
                for values in self.raw:
                    if values.skin_response and isinstance(values.skin_response, list):
                         all_sr.extend(values.skin_response)
            ##############################################3

            for values in data_capsule:
                if values.skin_response and isinstance(values.skin_response,list):
                    all_sr.extend(values.skin_response)
            if all_sr:
                self.summary_data["skin_response"] = {
                    "reference": self.participant.Baseline_Skin,
                    "max": max(all_sr),
                    "avg": round(sum(all_sr) / len(all_sr),2),
                    "min": min(all_sr)
                }

            elif not all_sr:
                self.summary_data["skin_response"] = {
                    "reference": self.participant.Baseline_Skin,
                    "max": 0,
                    "avg": 0,
                    "min": 0
                }
            else:
                return "something went wrong(line183)"
            return self.summary_data["skin_response"]
        except Exception as e:
            return f"something went wrong in sessionMath, sr_info (line 342)", str(e)


    def temp_info(self,recovery_msg=None):
        try:
            data_capsule=list(self.raw)

            #step 1 in filtering out recovery data as it polutes maximum, and average readings
            recovery_idx=list()
            if recovery_msg is not None:
                for msg in recovery_msg:
                    if isinstance(msg,tuple):
                        recovery_idx.append(msg[1]-1)


                filtered_data=list()
                for idx, data in enumerate(data_capsule):
                    if idx not in recovery_idx:
                        filtered_data.append(data)
                data_capsule=filtered_data
            all_temp=list()

             ###############################3   
            if not all_temp and self.raw:
                for values in self.raw:
                    if values.temperature and isinstance(values.temperature, list):
                         all_temp.extend(values.temperature)
            ##############################################3

            
            for values in data_capsule:
                if values.temperature and isinstance(values.temperature,list):
                    all_temp.extend(values.temperature)
            if all_temp:
                self.summary_data["temperature"] = {
                    "reference": self.participant.Baseline_Temp,
                    "max": max(all_temp),
                    "avg": round(sum(all_temp) / len(all_temp),1),
                    "min": min(all_temp)
                }

            elif not all_temp:
                self.summary_data["temperature"] = {
                    "reference": self.participant.Baseline_Temp,
                    "max": 0,
                    "avg": 0,
                    "min": 0
                }
            else:
                return "something went wrong(line183)"
            return self.summary_data["temperature"]
        except Exception as e:
            return f"something went wrong in sessionMath, temp_info (line 392)", str(e)


    def al_info(self, recovery_msg=None):
        try:
            data_capsule=list(self.raw)

            #step 1 in filtering out recovery data as it polutes maximum, and average readings
            recovery_idx=list()
            if recovery_msg is not None:
                for msg in recovery_msg:
                    if isinstance(msg,tuple):
                        recovery_idx.append(msg[1]-1)


                filtered_data=list()
                for idx, data in enumerate(data_capsule):
                    if idx not in recovery_idx:
                        filtered_data.append(data)
                data_capsule=filtered_data
            
            all_al=list()

             ###############################3   
            if not all_al and self.raw:
                for values in self.raw:
                    if values.activity_level and isinstance(values.activity_level, list):
                         all_al.extend(values.activity_level)
            ##############################################3

            for values in data_capsule:
                if values.activity_level and isinstance(values.activity_level,list):
                    all_al.extend(values.activity_level)
            if all_al:
                self.summary_data["activity_level"] = {
                    "reference": "NA",
                    "max": max(all_al),
                    "avg": round(sum(all_al) / len(all_al),2),
                    "min": min(all_al)
                }
            else:
                self.summary_data["activity_level"] = {
                "reference": "NA",
                "max": 0,
                "avg": 0,
                "min": 0
                }
            return self.summary_data["activity_level"]
        

        except Exception as e:
            return f"something went wrong in sessionMath, al_info (line 444)", str(e)
  

    def signal_info(self, recovery_msg=None):
        try:

            data_capsule=list(self.raw)

            #step 1 in filtering out recovery data as it polutes maximum, and average readings
            recovery_idx=list()
            if recovery_msg is not None:
                for msg in recovery_msg:
                    if isinstance(msg,tuple):
                        recovery_idx.append(msg[1]-1)


                filtered_data=list()
                for idx, data in enumerate(data_capsule):
                    if idx not in recovery_idx:
                        filtered_data.append(data)
                data_capsule=filtered_data

            all_sig=list()
            for values in data_capsule:
                if values.signal_quality and isinstance(values.signal_quality,list):
                    all_sig.extend(values.signal_quality)
            if all_sig:
                self.summary_data["signal_quality"] = {
                    "reference": "NA",
                    "max": max(all_sig),
                    "avg": round(sum(all_sig) / len(all_sig),2),
                    "min": min(all_sig)
                }
            else:
                self.summary_data["signal_quality"] = {
                "reference": "NA",
                "max": 0,
                "avg": 0,
                "min": 0
                }
            return self.summary_data["signal_quality"]
        

        except Exception as e:
            return f"something went wrong in sessionMath, temp_info (line 495)", str(e)

    @property
    def all_info_dict(self):
        return self.summary_data


    def SessionClassification(self):
        type_data=dict()
        rec_trac, rec_trac_msg= self.recoveryTracker()
        self.hr_info(rec_trac_msg)
        self.sr_info(rec_trac_msg)
        self.temp_info(rec_trac_msg)
        self.al_info(rec_trac_msg)
        

        for x in self.summary_data:
            if x == "heart_rate":
                hr_avg = self.summary_data[x].get("avg")
                if hr_avg == 0:
                    type_data["heart_rate"] = "---"
                elif 0 < hr_avg < self.participant._baseline_hr +10:
                    type_data["heart_rate"] = "resting"
                elif hr_avg < self.participant._baseline_hr+30:
                    type_data["heart_rate"] = "moderate activity"
                elif  hr_avg < 220: # general formulas set 220 as maximum heartrate value before heart damage
                    type_data["heart_rate"] = "high activity"

                else:
                    type_data["heart_rate"] = "inconclusive or unknown session type"

            elif x == "skin_response":
                sr_avg = self.summary_data[x].get("avg")
                if sr_avg == 0:
                    type_data["skin_response"] = "---"
                elif 0 < sr_avg < self.participant._baseline_skin + 0.30:
                    type_data["skin_response"] = "resting"
                elif sr_avg < self.participant._baseline_skin + 0.55:
                    type_data["skin_response"] = "moderate activity"
                elif self.participant._baseline_skin + 0.55 < sr_avg <5: # 5 is an arbitrary estimated value
                    type_data["skin_response"] = "high activity"
                else:
                    type_data["skin_response"] = "inconclusive or unknown session type"

            elif x == "temperature":
                temp_avg = self.summary_data[x].get("avg")
                if temp_avg == 0:
                    type_data["temperature"] = "---"
                elif 0 < temp_avg < self.participant._baseline_temp + 0.1:
                    type_data["temperature"] = "resting"
                elif temp_avg < self.participant._baseline_temp + 0.30:
                    type_data["temperature"] = "moderate activity"
                elif temp_avg < 42: # 42 is the temeperature human protein denaturates and is therefore set as max value
                    type_data["temperature"] = "high activity"
                else:
                    type_data["temperature"] = "inconclusive or unknown session type"

            elif x == "activity_level": #bsolute values, no scaling changes needed
                al_avg = self.summary_data[x].get("avg")
                if al_avg == 0:
                    type_data["activity_level"] = "---"
                elif 0 < al_avg <= 0.25:
                    type_data["activity_level"] = "resting"
                elif al_avg <= 0.67:
                    type_data["activity_level"] = "moderate activity"
                elif al_avg <= 1:
                    type_data["activity_level"] = "high activity"
                else:
                    type_data["activity_level"] = "inconclusive or unknown session type"

        return type_data

    def majority_session(self,type_data, is_recovery=False):
        values=list(type_data.values())
        #since the data_generator is based on rng and gauss distribution some values may become autliers and reult in,
        # some parameters not linight perfectly up with the others, by checking for majority/ minimum of 3 equals, 
        #  to mittigate this issue
        if self.summary_data["heart_rate"].get("max")==0:
            return "session type inconclusive due to missing / bad data"

        if is_recovery and majority(values, "moderate activity"):
            return "recovery"
        elif majority(values,"resting"):
            return "resting"
        elif majority(values, "moderate activity"):
            return "moderate activity"
        elif majority(values, "high activity"):
            return "high activity"
        # elif is_recovery or majority(values, "---"):
        #     return "recovery"
        else:
            return f"inconclusive or unknown session type"

    def SessionLogPrint(self,hr_data=None, sr_data=None, temp_data=None, al_data=None, activety_type=None, recover_status=None):
        "this function presents the calculated datas, and returns an ecouraging message"

        data_list=[hr_data,sr_data,temp_data, al_data]
        if recover_status:
            recovery_check="yes"
        elif recover_status == None:
            recovery_check= None
        elif not recover_status:
            recovery_check = "No"
        else:
            recovery_check="something went wrong (line 484)"
  
        sup_msg=suportive_messages(activety_type)

        summary_lines=[
            "_"*75,
            f"you just finished a session of {activety_type}",
            f"{sup_msg}",
            "_"*65,
            "your maximum values across the sessions were:",
            f"{self.format_text("your heart rate reached", hr_data.get('max'))} BPM",

            f"{self.format_text("your skin respone reached", sr_data.get('max'))}",

            f"{self.format_text("your temperature rate reached", temp_data.get('max'))} C",

            f"{self.format_text("your activety level reached", al_data.get('max'))}",
            "_"*65,
            "your average values across the sessions were:",
            f"{self.format_text("your heart rate averaged", hr_data.get('avg'))} BPM",

            f"{self.format_text("your skin respone averaged", sr_data.get('avg'))}",

            f"{self.format_text("your temperature averaged", temp_data.get('avg'))} C",

            f"{self.format_text("your acticity level averaged", al_data.get('avg'))}",
            "_"*65,
            "your minimum values across the sessions were:",
            f"{self.format_text("your heart rate hit", hr_data.get('min'))} BPM",

            f"{self.format_text("your skin respone hit", sr_data.get('min'))}",

            f"{self.format_text("your temperature hit", temp_data.get('min'))} C",

            f"{self.format_text("your activity level hit", al_data.get('min'))}",
            "_"*65,
            "your ranges were as follows",
            f"{self.format_text("your heart rate spanned", (hr_data.get('max')-hr_data.get('min')))} BPM",

            f"{self.format_text("your skin respone spanned", (sr_data.get("max")-sr_data.get('min')))}",

            f"{self.format_text("your temperature spanned", (temp_data.get("avg")-temp_data.get('min')))} C",

            f"{self.format_text("your acticety level spanned", (al_data.get("max")-al_data.get('min')))}",
            "_"*65,
            f"{self.format_text("recovery period?", recovery_check)}",
            f"{self.format_text("invalid data count?", self.total_unusable_observations)}",
            f"{self.format_text("valid data count?", self.total_usable_observations)}",
            "_"*75


        ]
        poor_data=["the data for this session was corrupted or not adequate for data processing",
                   "please adjust tracker"]



        try:
            if hr_data is None or sr_data is None or temp_data is None or al_data is None:
                return "missing data (line 446)"
            elif all(isinstance(data, dict) for data in data_list):
                if hr_data.get("max")==0:
                    return poor_data
                else:
                    return summary_lines
            else:
                return ["something went wrong(line 451)",""]

        except Exception as e:
            return ["something went wrong(line 451)",""], str(e)


    def data_dict(self,hr_data=None, sr_data=None, temp_data=None, al_data=None, activety_type=None, recover_status=None):
        return {"HEARTRATE":hr_data, 
                "SKINRESPONSE": sr_data, 
                "TEMPERATURE": temp_data, 
                "ACTIVITY": al_data, 
                "RECOVERY": recover_status,
                "ACTIVETY TYPE": activety_type,
                "DATASET w/INVALID DATA": len(self.invalid_records),
                "DATASET w/VALID DATA" : len(self.valid_records), 
                "INVALIDCOUNT": self.total_unusable_observations, 
                "VALIDCOUNT": self.total_usable_observations}