import csv
from pathlib import Path
from unittest import result
import tempfile

from fitness_analyzer.io_csv import load_profiles, load_sessions, load_all_sessions
from fitness_analyzer.reports import build_report_text

DATA_DIR = Path("data")
PROFILE_PATH = DATA_DIR / "participants.csv"
SESSIONS_PATH = DATA_DIR / "fitness_sessions.csv"
INVALID_PATH = DATA_DIR / "fitness_sessions_invalid.csv"

OUTPUT_DIR = Path("tests/fixtures")
TEST_SESSIONS_PATH = OUTPUT_DIR / "test_fit_ses.csv"
TEST_SESSIONS_INVALID_PATH = OUTPUT_DIR / "test_fit_ses_inv.csv"
TEST_PARTICIPANTS_PATH = OUTPUT_DIR / "test_participants.csv"

PROFILE_HEADER = [
    "participant_id", "name", "baseline_heart_rate",
                  "baseline_skin_response", "baseline_temperature"  
]

SESSION_HEADER = [
    "session_id", "participant_id", "timestamp", "heart_rate",
    "skin_response", "temperature", "activity_level", "signal_quality"
]

##______

def csv_wite(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

def expect_error(exc_type, func, *args):
    try:
        func(*args)
    except exc_type as e:
        return e
    raise AssertionError(f"expected {exc_type.__name__} but no exception was raised")

def load_real_participants():
    participant,_=load_profiles(PROFILE_PATH)
    return participant


##__________________________tests_________________________
def test_load_profiles():
    participants, rejections = load_profiles(PROFILE_PATH)
    assert set(participants.keys()) == {"P001", "P002", "P003"}, "got {set(participants.keys())}"
    assert len(rejections) == 0, f"got {len(rejections)} rejections"
    p=participants["P001"]
    assert p.Baseline_HR  == 68 and p.Baseline_Skin  == 1.2 and p.Baseline_Temp  == 32.4

    print("test_load_profiles passed")


def test_load_profiles_with_invalid():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "profiles.csv"
        csv_wite(path, PROFILE_HEADER, [
            ["P001", "Good One", "68", "1.2", "32.4"],
            ["001", "Bad Id", "70", "1.1", "32.0"],       # row 3: bad id
            ["P002", "Bad Number", "abc", "1.10", "32.0"],  # row 4: not a number
            ["P003", "Good Two", "63", "1.10", "32.3"],
        ])
        participants, rejections = load_profiles(path)
 
    assert set(participants) == {"P001", "P003"}, f"got {set(participants)}"
    assert len(rejections) == 2, f"expected 2 rejections, got {len(rejections)}"
    assert rejections[0].row_nr == 3 and rejections[0].field == "participant_id"
    assert rejections[1].row_nr == 4
    assert rejections[1].source_file == "profiles.csv"
    print("test_load_profiles_rejects_bad_rows passed")


def test_load_profiles_rejects_short_row():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "profiles.csv"
        csv_wite(path, PROFILE_HEADER, [
            ["P001", "Good One", "68", "1.20", "32.4"],
            ["P002", "Short Row", "70"],  # row 3: too short
            ["P003", "Good Two", "63", "1.10", "32.3"],
        ])
        participants, rejections = load_profiles(path)

    assert set(participants) == {"P001", "P003"}, f"got {set(participants)}"
    assert len(rejections) == 1, f"expected 1 rejection, got {len(rejections)}"
    assert rejections[0].row_nr == 3 and rejections[0].field is None
    print("test_load_profiles_rejects_short_row passed")

def test_load_profiles_missing_file():
    expect_error(FileNotFoundError, load_profiles,Path("data")/ "nonexistent.csv")
    print("test_load_profiles_missing_file passed")





def test_load_sessions():
    sessions, rejections = load_sessions(SESSIONS_PATH, load_real_participants())
    assert set(sessions) == {"FIT-2026-001", "FIT-2026-002", "FIT-2026-003", "FIT-2026-004"}, f"got {set(sessions)}"
    for session in sessions.values():
        assert session.usable_count == 6, f"{session.session_id} has {session.usable_count} usable observations"
    assert len(rejections) == 5, f"expected 5 rejections, got {len(rejections)}"
    print("test_load_sessions passed")



def test_load_sessions_with_invalid():
    sessions, rejections = load_sessions(INVALID_PATH, load_real_participants())
    assert set(sessions) == {"FIT-2026-101"}, f"got {set(sessions)}"
    assert sessions["FIT-2026-101"].usable_count == 1, f"got {sessions['FIT-2026-101'].usable_count}"
    assert len(rejections) == 10, f"expected 10 rejections, got {len(rejections)}"
    assert rejections[0].row_nr == 3 and rejections[0].field == "heart_rate"
    print("test_load_sessions_with_invalid passed")


def test_load_sessions_missing_file():
    expect_error(FileNotFoundError, load_sessions, Path("data") / "nonexistent.csv", load_real_participants())
    print("test_load_sessions_missing_file passed")


##___________________________tests_________________________
def test_load_all_sessions():
    sessions, rejections = load_all_sessions([SESSIONS_PATH, INVALID_PATH], load_real_participants())
    assert set(sessions) == {"FIT-2026-001", "FIT-2026-002", "FIT-2026-003", "FIT-2026-004", "FIT-2026-101"}, f"got {set(sessions)}"
    assert len(rejections) == 15, f"expected 15 rejections, got {len(rejections)}"
    print("test_load_all_sessions passed")



def run_all_tests():
    test_load_profiles()
    test_load_profiles_with_invalid()
    test_load_profiles_rejects_short_row()
    test_load_profiles_missing_file()
    test_load_sessions()
    test_load_sessions_with_invalid()
    test_load_sessions_missing_file()
    test_load_all_sessions()

if __name__=="__main__":
    run_all_tests()