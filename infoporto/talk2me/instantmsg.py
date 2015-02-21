from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Item

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder


from infoporto.talk2me import MessageFactory as _

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import datetime


# Interface class; used to define content-type schema.

class Iinstantmsg(form.Schema, IImageScaleTraversable):
    """
    Represent a single exchanged message
    """
    
    subject = schema.TextLine(
            title=_(u"Oggetto"),
        )

    body = schema.Text(
            title=_(u"Messaggio"),
        )

    author = schema.TextLine(
            title=_(u"Mittente")
        )

    recipient = schema.TextLine(
            title=_(u"Destinatario")
        )

    unread = schema.Bool(
            title=_(u"Non letto"),
            default=True
        )

    creation_date = schema.Datetime(
            title=_(u"Data ricezione"),
            default=datetime.datetime.now()
        )

    read_date = schema.Datetime(
            title=_(u"Letto il"),
            required=False
        )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class instantmsg(Item):
    grok.implements(Iinstantmsg)

    # Add your class methods and properties here
    pass


# View class
# The view will automatically use a similarly named template in
# instantmsg_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    """ sample view class """

    grok.context(Iinstantmsg)
    grok.require('zope2.View')

    grok.name('view')


class SendMsg(BrowserView):

    def __call__(self):
        container = api.content.get(path='/archivio/messaggi/')

        if not self.request.recipient:
            recipient = 'admin'
        else:
            recipient = self.request.recipient

        obj = api.content.create(
            type='infoporto.talk2me.instantmsg',
            title=self.request.subject,
            subject=self.request.subject,
            body=self.request.body,
            author=api.user.get_current().getUserName(),
            recipient=recipient,
            container=container)

        return "Sent."

class CountUnreadMsg(BrowserView):
    def __call__(self):
        container = api.content.get(path='/archivio/messaggi/')
        catalog = api.portal.get_tool(name='portal_catalog')
        documents = catalog(portal_type='infoporto.talk2me.instantmsg')
        return len(documents)


class MarkAsRead(BrowserView):
    def __call__(self):
        msg = api.content.get(UID=self.request.item)
        msg.unread = False
        return 'Letto.'

