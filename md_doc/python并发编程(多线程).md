![../_images/Page-7-Image-1.png](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/_images/Page-7-Image-1.png)

## 内存管理

<font color='red'>        所谓存取周期就是连续启动两次读或写操作所需间隔的最小时间</font>。处理器的周期通常比内存周期短得多。当处理器传送数据到内存或从内存中获取数据时，内存依旧在一个周期中，其他任何设备（I/O控制器，处理器）都不能使用内存，因为内存必须先对上一个请求作出响应。

​        为了解决 MIMD 架构访问内存的问题，业界提出了两种内存管理系统。第一种就是人们所熟知的<font color='red'>共享内存系统</font>，共享内存系统有大量的虚拟内存空间，而且各个处理器对内存中的数据和指令拥有平等的访问权限。另外一种类型是<font color='red'>分布式内存模型</font>，在这种内存模型中，每个处理器都有自己专属的内存，其他处理器都不能访问。共享内存和分布式内存的区别以处理器的角度来说就是内存和虚拟内存体系的不同。每个系统的内存都会分为能独立访问的不同部分。共享内存系统和分布式内存系统的处理单元管理内存访问的方式也不相同。 `load R0,i` 指令意味着将 `i` 内存单元的内容加载进 `R0` 寄存器，但内存管理方式的不同，处理器的处理方式也不尽相同。在共享内存的系统中， `i` 代表的是内存的全局地址，对系统中的所有处理器来说都指向同一块内存空间。如果两个处理器想同时执行该内存中的指令，它们会向 `R0` 寄存器载入相同的内容。在分布式内存系统中， `i` 是局部地址。如果两个处理器同时执行向 `R0` 载入内容的语句，执行结束之后，不同处理器 `R0` 寄存器中的值一般情况下是不一样的，因为每个处理器对应的内存单元中的 `i` 代表的全局地址不一样。对于程序员来说，必须准确的区分共享内存和分布式内存，因为在并行编程中需要考量内存管理方式来决定进程或线程间通讯的方式。对于共享内存系统来说，共享内存能够在内存中构建数据结构并在子进程间通过引用直接访问该数据结构。而对于分布式内存系统来说，必须在每个局部内存保存共享数据的副本。一个处理器会向其他处理器发送含有共享数据的消息从而创建数据副本。这使得分布式内存管理有一个显而易见的缺点，那就是，如果要发送的消息太大，发送过程会耗费相对较长的时间。

### 共享内存

![../_images/Page-8-Image-1.png](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/_images/Page-8-Image-1.png)

每一个处理器有自己的Cache，Cache里保存着局部内存中有可能被处理器使用的指令or数据，有可能别的处理器修改了数据，但是其他处理器正在使用，已经修改的值会随着cache传递到共享内存，进而传递到其他处理器的Cache中。这就是熟知的<font color='red'>Cache一致性问题</font>

共享内存系统的主要特性如下：

- 内存对于所有处理器来说是一样的，例如，所有处理器所对应的相同数据结构都存在于相同的逻辑地址，也就是说可以从相同的内存单元中获得该数据结构。
- 通过控制处理器对共享内存的访问权限可以达到同步控制的效果。实际上，每次只有一个处理器拥有对内存资源的访问权限。
- 当一个任务正在访问共享内存的时候，其它所有任务都不能改变内存单元的内容。
- 共享内存很快，两个任务通讯的时间和读取单个内存单元的时间相等（取决于内存的访问速度）

在共享内存系统中访问内存的方式如下

