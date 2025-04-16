# this code is to save the results of prediction in suitable format to calculate the confusion matrix of TP, FN, FP, TN
# using type match (at least part of the token text is annotated with the correct entity type)
# and using strict match (the token text and the entity type has to be matched the gold data)
# COR: correct annotation of type
# INC: incorrect annotation of type
# MIS: missing annotation by Med7
# SPU: Spurius is for a token predicted by Med7 with an entity label but it's not in the gold data

# see this website explains NER evaluation:
# https://www.davidsbatista.net/blog/2018/05/09/Named_Entity_Evaluation/


import pandas as pd

def processing(true_label_entity, predict_label_entity, name, path):

  Eval = []

  predict_label_entity_len = len(predict_label_entity)
  type_list = []
  strict_list = []
  for i, row in true_label_entity.iterrows():
    if i%500 == 0:

      print("batch: ", i)
    tmp = 0
    for c, srow in predict_label_entity.iterrows():
      #print(c)
      if srow[0] > row[0]:
        #print('LARGER', row[0], srow[0])
        break
      #if c%5000 == 0:
        #print("batch c", c)
      Eval_dic = {}
      if row[0] == srow[0]:
        #print('EQUALS', row[0], srow[0])
        if row[5] == srow[5] and row[6] == srow[6] and str(row[4]) == str(srow[4]):
        #if str(row[4]).lower() == str(srow[4]).lower():
          if str(row[1]).lower() == str(srow[1]).lower():
            Eval_dic['file_id'] = str(row[0])
            Eval_dic['true_label'] = str(row[1]).lower()
            Eval_dic['true_start'] = row[5]
            Eval_dic['true_end'] = row[6]
            Eval_dic['true_text'] = str(row[4])
            Eval_dic['predict_file_id'] = str(srow[0])
            Eval_dic['predict_label'] = str(srow[1]).lower()
            Eval_dic['predict_start'] = srow[5]
            Eval_dic['predict_end'] = srow[6]
            Eval_dic['predict_text'] = str(srow[4])
            Eval_dic['strict_label'] = 'COR'
            Eval_dic['type_label'] = 'COR'
            #print('str(row[4]).lower() == str(srow[4]).lower()', Eval_dic)
            Eval.append(Eval_dic)

            strict_list.append('COR')
            type_list.append('COR')
            #print("strict_list.append(COR), type_list.append(COR)")
            #true_label_entity = true_label_entity.drop([i])
            #predict_label_entity = predict_label_entity.drop([c])
            #predict_label_entity_len -= 1
            #tmp = 1
            #break
          elif str(row[1]).lower() != str(srow[1]).lower():
            Eval_dic['file_id'] = str(row[0])
            Eval_dic['true_label'] = str(row[1]).lower()
            Eval_dic['true_start'] = row[5]
            Eval_dic['true_end'] = row[6]
            Eval_dic['true_text'] = str(row[4])
            Eval_dic['predict_file_id'] = str(srow[0])
            Eval_dic['predict_label'] = str(srow[1]).lower()
            Eval_dic['predict_start'] = srow[5]
            Eval_dic['predict_end'] = srow[6]
            Eval_dic['predict_text'] = str(srow[4])
            Eval_dic['strict_label'] = 'INC'
            Eval_dic['type_label'] = 'INC'
            #print('str(row[4]).lower() == str(srow[4]).lower()', Eval_dic)
            Eval.append(Eval_dic)

            strict_list.append('INC')
            type_list.append('INC')
            #print("strict_list.append(INC), type_list.append(INC)")
          true_label_entity = true_label_entity.drop([i])
          predict_label_entity = predict_label_entity.drop([c])
          predict_label_entity_len -= 1
          tmp = 1
          break

        elif row[5] == srow[5] and str(row[4]) in str(srow[4]):
          if str(row[1]).lower() == str(srow[1]).lower():
            Eval_dic['file_id'] = str(row[0])
            Eval_dic['true_label'] = str(row[1]).lower()
            Eval_dic['true_start'] = row[5]
            Eval_dic['true_end'] = row[6]
            Eval_dic['true_text'] = str(row[4])
            Eval_dic['predict_file_id'] = str(srow[0])
            Eval_dic['predict_label'] = str(srow[1]).lower()
            Eval_dic['predict_start'] = srow[5]
            Eval_dic['predict_end'] = srow[6]
            Eval_dic['predict_text'] = str(srow[4])
            Eval_dic['strict_label'] = 'INC'
            Eval_dic['type_label'] = 'COR'
            #print('row[2] <= srow[2]', Eval_dic)
            Eval.append(Eval_dic)

            type_list.append('COR')
            strict_list.append('INC')
            #print("strict_list.append(INC), type_list.append(COR)")

          elif str(row[1]).lower() != str(srow[1]).lower():
            Eval_dic['file_id'] = str(row[0])
            Eval_dic['true_label'] = str(row[1]).lower()
            Eval_dic['true_start'] = row[5]
            Eval_dic['true_end'] = row[6]
            Eval_dic['true_text'] = str(row[4])
            Eval_dic['predict_file_id'] = str(srow[0])
            Eval_dic['predict_label'] = str(srow[1]).lower()
            Eval_dic['predict_start'] = srow[5]
            Eval_dic['predict_end'] = srow[6]
            Eval_dic['predict_text'] = str(srow[4])
            Eval_dic['strict_label'] = 'INC'
            Eval_dic['type_label'] = 'INC'
            #print('row[2] <= srow[2]', Eval_dic)
            Eval.append(Eval_dic)

            type_list.append('INC')
            strict_list.append('INC')
            #print("strict_list.append(INC), type_list.append(INC)")
          #predict_label_entity = predict_label_entity.drop([c])
          #predict_label_entity_len -= 1
          #if row[3] < srow[3]:
          true_label_entity = true_label_entity.drop([i])
          tmp = 1


        elif row[6] == srow[6] and str(row[4]) in str(srow[4]):
          if str(row[1]).lower() == str(srow[1]).lower():
            Eval_dic['file_id'] = str(row[0])
            Eval_dic['true_label'] = str(row[1]).lower()
            Eval_dic['true_start'] = row[5]
            Eval_dic['true_end'] = row[6]
            Eval_dic['true_text'] = str(row[4])
            Eval_dic['predict_file_id'] = str(srow[0])
            Eval_dic['predict_label'] = str(srow[1]).lower()
            Eval_dic['predict_start'] = srow[5]
            Eval_dic['predict_end'] = srow[6]
            Eval_dic['predict_text'] = str(srow[4])
            Eval_dic['strict_label'] = 'INC'
            Eval_dic['type_label'] = 'COR'
            #print('row[3] <= srow[3]', Eval_dic)
            Eval.append(Eval_dic)

            type_list.append('COR')
            strict_list.append('INC')
            #print("strict_list.append(INC), type_list.append(COR)")
              #true_label_entity = true_label_entity.drop([i])

              #break
          elif str(row[1]).lower() != str(srow[1]).lower():
              #print("equals", i, c)
            Eval_dic['file_id'] = str(row[0])
            Eval_dic['true_label'] = str(row[1]).lower()
            Eval_dic['true_start'] = row[5]
            Eval_dic['true_end'] = row[6]
            Eval_dic['true_text'] = str(row[4])
            Eval_dic['predict_file_id'] = str(srow[0])
            Eval_dic['predict_label'] = str(srow[1]).lower()
            Eval_dic['predict_start'] = srow[5]
            Eval_dic['predict_end'] = srow[6]
            Eval_dic['predict_text'] = str(srow[4])
            Eval_dic['strict_label'] = 'INC'
            Eval_dic['type_label'] = 'INC'
            #print('row[3] <= srow[3]', Eval_dic)
            Eval.append(Eval_dic)

            type_list.append('INC')
            strict_list.append('INC')
            #print("strict_list.append(INC), type_list.append(INC)")
              #true_label_entity = true_label_entity.drop([i])
          predict_label_entity = predict_label_entity.drop([c])
          predict_label_entity_len -= 1
          true_label_entity = true_label_entity.drop([i])
              #break
          tmp = 1



    if tmp == 0:
      if i in true_label_entity.index:
        Eval_dic = {}

        Eval_dic['file_id'] = str(row[0])
        Eval_dic['true_label'] = str(row[1]).lower()
        Eval_dic['true_start'] = row[5]
        Eval_dic['true_end'] = row[6]
        Eval_dic['true_text'] = str(row[4])
        Eval_dic['predict_file_id'] = str(srow[0])
        Eval_dic['predict_label'] = "O"
        Eval_dic['predict_start'] = row[5]
        Eval_dic['predict_end'] = row[6]
        Eval_dic['predict_text'] = str(row[4])
        Eval_dic['strict_label'] = 'MIS'
        Eval_dic['type_label'] = 'MIS'
        Eval.append(Eval_dic)

        #print(row)
        strict_list.append('MIS')
        type_list.append('MIS')
        #print("strict_list.append(MIS), type_list.append(MIS)")
        true_label_entity = true_label_entity.drop([i])

    #print(len(predict_label_entity), predict_label_entity_len)
  for c, srow in predict_label_entity.iterrows():
    #if len(predict_label_entity) > predict_label_entity_len:
    Eval_dic = {}
    Eval_dic['file_id'] = str(srow[0])
    Eval_dic['true_label'] = 'O'
    Eval_dic['true_start'] = srow[5]
    Eval_dic['true_end'] = srow[6]
    Eval_dic['true_text'] = str(srow[4])
    Eval_dic['predict_file_id'] = str(srow[0])
    Eval_dic['predict_label'] = str(srow[1]).lower()
    Eval_dic['predict_start'] = srow[5]
    Eval_dic['predict_end'] = srow[6]
    Eval_dic['predict_text'] = str(srow[4])
    Eval_dic['strict_label'] = 'SPU'
    Eval_dic['type_label'] = 'SPU'
    Eval.append(Eval_dic)
    #print(srow)
    strict_list.append('SPU')
    type_list.append('SPU')
    #print("strict_list.append(SPU), type_list.append(SPU)")
    predict_label_entity = predict_label_entity.drop([c])
    predict_label_entity_len -= 1

  true_predict_eval = pd.DataFrame.from_records(Eval)
  print(len(true_predict_eval))
  # uncomment this line to save the file, DO NOT FORGET TO CHANGE PATH AND FILE NAME
  true_predict_eval.to_excel(path+'true_predict_label_entity_76testDataset_'+name+'.xlsx', index=False)  #true_predict_label_entity_76testDataset_en_core_med7_trf or true_predict_label_entity_76testDataset_en_core_med7_lg


path = "/content/drive/MyDrive/collabrations_/HumanLoopH/Med7/data/"

true_label_entity = pd.read_excel(path+'gold_data_entity_CHoffsetEntitiesOnly_test_76.xlsx')
print(true_label_entity)

model = ["en_core_med7_lg", "en_core_med7_trf"]
for name in model:
  print("processing the output of "+name+" predictions over the testing set")
  predict_label_entity = pd.read_excel(path + 'predict_label_entity_76testDataset_'+name+'.xlsx') #predict_label_entity_76testDataset_en_core_med7_trf or predict_label_entity_76testDataset_en_core_med7_lg
  print(predict_label_entity)
  processing(true_label_entity, predict_label_entity, name, path)

