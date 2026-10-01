from pathlib import Path

from fitness_analyzer.analysis import summary, classify_hr, classify_sr, classify_temp, classify_al, recoveryDetection, SessionClass, analyseSession

from fitness_analyzer.io_csv import load_all_sessions, load_profiles, load_sessions

from fitness_analyzer.models import Participant, fitnessSession, Observation






DATA_DIR=Path("data")
TEMP_TEST_DIR=Path("tests/fixtures")

PROFILE_PATH= DATA_DIR/"participants.csv"

SESSION_PATHS = [
    DATA_DIR/ "fitness_sessions.csv" ,
    DATA_DIR/"fitness_sessions_invalid.csv"

    ]


def load_results():

    participant, _ = load_profiles(PROFILE_PATH)
    sessions, _ = load_all_sessions(SESSION_PATHS, participant)  

    return {session_id: analyseSession(session) for session_id, session in sessions.items()} 

def write_temp_results(results):
    TEMP_TEST_DIR.mkdir(parents=True, exist_ok=True)
    path= TEMP_TEST_DIR/ "test_fit_ses.csv"

    lines=[
        f"{sesssion_id}: {result}" 
        for sesssion_id, result in results.items()
    ]
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    print(f"wrote valid session results to {path}")
    print(f"wrote {len(results)} to {path}")

    
##  ___________________individual checks _________________

def test_resting_sessiom(results):
    result=result["FIT-2026-001"]
    assert result["classification"]=="resting", f"expected resting, got {result['classification']}"

