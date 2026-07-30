# Dynamic Question Generation

> **PRINCIPLE (MANDATORY):** Questions are not just data collection — they must **reveal architectural consequences**.
>
> Every question must connect to a concrete implementation decision that affects cost, complexity, or timeline.

---

## Core Principles

### 1. Questions Reveal Consequences

A good question is not "What color do you want?", but rather:

```markdown
BAD: "What authentication method?"
GOOD: "Should users log in with email/password or social login?"

   Impact:
   - Email/Password requires password reset, hashing, 2FA infrastructure
   - Social login requires OAuth providers, profile mapping, less control

   Trade-off: Security vs development time vs user friction
```

### 2. Context Before Content

First understand **where** the request fits:

| Context                       | Focus of Questions                                                            |
| ----------------------------- | ----------------------------------------------------------------------------- |
| **Greenfield** (new project)  | Foundation decisions: stack, hosting, scale                                   |
| **Feature Addition**          | Integration points, existing patterns, breaking changes                       |
| **Refactoring**               | Reason for refactoring: performance? maintainability? what's broken?          |
| **Debug**                     | Symptoms → root cause → reproduction path                                     |

### 3. Minimum Viable Questions

**PRINCIPLE:** Each question must eliminate a fork in the implementation path.

```text
Before the question:
├── Path A: Do X (5 min)
├── Path B: Do Y (15 min)
└── Path C: Do Z (1 hour)

After the question:
└── Confirmed path: Do X (5 min)
```

If the question does not reduce implementation paths → **ELIMINATE IT**.

### 4. Questions Generate Data, Not Assumptions

```markdown
ASSUMPTION: "The user probably wants Stripe"
QUESTION: "Which payment provider best fits your needs?"

   Stripe → great documentation, 2.9% + $0.30, US-focused
   LemonSqueezy → Merchant of Record, 5% + $0.50, global taxes
   Paddle → complex pricing, handles EU VAT, enterprise-focused
```

---

## Question Generation Algorithm

```text
INPUT: User request + Context (greenfield/feature/refactor/debug)
│
├── STEP 1: Interpret Request
│   ├── Extract domain (ecommerce, auth, realtime, cms, etc.)
│   ├── Extract features (explicit and implicit)
│   └── Extract scale indicators (users, data volume, frequency)
│
├── STEP 2: Identify Decision Points
│   ├── What MUST be decided before implementation? (blocking)
│   ├── What CAN be decided later? (deferrable)
│   └── What has ARCHITECTURAL impact? (high impact)
│
├── STEP 3: Generate Questions (Priority Order)
│   ├── P0: Blocking decisions (cannot proceed without answer)
│   ├── P1: High impact (affects >30% of implementation)
│   ├── P2: Medium impact (affects specific features)
│   └── P3: Nice-to-have (edge cases, optimization)
│
└── STEP 4: Format Each Question
    ├── What: clear question
    ├── Why: impact on implementation
    ├── Options: trade-offs (not just A vs B)
    └── Default: what happens if the user doesn't answer
```

---

## Domain-Specific Question Banks

### E-commerce

| Question                          | Why It Matters                                                     | Trade-offs                           |
| --------------------------------- | ------------------------------------------------------------------ | ------------------------------------ |
| **Single or multi-vendor?**       | Multi-vendor requires commission, seller panel, payment split      | +Revenue, -Complexity                |
| **Inventory control?**            | Requires stock tables, reservations, low-stock alerts              | +Accuracy, -Development time         |
| **Digital or physical products?** | Digital requires download links; physical requires shipping/tracking | +Coverage, -Complexity             |
| **Subscription or one-time purchase?** | Subscription requires recurrence, dunning, proration          | +Recurring revenue, -Complexity      |

### Authentication

