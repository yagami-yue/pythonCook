## 基础Python多进程

~~~python
from multiprocessing import Process
from os import getpid
from random import randint
from time import time, sleep


def download_task(filename):
    print('启动下载进程，进程号[%d].' % getpid())
    print('开始下载%s...' % filename)
    time_to_download = randint(5, 10)
    sleep(time_to_download)
    print('%s下载完成! 耗费了%d秒' % (filename, time_to_download))


def main():
    start = time()
    p1 = Process(target=download_task, args=('Python从入门到住院.pdf', ))
    p1.start()
    p2 = Process(target=download_task, args=('Peking Hot.avi', ))
    p2.start()
    p1.join()
    p2.join()
    end = time()
    print('总共耗费了%.2f秒.' % (end - start))


if __name__ == '__main__':
    main()
~~~

<font color='red'>Process的start方法用来启动进程，而join方法表示等待进程执行结束</font>

~~~python
from multiprocessing import Process
from time import sleep

counter = 0


def sub_task(string):
    global counter
    while counter < 10:
        print(string, end='', flush=True)
        counter += 1
        sleep(0.01)

        
def main():
    Process(target=sub_task, args=('Ping', )).start()
    Process(target=sub_task, args=('Pong', )).start()


if __name__ == '__main__':
    main()
~~~

上述代码希望2个进程一共输出10个，ping or pong，但是实际上一共输出了20次，因为多进程中通过global无法让2个进程间共享变量，因为进程有独立的内存空间，如果希望同步变量的值需要使用multiprocessing的Queue的类来共享变量

<font color='red'>queue可以被多个进程共享，底层通过管道和信号量机制来实现</font>

~~~python
q = multiprocessing.Queue()
# q常用的方法有put，get，empty
q.put() # 队列中新增元素，block为True，元素为块状
q.get() # 获取队列的一个元素，FIFO，获取后队列元素-1
q.empty() # 判断队列是否为空 t or f


# 想要实现输出10次ping or pong的代码如下
from multiprocessing import Process, Queue
from time import sleep


def sub_task(q, string):
    while True:
        if not q.empty():
            counter = int(q.get())
            while counter < 10:
                print(string, flush=True)
                q.put(str(counter + 1))
                sleep(0.01)
                counter = int(q.get())
            q.put('10')
            break


def main():
    q = Queue()
    q.put('0')
    p1 = Process(target=sub_task, args=(q, 'Ping'))
    p2 = Process(target=sub_task, args=(q, 'Pong'))
    p1.start()
    p2.start()

    # Process(target=sub_task, args=(q, 'Pong')).start()


if __name__ == '__main__':
    main()
~~~



## 基础Python多线程

python的多线程主要通过threading模块来实现

~~~python
from random import randint
from threading import Thread
from time import time, sleep


def download(filename):
    print('开始下载%s...' % filename)
    time_to_download = randint(5, 10)
    sleep(time_to_download)
    print('%s下载完成! 耗费了%d秒' % (filename, time_to_download))


def main():
    start = time()
    t1 = Thread(target=download, args=('Python从入门到住院.pdf',))
    t1.start()
    t2 = Thread(target=download, args=('Peking Hot.avi',))
    t2.start()
    t1.join()
    t2.join()
    end = time()
    print('总共耗费了%.3f秒' % (end - start))


if __name__ == '__main__':
    main()
# api跟multiprocessing差不多
~~~

可以通过threading模块直接创建线程，但是也可以继承Thread，来自定义线程类，然后创建线程对象并且启动

~~~python
from random import randint
from threading import Thread
from time import time, sleep


class DownloadTask(Thread):

    def __init__(self, filename):
        super().__init__()
        self._filename = filename

    def run(self):
        print('开始下载%s...' % self._filename)
        time_to_download = randint(5, 10)
        sleep(time_to_download)
        print('%s下载完成! 耗费了%d秒' % (self._filename, time_to_download))


