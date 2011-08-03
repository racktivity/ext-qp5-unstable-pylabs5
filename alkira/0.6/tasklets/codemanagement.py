__author__ = 'incubaid'
__tags__ = 'codemanagement',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    qpackage.checkoutRecipe()
