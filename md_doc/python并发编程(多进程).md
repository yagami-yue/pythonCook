任何Python线程执行前，必须先获得GIL锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。正是由于GIL的存在，python多线程不能利用多核CPU，不过多进程可以，每个进程有自己的GIL锁，有自己的变量，当然多进程带来的切换更耗时，所以当数据量不大时，可能多进程反而要慢一点



## 介绍

<font color='red'>multiprocessing</font> 是Python标准库中的模块，实现了<font color='red'>共享内存机制</font>，也就是说，可以让运行在不同处理器核心的进程能读取共享内存

<font color='red'>mpi4py</font>编程范例（设计模式）。简单来说，就是进程之间不靠任何共享信息来进行通讯（也叫做shared nothing），<font color='red'>所有的交流都通过传递信息代替</font>

```python
# -*- coding: utf-8 -*-

import multiprocessing

def foo(i):
    print ('called function in process: %s' %i)
    return

if __name__ == '__main__':
    Process_jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=foo, args=(i,))
        Process_jobs.append(p)
        p.start()
        p.join()
```

进程对象的时候需要分配一个函数，作为进程的执行任务，本例中，这个函数是 `foo()` 。我们可以用元组的形式给函数传递一些参数。最后，使用进程对象调用 `join()` 方法。

<font color='red'>如果没有 `join()` ，主进程退出之后子进程会留在idle中，你必须手动杀死它们。</font>

所以一般情况下会把目标函数放在别的文件中，在主程序中导入

```python
# 命名一个进程
import multiprocessing
import time

def foo():
    name = multiprocessing.current_process().name
    print("Starting %s \n" % name)
    time.sleep(3)
    print("Exiting %s \n" % name)

if __name__ == '__main__':
    process_with_name = multiprocessing.Process(name='foo_process', target=foo)
    process_with_name.daemon = True  # 注意原代码有这一行，但是译者发现删掉这一行才能得到正确输出，因为代码没有join所以主进程结束，子进程即便没结束也会直接被kill
    process_with_default_name = multiprocessing.Process(target=foo)
    process_with_name.start()
    process_with_default_name.start()
```

子进程设置了daemon属性，主进程结束，子进程也会结束，daemon=True，守护模式，主进程结束后，会继续执行子进程

默认名称process-2， 主进程名称multiprocessing.current_process().name，为MainProcess

为了在后台运行进程，我们设置 `daemon` 参数为 `True`

```
background_process.daemon = True
```

- 如果某个子线程的daemon属性为False，主线程结束时会检测该子线程是否结束，如果该子线程还在运行，则主线程会等待它完成后再退出；
- 如果某个子线程的daemon属性为True，主线程运行结束时不对这个子线程进行检查而直接退出，同时所有daemon值为True的子线程将随主线程一起结束，而不论是否运行完成。

## kill进程

```python

# 杀死一个进程
# 通过.terminate()来结束进程，.alive()可以判断一个进程是否存活，.exitcode可以判断进程是否正常结束
# .exitcode ==0:没有错误正常退出，>0进程有错误，且退出，<0被.terminate()kill退出
import multiprocessing
import time

def foo():
        print('Starting function')
        time.sleep(0.1)
        print('Finished function')

if __name__ == '__main__':
        p = multiprocessing.Process(target=foo)
        print('Process before execution:', p, p.is_alive())
        p.start()
        print('Process running:', p, p.is_alive())
        p.terminate()
        print('Process terminated:', p, p.is_alive())
        p.join()
        print('Process joined:', p, p.is_alive())
        print('Process exit code:', p.exitcode)
```

## 定义进程子类

实现一个自定义的进程子类，需要以下三步：

- 定义 `Process` 的子类
- 覆盖 `__init__(self [,args])` 方法来添加额外的参数
- 覆盖 `run(self, [.args])` 方法来实现 `Process` 启动的时候执行的任务

创建 `Porcess` 子类之后，你可以创建它的实例并通过 `start()` 方法启动它，启动之后会运行 `run()` 方法。

```python
# -*- coding: utf-8 -*-
# 自定义子类进程
import multiprocessing

class MyProcess(multiprocessing.Process):
        def run(self):
                print ('called run method in process: %s' % self.name)
                return

if __name__ == '__main__':
        jobs = []
        for i in range(5):
                p = MyProcess()
                jobs.append(p)
                p.start()
                p.join()
```