def main():
    start = time()
    t1 = DownloadTask('Python从入门到住院.pdf')
    t1.start()
    t2 = DownloadTask('Peking Hot.avi')
    t2.start()
    t1.join()
    t2.join()
    end = time()
    print('总共耗费了%.2f秒.' % (end - start))


if __name__ == '__main__':
    main()
~~~

​        多线程可以共享进程的内存空间，实现多个线程间的通信相对简单，大家能想到的最直接的方式就是设置一个全局变量，多个线程共享这个全局变量，但是多个线程共享资源（临界资源）需要加上保护，否则会造成错误的结果。这时候需要加锁来限制访问临界资源的线程。但是基于Cpython的python程序并不能发挥CPU多核的优势，<font color='red'>因为GIL（全局解释器锁），GIL不是python的特性</font>，它是Cpython解释器实现所引入的一个概念，Jpython解释器就没有GIL，然而因为Cpython是大部分情况下的默认Python执行环境，GIL是为了防止多线程并发执行机器码Mutex，任何线程执行前需要或者这个锁，然后执行100条字节码，解释器自动释放GIL，让别的线程有机会执行 慢慢的这种实现方式被发现是蛋疼且低效的。在CPython中，每一个Python线程执行前都需要去获得GIL锁 ，获得该锁的线程才可以执行，没有获得的只能等待 ，当具有GIL锁的线程运行完成后，其他等待的线程就会去争夺GIL锁，这就造成了，在Python中使用多线程，但同一时刻下依旧只有一个线程在运行 ，所以Python多线程其实并不是「并行」的，而是「并发」

​        但当大家试图去拆分和去除GIL的时候，发现大量库代码开发者已经重度依赖GIL而非常难以去除了。有多难？做个类比，像MySQL这样的“小项目”为了把Buffer Pool Mutex这把大锁拆分成各个小锁也花了从5.5到5.6再到5.7多个大版为期近5年的时间，本且仍在继续。MySQL这个背后有公司支持且有固定开发团队的产品走的如此艰难，那又更何况Python这样核心开发和代码贡献者高度社区化的团队呢？

​		GIL基本让python是一个单线程程序，现在比较好的解决方案有如下：

1.<font color='red'>用multiprocess替代Thread</font>

multiprocess库的出现很大程度上是为了弥补thread库因为GIL而低效的缺陷。它完整的复制了一套thread所提供的接口方便迁移。唯一的不同就是它使用了多进程而不是多线程。每个进程有自己的独立的GIL，因此也不会出现进程之间的GIL争抢。

当然multiprocess也不是万能良药。它的引入会增加程序实现时线程间数据通讯和同步的困难。就拿计数器来举例子，如果我们要多个线程累加同一个变量，对于thread来说，申明一个global变量，用thread.Lock的context包裹住三行就搞定了。而multiprocess由于进程之间无法看到对方的数据，只能通过在主线程申明一个Queue，put再get或者用share memory的方法。这个额外的实现成本使得本来就非常痛苦的多线程程序编码，变得更加痛苦了。

2.<font color='red'>用其他解析器</font>

之前也提到了既然GIL只是CPython的产物，那么其他解析器是不是更好呢？没错，像JPython和IronPython这样的解析器由于实现语言的特性，他们不需要GIL的帮助。然而由于用了Java/C#用于解析器实现，他们也失去了利用社区众多C语言模块有用特性的机会。所以这些解析器也因此一直都比较小众。毕竟功能和性能大家在初期都会选择前者

<font color='red'>有了多进程后，大部分程序都可以通过多进程的方式绕过GIL ，但如果依旧不满足，就需要使用C/C++来实现这部分代码，并生成对应的so或dll文件，再通过Python的ctypes将其调用起来 ，Python中很多对计算性能有较高要求的库都采用了这种方式，如Numpy、Pandas等等 。如果你对程序的性能要求的特别严格，此时更好的方法是选择其他语言</font>





## 网络编程

requests是一个基于HTTP协议来使用的网络第三方库，原生库，有效避免了安全缺陷、冗余代码以及重复写代码

### TCP套接字

