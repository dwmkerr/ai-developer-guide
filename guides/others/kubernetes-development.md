# Kubernetes Development

## Custom Resource Definitions (CRDs)

CRDs must be well documented with rich comments that become field descriptions in the generated OpenAPI schema and CRD YAML. Use kubebuilder validation tags, as well as  a comment above each field to ensure that a `description` field is set:

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
```

Additional printer columns show essential data in `kubectl get` output:

```bash
NAME              STATUS   AGE
spark-engine      Ready    5m
```

## Status Update Conflicts and Concurrency

When encountering optimistic concurrency conflicts ("object has been modified" errors), avoid retry logic as it masks genuine concurrency issues. Instead, identify why multiple controllers are updating the same resource simultaneously and fix the root cause. Ensure single ownership patterns where only one controller updates a resource's status, and audit your reconciliation logic for race conditions. Kubernetes conflicts typically indicate architectural problems, not transient issues requiring retries.
