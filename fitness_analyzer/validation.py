"""
- validation of data
- add complied regexes
- reuse from A1
>> checking signal quality
>> range checks

- make sure range constraints are from DATA_DESCRIPTION.md
- 

"""

## --------imported classes/libraries ------------##
import re

from fitness_analyzer.exceptions import InvalidIdentifierError, InvalidRecordError

## ----------decoder parameters ----------##
PARTICIPANT_ID_CODE=re.compile(r"^P\d{3}$")
SESSION_ID_CODE= re.compile(r"^FIT-\d{4}-\d{3}$")

## ------------values, ranges, descriptors ------------##
VALID_RANGES={
    "heart_rate" : (35,205),
    "skin_response" : (0,None),
    "temperature" : (25,42),
    "activity_level" : (0,1),
    "signal_quality" : (0,1)
}

MIN_SIGNALQ=0.5

REQUIRED_FIELDS =(
    "session_id", "participant_id", "timestamp", "heart_rate",
    "skin_response", "temperature", "activity_level",
    "signal_quality"
)

## identifier validation functions ##

def validate_participant_id(participant_id):
    if not PARTICIPANT_ID_CODE.fullmatch(participant_id):
        raise InvalidIdentifierError(
            participant_id, "participant_id",PARTICIPANT_ID_CODE.pattern
        )
    return(participant_id)

def validate_session_id(session_id):
    if not SESSION_ID_CODE.fullmatch(session_id):
        raise InvalidIdentifierError(
            session_id, "session_id", SESSION_ID_CODE.pattern
        )
    return session_id

## row level validation ##
def isRequiredField(row):
    for field in REQUIRED_FIELDS:
        value=row.get(field)
        if value is None or value == "":
            raise InvalidRecordError (
                reason="missing required field", field= field
            )

def convertType(row):
    convertion_unit=dict(row)
    int_field= ("timestamp", "heart_rate")
    float_field =("skin_response", "temperature","activity_level", "signal_quality")

    for field in int_field:
        try:
            convertion_unit[field]=int(row[field])
        except (TypeError, ValueError) as e:
            raise InvalidRecordError(
                reason=f"could not convert {row[field]} to int",
                field=field
            ) from e

    for field in float_field:
        try:
            convertion_unit[field]=float(row[field])
        except (TypeError, ValueError) as e:
            raise InvalidRecordError (
                reason=f"could not convert {row[field]} to int",
                field=field
            ) from e

    return convertion_unit


def isSignalQ(row):
    if row["signal_quality"] < MIN_SIGNALQ:
        raise InvalidRecordError(
            reason= f"Poor signal quality, {row['signal_quality']} bellow {MIN_SIGNALQ}",
            field="signal_quality"
        )
    

def isInRange(row):
    for field, (low,high) in VALID_RANGES.items():
        value=row[field]
        if low is not None and value<low:
            raise InvalidRecordError(
                reason= f"{value} is out of range (bellow minimum boundary {low})",
                field=field
            )
        if high is not None and value> high:
            raise InvalidRecordError(
                reason=f"{value} is out of range (above macimum boundary {high})",
                field=field
            )


def isRowLen(row):
    if None in row or len(row)!=len(REQUIRED_FIELDS):
        raise InvalidRecordError(
            reason=f"expected {len(REQUIRED_FIELDS)} fields, gor {len(row)}",
            field=None
        )  


def isValidRow(row, known_ids):
    isRowLen(row)
    isRequiredField(row)
    validate_participant_id(row["participant_id"])
    validate_session_id(row["session_id"])

    if row["participant_id"] not in known_ids:
        raise InvalidRecordError(
            reason= f"unknown participant id, '{row["participant_id"]}'",
            field="participant_id"
        )

    row= convertType(row)
    isInRange(row)
    isSignalQ(row)

    return row

