## 介绍



![../_images/asynchronous-programming-model.png](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/_images/asynchronous-programming-model.png)

如上图所示，任务（不同的颜色表示不同的任务）可能被其他任务插入，但是都处在同一个线程下。这表明，当某一个任务执行的时候，其他的任务都暂停了。与多线程编程模型很大的一点不同是， *多线程由操作系统决定在时间线上什么时候挂起某个活动或恢复某个活动，而在异步并发模型中，程序员必须假设线程可能在任何时间被挂起和替换。*

## concurrent.futures

Python3.2带来了 `concurrent.futures` 模块，这个模块具有线程池和进程池、管理并行编程任务、处理非确定性的执行流程、进程/线程同步等功能。

此模块由以下部分组成：

- `concurrent.futures.Executor`: 这是一个虚拟基类，提供了异步执行的方法。
- `submit(function, argument)`: 调度函数（可调用的对象）的执行，将 `argument` 作为参数传入。
- `map(function, argument)`: 将 `argument` 作为参数执行函数，以 **异步** 的方式。
- `shutdown(Wait=True)`: 发出让执行者释放所有资源的信号。
- `concurrent.futures.Future`: 其中包括函数的异步执行。Future对象是submit任务（即带有参数的functions）到executor的实例。

Executor是抽象类，可以通过子类访问，即线程或进程的 `ExecutorPools` 。因为，线程或进程的实例是依赖于资源的任务，所以最好以“池”的形式将他们组织在一起，作为可以重用的launcher或executor。

## 使用线程池和进程池

线程池或进程池是用于在程序中优化和简化线程/进程的使用。通过池，你可以提交任务给executor。池由两部分组成，一部分是内部的队列，存放着待执行的任务；另一部分是一系列的进程或线程，用于执行这些任务。池的概念主要目的是为了重用：让线程或进程在生命周期内可以多次使用。它减少了创建创建线程和进程的开销，提高了程序性能。重用不是必须的规则，但它是程序员在应用中使用池的主要原因。

![../_images/pooling-management.png](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/_images/pooling-management.png)

current.Futures模块提供了两种Executor的子类，各自独立操作一个线程池和一个进程池

- `concurrent.futures.ThreadPoolExecutor(max_workers)`
- `concurrent.futures.ProcessPoolExecutor(max_workers)`

```python
import concurrent.futures
import time
number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def evaluate_item(x):
        # 计算总和，这里只是为了消耗时间
        result_item = count(x)
        # 打印输入和输出结果
        return result_item

def  count(number) :
        for i in range(0, 10000000):
                i=i+1
        return i * number

if __name__ == "__main__":
        # 顺序执行
        start_time = time.time()
        for item in number_list:
                print(evaluate_item(item))
        print("Sequential execution in " + str(time.time() - start_time), "seconds")
        # 线程池执行
        start_time_1 = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(evaluate_item, item) for item in number_list]
                for future in concurrent.futures.as_completed(futures):
                        print(future.result())
        print ("Thread pool execution in " + str(time.time() - start_time_1), "seconds")
        # 进程池
        start_time_2 = time.time()
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(evaluate_item, item) for item in number_list]
                for future in concurrent.futures.as_completed(futures):
                        print(future.result())
        print ("Process pool execution in " + str(time.time() - start_time_2), "seconds")
```

线程池所需要的时间比顺序执行少一点点

如同 `ThreadPoolExecutor` 一样， `ProcessPoolExecutor` 是一个executor，使用一个线程池来并行执行任务。然而，和 `ThreadPoolExecutor` 不同的是， `ProcessPoolExecutor` 使用了多核处理的模块，让我们可以不受GIL的限制，大大缩短执行时间

## 使用Asyncio管理事件循环

python的Asyncio模块提供了管理时间、携程、任务和线程的方法，以及编写并发代码的原语

