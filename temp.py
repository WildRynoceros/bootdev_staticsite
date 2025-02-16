import re

string = 'This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)'
pattern = r'(?<!!)\[[^\[]*\)'