TCP套接字就是使用TCP协议提供的传输服务来实现网络通信的编程接口。在Python中可以通过创建socket对象并指定type属性为SOCK_STREAM来使用TCP套接字。由于一台主机可能拥有多个IP地址，而且很有可能会配置多个不同的服务，所以作为服务器端的程序，需要在创建套接字对象后将其绑定到指定的IP地址和端口上。这里的端口并不是物理设备而是对IP地址的扩展，用于区分不同的服务，

~~~python
# 定义一个套接字监听端口，返回当前时间
from socket import socket, SOCK_STREAM, AF_INET
from datetime import datetime


def main():
    # 1.创建套接字对象并指定使用哪种传输服务
    # family=AF_INET - IPv4地址
    # family=AF_INET6 - IPv6地址
    # type=SOCK_STREAM - TCP套接字
    # type=SOCK_DGRAM - UDP套接字
    # type=SOCK_RAW - 原始套接字
    server = socket(family=AF_INET, type=SOCK_STREAM)
    # 2.绑定IP地址和端口(端口用于区分不同的服务)
    # 同一时间在同一个端口上只能绑定一个服务否则报错
    server.bind(('192.168.91.25', 6789))
    # 3.开启监听 - 监听客户端连接到服务器
    # 参数512可以理解为连接队列的大小,至多接受512个请求
    server.listen(512)
    print('服务器启动开始监听...')
    while True:
        # 4.通过循环接收客户端的连接并作出相应的处理(提供服务)
        # accept方法是一个阻塞方法如果没有客户端连接到服务器代码不会向下执行
        # accept方法返回一个元组其中的第一个元素是客户端对象
        # 第二个元素是连接到服务器的客户端的地址(由IP和端口两部分构成)
        client, addr = server.accept()
        print(str(addr) + '连接到了服务器.')
        # 5.发送数据
        client.send(str(datetime.now()).encode('utf-8'))
        # 6.断开连接
        client.close()


if __name__ == '__main__':
    main()
~~~

上述的服务器端的代码没有使用多线程或者异步I/O的处理方式，这也就是说当服务器与一个客户端处于通信状态的时候，其他客户端会排队等待。

<font color='red'>多线程的服务器代码如下，服务器会向连接的客户端发送一张图片：</font>

~~~python
from socket import socket, SOCK_STREAM, AF_INET
from base64 import b64encode
from json import dumps
from threading import Thread


def main():
    
    # 自定义线程类
    class FileTransferHandler(Thread):

        def __init__(self, cclient):
            super().__init__()
            self.cclient = cclient

        def run(self):
            my_dict = {}
            my_dict['filename'] = 'guido.jpg'
            # JSON是纯文本不能携带二进制数据
            # 所以图片的二进制数据要处理成base64编码
            my_dict['filedata'] = data
            # 通过dumps函数将字典处理成JSON字符串
            json_str = dumps(my_dict)
            # 发送JSON字符串
            self.cclient.send(json_str.encode('utf-8'))
            self.cclient.close()

    # 1.创建套接字对象并指定使用哪种传输服务
    server = socket()
    # 2.绑定IP地址和端口(区分不同的服务)
    server.bind(('192.168.1.2', 5566))
    # 3.开启监听 - 监听客户端连接到服务器
    server.listen(512)
    print('服务器启动开始监听...')
    with open('guido.jpg', 'rb') as f:
        # 将二进制数据处理成base64再解码成字符串
        data = b64encode(f.read()).decode('utf-8')
    while True:
        client, addr = server.accept()
        # 启动一个线程来处理客户端的请求
        FileTransferHandler(client).start()


if __name__ == '__main__':
    main()
~~~

### UDP套接字

TCP和UDP都是提供端到端传输服务的协议，二者的差别就如同打电话和发短信的区别，后者不对传输的可靠性和可达性做出任何承诺从而避免了TCP中握手和重传的开销，所以在强调性能和而不是数据完整性的场景中（例如传输网络音视频数据），UDP可能是更好的选择。可能大家会注意到一个现象，就是在观看网络视频时，有时会出现卡顿，有时会出现花屏，这无非就是部分数据传丢或传错造成的,可以在构建socket的时候指定

