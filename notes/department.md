# Department Classification Findings

## Summary

The department-classification task performs much better than urgency classification. All four models in `train/department_classification` learn useful decision boundaries, and three of them achieve strong test performance. The task appears easier because the department labels are more separable from the text and the class distribution is much healthier than the urgency dataset.

Among the evaluated models, **DistilBERT is the best overall model** based on recorded test metrics. It achieves the highest test accuracy and the highest macro F1, while also maintaining consistently high precision and recall across all 12 department classes. More importantly, it is the best fit for this task because department routing depends heavily on contextual wording in the incident text, and DistilBERT can model that context better than bag-of-words approaches.

## Evaluated Models

The notebooks currently contain results for:
- `training_naive_bayes.ipynb`
- `training_svm.ipynb`
- `training_distillbert.ipynb`
- `training_LSTM.ipynb`

All four use:
- `2520` train rows
- `540` validation rows
- `540` test rows
- `12` department labels

## Test Results Comparison

### DistilBERT

From `train/department_classification/training_distillbert.ipynb`:
- `test accuracy = 0.9630`
- `macro F1 = 0.9643`

Strengths:
- best overall test accuracy
- best macro F1
- very consistent class-level performance
- strongest balance across all 12 departments

Examples from the test report:
- `IT`: F1 `0.98`
- `Reception`: F1 `0.98`
- `Security`: F1 `0.99`
- `Transport`: recall `1.00`, F1 `0.97`

Weakest area:
- `Supply Department`: F1 `0.91`

Even its weakest class remains strong.

### SVM

From `train/department_classification/training_svm.ipynb`:
- `test accuracy = 0.9519`
- `macro F1 = 0.95` from the classification report

Strengths:
- strongest classical ML baseline
- high precision and recall across almost every class
- very close to DistilBERT in absolute performance

Examples:
- `Housekeeping Department`: F1 `0.98`
- `Quality Assurance department`: F1 `0.98`
- `Reception`: F1 `0.99`
- `Transport`: F1 `0.96`

Weakest areas:
- `Facility Management`: F1 `0.92`
- `Supply Department`: F1 `0.92`

SVM is clearly strong and likely the best lightweight option.

### Naive Bayes

From `train/department_classification/training_naive_bayes.ipynb`:
- `test accuracy = 0.9352`
- `macro F1 = 0.94` from the classification report

Strengths:
- strong overall performance for a very simple model
- good department separation with low training complexity

Examples:
- `IT`: F1 `0.97`
- `Reception`: F1 `0.96`
- `Security`: F1 `0.96`

Weakest areas:
- `Facility Management`: F1 `0.89`
- `Supply Department`: F1 `0.91`

Naive Bayes performs well, but it is slightly behind SVM and DistilBERT across most classes.

### LSTM

From `train/department_classification/training_LSTM.ipynb`:
- `test accuracy = 0.7519`
- `macro F1 = 0.76` from the classification report

Strengths:
- learns something meaningful
- reasonable performance on some classes such as `Reception`, `Quality Assurance department`, and `Housekeeping Department`

Weaknesses:
- much lower than the other three models
- more confusion across classes
- clear gap between near-perfect train accuracy and much lower validation/test accuracy

This notebook also shows a strong overfitting pattern:
- by epoch 10, `train accuracy = 0.9996`
- but `validation accuracy = 0.7741`

That gap is large and explains why the final test result is much weaker than the TF-IDF baselines and DistilBERT.

## Which Model Is Best

The best model is **DistilBERT**.

### Why DistilBERT is the best

1. It has the highest recorded test performance.

- DistilBERT: `accuracy = 0.9630`, `macro F1 = 0.9643`
- SVM: `accuracy = 0.9519`, `macro F1 ≈ 0.95`
- Naive Bayes: `accuracy = 0.9352`, `macro F1 ≈ 0.94`
- LSTM: `accuracy = 0.7519`, `macro F1 ≈ 0.76`

2. It is the most consistent across classes.

Its classification report shows no major weak departments. Nearly every class is around `0.96` to `0.99` F1, with only `Supply Department` dropping to `0.91`, which is still acceptable.

3. It is the best match for the nature of the task.

Department classification is not only keyword lookup. Many incidents contain overlapping hospital vocabulary such as equipment requests, cleaning issues, staffing requests, transport needs, stock problems, billing issues, and system faults. The correct department often depends on how those terms are used together in context.

DistilBERT is well suited to this because:
- it captures word context rather than treating text as an unordered token count
- it can separate similar phrases that should route to different departments
- it can use role names, operational phrasing, and sentence context together

That matters in this task because departments like `Facility Management`, `Housekeeping Department`, `Supply Department`, `Biomedical Engineering`, and `Transport` can share similar surface words, but the routing decision depends on the full meaning of the incident description.

4. It generalizes better than the LSTM.

The LSTM shows classic overfitting. DistilBERT improves validation metrics steadily across epochs and ends with:
- `validation accuracy = 0.9389`
- `validation macro F1 = 0.9365`

It then reaches even stronger test metrics, which suggests stable generalization rather than memorization.

5. It improves on the already-strong SVM baseline.

SVM is close, but DistilBERT still wins on both overall accuracy and macro F1. That means the transformer is extracting additional signal beyond the strong TF-IDF baseline.

This is the important point: SVM and Naive Bayes already prove that simple text patterns are useful, but DistilBERT performs even better because it can use contextual semantics on top of those patterns. That is exactly why it is the best model for department routing.

## Practical Recommendation

If the only goal is the **best predictive performance**, use **DistilBERT**.

It should be the primary recommendation not only because it has the best numbers, but because department classification is fundamentally a contextual language-understanding problem. The best model for that type of task is the one that understands context most effectively, and the recorded results show that DistilBERT does exactly that.

If the goal is a **lighter and simpler production model** with very strong accuracy and much lower training/inference complexity, **SVM is the best fallback choice**. Its performance is close enough to DistilBERT that it may be preferable in constrained environments.

Recommended ranking:
1. `DistilBERT` for best overall quality
2. `SVM` for best lightweight model
3. `Naive Bayes` as a simpler but weaker classical baseline
4. `LSTM` is not recommended given the large performance gap and overfitting behavior
