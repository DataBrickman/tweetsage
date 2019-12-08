import re
import base64
import json

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        dict_data = base64.b64decode(record['data']).decode('utf-8').strip()

        text = dict_data.lower()
        text = re.sub("@", "a", text)
        text = re.sub("source uca", "", text)
        # text = re.sub("0", "o",text)
        text = re.sub(":\\)", "happyfaceemoji", text)
        text = re.sub(":\\(", "sadfaceemoji", text)
        text = re.sub("<3", "heartemoji", text)
        text = re.sub(";\\)", "winkfaceemoji", text)
        # text = emoji.demojize(text)
        text = re.sub(r'[0-9]+', '', text)
        text = re.sub("\\W+", ' ', text)
        text = text.split()
        stop = ['myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he',
                'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them',
                'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am',
                'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
                'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
                'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
                'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
                'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
                'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
                'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
        text = list(map(lambda x: x if not x in stop else '', text))
        text = list(filter(None, text))
        text = " ".join(text)
        text = text.split("href", 1)[0]
        text = re.sub("created_at", "", text)
        text = re.sub("id id_str text", "", text)
        data_record = {
            'message': text
        }

        print(text)
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(json.dumps(data_record).encode('utf-8')).decode('utf-8')
        }
        output.append(output_record)

    return {'records': output}