~~~python
server = socket(family=AF_INET, type=SOCK_DGRAM) # UDP套接字 dgram=数据报
~~~

### QQ邮件自动发送

~~~python
# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:smtp.py
@time:2021/09/02
"""
# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header


class Mail:
    def __init__(self):
        # 第三方 SMTP 服务
        self.mail_host = "smtp.qq.com"  # 设置服务器:这个是qq邮箱服务器，直接复制就可以
        self.mail_pass = "**********"  # 获取的授权码
        self.sender = '********@qq.com'  # 你的邮箱地址
        self.receivers = ['******@qq.com',  ]  # 收件人的邮箱地址，可设置为你的QQ邮箱或者其他邮箱，可多个，经过测试谷歌邮箱不生效

    def send(self):

        content = 'smtp test'  # 正文
        message = MIMEText(content, 'plain', 'utf-8')
		receivers = ','.join(self.receivers)
        message['From'] = formataddr(('yagami_yue', self.sender)) # 
        message['To'] = formataddr(('sdsdsdsdsdsds', receivers)) # 前面参数不生效，随便写
        subject = 'test'  # 发送的主题，可自由填写
        message['Subject'] = subject
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            print('邮件发送成功')
        except smtplib.SMTPException as e:
            print('邮件发送失败')


if __name__ == '__main__':
    mail = Mail()
    mail.send()



if __name__ == '__main__':
    mail = Mail()
    mail.send()
~~~

![image-20210902164658228](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20210902164658228.png)

授权码在qq邮箱的设置->账户里获取

## 进阶

### 函数的使用方式

- 将函数视为“一等公民”

  - 函数可以赋值给变量
  - 函数可以作为函数的参数
  - 函数可以作为函数的返回值

- 高阶函数的用法（`filter`、`map`以及它们的替代品）

  ```
  items1 = list(map(lambda x: x ** 2, filter(lambda x: x % 2, range(1, 10))))
  items2 = [x ** 2 for x in range(1, 10) if x % 2]
  ```

- 位置参数、可变参数、关键字参数、命名关键字参数

- 参数的元信息（代码可读性问题）

- 匿名函数和内联函数的用法（`lambda`函数）

- 闭包和作用域问题

  - Python搜索变量的LEGB顺序（Local >>> Embedded >>> Global >>> Built-in）

  - `global`和`nonlocal`关键字的作用

    `global`：声明或定义全局变量（要么直接使用现有的全局作用域的变量，要么定义一个变量放到全局作用域）。

    `nonlocal`：声明使用嵌套作用域的变量（嵌套作用域必须存在该变量，否则报错）。

- 装饰器函数（使用装饰器和取消装饰器）

  例子：输出函数执行时间的装饰器。

  ```
  def record_time(func):
      """自定义装饰函数的装饰器"""
      
      @wraps(func)
      def wrapper(*args, **kwargs):
          start = time()
          result = func(*args, **kwargs)
          print(f'{func.__name__}: {time() - start}秒')
          return result
          
      return wrapper
  ```

  如果装饰器不希望跟`print`函数耦合，可以编写可以参数化的装饰器。

  ```python
  from functools import wraps
  from time import time
  
  
  def record(output):
      """可以参数化的装饰器"""
  	
  	def decorate(func):
  		
  		@wraps(func)
  		def wrapper(*args, **kwargs):
  			start = time()
  			result = func(*args, **kwargs)
  			output(func.__name__, time() - start)
  			return result
              
  		return wrapper
  	
  	return decorate
  ```

  ```python
  from functools import wraps
  from time import time
  
  
  class Record():
      """通过定义类的方式定义装饰器"""
  
      def __init__(self, output):
          self.output = output
  
      def __call__(self, func):
  
          @wraps(func)
          def wrapper(*args, **kwargs):
              start = time()
              result = func(*args, **kwargs)
              self.output(func.__name__, time() - start)
              return result
  
          return wrapper
  ```

  > **说明**：由于对带装饰功能的函数添加了@wraps装饰器，可以通过`func.__wrapped__`方式获得被装饰之前的函数或类来取消装饰器的作用。

  例子：用装饰器来实现单例模式。

  ```python
  from functools import wraps
  
  
  def singleton(cls):
      """装饰类的装饰器"""
      instances = {}
  
      @wraps(cls)
      def wrapper(*args, **kwargs):
          if cls not in instances:
              instances[cls] = cls(*args, **kwargs)
          return instances[cls]
  
      return wrapper
  
  
  @singleton
  class President:
      """总统(单例类)"""
      pass
  ```

  > **提示**：上面的代码中用到了闭包（closure），不知道你是否已经意识到了。还没有一个小问题就是，上面的代码并没有实现线程安全的单例，如果要实现线程安全的单例应该怎么做呢？

  线程安全的单例装饰器。

  ```python
  from functools import wraps
  from threading import RLock
  
  
  def singleton(cls):
      """线程安全的单例装饰器"""
      instances = {}
      locker = RLock()
  
      @wraps(cls)
      def wrapper(*args, **kwargs):
          if cls not in instances:
              with locker:
                  if cls not in instances:
                      instances[cls] = cls(*args, **kwargs)
          return instances[cls]
  
      return wrapper
  ```

  > **提示**：上面的代码用到了`with`上下文语法来进行锁操作，因为锁对象本身就是上下文管理器对象（支持`__enter__`和`__exit__`魔术方法）。在`wrapper`函数中，我们先做了一次不带锁的检查，然后再做带锁的检查，这样做比直接加锁检查性能要更好，如果对象已经创建就没有必须再去加锁而是直接返回该对象就可以了。

### 垃圾回收

- 对象的复制（深复制/深拷贝/深度克隆和浅复制/浅拷贝/影子克隆）
- 垃圾回收、循环引用和弱引用

Python使用了自动化内存管理，这种管理机制以**引用计数**为基础，同时也引入了**标记-清除**和**分代收集**两种机制为辅的策略。

```c
typedef struct _object {
    /* 引用计数 */
    int ob_refcnt;
    /* 对象指针 */
    struct _typeobject *ob_type;
} PyObject;
```

```c
/* 增加引用计数的宏定义 */
#define Py_INCREF(op)   ((op)->ob_refcnt++)
/* 减少引用计数的宏定义 */
#define Py_DECREF(op) \ //减少计数
    if (--(op)->ob_refcnt != 0) \
        ; \
    else \
        __Py_Dealloc((PyObject *)(op))
```

导致引用计数+1的情况：

- 对象被创建，例如`a = 23`
- 对象被引用，例如`b = a`
- 对象被作为参数，传入到一个函数中，例如`f(a)`
- 对象作为一个元素，存储在容器中，例如`list1 = [a, a]`

导致引用计数-1的情况：

- 对象的别名被显式销毁，例如`del a`
- 对象的别名被赋予新的对象，例如`a = 24`
- 一个对象离开它的作用域，例如f函数执行完毕时，f函数中的局部变量（全局变量不会）
- 对象所在的容器被销毁，或从容器中删除对象

引用计数可能会导致循环引用问题，而循环引用会导致内存泄露，如下面的代码所示。为了解决这个问题，Python中引入了“标记-清除”和“分代收集”。在创建一个对象的时候，对象被放在第一代中，如果在第一代的垃圾检查中对象存活了下来，该对象就会被放到第二代中，同理在第二代的垃圾检查中对象存活下来，该对象就会被放到第三代中。

```python
# 循环引用会导致内存泄露 - Python除了引用技术还引入了标记清理和分代回收
# 在Python 3.6以前如果重写__del__魔术方法会导致循环引用处理失效
# 如果不想造成循环引用可以使用弱引用
list1 = []
list2 = [] 
list1.append(list2)
list2.append(list1)
```

以下情况会导致垃圾回收：

- 调用`gc.collect()`
- `gc`模块的计数器达到阀值
- 程序退出

如果循环引用中两个对象都定义了`__del__`方法，`gc`模块不会销毁这些不可达对象，因为gc模块不知道应该先调用哪个对象的`__del__`方法，这个问题在Python 3.6中得到了解决。

也可以通过`weakref`模块构造弱引用的方式来解决循环引用的问题。

### 单例模式

```python
from functools import wraps


def singleton(cls):
    """装饰类的装饰器"""
    instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


@singleton
class President:
    """总统(单例类)"""
    pass
```

> **提示**：上面的代码中用到了闭包（closure），不知道你是否已经意识到了。还没有一个小问题就是，上面的代码并没有实现线程安全的单例，如果要实现线程安全的单例应该怎么做呢？

~~~python
from functools import wraps
from threading import RLock


def singleton(cls):
    """线程安全的单例装饰器"""
    instances = {}
    locker = RLock()

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            with locker:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
~~~

### 迭代器和生成器

- 迭代器是实现了迭代器协议的对象。

  - Python中没有像`protocol`或`interface`这样的定义协议的关键字。
  - Python中用魔术方法表示协议。
  - `__iter__`和`__next__`魔术方法就是迭代器协议。

  ```python
  class Fib(object):
      """迭代器"""
      
      def __init__(self, num):
          self.num = num
          self.a, self.b = 0, 1
          self.idx = 0
     
      def __iter__(self):
          return self
  
      def __next__(self):
          if self.idx < self.num:
              self.a, self.b = self.b, self.a + self.b
              self.idx += 1
              return self.a
          raise StopIteration()
  ```

- 生成器是语法简化版的迭代器。

  ```python
  def fib(num):
      """生成器"""
      a, b = 0, 1
      for _ in range(num):
          a, b = b, a + b
          yield a
  ```

- 生成器进化为协程。

  生成器对象可以使用`send()`方法发送数据，发送的数据会成为生成器函数中通过`yield`表达式获得的值。这样，生成器就可以作为协程使用，协程简单的说就是可以相互协作的子程序。

  ```python
  def calc_avg():
      """流式计算平均值"""
      total, counter = 0, 0
      avg_value = None
      while True:
          value = yield avg_value
          total, counter = total + value, counter + 1
          avg_value = total / counter
  
  
  gen = calc_avg()
  next(gen)  # 启动携程,启动了才能发送值开始运算
  print(gen.send(10))
  print(gen.send(20))
  print(gen.send(30))
  ```

### 并发编程

python实现并发编程的三种方案：多线程、多进程、异步I/O

并发编程的好处自安于可以提升程序的执行效率以及改善用户体验；坏处在于并发的程序不容易开发和调试，同时对于其他程序来说它并不友好

#### 多线程

python有GIL来防止多个线程同时执行本地字节码，这个锁对于CPython来说是必须的，因为CPython的内存管理不是线程安全的，因为GIL的存在多线程不能完全发挥CPU多核特性

```python
"""
面试题：进程和线程的区别和联系？
进程 - 操作系统分配内存的基本单位 - 一个进程可以包含一个或多个线程
线程 - 操作系统分配CPU的基本单位
并发编程（concurrent programming）
1. 提升执行性能 - 让程序中没有因果关系的部分可以并发的执行
2. 改善用户体验 - 让耗时间的操作不会造成程序的假死
"""
import glob
import os
import threading

from PIL import Image

PREFIX = 'thumbnails'


def generate_thumbnail(infile, size, format='PNG'):
    """生成指定图片文件的缩略图"""
	file, ext = os.path.splitext(infile)
	file = file[file.rfind('/') + 1:]
	outfile = f'{PREFIX}/{file}_{size[0]}_{size[1]}.{ext}'
	img = Image.open(infile)
	img.thumbnail(size, Image.ANTIALIAS)
	img.save(outfile, format)


def main():
    """主函数"""
	if not os.path.exists(PREFIX):
		os.mkdir(PREFIX)
	for infile in glob.glob('images/*.png'):   # glob.glob 返回当前路径下所有符合规则的文件，还有一个glob.iglob的函数有着一样的功能，但是返回一个迭代器，对于内存比较友好
        for size in (32, 64, 128):
            # 创建并启动线程
			threading.Thread(
				target=generate_thumbnail, 
				args=(infile, (size, size))
			).start()
			

if __name__ == '__main__':
	main()
```

多个线程竞争资源的情况

```python
"""
多线程程序如果没有竞争资源处理起来通常也比较简单
当多个线程竞争临界资源的时候如果缺乏必要的保护措施就会导致数据错乱
说明：临界资源就是被多个线程竞争的资源
"""
import time
import threading

from concurrent.futures import ThreadPoolExecutor


class Account(object):
    """银行账户"""

    def __init__(self):
        self.balance = 0.0
        self.lock = threading.Lock()

    def deposit(self, money):
        # 通过锁保护临界资源
        with self.lock:
            new_balance = self.balance + money
            time.sleep(0.001)
            self.balance = new_balance


class AddMoneyThread(threading.Thread):
    """自定义线程类"""

    def __init__(self, account, money):
        self.account = account
        self.money = money
        # 自定义线程的初始化方法中必须调用父类的初始化方法
        super().__init__()

    def run(self):
        # 线程启动之后要执行的操作
        self.account.deposit(self.money)

def main():
    """主函数"""
    account = Account()
    # 创建线程池
    pool = ThreadPoolExecutor(max_workers=10)
    futures = []
    for _ in range(100):
        # 创建线程的第1种方式
        # threading.Thread(
        #     target=account.deposit, args=(1, )
        # ).start()
        # 创建线程的第2种方式
        # AddMoneyThread(account, 1).start()
        # 创建线程的第3种方式
        # 调用线程池中的线程来执行特定的任务
        future = pool.submit(account.deposit, 1)
        futures.append(future)
    # 关闭线程池
    pool.shutdown()
    for future in futures:
        future.result()
    print(account.balance)


if __name__ == '__main__':
    main()
```

#### 多进程

多进程可以有效解决GIL的问题，实现多进程的主要类的Process，其他辅助的类与threading模块类似，进程间的共享数据可以使用管道、套接字等，在multiprocessing模块有一个Queue类，它是基于管道和锁机制提供了多个进程共享的队列

```python
"""
多进程和进程池的使用
多线程因为GIL的存在不能够发挥CPU的多核特性
对于计算密集型任务应该考虑使用多进程
使用i7-8700实际测试
main use time:2.775926113128662
main1 use time:11.36860966682434
差了4倍左右的执行时间
"""
import time
from functools import wraps


def timeclock(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        with open('time.txt', 'a') as f:
            f.write('{} use time:{}\n'.format(func.__name__, end-start))
        return result
    return wrapper




import concurrent.futures
import math

PRIMES = [
    1116281,
    1297337,
    104395303,
    472882027,
    533000389,
    817504243,
    982451653,
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419
] * 5


def is_prime(n):
    """判断素数"""
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

@timeclock
def main():
    """主函数"""
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))


@timeclock
def main1():
    for number in PRIMES:
        print(is_prime(number))


if __name__ == '__main__':
    main()
    main1()
```

**重点**：**多线程和多进程的比较**。

以下情况需要使用多线程：

1. 程序需要维护许多共享的状态（尤其是可变状态），Python中的列表、字典、集合都是线程安全的，所以使用线程而不是进程维护共享状态的代价相对较小。
2. 程序会花费大量时间在I/O操作上，没有太多并行计算的需求且不需占用太多的内存。

以下情况需要使用多进程：

1. 程序执行计算密集型任务（如：字节码操作、数据处理、科学计算）。
2. 程序的输入可以并行的分成块，并且可以将运算结果合并。
3. 程序在内存使用方面没有任何限制且不强依赖于I/O操作（如：读写文件、套接字等）。

#### 异步I/O

异步处理：从调度程序的任务队列中挑选任务，该调度程序以交叉的形式执行这些任务，但是不能保证任务的执行顺序，因为执行顺序取决于队列中的一项任务是否愿意将CPU和时间片让给另一项任务。异步任务通常通过多任务协作处理的方式来实现，由于执行时间和顺序的不确定，因此需要通过回调式编程或者future对象来获取任务执行的结果。

~~~python
"""
异步I/O - async / await
"""
import asyncio


def num_generator(m, n):
    """指定范围的数字生成器"""
    yield from range(m, n + 1)


async def prime_filter(m, n):
    """素数过滤器"""
    primes = []
    for i in num_generator(m, n):
        flag = True
        for j in range(2, int(i ** 0.5 + 1)):
            if i % j == 0:
                flag = False
                break
        if flag:
            print('Prime =>', i)
            primes.append(i)

        await asyncio.sleep(0.001)
    return tuple(primes)


async def square_mapper(m, n):
    """平方映射器"""
    squares = []
    for i in num_generator(m, n):
        print('Square =>', i * i)
        squares.append(i * i)

        await asyncio.sleep(0.001)
    return squares


def main():
    """主函数"""
    loop = asyncio.get_event_loop()
    future = asyncio.gather(prime_filter(2, 100), square_mapper(1, 100))
    future.add_done_callback(lambda x: print(x.result()))
    loop.run_until_complete(future)
    loop.close()


if __name__ == '__main__':
    main()
~~~

说明：<font color='red'>上面的代码使用`get_event_loop`函数获得系统默认的事件循环，通过`gather`函数可以获得一个`future`对象，`future`对象的`add_done_callback`可以添加执行完成时的回调函数，`loop`对象的`run_until_complete`方法可以等待通过`future`对象获得协程执行结果</font>

python中有一个aiohttp的第三方库，提供了异步的HTTP客户端和服务器，这个第三方库可以跟asyncio模块一起工作，并提供了对Future对象的支持，Python3.6中引入了async和await来定义异步执行的函数以及创建异步上下文，在Python3.7中正式成为关键字。下面的代码异步从5个URL获取页面并且通过正则表达式来获取网站标题

~~~python
import asyncio
import re

import aiohttp

PATTERN = re.compile(r'\<title\>(?P<title>.*)\<\/title\>')


async def fetch_page(session, url):
    async with session.get(url, ssl=False) as resp:
        return await resp.text()


async def show_title(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch_page(session, url)
        print(PATTERN.search(html).group('title'))


def main():
    urls = ('https://www.python.org/',
            'https://git-scm.com/',
            'https://www.jd.com/',
            'https://www.taobao.com/',
            'https://www.douban.com/')
    loop = asyncio.get_event_loop()
    cos = [show_title(url) for url in urls]
    loop.run_until_complete(asyncio.wait(cos))
    loop.close()


if __name__ == '__main__':
    main()
~~~

> **重点**：**异步I/O与多进程的比较**。
>
> <font color='red'>当程序不需要真正的并发性或并行性，而是更多的依赖于异步处理和回调时，`asyncio`就是一种很好的选择。如果程序中有大量的等待与休眠时，也应该考虑`asyncio`，它很适合编写没有实时数据处理需求的Web应用服务器。</font>

Python还有很多用于处理并行任务的三方库，例如：`joblib`、`PyMP`等。实际开发中，要提升系统的可扩展性和并发性通常有垂直扩展（增加单个节点的处理能力）和水平扩展（将单个节点变成多个节点）两种做法。可以通过消息队列来实现应用程序的解耦合，消息队列相当于是多线程同步队列的扩展版本，不同机器上的应用程序相当于就是线程，而共享的分布式消息队列就是原来程序中的Queue。消息队列（面向消息的中间件）的最流行和最标准化的实现是AMQP（高级消息队列协议），AMQP源于金融行业，提供了排队、路由、可靠传输、安全等功能，最著名的实现包括：Apache的ActiveMQ、RabbitMQ等。

要实现任务的异步化，可以使用名为`Celery`的三方库。`Celery`是Python编写的分布式任务队列，它使用分布式消息进行工作，可以基于RabbitMQ或Redis来作为后端的消息代理。