"""
lods CSV and creates instance of models.py
"""


import csv
from pathlib import Path

from fitness_analyzer.exceptions import InvalidIdentifierError, InvalidRecordError
from fitness_analyzer.models import Participant, Observation, fitnessSession
from fitness_analyzer.validation import isValidRow


class Rejection:
    def __init__(self, source_file, row_nr, field, reason):
        self.source_file = source_file
        self.row_nr=row_nr
        self.field=field
        self.reason=reason



def _open_csv (path):
    path=Path(path)

    try:
        return open(path, "r", encoding="utf-8", newline="")
    except FileNotFoundError as e:
        raise FileNotFoundError (f" could not find CSV file: {path}") from e
    except PermissionError as e:
        raise PermissionError (f" No persmission to read CSV file: {path}") from e


def load_profiles(path):
    path=Path(path)
    paticipants=dict()
    rejections=list()

    with _open_csv(path) as file:
        try:
            reader =csv.DictReader(file)
            for row_nr, row in enumerate(reader,start=2):
                try:
                    participant = Participant.instanciate_row(row)
                    paticipants[participant.ID]=participant
                except InvalidIdentifierError as e:
                    rejections.append(Rejection(source_file=path.name,
                                                 row_nr=row_nr, field=e.id_type,
                                                   reason=str(e)))

                except (ValueError, KeyError, TypeError) as e:
                    rejections.append(Rejection(source_file=path.name, row_nr=row_nr,
                                                field=None, reason=f"could not load profile row, {e}"))
        except csv.Error as e:
            raise csv.Error(f" Error reading {path}: {e}") from e
    return paticipants, rejections



def load_sessions(path,participants):
    path=Path(path)
    sessions=dict()
    rejections=list()
    known_ids=set(participants.keys())

    with _open_csv(path) as file:
        try:
            reader =csv.DictReader(file)
            for row_nr, row in enumerate(reader,start=2):
                try:
                    validated=isValidRow(row,known_ids)
                except (InvalidIdentifierError, InvalidRecordError) as e:
                    field=getattr(e, "field", None) or getattr(e, "id_type", None)
                    reason=getattr(e, "reason", None) or str(e)

                    rejections.append(Rejection(source_file=path.name,
                                                 row_nr=row_nr, field=field,
                                                   reason=reason))
                    continue
                session_id=validated["session_id"]
                if session_id not in sessions:
                    sessions[session_id]= fitnessSession(
                    session_id=session_id,
                    participant=participants[validated["participant_id"]])
                observation=Observation.from_row(validated)
                sessions[session_id].add_obs(observation)


        except csv.Error as e:
            raise csv.Error(f" Error reading {path}: {e}") from e
    return sessions, rejections


def load_all_sessions(paths, participants):
    all_sessions = dict()
    all_rejections=list()

    for path in paths:
        sessions, rejections, =load_sessions(path, participants)
        all_rejections.extend(rejections)
        for session_id, session in sessions.items():
            if session_id not in all_sessions:
                all_sessions[session_id]=session
            else:
                for obs in session.observations:
                    all_sessions[session_id].add_obs(obs)
    return all_sessions, all_rejections


