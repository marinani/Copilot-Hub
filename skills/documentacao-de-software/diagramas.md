# Diagrams and Visualization

Use diagrams whenever text alone is insufficient to eliminate interpretation ambiguity.

All diagrams are created in **Mermaid.js** and stored in the corresponding type directories within `documentacao/processo_unificado/artefatos_aprovados/`, as defined in `estrutura.md`.

---

## Diagram types and when to use them

### Sequence Diagram

**Prefix:** none (embedded in the requirement or API document)
**Usage:** display interactions between components over time — ideal for API flows, authentication, asynchronous processes.

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant BE as Backend
    participant DB as Database

    U->>FE: Fills form and clicks Save
    FE->>BE: POST /api/v1/resource { payload }
    BE->>DB: EXEC sp_SaveRecord @param1, @param2
    DB-->>BE: Generated ID
    BE-->>FE: 200 OK { id, status }
    FE-->>U: Displays confirmation
```

---

### Use Case Diagram

**Usage:** show system boundaries, actors, and their high-level interactions.

```mermaid
graph LR
    A((User)) --> B[Log in]
    A --> C[Query orders]
    A --> D[Generate report]
    E((Administrator)) --> D
    E --> F[Manage users]
```

---

### Class Diagram (`dcl-`)

**File:** `documentacao/processo_unificado/artefatos_aprovados/diagrama_de_classes/dcl-diagram_name.md`
**Usage:** model code structure, attributes, methods, and relationships between classes.

```mermaid
classDiagram
    class User {
        +int id
        +string name
        +string email
        +authenticate()
    }
    class Order {
        +int id
        +date createdAt
        +calculateTotal()
    }
    User "1" --> "0..*" Order : places
```

---

### System Integration Diagram (`min-`)

**File:** `documentacao/processo_unificado/artefatos_aprovados/diagrama_de_integracao_de_sistemas/min-diagram_name.md`
**Usage:** map data flow between systems, services, and external integrations.

```mermaid
graph TD
    A[Web Application] -->|REST| B[API Gateway]
    B -->|REST| C[Order Service]
    B -->|REST| D[User Service]
    C -->|SQL| E[(Database)]
    C -->|Event| F[Message Queue]
    F -->|Consumes| G[Notification Service]
```

---

### Entity Relationship Diagram (`der-`)

**File:** `documentacao/processo_unificado/artefatos_aprovados/diagrama_de_entidades_e_relacionamento/der-diagram_name.md`
**Usage:** document the data model, entities, attributes, and relationships.

```mermaid
erDiagram
    USER {
        int id PK
        string name
        string email
        date created_at
    }
    ORDER {
        int id PK
        int user_id FK
        date created_at
        decimal total
    }
    USER ||--o{ ORDER : "places"
```

---

### Flow / State Diagram

**Usage:** represent navigation logic, entity states, or flow decisions.

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> InReview : Submit for review
    InReview --> Approved : Approve
    InReview --> Draft : Reject
    Approved --> [*]
```

---

## Usage Guidelines

- Prefer Mermaid.js for all diagrams — keeps documentation versionable alongside the code.
- Use ASCII Mermaid as a fallback only when the tool does not support rendering.
- **Every diagram must have a title and brief description** explaining what it represents.
- Validate Mermaid syntax before finalizing the document.
- Sequence diagrams are **mandatory** in API documents and in requirements describing multi-layer flows.
- ERD and Class diagrams are **mandatory** when the functionality involves a relevant data model.
