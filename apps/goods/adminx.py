import xadmin
from xadmin import views

from . import models





class BaseSetting(object):
    """xadmin的基本配置"""
    # enable_themes = True  # 开启主题切换功能
    use_bootswatch = True  # 设置为True才能查看到主题


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "运营管理系统"  # 设置站点标题
    site_footer = "集团有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)


class GoodsAdmin(object):
    list_display = ['id', 'title', 'sell_price', 'stock', 'sales', 'content']
    model_icon = 'fa fa-gift'
    search_fields = ['id', 'title']
    list_filter = ['category']
    list_editable = ['sell_price', 'stock']
    show_bookmarks = True
    show_detail_fields = ['title']


class BrandAdmin(object):
    """品牌管理"""


def save_models(self):
    """新增或修改数据"""
    obj = self.new_obj
    obj.save()
    print('------save_models------')


def delete_model(self):
    """删除一条数据"""
    obj = self.obj
    obj.delete()
    print('------delete_model------')


xadmin.site.register(models.Goods, GoodsAdmin)
xadmin.site.register(models.GoodsCategory)
