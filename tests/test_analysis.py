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

def test_resting_session(results):
    result=results["FIT-2026-001"]
    assert result["classification"]=="resting", f"expected resting, got {result['classification']}"
    print("test_resting_session passed")

def test_moderate_session(results):
    result=results["FIT-2026-002"]
    assert result["classification"]=="moderate activity", f"expected moderate activity, got {result['classification']}"
    print("test_moderate_session passed")

def test_high_session(results):
    result=results["FIT-2026-003"]
    assert result["classification"]=="high activity", f"expected high activity, got {result['classification']}"
    print("test_high_session passed")



def test_recovering_session(results):
    result=results["FIT-2026-005"]
    assert result["classification"]=="recovering", f"expected recovering, got {result['classification']}"
    print("test_recovering_session passed")    

def test_insufficient_data_session(results):
    result=results["FIT-2026-004"]
    assert result["classification"]=="insufficient data", f"expected insufficient data, got {result['classification']}"
    print("test_insufficient_data_session passed")


def expected_keys(results):
    expected_keys={
        "session_id", "participant_id", "usable_obs",
        "classification", "reason", 
        "hr_min", "hr_max", "hr_avg",
        "skin_min", "skin_max", "skin_avg",
        "temp_min", "temp_max", "temp_avg",
        "activity_min", "activity_max", "activity_avg",
        "signal_avg"
    }
    for session_id, result in results.items():
        missing= expected_keys - result.keys()
        assert not missing, f"session {session_id} is missing keys: {missing}"
    print("test_expected_keys passed")  



##_______________run tests_____________________
def run_all_tests():
    results=load_results()
    write_temp_results(results)
    test_resting_session(results)
    test_moderate_session(results)
    test_high_session(results)
    test_insufficient_data_session(results)
    test_recovering_session(results)
    expected_keys(results)

    print("all tests passed")


if __name__=="__main__":
    run_all_tests()