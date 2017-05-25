from dispatch.apps.api.serializers import ArticleSerializer, ImageSerializer, WidgetSerializer
from dispatch.apps.content.models import Article, Image

from dispatch.theme import ThemeManager
from dispatch.theme.exceptions import InvalidField, WidgetNotFound

class Field(object):
    """Base class for all widget fields"""

    _creation_counter = 0

    def __init__(self, label, many=False):
        self.label = label
        self.many = many

        if self.many:
            self.default = []
        else:
            self.default = None

        self._creation_counter = Field._creation_counter
        Field._creation_counter += 1

        if not isinstance(self.label, basestring):
            raise InvalidField('Label must be a string')

    def validate(self, data):
        """Validates the field data"""
        raise NotImplementedError

    def to_json(self, data):
        """Returns JSON representation of field data"""
        return {
            'label' : self.label,
            'data' : data
        }

    def prepare_data(self, data):
        """Prepares field data for use in a template"""
        return data

class CharField(Field):

    type = 'char'

    def validate(self, data):

        if not isinstance(data, basestring):
            raise InvalidField('%s data must be a string' % self.label)

        elif len(data) > 255:
            raise InvalidField('Max length for charfield data is 255')

class TextField(Field):

    type = 'text'

    def validate(self, data):
        if not isinstance(data, basestring):
            raise InvalidField('%s data must be a string' % self.label)

class ArticleField(Field):

    type = 'article'

    def validate(self, data):
        if self.many:
            if not isinstance(data, list) or not all([isinstance(id, int) for id in data]):
                raise InvalidField('Data must be list of integers')
        else:
            if not isinstance(data, int):
                raise InvalidField('Data must be an integer')

    def get_article(self, id):
        try:
            return Article.objects.get(pk=id)
        except Article.DoesNotExist:
            # TODO: better exception handling
            raise Article.DoesNotExist('Article does not exist')

    def get_article_json(self, id):
        article = self.get_article(id)
        serializer = ArticleSerializer(article)
        return serializer.data

    def to_json(self, data):

        def get_data():
            if not data:
                return self.default

            try:
                if self.many:
                    return map(self.get_article_json, data)
                else:
                    return self.get_article_json(data)
            except:
                return self.default

        return {
            'label': self.label,
            'data': get_data()
        }

    def prepare_data(self, data):
        if not data:
            return self.default

        if self.many:
            return map(self.get_article, data)
        else:
            return self.get_article(data)

class ImageField(Field):

    type = 'image'

    def validate(self, data):
        if self.many:
            if not isinstance(data, list) or not all([isinstance(id, int) for id in data]):
                raise InvalidField('Data must be list of integers')
        else:
            if not isinstance(data, int):
                raise InvalidField('Data must be an integer')

    def get_image(self, id):
        try:
            return Image.objects.get(pk=id)
        except Image.DoesNotExist:
            # TODO: better exception handling
            raise Image.DoesNotExist('Image does not exist')

    def get_image_json(self, id):
        image = self.get_image(id)
        serializer = ImageSerializer(image)
        return serializer.data

    def to_json(self, data):

        def get_data():
            if not data:
                return self.default

            try:
                if self.many:
                    return map(self.get_image_json, data)
                else:
                    return self.get_image_json(data)
            except:
                return self.default

        return {
            'label': self.label,
            'data': get_data()
        }

    def prepare_data(self, data):
        if self.many:
            return map(self.get_image, data)
        else:
            return self.get_image(data)

class WidgetField(Field):

    type = 'widget'

    def validate(self, data):
        if not isinstance(data, basestring):
            raise InvalidField('Data must be a string')

    def get_widget(self, id):
        try:
            return ThemeManager.Widgets.get(id)
        except WidgetNotFound:
            raise WidgetNotFound('Widget with id %s does not exist' % id)

    def get_widget_json(self, data):
        widget = self.get_widget(data['id'])
        widget.set_data(data['data'])
        serializer = WidgetSerializer(widget)
        return serializer.data

    def to_json(self, data):

        def get_data():
            if not data:
                return self.default

            return self.get_widget_json(data)

        return {
            'label': self.label,
            'data': get_data()
        }

    def prepare_data(self, data):
        widget = self.get_widget(data['id'])
        widget.set_data(data['data'])
        return widget
