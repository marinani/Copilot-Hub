---
description: 'Guidelines for creating risk impact matrices to prioritize software project risks, issues, and technical debt.'
applyTo: '**/*.md'
---

# Risk Impact Matrix for Software Projects

The **risk impact matrix** (also called **impact vs probability matrix**, **risk matrix**) is a widely used tool in **software project management** (and project management in general) to prioritize risks, issues, bugs, technical debt, or even new features/epics.

It helps answer the quick question:
"Which problems or risks should I focus on first?"

### 1. Basic concept

The matrix crosses two main axes:

|                        | Low impact  | Medium impact | High impact |
|------------------------|-------------|---------------|-------------|
| **Low probability**    | Low risk    | Low risk      | Medium risk |
| **Medium probability** | Low risk    | Medium risk   | High risk   |
| **High probability**   | Medium risk | High risk     | High risk   |

Risks that fall into the **red zone (high impact + high probability)** should be addressed with higher urgency.

### 2. How to create an impact matrix for software projects

Practical step-by-step:

1. **List all risks/issues/bugs/technical debt**
   Examples:
    - Authentication service may fail
    - Personal data leak
    - Poor performance during traffic peaks
    - Third-party library deprecated
    - Failure in automated deployment

2. **Define the scales (usually 3 or 5 levels)**
   You can use 3×3 (simpler) or 5×5 (more precise).

   **Impact (one axis) – software examples**
   | Level | Description (real examples)                             | Financial/operational impact |
   |-------|--------------------------------------------------------|------------------------------|
   | 1 | Very low | Minor rework, unnoticed |
   | 2 | Low | Some users affected, support resolves quickly |
   | 3 | Medium | Significant portion of users affected, small revenue loss |
   | 4 | High | Critical system down for hours, large revenue loss |
   | 5 | Critical | Data breach, legal issue, total loss of trust |

   **Probability (the other axis)**
   | Level | Description |
   |-------|-------------|
   | 1 | Very unlikely (< 10%) |
   | 2 | Unlikely (10–30%) |
   | 3 | Possible (30–70%) |
   | 4 | Likely (70–90%) |
   | 5 | Almost certain (> 90%) |

3. **Score each item**
   Bring the technical team + PO + stakeholders together and rate each risk's impact and probability from 1 to 5.

4. **Calculate the risk score**
   There are two common approaches:

   a) **Multiplicative** (most used)
   Risk = Impact × Probability
   Example: Impact 5 × Probability 4 = 20 (very high)

   b) **Qualitative matrix** (3×3 or 5×5 with colors)
   Place the item into a quadrant and define Green/Yellow/Red zones.

   Typical scoring ranges (5×5):
    - 1–6 → Low
    - 8–12 → Medium
    - 15–25 → High/Critical

5. **Create the visual matrix**
   You can use Excel, Google Sheets, Miro, Jira (with plugins), Confluence, Aha!, Azure DevOps, etc.

   Example visual 3×3:

   ```
         High  ◉ ◉ ● ● ●          ← Impact
        Medium ◉ ● ● ●
        Low    ● ● ◉
              Low   Medium  High  → Probability
   ```

   ● = address later
   ◉ = address now

### 3. Real-world examples in software

| Risk                                   | Impact | Probability | Score | Priority           |
|----------------------------------------|--------|-------------|-------|--------------------|
| Payment gateway failure                | 5      | 3           | 15    | High               |
| Visual bug on registration form        | 2      | 5           | 10    | Medium             |
| Third-party library with critical CVE  | 5      | 4           | 20    | Critical (fix now) |
| Slow report during peak hours (2h/day) | 3      | 4           | 12    | High               |
| Manual deploy process error risk       | 4      | 5           | 20    | Critical           |

### 4. Practical tips

- Build the matrix live with the team (a 1-hour workshop often suffices).
- Update it every sprint or after any major incident.
- Use it to justify technical debt to stakeholders ("look at the score 20").
- Combine it with an **effort vs value** matrix for feature prioritization—these tools complement each other.
- In Jira you can create custom fields "Impact" and "Probability" and use a plugin such as "Risk Management" or "Easy Risk Matrix".

### 5. Ready-made templates and resources

- Free Google Sheets 5×5 template: search for "risk matrix template site:vertex42.com"
- Miro has a built-in Risk Matrix template
- PMI Excel templates (available on PMI site)
- Jira plugin: "Risk Register" or "Project Risk Matrix"

## Advanced examples

Here are **advanced, real-world** examples of impact matrices that go beyond the basic 3×3 or 5×5, used by platform engineering, security, SRE and product teams at medium/large companies (e.g., Nubank, Mercado Libre, Netflix, Amazon, Spotify, etc.).

