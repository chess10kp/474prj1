# -------------------------------------------------------------------------
# dlang-parser.py: DLang Syntax Analyzer
# Run with source file 
# -------------------------------------------------------------------------
import sys
from sly import Lexer, Parser

class DLangLexer(Lexer):

    # Define names of tokens
    tokens ={LE, GE, R,  EQ, NE, AND, OR, INT, DOUBLE, STRING, IDENTIFIER, NOTHING, INTK, DOUBLEK, BOOL, BOOLK, STRINGK, INTERFACE, NULL, FOR, WHILE, IF, ELSE, RETURN, BREAK, ARRAYINSTANCE, OUTPUT, INPUTINT, INPUTLINE}
    
    # Single-character literals can be recognized without token names
    # If you use separate tokens for each literal, that is fine too
    literals = {'+', '-', '*', '/', '%', '<', '>', '=','!', ';', ',', '.', '[', ']','(',')','{','}'}
    
    # Specify things to ignore
    ignore = ' \t\r' # space, tab, and carriage return
    ignore_comment1= r'\/\*[^"]*\*\/' # c-style multi-line comment (note: test with input from file)
    ignore_comment = r'\/\/.*' # single line comment
    ignore_newline=r'\n+' # end of line

    # Specify REs for each token
    STRING = r'\"(.)*\"'
    DOUBLE = r'[0-9]+\.[0-9]*([E][+-]?\d+)?'
    INT = r'[0-9]+'
    EQ = r'=='
    NE = r'!='
    LE = r'<='
    GE = r'>='
    AND = r'&&' 
    OR =  r'\|\|'
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]{0,49}'

    # IDENTIFIER lexemes overlap with keywords.
    # To avoid confusion, we do token remaping.
    # Alternatively, you can specify each keywork before IDENTIFIER
    IDENTIFIER['nothing'] = NOTHING
    IDENTIFIER['int'] = INTK
    IDENTIFIER['double'] = DOUBLEK
    IDENTIFIER['string'] = STRINGK
    IDENTIFIER['bool'] = BOOLK
    IDENTIFIER['True'] = BOOL
    IDENTIFIER['False'] = BOOL
    IDENTIFIER['null'] = NULL
    IDENTIFIER['for'] = FOR
    IDENTIFIER['while'] = WHILE
    IDENTIFIER['if'] = IF
    IDENTIFIER['else'] = ELSE
    IDENTIFIER['return'] = RETURN
    IDENTIFIER['ArrayInstance'] = ARRAYINSTANCE
    IDENTIFIER['Output'] = OUTPUT
    IDENTIFIER['InputInt'] = INPUTINT
    IDENTIFIER['InputLine'] = INPUTLINE


    def error(self,t):
        print ("Invalid character '%s'" % t.value[0])
        self.index+=1

class DLangParser(Parser):


    precedence = (
        ("left", "+", "-"),
        ("left", "*", "/")
    )

    tokens = DLangLexer.tokens

    def __init__(self):
        self.IDENTIFIERs = { }

    # Program -> Decl+
    @_('Decls')
    def Program(self, p): 
        print('Parsing completed successfully!') # If we get here with no issues, bottom-up parsing is successful!
        return p
    
    @_('Decl Decls ','Decl')
    def Decls(self, p):
        #print(p)
        return p
    
    # Decl -> VariableDecl
    @_('VariableDecl')
    def Decl(self, p):
        return p.VariableDecl

    # Decl -> FunctionDecl
    @_('FunctionDecl')
    def Decl(self, p): 
        return p.FunctionDecl

    # VariableDecl -> Variable;
    @_('Variable ";" ')
    def VariableDecl(self, p):
        print ('Found VariableDecl', p.Variable)
        return p


    @_('Formals "," Variable' , 'Variable')
    def Formals(self, p): 
        return p.Variable


    @_('')
    def Formals(self, p): 
        return []

    # Variable -> Type ident
    @_('Type IDENTIFIER')
    def Variable(self, p):
        return p

    # FunctionDecl -> Type Ident (Formals) StmtBlock | nothing ident (Formals) StmtBlock
    @_('Type IDENTIFIER "(" Formals  ")" StmtBlock', 'NOTHING IDENTIFIER "(" Formals  ")" StmtBlock') 
    def FunctionDecl(self, p): 
        print("Found function declaration", p.IDENTIFIER) 
        return p


    # Type -> int | double | bool | string    
    @_('INTK', 'DOUBLEK', 'BOOLK', 'STRINGK')
    def Type(self, p):
        return p

    @_('IDENTIFIER')
    def Decl(self, p):
        try:
            return self.IDENTIFIERs[p.IDENTIFIER]
        except LookupError:
            print("Undefined IDENT '%s'" % p.IDENTIFIER)
            return 0



    @_('VariableDecl VariableDecls', 'VariableDecl', '')
    def VariableDecls(self, p):
        print("Found variable declaration")
        return p

    @_('Stmt Stmts', 'Stmt',  '') 
    def Stmts(self, p):
        print("Found statements", p)
        return p

