# -*- coding: utf-8 -*-
from plone.app.blob.field import BlobWrapper
from Products.CMFCore.CMFBTreeFolder import manage_addCMFBTreeFolder
from zipfile import  ZipFile
from plone.namedfile.utils import get_contenttype
import os
import io

def afterContentCreated(obj, event):
    if obj.package_content:
        content_hash = hash(obj.package_content)
        obj.package_signature = str(content_hash)
        manage_addCMFBTreeFolder(obj, str(content_hash))
        root_folder = getattr(obj, str(content_hash))
        extract_package_content(root_folder, obj.package_content)

def afterContentModified(obj, event):
    # Prevent looping while modifying object in this event
    if getattr(obj,'modified_in_progress',False):
        return
    setattr(obj, 'modified_in_progress',True)
    if obj.package_content:
        new_hash = hash(obj.package_content)
        print 'Old hash %s' % obj.package_signature
        print 'New hash %s' % new_hash
        if new_hash == obj.package_signature:
            return
        obj.manage_delObjects(obj.package_signature)
        obj.package_signature = str(new_hash)
        manage_addCMFBTreeFolder(obj, str(new_hash))
        root_folder = getattr(obj, str(new_hash))
        extract_package_content(root_folder, obj.package_content)
    setattr(obj, 'modified_in_progress', False)

def extract_package_content(root_folder, zip_blob):
    """
        Extract package content into ZOB Tree
    """
    zipfile = ZipFile(zip_blob.open('r'))
    parent_folders = {}
    for path in sorted(zipfile.namelist()):
        #skip path if it starts with underscore
        if path.startswith('_'):
            #TODO: replace underscoe in path and HTML source if possible
            continue
        if path.endswith('/'):
            # create directory
            path = path[:-1]
            foldername = path.split(os.sep)[-1]
            parent_folder_name = '/'.join(path.split(os.sep)[:-1])
            parent_folder = parent_folders[parent_folder_name] if parent_folder_name else root_folder
            manage_addCMFBTreeFolder(parent_folder, foldername)
            parent_folders[path] = getattr(parent_folder, foldername)
        else:
            # create file
            filename = path.split(os.sep)[-1]
            parent_folder_name = '/'.join(path.split(os.sep)[:-1])
            parent_folder = parent_folders[parent_folder_name] if parent_folder_name else root_folder
            data = zipfile.read(path)
            print get_contenttype(filename=filename)
            blob = BlobWrapper(get_contenttype(filename=filename))
            file_obj = blob.getBlob().open('w')
            file_obj.write(data)
            file_obj.close()
            blob.setFilename(filename)
            parent_folder._setObject(filename, blob)

