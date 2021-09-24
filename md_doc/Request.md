# Request

## .data

`request.data`返回请求正文的解析内容。这类似于标准`request.POST`和`request.FILES`属性，除了：

- 它包括所有解析的内容，包括*文件和非文件*输入。
- 它支持解析除 之外的 HTTP 方法的内容`POST`，这意味着您可以访问`PUT`和`PATCH`请求的内容。
- 它支持REST框架灵活的请求解析，而不仅仅是支持表单数据。例如，您可以像处理传入的表单数据样处理传入的Json数据。

## .query_params

`request.query_params`是更正确命名的同义词`request.GET`。

为了在您的代码中清晰起见，我们建议使用`request.query_params`Django 的标准`request.GET`. 这样做将有助于使您的代码库更加正确和明显 - 任何 HTTP 方法类型都可能包含查询参数，而不仅仅是`GET`请求

## .parsers

在`APIView`类或`@api_view`装饰将确保这个属性被自动设置为列表`Parser`实例的基础上，`parser_classes`对视图设置或基于该`DEFAULT_PARSER_CLASSES`设置。

您通常不需要访问此属性。

------

**注意：**如果客户端发送格式错误的内容，则访问`request.data`可能会引发`ParseError`. 默认情况下，REST 框架的`APIView`类或`@api_view`装饰器将捕获错误并返回`400 Bad Request`响应。

如果客户端发送具有无法解析的内容类型的请求，`UnsupportedMediaType`则会引发异常，默认情况下将被捕获并返回`415 Unsupported Media Type`响应

## .user

`request.user`通常返回 的实例`django.contrib.auth.models.User`，尽管行为取决于所使用的身份验证策略。

如果请求未经身份验证，则 的默认值`request.user`是 的实例`django.contrib.auth.models.AnonymousUser`。

## .auth

`request.auth`返回任何额外的身份验证上下文。的确切行为`request.auth`取决于所使用的身份验证策略，但它通常可能是对请求进行身份验证所依据的令牌实例。

如果该请求是未认证的，或者如果没有附加上下文存在时，默认值`request.auth`是`None`。

## .method

`request.method`返回请求的 HTTP 方法的**大写**字符串表示形式。

基于浏览器的`PUT`，`PATCH`而`DELETE`形式是透明的支持。

## .content_type

`request.content_type`, 返回表示 HTTP 请求正文的媒体类型的字符串对象，如果未提供媒体类型，则返回空字符串。

您通常不需要直接访问请求的内容类型，因为您通常会依赖 REST 框架的默认请求解析行为。

如果您确实需要访问请求的内容类型，您应该`.content_type`优先使用属性而不是使用`request.META.get('HTTP_CONTENT_TYPE')`，因为它为基于浏览器的非表单内容提供透明支持。

# Response

参数：

- `data`：响应的序列化数据

- `status`：响应的状态代码。默认为 200

- `template_name`：`HTMLRenderer`选择时使用的模板名称

- `headers`：在响应中使用的 HTTP 标头字典

- `content_type`：响应的内容类型。通常，这将由内容协商确定的渲染器自动设置，但在某些情况下，您可能需要明确指定内容类型

- `content`：响应的呈现内容。该`.render()`方法必须在`.content`可以访问之前被调用

  