#    # StmtBlock -> {VariableDecl* Stmt*}
    @_('"{" VariableDecls Stmts "}"')
    def StmtBlock(self, p): 
        print("Found Statement block", p.VariableDecls)
        return p

#    # Stmt -> <Expr> ; | IfStmt | WhileStmt | ForStmt | BreakStmt | ReturnStmt | OutputStmt | StmtBlock 
    @_('Expr ";"', 'IfStmt', 'WhileStmt', 'ForStmt', 'BreakStmt', 'ReturnStmt', 'OutputStmt', 'StmtBlock')
    def Stmt(self, p): 
        return p
#
    # IfStmt -> if {Expr} Stmt <else Stmt>
    @_('IF "(" Expr ")" Stmt ELSE Stmt')
    def IfStmt(self, p):
        print("Found if-else statement", p)
        return p
#
    @_('IF "{" Expr "}" Stmt ')
    def IfStmt(self, p):
        print("Found if statement", p)
        return p

    # WhileStmt -> while {Expr} Stmt
    @_('WHILE "(" Expr ")" Stmt')
    def WhileStmt(self, p):
        print("Found while statement", p)
        return p 

    @_('Expr Exprs', 'Expr') 
    def Exprs(self, p): 
        print("Comma separated expressions", p)
        return p

   # ForStmt -> for (Expr; Expr; Expr) Stmt
    @_("FOR '(' Expr ';' Expr ';' Expr ')' Stmt")
    def ForStmt(self, p): 
       print("Found for statement", p)
       return p
#
    # BreakStmt -> break ;
    @_('BREAK ";" ')
    def BreakStmt(self, p):
        print("Found break statement", p)
        return p 
#
    # ReturnStmt -> return <Expr> ;
    @_('RETURN Expr ";"')
    def ReturnStmt(self, p): 
        print("Found return statement", p)
        return p 
#    
    # OutputStmt -> Output (Expr+.);
    @_('OUTPUT "(" Exprs ")" ";"')
    def OutputStmt(self, p): 
        print("Found output statement", p)
        return p 
#
    # actuals -> Expr+, |e
    @_('Actuals "," Expr', 'Expr')
    def Actuals(self, p): 
        return p
#
#    
    # Expr -> IDENTIFIER = Expr | IDENTIFIER | Constant | Call | (Expr) | Expr+Expr | Expr - Expr | Expr *Expr | Expr/Expr | Expr % Expr | - Expr | Expr < Expr | Expr <= Expr | Expr > Expr | Expr >= Expr | Expr == Expr | Expr != Expr | Expr && Expr | Expr || Expr | !Expr | InputInt() | InputLine()
    @_('IDENTIFIER "=" Expr', 'IDENTIFIER', 'Constant', 'Call','"(" Expr ")"' ,  'Expr "+" Expr', 'Expr "-" Expr', 'Expr "*" Expr',
       'Expr "/" Expr', 'Expr "%" Expr', '"-" Expr', 'Expr "<" Expr', 'Expr LE Expr', 'Expr ">" Expr', 'Expr GE Expr', 'Expr EQ Expr',
       'Expr NE Expr', 'Expr AND Expr', 'Expr OR Expr', '"!" Expr', 'INPUTINT "(" ")"', 'INPUTLINE "(" ")" ')
    def Expr(self, p): 
        return p 
#
    # Call -> IDENTIFIER ( Actuals )
    @_('IDENTIFIER "(" Actuals ")"')
    def Call(self, p):
        return p 
#
    # Constant -> intConstant | doubleConstant | boolConstant | stringConstant | null
    @_('INT', 'DOUBLE', 'BOOL', 'STRING', 'NULL')
    def Constant(self, p): 
        return p

#
if __name__ == '__main__':

    lexer = DLangLexer()
    parser = DLangParser()
    with open('test-parser.dlang') as source:
        dlang_code = source.read()
        try:
            tokenized = lexer.tokenize(dlang_code)
            parser.parse(tokenized)
        except EOFError: exit(1)
    # Expects DLang source from file
    if len(sys.argv) == 2:
        lexer = DLangLexer()
        parser = DLangParser()
        with open(sys.argv[1]) as source:
            dlang_code = source.read()
            try:
                parser.parse(lexer.tokenize(dlang_code))
            except EOFError: exit(1)
    else:
        print("[DLang]: Source file missing")
