# Edit pre-process
import pandas as pd

df = pd.read_excel('/content/drive/MyDrive/Reasearch_Assistantship/HILO_project/n2c2_2018/train/output/output.xlsx')
print(df.columns)

df_copy = df.copy()
line = df_copy.index[df_copy['Unnamed: 2'] == "O"].tolist()
print(len(df_copy))
print(len(line))
df2 = pd.DataFrame(columns = ['Token', 'Label', 'Unnamed: 2'])
for id in line:
  tmp = df_copy.iloc[id]
  #print(tmp[2])

  test = pd.DataFrame({'Token' : tmp[0], 'Label' : tmp[2], 'Unnamed: 2' : pd.NA}, index=[id])
  df2 = pd.concat([df2, test], axis=0, ignore_index=False)
  #df2 = df2.append(test, ignore_index=False)
  test = pd.DataFrame({'Token' : tmp[1], 'Label' : tmp[2], 'Unnamed: 2' : pd.NA}, index=[id+1])
  df2 = pd.concat([df2, test], axis=0, ignore_index=False)
  #df2 = df2.append(test, ignore_index=False)

  #print(tmp)
print(len(df2))
print(df_copy.loc[[29490]])
df_copy = df_copy.drop(line)
print(len(df_copy))
line = df2.iloc[0]
print(line)
line = df2.iloc[1]
print(line)
# https://huggingface.co/course/chapter7/2
df3 = pd.concat([df2, df_copy], axis=0)
print(df3)
df3.to_excel('/content/drive/MyDrive/Reasearch_Assistantship/HILO_project/n2c2_2018/train/output/output2.xlsx', index=False)
 

###########

# split all discharge sammaries into seperate files, a file for a discharge summary

df = pd.read_excel('/content/drive/MyDrive/Reasearch_Assistantship/HILO_project/n2c2_2018/valid/output/output.xlsx', index=False)
print(len(df))
print(df.columns)

df_copy = df.copy()
line = []
for i, row in df_copy.iterrows():
  #print(i, row[0], row[1])
  if ".txt" in row[1]:
    print(i, row[0], row[1])
    line.append(i)
print(len(line))
print(line)
i = 0
while i+1 <= len(line):
  if i+1 == len(line):
    df_slice = df_copy.iloc[line[i]:len(df_copy), :]
    txt_ind = df_slice["Label"].tolist()
    print(txt_ind[0])
    df_slice.to_excel('/content/drive/MyDrive/Reasearch_Assistantship/HILO_project/n2c2_2018/valid/output/'+txt_ind[0]+'.xlsx', index=False)
  else:
    df_slice = df_copy.iloc[line[i]:line[i+1], :]
    txt_ind = df_slice["Label"].tolist()
    print(txt_ind[0])
    df_slice.to_excel('/content/drive/MyDrive/Reasearch_Assistantship/HILO_project/n2c2_2018/valid/output/'+txt_ind[0]+'.xlsx', index=False)
  i +=1