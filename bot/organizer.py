import shutil
import json
from pathlib import Path
from bot.name_suggester import classify_file

def organize_subject(subject_path: Path):
    """
    Organizes the files in a subject folder by category
    and moves them to appropriate subdirectories.
    Also collects a summary of file counts per category.
    """
    summary = {
        "raw/func": 0,
        "raw/anat": 0,
        "raw/dicom": 0,
        "meta": 0,
        "logs": 0,
        "protocols": 0,
        "unsorted": 0
    }

    for file in subject_path.iterdir():
        if file.is_file():
            category = classify_file(file.name)
            summary[category] = summary.get(category, 0) + 1

            target_folder = subject_path / category
            target_folder.mkdir(parents=True, exist_ok=True)
            target_path = target_folder / file.name

            shutil.move(str(file), str(target_path))
            print(f"Moved {file.name} → {category}")

    generate_report(subject_path, summary)


def generate_report(subject_path: Path, summary: dict):
    """
    Saves a report as JSON with the number of files per category.
    """
    subject_id = subject_path.name
    report_data = {subject_id: summary}

    results_path = Path("results")
    results_path.mkdir(exist_ok=True)

    output_file = results_path / f"report_{subject_id}.json"
    with open(output_file, "w") as f:
        json.dump(report_data, f, indent=4)

    print(f"📄 Report saved: {output_file}")
