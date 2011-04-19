__author__   = 'incubaid'
__tags__     = 'configure',
__priority__ = 1

def match(q, i, params, tags):
    return True

def main(q, i, params, tags):
    q.extensions.enable('q.manage.workflowengine')
    q.extensions.enable('q.workflowengine.agentcontroller')
    q.extensions.enable('q.workflowengine.actionmanager')
    q.extensions.enable('i.config.workflowengine')
    q.extensions.enable('q.workflowengine.jobmanager')

