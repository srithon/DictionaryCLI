import requests
import json

class DictionaryAPIInterface:
    def __init__(self):
        self.mode = 't'
        with open('keys.json', 'r') as keys_file:
            json_text = keys_file.read()
        self.keys_dict = json.loads(json_text)
        self.session = requests.Session()
    def request(self, word):
        key = self.keys_dict['dict-key'] if self.mode == 'd' else self.keys_dict['thes-key']
        response = self.session.get(f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/voluminous?key={key}')
        try:
            response = response.json()[0]
        except Exception as e:
            return e
        word_class = response['fl']
        definitions_base = response['def'][0]['sseq']
        definitions = list()
        for part in definitions_base:
            for section in part:
                definitions.append(section[1]['dt'][0][1])
        output = f'\"{word}\": {word_class}\n'
        for definition in definitions:
            definition = definition[4:].rstrip()
            definition = definition.split(' ')

            pretty_definition = ''

            for word in definition:
                # print(word)
                if word[0] != '{':
                    pretty_definition += word
                else:
                    word = word.split('|')
                    if word[1][-1] != '}':
                        pretty_definition += word[1]
                    else:
                        pretty_definition += word[1][:-1]
                pretty_definition += ' '
            output += pretty_definition
            output += '\n'
        return output
    def set_mode(self, mode):
        self.mode = mode

x = DictionaryAPIInterface()
x.set_mode('d')
print(x.request('hello'))

word = ''
while word != 'exit':
    word = input('Word: ')
    print(x.request(word))