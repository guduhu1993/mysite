from .models import Blog
from haystack import indexes


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    # 每个索引里面必须有且只能有一个字段为document=True
    text = indexes.CharField(document=True, use_template=True)
    '''
    document:指定了将模型类中的哪些字段建立索引
    use_template:在模板文件夹中创建文件夹指明具体的字段建立索引
    '''
    def get_model(self):
        return Blog

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
