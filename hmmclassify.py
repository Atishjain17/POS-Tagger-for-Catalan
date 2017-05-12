import json
import sys

input_file = open("catalan_corpus_dev_raw.txt","r", encoding="utf8")
input = input_file.read()
input_file.close()
input = input.split('\n')
del input[-1]

f=open('model.json','r',encoding="utf8")
hmm_model=json.load(f)
f.close()

emission_prob=hmm_model['emission_dict']
transmission_prob=hmm_model['transmission_dict']
default_tags=hmm_model['unique_tags']
zero_tag_prob = [0] * len(default_tags)
default_tag_prob=[]
default_tag_prob.append(default_tags)
default_tag_prob.append(zero_tag_prob)

# Create sentence node
class Node_State(object):
    """A class that makes a queue type table of nodes"""

    def __init__(self, previous_tag , word_tag,word,probability,level):
        self.previous_tag = previous_tag
        self.word_tag = word_tag
        self.word = word
        self.probability=probability
        self.level=level

    def description(self):
        return "Previous tag is %s, word tag %s, word is %s, probability is %s" % (self.previous_tag, self.word_tag, self.word, self.probability)
### Node_Sent Class Created

def get_tag(word):
    tag_prob=[]
    tag=[]
    prob=[]
    if word in emission_prob.keys():
        for key, value in emission_prob[word].items():
            tag.append(key)
            prob.append(value)
        tag_prob.append(tag)
        tag_prob.append(prob)
        return tag_prob
    else:
        return default_tag_prob

    #return tags

file = open("testoutput.txt", 'w+',encoding="utf8")
for i in range(len(input)):
    tree_queue = []
    history_queue = []
    level=0
    sentence = input[i].split(' ')
    #print(sentence)
    possible_tag= get_tag(sentence[0])
    for tags in range(len(possible_tag[0])):
        curr_prob = possible_tag[1][tags]+transmission_prob['start'][possible_tag[0][tags]]
        node = Node_State('start',possible_tag[0][tags],sentence[0], curr_prob,level)
        tree_queue.append(node)
    #for j in range(len(tree_queue)):
    #    print(tree_queue[j].description())
    for curr_word in range(1,len(sentence)):
        level=level+1
        ##print(sentence[curr_word])
        possible_tag= get_tag(sentence[curr_word])
        no_of_transitions=len(tree_queue)
        for tags in range(len(possible_tag[0])):
            tag_prob= float('-inf')
            prev_tag=None
            for transition in range(no_of_transitions):
                prev_node=tree_queue[transition]
                curr_prob = possible_tag[1][tags] + transmission_prob[prev_node.word_tag][possible_tag[0][tags]]
                curr_prob += prev_node.probability
                if(tag_prob<curr_prob):
                    tag_prob=curr_prob
                    prev_tag=prev_node.word_tag
            node = Node_State(prev_tag, possible_tag[0][tags], sentence[curr_word], tag_prob,level)
            tree_queue.append(node)
            ##print(node.description())

        for transition in range(no_of_transitions):
            history_queue.append(tree_queue.pop(0))
    last_tag_prob = float('-inf')
    for last_transition in range(len(tree_queue)):
        prev_node = tree_queue.pop(0)
        if (last_tag_prob < prev_node.probability):
            last_tag_prob = prev_node.probability
            last_node = prev_node

    answer=last_node.word+"/"+last_node.word_tag+"\n"
    parent=last_node.previous_tag
    child_word_level=last_node.level
    for print_word in reversed(history_queue):
        if(print_word.level==(child_word_level-1) and print_word.word_tag == parent):
            answer = print_word.word+"/"+print_word.word_tag+" "+answer
            parent=print_word.previous_tag
            child_word_level=print_word.level

    file.write(answer)
file.close()