# Kubernetes Development

## Custom Resource Definitions (CRDs)

CRDs must be well documented with rich comments. Essential fields should be shown. Use kubebuilder validation tags:

```go
// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
// +kubebuilder:printcolumn:name="Status",type="string",JSONPath=".status.phase"
// +kubebuilder:printcolumn:name="Age",type="date",JSONPath=".metadata.creationTimestamp"
type ExecutionEngine struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   ExecutionEngineSpec   `json:"spec,omitempty"`
    Status ExecutionEngineStatus `json:"status,omitempty"`
}

type ExecutionEngineSpec struct {
    // +kubebuilder:validation:Required
    // Address configuration for the execution service endpoint
    Address AddressSpec `json:"address"`
    
    // +kubebuilder:validation:Optional
    // +kubebuilder:default=30
    // Timeout in seconds for data workload execution
    TimeoutSeconds int32 `json:"timeoutSeconds,omitempty"`
}

type ExecutionEngineStatus struct {
    // +kubebuilder:validation:Optional
    // Current phase of the ExecutionEngine (Pending, Ready, Error)
    Phase string `json:"phase,omitempty"`
    
    // +kubebuilder:validation:Optional
    // Human-readable message describing the current status
    Message string `json:"message,omitempty"`
}
```

Additional printer columns show essential data in `kubectl get` output:

```bash
NAME              STATUS   AGE
spark-engine      Ready    5m
```