- 均匀内存访问 (Uniform memory access (UMA) )：这类系统的基本特征是无论对于处理器来说访问任意的内存区域速度是相同的。因此，这些系统也成为对称式多处理器 (symmetric multiprocessor (SMP)) 系统。这类系统实现起来相对简单，但是可扩展性较差，程序员需要通过插入适当的控制、信号量、锁等机制来管理同步，进而在程序中管理资源。
- 非均匀内存访问 (Non-uniform memory access (NUMA))：这类架构将内存分为高速访问区域和低速访问区域。高速访问区域是分配给各个处理器的区域，是用于数据交换的公用区域。这类系统也称为分布式共享内存系统 (Distributed Shared Memory Systems (DSM)) ，这类系统的扩展性很好，但开发难度较高。
- 无远程内存访问 (No remote memory access (NORMA))：对于处理器来说内存在物理上是分布式存在的。每个处理器只能访问其局部私有内存。处理器之间通过消息传递协议进行通讯。
- 仅Cache可访问 (Cache only memory access (COMA))：这类系统中仅有Cache内存。分析 NUMA 架构时，需要注意的是这类系统会把数据的副本保存在Cache中供处理器使用，并且在主存中也保留着重复的数据。COMA 架构可以移除重复的主存数据，而只保留Cache内存。对于处理器来说内存在物理上是分布式存在的。每个处理器只能访问其局部私有内存。处理器之间通过消息传递协议进行通讯。

## 分布式内存

在使用分布式内存的系统中，各个处理器都有其各自的内存，而且每个处理器只能处理属于自己的内存。某些学者把这类系统称为“多计算机系统”，这个名字很真实地反映了组成这类系统的元素能够独立作为一个具有内存和处理器的微型系统，如下图所示：

![../_images/Page-10-Image-1.png](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/_images/Page-10-Image-1.png)

这种内存管理方式有几个好处。第一，<font color='red'>总线和开关级别的的通讯不会发生冲突。每个处理器都可以无视其他处理器的干扰而充分利用局部内存的带宽；第二，没有通用总线意味着没有处理器数量的限制，系统的规模只局限于连接处理器的网络带宽；第三，没有Cache一致性问题的困扰</font>。每个处理器只需要处理属于自己的数据而无须关心上传数据副本的问题。但最大的缺点是，很难实现处理器之间的通讯。如果一个处理器需要其他处理器的数据，这两个处理器必须要通过消息传递协议来交换消息。这样进行通讯会导致速度降低，原因有两个，首先，从一个处理器创建和发送消息到另外一个处理器需要时间；其次，任何处理器都需要停止工作，处理来自其他处理器的消息。面向分布式内存机器的程序必须按照尽量相互独立的任务来组织，任务之间通过消息进行通讯。

![../_images/Page-11-Image-1.png](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/_images/Page-11-Image-1.png)

分布式内存系统的特性如下：

- 内存通常分布在不同的处理器之中，局部内存只能由对应的处理器访问。
- 同步控制通过在处理器之间转移数据 (也可以是消息本身) 来实现， 同理通讯的实现方式也一样。
- 局部内存的数据分支会影响机器的性能——有必要精确地进行数据分割最小化 CPU 间的通讯。另外，协调数据的分解合成操作的处理器必须与处理部分数据的处理器高效地通讯。
- 消息传递协议用于 CPU 间通过交换数据包通讯。消息是信息的分解单元，他们经过良好的定义，所以处理器之间能够准确地识别出消息地内容。

### 大规模并行处理 

MPP (Massively parallel processing )机器由上百个处理器 (在一些机器中达到成千上万个) 通过通讯网络连接而成。世界上最快的计算机几乎都基于这种架构，采用这种架构的计算机系统有:Earth Simulator， Blue Gene， ASCI White， ASCI Red， ASCI Purple 以及 Red Storm 等。

### 工作站集群

工作站集群是指将传统的计算机通过通讯网络连接起来。在集群架构中，一个节点就是集群中的一个计算单元。对于用户来说，集群是完全透明的，掩盖了软硬件的复杂性，使得数据以及应用仿佛从一个节点中得到的。

在这里，会定义三种集群：

