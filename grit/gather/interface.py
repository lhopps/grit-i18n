#!/usr/bin/env python
# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

'''Interface for all gatherers.
'''


from grit import clique


class GathererBase(object):
  '''Interface for all gatherer implementations.  Subclasses must implement
  all methods that raise NotImplemented.'''

  def __init__(self):
    # A default uberclique that is local to this object.  Users can override
    # this with the uberclique they are using.
    self.uberclique = clique.UberClique()
    # Indicates whether this gatherer is a skeleton gatherer, in which case
    # we should not do some types of processing on the translateable bits.
    self.is_skeleton = False
    # Stores the grd node on which this gatherer is running. This allows
    # evaluating expressions.
    self.grd_node = None

  def SetAttributes(self, attrs):
    '''Sets node attributes used by the gatherer.

    By default, this does nothing.  If special handling is desired, it should be
    overridden by the child gatherer.

    Args:
      attrs: The mapping of node attributes.
    '''
    pass

  def SetDefines(self, defines):
    '''Sets global defines used by the gatherer.

    By default, this does nothing.  If special handling is desired, it should be
    overridden by the child gatherer.

    Args:
      defines: The mapping of define values.
    '''
    pass

  def SetGrdNode(self, node):
    '''Sets the grd node on which this gatherer is running.
    '''
    self.grd_node = node

  def SetUberClique(self, uberclique):
    '''Overrides the default uberclique so that cliques created by this object
    become part of the uberclique supplied by the user.
    '''
    self.uberclique = uberclique

  def SetSkeleton(self, is_skeleton):
    self.is_skeleton = is_skeleton

  def IsSkeleton(self):
    return self.is_skeleton

  def Parse(self):
    '''Parses the contents of what is being gathered.'''
    raise NotImplementedError()

  def GetData(self, lang, encoding):
    '''Returns the data to be added to the DataPack for this node or None if
    this node does not add a DataPack entry.
    '''
    return None

  def GetText(self):
    '''Returns the text of what is being gathered.'''
    raise NotImplementedError()

  def GetTextualIds(self):
    '''Returns the mnemonic IDs that need to be defined for the resource
    being gathered to compile correctly.'''
    return []

  def GetCliques(self):
    '''Returns the MessageClique objects for all translateable portions.'''
    return []

  def Translate(self, lang, pseudo_if_not_available=True,
                skeleton_gatherer=None, fallback_to_english=False):
    '''Returns the resource being gathered, with translateable portions filled
    with the translation for language 'lang'.

    If pseudo_if_not_available is true, a pseudotranslation will be used for any
    message that doesn't have a real translation available.

    If no translation is available and pseudo_if_not_available is false,
    fallback_to_english controls the behavior.  If it is false, throw an error.
    If it is true, use the English version of the message as its own
    "translation".

    If skeleton_gatherer is specified, the translation will use the nontranslateable
    parts from the gatherer 'skeleton_gatherer', which must be of the same type
    as 'self'.

    If fallback_to_english

    Args:
      lang: 'en'
      pseudo_if_not_available: True | False
      skeleton_gatherer: other_gatherer
      fallback_to_english: True | False

    Return:
      e.g. 'ID_THIS_SECTION TYPE\n...BEGIN\n  "Translated message"\n......\nEND'

    Raises:
      grit.exception.NotReady() if used before Parse() has been successfully
      called.
      grit.exception.NoSuchTranslation() if 'pseudo_if_not_available' and
      fallback_to_english are both false and there is no translation for the
      requested language.
    '''
    raise NotImplementedError()

  @staticmethod
  def FromFile(rc_file, extkey=None, encoding = 'cp1252'):
    '''Loads the resource from the file 'rc_file'.  Optionally an external key
    (which gets passed to the gatherer's constructor) can be specified.

    If 'rc_file' is a filename, it will be opened for reading using 'encoding'.
    Otherwise the 'encoding' parameter is ignored.

    Args:
      rc_file: file('') | 'filename.rc'
      extkey: e.g. 'ID_MY_DIALOG'
      encoding: 'utf-8'

    Return:
      grit.gather.interface.GathererBase subclass
    '''
    raise NotImplementedError()

  def SubstituteMessages(self, substituter):
    '''Applies substitutions to all messages in the gatherer.

    Args:
      substituter: a grit.util.Substituter object.
    '''
    pass

