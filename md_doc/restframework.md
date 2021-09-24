

# Serialization

~~~python
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
serialization.data   // 序列化对象数据
serializer.is_valid() // True or False 查看序列化对象是否合法
JSONRenderer().render(serializer.data) // 把数据序列化转换为二进制
serializer.validated_data  // 
# OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
~~~

请注意 API 与使用表单的相似程度。当开始编写使用序列化程序的视图时，这种相似性应该变得更加明显。

我们还可以序列化查询集而不是模型实例。为此，我们只需`many=True`向序列化程序参数添加一个标志

`ModelSerializer`类不会快速根据所给模型生成序列化对象

```python
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data
// 把所有Snippet模型实例序列化
content = JSONRenderer().render(serializer.data)
// 反序列化
import io
stream = io.BytesIO(content)
data = JSONParser().parse(stream)
```

序列化数据的repr属性可以显示出其定义语句

```python
serializers.Serializer // 需要自己定义字段
serializers.Modelserializer
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
```

```python
// 理解：跨域不是服务器不给数据，也不是浏览器发现了跨域，不进行了请求。
// 解决：同源策略是浏览器的策略，和服务器没有关系，不过我们可以通过对服务器的响应头配置，让浏览器接收这次数据(后端解决办法)
@csrf_exempt
```

有时需要修改序列化器，控制序列化后的数据输出格式，有三种常用的方式

方法1：指定source

```python
class ArticleSerializer(serializers.ModelSerializer): 
	author = serializers.ReadOnlyField(source="author.username")
    status = serializers.ReadOnlyField(source="get_status_display")
    class Meta:
    	model = Article
        fields = '__all__' 
        read_only_fields = ('id', 'author', 'create_date')
```

但是这个方式用新的字段覆盖了原来模型的字段数值。这样反序列化时用户将不能再对文章发表状态进行修改（原来的status字段是可读可修改的）。一个更好的方式在ArticleSerializer新增一个为full_status的可读字段，这样相当于给序列化对象加了一个字段，而不是简单覆盖原本可读可写的字段。

~~~python
class ArticleSerializer(serializers.ModelSerializer): 
	author = serializers.ReadOnlyField(source="author.username")
    full_status = serializers.ReadOnlyField(source="get_status_display")
    class Meta:
    	model = Article
        fields = '__all__' 
        read_only_fields = ('id', 'author', 'create_date')
~~~

--------



方法2：使用SerializerMethodField自定义方法

~~~python
class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    status = serializers.ReadOnlyField(source="get_status_display")
    cn_status = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'author', 'create_date')

    def get_cn_status(self, obj):
        if obj.status == 'p':
            return "已发表"
        elif obj.status == 'd':
            return "草稿"
        else:
            return ''
~~~

cn_status指定了SerializerMethodField，它的值指向了get_字段名方法的值

不过需要注意的是SerializerMethodField通常用于显示模型中原本不存在的字段，类似可读字段，你不能通过反序列化对其直接进行修改。

------

方法3：使用嵌套序列化

我们文章中的author字段实际上对应的是一个User模型实例化后的对象，既不是一个整数id，也不是用户名这样一个简单字符串，显示更多用户对象信息呢? 其中一种解决方法是使用嵌套序列化器，如下所示：

~~~python
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer() # 设置required=False表示可以接受匿名用户
    status = serializers.ReadOnlyField(source="get_status_display")
    cn_status = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'author', 'create_date')

    def get_cn_status(self, obj):
        if obj.status == 'p':
            return "已发表"
        elif obj.status == 'd':
            return "草稿"
        else:
            return ''
~~~

此时发送GET请求展示文章列表资源是没问题的，但如果你希望发送POST请求到v1/articles/提交新文章你将会收到author字段是required的这样一个错误。为了使我们代码正确工作，我们还需要手动指定read_only=True这个选项。尽管我们在Meta选项已经指定了author为read_only_fields, 但使用嵌套序列化器时还需要重新指定一遍

还有一种方式，在Meta里加入depth = 1 ,这样写的非常简单，但是这样会显示出关联模型的所有字段，包含密码这样的隐藏字段

```
class ArticleSerializer(serializers.ModelSerializer): 
	# author = UserSerializer(read_only=True)    
	status = serializers.ReadOnlyField(source="get_status_display")
    cn_status = serializers.SerializerMethodField()
    class Meta:
    	model = Article
    	fields = '__all__'
        read_only_fields = ('id', 'author', 'create_date')
        depth = 1
        def get_cn_status(self, obj):
        	if obj.status == 'p':
            	return "已发表"
            elif obj.status == 'd':
            	return "草稿"
            else:
            	return ''
```

# Responds and Request