- 故障切换集群 (The fail-over cluster) ：在这类集群中，会持续检测节点的活动状态，当一个节点出现故障，另外一台机器会马上接管故障节点的工作。这类集群通过这种冗余架构可以保证系统的可用性。
- 负载均衡集群 (The load balancing cluster) ：在这类系统中，会将一个作业请求发送给负载较小的节点上执行。这样做可以减少整个处理过程所耗费的时间。
- 高性能计算集群 (The high-performance cluster) :在这类系统中，每个节点都可以提供极高的性能，一个任务依旧分解为若干个子任务交给各个节点处理。任务是并行化的，分配给不同的机器进行处理。

### 异构架构

在同构的超级计算机中采用GPU加速器改变了之前超级计算机的使用规则。即使GPU能够提供高性能计算，但是不能把它看作一个独立的处理单元，因为GPU必须在CPU的配合下才能顺利完成工作。因此，异构计算的程序设计方法很简单，首先CPU通过多种方式计算和控制任务，将计算密集型和具有高并行性的任务分配给图形加速卡执行。CPU和GPU之间不仅可以通过高速总线通讯，也可以通过共享一块虚拟内存或物理内存通讯。事实上，在这类设备上GPU和CPU都没有独立的内存区域，一般是通过由各种编程框架(如CUDA，OpenCL)提供的库来操作内存。这类架构被称之为异构架构，在这种架构中，应用程序可以在单一的地址空间中创建数据结构，然后将任务分配给合适的硬件执行。通过原子性操作，多个任务可以安全地操控同一个内存区域同时避免数据一致性问题。所以，尽管CPU和GPU看起来不能高效联合工作，但通过新的架构可以优化它们之间的交互和提高并行程序的性能。

![../_images/Page-13-Image-1.png](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/_images/Page-13-Image-1.png)

## 并行编程模型

并行编程模型是作为对硬件和内存架构的抽象而存在的。事实上，这些模式不是特定的，而且和机器的类型或内存的架构无关。他们在理论上能在任何类型的机器上实现。相对于前面的架构细分，这些编程模型会在更高的层面上建立，用于表示软件执行并行计算时必须实现的方式。为了访问内存和分解任务，每一个模型都以它独自的方式和其他处理器共享信息。

需要明白的是没有最好的编程模型，模型的效果如何很大程度上取决于实际的问题。使用范围最广的并行编程模型有：

- 共享内存模型
- 多线程模型
- 分布式内存/消息传递模型
- 数据并行模型

在这节中，会描述这些编程模型的概览。在下一章会更加准确的描述这些编程模型，并会介绍Python中实现这些模型的相应模块

### 共享内存模型

在这个编程模型中所有任务都共享一个内存空间，对共享资源的读写是异步的。系统提供一些机制，如锁和信号量，来让程序员控制共享内存的访问权限。使用这个编程模型的优点是，程序员不需要清楚任务之间通讯的细节。但性能方面的一个重要缺点是,了解和管理数据区域变得更加困难;将数据保存在处理器本地才可以节省内存访问，缓存刷新以及多处理器使用相同数据时发生的总线流量。

### 多线程模型

在这个模型中，单个处理器可以有多个执行流程，例如，创建了一个顺序执行任务之后，会创建一系列可以并行执行的任务。通常情况下，这类模型会应用在共享内存架构中。由于多个线程会对共享内存进行操作，所以进行线程间的同步控制是很重要的，作为程序员必须防止多个线程同时修改相同的内存单元。现代的CPU可以在软件和硬件上实现多线程。POSIX 线程就是典型的在软件层面上实现多线程的例子。Intel 的超线程 (Hyper-threading) 技术则在硬件层面上实现多线程，超线程技术是通过当一个线程在停止或等待I/O状态时切换到另外一个线程实现的。使用这个模型即使是非线性的数据对齐也能实现并行性。

### 消息传递模型

