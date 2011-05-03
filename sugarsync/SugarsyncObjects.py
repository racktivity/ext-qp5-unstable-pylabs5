from xml.dom import minidom
import new
import re

def User(xmlResponse):
    return xml2Dic(xmlResponse).get('user', Hook())

def Folder(xmlResponse):
    return xml2Dic(xmlResponse).get('folder', Hook())

def Workspace(xmlResponse):
    return xml2Dic(xmlResponse).get('workspace', Hook())

def File(xmlResponse):
    return xml2Dic(xmlResponse).get('file', Hook())

def CollectionContents(xmlResponse):
        return xml2Dic(xmlResponse).get('collectionContents', Hook())
    
def Albums(xmlResponse):
    return xml2Dic(xmlResponse).get('albums', Hook())
        
def Album(xmlResponse):
    return xml2Dic(xmlResponse).get('album', Hook())

#http://code.activestate.com/recipes/116539/
#Recipe 116539: turn the structure of a XML-document into a combination of dictionaries and lists

class Hook(object):
    pass

class NotTextNodeError:
    pass

def cleanString(s):
    # Remove invalid characters
    s = re.sub('[^0-9a-zA-Z_]', '', s)
    # Remove leading characters until we find a letter or underscore
    s = re.sub('^[^a-zA-Z_]+', '', s)
    return s   

def getTextFromNode(node):
    """
    scans through all children of node and gathers the
    text. if node has non-text child-nodes, then
    NotTextNodeError is raised.
    """
    t = ""
    for n in node.childNodes:
        if n.nodeType == n.TEXT_NODE:
            t += n.nodeValue
        else:
            raise NotTextNodeError
    return t


def xml2Dic(xmlDoc):
    return node2Dic(minidom.parseString(xmlDoc))

def node2Dic(node):
    """
    node2Dic() scans through the children of node and makes a
    dictionary from the content.
    three cases are differentiated:
    - if the node contains no other nodes, it is a text-node
    and {nodeName:text} is merged into the dictionary.
    - if the node has the attribute "method" set to "true",
    then it's children will be appended to a list and this
    list is merged to the dictionary in the form: {nodeName:list}.
    - else, nodeToDic() will call itself recursively on
    the nodes children (merging {nodeName:nodeToDic()} to
    the dictionary).
    """
    dic = {} 
    for n in node.childNodes:
        if n.nodeType != n.ELEMENT_NODE:
            continue
#        if n.hasChildNodes():
        if n.getAttribute("multiple") == "true" or n.nodeName == 'collectionContents':
            # node with multiple children:
            # put them in a list
            childrenDict = {}
            childrenDict.update(dict(n.attributes.items()))
            counter = int(childrenDict.get('start', -1))
            for c in n.childNodes:
                if c.nodeType != n.ELEMENT_NODE:
                    continue
#                childrenDict['%s_%s'%(c.nodeName, counter)] = node2Dic(c)
                childrenDict.update({'%s_%.03d'%(str(c.nodeName), counter) : new.classobj(str('%s_%.03d'%(c.nodeName, counter)), (Hook,), node2Dic(c))})
                if counter > -1: counter += 1
#            dic.update({n.nodeName: childrenDict})
            dic.update({n.nodeName : new.classobj(str(n.nodeName), (Hook,), childrenDict)})
            continue
        
        try:
            text = getTextFromNode(n)
        except NotTextNodeError:
                # 'normal' node
#                dic.update({n.nodeName:node2Dic(n)})
                dic.update({n.nodeName : new.classobj(str(n.nodeName), (Hook,), node2Dic(n))})
                continue
        
            # text node
        dic.update({n.nodeName:text})
        continue
    return dic



