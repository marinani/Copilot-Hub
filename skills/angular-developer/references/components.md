# Components

Angular components are the fundamental building blocks of an application. Each component consists of a TypeScript class with behaviors, an HTML template, and a CSS selector.

## Component Definition

Use the `@Component` decorator to define a component's metadata. **Note**: In this project, inline templates and styles are prohibited.

```ts
@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [...],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {
  save() {
    /* ... */
  }
}
```

## Mandatory Structure

Every component MUST follow these strict rules:

- **Directory**: Must have its own directory with the suffix `-component` (e.g., `profile-component`).
- **Mandatory Files**: Exactly 4 files per directory:
  1. `[name].component.ts`
  2. `[name].component.html`
  3. `[name].component.css`
  4. `[name].component.spec.ts`

## Metadata Options

- `selector`: The CSS selector that identifies this component in templates.
- `templateUrl`: **Mandatory**. Path to an external HTML file.
- `styleUrl` / `styleUrls`: **Mandatory**. Path(s) to external CSS file(s).
- `imports`: Lists the components, directives, or pipes used in this component's template.
- `template` / `styles`: **Prohibited**. Use external files instead.

## Using Components

To use a component, add it to the `imports` array of the consuming component and use its selector in the template.

```ts
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ProfileComponent],
  templateUrl: './app.component.html',
})
export class AppComponent {}
```

## CLI Commands

To generate a component following these standards:
`ng generate component [name] --inline-style=false --inline-template=false`
(Remember to rename the directory to include the `-component` suffix).

## Template Control Flow

Angular uses built-in blocks for conditional rendering and loops.

### Conditional Rendering (`@if`)

Use `@if` to conditionally show content. You can include `@else if` and `@else` blocks.

```html
@if (user.isAdmin) {
<admin-dashboard />
} @else if (user.isModerator) {
<mod-dashboard />
} @else {
<standard-dashboard />
}
```

**Result aliasing**: Save the result of the expression for reuse.

```html
@if (user.settings(); as settings) {
<p>Theme: {{ settings.theme }}</p>
}
```

### Loops (`@for`)

The `@for` block iterates over collections. The `track` expression is **required** for performance and DOM reuse.

```html
<ul>
  @for (item of items(); track item.id; let i = $index, total = $count) {
  <li>{{ i + 1 }}/{{ total }}: {{ item.name }}</li>
  } @empty {
  <li>No items to display.</li>
  }
</ul>
```

**Implicit Variables**: `$index`, `$count`, `$first`, `$last`, `$even`, `$odd`.

### Switching Content (`@switch`)

The `@switch` block renders content based on a value. It uses strict equality (`===`) and has **no fallthrough**.

```html
@switch (status()) { @case ('loading') { <app-spinner /> } @case ('error') { <app-error-msg /> }
@case ('success') { <app-data-grid /> } @default {
<p>Unknown status</p>
} }
```

**Exhaustive Type Checking**: Use `@default never;` to ensure all cases of a union type are handled.

```html
@switch (state) { @case ('on') { ... } @case ('off') { ... } @default never; // Errors if a new
state like 'standby' is added }
```

## Core Concepts

- **Host Element**: The DOM element that matches the component's selector.
- **View**: The DOM rendered by the component's template inside the host element.
- **Standalone**: By default, components are standalone (since Angular 19, `standalone: true` is default). For older versions, `standalone: true` must be explicit or the component must be part of an `NgModule`.
- **Component Tree**: Angular applications are structured as a tree of components, where each component can host child components.
- **Component Naming**: Component classes MUST use the `Component` suffix (e.g., `ProfileComponent`). The directory name MUST include the `-component` suffix (e.g., `profile-component`).
- **Standardization**: This project enforces a strict 4-file structure with no exceptions for small components.
