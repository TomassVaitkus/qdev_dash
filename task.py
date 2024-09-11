import pandas as pd

data_df = pd.read_csv('data.txt')


def filtering_function(inp):
    row_data_tmp = inp
    row_data_tmp.suma = row_data_tmp.Red + row_data_tmp.Yellow + row_data_tmp.Green
    wrong_data = row_data_tmp.loc[row_data_tmp['Red'] + row_data_tmp['Yellow'] + row_data_tmp['Green']  > 1]
    right_data = row_data_tmp.loc[row_data_tmp['Red'] + row_data_tmp['Yellow'] + row_data_tmp['Green']  == 1]
    df_red = right_data.loc[right_data.Red == 1]
    df_green = right_data.loc[right_data.Green == 1]
    df_yellow = right_data.loc[right_data.Yellow == 1]
    red_time = sum(df_red.TimeActive)
    green_time = sum(df_green.TimeActive)
    yellow_time = sum(df_yellow.TimeActive)



    return df_red, df_green, df_yellow, len(df_red), len(df_yellow), len(df_green),\
        wrong_data, red_time, green_time, yellow_time



def apperance_counting(inp):
    pattern_list = [1, 1, 1, 1, 1]

    apperence_counter = 0
    counter = 0

    for idx in range(len(inp)):
        if inp.Red[idx] != 1:
            continue
        if inp.Red[idx] == 1:
            if idx == len(inp) - 4:
                break
            else:
                for element in pattern_list:
                    idx_tmp = idx
                    if element == inp.Red[idx_tmp]:
                        counter = counter + 1
                        idx_tmp = idx_tmp + 1
                        continue
                    elif element == inp.Yellow[idx_tmp]:
                        counter = counter + 1
                        idx_tmp = idx_tmp + 1
                        continue
                    elif element == inp.Green[idx_tmp]:
                        counter = counter + 1
                        idx_tmp = idx_tmp + 1
                        continue
                    elif element == inp.Yellow[idx_tmp]:
                        counter = counter + 1
                        idx_tmp = idx_tmp + 1
                        continue
                    elif element == inp.Red[idx_tmp]:
                        counter = counter + 1
                        idx_tmp = idx_tmp + 1
                        continue
                    else:
                        continue
            if counter == 5:
                apperence_counter = apperence_counter + 1
                counter = 0
        else: continue
    
    return apperence_counter
    
filtering_function(data_df)



