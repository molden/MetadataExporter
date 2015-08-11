import os, sys
from stat import *
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
from xml.etree import ElementTree


def walktree(top, parent):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname).st_mode
        modification_time=os.stat(pathname).st_mtime
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            child = SubElement(parent,'dir',{'name':f,'modtime':str(modification_time)})
            walktree(pathname, child)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            child = SubElement(parent,'file',{'name':f,'modtime':str(modification_time)})
        else:
            # Unknown file type, print a message
            print 'Skipping %s' % pathname

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

if __name__ == '__main__':
    metadata = Element('root')
    walktree(sys.argv[1], metadata)
    print prettify(metadata)

