class Reporter:
    def __init__(self, smells):
        self.smells = smells

    def generate_report(self):
        '''
        :param smells: Dictionary containing the output of all smell detectors.
        Example:
            {
            'long_functions': {...},
            'large_classes': {...},
            'too_many_parameters': {...},
            'deep_nesting': {...}
            }
        '''
        print(('=' * 10), 'CODE SMELL REPORT', ('=' * 10))

        # Loop through all smell types and their results
        for smell_name, results in self.smells.items():
            self.print_smell(smell_name, results)
            print()


    def print_smell(self, smell_name, results):
        '''
        Print each smell type and its detected results.

        :param smell_name: The name of the smell (e.g. 'long_functions')
        :param results: The dictionary of detected issues for that smell
        '''

        # Format the smell name to make it more readable
        format_name = smell_name.replace('_', ' ').title()

        print(f'[SMELL] {format_name}:')

        # If no issues found / results is empty, print message
        if not results:
            print(' no issues found.')
            return

        # Print details depending on smell type
        for name, value in results.items():
            if smell_name == 'long_functions':
                print(f' - {name}: {value} lines')
            elif smell_name == 'large_classes':
                print(f"  - {name}: {value} methods")
            elif smell_name == 'too_many_parameters':
                print(f"  - {name}: {value} parameters")
            elif smell_name == 'deep_nesting':
                print(f"  - {name}: nesting depth {value}")
            else:
                print(f"  - {name}: {value}")  # fallback
