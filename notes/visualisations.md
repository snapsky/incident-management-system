# Data Visualization Report

## Summary

The notebook [data_visualization.ipynb](/home/lakshan/ssp/IMS/preprocess/data_visualization.ipynb) performs four main exploratory visualizations on the processed incident dataset:

1. incident distribution by urgency
2. incident text length distribution
3. incident volume heatmap by day and hour
4. n-gram frequency analysis on incident descriptions

These visualizations are important because they reveal the structure of the dataset before modeling. They help explain later model behavior, especially:
- why urgency classification is difficult
- why department classification performs better
- why binary screening is more practical than 4-class urgency prediction
- what kinds of language patterns dominate the incident text

## Visualizations Performed

### 1. Incident distribution by criticality

The notebook builds a count plot for the `urgency` field using the ordered classes:
- `Low`
- `Medium`
- `High`
- `Critical`

Recorded counts:
- `Low = 72`
- `Medium = 1164`
- `High = 1800`
- `Critical = 564`

### 2. Incident text length distribution

The notebook creates two histograms:
- character-length distribution of `incident_description`
- word-count distribution of `incident_description`

Recorded summary statistics:
- mean character length: `132.68`
- median character length: `131`
- min character length: `56`
- max character length: `245`

- mean word count: `19.70`
- median word count: `19`
- min word count: `7`
- max word count: `36`

### 3. Incident time heatmap

The notebook combines `date` and `time` into a timestamp, extracts:
- `hour_of_day`
- `day_of_week`

Then it creates a heatmap of incident counts across:
- 7 weekdays
- 24 hours of the day

### 4. N-gram analysis

The notebook computes:
- top unigrams
- top bigrams
- top trigrams

from `incident_description`.

The visible top bigrams include:
- `due to` = `170`
- `reception to` = `155`
- `heavy rain` = `114`
- `request immediate` = `96`
- `security to` = `91`
- `request qa` = `82`
- `need immediate` = `74`

## Insights Derived from the Visualizations

## 1. The urgency dataset is strongly imbalanced

This is the most important insight from the criticality plot.

The distribution is heavily skewed toward `High` and `Medium`, while `Low` is extremely rare:
- `High` has `1800` examples
- `Medium` has `1164`
- `Critical` has `564`
- `Low` has only `72`

### What this means

- The dataset is not balanced enough for stable 4-class urgency learning.
- Any model trained directly on these four classes will see very few `Low` examples.
- The model will naturally learn the dominant classes much better than the rare class.

### Why this matters

This visualization directly explains why the urgency notebooks show poor `Low`-class recall and unstable macro F1. The problem is not only the model choice. The label distribution itself is a major constraint.

It also supports the decision to use binary screening:
- merge `Low + Medium` into `routine-review`
- merge `High + Critical` into `immediate-attention`

That creates a much healthier learning problem.

## 2. Incident descriptions are fairly standardized in length

The text-length histograms show that incident descriptions are neither extremely short nor extremely long. Most incidents are written in a relatively narrow band:
- about `131` characters on median
- about `19` words on median

### What this means

- Most records contain enough information for classification.
- The dataset is operationally structured rather than noisy free-form narrative.
- The texts are long enough to contain actionable clues, but short enough that concise patterns matter.

### Why this matters

This is a good sign for text classification:
- TF-IDF models can extract meaningful tokens and phrases
- transformer models do not face extreme sequence length problems
- sequence models are not forced to handle very long reports

It also suggests that the classification task depends more on the content of the wording than on handling long-document complexity.

## 3. Incident volume follows a clear working-day and working-hour pattern

The time heatmap shows incidents are concentrated mainly in daytime and operational hours, especially:
- roughly from morning through late afternoon
- with strong activity around `08:00` to `16:00`

Late-night hours are much quieter across most days.

There are also visible day-level differences, but the stronger pattern is the hour-of-day concentration.

### What this means

- Incident generation is tied to hospital operational activity rather than being uniformly distributed through the day.
- Day-shift workflows likely create most of the reporting load.
- The system sees much more structured human reporting during active hours.

### Why this matters

This has several implications:

- Operational planning:
  staffing, triage attention, and ticket-routing support should be strongest during daytime peaks.

- Modeling:
  if future feature engineering uses `time` or `day`, these variables may improve routing or urgency prediction.

- Evaluation:
  current models do not yet use these temporal features, so the heatmap suggests there is still unused predictive information in the dataset.

## 4. The dataset contains repeated operational language patterns

The n-gram plots show that many phrases recur across incidents. Examples such as:
- `due to`
- `heavy rain`
- `request immediate`
- `need immediate`
- `security to`
- `request qa`

show that the dataset is not random text. It is operational text with repeated reporting patterns.

### What this means

- Incidents are written using semi-structured institutional language.
- There are frequent trigger phrases connected to operational urgency, routing, or environmental conditions.
- Many incidents likely share templates or habitual reporting styles.

### Why this matters

This helps explain why classical text models like SVM and Naive Bayes perform strongly on department classification:
- repeated token patterns are highly useful for department routing
- short operational phrases are often enough to identify the destination department

It also helps explain why binary urgency screening works:
- phrases like `request immediate` and `need immediate` are directly aligned with urgent escalation cues

At the same time, repeated n-grams alone are not enough for fine-grained 4-class urgency prediction, because the difference between `High` and `Critical` often depends on context, not only phrase frequency.

## 5. The dataset is suitable for text classification, but not all tasks are equally easy

Taken together, the plots show two things at the same time:

### The dataset is well suited for text modeling because:
- descriptions have useful length
- language is repetitive enough to learn from
- the reporting vocabulary is operational and informative

### But urgency classification remains difficult because:
- the label distribution is strongly imbalanced
- the rare `Low` class is underrepresented
- the semantic boundary between `High` and `Critical` is narrower than the department-routing boundary

This is an important combined insight. The problem is not “the text is bad.” The text is actually quite usable. The difficulty comes from the target structure, especially for urgency.

## Implications for the Project

## For urgency modeling

The visualizations support these conclusions:
- direct 4-class urgency classification is structurally hard
- class imbalance is a major reason
- binary screening is the more realistic first-stage solution

This matches the later modeling results, where binary screening performs much better than 4-class urgency classification.

## For department modeling

The visualizations suggest department classification should work well because:
- repeated departmental phrasing exists in the text
- description lengths are sufficient
- operational vocabulary is informative

This also matches the later training results, where department classifiers perform strongly.

## For future feature engineering

The heatmap indicates that the project may benefit from adding:
- hour-of-day features
- day-of-week features

The n-gram analysis suggests possible gains from:
- domain phrase normalization
- reporter-role normalization
- curated phrase dictionaries for urgency or routing cues

## Overall Conclusion

The visualization notebook provides useful evidence about both the data and the modeling problem.

The strongest insights are:
- the urgency labels are highly imbalanced
- incident text is structured and informative
- reporting activity is concentrated in operational hours
- repeated phrases provide strong routing and urgency cues

These visualizations are important because they explain later model results, not just describe the data. In particular:
- they explain why urgency 4-class models struggle
- they justify why binary screening works better
- they explain why department classification achieves strong performance

So the visualizations are not only descriptive. They are diagnostic: they reveal the main statistical and linguistic properties that shape the success or failure of the downstream models.
