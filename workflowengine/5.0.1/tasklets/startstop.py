
__author__ = 'incubaid'
__tags__ = 'startstop',

def main(q, i, params, tags):
    qpackage = params['qpackage']

    def startmethod():
        pass

    def stopmethod():
        pass



    #GENERATED###################################################################
    if params['action']=="start":
        startmethod()
    if params['action']=="stop":
        stopmethod()
    if params['action']=="restart":
        stopmethod()
        startmethod()
