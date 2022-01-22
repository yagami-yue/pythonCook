## 1.1 FFmpeg的基本组成

FFmpeg的框架基本组成包含：

- AVFormat
- AVCodec
- AVFilter
- AVDevice
- AVUtil

### 1.AVFormat(封装)

​        <font color='red'> <font color='red'>AVFormat</font>中实现了大多数的媒体封装格式</font>，包括了封装和解封装，如MP4，FLV、KV、TS等文件封装格式，取决于编译时是够包含了该格式的封装库，可以根据实际需求扩展自己封装的处理模块



### 2.AVCodec(编解码)

​        <font color='red'>AVCodec中实现了目前多媒体领域绝大多数常用的编解码格式</font>，除了支持MPEG4、AAC、MJPEG等自带的媒体编解码格式之外，还支持第三方的编解码器，如H.264(AVC)编码，需要使用x264编码器，H.265(HEVC)编码，需要使用x265编码器；MP3(mp3lame)编码，需要使用libmp3lame编码器.这一块如果需要增加自己跌编码格式或者硬件编解码则需要在AVCodec中增加相应的编解码模块。



### 3.AVFilter(滤镜模块)

![Snipaste_2022-01-19_15-14-27](D:\study_md_doc\img\Snipaste_2022-01-19_15-14-27.png)

​      <font color='red'> AVFilter库提供了一个通用的音频、视频、字幕等滤镜处理框架</font>。在AVFilter中滤镜框架可以有多个输入输出，在上图中把输入视频切割成两个流，一部分抛给crop和vflip处理，另一部分保持原样，处理完成的流合并到原有的overlay图层中，并显示在最上面一层，输出新的视频。

​      命令：

1.相同的Filter线性链之间用逗号分割

2.不同的Filter线性链之间用分号分割

3.用[]可以对处理后的流打上标签





### 4.FFmpeg的视频图像转换计算模块Swscale

​        swscale模块提供了<font color='red'>高级别的图像转换API</font>，例如它允许进行图像缩放和像素格式转换，常见于将图像从1080p转换成720p或者480p的缩放。或者将图像数据从YUV420P转换成为YUYV或者YUV转RGB等图像格式转换



### 5.FFmpeg的音频转换计算模块swresample

​       该模块提供了<font color='red'>高级别的音频重采样API</font>，例如它允许操作音频采样、音频通道布局转换和布局调整



## 1.2 FFmpeg的编解码工具ffmpeg

​        ffmpeg是FFmpeg源代码编译后生成的一个可执行程序，其可以作为命令行工具来使用。

~~~shell
./ffmpeg -i input.mp4 output.avi
~~~

​		简单的一条ffmpeg命令可以看到ffmpeg可以通过-i参数将后面的文件作为输入源，然后就行转码和转封装操作输出到output.avi中，这一条命令做了三件事：

1.获得源数据

2.转码

3.输出文件

看似简单的工作，不是简单的把 .mp4-> .avi，因为在ffmpeg中MP4跟AVI是两种文件封装格式，并不是后缀名就可以决定的

上述命令可以写成

~~~shell
./ffmpeg -i input.mp4 -f avi output.dat
~~~

-f参数指定了输出文件的容器格式，

ffmpeg的主要工作流程相对比较简单：

1.解封装(Demuxing)

2.解码(Decoding)

3.编码(Encoding)

4.封装(Muxing)

其中需要经过6个步骤：

1.读取输入源

2.进行音视频的解封装

3.解码每一帧音视频数据

4.编码每一帧音视频数据

5.重新封装

6.输出到目标





​		ffmpeg首先读取输入源，然后通过Demuxer将音视频包进行解封装，这个动作通过调用<font color='red'>libavformat</font>中的接口即可实现；接下来通过Decoder进行解码，将音视频通过Decoder解包成为YVU或者PCM这样的数据，Decoder通过<font color='red'>libavcodec</font>中的接口即可实现；然后通过Encoder将对应的数据进行编码，编码也是通过<font color='red'>libavcodec</font>中的接口来实现。接下来将编码后的音视频数据通过<font color='red'>Muxer(libavformat)</font>就行封装输出到目标文件中





## 1.3 FFmpeg的播放器ffplay

​		FFmpeg不但可以转码、转封装,还提供了播放器的相关功能，但是需要一定的SDL的版本来支持

​		<font color='red'>SDL（Simple DirectMedia Layer）</font>是一套[开放源代码](https://baike.baidu.com/item/开放源代码/114160)的跨平台多媒体开发库，使用C语言写成。SDL提供了数种控制图像、声音、输出入的函数，让开发者只要用相同或是相似的代码就可以开发出跨多个平台（Linux、Windows、Mac OS X等）的应用软件。现SDL多用于开发游戏、模拟器、媒体播放器等多媒体应用领域

​		<font color='red'>有时候通过编译产生的ffplay不一定能够成功，因为ffpaly在旧版本依赖SDL1.2,但是ffpaly在新版本依赖于SDL-2.0</font>



## 1.4 FFmpeg的多媒体分析器ffprobe

​		ffprobe也是FFmpeg源码编译后生成的一个可执行程序。ffprobe是一个非常强大的多媒体分析工具，可以从媒体文件或者媒体流中获取媒体信息，如音频的参数，视频的参数、媒体容器的参数信息等。

​		分析文件音频、视频的编码格式，总时长、复合码率等信息。包括每个包的长度，类型、帧的信息等等

~~~shell
./ffprobe -show_streams test.mp4
~~~



2.1 ffmpeg 的封装转换

​		<font color='red'>ffmpeg的封装转换功能包含在AVFormat模块中</font>， 通过libavformat库就行Mux和Demux操作，多媒体文件的格式有很多种，这些格式中的很多参数在Mux和Demux的操作参数中是公用的

​		通过

~~~shell
ffmpeg --help full
~~~

​		找到AVFormatContext参数部分，该参数下的所有参数均为封装转换可使用的参数![Snipaste_2022-01-22_15-44-48](D:\study_md_doc\img\Snipaste_2022-01-22_15-44-48.png)

这些都是通用的封装、解封装操作时使用的参数