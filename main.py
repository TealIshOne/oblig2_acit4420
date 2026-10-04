import csv
import argparse
import sys 
from pathlib import Path

from fitness_analyzer.io_csv import load_profiles, load_all_sessions

from fitness_analyzer.analysis import analyseSession

from fitness_analyzer.reports import write_summary_csv, write_report_txt, write_rejected

#----------------paths -------------------------

BASE_DIR= Path(__file__).resolve().parent
DATA_DIR=BASE_DIR/"data"

PROFILE_PATH=DATA_DIR/"participants.csv"
SESSION_PATHS=[
    DATA_DIR/"fitness_sessions.csv",
    DATA_DIR/"fitness_sessions_invalid.csv"
]

OUTPUT_DIR=BASE_DIR/"outputs"

#-----------------------------------------

def parse_args():
    parser=argparse.ArgumentParser(
        description="analyse simulated fitness sessions and write rpeorts"
    )

    parser.add_argument(
        "--profiles", type=Path, default=PROFILE_PATH,
        help="participant profiles csv (defualt data/participant.csv)"
    
    )

    parser.add_argument(
        "--sessions", type=Path, nargs="+", default=SESSION_PATHS,
        help="session csv file(s) (defualt: sesson(s) found in data/)"
    )

    parser.add_argument(
        "--output", type=Path, default=OUTPUT_DIR,
        help="folder the output raports are writen to, both txt and csv type files (defualt: output/)"
    )

    return parser.parse_args()

def run(profile_path, session_paths, output_dir):
    participant, profile_rejects=load_profiles(profile_path)
    sessions, sessions_rejects=load_all_sessions(session_paths, participant)


    results=[analyseSession(session) for session in sessions.values()]
    rejections=profile_rejects +sessions_rejects

    output_dir.mkdir(parents=True, exist_ok=True)
    write_summary_csv(results, output_dir)
    write_report_txt(results, output_dir)
    write_rejected(rejections, output_dir)

    return results, rejections


def print_overview(results, rejections, output_dir):
    accepted_rows=sum(r["usable_obs"] for r in results)
    print("-"*60)
    print(f"accepted rows: {accepted_rows} in {len(results)} sessions(s)")
    print(f"rejected rows: {len(rejections)}")
    print("-"*60)

    for r in results:
        print(f"{r['session_id']}  {r['participant_id']} {r['usable_obs']} obs -> {r['classification']}")
    print("-"*60)


def main():
    args_=parse_args()
    try:
        result, rejects=run(args_.profiles, args_.sessions, args_.output)
    except (FileNotFoundError, PermissionError) as e:
        print(f"error {e}")
    except csv.Error as e:
        print(f"error: could not read csv file: {e}")

    print_overview(result,rejects,args_.output)


if __name__ == "__main__":
    main()


