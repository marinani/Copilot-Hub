---
name: object-oriented-programing
description: Instructions for object oriented programing
---

# Object-Oriented Programming (OOP)

## 1. Introduction

Object-Oriented Programming (OOP) is a software development paradigm based on the concept of "objects"—abstractions that represent real-world entities or domain concepts. Each object encapsulates data (attributes/properties) and behavior (methods/functions), enabling modular, reusable, and maintainable code.

### 1.1. Simple Example (Python)

---

## 3. Pros and Cons of OOP

### 3.1. Advantages

- **Natural modeling**: brings code closer to real-world concepts
- **Reusability**: inheritance and composition facilitate code reuse
- **Maintainability**: changes are localized to classes
- **Scalability**: large systems become more manageable

### 3.2. Disadvantages

- **Learning curve**: can be harder for beginners
- **Overhead**: may be overkill for simple problems
- **Performance**: sometimes less efficient than procedural approaches

---

## 4. OOP Best Practices

### 4.1. Core Architectural Philosophy

- **Program to an Interface, not an Implementation:** Always favor abstract classes or interfaces over concrete implementations. Use dependency injection to provide concrete instances.
- **Favor Object Composition over Class Inheritance:** Use composition to combine behaviors dynamically at runtime. Avoid deep inheritance trees. Use Delegation where appropriate to reuse behavior without breaking encapsulation.
- **Encapsulate What Varies:** Identify the aspects of the application that vary and separate them from what stays the same. Use patterns like Strategy, State, or Bridge to isolate these variations.
- **Loose Coupling:** Minimize direct dependencies between classes. Use Mediator, Observer, or abstract factories to keep components decoupled.

### 4.2. Use Clear and Descriptive Names

Class, method, and attribute names should reflect their purpose.

```csharp
// Bad:
class P {
    int i;
    void f() { }
}

// Good:
class Product {
    private int quantity;
    public void UpdateStock(int newQuantity) {
        quantity = newQuantity;
    }
}
```

### 4.2. Encapsulate Sensitive Data

Use access modifiers (private, protected, public) to protect attributes and expose only what is necessary.

```csharp
class CheckingAccount {
    private decimal balance;
    public CheckingAccount(decimal initialBalance) {
        balance = initialBalance;
    }
    public void Deposit(decimal amount) {
        balance += amount;
    }
    public decimal GetBalance() {
        return balance;
    }
}

// Usage:
var account = new CheckingAccount(1000);
account.Deposit(250);
Console.WriteLine(account.GetBalance()); // 1250
```

### 4.3. Prefer Composition Over Inheritance

Composition allows greater flexibility and lower coupling between classes.

```csharp
class Engine {
    public void Start() => Console.WriteLine("Engine started");
}

class Car {
    private Engine engine = new Engine();
    public void StartCar() {
        engine.Start();
    }
}

// Usage:
var car = new Car();
car.StartCar();
```

### 4.4. Use Interfaces for Abstraction

Interfaces define contracts and facilitate testing and maintenance.

```csharp
interface INotification {
    void Send(string message);
}

class Email : INotification {
    public void Send(string message) {
        Console.WriteLine($"Sending email: {message}");
    }
}

class SMS : INotification {
    public void Send(string message) {
        Console.WriteLine($"Sending SMS: {message}");
    }
}

// Usage:
INotification notification = new Email();
notification.Send("Hello!");
notification = new SMS();
notification.Send("Hi!");
```

### 4.5. Follow SOLID Principles

Follow the SOLID principles to create robust and maintainable OOP systems:

- **S**: Single Responsibility Principle
- **O**: Open/Closed Principle
- **L**: Liskov Substitution Principle
- **I**: Interface Segregation Principle
- **D**: Dependency Inversion Principle

#### Example: Single Responsibility Principle

```csharp
class ReportGenerator {
    public void Generate() {
        // ... generates report
    }
}

class EmailSender {
    public void Send(string recipient) {
        // ... sends email
    }
}
```

// Uso:
var carro = new Carro();
carro.LigarCarro();

````

### 4. Utilize interfaces para abstração

Interfaces permitem definir contratos e facilitam testes e manutenção.

```csharp
interface INotificacao {
	void Enviar(string mensagem);
}

class Email : INotificacao {
	public void Enviar(string mensagem) {
		Console.WriteLine($"Enviando email: {mensagem}");
	}
}

class SMS : INotificacao {
	public void Enviar(string mensagem) {
		Console.WriteLine($"Enviando SMS: {mensagem}");
	}
}

// Uso:
INotificacao notificacao = new Email();
notificacao.Enviar("Olá!");
notificacao = new SMS();
notificacao.Enviar("Oi!");
````

### 5. Princípios SOLID

Siga os princípios SOLID para criar sistemas orientados a objetos robustos e de fácil manutenção:

- **S**: Single Responsibility Principle (Responsabilidade Única)
- **O**: Open/Closed Principle (Aberto/Fechado)
- **L**: Liskov Substitution Principle (Substituição de Liskov)
- **I**: Interface Segregation Principle (Segregação de Interface)
- **D**: Dependency Inversion Principle (Inversão de Dependência)

#### Exemplo de Responsabilidade Única:

```csharp
class GeradorDeRelatorio {
	public void Gerar() {
		// ... gera relatório
	}
}