消息传递模型通常在分布式内存系统（每一个处理器都有独立的内存空间）中应用。更多的任务可以驻留在一台或多台物理机器上。程序员需要确定并行和通过消息产生的数据交换。实现这个数据模型需要在代码中调用特定的库。于是便出现了大量消息传递模型的实现，最早的实现可以追溯到20世纪80年代，但直到90年代中期才有标准化的模型——实现了名为MPI (the Message Passing Interface, 消息传递接口)的事实标准。MPI 模型是专门为分布式内存设计的，但作为一个并行编程模型，也可以在共享内存机器上跨平台使用。

![../_images/Page-15-Image-1.png](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/_images/Page-15-Image-1.png)

### 数据并行模型

在这个模型中，有多个任务需要操作同一个数据结构，但每一个任务操作的是数据的不同部分。在共享内存架构中，所有任务都通过共享内存来访问数据；在分布式内存架构中则会将数据分割并且保存到每个任务的局部内存中。为了实现这个模型，程序员必须指定数据的分配方式和对齐方式。现代的GPU在数据已对齐的情况下运行的效率非常高。

![../_images/Page-16-Image-1.png](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/_images/Page-16-Image-1.png)

## 线程Threading

~~~python
import threading

def function(i):
    print ("function called by thread %i\n" % i)
    return

threads = []

for i in range(5):
    t = threading.Thread(target=function , args=(i, ))
    threads.append(t)
    t.start()  # start()让线程开始
    t.join() # join让调用它的线程等待知道执行结束，即阻塞调用它的主线程，t执行结束，主线程才会继续
~~~

~~~python
import threading
import time

def first_function():
    print(threading.currentThread().getName() + str(' is Starting '))
    time.sleep(2)
    print (threading.currentThread().getName() + str(' is Exiting '))
    return

def second_function():
    print(threading.currentThread().getName() + str(' is Starting '))
    time.sleep(2)
    print (threading.currentThread().getName() + str(' is Exiting '))
    return

def third_function():
    print(threading.currentThread().getName() + str(' is Starting '))
    time.sleep(2)
    print(threading.currentThread().getName() + str(' is Exiting '))
    return

if __name__ == "__main__":
    t1 = threading.Thread(name='first_function', target=first_function)
    t2 = threading.Thread(name='second_function', target=second_function)
    t3 = threading.Thread(name='third_function', target=third_function)
    t1.start()
    t2.start()
    t3.start() # 如果t3的定义不加入name属性，那么默认获取到的name=Thread-1，因为默认情况下线程的name为Thread-n，n为创建的线程数目
~~~

`threading` 模块是创建和管理线程的首选形式。每一个线程都通过一个继承 `Thread` 类，重写 `run()` 方法来实现逻辑，这个方法是线程的入口。在主程序中，我们创建了多个 `myThread` 的类型实例，然后执行 `start()` 方法启动它们。调用 `Thread.__init__` 构造器方法是必须的，通过它我们可以给线程定义一些名字或分组之类的属性。调用 `start()` 之后线程变为活跃状态，并且持续直到 `run()` 结束，或者中间出现异常。所有的线程都执行完成之后，程序结束。

`join()` 命令控制主线程的终止。

## 利用Lock进行线程同步

~~~python
import threading

shared_resource_with_lock = 0
shared_resource_with_no_lock = 0
COUNT = 100000
shared_resource_lock = threading.Lock()

# 有锁的情况
def increment_with_lock():
    global shared_resource_with_lock
    for i in range(COUNT):
        shared_resource_lock.acquire()
        shared_resource_with_lock += 1
        shared_resource_lock.release()

def decrement_with_lock():
    global shared_resource_with_lock
    for i in range(COUNT):
        shared_resource_lock.acquire()
        shared_resource_with_lock -= 1
        shared_resource_lock.release()

# 没有锁的情况
def increment_without_lock():
    global shared_resource_with_no_lock
    for i in range(COUNT):
        shared_resource_with_no_lock += 1

def decrement_without_lock():
    global shared_resource_with_no_lock
    for i in range(COUNT):
        shared_resource_with_no_lock -= 1

