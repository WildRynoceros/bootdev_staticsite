text = "### ###2 HEADER"

def block_to_block_type(block):
    # Headings
    if block[0] == '#':
        try:
            if block[0:block.index(' ') + 1] in [('#' * i) + ' ' for i in range(1, 7)]:
                return 'HEADING'
        except ValueError:
            pass
    # Code
    if block[0:3] == '```' and block[-3:] == '```':
        return 'CODE'
    # Quote
    if block[0:2] == '> ':
        lines = block.splitlines()
        if all(line[0:2] == '> ' for line in lines):
            return 'QUOTE'
    # Unordered list
    if (block[0:2] == '* ') or (block[0:2] == '- '):
        lines = block.splitlines()
        if all((line[0:2] == '* ' or line[0:2] == '- ') for line in lines):
            return 'UNORDERED_LIST'
    # Ordered list
    if block[0:3] == '1. ':
        lines = block.splitlines()
        pairs = list(enumerate(lines, start=1))
        # Why doesn't this conditional break out to the else block?
        if all(pair[1][0:3] == f'{pair[0]}. ' for pair in pairs):
            return 'ORDERED_LIST'
        else:
            return 'PARAGRAPH'
    else:
        return 'PARAGRAPH'

def main():
    print(block_to_block_type(text))

if __name__ == '__main__':
    main()