```python
request.POST  # Only handles form data.  Only works for 'POST' method.只能处理表单数据，也只能作用于POST方法
request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.可以处理任意数据，可以作用于post，put，patch方法
from rest_framework.decorators import api_view, APIView 
// api_view 用来装饰普通的视图函数
// APIView 视图函数直接继承即可
example:
@api_view(['GET', 'POST'])
@api_view(['GET', 'PUT', 'DELETE'])

```

有时候需要灵活的让响应连接到内容，让API接口增加对格式后缀的支持。可以在定义视图函数时增加format = None

```python
// 类似：
def snippet_list(request, format=None):
def snippet_detail(request, pk, format=None):
    
// 在urls.py 中添加

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)

//  使用Accept来控制我们返回的响应的格式
http http://127.0.0.1:8000/snippets/ Accept:application/json  # Request JSON
http http://127.0.0.1:8000/snippets/ Accept:text/html         # Request HTML
//  可以通过附加格式后缀
http http://127.0.0.1:8000/snippets.json  # JSON suffix
http http://127.0.0.1:8000/snippets.api   # Browsable API suffix
// 可以使用content-Type来控制发送请求的格式
http --form POST http://127.0.0.1:8000/snippets/ code="print(123)"
```

# Views based on class

```python
from rest_framework.views import APIView
class SnippetList(APIView):
    def get(self, request, format=None):
        pass
    def post(self, request, format=None):
        pass
    
```

对于创建、查询、更新、删除操作对于model支持的API视图都很相似，可以使用rest-framework中的mixin类来组合视图

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    
    
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

