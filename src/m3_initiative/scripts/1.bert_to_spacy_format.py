# DO NOT FORGET TO CHANGE THE PATHS AND THE FILES NAMES

# this code is to read bert data format (tokens, ner_tags, input_ids, attention_mask, labels)
# and change the data format to character offset for spacy ner model
# it generate  an excel file with all the tokens in the discharge summary that are labelled as entities only.
# you can edit the code to generate an excel file with all the tokens in the discharge summary, either an entity or not
# by uncommenting line No 34 "gold_data.append(gold_data_dic)"

import pandas as pd


def preprocess(df, name, path):
  gold_data_entities = []
  gold_data_tokens = []
  for i, tags in enumerate(df.ner_tags.to_list()):
    gold = []
    ch_start = 0
    for l, label in enumerate(tags):
      if label == "O":
        token = df._get_value(i, 'tokens')
        tmp_token = token[l]
        tmp_label = label
        tmp_start = l
        tmp_end = l+1

        gold_data_dic = {}
        ch_end = ch_start + len(tmp_token)
        gold_data_dic["file_id"] = i
        gold_data_dic['gold_label'] = tmp_label
        gold_data_dic['token_start'] = tmp_start
        gold_data_dic['token_end'] = tmp_end
        gold_data_dic['entity_text'] = tmp_token
        gold_data_dic['ch_start'] = ch_start
        gold_data_dic['ch_end'] = ch_end
        ch_start = ch_end+1
        #print(tmp_start, tmp_end, tmp_label, tmp_token)
        # uncomment the line below if you want to generate a file with all the tokens (entity or not)
        #gold_data_entities.append(gold_data_dic)
        gold_data_tokens.append(gold_data_dic)

      if label != "O":
        if "B-" in label:
          token = df._get_value(i, 'tokens')
          tmp_token = token[l]
          tmp_label = label[2:]
          tmp_start = l

          out = 0
          if l+1 < len(tags):
            tmp_end = l+1
            #print(l, l+1, tmp_label, tmp_token)
            for nl in range(l+1,len(tags)):
              #print(nl, token[nl])
              if "B-" in tags[nl]:
                out = 1
                break
              elif "O" == tags[nl]:
                out = 1
                break
              elif "I-" in tags[nl]:
                token = df._get_value(i, 'tokens')
                tmp_token += " " + token[nl]
                tmp_start = l
                tmp_end = nl+1
                #print(tmp_start, tmp_end, tmp_label, tmp_token)
            if out == 1:
              gold_data_dic = {}

              ch_end = ch_start + len(tmp_token)
              gold_data_dic["file_id"] = i
              gold_data_dic['gold_label'] = tmp_label
              gold_data_dic['token_start'] = tmp_start
              gold_data_dic['token_end'] = tmp_end
              gold_data_dic['entity_text'] = tmp_token
              gold_data_dic['ch_start'] = ch_start
              gold_data_dic['ch_end'] = ch_end
              ch_start = ch_end+1
              #print(tmp_start, tmp_end, tmp_label, tmp_token)
              gold_data_entities.append(gold_data_dic)
              gold_data_tokens.append(gold_data_dic)


  gold_data_entity = pd.DataFrame.from_records(gold_data_entities)
  gold_data_token = pd.DataFrame.from_records(gold_data_tokens)
  print(len(gold_data_entity), len(gold_data_token))
  print(gold_data_entity)
  print(gold_data_token)

  # this line to save the excel file of entities only
  gold_data_entity.to_excel(path+'gold_data_entity_CHoffsetEntitiesOnly_'+name+'.xlsx', index=False)

  # this line to save the excel file with all tokens
  gold_data_token.to_excel(path+'gold_data_entity_CHoffset_all_token_'+name+'.xlsx', index=False)




path = "/content/drive/MyDrive/collabrations_/HumanLoopH/Med7/data/"

train_validation = pd.read_json(path+"train_validation_429.json", lines=True)
print("pre-processing train_validation set")
preprocess(train_validation, 'train_validation_429', path)

train = pd.read_json(path+"train_353.json", lines=True)
print("pre-processing training set")
preprocess(train, 'train_353', path)

validation = pd.read_json(path+"validation_76.json", lines=True)
print("pre-processing validation set")
preprocess(validation, 'validation_76', path)

test = pd.read_json(path+"test_76.json", lines=True)
print("pre-processing testing set")
preprocess(test, 'test_76', path)