- **事件循环**: 在Asyncio模块中，每一个进程都有一个事件循环。
- **协程**: 这是子程序的泛化概念。协程可以在执行期间暂停，这样就可以等待外部的处理（例如IO）完成之后，从之前暂停的地方恢复执行。
- **Futures**: 定义了 `Future` 对象，和 `concurrent.futures` 模块一样，表示尚未完成的计算。
- **Tasks**: 这是Asyncio的子类，用于封装和管理并行模式下的协程。

### 事件循环

在计算机系统中，可以产生事件的实体叫做事件源，能处理事件的实体叫做事件处理者。此外还有一些第三方实体叫做事件循环，作用是管理所有的时间，在整个程序运行过程中不断循环执行，追踪事件发生的顺序将它们放到队列中，当主线程空闲的时候，调用相应的事件处理者处理事件。

- `loop = get_event_loop()`: 得到当前上下文的事件循环。
- `loop.call_later(time_delay, callback, argument)`: 延后 `time_delay` 秒再执行 `callback` 方法。
- `loop.call_soon(callback, argument)`: 尽可能快调用 `callback`, `call_soon()` 函数结束，主线程回到事件循环之后就会马上调用 `callback` 。
- `loop.time()`: 以float类型返回当前时间循环的内部时间。
- `asyncio.set_event_loop()`: 为当前上下文设置事件循环。
- `asyncio.new_event_loop()`: 根据此策略创建一个新的时间循环并返回。
- `loop.run_forever()`: 在调用 `stop()` 之前将一直运行。



~~~python
import asyncio
import datetime
import time

def function_1(end_time, loop):
    print ("function_1 called")
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, function_2, end_time, loop)
    else:
        loop.stop()

def function_2(end_time, loop):
    print ("function_2 called ")
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, function_3, end_time, loop)
    else:
        loop.stop()

def function_3(end_time, loop):
    print ("function_3 called")
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, function_4, end_time, loop)
    else:
        loop.stop()

def function_4(end_time, loop):
    print ("function_4 called")
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, function_1, end_time, loop)
    else:
        loop.stop()

loop = asyncio.get_event_loop()

end_loop = loop.time() + 9.0
loop.call_soon(function_1, end_loop, loop)
# loop.call_soon(function_4, end_loop, loop)
loop.run_forever()
loop.close()
~~~

一个事件循环

```python
@asyncio.coroutine
# 定义一个携程用装饰器即可，但是更新的做法是用
# async def fun() 然后用await代替yield from
```



```python
import asyncio
import time
from random import randint



async def StartState():
    print("Start State called \n")
    input_value = randint(0, 1)
    time.sleep(1)
    if (input_value == 0):
        result = await State2(input_value)
    else:
        result = await State1(input_value)
    print("Resume of the Transition : \nStart State calling " + result)


async def State1(transition_value):
    outputValue =  str("State 1 with transition value = %s \n" % transition_value)
    input_value = randint(0, 1)
    time.sleep(1)
    print("...Evaluating...")
    if input_value == 0:
        result = await State3(input_value)
    else :
        result = await State2(input_value)
    result = "State 1 calling " + result
    return outputValue + str(result)


async def State2(transition_value):
    outputValue =  str("State 2 with transition value = %s \n" % transition_value)
    input_value = randint(0, 1)
    time.sleep(1)
    print("...Evaluating...")
    if (input_value == 0):
        result = await State1(input_value)
    else :
        result = await State3(input_value)
    result = "State 2 calling " + result
    return outputValue + str(result)


async def State3(transition_value):
    outputValue = str("State 3 with transition value = %s \n" % transition_value)
    input_value = randint(0, 1)
    time.sleep(1)
    print("...Evaluating...")
    if (input_value == 0):
        result = await State1(input_value)
    else :
        result = await EndState(input_value)
    result = "State 3 calling " + result
    return outputValue + str(result)



async def EndState(transition_value):
    outputValue = str("End State with transition value = %s \n" % transition_value)
    print("...Stop Computation...")
    return outputValue

if __name__ == "__main__":
    print("Finite State Machine simulation with Asyncio Coroutine")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(StartState())
```

时间循环会一直持续到State3产生了一个1才会终止，所以理论上运行时间可以无限大