class EnviadorDeEmail {
	public void Enviar(string destinatario) {
		// ... envia email
	}
}
```

---

## 5. Design Patterns Guidelines

Apply Gang of Four (GoF) patterns and SOLID principles to ensure clean, maintainable, and scalable code.

### 5.1. Creational Patterns

- **Abstract Factory:** Use when a system must be configured with one of multiple families of related products. Ensure clients only interact with the abstract factory and abstract product interfaces.
- **Factory Method:** Use when a class cannot anticipate the class of objects it must create. Defer instantiation to subclasses.
- **Builder:** Use when constructing a complex object requires a step-by-step process.
- **Singleton:** Use *only* when absolutely necessary. Prefer Dependency Injection where possible.
- **Prototype:** Use to avoid building a class hierarchy of factories or when cloning is cheaper than scratch creation.

### 5.2. Structural Patterns

- **Adapter:** Use to make incompatible interfaces work together. Prefer Object Adapters (composition).
- **Bridge:** Use to separate an abstraction from its implementation.
- **Composite:** Use to represent part-whole hierarchies.
- **Decorator:** Use to attach additional responsibilities to an object dynamically.
- **Facade:** Use to provide a simple, unified interface to a complex subsystem.
- **Flyweight:** Use to minimize memory usage by sharing state.
- **Proxy:** Use to control access to another object (e.g., lazy loading, security).

### 5.3. Behavioral Patterns

- **Strategy:** Use to define a family of algorithms and make them interchangeable.
- **Observer:** Use to define a one-to-many dependency for automatic updates.
- **Command:** Use to encapsulate a request as an object (essential for undo/redo).
- **State:** Use when an object's behavior depends on its internal state.
- **Template Method:** Use to define the algorithm skeleton in a base class, deferring steps to subclasses.
- **Chain of Responsibility:** Use to pass a request along a chain of handlers.
- **Mediator:** Use to centralize complex communications between objects.
- **Iterator:** Use to sequentially access elements of an aggregate object.
- **Visitor:** Use to define new operations on an object structure without changing its classes.
- **Memento:** Use to capture and restore an object's internal state.

---

## 6. Code Generation & Quality Rules

### 6.1. Pattern Application
- **Pattern Recognition:** When solving problems that map to a GoF pattern, explicitly mention the pattern in comments.
- **Interface First:** Generate the interface/abstract base class *before* concrete implementations.
- **Naming:** Use pattern names in class names where it aids understanding (e.g., `TaxCalculationStrategy`).

### 6.2. SOLID Enforcement
- **SRP:** Ensure each class has only one reason to change.
- **OCP:** Design for extension, not modification.
- **LSP:** Subclasses must be substitutable for base classes.
- **ISP:** Favor specific interfaces over general-purpose ones.
- **DIP:** Depend on abstractions, not concretions.

### 6.3. Logging & Error Handling
- **Fail Safe:** Fail loud, clear, and early.
- **Context:** Log errors with sufficient context. Avoid silent failures.
- **Levels:** Use appropriate log levels (info, debug, warning, error, critical) in every class and function.

### 6.4. Documentation Standards
- **Intent:** Explain *why* a pattern was chosen.
- **Format:** Use docstrings (English). Default to the **numpy pattern** for parameters/returns unless the project uses another.
- **Diagrams:** Use Mermaid/UML diagrams to represent complex relationships.
- **Structure:** Divide into user (how to use) and developer (how it works) documentation.

---

## 7. Practical Examples

### 7.1. Procedural vs. Object-Oriented (C#)

// Procedural

```csharp
decimal balance = 1000;
void Deposit(decimal amount) {
    balance += amount;
}
Deposit(200);
Console.WriteLine(balance); // 1200
```

// Object-Oriented

```csharp
class Account {
    private decimal balance;
    public Account(decimal initialBalance) {
        balance = initialBalance;
    }
    public void Deposit(decimal amount) {
        balance += amount;
    }
    public decimal GetBalance() => balance;
}

var account = new Account(1000);
account.Deposit(200);
Console.WriteLine(account.GetBalance()); // 1200
```

---

## 8. Conclusion

OOP is a powerful paradigm for modeling complex systems, promoting code reuse, and facilitating maintenance. Use practical examples, follow best practices, and adapt the paradigm to your project's context.

---

## Clarifications

This document provides detailed instructions and practical examples to facilitate understanding and application of Object-Oriented Programming in different languages. For questions or suggestions, contact the project documentation owner.