使用mixin类，可以使用较少的代码量，但是可以更进一步，使用generics：

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
```

**使用哪种CBV类更好?**

DRF提供了4种编写CBV类API的方式，哪种更好呢? 答案是各有利弊。小编个人认为大家只需掌握以下三种方式即可：

- 基础的API类：可读性最高，代码最多，灵活性最高。当你需要对的API行为进行个性化定制时，建议使用这种方式。
- 通用generics.*类：可读性好，代码适中，灵活性较高。当你需要对一个模型进行标准的增删查改全部或部分操作时建议使用这种方式。
- 使用视图集viewset: 可读性较低，代码最少，灵活性最低。当你需要对一个模型进行标准的增删查改的全部操作且不需定制API行为时建议使用这种方式
- 使用mixin类和generics一起使用效果是最差的，代码可读性差，写的也很复杂

# Authentication & Permissions

认证(Authentication)与权限(Permission)不是一回事。认证是通过用户提供的用户ID/密码组合或者Token来验证用户的身份。权限(Permission)的校验发生验证用户身份以后，是由系统根据分配权限确定用户可以访问何种资源以及对这种资源进行何种操作，这个过程也被称为授权(Authorization)。

## 数据验证

在反序列化数据时，在尝试访问经过验证的数据或保存对象实例之前，总是需要调用 `is_valid()`方法。如果发生任何验证错误，`.errors` 属性将包含表示结果错误消息的字典，如下所示

~~~python
serializer = CommentSerializer(data={'email': 'foobar', 'content': 'baz'})
serializer.is_valid() // 判断序列化对象是否合法
# False
serializer.errors
# {'email': [u'Enter a valid e-mail address.'], 'created': [u'This field is required.']}
~~~

### 引发无效数据的异常 (Raising an exception on invalid data)

`.is_valid()` 方法使用可选的 `raise_exception` 标志，如果存在验证错误，将会抛出 `serializers.ValidationError` 异常。

这些异常由 REST framework 提供的默认异常处理程序自动处理，默认情况下将返回 `HTTP 400 Bad Request` 响应。

```python
# Return a 400 response if the data was invalid.
serializer.is_valid(raise_exception=True)
```

### 字段级别验证 (Field-level validation)

您可以通过向您的 `Serializer` 子类中添加 `.validate_<field_name>` 方法来指定自定义字段级的验证。这些类似于 Django 表单中的 `.clean_<field_name>` 方法。这些方法采用单个参数，即需要验证的字段值。

您的 `validate_<field_name>` 方法应该返回已验证的值或抛出 `serializers.ValidationError` 异常。例如：

~~~python
from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)

    def validate_title(self, value):
        """
        Check that the article is about Django.
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Article is not about Django")
        return value
~~~

注意：如果序列化定义时声明了 `<field_name>` 的参数为 `required=False`，那么如果不包含该字段，则此验证步骤不会发生

### 对象级别验证 (Object-level validation)

要执行多个字段的验证，需要在序列化对象中定义名为 `.validate()` 的方法。此方法采用单个参数，该参数是字段值的字典。如果需要，它应该抛出 `ValidationError` 异常，或者只返回经过验证的值。例如：

~~~python
from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    start = serializers.DateTimeField()
    finish = serializers.DateTimeField()

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data
~~~

### **验证器 (Validators)**

序列化器上的各个字段都可以包含验证器，通过在字段实例上声明，例如：

~~~python
def multiple_of_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError('Not a multiple of ten')

class GameRecord(serializers.Serializer):
    score = IntegerField(validators=[multiple_of_ten])
~~~

DRF还提供了很多可重用的验证器，比如**UniqueValidator**,**UniqueTogetherValidator**等等。通过在内部 `Meta` 类上声明来包含这些验证器，如下所示。下例中会议房间号和日期的组合必须要是独一无二的。

~~~python
class EventSerializer(serializers.Serializer):
    name = serializers.CharField()
    room_number = serializers.IntegerField(choices=[101, 102, 103, 201])
    date = serializers.DateField()

    class Meta:
        # Each room only has one event per day.
        validators = UniqueTogetherValidator(
            queryset=Event.objects.all(),
            fields=['room_number', 'date']
        )  //  让room_number和date不重复
~~~

### 重写序列化对象的create和update方法

假设Profile模型与User模型是一对一的关系

当用户注册时我们希望把用户提交的数据分别存入User和Profile模型，这时我们就不得不重写序列化器自带的create方法了。下例演示了如何通过一个序列化器创建两个模型对象

~~~python
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'profile')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        # 除非应用程序正确地强制始终设置该字段，否则就应该抛出一个需要处理的`DoesNotExist`。
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.is_premium_member = profile_data.get(
            'is_premium_member',
            profile.is_premium_member
        )
        profile.has_support_contract = profile_data.get(
            'has_support_contract',
            profile.has_support_contract
         )
        profile.save()

        return instance
~~~

因为序列化器使用嵌套后，创建和更新的行为可能不明确

并且可能需要相关模型之间的复杂依赖关系，REST framework 3 要求你始终显式的编写这些方法。

默认的 `ModelSerializer` `.create()` 和 `.update()` 方法不包括对可写嵌套表示的支持，所以我们总是需要对create和update方法进行重写。

## 权限验证

任何用户包括匿名用户也可以对文章资源进行修改。比如当你访问单篇文章资源时，你不仅可以看到红色的delete按钮和修改文章内容的表单，而且可以在未登录的情况对它们进行操作。

传统的做法是给视图函数加上权限认证的装饰器：

@login_required和@permission_required这样的装饰器要求用户先登录或进行权限验证。在DRF中你不需要做，这是因为REST framework 包含许多默认权限类，我们可以用来限制谁可以访问给定的视图。在这种情况下，我们需要的是 `IsAuthenticatedOrReadOnly` 类，它将确保经过身份验证的请求获得读写访问权限，未经身份验证的请求将获得只读的权限。

~~~python
// 给视图函数加入以下内容即可添加权限验证
permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
~~~

### **常用DRF自带权限类**

除了`IsAuthenticatedOrReadOnly` 类，DRF自带的常用权限类还包括：

- IsAuthenticated类：仅限已经通过身份验证的用户访问；
- AllowAny类：允许任何用户访问；
- IsAdminUser类：仅限管理员访问；
- DjangoModelPermissions类：只有在用户经过身份验证并分配了相关模型权限时，才会获得授权访问相关模型。
- DjangoModelPermissionsOrReadOnly类：与前者类似，但可以给匿名用户访问API的可读权限。
- DjangoObjectPermissions类：只有在用户经过身份验证并分配了相关对象权限时，才会获得授权访问相关对象。通常与django-gaurdian联用实现对象级别的权限控制。

### 自定义权限

有时需要自己写一些权限类，比如自己写的博客才能修改、删除

~~~python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限只允许对象的创建者才能编辑它。"""
    def has_object_permission(self, request, view, obj):
        # 读取权限被允许用于任何请求，
        # 所以我们始终允许 GET，HEAD 或 OPTIONS 请求。
        if request.method in permissions.SAFE_METHODS:
            return True
        # 写入权限只允许给 article 的作者。
        return obj.author == request.user
~~~

在使用时在views.py引入该文件一般命名为permissions.py 然后在permission_classses = ()该元组中加入该类，可以添加多个

### **更多设置权限的方式**

在前面的案例中，我们都是在基于类的API视图里通过**permission_classes**属性设置的权限类。如果你有些权限是全局或全站通用的，你还可以在settings.py中使用 `DEFAULT_PERMISSION_CLASSES` 全局设置默认权限策略。

~~~python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
~~~

如果不设置默认设置为所有人都可以访问

```python
'DEFAULT_PERMISSION_CLASSES': (
   'rest_framework.permissions.AllowAny',
)
```

以上都是基于类的视图函数，如果写的是单纯的视图函数

用装饰器即可：

~~~python
@api_view(['GET'])
@permission_classes((IsAuthenticated, )) // 可以添加其他的permissions类，包括自定义的
def example_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
~~~

**注意**：当通过类属性或装饰器设置新的权限类时，您会告诉视图忽略配置文件上设置的默认列表。

## 认证

身份验证是将传入的请求对象(request)与一组标识凭据（例如请求来自的用户或其签名的令牌token）相关联的机制。REST framework 提供了一些开箱即用的身份验证方案，并且还允许你实现自定义方案。

DRF的每个认证方案实际上是一个类。你可以在视图中使用一个或多个认证方案类。REST framework 将尝试使用列表中的每个类进行身份验证，并使用成功完成验证的第一个类的返回的元组设置 `request.user`和`request.auth`。

用户通过认证后request.user返回Django的User实例，否则返回`AnonymousUser`的实例。request.auth通常为None。如果使用token认证，request.auth可以包含认证过的token。

注：认证一般发生在权限校验之前

### DRF自带了几种认证方式

Django REST Framework提供了如下几种认证方案:

- Session认证`SessionAuthentication`类：此认证方案使用Django的默认session后端进行身份验证。当客户端发送登录请求通过验证后，Django通过session将用户信息存储在服务器中保持用户的请求状态。**Session身份验证适用于与你的网站在相同的Session环境中运行的AJAX客户端** (注：这也是Session认证的最大弊端)一旦有多个服务器，session也只存在第一次连接的服务器中，不共享session。
- 基本认证`BasicAuthentication`类：此认证方案使用HTTP 基本认证，针对用户的用户名和密码进行认证。使用这种方式后浏览器会跳出登录框让用户输入用户名和密码认证。**基本认证通常只适用于测试**。
- 远程认证`RemoteUserAuthentication`类：**此认证方案为用户名不存在的用户自动创建用户实例。这个很少用，具体见文档**。
- Token认证`TokenAuthentication`类：该认证方案是DRF提供的使用简单的基于Token的HTTP认证方案。当客户端发送登录请求时，服务器便会生成一个Token并将此Token返回给客户端，作为客户端进行请求的一个标识以后客户端只需带上这个Token前来请求数据即可，无需再次带上用户名和密码。

**注意：如果你在生产环境下使用BasicAuthentication和`TokenAuthentication`认证，你必须确保你的API仅在`https`可用。**

### 如何使用认证方案

#### 1.使用全局配置

在setting中写入

```python
REST_FRAMEWORK = { 
'DEFAULT_AUTHENTICATION_CLASSES': (
'rest_framework.authentication.BasicAuthentication',
'rest_framework.authentication.SessionAuthentication',
)}
```

#### 2.在基于类的视图中使用

```
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
class ExampleView(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
```

#### 3.在视图函数中使用装饰器

~~~python
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication)) // 可以用元组写入多个
@permission_classes((IsAuthenticated,))
def example_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` 实例。
        'auth': unicode(request.auth),  # None
    }
    return Response(content)