## 进程间交换对象

![../_images/communication-channel.png](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/_images/communication-channel.png)

并行的应用常常需要在进程之间交换数据，Multiprocessing有两个方式可以交换对象：<font color='red'>pipe和queue</font>

### 队列（Queue）

Queue([maxsize])  创建共享的进程队列。maxsize是队列中允许的最大项数。如果省略此参数，则无大小限制

底层队列使用管道和锁定实现。另外，还需要运行支持线程以便队列中的数据传输到底层管道中。  Queue的实例q具有以下方法：

<font color='red'> q.get( [ block [ ,timeout ] ] ) </font> 返回q中的一个项目。如果q为空，此方法将阻塞，直到队列中有项目可用为止。block用于控制阻塞行为，默认为True. 如果设置为False，将引发Queue.Empty异常（定义在Queue模块中）。timeout是可选超时时间，用在阻塞模式中。如果在制定的时间间隔内没有项目变为可用，将引发Queue.Empty异常。

<font color='red'> q.get_nowait( )</font>  同q.get(block=False)方法。 

<font color='red'>q.put(item [, block [,timeout ] ] ) </font> 将item放入队列。如果队列已满，此方法将阻塞至有空间可用为止。block控制阻塞行为，默认为True。如果设置为False，将引发Queue.Empty异常（定义在Queue库模块中）。timeout指定在阻塞模式中等待可用空间的时间长短。超时后将引发Queue.Full异常。

<font color='red'> q.qsize()  </font>返回队列中目前项目的正确数量。此函数的结果并不可靠，因为在返回结果和在稍后程序中使用结果之间，队列中可能添加或删除了项目。在某些系统上，此方法可能引发NotImplementedError异常。  q.empty()  如果调用此方法时 q为空，返回True。如果其他进程或线程正在往队列中添加项目，结果是不可靠的。也就是说，在返回和使用结果之间，队列中可能已经加入新的项目。 q.full() 

```python
import multiprocessing
import random
import time

class Producer(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            print("Process Producer : item %d appended to queue %s" % (item, self.name))
            time.sleep(1)
            print("The size of queue is %s" % self.queue.qsize())

class Consumer(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                print("the queue is empty")
                break
            else:
                time.sleep(2)
                item = self.queue.get()
                print('Process Consumer : item %d popped from by %s \n' % (item, self.name))
                time.sleep(1)

if __name__ == '__main__':
    queue = multiprocessing.Queue()
    process_producer = Producer(queue)
    process_consumer = Consumer(queue)
    process_producer.start()
    process_consumer.start()
    process_producer.join()
    process_consumer.join()
```

**JoinableQueue([maxsize])** 
创建可连接的共享进程队列。这就像是一个Queue对象，但队列允许项目的使用者通知生产者项目已经被成功处理。通知进程是使用共享的信号和条件变量来实现的。 

```
JoinableQueue的实例p除了与Queue对象相同的方法之外，还具有以下方法：

q.task_done() 
使用者使用此方法发出信号，表示q.get()返回的项目已经被处理。如果调用此方法的次数大于从队列中删除的项目数量，将引发ValueError异常。

q.join() 
生产者将使用此方法进行阻塞，直到队列中所有项目均被处理。阻塞将持续到为队列中的每个项目均调用q.task_done()方法为止。 
下面的例子说明如何建立永远运行的进程，使用和处理队列上的项目。生产者将项目放入队列，并等待它们被处理。
```

### 管道（pipe）