| Question                         | Why It Matters                                         | Trade-offs                            |
| -------------------------------- | ------------------------------------------------------- | ------------------------------------- |
| **Need social login?**           | OAuth vs full password/reset infrastructure             | +UX, -Control                         |
| **Role-based permissions (RBAC)?** | Requires role tables, policies, and admin UI          | +Security, -Development time          |
| **2FA mandatory?**               | Requires TOTP/SMS, backup codes, and recovery           | +Security, -Friction                  |
| **Email verification?**          | Requires tokens, email service, and resend              | +Security, -Friction at registration  |

### Real-time

| Question                             | Why It Matters                                                       | Trade-offs                      |
| ------------------------------------ | ------------------------------------------------------------------- | ------------------------------- |
| **WebSocket or polling?**            | WS requires connection management and scale; polling is simpler     | +Scale/latency, -Complexity     |
| **Expected concurrent users?**       | <100 can be simple; >1000 requires pub/sub; >10k requires dedicated infra | +Scale, -Complexity          |
| **Message persistence?**             | Requires history, storage cost, and pagination                     | +UX, -Cost                      |
| **Ephemeral or durable?**            | Ephemeral can be in-memory; durable requires write before emit     | +Reliability, -Latency          |

### Content/CMS

| Question                       | Why It Matters                                       | Trade-offs                           |
| ------------------------------ | ---------------------------------------------------- | ------------------------------------ |
| **Rich text or Markdown?**     | Rich text requires sanitization/XSS; Markdown simplifies | +Features, -Complexity            |
| **Draft/publication flow?**    | Requires status, scheduled jobs, versioning          | +Control, -Complexity                |
| **Media handling?**            | Requires upload, storage, and optimization           | +Features, -Development time         |
| **Multi-language?**            | Requires i18n, fallback, and translation UI          | +Reach, -Complexity                  |

---

## Dynamic Question Template

```markdown
Based on your [DOMAIN] [FEATURE] request:

## CRITICAL (Blocking Decisions)

### 1. **[DECISION POINT]**

**Question:** [Clear and specific question]

**Why this matters:**
- [Architectural consequence]
- [Impacts: cost / complexity / timeline / scale]

**Options:**
| Option | Pros         | Cons            | Best for       |
| ------ | ------------ | --------------- | -------------- |
| A      | [Advantage]  | [Disadvantage]  | [Use case]     |
| B      | [Advantage]  | [Disadvantage]  | [Use case]     |

**If not specified:** [Default choice + justification]

---

## HIGH IMPACT (Affects Implementation)

### 2. **[DECISION POINT]**
[Same format]

---

## NICE-TO-HAVE (Edge Cases)

### 3. **[DECISION POINT]**
[Same format]
```

---

## Iterative Questioning

### First Pass (3-5 questions)

Focus on **blocking decisions**. Do not proceed without answers.

### Second Pass (after initial implementation)

When patterns emerge, ask:

- "This feature implies [X]. Should we handle [edge case] now or defer?"
- "We are using [Pattern A]. Should [Feature B] follow the same pattern?"

### Third Pass (optimization)

With functionality already running, ask:

- "There is a performance bottleneck in [X]. Do we optimize now or is it acceptable?"
- "Do we refactor [Y] for maintainability or deliver as-is?"

---

## Example: Complete Question Generation

```text
USER REQUEST: "Build an Instagram clone"

STEP 1: Interpret
├── Domain: Social media
├── Features: Photo sharing, engagement (likes/comments), profiles
├── Implicit: Feed, follow users, authentication
└── Scale: Potentially high

STEP 2: Decision points
├── Blocking: storage strategy, authentication, feed type
├── High impact: real-time notifications, data model
└── Deferrable: analytics, advanced search, reels/video

STEP 3: Generate questions (priority)

P0 (Blocking):
1. Storage strategy → affects architecture, cost, and speed
2. Feed strategy → affects query and complexity
3. Auth method → affects dev time, UX, and security

P1 (High impact):
4. Real-time notifications → WebSocket vs polling
5. Media processing → client-side vs server-side

P2 (Deferrable):
6. Story/Reels → scope risk; push to v2
7. DM/Chat → separate subsystem; push to v2

STEP 4: Format output
```

---

## Generated Output (Example)

