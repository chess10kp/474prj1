from sly import Lexer

class Winter2024Lexer(Lexer):
    # define names of tokens
    tokens = {AND, OR, LEFTPAR, RIGHTPAR, LEFTBRACKET, RIGHTBRACKET, LEFTBRACE, RIGHTBRACE, EQUALITY, INEQUALITY, SEMICOLON, ASSIGN, INTEGER, DOUBLE, IDENTIFIER, INTK, FLOATK, DOUBLEK, CHAR, FOR, WHILE, IF, BREAK, SWITCH,
               NOTHING, BOOLK, BOOL, STRING, CLASS, INTERFACE, NULL, THIS, EXTENDS, IMPLEMENTS, FOR, WHILE, IF, ELSE, RETURN, BREAK, NEW, ARRAYINSTANCE, OUTPUT, INPUTINT, INPUTLINE, LESSTHANEQ, LESSTHAN, GREATERTHAN, GREATERTHANEQ}

    literals = {'+', '-', '*', '/', '%', '!', "." , "," }

    ignore = ' \t'  # ignore white space
    ignore_newline = r'\n+'  # ignore newlines
    ignore_comment1 = '\/\/.*'  # comments
    ignore_comment2 = '\/\*(.|\n|\t|\r)*\*\/'

    # define regex for symbols
    STRING = r'\"(.)*\"'
    AND = r'&&'
    OR = r'\|\|'
    LEFTPAR = r'\('
    RIGHTPAR = r'\)'
    LEFTBRACKET = r'\['
    RIGHTBRACKET = r'\]'
    LEFTBRACE = r'\{'
    RIGHTBRACE = r'\}'
    SEMICOLON = r'\;'
    EQUALITY = r'\=='
    ASSIGN = r'\='
    INEQUALITY = r'\!='
    LESSTHANEQ = r'<='
    GREATERTHANEQ = r'>='
    LESSTHAN = r'<'
    GREATERTHAN = r">"

    # define regex for numbers
    DOUBLE = r'[-|+]?[0-9]+\.(E[-|+]?[0-9]+)?'
    INTEGER = r'[-|+]?[0-9]+'

    # define regex for identifiers
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]{0,49}'
    IDENTIFIER['int'] = INTK
    IDENTIFIER['float'] = FLOATK
    IDENTIFIER['double'] = DOUBLEK
    IDENTIFIER['char'] = CHAR
    IDENTIFIER['for'] = FOR
    IDENTIFIER['while'] = WHILE
    IDENTIFIER['if'] = IF
    IDENTIFIER['else'] = ELSE
    IDENTIFIER['break'] = BREAK
    IDENTIFIER['nothing'] = NOTHING
    IDENTIFIER['this'] = THIS
    IDENTIFIER['class'] = CLASS
    IDENTIFIER['bool'] = BOOLK
    IDENTIFIER['class'] = CLASS
    IDENTIFIER['null'] = NULL
    IDENTIFIER['this'] = THIS
    IDENTIFIER['extends'] = EXTENDS
    IDENTIFIER['implements'] = IMPLEMENTS
    IDENTIFIER['return'] = RETURN
    IDENTIFIER['new'] = NEW
    IDENTIFIER['ArrayInstance'] = ARRAYINSTANCE
    IDENTIFIER['Output'] = OUTPUT
    IDENTIFIER['InputInt'] = INPUTINT
    IDENTIFIER['InputLine'] = INPUTLINE
    IDENTIFIER['True'] = BOOL
    IDENTIFIER['False'] = BOOL

    #define error handling
    def error(self, t):
        print('Invalid character/token: ', t.value[0])
        self.index += 1

# test the lexer
if __name__ == '__main__':
    myscanner = Winter2024Lexer()
    try:
        while True:
            try:
                stream = input("DLang>>>")
                for token in myscanner.tokenize(stream):
                    print('type=%r , value=%r' % (token.type, token.value))
            except EOFError as e:
                break
    # handle C-c gracefully
    except KeyboardInterrupt as e:
        pass
