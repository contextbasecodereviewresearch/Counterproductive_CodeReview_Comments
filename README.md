# Counterproductive Behavior Detection in Code Review Comments  
### Replication Package & Online Supplement

This repository provides the full replication materials for the study:

> **Do Not Review My Code Harshly: Identifying Counterproductive Behavior in Code Review Comments**  

---

## 📌 Overview

Modern code review depends heavily on written communication. While prior research has focused mainly on **toxicity**, many harmful review behaviors are **non-toxic but still discouraging, obstructive, or socially destructive**.

To address this gap, this work introduces the concept of:

### **Counterproductive Behavior**

A broader taxonomy extending toxicity by capturing subtle but harmful interaction patterns in code review comments.

This replication package contains:

- A human-labeled dataset of **310 real code review comments**
- A taxonomy of **9 primitive counterproductive traits**
- Statistical validation of toxicity incompleteness
- Trait relationship analysis (ANOVA + Tukey HSD)
- Preprocessing and embedding pipelines (Word2Vec)
- Trait-based ensemble ML models for detection
- Full scripts, outputs, and supplementary evidence

All materials needed to reproduce the paper are included here  

---

## 📂 Repository Structure (Full Workflow)

The project is organized into six folders following the paper pipeline:


1. hypothesisTesting/ → Toxicity comprehensiveness validation (Z-test)

2. ANOVAandHSD/ → Trait relationship analysis + Tukey similarity graph

3. Preprocessing/ → Full NLP cleaning pipeline + evidence tables

4. WordVectorization/ → Word2Vec embedding training and feature extraction

5. Models/ → Trait-specific ensemble detection models (5 improved traits)

6. DataSample/ → Annotated dataset sample + label distributions


---

## 🧾 Dataset Summary

### Source and Sampling

- Comments were sampled from the SE-specific **ToxiCR dataset**  
  (19,651 Gerrit review comments).
- Duplicate entries were removed.
- Sampling was intentionally **toxicity-oversampled (3:1)** to ensure sufficient unhealthy behavior coverage.

Final dataset:

- **N = 310 labeled comments**
- **180 counterproductive**
- **130 productive**


---

## 📊 Descriptive Statistics of Primitive Counterproductive Traits

Dataset size: **N = 310** code review comments  
(180 counterproductive-labeled, 130 productive)

| Trait | Frequency | Proportion (Mean) | SD |
|------|----------:|------------------:|---:|
| Lack of specification | 100 | 0.323 | 0.467 |
| Discouragement without guidance | 62 | 0.200 | 0.400 |
| Mockery | 42 | 0.135 | 0.342 |
| Dismissive attitude | 31 | 0.100 | 0.300 |
| Personal attacks | 28 | 0.090 | 0.287 |
| Excessive control | 17 | 0.055 | 0.228 |
| Unconscious bias | 16 | 0.052 | 0.223 |
| Disregard for others’ time or boundaries | 14 | 0.045 | 0.208 |
| Threats or intimidation | 4 | 0.013 | 0.112 |



### 📐 Trait Proportion (Mean Occurrence Rate) and SD

```math
p_t = \text{Proportion}(t) = \frac{\text{Frequency}(t)}{N}
```

```math
SD(t) = \sqrt{p_t(1-p_t)}
```
---

### Inter-Rater Reliability (IRR) on Raw Crowd Annotations

To evaluate initial crowd consistency (before majority vote and author adjudication), we computed **Krippendorff's alpha (nominal)** on the raw annotations from the first 2–3 annotators per comment, separately for each antisocial trait.

**Results** (raw IRR before resolution):

| Trait                                      | Krippendorff's alpha | Interpretation      |
|--------------------------------------------|----------------------|---------------------|
| Lack of specificity                        | 0.72                 | Moderate            |
| Discouragement without guidance            | 0.57                 | Moderate            |
| Mockery                                    | 0.62                 | Substantial         |
| Dismissive attitude                        | 0.40                 | Moderate            |
| Personal attacks                           | 0.55                 | Substantial         |
| Excessive control                          | 0.28                 | Fair–moderate       |
| Unconscious bias                           | 0.63                 | Moderate            |
| Disregard for other time or boundaries     | 0.4504                 | Fair                |
| Threats or intimidation                    | 1.00                 | Substantial         |
| **Average across 9 traits**                | **0.58**             | **Moderate**        |