```text
Based on your Instagram clone request:

## CRITICAL DECISIONS (Cannot proceed without answers)

### 1. **Photo Storage Strategy**

**Question:** Where will user photos be stored and served?

**Why this matters:**
- Affects monthly cost, loading speed, and CDN complexity
- Scale example: 1000 users x 10 photos x 2MB = 20GB

**Options:**
| Option                   | Cost              | Speed     | Complexity | Best for                    |
| ------------------------ | ----------------- | --------- | ---------- | --------------------------- |
| **Cloudinary**           | $89/month (25GB)  | High (CDN)| Low        | Fast MVP                    |
| **AWS S3 + CloudFront**  | $0.023/GB         | High (CDN)| Medium     | Cost-optimized production   |
| **Supabase Storage**     | Free tier 1GB     | Medium    | Low        | Small scale                 |
| **Local storage**        | Server cost       | Low       | Low        | Development only            |

**If not specified:** Cloudinary (balanced for MVP)

---

### 2. **Feed Algorithm Choice**

**Question:** How should the main feed work?

**Why this matters:**
- Affects query complexity, caching, and development time
- Algorithmic feed requires signals and additional infrastructure

**Options:**
| Option               | Complexity | Database Impact     | Best for              |
| -------------------- | ---------- | ------------------- | --------------------- |
| **Chronological**    | Low        | Simple query        | Initial stage         |
| **Following only**   | Medium     | JOIN + pagination   | Classic social apps   |
| **Algorithmic**      | High       | Pre-computed feed   | Advanced product      |

**If not specified:** Following-based feed

---

### 3. **Authentication Approach**

**Question:** How will registration/login work?

**Why this matters:**
- Affects development time, security posture, and UX friction

**Options:**
| Option            | Dev Time | Security              | UX           | Best for          |
| ----------------- | -------- | --------------------- | ------------ | ----------------- |
| **Email/password**| 4-5h     | High (with 2FA)       | Medium       | Full control      |
| **Social only**   | 1-2h     | Provider-dependent    | Fluid        | Fast B2C          |
| **Magic link**    | 2-3h     | Medium                | Very fluid   | Simplicity focus  |
| **Clerk/Auth0**   | ~1h      | High                  | Fluid        | Time-to-market    |

**If not specified:** Clerk/Auth0 for MVP

---

## HIGH IMPACT

### 4. **Real-Time Notifications**

**Question:** Do you need instant notifications for likes/comments?

**Why this matters:**
- WebSocket increases infrastructure complexity
- Polling is simpler but has higher latency

**Options:**
| Option                 | Complexity | Scale Cost          | Best for           |
| ---------------------- | ---------- | ------------------- | ------------------ |
| **WebSocket + Redis**  | High       | $10+/month          | >1000 concurrent   |
| **Polling (30s)**      | Low        | Database load       | <1000 users        |
| **No real-time**       | None       | None                | Initial MVP        |

**If not specified:** Polling for MVP

---

## NICE-TO-HAVE (v2)

### 5. **Video/Reels Support**
- High complexity (processing/streaming)
- Recommendation: launch with photos and evolve later

### 6. **Direct Messages**
- Separate chat subsystem
- Recommendation: defer to v2

---

## Summary

| Decision    | Recommendation | If Changed              |
| ----------- | -------------- | ----------------------- |
| Storage     | Cloudinary     | +3h setup               |
| Feed        | Following      | +2h query optimization  |
| Auth        | Clerk/Auth0    | -3h dev time            |
| Real-time   | Polling        | +5h WebSocket           |
| Video       | v2             | N/A                     |
| DM          | v2             | N/A                     |

**Estimated MVP time:** 15-20 hours
```

---

## Principle Recap

1. **Every question = architectural decision** → not generic collection.
2. **Expose trade-offs** → user understands consequences.
3. **Prioritize blocking items** → without these, you cannot safely proceed.
4. **Define default** → allows progress if answer is missing.
5. **Be domain-oriented** → questions change by context.
6. **Iterate with implementation progress** → new points emerge along the way.
