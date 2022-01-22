main.py 启动参数说明

  -h, --help     show this help message and exit
  --h  H          指定host 默认localhost
  --p  P          指定port 默认 5678
  --appid      指定appid (必传)

文件目录说明:

启动文件上一级需要有bin目录打包py文件

pyinstall -D/-F ./src/main.py

-F 生成exe需要在外面有bin目录(跟外层bin目录内容相同)

-D 生成exe也需要在exe文件上一级bin目录,两种方式打完包都需要在exe文件同级新建一个logs目录

前端连接使用原始websocket连接，地址类似

```
ws://localhost:9876
```

连接到以后发送字符串 'start'，服务端会反传一个'start'

然后开始传二进制的音频数据，如果收到字符串'awake'说明唤醒成功,收到'not awake'说明唤醒失败

默认需要传递字符串'end',结束本次唤醒



