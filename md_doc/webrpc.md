## RTP&&RTCP

RTP/RTCP协议是流媒体通信的基石，<font color='red'>RTP协议定义了流媒体数据在互联网上传输的数据包格式，而RTCP协议则负责可靠传输、流量控制和拥塞控制等服务质量保证</font>。在webrtc项目中，RTP/RTCP模块作为传输模块的一部分，负责对发送端采集到的媒体数据进行封包，然后交给上层网络模块发送；

![sctp](D:\python\webrtc_proxy_py\doc\static\sctp.jpg)

## SCTP

 SCTP (Stream Control Transmission Protocol)是一种传输协议

SCTP是可以确保数据传输的，和TCP类似，也是通过确认机制来实现的。和TCP不同的是：

**1.** **TCP是以字节为单位传输的，SCTP是以数据块为单位传输的**

TCP接收端确认的是收到的字节数，SCTP接收端确认的是接收到的数据块。SCTP的这种数据块（被称为DATA CHUNK）通常会携带应用的一个数据包，或者说是应用要发送的一个消息。

在实际的应用中，TCP发送方的可以将应用程序需要发送的多个消息打包到一个TCP包里面发出去。比如，应用程序连续调用两次send()向对端发送两条消息，TCP协议可能把这两条消息都打包放在同一个TCP包中。接收端在收到这个TCP包时，回给对端的ACK只是表明自己接收到了多少个字节，TCP协议本身并不会把收到的数据重新拆散分成两条应用层消息并通知应用程序去接收。事实上，应用程序可能只需要调用一次receive()，就会把两条消息都收上来，然后应用需要根据应用程序自己定义的格式去拆成两条消息。

与TCP不同，SCTP是将应用程序的每次调用sendmsg()发送的数据当作一个整体，放到一个被称为DATA CHUNK的数据块里面，接收端也是以DATA CHUNK为单位接收数据，并重新组包，通知应用程序接收。通常，应用程序每次调用recvmesg()都会收到一条完整的消息。

在SCTP的发送端，多条短的应用层消息可以被SCTP协议打包放在同一个SCTP包中，此时在SCTP包中可以看到多个DATA CHUNK。另一方面，一条太长（比如，超过了路径MTU）的应用层消息也可能被SCTP协议拆分成多个片段，分别放在多个DATA CHUNK并通过不同的SCTP包发送给对端。这两种情况下，SCTP的接收端都能重新组包，并通知应用程序去接收。

**2.** **TCP通常是单路径传输，SCTP可以多路径传输**

TCP的两端都只能用一个IP来建立连接，连接建立之后就只能用这一对IP来相互收发消息了。如果这一对IP之间的路径出了问题，那这条TCP连接就不可用了。

SCTP不一样的地方是，两端都可以绑定到多个IP上，只要有其中一对IP能通，这条SCTP连接就还可以用。



![img](https://img-blog.csdn.net/20161001154325290?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)![img](https://blog.csdn.net/scutzxb_2/article/details/52717392)

体现在socket API中，TCP只能bind一个IP，而SCTP可以bind到多个IP。

**3.** **TCP是单流有序传输，SCTP可以多流独立有序/无序传输**

一条SCTP连接里面，可以区分多条不同的流（stream），不同的流之间的数据传输互不干扰。这样做理论上的好处是，如果其中某一条流由于丢包阻塞了，那只会影响到这一条流，其他的流并不会被阻塞。但是实际上，如果某一条流由于丢包阻塞，其他的流通常也会丢包，被阻塞，最后导致所有的流都被阻塞，SCTP连接中断。

![img](https://img-blog.csdn.net/20161001154333606?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

在同一条stream里面，SCTP支持有序/无序两种传输方式，应用程序在调用sendmsg()的时候，需要指定用哪一条stream传输，以及指定这条要发送的消息是需要有序传输还是无序传输的。如果在传输过程中丢包，则有序传递模式可能会在接收端被阻塞，而无序传输模式不会在接收端被阻塞。

![img](https://blog.csdn.net/scutzxb_2/article/details/52717392)

**4. TCP连接的建立过程需要三步握手，SCTP连接的建立过程需要四步握手**

TCP连接建立过程，容易受到DoS攻击。在建立连接的时候，client端需要发送SYN给server端，server端需要将这些连接请求缓存下来。通过这种机制，攻击者可以发送大量伪造的SYN包到一个server端，导致server端耗尽内存来缓存这些连接请求，最终无法服务。

SCTP的建立过程需要四步握手，server端在收到连接请求时，不会立即分配内存缓存起来，而是返回一个COOKIE。client端需要回送这个COOKIE，server端校验之后，从cookie中重新获取有效信息（比如对端地址列表），才会最终建立这条连接。这样，可以避免类似TCP的SYN攻击。

应用程序对此感知不到，对应用程序来说，不管是TCP还是SCTP，都只需要在server端listen一个socket，client调用connect()去连接到一个server端。

**5. SCTP有heartbeat机制来管理路径的可用性**

SCTP协议本身有heartbeat机制来监控连接/路径的可用性。

前面说过，SCTP两端都可以bind多个IP，因此同一条SCTP连接的数据可以采用不同的IP来传输。不同的IP传输路径对应一条path，不同的path都可以由heartbeat或者是数据的传输/确认来监控其状态。

如果heartbeat没相应，或者是数据在某条path超时没收到确认导致重传，则认为该path有一次传输失败。如果该path的连续传输失败次数超过path的连续重传次数，则认为该path不可用，并通知应用程序。如果一条连接的连续传输次数超过设定的“连接最大重传次数”，则该连接被认为不可用，该连接会被关闭并通知应用程序。

## DTLS

在 WebRTC 中，为了保证媒体传输的安全性，引入了 DTLS 来对通信过程进行加密。DTLS 的作用、原理与 SSL/TLS 类似，都是为了使得原本不安全的通信过程变得安全。它们的区别点是 DTLS 适用于加密 UDP 通信过程，SSL/TLS 适用于加密 TCP 通信过程，正是由于使用的传输层协议不同，造成了它们实现上面的一些差异。



