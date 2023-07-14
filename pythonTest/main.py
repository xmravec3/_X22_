import json
import HELLO.HELLO as hello


#if __name__ == "__main__":
    #text = hello.getText()
text = hello.getText()
#text.append({'text': 'HELLO'})
    
json_result = json.dumps(text)
print(json_result)