if __name__ == "__main__":
    t1 = threading.Thread(target=increment_with_lock)
    t2 = threading.Thread(target=decrement_with_lock)
    t3 = threading.Thread(target=increment_without_lock)
    t4 = threading.Thread(target=decrement_without_lock)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    print ("the value of shared variable with lock management is %s" % shared_resource_with_lock)
    print ("the value of shared variable with race condition is %s" % shared_resource_with_no_lock)
~~~

## 利用RLock进行线程同步



~~~python
import threading
import time

class Box(object):
    lock = threading.RLock()

    def __init__(self):
        self.total_items = 0

    def execute(self, n):
        Box.lock.acquire()
        self.total_items += n
        Box.lock.release()

    def add(self):
        Box.lock.acquire()
        self.execute(1)
        Box.lock.release()

    def remove(self):
        Box.lock.acquire()
        self.execute(-1)
        Box.lock.release()

## These two functions run n in separate
## threads and call the Box's methods
def adder(box, items):
    while items > 0:
        print("adding 1 item in the box")
        box.add()
        time.sleep(1)
        items -= 1

def remover(box, items):
    while items > 0:
        print("removing 1 item in the box")
        box.remove()
        time.sleep(1)
        items -= 1

## the main program build some
## threads and make sure it works
if __name__ == "__main__":
    items = 5
    print("putting %s items in the box " % items)
    box = Box()
    t1 = threading.Thread(target=adder, args=(box, items))
    t2 = threading.Thread(target=remover, args=(box, items))
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print("%s items still remain in the box " % box.total_items)
~~~

## 两种线程锁的区别

Lock：Lock被称为①原始锁，原始锁是一个②在锁定时不属于特定线程的同步基元组件，它是能用的最低级的同步基元组件。原始锁处于 "锁定" 或者 "非锁定" 两种状态之一。它被创建时为非锁定状态。它有两个基本方法， `acquire()` 和 `release()` 。当状态为非锁定时， `acquire()` 将状态改为锁定并立即返回。当状态是锁定时， `acquire()` 将阻塞至其他线程调用 `release()` 将其改为非锁定状态，然后 `acquire()` 调用重置其为锁定状态并返回。 `release()` 只在锁定状态下调用； 它将状态改为非锁定并立即返回。如果尝试释放一个非锁定的锁，则会引发 `RuntimeError` 异常。锁支持 上下文管理协议，即支持with语句，下文例子中会用到。

RLock：RLock被称为重入锁，若要锁定锁，线程调用其 `acquire()` 方法；一旦线程拥有了锁，方法将返回。若要解锁，线程调用 `release()` 方法。 ③`acquire()`/`release()` 对可以嵌套，重入锁必须由获取它的线程释放。一旦线程获得了重入锁，同一个线程再次获取它将不阻塞。只有最终 `release()` (最外面一对的 `release()` ) 将锁解开，才能让其他线程继续处理 `acquire()` 阻塞。；线程必须在每次获取它时释放一次。

两者使用的方法大部分还是相同的，下面根据以上红色强调部分描述一下二者的区别

①是名称的区别，一个叫原始锁，一个叫重入锁，这没啥好说的

②Lock在锁定时不属于特定线程，也就是说，Lock可以在一个线程中上锁，在另一个线程中解锁。而对于RLock来说，只有当前线程才能释放本线程上的锁，即解铃还须系铃人：

## 使用信号量进行线程同步

信号量是由操作系统管理的一种抽象数据类型，用于在多线程中同步对共享资源的使用。本质上说，信号量是一个内部数据，用于标明当前的共享资源可以有多少并发读取。

同样的，在threading模块中，信号量的操作有两个函数，即 `acquire()` 和 `release()` ，解释如下：

- 每当线程想要读取关联了信号量的共享资源时，必须调用 `acquire()` ，此操作减少信号量的内部变量, 如果此变量的值非负，那么分配该资源的权限。如果是负值，那么线程被挂起，直到有其他的线程释放资源。
- 当线程不再需要该共享资源，必须通过 `release()` 释放。这样，信号量的内部变量增加，在信号量等待队列中排在最前面的线程会拿到共享资源的权限。