~~~



# Relationships and  Hyperlinked APIs

~~~python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),  // 反向解析url
        'snippets': reverse('snippet-list', request=request, format=format)
    })
~~~

反向解析需要urls被命名

如果有分页的需求：

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

如果序列化对象需要一些模型中没有的字段，可以在序列化对象定义时使用serializers.SerializerMethodField()加入其他字段

~~~python
cn_status = serializers.SerializerMethodField()


 def get_cn_status(self, obj):
        if obj.status == 'p':
            return "已发表"
        elif obj.status == 'd':
            return "草稿"
        else:
            return ''
~~~

如果需要在序列化时更深一步显示可以在序列化对象定义中加入depth=1：

但是这个方式会把关联对象（model）的所有属性都列出来，包括例如密码这样需要隐藏的字段

```python
    class Meta: 
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'author', 'create_date')
        depth = 1
```

# ViewsSets and Routers

使用viewsSets可以不写很多方法， 比方说下面这个例子list操作和retrieve操作已经被封装在视图集这个类中

```python
from rest_framework import viewsets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

```python
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

使用action装饰器可以创建一个自定义的操作，而不仅仅局限在创建、更新、删除等常规操作

但是使用视图集来代替视图函数需要跟路由规则进行绑定：

```
from snippets.views import SnippetViewSet, UserViewSet, api_root
from rest_framework import renderers

snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
```

通过字典的形式绑定操作跟request的类型 key为request.method，value是视图类的操作方法

```
urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])
```

使用路由器

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
```