### 1. 5×5 Impact Matrix with Quantified Financial Exposure

Used when you need to justify budget or prioritize for directors/C-level.

| Probability →                                     | Very Low (1) | Low (2) | Medium (3) | High (4) | Almost Certain (5) |
|---------------------------------------------------|--------------|---------|------------|----------|--------------------|
| **Catastrophic (5)** > $5M or total loss of trust | 5            | 10      | 15         | 20       | **25**             |
| **Critical (4)** $1M–5M or outage > 4h            | 4            | 8       | 12         | **16**   | **20**             |
| **Serious (3)** $100k–1M or outage 1–4h           | 3            | 6       | 9          | 12       | 15                 |
| **Moderate (2)** $10k–100k or < 1h                | 2            | 4       | 6          | 8        | 10                 |
| **Negligible (1)** < $10k                         | 1            | 2       | 3          | 4        | 5                  |

**Real examples I've seen with scores 20–25 (handled in 24–48h):**

- Critical vulnerability in the authorization microservice (5 × 5 = 25)
- CI/CD pipeline failure that breaks all deploys (4 × 5 = 20)
- Critical CVE in a library used by all services (5 × 4 = 20)

### 2. Technical Impact + Business Impact Matrix (two-dimensional)

Used by Platform Engineering and Architecture Review Boards.

X-axis = Technical probability of occurrence
Y-axis = Business impact
Each item also receives two extra scores:

- Mitigation cost (in story points or money)
- Time to mitigate (in days/weeks)

| Risk                                        | Prob | BizImp | Score | Mitigation Cost | Time      | Real Priority               |
|---------------------------------------------|------|--------|-------|-----------------|-----------|-----------------------------|
| Monorepo without branch protection          | 5    | 5      | 25    | 80 SP           | 3 sprints | HIGH (but delayed for cost) |
| OpenSearch without replica + failing backup | 4    | 5      | 20    | 20 SP           | 1 sprint  | CRITICAL (fix now)          |
| Old feature flags not removed (500+)        | 3    | 4      | 12    | 200 SP          | 3 months  | Low priority                |

Result: even high-scoring items that are expensive to mitigate can be accepted as technical debt with monitoring.

### 3. Security impact matrix (OWASP style) – 8 factors (Likelihood + Impact)

Used by AppSec teams.

| Factor                    | Weight | Score (1-9) | Points |
|---------------------------|--------|-------------|--------|
| Threat Agent Factors      | –      | –           | –      |
| Skill level               | 1–9    | 9           | 9      |
| Motive                    | 1–9    | 9           | 9      |
| Opportunity               | 0–9    | 5           | 0      |
| Size                      | 1–9    | 6           | 6      |
| **Vulnerability Factors** |        |             |        |
| Ease of discovery         | 1–9    | 9           | 9      |
| Ease of exploit           | 1–9    | 9           | 9      |
| Awareness                 | 1–9    | 8           | 8      |
| Intrusion detection       | 1–9    | 3           | 3      |
| **Technical Impact**      |        |             |        |
| Loss of confidentiality   | 1–9    | 9           | 9      |
| Loss of integrity         | 1–9    | 6           | 6      |
| Loss of availability      | 1–9    | 9           | 9      |
| Loss of accountability    | 1–9    | 5           | 5      |
| **Business Impact**       |        |             |        |
| Financial damage          | 1–9    | 9           | 9      |
| Reputation damage         | 1–9    | 9           | 9      |
| Non-compliance            | 1–9    | 7           | 7      |
| Privacy violation         | 1–9    | 9           | 9      |

Final average = ~7.8 → Critical → goes directly to security sprint.

### 4. Performance impact matrix (used by SRE)

X = Probability of happening at the next peak (Black Friday, etc.)
Y = Severity of impact on latency or error rate

| Probability \ Impact | P99 +100ms | P99 +500ms | P99 +2s  | 5xx > 1% | 5xx > 10%    |
|----------------------|------------|------------|----------|----------|--------------|
| > 90%                | Medium     | High       | Critical | Critical | Catastrophic |
| 50–90%               | Low        | Medium     | High     | Critical | Critical     |
| 10–50%               | Low        | Low        | Medium   | High     | Critical     |
| < 10%                | Monitor    | Low        | Low      | Medium   | High         |

Real example: "Redis cache with wrong TTL" → 90% chance of P99 +2s on Black Friday → Critical → mitigated 1 month before.

### 5. Technical debt impact matrix with "compound interest"

Used by CTOs and VPs of Engineering to decide on large refactors.