**Interpretation**:
- 0.41–0.60: Moderate agreement
- 0.61–0.80: Substantial agreement

The average raw agreement of 0.55 is typical for subjective multi-label tasks like antisocial/toxicity labeling in text. Final labels were resolved via majority vote (among 2–3 annotators) and author adjudication for persistent ambiguities, resulting in higher-confidence data used for training and analysis.

**Note**: Reported Krippendorff’s α values are based on raw, unresolved crowd annotations. Because all disagreements were resolved via justification-based majority voting and author adjudication, these scores do not reflect the reliability of the final dataset.

full code: `6_datasetSample/`


---

## 📉 Toxicity is NOT Comprehensive

A central contribution is showing that toxicity fails to cover all harmful review behavior.

### Hypothesis Test (Z-test for Proportions)

- Counterproductive subset: **n = 180**
- Toxic overlap: **k = 131**
- Observed coverage: **p̂ = 72.8%**

Tested benchmark:

- **H₀: p ≥ 0.80**
- **H₁: p < 0.80**

Result:

- z = −2.42  
- p-value < 0.05  
- **Reject toxicity comprehensiveness**


A sensitivity analysis confirms robustness across thresholds (50–90%).

full code: ```1_hypothesisTesting```

---

## 🔗 Trait Relationship Analysis (ANOVA + Tukey HSD)

To refine the taxonomy, trait co-occurrence was analyzed:

- One-way ANOVA: **F(8,2781)=31.39, p ≪ 0.001**
- Tukey HSD produced a similarity graph

Five traits formed a complete subgraph and were consolidated into:

### **Counterproductive Interaction Pattern (CIP)**

CIP includes:

- Personal attacks  
- Excessive control  
- Dismissive attitude  
- Unconscious bias  
- Disregard for boundaries  

full code: ```2_ANOVAandHSDTesting/```

---

## 🤖 Detection Models (Improved Trait Set)

The final detection framework models **5 improved counterproductive traits**:

1. Lack of specification  
2. Discouragement without guidance  
3. Mockery  
4. Threats or intimidation  
5. CIP (Social Destructive Pattern)

Each trait has its own classifier, combined via an ensemble OR-rule to maximize recall.

Mean recall achieved:

- **94% ± 13%** (recall-focused design)


All trained models are available in: ```5-Models/```


---

## ⚙️ Preprocessing Pipeline Evidence

The preprocessing workflow includes:

- Lowercasing
- URL removal
- Stopword filtering
- Identifier decomposition
- Keyword elimination
- Adversarial correction

### Dataset Statistics Before vs After

| Statistic | Before | After | Change (%) |
|---------|--------|-------|------------|
| Number of comments | 310 | 310 | 0.0 |
| Vocabulary size | 1734 | 1551 | -10.55 |
| Avg. tokens per comment | 25.5 | 15.2 | -0.59 |
| Median tokens per comment | 16 | 8 | -50.0 |





| No. | Data Preprocessing                                  | Number of Changed Comments |
|----:|----------------------------------------------------|----------------------------|
| 1   | Lowercasing                                         | 246                        |
| 2   | URL Removal                                         | 7                          |
| 3   | Contraction Expansion                               | 97                         |
| 4.1 | Stopwords                                           | 292                        |
| 4.2 | Symbol Elimination                                  | 285                        |
| 5   | Word Correction                                     | 241                        |
| 6   | Adversarial Pattern Detection and Correction        | 78                         |
| 7   | Identifiers Decomposition                           | 257                        |
| 8   | Removal of Programming Keywords                     | 207                        |


Full code: `3-Preprocessing/`

---

## 🚀 Reproducing the Results

### Requirements

- Python ≥ 3.8
- scikit-learn
- numpy, pandas
- gensim (Word2Vec)
- statsmodels

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Full Pipeline:

```
## 1. Preprocess dataset
python 3-Preprocessing/run_preprocessing.py

## 2. Statistical validation
python 1-hypothesisTesting/ztest_toxicity.py

## 3. Trait relationship analysis
python 2-ANOVAandHSD/anova_hsd.py

## 4. Train embeddings
python 4-WordVectorization/train_word2vec.py

## 5. Train detection models
python 5-Models/train_models.py

```