![../_images/semaphores.png](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/_images/semaphores.png)

虽然表面上看信号量机制没什么明显的问题，如果信号量的等待和通知操作都是原子的，确实没什么问题。但如果不是，或者两个操作有一个终止了，就会导致糟糕的情况。

举个例子，假设有两个并发的线程，都在等待一个信号量，目前信号量的内部值为1。假设第线程A将信号量的值从1减到0，这时候控制权切换到了线程B，线程B将信号量的值从0减到-1，并且在这里被挂起等待，这时控制权回到线程A，信号量已经成为了负值，于是第一个线程也在等待。

这样的话，尽管当时的信号量是可以让线程访问资源的，但是因为非原子操作导致了所有的线程都在等待状态。

```python
# -*- coding: utf-8 -*-

"""Using a Semaphore to synchronize threads"""
import threading
import time
import random

# The optional argument gives the initial value for the internal
# counter;
# it defaults to 1.
# If the value given is less than 0, ValueError is raised.
semaphore = threading.Semaphore(0)

def consumer():
        print("consumer is waiting.")
        # Acquire a semaphore
        semaphore.acquire()
        # The consumer have access to the shared resource
        print("Consumer notify : consumed item number %s " % item)

def producer():
        global item
        time.sleep(10)
        # create a random item
        item = random.randint(0, 1000)
        print("producer notify : produced item number %s" % item)
         # Release a semaphore, incrementing the internal counter by one.
        # When it is zero on entry and another thread is waiting for it
        # to become larger than zero again, wake up that thread.
        semaphore.release()

if __name__ == '__main__':
        for i in range (0,5) :
                t1 = threading.Thread(target=producer)
                t2 = threading.Thread(target=consumer)
                t1.start()
                t2.start()
                t1.join()
                t2.join()
        print("program terminated")
```

信号量的一个特殊用法是互斥量。互斥量是初始值为1的信号量，可以实现数据、资源的互斥访问。

信号量在支持多线程的编程语言中依然应用很广，然而这可能导致<font color='red'>死锁</font>的情况。例如，现在有一个线程t1先等待信号量s1，然后等待信号量s2，而线程t2会先等待信号量s2，然后再等待信号量s1，这样就可能会发生死锁，导致t1等待s2，但是t2在等待s1。

## 使用条件进行线程同步

~~~python
from threading import Thread, Condition
import time

items = []
condition = Condition()

class consumer(Thread):

    def __init__(self):
        Thread.__init__(self)

    def consume(self):
        global condition
        global items
        condition.acquire()
        if len(items) == 0:
            condition.wait() # 释放condition等待生产者生产，使用condition.notify()提醒消费者，然后继续执行
            print("Consumer notify : no item to consume")
        items.pop()
        print("Consumer notify : consumed 1 item")
        print("Consumer notify : items to consume are " + str(len(items)))

        condition.notify()
        condition.release()

    def run(self):
        for i in range(0, 20):
            time.sleep(2)
            self.consume()

class producer(Thread):

    def __init__(self):
        Thread.__init__(self)

    def produce(self):
        global condition
        global items
        condition.acquire()
        if len(items) == 10:
            condition.wait()  # wait会释放锁，然后通过notify尝试重新获取锁
            print("Producer notify : items producted are " + str(len(items)))
            print("Producer notify : stop the production!!")
        items.append(1)
        print("Producer notify : total items producted " + str(len(items)))
        condition.notify()
        condition.release()

    def run(self):
        for i in range(0, 20):
            time.sleep(1)
            self.produce()

if __name__ == "__main__":
    producer = producer()
    consumer = consumer()
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()
~~~

~~~python
from threading import Thread, Condition

condition = Condition()
current = "A"


