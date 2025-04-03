Title: AWS SDK không tự chuyển tới S3 bucket khác region
Date: 2025/04/04
Category: frontpage
Tags: aws, boto3, python, java
Slug: aws-s3-cross

AWS cloud hỗ trợ tới hơn 10 ngôn ngữ lập trình khác nhau với bộ SDK cho riêng từng ngôn ngữ.
AWS SDK cho mỗi language có nhiều điểm khác nhau về các hoạt động có thể gây bất ngờ.
Bài này bàn về sự khác biệt của Java SDK v2 so với Python SDK boto3 khi truy cập 1 bucket ở khác region.

### S3 là dịch vụ toàn cầu, nhưng dữ liệu nằm ở 1 region cố định
S3 là dịch vụ toàn cầu, cụ thể là không tồn tại 2 bucket cùng tên, mỗi tên bucket là duy nhất. 
Thế nhưng dữ liệu S3 bucket thì lại nằm ở 1 region cụ thể khi nó được tạo.

Nếu bucket tạo ở `us-east-1`, dữ liệu sẽ nằm ở `us-east-1`, khi code chạy ở region `ap-southeast-1`, mặc định code sẽ truy cập tới bucket ở region `ap-southeast-1`, và nhận được HTTP status code 301.

### Python Boto3 tự chuyển tới region khác
Một ví dụ nhặt ở trên mạng: 
```
2022-09-30 15:51:09,844 botocore.utils [DEBUG] S3 client configured for region us-east-1 but the bucket testbucket2ffd929fin is in region us-west-2; Please configure the proper region to avoid multiple unnecessary redirects and signing attempts.
2022-09-30 15:51:09,844 botocore.utils [DEBUG] Updating URI from https://s3.amazonaws.com/testbucket2ffd929fin to https://s3.us-west-2.amazonaws.com/testbucket2ffd929fin
```

<https://stackoverflow.com/questions/73910120/can-i-disable-region-redirector-s3regionredirector-in-boto3>

cho thấy botocore (thư viện bên dưới boto3) mặc định sẽ nhận kết quả 301 rồi tự động chuyển kết nối tới đúng region nhận được từ error 301.

Code [botocore](https://github.com/boto/botocore/blob/71c41781a74c55e9f64c2424d6c11513b9ee704d/botocore/utils.py#L1806C1-L1836C1)
```py
logger.debug(
    f"S3 client configured for region {client_region} but the bucket {bucket} "
    f"is in region {new_region}; Please configure the proper region to "
    f"avoid multiple unnecessary redirects and signing attempts."
)
# Adding the new region to _cache will make construct_endpoint() to
# use the new region as value for the AWS::Region builtin parameter.
self._cache[bucket] = new_region

# Re-resolve endpoint with new region and modify request_dict with
# the new URL, auth scheme, and signing context.
ep_resolver = self._client._ruleset_resolver
ep_info = ep_resolver.construct_endpoint(
    operation_model=operation,
    call_args=request_dict['context']['s3_redirect']['params'],
    request_context=request_dict['context'],
)
request_dict['url'] = self.set_request_url(
    request_dict['url'], ep_info.url
)
request_dict['context']['s3_redirect']['redirected'] = True
```

### Java SDK v2.x không tự chuyển region

Doc AWS <https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/s3-cross-region.html>
```java
S3AsyncClient client = S3AsyncClient.builder()
                                    .crossRegionAccessEnabled(true)
                                    .build();
```

Nếu quên set `.crossRegionAccessEnabled(true)`, code sẽ fail vì không redirect tới đúng region. Khi code chỉ hỗ trợ 1 region, lỗi này sẽ ít xảy ra, nhưng nếu code cần chạy ở region khác (như hỗ trợ Disaster Recovery),
thì bất ngờ này sẽ chỉ xảy ra lúc đã quá muộn...

> How the SDK provides cross-Region access

> When you reference an existing bucket in a request, such as when you use the putObject method, the SDK initiates a request to the Region configured for the client.
> If the bucket does not exist in that specific Region, the error response includes the actual Region where the bucket resides. The SDK then uses the correct Region in a second request.
> To optimize future requests to the same bucket, the SDK caches this Region mapping in the client.
                            
### Kết luận
Python SDK và Java SDK cho AWS có nhiều khác biệt. Python rất tiện lợi, dynamic nên khi chuyển sang các ngôn ngữ khác sẽ gặp rất nhiều sự cứng nhắc.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
