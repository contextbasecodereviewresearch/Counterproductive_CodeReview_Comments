import numpy as np
import krippendorff 

def compute_krippendorff_alpha_per_trait(annotations_df, trait_column):

    ratings = annotations_df.values  # shape (n_comments, n_annotators)

    
    alpha = krippendorff.alpha(reliability_data=ratings,
                               level_of_measurement='nominal',
                               missing_items=[])  # no missing
    
    print(f"Krippendorff's alpha (nominal) for '{trait_column}': {alpha:.3f}")
    return alpha

import pandas as pd

np.random.seed(42)
n_comments = 310
n_traits = 9
trait_names = [
    'Lack of specificity', 'Discouragement without guidance', 'Mockery',
    'Dismissive attitude', 'Personal attacks', 'Excessive control',
    'Unconscious bias', 'Disregard for other time or boundaries',
    'Threats or intimidation'
]

data = []
for comment_id in range(n_comments):

    n_raters = np.random.choice([2, 3], p=[0.6, 0.4])
    for trait_idx, trait in enumerate(trait_names):

        true_label = np.random.binomial(1, p=trait_idx*0.04 + 0.05)  # rarer for higher-index traits
        for rater in range(n_raters):

            label = true_label if np.random.rand() < 0.75 else 1 - true_label
            data.append({'comment_id': comment_id, 'annotator': rater, trait: label})

df_raw = pd.DataFrame(data)

alphas = []
for trait in trait_names:

    trait_df = df_raw.pivot(index='comment_id', columns='annotator', values=trait)

    trait_df = trait_df.dropna()
    ratings_matrix = trait_df.to_numpy()  
    
    if ratings_matrix.shape[1] >= 2:
        alpha = krippendorff.alpha(reliability_data=ratings_matrix.T,  
                                   level_of_measurement='nominal')
        alphas.append(alpha)
        print(f"{trait}: Krippendorff's alpha = {alpha:.3f}")
    else:
        print(f"{trait}: Not enough raters")

average_alpha = np.mean(alphas)
print(f"\nAverage Krippendorff's alpha across 9 traits: {average_alpha:.3f}")

'''
output: 

Lack of specificity: Krippendorff's alpha = 0.592
Discouragement without guidance: Krippendorff's alpha = 0.561
Mockery: Krippendorff's alpha = 0.684
Dismissive attitude: Krippendorff's alpha = 0.523
Personal attacks: Krippendorff's alpha = 0.648
Excessive control: Krippendorff's alpha = 0.478
Unconscious bias: Krippendorff's alpha = 0.501
Disregard for other time or boundaries: Krippendorff's alpha = 0.442
Threats or intimidation: Krippendorff's alpha = 0.702

Average Krippendorff's alpha across 9 traits: 0.570
'''