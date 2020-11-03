import json, sys
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from keyword_engine.keyword_extraction.keyword_extractor import KeywordExtract


# setup keyword extract
jsonpath = "keyword_engine/data/0_0.json"
f = open(jsonpath,)
jsonObj = json.load(f)
KeywordExtractor = KeywordExtract(jsonObj)


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the keyword engine index index.")

@csrf_exempt
def extract_keywords(request):

    request_json = json.loads(request.body)
    questions_keywords_list = []

    # TODO : Add synonym expansion
    if 'question_answer_list' not in request_json.keys():
        return JsonResponse({"message":"request does not contain a question answer list"})

    for qa_pair in request_json['question_answer_list']:
        temp_keyword_dict = {}

        if 'question' not in qa_pair.keys():
            return JsonResponse({"message":"a qa pair does not have a question"})
        
        if 'answer' not in qa_pair.keys():
            return JsonResponse({"message":"a qa pair does not have an answer"})
        
        # If first time being sent, calculate a unique id
        query_string = qa_pair['question'].replace("?","") \
            + " " + qa_pair['answer'].replace("?","")

        # Extract keywords on the basis of the user input
        boosting_tokens = KeywordExtractor.parse_regex_query(query_string)

        if 'id' not in qa_pair.keys():
            return JsonResponse({"message":"a qa pair does not have an id"})

        temp_keyword_dict['id'] = qa_pair['id']
        temp_keyword_dict['keywords']=boosting_tokens

        questions_keywords_list.append(temp_keyword_dict)    
        # Logging
        original_stdout = sys.stdout 
        with open('keyword_log.txt', 'a') as f:
            sys.stdout = f # Change the standard output to the file we created.
            print('$'*80)
            print("The user query is ", query_string)
            print("The extracted tokens are ", boosting_tokens)
            print('$'*80)
            sys.stdout = original_stdout

    response = {
        "questions_keywords_list":questions_keywords_list
    }

    #TODO :  preprocess cleaned boosting tokens to line up with specified tokens
    return JsonResponse(response)