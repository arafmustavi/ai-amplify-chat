# Architecture

## Strategy pattern for inference

`app.py` is a thin conductor. All heavy lifting sits behind
`amplify.backends.base.BaseInferenceBackend` — a two-method contract:

```python
class BaseInferenceBackend(ABC):
    def warmup(self) -> None: ...
    @abstractmethod
    def generate(self, prompt: str) -> tuple[str, float]: ...
```

At boot, `get_backend(settings.BACKEND)` returns the correct adapter. Route
handlers never branch on backend name — they just call `.generate()`.

## Request lifecycle

```mermaid
sequenceDiagram
    participant U as User (browser)
    participant N as nginx
    participant A as Flask app
    participant S as Sanitizer
    participant B as Backend
    participant L as ChatLogger (CSV)

    U->>N: POST /chat {message}
    N->>A: proxy
    A->>S: sanitize_for_model()
    A->>B: generate(prompt)
    B-->>A: (response, latency_ms)
    A->>L: append row (thread-safe)
    A-->>U: {response, latency_ms, backend}
```
