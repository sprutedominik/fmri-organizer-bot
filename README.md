# fMRI Organizer Bot

A small command-line tool that sorts the raw files of an fMRI study into a fixed folder layout per participant and writes a count per category.

## Why

After a scan session, a participant folder holds a mix of functional runs, anatomical scans, DICOM files, questionnaires and logs, named however the scanner or the lab named them. Sorting that by hand for every participant is slow and easy to get wrong. I wanted one command that does it the same way each time.

## What it does

For every folder in `data/` whose name starts with `VP` (for example `data/VP02`), the tool:

1. looks at each file name,
2. assigns a category,
3. moves the file into a subfolder of that name,
4. writes `results/report_<VP>.json` with the number of files per category.

Categories: `raw/func`, `raw/anat`, `raw/dicom`, `protocols`, `meta`, `logs`, `unsorted`.

## How it works

- **Rules first.** Regular expressions on the lower-cased file name. `func`, `bold`, `run1` or `task` mean functional; `t1w`, `anat` or `mprage` mean anatomical; `.dcm` means DICOM; and so on. Order matters: the first rule that matches wins.
- **Model as fallback.** If no rule matches and a trained model exists, a TF-IDF vectoriser with logistic regression (scikit-learn) guesses the category from the file name. If there is no model either, the file goes to `unsorted`.
- **Training.** `python main.py train` fits the model on six example file names. That is enough to show the mechanism, not enough to trust the model on real data.

Example run on ten empty dummy files (sklearn installed, no model trained):

```text
Processing VP02
  readme_old.md -> unsorted
  task-familiarity_events.tsv -> raw/func
  scaninfo.txt -> meta
  questionnaire_pre.json -> protocols
  sub-02_T1w.nii -> raw/anat
  bold_run2_func.nii.gz -> raw/func
  MR000243.dcm -> raw/dicom
  participants.csv -> meta
  bold_run1_func.nii.gz -> raw/func
  MR000244.dcm -> raw/dicom
```

```json
{
    "VP02": {
        "raw/func": 3,
        "raw/anat": 1,
        "raw/dicom": 2,
        "meta": 2,
        "logs": 0,
        "protocols": 1,
        "unsorted": 1
    }
}
```

Two of these show the limits of rule order: the events file lands in `raw/func` because its name contains `task`, and `scaninfo.txt` lands in `meta` because the `.txt` rule comes before the log rule.

## How to run

```bash
pip install scikit-learn joblib
python main.py train      # optional, fits the fallback model
python main.py organize   # sorts every data/VP* folder
```

The tool **moves** files. Run it on a copy of your data first.

## Limits

- Rules are tuned to one lab's naming. Any `.json` file, including BIDS sidecars, lands in `protocols`.
- The fallback model is a demonstration trained on six names.
- `main.py` is the working entry point. The `bot/` package holds an earlier variant (Naive Bayes, separate rules) that `main.py` does not use.
- `requirements.txt` is empty; the command under "How to run" installs what `main.py` needs.

## Tech

Python · scikit-learn · joblib · pathlib
