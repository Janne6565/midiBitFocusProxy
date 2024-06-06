import mido, requests
from collections import defaultdict

DEBUG_MODE = False
MAPPINGS = defaultdict(lambda: defaultdict(lambda: lambda: ""))

MAPPINGS['note_on'][40] = lambda: print("test")


def create_get_request(url):
    return lambda: requests.get(url)    

def get_user_select(options, output_function, title="Select:", formatting=lambda index, item: index + ": " + item):
    output_function(title)
    for index, option in enumerate(options):
        output_function(formatting(str(index), str(option)))
    
    output_function("")
    
    while (user_input := input("Your Choice: ")):
        try:
            parsed_user_input = int(user_input)
            if parsed_user_input >= 0 and parsed_user_input < len(options):
                return parsed_user_input
            raise Exception("unusable user input")
        except:
            output_function("Please enter a valid option")
            pass


def main():
    inputs = mido.get_input_names()
    selected_input_index = get_user_select(inputs, print, title="Select input device", formatting=lambda index, word: index + ": " + " ".join(word.split(" ")[:-1]))
    input_device = inputs[selected_input_index]
    
    with mido.open_input(input_device) as midi_input:
        for message in midi_input:
            if DEBUG_MODE:
                print(message)
            try:
                type = message.type
                MAPPINGS[type][message.note]()
            except:
                pass


if __name__ == '__main__':
    main()