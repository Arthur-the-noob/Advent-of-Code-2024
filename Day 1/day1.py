'''Day one advent'''
import pandas as pd

#Reading the input
elvish_input = pd.read_csv('Day 1\elv_input.txt', names = ['ListA', 'ListB'], delim_whitespace=True, engine= 'python')

ListA_series = elvish_input['ListA'].sort_values().reset_index()
ListA_series = ListA_series['ListA']

ListB_series = elvish_input['ListB'].sort_values().reset_index()
ListB_series = ListB_series['ListB']

Result_series = ListA_series - ListB_series
Result_series = Result_series.apply(abs)

full_result = Result_series.sum()

print(f'Distance: {full_result}')

Similarity_scores = []
affinity = 0
for index, value_to_compare in enumerate(ListA_series):
    score = (ListB_series.values == value_to_compare).sum()*value_to_compare
    Similarity_scores.append(score)
    affinity += score

print(f'Affinity score:{affinity}')



