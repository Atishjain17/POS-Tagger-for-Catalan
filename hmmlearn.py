import json
import collections
import sys
import math

input_file = open("catalan_corpus_train_tagged.txt","r", encoding="utf8")
input = input_file.read()
input_file.close()
input = input.split('\n')
del input[-1]
sentence = [[]]*len(input)
input_tag = [[]]*len(input)
unique_tags=set()
for i in range(len(input)):
    sentence[i] = input[i].split(' ')
    tag_words=[]
    for word in range(len(sentence[i])):
        tag_words.append(sentence[i][word][-2:])
        unique_tags.add(sentence[i][word][-2:])
        sentence[i][word] = sentence[i][word][:-3]
    input_tag[i]=tag_words

emission_dict = {}
unique_tags=list(unique_tags)

for i in range(len(input)):
    for word in range(len(sentence[i])):
        if(sentence[i][word] not in emission_dict):
            emission_dict[sentence[i][word]]={}
            emission_dict[sentence[i][word]][input_tag[i][word]]=1
        elif(input_tag[i][word] not in emission_dict[sentence[i][word]]):
            emission_dict[sentence[i][word]][input_tag[i][word]] = 1
        else:
            emission_dict[sentence[i][word]][input_tag[i][word]] += 1

transmission_dict = collections.OrderedDict()
transmission_denominator = collections.OrderedDict()
tag_count = collections.OrderedDict()

for tag in range(len(unique_tags)):
    transmission_dict[unique_tags[tag]] = collections.OrderedDict()
    transmission_denominator[unique_tags[tag]] = 0
    tag_count[unique_tags[tag]] = 0
    for next_tag in range(len(unique_tags)):
        transmission_dict[unique_tags[tag]][unique_tags[next_tag]]=1

transmission_dict['start'] = collections.OrderedDict()
transmission_denominator['start'] = 0
for next_tag in range(len(unique_tags)):
    transmission_dict['start'][unique_tags[next_tag]] = 1

for sentences in range(len(input_tag)):
    for curr_tag in range (len(input_tag[sentences])-1):
        transmission_dict[input_tag[sentences][curr_tag]][input_tag[sentences][curr_tag+1]] += 1
    transmission_dict['start'][input_tag[sentences][0]] += 1

for key in transmission_dict:
    for key1,value in transmission_dict[key].items():
        transmission_denominator[key] += value
#print(transmission_denominator)

for key in transmission_dict:
    for key1 in transmission_dict[key]:
        transmission_dict[key][key1] = math.log(transmission_dict[key][key1])-math.log(transmission_denominator[key])

#print(transmission_dict)
for word in emission_dict:
    for tag_key,count in emission_dict[word].items():
        tag_count[tag_key] += count

for word in emission_dict:
    for tag_key in emission_dict[word]:
        emission_dict[word][tag_key] = math.log(emission_dict[word][tag_key])-math.log(tag_count[tag_key])
#print(tag_count)
#print(emission_dict)
model={}
model['emission_dict']=emission_dict
model['transmission_dict']=transmission_dict
model['unique_tags']=unique_tags
f = open("model.json", "w+", encoding="utf8")
json.dump(model,f)
f.close()