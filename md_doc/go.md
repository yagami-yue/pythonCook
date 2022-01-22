# Go语言特色

1.简介、快速、安全

2.并行，开源

3.内存管理、数组安全、编译迅速

# Go语言用途

Go语言被设计成一门应用于搭载Web服务器，存储集群或类似用途的巨型中央服务器的系统编程语言

对于高性能分布式系统来说，Go语言比大多数语言有着更高的开发效率，它提供了海量并行的支持

~~~go
/* helloworld */
/* package在一个文件夹内所有的go文件只能有一个包名，fmt类似于stdio.h实现了标准输入输出 */
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
/* 运行方式 go run xx.go*/
/* 或者 go build xx.go生成二进制文件 然后./xx运行 */
~~~

# Go基础语法

注释

~~~go
// 单行注释
/*
 Author by 菜鸟教程
 我是多行注释
 */
~~~

字符串连接可以直接使用+

变量声明使用空格隔开

格式化字符串

~~~go
package main

import (
    "fmt"
)

func main() {
   // %d 表示整型数字，%s 表示字符串
    var stockcode=123
    var enddate="2020-12-31"
    var url="Code=%d&endDate=%s"
    var target_url=fmt.Sprintf(url,stockcode,enddate)
    fmt.Println(target_url)
}
~~~



# Go数据类型

1.布尔

2.数字(int, int8.......)

3.字符串

4.派生类型(包括指针、数组、struct、Channel、函数、切片、接口、Map)

# Go语言变量

1.通过var关键字定义变量类型然后指定值

2.通过var 定义变量并赋值，类型由系统自己判断

3.通过:=声明变量

~~~go
// 1
var num int
// 2
var num = 8
// 3
num := 8



//类型相同多个变量, 非全局变量
var vname1, vname2, vname3 type
vname1, vname2, vname3 = v1, v2, v3

var vname1, vname2, vname3 = v1, v2, v3 // 和 python 很像,不需要显示声明类型，自动推断

vname1, vname2, vname3 := v1, v2, v3 // 出现在 := 左侧的变量不应该是已经被声明过的，否则会导致编译错误


// 这种因式分解关键字的写法一般用于声明全局变量
var (
    vname1 v_type1
    vname2 v_type2
)


// 常量可以使用const来定义，不需要指定类型编译器可以自动推断其类型
const c_name1, c_name2 = value1, value2
// 可以做枚举
const (
    Unknown = 0
    Female = 1
    Male = 2
)
~~~

iota，特殊常量，可以认为是一个可以被编译器修改的常量。

iota 在 const关键字出现时将被重置为 0(const 内部的第一行之前)，const 中每新增一行常量声明将使 iota 计数一次(iota 可理解为 const 语句块中的行索引)。

iota 可以被用作枚举值：

```go
const (
    a = iota
    b = iota
    c = iota
)
```

第一个 iota 等于 0，每当 iota 在新的一行被使用时，它的值都会自动加 1；所以 a=0, b=1, c=2 可以简写为如下形式：

```go
const (
    a = iota
    b
    c
)


package main

import "fmt"

func main() {
    const (
            a = iota   //0
            b          //1
            c          //2
            d = "ha"   //独立值，iota += 1
            e          //"ha"   iota += 1
            f = 100    //iota +=1
            g          //100  iota +=1
            h = iota   //7,恢复计数
            i          //8
    )
    fmt.Println(a,b,c,d,e,f,g,h,i)
}
// 0 1 2 ha ha 100 100 7 8
```

对于数组的初始化

在不考虑逃逸分析的情况下，如果数组中元素的个数小于或者等于 4 个，那么所有的变量会直接在栈上初始化，如果数组元素大于 4 个，变量就会在静态存储区初始化然后拷贝到栈上，这些转换后的代码才会继续进入[中间代码生成](https://draveness.me/golang/docs/part1-prerequisite/ch02-compile/golang-ir-ssa/)和[机器码生成](https://draveness.me/golang/docs/part1-prerequisite/ch02-compile/golang-machinecode/)两个阶段，最后生成可以执行的二进制文件。

# 操作符

*:指针变量，取后面变量(地址)的值

&: 取地址符

空指针为nil

~~~go
package main

import "fmt"

func main() {
   var a int= 20   /* 声明实际变量 */
   var ip *int        /* 声明指针变量 */

   ip = &a  /* 指针变量的存储地址 */

   fmt.Printf("a 变量的地址是: %x\n", &a  )

   /* 指针变量的存储地址 */
   fmt.Printf("ip 变量储存的指针地址: %x\n", ip )

   /* 使用指针访问值 */
   fmt.Printf("*ip 变量的值: %d\n", *ip )
}
~~~





# 函数

```go
func function_name( [parameter list] ) [return_types] {
   函数体
}
```

函数定义解析：

- func：函数由 func 开始声明
- function_name：函数名称，参数列表和返回值类型构成了函数签名。
- parameter list：参数列表，参数就像一个占位符，当函数被调用时，你可以将值传递给参数，这个值被称为实际参数。参数列表指定的是参数类型、顺序、及参数个数。参数是可选的，也就是说函数也可以不包含参数。
- return_types：返回类型，函数返回一列值。return_types 是该列值的数据类型。有些功能不需要返回值，这种情况下 return_types 不是必须的。
- 函数体：函数定义的代码集合。

![image-20211104141020609](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20211104141020609.png)

**所有参数都是值传递：**slice，map，channel 会有传引用的错觉(比如切片，他背后对应的是一个数组，切片本身是一个数据结构，在这个数据结构中包含了指向了这个数组的指针。所以说，即便是在传值的情况下这个结构被复制到函数里了，在通过指针去操作这个数组的值的时候，其实是操作的是同一块空间，实际上是结构被复制了，但是结构里包含的指针指向的是同一个数组，所以才有这个错觉)

 



