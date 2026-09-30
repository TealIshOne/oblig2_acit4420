"""
this unit will include OOP class structures that analyse
provided data and return datasets of relevant 

## from assignemnt 1:
 include into summary(): hr_info, sr_info, temp_info, etc.

 include into detect_recovery(): downwardTrend

 include into classify_data: SessionClassification 
"""


## -------------------thresholds ------------------##
HR_MOD_OFFSET = 10
HR_HIGH_OFFSET = 30

SKIN_MOD_OFFSET = 0.30
SKIN_HIGH_OFFSET = 0.55

TEMP_MOD_OFFSET = 0.35
TEMP_HIGH_OFFSET = 0.30

ACTIVITY_MOD_MAX = 0.35
ACTIVITY_HIGH_MAX = 0.67

MIN_USABLE_OBS = 3

REC_HR_VAL = 0.60
REC_ACT_VAL = 0.50
## --------------------------------------------------##

def majority(val, target):
    return val.count(target) >= len(val)/2
  

def summary(target_values):
    if not target_values:
        return None
    return {
        "min": min(target_values),
        "max" : max(target_values),
        "avg" : round(sum(target_values)/len(target_values),2)
    }


def classify_hr(avg_hr, baseline_hr):
    if avg_hr <= baseline_hr + HR_MOD_OFFSET:
        return "resting"
    elif avg_hr <= baseline_hr + HR_HIGH_OFFSET:
        return "moderate activity"
    else:
        return "high activity"


def classify_sr(avg_sr, baseline_sr):
    if avg_sr <= baseline_sr + SKIN_MOD_OFFSET:
        return "resting"
    elif avg_sr <= baseline_sr + SKIN_HIGH_OFFSET:
        return "moderate activity"
    else:
        return "high activity"


def classify_temp(avg_temp, baseline_temp):
    if avg_temp <= baseline_temp + TEMP_MOD_OFFSET:
        return "resting"
    elif avg_temp <= baseline_temp + TEMP_HIGH_OFFSET:
        return "moderate activity"
    else:
        return "high activity"


def classify_al(avg_al):
    if avg_al <=  ACTIVITY_MOD_MAX:
        return "resting"
    elif avg_al <= ACTIVITY_HIGH_MAX:
        return "moderate activity"
    else:
        return "high activity"





    

def _reduction_fraction(values):
    peak= max(values)
    end=values[-1]

    if peak==0:
        return 0.0
    return max(0.0,(peak-end)/peak)



def recoveryDetection(session):
    hr_values=session.values("heart_rate")
    activity_values=session.values("activity_level")

    if len(hr_values) < 2 or len(activity_values)<2:
        return False, "not enough observations to asses recovery"
    hr_fraction= _reduction_fraction(hr_values)
    activity_fraction= _reduction_fraction(activity_values)
    isRecovery=(hr_fraction>=REC_HR_VAL and activity_fraction >=REC_ACT_VAL)

    reason= ( 
        f"heartrate recovered {hr_fraction:.0%} from peak"
        f"activitylevels fell {activity_fraction:.0%} from peak"
    )

    return isRecovery, reason


def SessionClass(session, hr_summary, skin_summary, temp_summary, activity_summary):
    if session.usable_count < MIN_USABLE_OBS:
        return (
            "innsufficient data"
            f"only {session.usable_count} usable obervation(s)"
            f"minimum amount of observations is {MIN_USABLE_OBS}"
        )

    is_recovery, recovery_Reason=recoveryDetection(session)
    if is_recovery:
        return "revovering", recovery_Reason


    participant=session.participant
    classification=[
        classify_hr(hr_summary["avg"], participant.Baseline_HR),
        classify_sr(skin_summary["avg"], participant.Baseline_Skin),
        classify_temp(temp_summary["avg"], participant.Baseline_Temp),
        classify_al(skin_summary["avg"]),
    ]

    for label in  ("resting", "moderate activity", "high activity"):
        if majority(classification, label):
            return label, f"majority metrics classified as {label}: {classification}"'

    return "inconclusive", f"no majority among metric classification: {classification}"



def analyseSession(session):
    hr_summary = summary(session.values("heart_rate"))
    skin_summary=summary(session.values("skin_response"))
    temp_summary = summary(session.values("temperature"))
    al_summary=summary(session.values("activity_level"))
    sig_summary= summary(session.values("signal_quality"))

    if session.usable_count < MIN_USABLE_OBS:
        label, reason = SessionClass(session, {},{},{},{})
    else:
        label, reason =SessionClass(
            session, hr_summary,skin_summary,temp_summary, al_summary
        )

    participant= session.participant

    return {
        "session_id" : session.session_id,
        "participant_id" : participant.ID,
        "usable_obs" : session.usable_count,
        "classification" : label,
        "hr_min" : hr_summary["min"] if hr_summary else None,
        "hr_max" : hr_summary["max"] if hr_summary else None,
        "hr_avg" : hr_summary["avg"] if hr_summary else None,
        "skin_min" : skin_summary["min"] if skin_summary else None,
        "skin_max" : skin_summary["max"] if skin_summary else None,
        "skin_avg" : skin_summary["avg"] if skin_summary else None,
        "temp_min" : temp_summary["min"] if temp_summary else None,
        "temp_max" : temp_summary["max"] if temp_summary else None,
        "temp_avg" : temp_summary["avg"] if temp_summary else None,
        "activity_min" : al_summary["min"] if al_summary else None,
        "activity_max" : al_summary["max"] if al_summary else None,
        "activity_avg" : al_summary["avg"] if al_summary else None,
        "signal_avg" : sig_summary["avg"] if sig_summary else None
    }