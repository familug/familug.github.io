Title: Chơi CTF giúp gì cài OpenSearch?
Date: 2024-07-12
Category: frontpage
Tags: elasticsearch, CTF, opensearch, podman


## OpenSearch vs ElasticSearch
[OpenSearch](https://opensearch.org/) là 1 bản fork của Amazon từ ElasticSearch, sau [vụ đổi license đình đám từ công ty Elastic](https://www.elastic.co/blog/why-license-change-aws) đứng sau ElasticSearch không muốn Amazon thu lời từ sản phẩm open-source của họ.
OpenSearch ngày càng khác biệt với ElasticSearch, mang theo những ưu / nhược điểm riêng.

Một nhược điểm là nó fork từ bản cũ của ElasticSearch, nên nhiều lỗi còn rất khó đọc. Bài này nhờ kỹ năng chơi [CTF](https://pp.pymi.vn/article/pymictf/) với team PyMi mà giải quyết một vấn đề đau đầu.

Một ưu điểm là OpenSearch hỗ trợ login bằng SSO: SAML, OIDC, LDAP... còn ElasticSearch phải trả phí.

### Chạy 1 node trên máy bằng podman (docker)
podman là 1 phần mềm phát triển bởi RedHat thay thế cho docker, sau khi docker đổi qua tính phí trên Desktop (DockerDesktop), podman dần trở nên phổ biến.
Câu lệnh podman tương thích với docker nên chỉ cần thay chữ `podman` trong bài thành `docker` là được. Bài này chạy bằng podman trên máy để bạn đọc có thể làm theo, thực tế chạy trên 1 K8S cluster

Chạy 1 container opensearch theo hướng dẫn tại [trang dockerhub](https://hub.docker.com/r/opensearchproject/opensearch), thấy rất nhiều log:


```
$ podman run -it -p 9200:9200 -p 9600:9600 -e OPENSEARCH_INITIAL_ADMIN_PASSWORD=daemonH4gx@4 -e "discovery.type=single-node" --name opensearch-node docker.io/opensearchproject/opensearch:2.15.0

Enabling OpenSearch Security Plugin
Enabling execution of install_demo_configuration.sh for OpenSearch Security Plugin 
OpenSearch 2.12.0 onwards, the OpenSearch Security Plugin a change that requires an initial password for 'admin' user. 
Please define an environment variable 'OPENSEARCH_INITIAL_ADMIN_PASSWORD' with a strong password string. 
If a password is not provided, the setup will quit. 
 For more details, please visit: https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/
### OpenSearch Security Demo Installer
### ** Warning: Do not use on production or public reachable systems **
OpenSearch install type: rpm/deb on Linux 6.5.0-41-generic amd64
OpenSearch config dir: /usr/share/opensearch/config/
OpenSearch config file: /usr/share/opensearch/config/opensearch.yml
OpenSearch bin dir: /usr/share/opensearch/bin/
OpenSearch plugins dir: /usr/share/opensearch/plugins/
OpenSearch lib dir: /usr/share/opensearch/lib/
Detected OpenSearch Version: 2.15.0
Detected OpenSearch Security Version: 2.15.0.0
Admin password set successfully.
### Success
...
[2024-07-12T13:16:30,697][INFO ][o.o.s.c.ConfigurationRepository] [00a159b488ac] Node '00a159b488ac' initialized
```

server đã mặc định setup sẵn SSL/TLS port 9200.

Sau khi cài lên trên k8s cluster, bỗng dưng xuất hiện hàng đống log error như sau, dễ dàng tìm trên mạng

```
[2024-07-12T13:16:36,456][ERROR][o.o.h.n.s.SecureNetty4HttpServerTransport] [00a159b488ac] Exception during establishing a SSL connection: io.netty.handler.ssl.NotSslRecordException: not an SSL/TLS record: 474554202f20485454502f312e310d0a486f73743a206c6f63616c686f73743a393230300d0a557365722d4167656e743a206375726c2f372e38312e300d0a4163636570743a202a2f2a0d0a0d0a
io.netty.handler.ssl.NotSslRecordException: not an SSL/TLS record: 474554202f20485454502f312e310d0a486f73743a206c6f63616c686f73743a393230300d0a557365722d4167656e743a206375726c2f372e38312e300d0a4163636570743a202a2f2a0d0a0d0a
	at io.netty.handler.ssl.SslHandler.decodeJdkCompatible(SslHandler.java:1314) ~[netty-handler-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.handler.ssl.SslHandler.decode(SslHandler.java:1387) ~[netty-handler-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.handler.codec.ByteToMessageDecoder.decodeRemovalReentryProtection(ByteToMessageDecoder.java:530) ~[netty-codec-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.handler.codec.ByteToMessageDecoder.callDecode(ByteToMessageDecoder.java:469) ~[netty-codec-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.handler.codec.ByteToMessageDecoder.channelRead(ByteToMessageDecoder.java:290) ~[netty-codec-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:444) [netty-transport-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:420) [netty-transport-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:412) [netty-transport-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.channel.DefaultChannelPipeline$HeadContext.channelRead(DefaultChannelPipeline.java:1407) [netty-transport-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:440) [netty-transport-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:420) [netty-transport-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.channel.DefaultChannelPipeline.fireChannelRead(DefaultChannelPipeline.java:918) [netty-transport-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.channel.nio.AbstractNioByteChannel$NioByteUnsafe.read(AbstractNioByteChannel.java:166) [netty-transport-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.channel.nio.NioEventLoop.processSelectedKey(NioEventLoop.java:788) [netty-transport-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.channel.nio.NioEventLoop.processSelectedKeysPlain(NioEventLoop.java:689) [netty-transport-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.channel.nio.NioEventLoop.processSelectedKeys(NioEventLoop.java:652) [netty-transport-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.channel.nio.NioEventLoop.run(NioEventLoop.java:562) [netty-transport-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.util.concurrent.SingleThreadEventExecutor$4.run(SingleThreadEventExecutor.java:994) [netty-common-4.1.110.Final.jar:4.1.110.Final]
	at io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74) [netty-common-4.1.110.Final.jar:4.1.110.Final]
	at java.base/java.lang.Thread.run(Thread.java:1583) [?:?]
```

nhưng ai gửi request http đến địa chỉ này?
### Tìm ai gửi request

Các phương án:

- cài tcpdump, ngrep để dump traffic pod 9200 xem nội dung traffic, không dễ cài được package nếu image đã remove các package manager (như dùng distroless images)
- đọc log?! ai đọc stacktrace Java???

Giải pháp là đọc log, phần nội dung bí hiểm trong log message: 

> 474554202f20485454502f312e310d0a486f73743a206c6f63616c686f73743a393230300d0a557365722d4167656e743a206375726c2f372e38312e300d0a4163636570743a202a2f2a0d0a0d0a

chứa chuỗi 45 47 55 ... các ký tự từ a-e từ 0-9... với kinh nghiệm chơi các bài dễ trong các giải CTF, đoán ngay dùng hex <https://n.pymi.vn/base16.html> để xem là gì. Bật Python:

```py
>>> s = "474554202f20485454502f312e310d0a486f73743a206c6f63616c686f73743a393230300d0a557365722d4167656e743a206375726c2f372e38312e300d0a4163636570743a202a2f2a0d0a0d0a"
>>> bytes.fromhex(s)
b'GET / HTTP/1.1\r\nHost: localhost:9200\r\nUser-Agent: curl/7.81.0\r\nAccept: */*\r\n\r\n'
```

đọc được nội dung của request đã gửi tới server.

Trên thực tế, đống log spam có User-Agent là 1 chương trình monitoring, từ đó tìm ra và tắt nó đi.

PS: có thể dùng <https://gchq.github.io/CyberChef/> để decode hex.

## Kết luận
Chơi CTF không bổ ngang thì bổ dọc,
không bổ dọc thì lại bổ ngang.
Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
