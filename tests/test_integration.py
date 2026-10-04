
import csv
from pathlib import Path
from unittest import result
import tempfile

from fitness_analyzer.analysis import analyseSession
from fitness_analyzer.analysis import analyseSession
from fitness_analyzer.io_csv import load_profiles, load_sessions, load_all_sessions
from fitness_analyzer.reports import build_report_text, write_report_txt, write_summary_csv, write_rejected, read_report_csv, read_report_text, read_reject


DATA_DIR = Path("data")
PROFILE_PATH = DATA_DIR / "participants.csv"
SESSIONS_PATH = DATA_DIR / "fitness_sessions.csv"
INVALID_PATH = DATA_DIR / "fitness_sessions_invalid.csv"

SESSION_PATHS = [SESSIONS_PATH, INVALID_PATH]

PROFILE_HEADER = [
    "participant_id", "name", "baseline_heart_rate",
                  "baseline_skin_response", "baseline_temperature"  
]

SESSION_HEADER = [
    "session_id", "participant_id", "timestamp", "heart_rate",
    "skin_response", "temperature", "activity_level", "signal_quality"
]

EXPECTED_CLASSIFICATION = {
    "FIT-2026-001": "resting",
    "FIT-2026-002": "moderate activity",
    "FIT-2026-003": "high activity",
    "FIT-2026-004": "recovering",
    "FIT-2026-101": "insufficient data",

}

OUTPUT_FILES = ("analysis_summary.csv", "analysis_report.txt", "rejected_input.txt")

