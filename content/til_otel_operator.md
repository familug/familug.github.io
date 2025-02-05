Title: [TIL] K8S Opentelemetry operator thêm environment cho pod
Date: 2025-02-05
Category: frontpage
Tags: til, k8s, kubernetes
slug: til-otel-operator

Các kubernetes operator có đủ loại và đủ tính năng, nhưng tự thêm biến environment vào cho pod (sau khi thêm annotations vào pod) thì nay thấy có OpenTelemetry Operator, trích [code](https://github.com/open-telemetry/opentelemetry-operator/blob/6782fdfb2a4cb59541bec2299a4553cd952debee/pkg/instrumentation/sdk.go#L296):

```go
// injectCommonSDKConfig adds common SDK configuration environment variables to the necessary pod
// agentIndex represents the index of the pod the needs the env vars to instrument the application.
// appIndex represents the index of the pod the will produce the telemetry.
// When the pod handling the instrumentation is the same as the pod producing the telemetry agentIndex
// and appIndex should be the same value.  This is true for dotnet, java, nodejs, and python instrumentations.
// Go requires the agent to be a different container in the pod, so the agentIndex should represent this new sidecar
// and appIndex should represent the application being instrumented.
func (i *sdkInjector) injectCommonSDKConfig
    ...
	configureExporter(otelinst.Spec.Exporter, &pod, container)
    ...
```

```go
// https://github.com/open-telemetry/opentelemetry-operator/blob/af567cdfd563e8a5c7a221337c4ff5edfbdf63b9/pkg/instrumentation/exporter.go#L17
func configureExporter(exporter v1alpha1.Exporter, pod *corev1.Pod, container *corev1.Container) {
	if exporter.Endpoint != "" {
		if getIndexOfEnv(container.Env, constants.EnvOTELExporterOTLPEndpoint) == -1 {
			container.Env = append(container.Env, corev1.EnvVar{
				Name:  constants.EnvOTELExporterOTLPEndpoint,
				Value: exporter.Endpoint,
			})
		}
	}
    ...
```


sau khi thêm annotations:

```
annotations:
  instrumentation.opentelemetry.io/inject-sdk: "true"
```


sẽ thêm nhiều environments `OTEL_.*` cho pod.

Hết.
