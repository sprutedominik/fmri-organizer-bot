#!/usr/bin/env python3
import sys
import shutil
import json
import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

def classify_file_regex(filename: str) -> str:
    name = filename.lower()
    if re.search(r'func|bold|run\d|task', name):
        return 'raw/func'
    if re.search(r't1w|anat|mprage|sag|brain', name):
        return 'raw/anat'
    if name.endswith('.dcm'):
        return 'raw/dicom'
    if re.search(r'proto|questionnaire|survey|form|json', name):
        return 'protocols'
    if name.endswith(('.txt', '.tsv', '.csv')):
        return 'meta'
    if 'log' in name or 'scaninfo' in name:
        return 'logs'
    return None

class FileClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression()
    def train(self, filenames, labels):
        X = self.vectorizer.fit_transform(filenames)
        self.model.fit(X, labels)
    def predict(self, filename):
        X = self.vectorizer.transform([filename])
        return self.model.predict(X)[0]
    def save(self, path='results/model.joblib'):
        Path('results').mkdir(exist_ok=True)
        joblib.dump((self.vectorizer, self.model), path)
    def load(self, path='results/model.joblib'):
        self.vectorizer, self.model = joblib.load(path)

clf = FileClassifier()
try:
    clf.load()
    ml_ready = True
except:
    ml_ready = False

def generate_report(subject_path: Path, summary: dict):
    report = {subject_path.name: summary}
    out = Path('results')
    out.mkdir(exist_ok=True)
    fpath = out / f'report_{subject_path.name}.json'
    with open(fpath, 'w') as fp:
        json.dump(report, fp, indent=4)
    print(f'Report written to {fpath}')

def organize():
    print('Starting organization...')
    base = Path('data')
    if not base.exists():
        print(f'Data folder not found: {base.resolve()}')
        return
    for subj in base.iterdir():
        if subj.is_dir() and subj.name.startswith('VP'):
            print(f'Processing {subj.name}')
            summary = dict.fromkeys(['raw/func','raw/anat','raw/dicom','meta','logs','protocols','unsorted'], 0)
            for fpath in list(subj.iterdir()):
                if not fpath.is_file():
                    continue
                cat = classify_file_regex(fpath.name)
                if cat is None and ml_ready:
                    cat = clf.predict(fpath.name)
                if cat is None:
                    cat = 'unsorted'
                summary[cat] += 1
                tgt = subj / cat
                tgt.mkdir(parents=True, exist_ok=True)
                shutil.move(str(fpath), str(tgt / fpath.name))
                print(f'  {fpath.name} -> {cat}')
            generate_report(subj, summary)
    print('Organization completed.')

def train():
    print('Starting training...')
    example_filenames = ['func_run1_bold.nii.gz','T1w_brain.nii','scaninfo.txt','form_survey.json','notes.csv','MR000243.dcm']
    example_labels = ['raw/func','raw/anat','logs','protocols','meta','raw/dicom']
    clf.train(example_filenames, example_labels)
    clf.save()
    print('Model trained and saved.')

def usage():
    print('Usage:')
    print('  python main.py organize')
    print('  python main.py train')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    elif sys.argv[1] == 'organize':
        organize()
    elif sys.argv[1] == 'train':
        train()
    else:
        usage()