class ThreadA(Thread):
    def run(self):
        global current
        for _ in range(10):
            with condition:
                while current != "A":
                    condition.wait()
                print("A")
                current = "B"
                condition.notify_all()


class ThreadB(Thread):
    def run(self):
        global current
        for _ in range(10):
            with condition:
                while current != "B":
                    condition.wait()
                print("B")
                current = "C"
                condition.notify_all()


class ThreadC(Thread):
    def run(self):
        global current
        for _ in range(10):
            with condition:
                while current != "C":
                    condition.wait()
                print("C")
                current = "A"
                condition.notify_all()


a = ThreadA()
b = ThreadB()
c = ThreadC()

a.start()
b.start()
c.start()

a.join()
b.join()
c.join()

### 开三个线程，顺序打印ABC三次
~~~

## 使用事件进行线程同步





![../_images/event.png](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/_images/event.png)



~~~python
import time
from threading import Thread, Event
import random
items = []
event = Event()

class consumer(Thread):
    def __init__(self, items, event):
        Thread.__init__(self)
        self.items = items
        self.event = event

    def run(self):
        while True:
            time.sleep(2)
            self.event.wait()
            item = self.items.pop()
            print('Consumer notify : %d popped from list by %s' % (item, self.name))

class producer(Thread):
    def __init__(self, items, event):
        Thread.__init__(self)
        self.items = items
        self.event = event

    def run(self):
        global item
        for i in range(100):
            time.sleep(2)
            item = random.randint(0, 256)
            self.items.append(item)
            print('Producer notify : item N° %d appended to list by %s' % (item, self.name))
            print('Producer notify : event set by %s' % self.name)
            self.event.set()
            print('Produce notify : event cleared by %s '% self.name)
            self.event.clear()

if __name__ == '__main__':
    t1 = producer(items, event)
    t2 = consumer(items, event)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
~~~

在run方法中，每当item创建， `producer` 类将新item添加到list末尾然后发出事件通知。使用事件有两步，第一步：

```python
self.event.set() # 此时消费者在wait状态被激活
```

第二步：

```python
self.event.clear() # 清空事件
```

## 使用队列进行线程通信

​        当线程之间如果要共享资源或数据的时候，可能变的非常复杂，Python的threading模块提供了很多同步原语，包括信号量，条件变量，事件和锁。如果可以使用这些原语的话，应该优先考虑使用这些，而不是使用queue（队列）模块。队列操作起来更容易，也使多线程编程更安全，因为队列可以将资源的使用通过单线程进行完全控制，并且允许使用更加整洁和可读性更高的设计模式。

```python
from threading import Thread, Event
from queue import Queue
import time
import random
class producer(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self) :
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            print('Producer notify: item N° %d appended to queue by %s' % (item, self.name))
            time.sleep(1)

class consumer(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            item = self.queue.get()
            print('Consumer notify : %d popped from queue by %s' % (item, self.name))
            self.queue.task_done() # task_done() 方法将其标为任务已处理

if __name__ == '__main__':
    queue = Queue() # 队列不指定maxsize，默认queue=deque()，大小为无限大
    t1 = producer(queue)
    t2 = consumer(queue)
    t3 = consumer(queue)
    t4 = consumer(queue)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
```

## 评估多线程应用

​        <font color='red'>在 I/O 期间，GIL释放了</font>。多线程执行比单线程快的多。鉴于大多数应用需要很多I/O操作，GIL并没有限制程序员在这方面使用多线程对程序进行性能优化。你应该记住，增加线程并不会提高应用启动的时间，但是可以支持并发。例如，一次性创建一个线程池，并重用worker会很有用。这可以让我们切分一个大的数据集，用同样的函数处理不同的部分（生产者消费者模型）。那么GIL会成为试图发挥多线程应用潜能的纯Python开发的瓶颈吗？是的。线程是编程语言的架构，CPython解释器是线程和操作系统的桥梁。这就是为什么Jython，IronPython， Pypy没有GIL的原因，因为它不是必要的。

