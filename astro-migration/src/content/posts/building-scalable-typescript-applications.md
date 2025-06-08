---
title: Building Scalable TypeScript Applications
date: 2025-06-06
categories: 
  - TypeScript
  - Architecture
  - Web Development
tags: 
  - typescript
  - architecture
  - scalability
  - patterns
  - clean-code
excerpt: Explore proven architectural patterns and best practices for building maintainable and scalable TypeScript applications.
author: Lars van Blitterswijk
draft: false
---

# Building Scalable TypeScript Applications: Architecture Patterns and Best Practices

As TypeScript continues to gain popularity in enterprise development, building scalable and maintainable applications becomes increasingly important. This post explores proven architectural patterns and best practices that will help you create robust TypeScript applications.

## Why Architecture Matters

Good architecture is the foundation of any successful software project. It provides:

- **Maintainability** - Easy to understand and modify
- **Scalability** - Can grow with your business needs
- **Testability** - Components can be easily tested in isolation
- **Flexibility** - Adaptable to changing requirements
- **Team productivity** - Clear structure helps teams work efficiently

## Core Architectural Principles

### 1. Separation of Concerns

Divide your application into distinct layers, each with a specific responsibility:

```typescript
// Domain layer - Business logic
export class User {
  constructor(
    private readonly id: UserId,
    private readonly email: Email,
    private readonly name: UserName
  ) {}

  public changeEmail(newEmail: Email): void {
    // Business rules for email change
    if (this.email.equals(newEmail)) {
      throw new Error('New email must be different from current email');
    }
    
    this.email = newEmail;
  }
}

// Application layer - Use cases
export class ChangeUserEmailUseCase {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly emailService: EmailService
  ) {}

  async execute(userId: string, newEmail: string): Promise<void> {
    const user = await this.userRepository.findById(new UserId(userId));
    const email = new Email(newEmail);
    
    user.changeEmail(email);
    
    await this.userRepository.save(user);
    await this.emailService.sendEmailChangeNotification(user);
  }
}

// Infrastructure layer - External concerns
export class PostgresUserRepository implements UserRepository {
  async findById(id: UserId): Promise<User> {
    // Database-specific implementation
  }
  
  async save(user: User): Promise<void> {
    // Database-specific implementation
  }
}
```

### 2. Dependency Inversion

Depend on abstractions, not concretions:

```typescript
// Define interfaces for dependencies
interface PaymentGateway {
  processPayment(amount: Money, card: CreditCard): Promise<PaymentResult>;
}

interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: OrderId): Promise<Order>;
}

// Business logic depends on abstractions
export class OrderService {
  constructor(
    private readonly paymentGateway: PaymentGateway,
    private readonly orderRepository: OrderRepository
  ) {}

  async processOrder(orderRequest: OrderRequest): Promise<Order> {
    const order = Order.create(orderRequest);
    
    const paymentResult = await this.paymentGateway.processPayment(
      order.totalAmount,
      orderRequest.creditCard
    );
    
    if (paymentResult.isSuccessful) {
      order.markAsPaid();
      await this.orderRepository.save(order);
    }
    
    return order;
  }
}
```

### 3. Single Responsibility Principle

Each class should have one reason to change:

```typescript
// Bad: Multiple responsibilities
class UserService {
  validateUser(user: User): boolean { /* validation logic */ }
  saveUser(user: User): Promise<void> { /* database logic */ }
  sendWelcomeEmail(user: User): Promise<void> { /* email logic */ }
}

// Good: Single responsibilities
class UserValidator {
  validate(user: User): ValidationResult {
    // Only validation logic
  }
}

class UserRepository {
  async save(user: User): Promise<void> {
    // Only data persistence logic
  }
}

class EmailService {
  async sendWelcomeEmail(user: User): Promise<void> {
    // Only email sending logic
  }
}
```

## Advanced Patterns

### 1. Domain-Driven Design (DDD)

Organize code around business domains:

```typescript
// Value Objects
export class Email {
  private constructor(private readonly value: string) {
    if (!this.isValid(value)) {
      throw new Error('Invalid email format');
    }
  }

  static create(value: string): Email {
    return new Email(value);
  }

  private isValid(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }

  toString(): string {
    return this.value;
  }
}

// Entities
export class User {
  constructor(
    private readonly id: UserId,
    private email: Email,
    private readonly createdAt: Date
  ) {}

  changeEmail(newEmail: Email): DomainEvent[] {
    const oldEmail = this.email;
    this.email = newEmail;
    
    return [new UserEmailChangedEvent(this.id, oldEmail, newEmail)];
  }
}

// Aggregates
export class Order {
  private constructor(
    private readonly id: OrderId,
    private readonly customerId: CustomerId,
    private readonly items: OrderItem[],
    private status: OrderStatus
  ) {}

  static create(customerId: CustomerId, items: OrderItem[]): Order {
    const id = OrderId.generate();
    const status = OrderStatus.PENDING;
    
    return new Order(id, customerId, items, status);
  }

  addItem(item: OrderItem): void {
    if (this.status !== OrderStatus.PENDING) {
      throw new Error('Cannot add items to non-pending order');
    }
    
    this.items.push(item);
  }
}
```

### 2. CQRS (Command Query Responsibility Segregation)

Separate read and write operations:

```typescript
// Commands - Write operations
export interface Command {
  readonly type: string;
}

export class CreateUserCommand implements Command {
  readonly type = 'CREATE_USER';
  
  constructor(
    public readonly email: string,
    public readonly name: string
  ) {}
}

export class CreateUserCommandHandler {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly eventBus: EventBus
  ) {}

  async handle(command: CreateUserCommand): Promise<void> {
    const user = User.create(
      Email.create(command.email),
      UserName.create(command.name)
    );
    
    await this.userRepository.save(user);
    await this.eventBus.publish(new UserCreatedEvent(user.id));
  }
}

// Queries - Read operations
export interface Query<T> {
  readonly type: string;
}

export class GetUserByIdQuery implements Query<UserView> {
  readonly type = 'GET_USER_BY_ID';
  
  constructor(public readonly userId: string) {}
}

export class GetUserByIdQueryHandler {
  constructor(private readonly userReadModel: UserReadModel) {}

  async handle(query: GetUserByIdQuery): Promise<UserView> {
    return this.userReadModel.findById(query.userId);
  }
}
```

### 3. Event-Driven Architecture

Use events for loose coupling:

```typescript
// Domain Events
export abstract class DomainEvent {
  readonly occurredOn: Date = new Date();
  readonly eventId: string = crypto.randomUUID();
  
  abstract readonly eventName: string;
}

export class UserRegisteredEvent extends DomainEvent {
  readonly eventName = 'USER_REGISTERED';
  
  constructor(
    public readonly userId: string,
    public readonly email: string
  ) {
    super();
  }
}

// Event Handlers
export class SendWelcomeEmailHandler {
  constructor(private readonly emailService: EmailService) {}

  async handle(event: UserRegisteredEvent): Promise<void> {
    await this.emailService.sendWelcomeEmail({
      to: event.email,
      userId: event.userId
    });
  }
}

export class CreateUserProfileHandler {
  constructor(private readonly profileService: ProfileService) {}

  async handle(event: UserRegisteredEvent): Promise<void> {
    await this.profileService.createDefaultProfile(event.userId);
  }
}

// Event Bus
export class EventBus {
  private handlers = new Map<string, Array<(event: DomainEvent) => Promise<void>>>();

  subscribe<T extends DomainEvent>(
    eventName: string, 
    handler: (event: T) => Promise<void>
  ): void {
    if (!this.handlers.has(eventName)) {
      this.handlers.set(eventName, []);
    }
    
    this.handlers.get(eventName)!.push(handler);
  }

  async publish(event: DomainEvent): Promise<void> {
    const handlers = this.handlers.get(event.eventName) || [];
    
    await Promise.all(
      handlers.map(handler => handler(event))
    );
  }
}
```

## Testing Strategies

### Unit Testing

Test business logic in isolation:

