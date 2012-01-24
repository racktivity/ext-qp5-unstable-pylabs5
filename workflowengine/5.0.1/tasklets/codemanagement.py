__author__ = 'incubaid'
__tags__     = "codemanagement",
__priority__ = 1

def match(q, i, params, tags):
    return True

def main(q, i, params, tags):
    qpackage = params['qpackage']
    qpackage.checkoutRecipe()
