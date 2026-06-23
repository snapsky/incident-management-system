# Feature Engineering and Preprocessing Report

## Summary

The notebook [feature_engineering_and_preprocess.ipynb](/home/lakshan/ssp/IMS/preprocess/feature_engineering_and_preprocess.ipynb) follows a deliberately simple preprocessing pipeline. It does not apply heavy text cleaning, stemming, lemmatization, or handcrafted statistical features. Instead, it performs three core operations:

1. text feature construction through concatenation
2. label encoding for target variables
3. randomized dataset splitting into train, validation, and test sets

This is a lightweight but practical design. The downstream models in this project, especially TF-IDF models and transformer-based models, already perform much of the useful representation learning themselves. The preprocessing stage therefore focuses on building a clean, consistent, model-ready dataset rather than aggressively transforming the raw text.

## Feature Engineering Steps Used

### 1. Feature concatenation

The notebook creates a new column called `feature_concatanation` by combining:
- `reporter_role`
- `incident_description`

The logic is:
- fill missing values with empty strings
- strip surrounding whitespace
- join both fields with a space
- strip the final combined string again

Resulting example structure:

`reporter_role + " " + incident_description`

This engineered text feature is then stored in:
- `data/processed/incidents_feature_engineered.csv`

### 2. Label encoding

The notebook converts categorical targets into numeric labels.

For department classification:
- it collects the unique `assigned_department` values
- sorts them
- assigns integer IDs from `0` upward

It saves the mapping to:
- `data/processed/department_label_mapping.csv`

For urgency classification:
- it enforces an explicit ordinal order:
  - `Low`
  - `Medium`
  - `High`
  - `Critical`
- it maps those to integers:
  - `Low -> 0`
  - `Medium -> 1`
  - `High -> 2`
  - `Critical -> 3`

It saves the mapping to:
- `data/processed/urgency_label_mapping.csv`

The fully encoded dataset is saved to:
- `data/processed/incidents_feature_engineered_encoded.csv`

### 3. Random shuffle and split

The notebook shuffles the encoded dataset using:
- `random_state = 42`

Then it splits the data into:
- `70%` train
- `15%` validation
- `15%` test

The generated files are:
- `data/processed/incidents_train.csv`
- `data/processed/incidents_validation.csv`
- `data/processed/incidents_test.csv`

The notebook records the final sizes as:
- train: `2520`
- validation: `540`
- test: `540`

## Why These Engineering Steps Are Required

### 1. Why feature concatenation is required

The raw dataset separates useful signal across more than one text field.

`incident_description` contains the main operational problem, but `reporter_role` also carries important context. In this project, the reporter’s role is often highly informative:
- a `Pharmacy Manager` report is more likely to map to supply, quality, or stock-related workflows
- an `ICU Charge Nurse` report may carry urgency and infrastructure context
- an `Accounts Officer` or administrative reporter can signal finance-related routing

If the model uses only `incident_description`, it loses this contextual cue. If it uses only `reporter_role`, it loses the actual incident content. Concatenation is therefore necessary because it fuses:
- role-based context
- incident-specific context

This is especially important for department classification, where routing decisions often depend on both:
- who is reporting
- what exactly happened

Without this engineered combined feature, downstream text models would receive an incomplete representation of the incident.

### 2. Why label encoding is required

Most machine-learning training pipelines do not operate directly on raw string labels. They require stable numeric target values.

Label encoding is required because it:
- converts department names into classifier-ready integers
- converts urgency classes into numeric targets for multiclass learning
- ensures consistent label usage across training, evaluation, saving, and inference

For urgency classification, the explicit ordering is particularly important. The notebook does not assign urgency IDs alphabetically. It uses a domain-correct severity order:
- `Low < Medium < High < Critical`

That matters because:
- it preserves semantic meaning
- it avoids accidental remapping if categories are discovered in a different order
- it keeps all urgency notebooks aligned to the same target definition

Without fixed label mappings, different notebooks or reruns could silently use inconsistent class IDs, which would invalidate model comparisons.

### 3. Why shuffling and splitting are required

A model cannot be evaluated honestly on the same data it was trained on. The split process is therefore essential, not optional.

The shuffle-and-split step is required because it:
- reduces ordering bias from the source CSV
- creates separate data for training, model selection, and final evaluation
- makes notebook comparisons fair because the same split files are reused across models

The three-way split has a specific purpose:

- `train`
  - used to fit the model parameters
- `validation`
  - used to compare configurations, tune thresholds, and choose between candidate models
- `test`
  - used only for final performance reporting

This separation is important because many notebooks in the project select models or thresholds using validation metrics. Without a distinct validation set, the test set would be indirectly used for tuning, and the reported results would be optimistic and unreliable.

The fixed random seed is also important because it gives reproducibility. All models trained later in the repository are evaluated on the same split, which makes cross-model comparison meaningful.

## Why This Preprocessing Design Is Important

The design is intentionally minimal, and that is a strength rather than a weakness.

### 1. It keeps the raw semantic signal intact

The notebook does not aggressively normalize the text. It does not remove domain phrasing, abbreviations, or sentence structure. That is useful because hospital incident text often contains meaningful operational detail such as:
- unit names
- role titles
- department references
- equipment names
- timing cues
- service-specific terminology

For modern NLP pipelines, preserving this raw wording is often better than heavy manual cleaning.

### 2. It supports multiple model families with one shared dataset

The engineered outputs are reused by:
- Naive Bayes
- SVM
- XGBoost / LightGBM text pipelines
- LSTM
- DistilBERT

This is important because it gives the project a single preprocessing contract. All department and urgency experiments consume the same prepared files, which improves consistency and comparability.

### 3. It separates data preparation from modeling

The notebook builds reusable processed datasets once and saves them to disk. That keeps training notebooks focused on modeling rather than repeatedly rebuilding the same inputs.

This is operationally important because it:
- reduces duplication
- lowers the chance of preprocessing drift between notebooks
- makes debugging easier
- allows future models to plug into the same prepared data

## Strengths of the Current Approach

- simple and easy to audit
- reproducible because of fixed saved outputs and fixed split seed
- preserves domain language rather than over-cleaning it
- gives both text features and numeric targets in a reusable format
- supports both classical ML and deep learning workflows

## Limitations of the Current Approach

The notebook is effective, but it is still a minimal preprocessing pipeline. It does not yet include:
- text normalization beyond whitespace trimming
- timestamp-derived features from `date` or `time`
- role normalization or hierarchy grouping
- spelling correction or abbreviation normalization
- stratified splitting
- explicit handling of class imbalance during splitting

These are not necessarily mistakes. In many cases, the current models can already learn effectively from the existing text fields. But these are possible future improvements if the project needs stronger performance or more robust class coverage.

## Overall Conclusion

The notebook applies a small number of preprocessing steps, but each one is essential.

The core engineering logic is:
- combine the most informative text fields into one model-ready input
- convert categorical targets into stable numeric labels
- create reproducible train, validation, and test splits

These steps are important because they transform raw incident records into a consistent dataset that all later training notebooks can use safely. The preprocessing is not sophisticated in quantity, but it is strong in purpose: it preserves meaningful hospital text context while establishing the exact structure required for reliable machine-learning experiments.
