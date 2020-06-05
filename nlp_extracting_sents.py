# -*- coding: utf-8 -*-
"""
@author: mahamudulrahat94
"""
#import necessary libraries

import pandas as pd
import numpy as np
import spacy 
from spacy.matcher import Matcher 
from spacy.tokens import Span 



#import the data
data=pd.read_csv('Company descriptions-Grid view.csv')
data.dropna(axis='index',inplace=True)
data=data.reset_index()

#This is the most important part of the code,performace depends on this two parameter
sentence_breaker=['.','which','that',',','to']
stop_words=['is','was','founded','has','had','have','supports','visualizes','compatible',':',
                'believe','believes','accurately','partnered','partner','retrieves','brand','based']


#this creates custom rule to break the sentences (default is full stop(.))

def set_custom_boundaries(doc_):
        for token in doc_[:-1]:
            if token.text in sentence_breaker:
                 doc_[token.i+1].is_sent_start = True
        return doc_
#creating instances of nlp object from spacy
custom_nlp = spacy.load('en_core_web_sm')
custom_nlp.add_pipe(set_custom_boundaries, before='parser')
    

companies=[ ]
description=[ ]

#working with 10 companies
company_number=10
for company_index in range(0,company_number):
    doc = custom_nlp(str(data['Description'][company_index]))
    doc_sentences = list(doc.sents)
    #storing the sentences in a list
    doc_sentences_c=[ ]
    for sentence in doc_sentences:
       doc_sentences_c.append(str(sentence))  
    #indexes to keep the sentence or delete
    to_del=[ ]
    to_keep=[ ]
    for i in range(0,len(doc_sentences_c)):
        s_nlp=nlp(str(doc_sentences_c[i]).lower())#created another instance of nlp for the extracted sentence
        p=0
        for tok in s_nlp: 
           if tok.text in stop_words:#checking if the sentence contain stop word
               to_del.append(i)
               p=1
        #checking if the sentence contain root VERB and also does not contain any stop words
           if (tok.dep_=='ROOT' and tok.pos_=='VERB') and p==0:
               to_keep.append(i)
           elif (tok.dep_=='advcl' and tok.pos_=='VERB') and p==0:
               to_keep.append(i)
    #keeping the extracted sentences in a list
    extracted_doc_sentences=[ ]
    for index in set(to_keep):
        extracted_doc_sentences.append(doc_sentences_c[index])
    #storing the tokenization number of the words to find out the first word,which is company name
    token_dict={}
    for tok in doc: 
        token_dict[tok.idx]=tok.text
    company_name=str(token_dict[0])
    companies.append(company_name)

    #joing the extracted sentence list into a string
    s = ','.join(extracted_doc_sentences)
    #keeping the string in a list for all the companies
    description.append(s)
    
#created a new dataframe to store the new values
new_df=pd.DataFrame()  
new_df['Company']=companies
new_df['Description']=data['Description'].loc[0:company_number]
new_df['Summary']=description
    
new_df.to_csv('extracted10.csv')