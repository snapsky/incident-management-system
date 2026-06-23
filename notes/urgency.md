# Urgency Classification Findings

## Summary

The models in `train/urgency_classification` struggle on the original 4-class urgency task mainly because the dataset is highly imbalanced. The rarest class, `Low`, has extremely small support, and `Critical` is also much less frequent than `Medium` and `High`. As a result, the models learn the dominant classes well enough to get moderate overall accuracy, but they fail to separate all four urgency levels reliably.

Binary screening works better because it changes the problem from fine-grained triage into a safer operational decision:
- `Low` and `Medium` are merged into `routine-review`
- `High` and `Critical` are merged into `immediate-attention`

That reduces class sparsity, removes the hardest boundary around the tiny `Low` class, and aligns the task with the real screening objective: avoid missing urgent incidents.

## Why 4-Class Models Fail

The main issue is class imbalance.

From the executed notebooks:
- In the LightGBM notebook, the test split has only `6` `Low` cases and `75` `Critical` cases, versus `192` `Medium` and `267` `High`.
- Similar imbalance appears across the other urgency notebooks.

This creates three problems:

1. `Low` is too rare to learn robustly.

Across multiple multiclass models, `Low` recall is effectively zero or near zero:
- LightGBM cost-sensitive test: `Low recall = 0.00`
- Naive Bayes cost-sensitive test: `Low recall = 0.17`
- XGBoost cost-sensitive test: `Low recall = 0.09`

That means the model does not have enough signal to consistently identify `Low` incidents as a distinct class.

2. `Critical` is consistently pulled toward `High`.

Even when cost-sensitive training helps, there is still heavy confusion between `High` and `Critical`.
- LightGBM cost-sensitive test: `Critical recall = 0.31`
- XGBoost cost-sensitive test: `Critical recall = 0.46`
- Naive Bayes cost-sensitive test: `Critical recall = 0.81`, but at the cost of more false positives into `Critical`

This shows the features are much better at detecting "some urgency" than at separating nearby severity bands.

3. Accuracy hides the real failure.

Some models reach around `0.58` to `0.61` test accuracy, but this is misleading because the majority classes dominate the score.
- Naive Bayes baseline test accuracy: `0.6111`
- LightGBM cost-sensitive test accuracy: `0.6037`
- XGBoost cost-sensitive test accuracy: `0.5741`

The better indicators are macro F1 and balanced accuracy, and those stay much weaker:
- LightGBM cost-sensitive test: `balanced accuracy = 0.3995`, `macro F1 = 0.4081`
- XGBoost cost-sensitive test: `balanced accuracy = 0.4441`, `macro F1 = 0.4501`
- Naive Bayes cost-sensitive test: `balanced accuracy = 0.5157`, `macro F1 = 0.4580`

So the multiclass models are not failing because the algorithms are fundamentally poor. They are failing because the dataset distribution does not support stable 4-way separation, especially for `Low` and the `High`/`Critical` boundary.

## Why Binary Screening Works Better

Binary screening works because it simplifies the question to the one that matters operationally:

`Should this incident stay in the routine queue, or should it be escalated for immediate attention?`

This works better for three reasons:

1. The class distribution becomes much healthier.

Instead of trying to learn four uneven buckets, the model learns two larger buckets. That gives each side more examples and reduces instability caused by tiny minority classes.

2. The task matches the signal in the text better.

The text appears to encode urgency cues strongly enough to distinguish routine incidents from urgent incidents, but not strongly enough to reliably split `Low` from `Medium` or `High` from `Critical`.

3. Screening prioritizes recall, which is the correct operational goal.

For hospital-style urgency triage, the highest risk is a false negative: an actually urgent incident being left in the routine queue. Binary screening lets us tune a threshold to favor urgent-case recall directly.

This is visible in the executed screening notebooks:
- LightGBM screening test recall for `immediate-attention`: `0.8918`
- Naive Bayes screening test recall: `0.9854`
- SVM screening test recall: `0.9795`

Those recall numbers are much stronger than the corresponding 4-class performance on `Critical`.

## Best Binary Screening Model

The best current model for binary screening is the **SVM screening model** in `train/urgency_classification/training_svm.ipynb`.

### Test-set results

- `Accuracy = 0.7370`
- `Precision (immediate-attention) = 0.7128`
- `Recall (immediate-attention) = 0.9795`
- `F1 (immediate-attention) = 0.8251`
- `PR-AUC = 0.9179`

### Why SVM is the best choice

It gives the best overall balance among the evaluated screening models.

Compared with the alternatives:

- **Naive Bayes**
  - `Recall = 0.9854`
  - `F1 = 0.8082`
  - `PR-AUC = 0.9092`
  - Naive Bayes has slightly higher recall, but it produces more false positives and lower overall ranking quality.

- **LightGBM**
  - `Recall = 0.8918`
  - `F1 = 0.8005`
  - `PR-AUC = 0.8709`
  - LightGBM is clearly weaker on urgent-case recall and on overall screening quality.

SVM is the best recommendation because:
- it keeps urgent-case recall extremely high (`0.9795`)
- it achieves the best F1 for the urgent class (`0.8251`)
- it achieves the best PR-AUC (`0.9179`)
- it also has the best test accuracy among the executed screening notebooks (`0.7370`)

In practical terms, SVM misses very few urgent incidents while reducing unnecessary escalations better than Naive Bayes.

## Recommendation

Do not use the current models as final 4-class urgency classifiers. The data imbalance is too severe, and the reports show unstable minority-class performance.

Use the binary screening setup instead, and use the **SVM screening model** as the current best option.

Recommended workflow:
- first run SVM binary screening to separate `routine-review` from `immediate-attention`
- then let staff perform the final fine-grained decision within the urgent queue

This fits the observed model behavior much better than forcing direct 4-class prediction from the current dataset.
