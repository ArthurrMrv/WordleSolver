import pandas as pd
import random

def main():
    df = pd.read_csv('5_letters.csv')
    df = pd.DataFrame(df)
    
    to_find = word_to_find(df)
    print("to_find: ", to_find)
    
    current_word = '11111'
    tries = -1
    while (current_word != to_find) and tries < 5:
        tries += 1
        
        validations = score(to_find, current_word)
        current_word, unwanted = next_word(df, current_word, validations)
        print("tries: ", tries)
    print("current: ", current_word)

def df_no(df: pd.DataFrame, 
       unwanted_list : list):
    for i in unwanted_list:
        df = df[~df.apply(lambda row: i[i] in row[[str(i) for i in range(1, 6)]].values, axis=1)]
    return df

def word_to_find(df : pd.DataFrame,
                 seed = 42):
    random.seed(seed)
    return ''.join(df.iloc[random.randint(0, df.shape[0]-1)].values)

def score(word_to_find, 
         current_word):
    
    compo_word_to_find = list(word_to_find)
    sc = [0 for _ in range(len(word_to_find))]
    
    for i in range(len(current_word)):
        if current_word[i] == word_to_find[i]:
            compo_word_to_find.remove(current_word[i])
            sc[i] = 1
    
    for i in range(len(current_word)):
        if sc[i] == 0 and current_word[i] in compo_word_to_find:
            compo_word_to_find.remove(current_word[i])
            sc[i] = 0.5

    return sc
    
def next_word(df : pd.DataFrame,
              previous : str,
              validations : list,
              unwanted_list : list = []):
    
    df_temp = pd.DataFrame()
    
    for i in range(len(validations)):
        match validations[i]:
            case 1:
                df_temp = df.loc[df[str(i+1)] == previous[i]]
            case 0.5:
                # all words with the letter but not in the i position
                df_temp = df.loc[df[str(i+1)].str.contains(previous[i])]
                unwanted_list.append([previous[i] if j == i else 0 for j in range(5)])
            case 0:
                unwanted_list.append([previous[i] for _ in range(5)])
                
    for i in unwanted_list:
        df_temp = df_no(df_temp, i)
    
    return list(df_temp.sample(1).values[0]), unwanted_list
  
if __name__ == '__main__':
    main()