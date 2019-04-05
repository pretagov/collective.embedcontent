# -*- coding: utf-8 -*-

from Products.CMFCore.CMFBTreeFolder import manage_addCMFBTreeFolder
from zipfile import  ZipFile
import os
import io

def afterContentCreated(obj, event):
    #manage_addCMFBTreeFolder(obj, id='plomino_documents')
    #for i in ['resources', 'scripts']:
    #    manage_addCMFBTreeFolder(obj, id=i)
    if obj.package_content:
        content_hash = hash(obj.package_content)
        obj.package_signature = content_hash
        root_folder = manage_addCMFBTreeFolder(obj, content_hash)
        extract_package_content(root_folder, obj.package_content)

def afterContentModified(obj, event):
    """
    """
    # Prevent looping while modifying object in this event
    if getattr(obj,'modified_in_progress',False):
        return
    setattr(obj, 'modified_in_progress',True)
    if obj.package_content:
        new_hash = hash(obj.package_content)
        if new_hash == obj.package_signature:
            return
        obj.manage_delObjects(obj.package_signature)
        obj.package_signature = new_hash
        root_folder = manage_addCMFBTreeFolder(obj, new_hash)
        extract_package_content(root_folder, obj.package_content)
    setattr(obj, 'modified_in_progress', False)

def extract_package_content(root_folder, zip_blob):
    zipfile = ZipFile(zip_blob.open('r'))
    import pdb
    pdb.set_trace()
    for f in zipfile.namelist():
        # get directory name from file
        dirname = os.path.splitext(f)[0]
        # create new directory
        print 'Make dir %s' % dirname
        # read inner zip file into bytes buffer
        content = io.BytesIO(zipfile.read(f))
        zip_file = ZipFile(content)
        for i in zip_file.namelist():
            print 'Extract %s' % i
