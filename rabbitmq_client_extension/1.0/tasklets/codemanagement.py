
__author__ = 'aserver'
__tags__   = 'codemanagement',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    qpackage.checkoutRecipe()
