from pathlib import Path

from fitness_analyzer.analysis import summary, classify_hr, classify_sr, classify_temp, classify_al, recoveryDetection, SessionClass, analyseSession

from fitness_analyzer.io_csv import load_all_sessions, load_profiles, load_sessions

from fitness_analyzer.models import Participant, fitnessSession, Observation

from fitness_analyzer.validation import InvalidRecordError, isValidRow, validate_participant_id, validate_session_id, isRowLen

from fitness_analyzer.exceptions import InvalidRecordError, InvalidIdentifierError





DATA_DIR=Path("data")
TEMP_TEST_DIR=Path("tests/fixtures")

PROFILE_PATH= DATA_DIR/"participants.csv"

SESSION_PATHS = [
    DATA_DIR/ "fitness_sessions.csv" ,
    DATA_DIR/"fitness_sessions_invalid.csv"

    ]


KNOWN_IDS = {"P001", "P002", "P003"}

KNOWN_SESSIONS = {"FIT-2026-001", "FIT-2026-002", "FIT-2026-003"}

def make_row(**changes):
    row = {
        "session_id": "FIT-2026-001",
        "participant_id": "P001",
        "timestamp": "0",
        "heart_rate": "70",
        "skin_response": "1.20",
        "temperature": "32.5",
        "activity_level": "0.10",
        "signal_quality": "0.96",
    }
    row.update(changes)
    return row
  


def expect_error(exc_type, func, *args):
    try:
        func(*args)
    except exc_type as e:
        return e
    raise AssertionError(f"expected {exc_type.__name__} but no exception was raised")



def test_valid_participant_id():
    assert validate_participant_id("P001") in KNOWN_IDS
    print("test_valid_participant_id passed")



def test_invalid_participant_ids():
    invalid_ids = ["P01", "P0001", "p001", "001", "P00A"]
    for id_check in invalid_ids:
        expect_error(InvalidIdentifierError, validate_participant_id, id_check)
    print("test_invalid_participant_ids passed")


def test_valid_session_id():
    assert validate_session_id("FIT-2026-001") in KNOWN_SESSIONS
    print("test_valid_session_id passed")

def test_invalid_session_ids():
    invalid_ids = ["FIT-2026-00", "FIT-2026-7000", "fit-2026-001"]
    for id_check in invalid_ids:
        expect_error(InvalidIdentifierError, validate_session_id, id_check)
    print("test_invalid_session_ids passed")



##___________________________row level validation tests_____________________
def test_valid_row_is_converted():
        row = isValidRow(make_row(), KNOWN_IDS)
        assert isinstance(row['timestamp'], int), "timestamp is not an int"
        assert isinstance(row['heart_rate'], int), "heart_rate is not an int"

        for field in ("skin_response", "temperature", "activity_level", "signal_quality"):
            assert isinstance(row[field], float), f"{field} is not a float"
        print("test_valid_row_is_converted passed")


def test_unknown_participant():
    e=expect_error(InvalidRecordError, isValidRow, make_row(participant_id="P999"), KNOWN_IDS) 
    assert e.field=="participant_id"
    print("test_unknown_participant passed")

def test_bad_ids_in_row():
    expect_error(InvalidIdentifierError, isValidRow, make_row(participant_id="P01"), KNOWN_IDS)
    expect_error(InvalidIdentifierError, isValidRow, make_row(session_id="FIT-2026-00"), KNOWN_IDS)   
    print("test_bad_ids_in_row passed")

def test_missing_required_field():
    for field in ("session_id", "participant_id", "timestamp", "heart_rate",
                  "skin_response", "temperature", "activity_level",
                  "signal_quality"):
        row = make_row(**{field: ""})
        e=expect_error(InvalidRecordError, isValidRow, row, KNOWN_IDS)
        assert e.field==field

    row2 = make_row()
    row2["activity_level"] = None
    e2=expect_error(InvalidRecordError, isValidRow, row2, KNOWN_IDS)
    assert e2.field=="activity_level"
    print("test_missing_required_field passed")   

def test_wrong_type():
    e=expect_error(InvalidRecordError, isValidRow, make_row(heart_rate="fast"), KNOWN_IDS)
    assert e.field=="heart_rate"
    e=expect_error(InvalidRecordError, isValidRow, make_row(skin_response="one.point.two"), KNOWN_IDS)
    assert e.field=="skin_response" 
    e=expect_error(InvalidRecordError, isValidRow, make_row(temperature="thirty.two"), KNOWN_IDS)
    assert e.field=="temperature"
    e=expect_error(InvalidRecordError, isValidRow, make_row(activity_level="zero.point.one"), KNOWN_IDS)
    assert e.field=="activity_level"
    e=expect_error(InvalidRecordError, isValidRow, make_row(signal_quality="high"), KNOWN_IDS)
    assert e.field=="signal_quality"
    e=expect_error(InvalidRecordError, isValidRow, make_row(heart_rate="70.3"), KNOWN_IDS)
    print("test_wrong_type passed")

def test_out_of_range_values():
    bad_values = {
        "heart_rate": [-1, 300],    
        "skin_response": [-1],
        "temperature": [10.0, 60.0],
        "activity_level": [-0.1, 1.1],
        "signal_quality": [-0.1, 1.1]
    }
    for field, values in bad_values.items():
        for value in values:
    
            e=expect_error(InvalidRecordError, isValidRow, make_row(**{field: value}), KNOWN_IDS)
            assert e.field==field
    print("test_out_of_range_values passed")    


def test_range_boundaries_are_accepted():
    good_values = {
        "heart_rate": [40, 205], 
        "skin_response": [0.0, 90.9],
        "temperature": [25, 42],
        "activity_level": [0.0, 1.0],
        "signal_quality": [0.5, 1.0]
    }
    for field, values in good_values.items():
        for value in values:
            isValidRow(make_row(**{field: value}), KNOWN_IDS)
    print("test_range_boundaries_are_accepted passed")

def test_poor_signal_quality():
    e=expect_error(InvalidRecordError, isValidRow, make_row(signal_quality=0.4), KNOWN_IDS)
    assert e.field=="signal_quality"    
    e=expect_error(InvalidRecordError, isValidRow, make_row(signal_quality=0.49), KNOWN_IDS)
    assert e.field=="signal_quality"
    e=expect_error(InvalidRecordError, isValidRow, make_row(signal_quality=1.2), KNOWN_IDS)
    assert e.field=="signal_quality"    
    print("test_poor_signal_quality passed")


def test_wrong_column_count():
    row= make_row()
    row["extra_column"]="extra"
    e=expect_error(InvalidRecordError, isRowLen, row)
    e=expect_error(InvalidRecordError, isValidRow, row, KNOWN_IDS)


    short_row=make_row()
    del short_row["activity_level"]
    e=expect_error(InvalidRecordError, isRowLen, short_row)
    e=expect_error(InvalidRecordError, isValidRow, short_row, KNOWN_IDS)

    print("test_wrong_column_count passed")





#__________________________session RUN_ALL tests_____________________  

def run_all_tests():

    test_valid_participant_id()
    test_invalid_participant_ids()
    test_valid_session_id()
    test_invalid_session_ids()
    test_valid_row_is_converted()
    test_unknown_participant()
    test_bad_ids_in_row()
    test_missing_required_field()
    test_wrong_type()
    test_out_of_range_values()
    test_range_boundaries_are_accepted()
    test_poor_signal_quality()
    test_wrong_column_count()

    print("all tests passed")


if __name__=="__main__":
    run_all_tests()