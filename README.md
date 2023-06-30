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

[Eval metrics](https://www.davidsbatista.net/blog/2018/05/09/Named_Entity_Evaluation/#:~:text=When%20you%20train%20a%20NER,a%20full%20named%2Dentity%20level.):

Strict: exact boundary surface string match and entity type;
Exact: exact boundary match over the surface string, regardless of the type;
Partial: partial boundary match over the surface string, regardless of the type;
Type: some overlap between the system tagged entity and the gold annotation is required;

# Evaluation Scores

Med7+

<img src="https://github.com/HECTA-UoM/M3/blob/main/Med7_plus.png" width=700>

Clinical-xlm-Roberta:
'overall_precision': 0.8798480837840948,
 'overall_recall': 0.9014267185473411,
 'overall_f1': 0.8905066977285965,
 'overall_accuracy': 0.9676871902790035}

<img src="https://github.com/HECTA-UoM/M3/blob/main/clinical-xlm-roberta.png" width=700>

# Acknowledgement 
[Med7](https://github.com/kormilitzin/med7)
[xlm-Roberta-base](https://huggingface.co/xlm-roberta-base)


