"""
primary purpose of formatinf, printing and writing to csv files

from A1:
- logprint, formattext,
"""
import csv
## --------------text aid --------------##
def formatPrintText():
    pass

def suportive_messages(assign1):
    messages=["rest is important!",
              "Good job!",
              "great!",
              "a good rest is good for the soul!",
              "recorded data is insufficient :("
              ]
    possible_assign=["resting", "moderate activity", "high activity", "recovering", "insufficient data"]
    if assign1 in possible_assign:
        if assign1==possible_assign[0]:
            return messages[0]
        elif assign1==possible_assign[1]:
            return messages[1]
        elif assign1==possible_assign[2]:
            return messages[2]
        elif assign1==possible_assign[3]:
            return messages[3]
        elif assign1==possible_assign[4]:
            return messages[4]
    else:
        return "hello, your activety class has eluded me"


def get_simmilar(aDict, metric):
    simmilar_items=[(k,v) for k,v in aDict.items() if metric in k]
    return simmilar_items

## -----------------------------------------------##
def TerminalLogPrint():
    pass




def write_summary_csv(result, output_dir):
    """
    writes to CSV file: analysis_summary.csv
    """
    path= output_dir/ "analysis_summary.csv"
    field_names= [
        "session_id", "participant_id", "usable_obs",
        "classification", "reason", 
        "hr_min", "hr_max", "hr_avg",
        "skin_min", "skin_max", "skin_avg",
        "temp_min", "temp_max", "temp_avg",
        "activity_min", "activity_max", "activity_avg",
        "signal_avg"

    ]
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer=csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        for res in result:
            writer.writerow(res)


def build_report_text(result):
    """

    """
    sup_msg=suportive_messages(result["classification"])
    hr_sum=get_simmilar(result, "hr")
    sr_sum=get_simmilar(result,"skin")
    temp_sum=get_simmilar(result, "temp")
    al_sum=get_simmilar(result, "activity")
    summary_lines=[
        "-"*75,
        f"hello {result['participant_id']}",
        f"your session: {result['session_id']}",
        f"you just finished a session of {result['classification']}",
        f"{sup_msg}",
        f"you had {result['usable_obs']} usable observation(s)",
        "here are your data summaries",
        "-"*20+"heart rate"+"-"*20,
        f"{hr_sum[0]}, {hr_sum[1]}, {hr_sum[2]}",
        "-"*20+"skin response"+"-"*20,
        f"{sr_sum[0]}, {sr_sum[1]}, {sr_sum[2]}",
        "-"*20+"temperature"+"-"*20,
        f"{temp_sum[0]}, {temp_sum[1]}, {temp_sum[2]}",
        "-"*20+"activity level"+"-"*20,
        f"{al_sum[0]}, {al_sum[1]}, {al_sum[2]}",
        f"throughotut the session your siganl quality averaged {result['signal_avg']}"
    ]

    return "\n".join(summary_lines)




def write_report_txt(result, ourput_dir):
    """
    writes to analysis_report.txt
    """
    path = ourput_dir/"analysis_report.txt"

    report_blocks =  [build_report_text(r) for r in result]

    with open(path, "w", encoding="utf-8") as file:
        file.write("\n\n".join(report_blocks))



def write_rejected(rejections, output_dir):
    """
    writes to rejected_input.txt
    """

    path = output_dir/"rejected_input.txt"

    rejects= rejections
    if not rejects:
        lines=["no rejected records. "]

    else:
        lines=[
            f"{r.source_file} (row {r.row_nr}):"
            f"field={r.field}, reason={r.reason}"
            for r in rejects
        ]
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))






def read_report_csv(output_dir):
    path= output_dir/ "analysis_summary.csv"
    with open(path, "r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))

def read_report_text(output_dir):
    path = output_dir/"analysis_report.txt"
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def read_reject(output_dir):
    path= output_dir/ "rejected_input.txt"
    with open(path, "r", encoding="utf-8") as file:
        return file.read()




