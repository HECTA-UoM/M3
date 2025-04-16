# this code is to fine-tune Med7 with two versions
#en_core_med7_trf en_core_med7_lg

import random
import pandas as pd
import spacy
from spacy import util
from spacy.tokens import Doc
from spacy.training import Example
from spacy.tokens import DocBin
from spacy.language import Language


def customizing_pipeline_component(path, nlp: Language, offset, name):
    file = open(path+"loss_log.txt", "w")

    #optimizer = nlp.create_optimizer()
    optimizer = nlp.resume_training()
    print(type(offset), len(offset))
    print("   Training ...")
    # setup the number of iterations here
    iter = 2
    file.writelines("post-training " + name + "for " + str(iter) + "iterations\n")
    for _ in range(iter):
        print("iteration: " + str(_))
        random.shuffle(offset)
        losses = {}
        for raw_text, entity_offsets in offset: # add character indexes
            entities = spacy.training.offsets_to_biluo_tags(nlp.make_doc(raw_text), entity_offsets)
            #print(entities)
            doc = nlp.make_doc(raw_text)
            example = Example.from_dict(doc, {"entities": entity_offsets})
            #print('[example]', len([example]))
            nlp.update([example], sgd=optimizer, losses=losses)
        print(_, losses)
        file.writelines("iteration: "+ str(_) + str(losses)+"\n")
    file.close()
    # save the post-trained model
    nlp.to_disk(path + name +"_plus")

    # Result after training
    print(f"Result AFTER training:")
    df = pd.read_json(path + "test_76.json", lines=True)

    predict_labels_lg_dic = []

    for i, token in enumerate(df.tokens.to_list()):
      token_str_lg = ' '.join(str(t) for t in token)

      entities = nlp(token_str_lg)
      for e in entities.ents:
        predict_dic = {}
        predict_dic["predict_file_id"] = i
        predict_dic['predict_label'] = e.label_
        predict_dic['predict_start'] = e.start
        predict_dic['predict_end'] = e.end
        predict_dic['predict_text'] = e.text
        predict_dic['start_char'] = e.start_char
        predict_dic['end_char'] = e.end_char

        predict_labels_lg_dic.append(predict_dic)
      print('file_id:', i)

    print(len(predict_labels_lg_dic))
    predict_label_entity = pd.DataFrame.from_records(predict_labels_lg_dic)
    print(predict_label_entity)

    # uncomment to save the output of the prediction after fine-tuning MED7
    predict_label_entity.to_excel(path + 'test_76_'+name+'_fine_tuned_'+str(iter)+'iterations.xlsx', index=False)

def main():
    input_dir = "/content/drive/MyDrive/collabrations_/HumanLoopH/Med7/data/"
    print("read data")
    json = pd.read_json(input_dir + "train_validation_429.json", lines=True)
    excel = pd.read_excel(input_dir + 'gold_data_entity_CHoffsetEntitiesOnly_train_validation_429.xlsx')
    input_annotations_all = []
    print("processing data")
    for i, token in enumerate(json.tokens.to_list()):
      input_annotations = []
      # create one discharge summary with its NER labels
      token_str_lg = ' '.join(str(t) for t in token)
      file_id =  excel[excel['file_id'] == i]
      for i, row in file_id.iterrows():
        input_annotations.append((int(row[5]), int(row[6]), row[1])) #(start, end, label)
      input_annotations_all.append([token_str_lg, input_annotations])
    print("post-training en_core_med7_lg")
    med7 = spacy.load("en_core_med7_lg")
    customizing_pipeline_component(input_dir, med7, input_annotations_all, "en_core_med7_lg")

    # uncomment th elines below to fine-tune "en_core_med7_trf"
    print("post-training en_core_med7_trf")
    med7 = spacy.load("en_core_med7_trf")
    customizing_pipeline_component(input_dir, med7, input_annotations_all, "en_core_med7_trf")

if __name__ == '__main__':
    main()