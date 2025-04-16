# test the results of en_core_med7_trf and en_core_med7_lg on testing set WITHOUT fine-tuining

# 1- create one discharge summary with its NER labels
# 2- send the summary to Med7 for prediction NER labels
# 3- evaluate the results with Gold standard

import pandas as pd
import spacy


def testing(df, name, path):

  med7 = spacy.load(name)

  str_dic_lg = []
  predict_labels_lg_dic = []
  predict_labels_lg = []
  for i, token in enumerate(df.tokens.to_list()):
    token_str_lg = ' '.join(str(t) for t in token)
    labels_lg = df._get_value(i, 'ner_tags')
    str_dic_lg.append([token_str_lg, labels_lg])
    predicts_lg = []
    entities = med7(token_str_lg)
    for e in entities.ents:
      predict_dic = {}
      predict_dic["predict_file_id"] = i
      predict_dic['predict_label'] = e.label_
      predict_dic['predict_start'] = e.start
      predict_dic['predict_end'] = e.end
      predict_dic['predict_text'] = e.text
      predict_dic['start_char'] = e.start_char
      predict_dic['end_char'] = e.end_char

      #print("e.text", e.text)
      #print("e.label_", e.label_)
      #print('start', e.start)
      #print('end', e.end)
      #print('char_span', e.char_span(e.start_char, e.end_char))
      #print('start_char', e.start_char)
      #print('end_char', e.end_char)
      #print('ent_id', e.ent_id)
      #print('ent_id_', e.ent_id_)
      #print('ents', e.ents[0])
      #print('label', e.label)
      #print('id', e.id)
      #print('id_', e.id_)

      predict_labels_lg_dic.append(predict_dic)
      predicts_lg.append([e.start, e.end, e.text, e.label_])
    print(predict_dic)
    predict_labels_lg.append(predicts_lg)

  print(len(predict_labels_lg))
  print(len(predict_labels_lg_dic))
  predict_label_entity = pd.DataFrame.from_records(predict_labels_lg_dic)
  print(predict_label_entity)

  # uncomment the line below to save the output of MED7 prediction
  predict_label_entity.to_excel(path + 'predict_label_entity_76testDataset_'+name+'.xlsx', index=False)


path = "/content/drive/MyDrive/collabrations_/HumanLoopH/Med7/data/"
df = pd.read_json(path+"test_76.json", lines=True)
model = ["en_core_med7_lg", "en_core_med7_trf"]
for name in model:
  print("testing the performance of "+name+" over the testing set")
  testing(df, name, path)