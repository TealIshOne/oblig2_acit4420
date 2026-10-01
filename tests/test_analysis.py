from pathlib import Path

from fitness_analyzer.analysis import summary, classify_hr, classify_sr, classify_temp, classify_al, recoveryDetection, SessionClass, analyseSession


from fitness_analyzer.models import Participant, fitnessSession, Observation






DATA_DIR=Path("data")
TEMP_TEST_DIR=Path("tests/fixtures")

PROFILE_PATH= DATA_DIR/"participants (1).csv"

SESSION_PATH = [
    DATA_DIR/ "fitness_sessions (1).csv" ,
    DATA_DIR/"fitness_sessions_invalid (1).csv"

    ]


def load_results():

    participant, _ = load_p