```python
#创建管道的类（强调一点：必须在产生Process对象之前产生管道）：
Pipe([duplex]):在进程之间创建一条管道，并返回元组（conn1,conn2）,其中conn1，conn2表示管道两端的连接对象，
#参数介绍：
dumplex:默认管道是全双工的，如果将duplex射成False，conn1只能用于接收，conn2只能用于发送。
#主要方法：
    conn1.recv():接收conn2.send(obj)发送的对象。如果没有消息可接收，recv方法会一直阻塞。如果连接的另外一端已经关闭，那么recv方法会抛出EOFError。
    conn1.send(obj):通过连接发送对象。obj是与序列化兼容的任意对象
 #其他方法：
conn1.close():关闭连接。如果conn1被垃圾回收，将自动调用此方法
conn1.fileno():返回连接使用的整数文件描述符
conn1.poll([timeout]):如果连接上的数据可用，返回True。timeout指定等待的最长时限。如果省略此参数，方法将立即返回结果。如果将timeout射成None，操作将无限期地等待数据到达。
 
conn1.recv_bytes([maxlength]):接收c.send_bytes()方法发送的一条完整的字节消息。maxlength指定要接收的最大字节数。如果进入的消息，超过了这个最大值，将引发IOError异常，并且在连接上无法进行进一步读取。如果连接的另外一端已经关闭，再也不存在任何数据，将引发EOFError异常。
conn.send_bytes(buffer [, offset [, size]])：通过连接发送字节数据缓冲区，buffer是支持缓冲区接口的任意对象，offset是缓冲区中的字节偏移量，而size是要发送字节数。结果数据以单条消息的形式发出，然后调用c.recv_bytes()函数进行接收    
 
conn1.recv_bytes_into(buffer [, offset]):接收一条完整的字节消息，并把它保存在buffer对象中，该对象支持可写入的缓冲区接口（即bytearray对象或类似的对象）。offset指定缓冲区中放置消息处的字节位移。返回值是收到的字节数。如果消息长度大于可用的缓冲区空间，将引发BufferTooShort异常。
```

应该特别注意管道端点的正确管理问题。**如果是生产者或消费者中都没有使用管道的某个端点，就应将它关闭**。这也说明了为何在**生产者中关闭了管道的输出端，在消费者中关闭管道的输入端**。如果忘记执行这些步骤，程序可能在消费者中的recv（）操作上挂起。管道是由操作系统进行引用计数的，必须在所有进程中关闭管道后才能生成EOFError异常。因此，在生产者中关闭管道不会有任何效果，除非消费者也关闭了相同的管道端点。 

```python
# 管道
# from multiprocessing import Pipe
# left,right = Pipe()
# left.send('1234')
# print(right.recv())
# left.send('1234')
# print(right.recv())
# 管道的信息发送接收信息是不需要进行编码转码的
from multiprocessing import Process, Pipe

def f(parent_conn,child_conn):
    parent_conn.close() #不写close将不会引发EOFError
    while True:
        try:
            print(child_conn.recv())
        except EOFError:
            child_conn.close()
            break

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(parent_conn,child_conn,))
    p.start()
    child_conn.close()
    parent_conn.send('hello')
    parent_conn.send('hello')
    parent_conn.send('hello')
    parent_conn.close()
    p.join()
```

```python
import multiprocessing

def create_items(pipe):
    output_pipe, _ = pipe
    for item in range(10):
        output_pipe.send(item)
    output_pipe.close()

def multiply_items(pipe_1, pipe_2):
    close, input_pipe = pipe_1
    close.close()
    output_pipe, _ = pipe_2
    try:
        while True:
            item = input_pipe.recv()
            output_pipe.send(item * item)
    except EOFError:
        output_pipe.close()

if __name__== '__main__':
    # 第一个进程管道发出数字
    pipe_1 = multiprocessing.Pipe(True)
    process_pipe_1 = multiprocessing.Process(target=create_items, args=(pipe_1,))
    process_pipe_1.start()
    # 第二个进程管道接收数字并计算
    pipe_2 = multiprocessing.Pipe(True)
    process_pipe_2 = multiprocessing.Process(target=multiply_items, args=(pipe_1, pipe_2,))
    process_pipe_2.start()
    pipe_1[0].close()
    pipe_2[0].close()
    try:
        while True:
            print(pipe_2[1].recv())
    except EOFError:
        print("End")
```

## 进程如何同步

多个进程可以协同工作来完成一项任务。通常需要共享数据。所以在多进程之间保持数据的一致性就很重要了。需要共享数据协同的进程必须以适当的策略来读写数据。相关的同步原语和线程的库很类似。

进程的同步原语如下：