def csv_write(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

def main_run(profile_path, session_paths, output_dir):
    participants, prof_rejections = load_profiles(profile_path)
    sessions, ses_rejections = load_all_sessions(session_paths, participants)   
    result=[analyseSession(s) for s in sessions.values()]
    rejections= prof_rejections + ses_rejections

    write_summary_csv(result, output_dir)
    write_report_txt(result, output_dir)
    write_rejected(rejections, output_dir)

    return result, rejections


def test_main_creates_all_output_files():
    with tempfile.TemporaryDirectory() as tmp:
        output_dir = Path(tmp)
        main_run(PROFILE_PATH, SESSION_PATHS, output_dir)
        for file in OUTPUT_FILES:
            path = output_dir / file
            assert path.exists(), f"{file} was not created"
            assert path.stat().st_size > 0, f"{file} is empty"
        print("test_main_creates_all_output_files passed")    

def test_summary_csv_has_expected_sessions():
    with tempfile.TemporaryDirectory() as tmp:
        output_dir = Path(tmp)
        main_run(PROFILE_PATH, SESSION_PATHS, output_dir)
        rows = read_report_csv(output_dir)

        assert len(rows) == 5, f"expected 5 rows but got {len(rows)}"
        found={row["session_id"] : row["classification"] for row in rows}

        assert found == EXPECTED_CLASSIFICATION, f"expected {EXPECTED_CLASSIFICATION} but got {found}"
        print("test_summary_csv_has_expected_sessions passed")



def test_csvVal_match_analysis():
    with tempfile.TemporaryDirectory() as tmp:
        output_dir = Path(tmp)
        results, _= main_run(PROFILE_PATH, SESSION_PATHS, output_dir)
        rows = read_report_csv(output_dir)

        rows_id={row["session_id"] : row for row in rows}

        for result in results:
            row=rows_id[result["session_id"]]

            for key, value in result.items():
                assert row[key]==str(value), (f"{result['session_id']} {key} expected {value} but got {row[key]}")

        print("test_csvVal_match_analysis passed")

def test_numeric_csv_values():
    with tempfile.TemporaryDirectory() as tmp:
        output_dir = Path(tmp)
        main_run(PROFILE_PATH, SESSION_PATHS, output_dir)
        rows = read_report_csv(output_dir)

        row=next(r for r in rows if r["session_id"]=="FIT-2026-001")

        assert int(row["usable_obs"]) == 6, f"expected 6 usable_obs but got {row['usable_obs']}"
        assert float(row["signal_avg"]) == 0.97, f"expected 0.95 signal_avg but got {row['signal_avg']}"
        assert float(row["hr_min"]) <= float(row["hr_max"]), f"expected hr_min <= hr_max but got {row['hr_min']} > {row['hr_max']}"
        
        print("test_numeric_csv_values passed")
    

def test_report_all_expected_sessions():
    with tempfile.TemporaryDirectory() as tmp:
        output_dir = Path(tmp)
        main_run(PROFILE_PATH, SESSION_PATHS, output_dir)
        text = read_report_text(output_dir)

    for session_id, classification in EXPECTED_CLASSIFICATION.items():
        assert f"your session: {session_id}" in text, f"session id missing from text"

    for classification in set(EXPECTED_CLASSIFICATION.values()):
        assert f"session of {classification}" in text, f"'{classification}' missing from text"
   
    assert text.count("hello P") == 5, f"expected 5text blocks, got {text.count('hello P')}"
    print("test_report_all_expected_sessions passed")
    

def test_rejected_all_sessions_report():

    with tempfile.TemporaryDirectory() as tmp:
        output_dir= Path(tmp)
        _,rejections=main_run(PROFILE_PATH, SESSION_PATHS, output_dir)
        lines=read_reject(output_dir).splitlines()

        assert len(rejections) ==15, f"expected 15 rejections, got {len(rejections)}"
        assert len(lines) == 15, f"expected 15 lines in rejected_input.txt, got {len(lines)}"
        print("test_rejected_all_sessions_report passed")


def test_poorSignal_only_rejected_sessions_report():
    with tempfile.TemporaryDirectory() as tmp:
        output_dir=Path(tmp)
        main_run(PROFILE_PATH, SESSION_PATHS, output_dir)
        summary_ids={row["session_id"] for row in read_report_csv(output_dir)}
        report=read_report_text(output_dir)
        reject=read_reject(output_dir)

    assert "FIT-2026-005" not in summary_ids, "'FIT-2026-005' should not be in summary"
    assert "FIT-2026-005" not in report, "'FIT-2026-005' should not be in report"
    assert reject.count("field=signal_quality, reason=Poor signal quality") == 5

    print("test_poorSignal_only_rejected_sessions_report passed")


def test_run_main_multiple_times():
    with tempfile.TemporaryDirectory() as tmp:
        output_dir=Path(tmp)
        main_run(PROFILE_PATH, SESSION_PATHS, output_dir)
        first=[(output_dir/name).read_text(encoding="utf-8") for name in OUTPUT_FILES]
        main_run(PROFILE_PATH, SESSION_PATHS, output_dir)
        second=[(output_dir/name).read_text(encoding="utf-8") for name in OUTPUT_FILES]

    assert first == second, "output change dbetween two runs of same data"
    print("test_run_main_multiple_times passed")
   


def test_w_clean_data(): 
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        profile_path=tmp/"profile.csv"
        session_path=tmp/"session.csv"
        output_dir=tmp/"out"
        output_dir.mkdir()

        csv_write(profile_path, PROFILE_HEADER, [["P001", "test_person", "69", "1.20", "32.4"]])
        csv_write(session_path, SESSION_HEADER, [
            ["FIT-2026-001", "P001", "0", "68", "1.18", "32.4", "0.08", "0.98"],
            ["FIT-2026-001", "P001", "1", "69", "1.22", "33.0", "0.13", "0.95"],
            ["FIT-2026-001", "P001", "2", "70", "1.20", "32.8", "0.10", "0.97"]
            ])   
        results, rejects=main_run(profile_path, [session_path], output_dir)
        rejected_text=read_reject(output_dir)
        rows=read_report_csv(output_dir)

    assert len(rejects) ==0 , f"expected 0 rejected data, got {len(rejects)}"
    assert "no rejected records." in rejected_text
    assert len(rows) == 1 and rows[0]["classification"] =="resting"
    print( "test_w_clean_data passed")


def test_dirty_data():
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        profile_path=tmp/"profile.csv"
        session_path=tmp/"session.csv"
        output_dir=tmp/"out"
        output_dir.mkdir()

        csv_write(profile_path, PROFILE_HEADER, [["P001", "good_test", "69", "1.20", "32.4"], ["P02", "bad_test", "69", "1.20", "32.4"]])
        csv_write(session_path, SESSION_HEADER, [
            ["FIT-2026-001", "P001", "0", "68", "1.18", "32.4", "0.08", "0.98"],
            ["FIT-2026-001", "P001", "1", "69", "1.22", "33.0", "0.13", "0.95"],
            ["FIT-2026-001", "P001", "2", "70", "1.20", "32.8", "0.10", "0.97"],
            ["FIT-2026-001", "P002", "0", "75", "1.23", "31.9", "0.25", "0.96"]
            ])   
        results, rejects=main_run(profile_path, [session_path], output_dir)
        rejected_text=read_reject(output_dir)
        rows=read_report_csv(output_dir)

    assert len(rejects) ==2 , f"expected 0 rejected data, gor {len(rejects)}"
    assert "no rejected records." not in rejected_text
    assert len(rows) == 1 and rows[0]["session_id"] =="FIT-2026-001"
    print( "test_w_clean_data passed")

##____________________________________________----
def run_all_tests():
    test_main_creates_all_output_files()
    test_summary_csv_has_expected_sessions()
    test_csvVal_match_analysis()
    test_numeric_csv_values()
    test_report_all_expected_sessions()
    test_rejected_all_sessions_report()
    test_poorSignal_only_rejected_sessions_report()
    test_run_main_multiple_times()
    test_w_clean_data()
    test_dirty_data()


if __name__=="__main__":
    run_all_tests()


