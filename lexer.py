from sly import Lexer


class Winter2024Lexer(Lexer):
  # define names of tokens
  tokens = { AND, OR, LEFTPAR,RIGHTPAR, LEFTBRACKET, RIGHTBRACKET, LEFTBRACE, RIGHTBRACE,EQUALITY,INEQUALITY, SEMICOLON, ASSIGN, INTEGER, DOUBLE,IDENTIFIER, INTK, FLOATK, DOUBLEK, CHAR, FOR, WHILE, IF, BREAK, SWITCH, CLASS, PRIVATE, PUBLIC,  NOTHING,   BOOLK, BOOL, STRING, CLASS, INTERFACE, NULL, THIS, EXTENDS, IMPLEMENTS, FOR, WHILE, IF, ELSE, RETURN, BREAK, NEW, ARRAYINSTANCE, OUTPUT, INPUTINT, INPUTLINE, LESSTHANEQ, GREATERTHANEQ }

  literals ={'+', '-', '*', '/', '%', '>', '<', '!' } 
  # specify items to ignore
  ignore = ' \t' # ignore white space
  ignore_newline = r'\n+' # ignore newlines
  ignore_comment1 = '\/\/.*'  # // comment goes here
  ignore_comment2 = '\/\*(.|\n|\t|\r)*\*\/'

  # String
  STRING = r'\"(.)*\"'
  # Special symbols
  AND = r'&&'
  OR = r'\|\|'
  LEFTPAR = r'\('
  RIGHTPAR =r'\)'
  LEFTBRACKET = r'\['
  RIGHTBRACKET = r'\]'
  LEFTBRACE = r'\{'
  RIGHTBRACE = r'\}'
  SEMICOLON = r'\;'
  EQUALITY = r'\=='
  ASSIGN= r'\='
  INEQUALITY = r'\!='
  LESSTHANEQ = r'<='
  GREATERTHANEQ = r'>='

  # Numbers
  DOUBLE= r'[-|+]?[0-9]+\.[0-9]+(E[-|+]?[0-9]+)?'
  INTEGER = r'[-|+]?[0-9]+'

  # Identifiers
  IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]{0,49}'
  IDENTIFIER['int'] = INTK
  IDENTIFIER['float'] = FLOATK
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


  # Have error handling
  def error(self, t):
    print ('Invalid character/token: ', t.value[0])
    self.index+= 1



if __name__ =='__main__':
  myscanner = Winter2024Lexer()
  stream = '''
hello

ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJ
ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJhello
ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJ12345
ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJ1234.22323
ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJ1234.2323E+123

""

    " this is a string. Anything (for example,? $ #) except double qoutes can appear here."

"
This is a multiline string
It is not accepted.
"

____varname
____
2323432

121.1212
123.
1232.12321E33
1212.212E+2
2323.234342E-2342
233.232e+23
_sdfsd

true
True
False

TrueFalse

for

while

new
this

class
nothing
break
if
else
bool
// singe line comment. anything i$ p0$$ible here

/* 
This 
is 
a 
multi-line
comment.
Should be ignored.

*/


/*

*/
,
.


=
==
<=
&&
&
?
||
!=
!

// check invalid doubles
.4E7
1.E5
1.3E

// Check empty string
""

// check identifiers again
ABABABABABABABABABABABABABABABABABABABABABABABABABintxy
ABABABABABABABABABABABABABABABABABABABABABABABABABintxy int

      '''
  # input('Winter2024Lexer$')
  for token in myscanner.tokenize(stream):
    print ('type=%r , value=%r' %(token.type, token.value))