### Futures

Asyncio模块另一个重要的组件是Future类，它跟concurrent.futures.Futures很像，但是针对Asyncio的事件循环做了很多定制。Asyncio.Futures类代表还未完成的结果(有可能是一个Exception)，所以综合来说，它是一种抽象，代表还没有做完的事情

```python
import asyncio
future = asyncio.Future()
```

Future的基本方法有：

- `cancel()`: 取消future的执行，调度回调函数
- `result()`: 返回future代表的结果
- `exception()`: 返回future中的Exception
- `add_done_callback(fn)`: 添加一个回调函数，当future执行的时候会调用这个回调函数
- `remove_done_callback(fn)`: 从“call whten done”列表中移除所有callback的实例
- `set_result(result)`: 将future标为执行完成，并且设置result的值
- `set_exception(exception)`: 将future标为执行完成，并设置Exception

```python
# -*- coding: utf-8 -*-

"""
Asyncio.Futures -  Chapter 4 Asynchronous Programming
"""
import asyncio
import sys


async def first_coroutine(future, N):
    """前n个数的和"""
    count = 0
    for i in range(1, N + 1):
        count = count + i
    await asyncio.sleep(3)
    future.set_result("first coroutine (sum of N integers) result = " + str(count))


async def second_coroutine(future, N):
    count = 1
    for i in range(2, N + 1):
        count *= i
    await asyncio.sleep(4)
    future.set_result("second coroutine (factorial) result = " + str(count))

def got_result(future):
   print(future.result())

if __name__ == "__main__":
   N1 = int(sys.argv[1])
   N2 = int(sys.argv[2])
   loop = asyncio.get_event_loop()
   future1 = asyncio.Future()
   future2 = asyncio.Future()
   tasks = [
       first_coroutine(future1, N1),
       second_coroutine(future2, N2)]
   future1.add_done_callback(got_result)
   future2.add_done_callback(got_result)
   loop.run_until_complete(asyncio.wait(tasks))
   loop.close()
```

## 分布式计算

分布式计算基本的思想是将<font color='red'>一个大任务分散成几个小任务</font>，交给分布式网络中的计算机去完成。在分布式计算的环境中，必须保证网络中的计算机的可用性（避免网络延迟、非预知的崩溃等），所以就需要可持续的监控架构。

采用这种技术产生的根本问题是对各种类型的流量（数据，任务，命令等）进行适当的分配。此外，还有一个分布式系统基础特征产生的问题：网络由不同操作系统的计算机组成，很多互不兼容。实际上，随着时间的推移，为了使用分布式环境中的不同资源，已经可以识别不同的计算模型。他们的目标是提供一个框架，为一个分布式应用的不同处理器之间描述合作方法。

基本上各种模型的不同点是分布式系统能提供的容量的大小。最常用的模型是服务器/客户端模型。它可以让不同的进程运行在不同的计算机上，通过交换消息进行实时的合作。相对于前一个模型有很大的提高，前一个模型要求将所有的文件分发到所有的机器上，从而进行离线的计算。客户端/服务器模型典型的实现是通过远程的程序调用（这是本地调用的扩展），或者通过分布式对象的程序（面向对象的中间件）。本章将介绍一些Python提供的类似的计算架构。然后我们会介绍一些用OO的方法或远程调用实现了分布式架构的库，例如 Celery，SCOOP， Pyro4 和 RPyC，也有一些使用了不同方法的库，例如 PyCSP 和Disco，Python版本的 MapReduce 算法。

### celery

celery是一个Python框架，用来管理分布式任务，遵循面对对象的中间件方法，它的主要feature是可以将许多小任务分布到一个大型的计算集群中，最后把任务的结果收集起来，组成整体的解决方案。

使用celery除了安装Celery的库，还需要一个消息代理（Message Broker），这是独立于Celery的一个中间件，用来和分布式的worker收发消息，它会处理通信网络中的信息交换。这种中间件的消息发送方案不再是点对点的，而是面向消息的方式