- **Lock**: 这个对象可以有两种装填：锁住的（locked）和没锁住的（unlocked）。一个Lock对象有两个方法， `acquire()` 和 `release()` ，来控制共享数据的读写权限。
- **Event**: 实现了进程间的简单通讯，一个进程发事件的信号，另一个进程等待事件的信号。 `Event` 对象有两个方法， `set()` 和 `clear()` ，来管理自己内部的变量。
- **Condition**: 此对象用来同步部分工作流程，在并行的进程中，有两个基本的方法： `wait()` 用来等待进程， `notify_all()` 用来通知所有等待此条件的进程。
- **Semaphore**: 用来共享资源，例如，支持固定数量的共享连接。
- **Rlock**: 递归锁对象。其用途和方法同 `Threading` 模块一样。
- **Barrier**: 将程序分成几个阶段，适用于有些进程必须在某些特定进程之后执行。处于障碍（Barrier）之后的代码不能同处于障碍之前的代码并行。barrier声明的第二个参数代表要管理的进程总数：

### Barrier+lock

```python
import multiprocessing
from multiprocessing import Barrier, Lock, Process
from time import time
from datetime import datetime

def test_with_barrier(synchronizer, serializer):
    name = multiprocessing.current_process().name
    synchronizer.wait() # 相当于推进了一次，定义barrier的时候的数字代表需要推几次继续执行
    now = time()
    with serializer:
        print("process %s ----> %s" % (name, datetime.fromtimestamp(now)))

def test_without_barrier():
    name = multiprocessing.current_process().name
    now = time()
    print("process %s ----> %s" % (name, datetime.fromtimestamp(now)))

if __name__ == '__main__':
    synchronizer = Barrier(2)
    serializer = Lock()
    Process(name='p1 - test_with_barrier', target=test_with_barrier, args=(synchronizer,serializer)).start()
    Process(name='p2 - test_with_barrier', target=test_with_barrier, args=(synchronizer,serializer)).start()
    Process(name='p3 - test_without_barrier', target=test_without_barrier).start()
    Process(name='p4 - test_without_barrier', target=test_without_barrier).start()
```

![../_images/barrier.png](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/_images/barrier.png)

### 管理状态Manage

```python
import multiprocessing

def worker(dictionary, key, item):
   dictionary[key] = item
   print("key = %d value = %d" % (key, item))

if __name__ == '__main__':
    mgr = multiprocessing.Manager() # Manager注册了很多python的数据结构，字典、队列等等
    SyncManager.register('Queue', queue.Queue)
    # SyncManager.register('JoinableQueue', queue.Queue)
    # SyncManager.register('Event', threading.Event, EventProxy)
    # SyncManager.register('Lock', threading.Lock, AcquirerProxy)
    # SyncManager.register('RLock', threading.RLock, AcquirerProxy)
    # SyncManager.register('Semaphore', threading.Semaphore, AcquirerProxy)

    # SyncManager.register('Condition', threading.Condition, ConditionProxy)
    # SyncManager.register('Barrier', threading.Barrier, BarrierProxy)
    # SyncManager.register('Pool', pool.Pool, PoolProxy)
    # SyncManager.register('list', list, ListProxy)
    # SyncManager.register('dict', dict, DictProxy)
    # SyncManager.register('Value', Value, ValueProxy)

    dictionary = mgr.dict() # 相当于全局注册一个字典，如果dictionary是一个普通的字典，则在主线程打印出来的为空
    jobs = [multiprocessing.Process(target=worker, args=(dictionary, i, i*2)) for i in range(10)]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print('Results:', dictionary)
```

### 如何使用进程池

多进程库提供了 `Pool` 类来实现简单的多进程任务。 `Pool` 类有以下方法：

- `apply()`: 直到得到结果之前一直阻塞。
- `apply_async()`: 这是 `apply()` 方法的一个变体，返回的是一个result对象。这是一个异步的操作，在所有的子类执行之前不会锁住主进程。
- `map()`: 这是内置的 `map()` 函数的并行版本。在得到结果之前一直阻塞，此方法将可迭代的数据的每一个元素作为进程池的一个任务来执行。
- `map_async()`: 这是 `map()` 方法的一个变体，返回一个result对象。如果指定了回调函数，回调函数应该是callable的，并且只接受一个参数。当result准备好时会自动调用回调函数（除非调用失败）。回调函数应该立即完成，否则，持有result的进程将被阻塞。

```python
import multiprocessing

def function_square(data):
    result = data*data
    return result

if __name__ == '__main__':
    inputs = list(range(100))
    pool = multiprocessing.Pool(processes=4) # 分给4个进程 
    pool_outputs = pool.map(function_square, inputs) # map函数
    pool.close()
    pool.join()
    print('Pool:',pool_outputs)
```

## MPI4py