| Debt                      | Current Impact | Probability of becoming incident | Monthly interest (% productivity lost) | Time to pay | Priority |
|---------------------------|----------------|----------------------------------|----------------------------------------|-------------|----------|
| Rails 4.2 → 7.x migration | 4              | 5                                | 8–12%                                  | 9 months    | High     |
| 400 dead feature flags    | 3              | 4                                | 5%                                     | 3 months    | Medium   |
| Flaky integration tests   | 4              | 5                                | 15–20% (blocks deploys)                | 6 months    | Critical |

### 6. Automated matrix (the dream for mature teams)

Tools I've seen automate this:

- SonarQube + Security Hot Spots → generates security risk scores
- Snyk + Dependabot → vulnerabilities with CVSS → includes impact/probability
- Datadog APM + Error Tracking → shows "this endpoint is exploding in production" → automatic score
- LaunchDarkly → shows % of traffic exposed to each flag → blast radius risk

Result: a dashboard that updates the risk matrix in near real-time.

## Templates

Below are structured templates for each of the matrices mentioned above.

---

## 🚀 1. RICE Prioritization Matrix (Feature/Product)

The RICE Matrix (Reach, Impact, Confidence, Effort) is ideal for Product Managers and teams who need to prioritize backlog features quantitatively.

The prioritization formula is:

$$RICE = \frac{Reach \times Impact \times Confidence}{Effort}$$

| # | Item/Feature                      | Reach | Impact | Confidence | Effort |                **RICE Score**                | **Priority** |
|:-:|:----------------------------------|:-----:|:------:|:----------:|:------:|:--------------------------------------------:|:------------:|
| 1 | Refactor Login Screen             | 1000  | 2      | 80%        | 5      |  $\frac{1000 \times 2 \times 0.8}{5} = 320$  | Medium       |
| 2 | New Reporting Feature             | 5000  | 3      | 95%        | 15     | $\frac{5000 \times 3 \times 0.95}{15} = 950$ | **High**     |
| 3 | Footer color adjustment           | 2000  | 0.25   | 100%       | 1      | $\frac{2000 \times 0.25 \times 1}{1} = 500$  | Medium       |
| 4 | Checkout optimization             | 3000  | 4      | 70%        | 8      | $\frac{3000 \times 4 \times 0.7}{8} = 1050$  | **Highest**  |

### 📝 Criteria definitions (scoring scale)

| Criterion        | Definition                                                                 | Example scale                        |
|:-----------------|:---------------------------------------------------------------------------|:-------------------------------------|
| **Reach**        | How many people/customers will be affected in a period (e.g., per month).  | Absolute number (e.g., 100 users/month) |
| **Impact**       | How big the benefit will be (e.g., conversion, satisfaction).              | 5 (Massive) to 0.25 (Minimal)         |
| **Confidence**   | How confident you are in the Reach and Impact estimates.                   | Percentage (100%, 80%, 50%, <50%)     |
| **Effort**       | Total development cost (team, design, QA).                                | Number of person-months or story points |

---

## 🚨 2. GUT Prioritization Matrix (Problems/Risks)

The GUT Matrix (Gravity, Urgency, Tendency) is excellent to prioritize problems, bugs, project risks or non-conformities.

Prioritization formula:

$$\text{GUT Score} = Gravity \times Urgency \times Tendency$$

| # | Risk/Problem                               | Gravity (G) | Urgency (U) | Tendency (T) |        **GUT Score**        | **Priority** |               Suggested Action                |
|:-:|:-------------------------------------------|:-----------:|:-----------:|:------------:|:---------------------------:|:------------:|:---------------------------------------------:|
| 1 | Critical failure in payment processor      |      5      |      5      |      4       | $5 \times 5 \times 4 = 100$ | **Highest**  | Immediate action / contingency plan          |
| 2 | Minor layout bug in footer                 |      1      |      2      |      1       | $1 \times 2 \times 1 = 2$   | Low          | Fix in next maintenance cycle                |
| 3 | Single-vendor dependency for an API        |      4      |      3      |      5       | $4 \times 3 \times 5 = 60$  | High         | Mitigate (seek alternative provider)         |

### 📝 Criteria definitions (1–5 scale)

Commonly a 1–5 scale is used, where 5 is the worst-case scenario.

| Criterion       | Definition                                                                                                 | Example scale (1–5)                                       |
|:----------------|:-----------------------------------------------------------------------------------------------------------|:----------------------------------------------------------|
| **Gravity (G)** | The impact if the problem occurs (financial, customer loss, legal, reputation).                           | 1 (No impact) to 5 (Irreparable damage / Business loss)    |
| **Urgency (U)** | How quickly the problem requires attention.                                                               | 1 (Can wait) to 5 (Requires immediate action)              |
| **Tendency (T)**| The likelihood the problem will worsen or increase in impact if left unresolved.                           | 1 (Unlikely to change) to 5 (Rapid and dramatic worsening) |

---
