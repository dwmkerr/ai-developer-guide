# Go

Follow Go idioms and conventions. Write idiomatic Go, not Java or Python in Go syntax.

## Project Structure

Standard Go layout:
- `/cmd` - main application entry points (one subdirectory per executable)
- `/internal` - private code that cannot be imported by other projects
- `/pkg` - public libraries safe for external use
- NO `/src` directory (not idiomatic in Go)
- Keep `main` packages minimal; put logic in importable packages

```
project/
├── cmd/
│   ├── server/main.go
│   └── cli/main.go
├── internal/
│   ├── auth/
│   └── handler/
└── pkg/
    └── models/
```

Reference: https://github.com/golang-standards/project-layout

## Naming

- **Exported**: PascalCase (e.g., `UserService`, `Config`)
- **Unexported**: camelCase (e.g., `userData`, `handleRequest`)
- **Acronyms**: All caps (e.g., `HTTPServer`, `IDToken`, not `HttpServer`, `IdToken`)
- **Getters**: No "Get" prefix (e.g., `user.Name()`, not `user.GetName()`)
- **Interfaces**: Use `-er` suffix for single-method interfaces (e.g., `Reader`, `Writer`, `Stringer`)
- **Packages**: Short, lowercase, singular form (e.g., `time`, `http`, not `times`, `utils`)

## Error Handling

Always check and handle errors. Never ignore them with `_`.

```go
// Don't do this - ignoring errors:
data, _ := ioutil.ReadFile("file.txt")

// Do this - always handle errors:
data, err := ioutil.ReadFile("file.txt")
if err != nil {
    return fmt.Errorf("reading config: %w", err)
}
```

- Use `fmt.Errorf` with `%w` to wrap errors with context
- Return errors rather than using `panic` for normal flows
- Error strings should be lowercase and not end with punctuation
- Create custom error types for specific cases
- Use `errors.Is()` and `errors.As()` for error comparison
- Return early on errors to avoid deep nesting

## Testing

- Write table-driven tests for multiple scenarios
- Use subtests with `t.Run()` for organizing related cases
- Test both success and error paths
- Use `testify/assert` or `testify/require` for cleaner assertions
- Place tests in same package with `_test.go` suffix
- Aim for 80%+ test coverage

```go
func TestParseConfig(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        wantErr bool
    }{
        {"valid config", `{"port": 8080}`, false},
        {"invalid json", `{broken`, true},
        {"empty input", ``, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            _, err := ParseConfig(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("got error=%v, wantErr=%v", err, tt.wantErr)
            }
        })
    }
}
```

## Concurrency

- Use channels for communication between goroutines
- Use `sync.Mutex` for shared memory access
- Always use `context.Context` for cancellation and timeouts
- Beware of goroutine leaks - ensure all goroutines can exit
- Use `sync.WaitGroup` for waiting on multiple goroutines
- Use `errgroup` for handling errors from multiple goroutines

```go
// Don't do this - goroutine leak (never exits):
go func() {
    for {
        doWork()
    }
}()

// Do this - provide exit mechanism:
go func() {
    for {
        select {
        case <-ctx.Done():
            return
        case work := <-workCh:
            doWork(work)
        }
    }
}()
```

## Code Organization

- Organize by domain functionality, not by layer (avoid `/models`, `/controllers` structure)
- Keep functions focused on single responsibility (< 50 lines)
- Limit parameters (aim for ≤ 3; use structs or options pattern for more)
- Use function options pattern for complex constructors
- Prefer composition over embedding
- Keep exported API surface minimal

## Performance

- Profile before optimizing (`pprof`)
- Use `strings.Builder` for string concatenation, not `+=`
- Pre-allocate slices when size is known: `make([]T, 0, capacity)`
- Use pointers judiciously; prefer values for small structs (< 64 bytes)
- Use `sync.Pool` for frequently allocated objects
- Batch database operations

## Dependencies

- Use Go modules (`go.mod`, `go.sum`)
- Run `go mod tidy` to clean up unused dependencies
- Pin versions for stability in production
- Keep dependencies minimal
- Regularly update for security fixes (`go get -u`)
- Document external dependencies in README

## Code Quality

Use `golangci-lint` with these essential linters:
- `gofmt` / `goimports` - standard formatting (always run before commit)
- `govet` - detect suspicious constructs
- `staticcheck` - advanced static analysis
- `errcheck` - ensure errors are handled
- `gosec` - security issues
- `revive` - style checks

Group imports: stdlib, external packages, internal packages (with blank lines between).

```go
import (
    "context"
    "fmt"

    "github.com/pkg/errors"
    "go.uber.org/zap"

    "github.com/myorg/myproject/internal/config"
)
```

## Documentation

- Every exported symbol MUST have a doc comment
- Comments start with the symbol name: `// User represents...`
- Use full sentences with proper punctuation
- Package-level comment at top of one file explains package purpose
- Use godoc format for documentation
- Include examples for complex functions

```go
// Package auth provides user authentication and authorization.
package auth

// Authenticate verifies credentials and returns a session token.
// Returns an error if authentication fails.
func Authenticate(email, password string) (string, error) {
    // implementation
}
```

## Security

- Never hardcode secrets; use environment variables or secret managers
- Use `crypto/rand` for random generation, not `math/rand`
- Use prepared statements for SQL queries (prevent injection)
- Set timeouts on HTTP clients and servers
- Validate and sanitize all user input
- Use `crypto/subtle` for constant-time comparisons of sensitive data
- Use TLS for network communications

## Common Pitfalls

**Range loop variable capture**:
```go
// Don't do this - all goroutines see last value:
for _, v := range items {
    go func() {
        process(v) // Wrong!
    }()
}

// Do this - pass value explicitly:
for _, v := range items {
    go func(item Item) {
        process(item)
    }(v)
}
```

**Pointer to loop variable**:
```go
// Don't do this - all pointers point to same variable:
for _, v := range items {
    results = append(results, &v)
}

// Do this - shadow variable first:
for _, v := range items {
    v := v
    results = append(results, &v)
}
```

## Reference Projects

Excellent examples of idiomatic Go:
- [Kubernetes](https://github.com/kubernetes/kubernetes) - Large-scale project structure
- [Docker](https://github.com/moby/moby) - CLI patterns and architecture
- [Terraform](https://github.com/hashicorp/terraform) - Plugin architecture
- [Hugo](https://github.com/gohugoio/hugo) - Fast build tool patterns
- [CockroachDB](https://github.com/cockroachdb/cockroach) - Database patterns
