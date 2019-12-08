
def clean_text(object):
    body = object.get()['Body'].read().decode().split("}{")
    cleaned_list = list(filter(lambda x: len(x) > 14, body))
    return cleaned_list

def generate_text_file(text):
    with open('tweet_text.txt', 'w') as f:
        for item in text:
            f.write("{}\n".format(item))