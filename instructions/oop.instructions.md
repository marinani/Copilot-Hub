---
name: Object Oriented Programing Instructions
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

### 4.1. Use Clear and Descriptive Names

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

## 5. Practical Examples

### 5.1. Procedural vs. Object-Oriented (C#)

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

## 6. Conclusion

OOP is a powerful paradigm for modeling complex systems, promoting code reuse, and facilitating maintenance. Use practical examples, follow best practices, and adapt the paradigm to your project's context.

---

## Clarifications

This document provides detailed instructions and practical examples to facilitate understanding and application of Object-Oriented Programming in different languages. For questions or suggestions, contact the project documentation owner.
