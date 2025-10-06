import re
from setup.default_values import defaults


class CustomConfigParser:
    """
    A simple configuration file parser that supports sections, key-value pairs,
    comments, and multiline values.
    1. Sections are defined by [section_name].
    2. Key-value pairs are defined by key=value.
    3. Comments start with # or ; and are ignored.
    4. Multiline values are supported using a backslash (\\) at the end of a line.
    5. The parser reads the configuration file and stores the data in a nested dictionary.
    6. The get method retrieves values with support for default values if the key or section is missing.
    7. Example configuration file:
        # This is a comment
        [General]
        key1=value1
        key2=value2 line1 \
        value2 line2
        ; Another comment
        [Settings]
        option1=option_value1
        option2=option_value2
    8. Example usage:
        config = CustomConfigParser()
        config.read('config.txt')
        value = config.get('General', 'key2')
    9. This will return 'value2 line1 \nvalue2 line2'
    10. If 'key2' or 'General' section is missing, it will return the default value if defined in defaults.py.
    11. The defaults.py file should contain a dictionary named 'defaults' with default values.
    12. Example defaults.py:
        defaults = {
            'General': {
                'key1': 'default_value1',
                'key2': 'default_value2'
            },
            'Settings': {
                'option1': 'default_option_value1'
            }
        }
    13. This parser does not handle nested sections or complex data types.
    14. It is designed for simplicity and ease of use in basic configuration scenarios.
    15. Error handling is minimal; it assumes the configuration file is well-formed.
    16. The parser can be extended to include more features as needed.
    17. when a = have to be passed in the value it should be escaped like this \\-
    and that will be converted back to =
    18. The parser is case-sensitive for section names and keys.
    19. Leading and trailing whitespace around keys and values are stripped.
    """
    def __init__(self):
        self.data = {}

    def read(self, filename):
        with open(filename, 'r') as file:
            current_section = None
            multiline_value = None
            multiline_key = None

            for line in file:
                line = line.strip()

                # comments
                if line.startswith('#') or line.startswith(';') or not line:
                    continue

                # Section
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
                        try:
                            self.data[current_section][key] = value
                            continue
                        except Exception as e:
                            print(F"Error in the config file: {e}")
                            exit()


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

        val = self.data.get(section, {}).get(key)

        if not val:
            val = defaults.get(section, {}).get(key)
        return val


if __name__ == "__main__":
    config = CustomConfigParser()
    config.read('exampleInput.txt')
    value = config.get('General', 'key2')
    print(value)






