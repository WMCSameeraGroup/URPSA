import re

class CustomConfigParser:
    def __init__(self):
        self.data = {}

    def read(self, filename):
        with open(filename, 'r') as file:
            current_section = None
            multiline_value = None
            multiline_key = None

            for line in file:
                line = line.strip()

                # Ignore comments
                if line.startswith('#') or line.startswith(';') or not line:
                    continue

                # Section header
                section_match = re.match(r'\[(.*?)\]', line)
                if section_match:
                    current_section = section_match.group(1)
                    self.data[current_section] = {}
                    continue

                # Key-Value pair
                key_value_match = re.match(r'([^=]+)=(.*)', line)
                if key_value_match:
                    key, value = key_value_match.groups()
                    key = key.strip()
                    value = value.strip()

                    # Check for multiline value continuation
                    if value.endswith('\\'):
                        multiline_key = key
                        multiline_value = value[:-1].strip() + '\n'
                        continue
                    else:
                        self.data[current_section][key] = value
                        continue

                # Continuation of a multiline value
                if multiline_key and current_section:
                    if line.endswith('\\'):
                        multiline_value += line[:-1].strip() + '\n'
                    else:
                        multiline_value += line
                        self.data[current_section][multiline_key] = multiline_value
                        multiline_key = None
                        multiline_value = None

    def get(self, section, key):
        return self.data.get(section, {}).get(key)


if __name__ == "__main__":
    config = CustomConfigParser()
    config.read('config.txt')
    value = config.get('General', 'key2')
    print(value)







