<img src="https://github.com/HECTA-UoM/M3/blob/main/M3_logo.png" width=200>

# M3: Manchester Medical Mining

Place holder for M3 packages to be shared including codes, tools, and some learning data, and sample testing data.

# Presentations and Reports
Arooj Hussain, Haifa Alrdahi, Hendrik Šuvalov, Lifeng Han, Meghna Jani, Will Dixon, Goran Nenadic.
''M3: Extracting medication and related attributes from outpatient letters''. Conference: HealTAC 2023: HEALTHCARE TEXT ANALYTICS CONFERENCE 2023 MANCHESTER, JUNE 14-16, 2023.
Poster link: 
[M3-Poster](https://www.researchgate.net/publication/371696214_M3_Extracting_medication_and_related_attributes_from_outpatient_letters)
| [Presentation-photo](https://drive.google.com/file/d/1BE74mrRNCeT77IVMRveJHcv3QpZSfMVM/view?usp=sharing) | [Presentation-film](https://drive.google.com/file/d/1eWsemaMpbARxbmEAh7rpPltN9oNeTTzt/view?usp=sharing)
 
# Models included: xlm-Roberta-base, Med7, DrugNER

Fine-tuned on these models. Outcomes:

1) Clinical-xlm-Roberta: to medication extraction task

2) Extended-Med7 (Med7+): to 9 labels

Direct deployment: DrugNER

# Evaluation Metrics

[Eval metrics](https://www.davidsbatista.net/blog/2018/05/09/Named_Entity_Evaluation/#:~:text=When%20you%20train%20a%20NER,a%20full%20named%2Dentity%20level.):

Strict: exact boundary surface string match and entity type;
Exact: exact boundary match over the surface string, regardless of the type;
Partial: partial boundary match over the surface string, regardless of the type;
Type: some overlap between the system tagged entity and the gold annotation is required;

# Model instructions and running logs

[Med7+ Instruction using Colab step-by-step documentation](https://drive.google.com/drive/folders/1qrVerDLTlmQevA7qlpiVpGRW_L4zvtpA?usp=sharing)
[Med7+ Colab file download](https://github.com/HECTA-UoM/M3/blob/main/Med7Plus_fine-tuning.ipynb)
[Clinical-XLM-R Instruction using Colab: *coming soon*]()

# Evaluation Scores



Deirect deployment of Med7 15% testing set. 

<img src="https://github.com/HECTA-UoM/M3/blob/main/Med7_deploy.png" width=700>


Med7+
Fine-tuned Med7+ performances on n2c2-2018 shared task data using our own data splition (70/15/15%) for overall 505 original annotated letters:

<img src="https://github.com/HECTA-UoM/M3/blob/main/Med7_plusV2.png" width=700>


- generating 9 labels, vs 7 from original Med7
- micro: precision 91%, recall 88%, f1 89%. weighted: precision 90%, recall 88%, f1 89%.

  

Clinical-xlm-Roberta:

'overall_precision': 0.8798480837840948,
 'overall_recall': 0.9014267185473411,
 'overall_f1': 0.8905066977285965,
 'overall_accuracy': 0.9676871902790035}

<img src="https://github.com/HECTA-UoM/M3/blob/main/clinical-xlm-r.png" width=700>



# Acknowledgement 
[Med7](https://github.com/kormilitzin/med7)
[xlm-Roberta-base](https://huggingface.co/xlm-roberta-base)

# References

@misc{alrdahi2023medmine,
      title={MedMine: Examining Pre-trained Language Models on Medication Mining}, 
      author={Haifa Alrdahi and Lifeng Han and Hendrik Šuvalov and Goran Nenadic},
      year={2023},
      eprint={2308.03629},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
