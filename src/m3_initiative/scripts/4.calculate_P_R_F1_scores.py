# This code is to calculate P, R, F1 scores based on matching the entity type between reference and candidate.
# support in the output is the number of reference per entity type.

import pandas as pd
from sklearn.metrics import classification_report
def class_report(y_true, y_pred, path, name):

  file = open(path+"prediction_results_without_fine-tuning_"+name+".txt", 'w')
  labels = ['reason', 'ade', 'form', 'strength', 'dosage', 'drug', 'route', 'frequency', 'duration']
  print(type(labels), labels)
  report = classification_report(y_true, y_pred, labels = labels)
  print(report)
  file.writelines(report)

  labels.remove('reason') # remove 'reason' label from evaluation
  labels.remove('ade') # remove 'reason' label from evaluation
  print(type(labels), labels)
  report = classification_report(y_true, y_pred, labels = labels)
  print(report)
  file.writelines(report)
  file.close()


  #return report


path = "/content/drive/MyDrive/collabrations_/HumanLoopH/Med7/data/"
model = ["en_core_med7_lg", "en_core_med7_trf"]
for name in model:
  print("caluculating P, R, F1 scores of "+name+" predictions over the testing set")
  eval_report_all = pd.read_excel(path+'true_predict_label_entity_76testDataset_'+name+'.xlsx') #predict_label_entity_76testDataset_en_core_med7_trf or predict_label_entity_76testDataset_en_core_med7_lg
  print("76 Test dataset "+name)
  eval_report_copy_all = eval_report_all.copy()
  y_true = eval_report_copy_all['true_label'].tolist()
  y_pred = eval_report_copy_all['predict_label'].tolist()
  print('type matching')
  #all = class_report(y_true, y_pred)
  class_report(y_true, y_pred, path, name)
