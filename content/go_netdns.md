Title: antigravity agy failed to login, it's always DNS
Date: 20260630
Category: frontpage
Tags: golang, dns, network 
Slug: go_netdns

On one cool mid summer not so good day, `agy` suddenly failed to login with error:

> Got an error: token exchange failed: Post "https://oauth2.googleapis.com/token": dial tcp: lookup oauth2.googleapis.com: no such host

So it clearly is a network issue, but what?

## It is NOT DNS
```
$ dig oauth2.googleapis.com +short
142.251.8.95
```

dig works, so it is **NOT** DNS, right?

But ping / curl fail:

```
$ ping -c1 oauth2.googleapis.com  -t 2
zsh: alarm      ping -c1 oauth2.googleapis.com -t 2
$ curl -v https://oauth2.googleapis.com  --max-time 5
* Resolving timed out after 5005 milliseconds
* Closing connection
curl: (28) Resolving timed out after 5005 milliseconds
```

And both error messages from `agy` and `curl` says "lookup"/"resolve", it must be DNS.

## It must be DNS
A search for `dial tcp: lookup no such host` return a Go issue <https://github.com/golang/go/issues/41425>. AI would also very good at detect language used base on error message. `agy` is a Go program, so it means "it is a DNS issue hit a Go program".

## The fix
Go net package <https://pkg.go.dev/net#hdr-Name_Resolution> writes:

> The resolver decision can be overridden by setting the netdns value of the GODEBUG environment variable (see package runtime) to go or cgo, as in:

```
GODEBUG=netdns=go agy   # force pure Go resolver
```

and problem solved.

## The problem
It turns out the MacOS DNS daemon failed after multiple sleep/wakeup cycles.

```
sudo killall -HUP mDNSResponder
```

would give a new fresh one and now everything is fresh, again.

### Kết luận
It's always DNS.

### Tham khảo
- <https://pkg.go.dev/net#hdr-Name_Resolution>

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
