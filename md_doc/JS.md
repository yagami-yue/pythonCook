~~~javascript
<script defer src="1.js"></script>
<!-- defer 属性可以让页面渲染完成后再下载解析js脚本，说明该脚本是外部脚本，并且执行时不会对页面造成修改-->
    
    
<script async src="1.js"></script>
<!-- async 属性表示可以不必等脚本下载和执行完后再加载页面，如果有多个js文件都有标记async，那它们之间必须没有依赖关系，因为异步加载，代码顺序≠下载执行顺序-->
    不推荐使用
~~~

