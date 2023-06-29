<img src="https://github.com/HECTA-UoM/M3/blob/main/M3_logo.png" width=200>

# M3: Manchester Medical Mining

Place holder for M3 packages to be shared including codes, tools, and some learning data, and sample testing data.

# Presentations and Reports

''M3: Extracting medication and related attributes from outpatient letters''. Conference: HealTAC 2023: HEALTHCARE TEXT ANALYTICS CONFERENCE 2023 MANCHESTER, JUNE 14-16, 2023.
Poster link: 
[M3-Poster](https://www.researchgate.net/publication/371696214_M3_Extracting_medication_and_related_attributes_from_outpatient_letters)
| [Presentation-photo](https://drive.google.com/file/d/1BE74mrRNCeT77IVMRveJHcv3QpZSfMVM/view?usp=sharing) | [Presentation-film](https://drive.google.com/file/d/1eWsemaMpbARxbmEAh7rpPltN9oNeTTzt/view?usp=sharing)
 
# Models included: fine-tuned xlm-Roberta and Med7
Clinical-xlm-Roberta: to medication extraction task

Extended-Med7 (Med7+): to 9 labels

# Evaluation Metrics

# Evaluation Scores

Med7+

This is based on Lineint string overlap Matching based on SEMEVAL. (Type) on train+valid (303 letters)
                precision    recall  f1-score   support
      dosage       0.94      0.93      0.93      4221
        drug       0.93      0.89      0.91     16225
    duration       0.82      0.85      0.83       592
        form       0.94      0.92      0.93      6651
   frequency       0.88      0.82      0.85      6281
       route       0.96      0.96      0.96      5476
    strength       0.93      0.94      0.94      6691
    accuracy                           0.85     49003
   macro avg       0.80      0.79      0.79     49003
weighted avg       0.87      0.85      0.86     49003

This is based on Strict string overlap Matching. Labelled ‘O’ if string not matching (Strict) on train+valid (303 letters)
             precision    recall  f1-score   support
      dosage       0.94      0.91      0.92      4221
        drug       0.93      0.88      0.90     16225
    duration       0.81      0.82      0.82       592
        form       0.94      0.91      0.92      6651
   frequency       0.88      0.77      0.82      6281
       route       0.96      0.96      0.96      5476
    strength       0.93      0.94      0.93      6691
    accuracy                           0.83     49003
   macro avg       0.80      0.77      0.78     49003
weighted avg       0.87      0.83      0.85     49003

