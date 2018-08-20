from pyparsing import *

from geosolver.ontology.ontology_definitions import signatures, FunctionSignature, VariableSignature
from geosolver.text.rule import TagRule
from geosolver.text.semantic_tree import SemanticTreeNode
from geosolver.utils.num import is_number

__author__ = 'minjoon'


def annotation_to_semantic_tree(syntax_parse, annotation_string):
    words = syntax_parse.words
    def span_f(a, b, c):
        if len(c) == 1:
            if c[0] == 'i':
                return 'i'
            else:
                return int(c[0]), int(c[0])+1
        else:
            return int(c[0]), int(c[1])+1

    def tag_f(a, b, c):
        assert len(c) == 1
        if c[0][0].isupper() or is_number(c[0]):
            return 'function', c[0]
        else:
            return 'variable', c[0]

    def expr_f(a, b, c):
        local_span = c[1]
        children = c[2:]
        type_, s = c[0]
        # print 'words ', words
        # print 'a#b#c', a, '#', b, '#', c
        name = "_".join(words[idx] for idx in range(*local_span))
        # print 'name',name
        if s in signatures:            
            signature = signatures[s]
            # print 'name signature', signature
        elif type_ == 'function' and len(children) == 0:
            # Constant number
            signature = FunctionSignature(name, 'number', [], name=name)
            # print 'function signature', signature
        elif type_ == 'variable' and len(children) == 0:
            signature = VariableSignature((local_span, s), s, name=name)
            # print 'variable signature', signature
        else:
            raise Exception("local span: %r, children: %r, type: %r, s: %r"
                            % (local_span, children, type_, s))
        content = TagRule(syntax_parse, local_span, signature)
        # print 'content', content
        return SemanticTreeNode(content, children)

    current = Word(alphanums)
    span = (Word(nums) + Literal(":").suppress() + Word(nums)) | Word(nums)
    string = Literal("[").suppress() + Word(alphanums+"_") + Literal("]").suppress()
    tag = current.setParseAction(tag_f) + Literal("@").suppress() + span.setParseAction(span_f) + Optional(string).suppress()
    expr = Forward()
    expr << (tag + Optional(Literal("(").suppress() + expr +
                           ZeroOrMore(Literal(",").suppress() + expr) + Literal(")").suppress()))
    tokens = expr.setParseAction(expr_f).parseString(annotation_string)
    # print 'annotation_string', annotation_string
    # print 'tokens', tokens
    return tokens[0]

def is_valid_annotation(syntax_parse, annotation_string):
    try:
        annotation_to_semantic_tree(syntax_parse, annotation_string)
        return True
    except:
        return False





