import json, hashlib, requests
from django.test import TestCase, Client


class QAResponseTest(TestCase):
    def test_response(self):
        c = Client()
        qa_list = [
            {
                "question":"My child is sick where can he get measles vaccine ?",
                "answer":"Please go to khandala",
            },
            {
                "question":"My child is sick where can he get rubella vaccine ?",
                "answer":"Please go to khandala",
            },
            {
                "question":"My child is sick where can he get polio vaccine ?",
                "answer":"Please go to khandala",
            },
        ]

        for x in qa_list:
            query_string = x['question']+x['answer']
            qa_hash = hashlib.sha512(query_string.encode()).hexdigest()
            x['id']=qa_hash

        batch_response_test = {
            "question_answer_list" : qa_list
        }

        # import pdb
        # pdb.set_trace()
        url = "http://0.0.0.0:8000"
        base_url = url  + "/extract-keywords"
        response = requests.post(base_url, data=json.dumps(batch_response_test))
        print(response.text)

        # response = c.post('/extract-keywords', data=batch_response_test)
        # print(response)