```typescript
describe('User', () => {
  it('should change email when provided with valid new email', () => {
    // Arrange
    const user = User.create(
      Email.create('old@example.com'),
      UserName.create('John Doe')
    );
    const newEmail = Email.create('new@example.com');

    // Act
    const events = user.changeEmail(newEmail);

    // Assert
    expect(user.email.toString()).toBe('new@example.com');
    expect(events).toHaveLength(1);
    expect(events[0]).toBeInstanceOf(UserEmailChangedEvent);
  });

  it('should throw error when trying to change to same email', () => {
    // Arrange
    const email = Email.create('test@example.com');
    const user = User.create(email, UserName.create('John Doe'));

    // Act & Assert
    expect(() => user.changeEmail(email))
      .toThrow('New email must be different from current email');
  });
});
```

### Integration Testing

Test component interactions:

```typescript
describe('ChangeUserEmailUseCase', () => {
  let useCase: ChangeUserEmailUseCase;
  let userRepository: jest.Mocked<UserRepository>;
  let emailService: jest.Mocked<EmailService>;

  beforeEach(() => {
    userRepository = {
      findById: jest.fn(),
      save: jest.fn(),
    };
    
    emailService = {
      sendEmailChangeNotification: jest.fn(),
    };

    useCase = new ChangeUserEmailUseCase(userRepository, emailService);
  });

  it('should change user email and send notification', async () => {
    // Arrange
    const userId = 'user-123';
    const newEmail = 'new@example.com';
    const user = User.create(
      Email.create('old@example.com'),
      UserName.create('John Doe')
    );
    
    userRepository.findById.mockResolvedValue(user);

    // Act
    await useCase.execute(userId, newEmail);

    // Assert
    expect(userRepository.save).toHaveBeenCalledWith(user);
    expect(emailService.sendEmailChangeNotification).toHaveBeenCalledWith(user);
  });
});
```

## Performance Considerations

### Lazy Loading

Load resources only when needed:

```typescript
class ModuleLoader {
  private modules = new Map<string, Promise<any>>();

  async loadModule(moduleName: string): Promise<any> {
    if (!this.modules.has(moduleName)) {
      const modulePromise = this.createModuleLoader(moduleName)();
      this.modules.set(moduleName, modulePromise);
    }
    
    return this.modules.get(moduleName)!;
  }

  private createModuleLoader(moduleName: string): () => Promise<any> {
    switch (moduleName) {
      case 'analytics':
        return () => import('./analytics/AnalyticsModule');
      case 'reporting':
        return () => import('./reporting/ReportingModule');
      default:
        throw new Error(`Unknown module: ${moduleName}`);
    }
  }
}
```

### Caching Strategies

Implement efficient caching:

```typescript
interface CacheStrategy<T> {
  get(key: string): Promise<T | null>;
  set(key: string, value: T, ttl?: number): Promise<void>;
  invalidate(key: string): Promise<void>;
}

class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly cache: CacheStrategy<User>
  ) {}

  async getUserById(id: string): Promise<User> {
    const cacheKey = `user:${id}`;
    
    // Try cache first
    const cachedUser = await this.cache.get(cacheKey);
    if (cachedUser) {
      return cachedUser;
    }

    // Fallback to repository
    const user = await this.userRepository.findById(new UserId(id));
    
    // Cache for future requests
    await this.cache.set(cacheKey, user, 300); // 5 minutes TTL
    
    return user;
  }
}
```

## Conclusion

Building scalable TypeScript applications requires careful consideration of architecture patterns and best practices. Key takeaways:

1. **Apply SOLID principles** consistently throughout your codebase
2. **Use Domain-Driven Design** to organize complex business logic
3. **Implement proper separation of concerns** with layered architecture
4. **Leverage TypeScript's type system** for better code quality
5. **Write comprehensive tests** at all levels
6. **Consider performance implications** of architectural decisions

Remember, architecture is not about following patterns blindly but about choosing the right patterns for your specific context and requirements.

---

*What architectural patterns have you found most effective in your TypeScript projects? Share your experiences on [Twitter](https://twitter.com/Larsjelle18) or connect with me on [LinkedIn](https://www.linkedin.com/in/lars-van-blitterswijk/)!*
