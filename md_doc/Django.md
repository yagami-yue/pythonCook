## <font color='red'>优化orm</font>

### N+1问题

对于多对一关联（如老师和学科），我们可以使用`QuerySet`的用`select_related()`方法来加载关联对象；而对于多对多关联（如电商网站中的订单和商品），我们可以使用`prefetch_related()`方法来加载关联对象。

```python
queryset = Teacher.objects.all().select_related('subject')
queryset = Order.objects.all().prefetch_related('good')
```

---------

----------------------------------

### 查询模型过滤不需要的字段

```python
queryset = Teacher.objects.all().only('name', 'good_count', 'bad_count')  # 取需要的字段
queryset = Teacher.objects.all().defer('name', 'good_count', 'bad_count') # 过滤不需要的字段
queryset = Teacher.objects.values('name') # 只需要一个字段
queryset = Teacher.objects.values('subject').annotate(good=Avg('good_count'), bad=Avg('bad_count')) # 用annotate指定新字段=计算方式

```

## <font color='red'>返回数据</font>

```python
def show_subjects(request):
    queryset = Subject.objects.all()
    subjects = []
    for subject in queryset:
        subjects.append({
            'no': subject.no,
            'name': subject.name,
            'intro': subject.intro,
            'isHot': subject.is_hot
        })
    return JsonResponse(subjects, safe=False)
```

在前后端分离的开发模式下，后端需要为前端提供数据接口，通常返回JSON格式的数据，如果不使用rest frame work 可以使用Django自带的JsonResponse，第一个参数如果是字典，不需要写safe=False，如果是批量数据的列表则需要写safe=False

但是自己手动把模型对象整理成字典是不太便捷的一件事，所以可以安装<font color='red'>bpmappers</font>来解决这个问题，这个第三方的库本身也提供了对Django框架的支持

编写映射器：

```python
from bpmappers.djangomodel import ModelMapper

from poll2.models import Subject


class SubjectMapper(ModelMapper):
   
    class Meta:
        model = Subject
        exclude = ('字段1', '字段2') # 排除一些不需要显示的字段
```

修改视图函数

```python
def show_subjects(request):
    queryset = Subject.objects.all()
    subjects = []
    for subject in queryset:
        subjects.append(SubjectMapper(subject).as_dict())
    return JsonResponse(subjects, safe=False)
```

​                                        