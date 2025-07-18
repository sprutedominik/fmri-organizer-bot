# fMRI Organizer Bot

This repository contains a modular Python-based command-line tool for the automated organization of raw fMRI study files. It uses both rule-based logic and a lightweight machine learning model to classify files into standardized folder structures.

## Overview

The tool processes subject folders (e.g., `data/VP02`) and assigns files to categories such as:

- `raw/func` (functional scans)
- `raw/anat` (anatomical scans)
- `raw/dicom` (DICOM files)
- `protocols` (questionnaires, study protocols)
- `meta` (metadata files, CSVs, TSVs, etc.)
- `logs` (scanner logs and auxiliary files)
- `unsorted` (fallback category for unclassified files)

After classification, files are moved accordingly and a summary report is generated in JSON format for each subject.

## Key Features

- Rule-based file classification using regular expressions
- Optional use of machine learning (TF-IDF + Logistic Regression) when pattern-based classification fails
- Modular structure with separate components for classification, file management, and reporting
- JSON report generation with file counts per category
- Easily adaptable to other studies or institutions

## Usage

Train the machine learning model on sample filenames (optional):

```bash
python main.py train

