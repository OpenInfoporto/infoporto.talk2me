from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder


from infoporto.talk2me import MessageFactory as _
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


# Interface class; used to define content-type schema.

class IMailbox(form.Schema, IImageScaleTraversable):
    """
    Location for messages archive
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/mailbox.xml to define the content type.

    form.model("models/mailbox.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Mailbox(Container):
    grok.implements(IMailbox)

    # Add your class methods and properties here
    pass


# View class
# The view will automatically use a similarly named template in
# mailbox_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    """ sample view class """

    grok.context(IMailbox)
    grok.require('zope2.View')

    grok.name('view')

    # Add view methods here
    def getMyMessages(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        documents = catalog(portal_type='infoporto.talk2me.instantmsg', recipient=api.user.get_current().getUserName())
		
		# filter for only my message
        #import pdb; pdb.set_trace()
        msgs = []
        userGroups = []
       
        for gg in api.group.get_groups(username=api.user.get_current().getUserName()):
            if gg:
                userGroups.append(gg.getGroupName())

        print userGroups
        for dd in documents:
            if dd.getObject().recipient in userGroups:
                msgs.append(dd.getObject())

        return msgs

class ComposeView(BrowserView):
    template = ViewPageTemplateFile('mailbox_templates/compose.pt')
 
    def getRecipients(self):
        groups = []
        for gg in api.group.get_groups():
            groups.append({'gname': gg.getGroupName()})
            
        return groups
   
    def __call__(self):
        return self.template()


class SentMsgs(BrowserView):
    template = ViewPageTemplateFile('mailbox_templates/sent.pt')

    # Add view methods here
    def getMyMessages(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        documents = catalog(portal_type='infoporto.talk2me.instantmsg', author=api.user.get_current().getUserName())

        return [dd.getObject() for dd in documents]

    def __call__(self):
        return self.template()


class UnreadMsgs(BrowserView):
    
    def __call__(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        documents = catalog(portal_type='infoporto.talk2me.instantmsg', 
                            unread=True)

        msgs = []
        userGroups = []
    
        for gg in api.group.get_groups(username=api.user.get_current().getUserName()):
            if gg:
                userGroups.append(gg.getGroupName())

        print userGroups
        for dd in documents:
            if dd.getObject().recipient in userGroups:
                msgs.append(dd.getObject())

        return len(msgs)


class IncomingMsgs(BrowserView):
    template = ViewPageTemplateFile('mailbox_templates/incoming.pt')

    # Add view methods here
    def getMyMessages(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        documents = catalog(portal_type='infoporto.talk2me.instantmsg', recipient=api.user.get_current().getUserName())

        msgs = []
        userGroups = []

        for gg in api.group.get_groups(username=api.user.get_current().getUserName()):
            if gg:
                userGroups.append(gg.getGroupName())

        print userGroups
        for dd in documents:
            if dd.getObject().recipient in userGroups:
                msgs.append(dd.getObject())

        return msgs

    def __call__(self):
        return self.template()

