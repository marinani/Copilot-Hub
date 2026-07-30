---
name: angular-material
description: "Instruções consolidadas para uso do Angular Material 20, incluindo instalação, configuração, componentes e CDK."
---

# Instruções Consolidadas para Angular Material 20

## Introdução

Angular Material 20 oferece componentes UI baseados no Material Design 3, compatíveis com Angular 20. Foco em componentes standalone, acessibilidade e responsividade.

## Instalação

Execute no diretório do projeto:

```bash
ng add @angular/material
```

Durante a instalação, selecione tema, tipografia e animações.

## Configuração

### Tema e Customização

Edite `styles.scss` para customizar cores:

```scss
@use "@angular/material" as mat;
$primary: mat.define-palette(mat.$indigo-palette);
$theme: mat.define-light-theme(
  (
    color: (
      primary: $primary,
    ),
  )
);
@include mat.core();
@include mat.all-component-themes($theme);
```

Para temas escuros, use `mat.define-dark-theme()`.

### Standalone Components

Importe módulos diretamente nos componentes (padrão no Angular 20).

## Componentes Principais

### Botões

```ts
import { MatButtonModule } from "@angular/material/button";

@Component({
  standalone: true,
  imports: [MatButtonModule],
  template: `
    <button mat-raised-button color="primary">Raised</button>
    <button mat-stroked-button color="accent">Stroked</button>
    <button mat-flat-button color="warn">Flat</button>
  `,
})
export class ButtonComponent {}
```

### Toolbar

```ts
import { MatToolbarModule } from "@angular/material/toolbar";

@Component({
  standalone: true,
  imports: [MatToolbarModule],
  template: `
    <mat-toolbar color="primary">
      <span>Título</span>
      <span class="spacer"></span>
      <button mat-icon-button><mat-icon>menu</mat-icon></button>
    </mat-toolbar>
  `,
})
export class ToolbarComponent {}
```

### Formulários e Inputs

```ts
import { MatInputModule, MatFormFieldModule } from "@angular/material/input";
import { FormsModule } from "@angular/forms";

@Component({
  standalone: true,
  imports: [MatInputModule, MatFormFieldModule, FormsModule],
  template: `
    <mat-form-field appearance="outline">
      <mat-label>Nome</mat-label>
      <input matInput [(ngModel)]="nome" />
    </mat-form-field>
  `,
})
export class InputComponent {
  nome = "";
}
```

### Diálogos

```ts
import { MatDialog, MatDialogModule } from "@angular/material/dialog";

@Component({
  standalone: true,
  imports: [MatDialogModule],
  template: `<button (click)="openDialog()">Abrir</button>`,
})
export class DialogComponent {
  constructor(private dialog: MatDialog) {}

  openDialog() {
    this.dialog.open(DialogContentComponent);
  }
}
```

### Tabelas

```ts
import { MatTableModule } from "@angular/material/table";

@Component({
  standalone: true,
  imports: [MatTableModule],
  template: `
    <table mat-table [dataSource]="data">
      <ng-container matColumnDef="name">
        <th mat-header-cell *matHeaderCellDef>Nome</th>
        <td mat-cell *matCellDef="let item">{{ item.name }}</td>
      </ng-container>
      <tr mat-header-row *matHeaderRowDef="['name']"></tr>
      <tr mat-row *matRowDef="let row; columns: ['name']"></tr>
    </table>
  `,
})
export class TableComponent {
  data = [{ name: "Exemplo" }];
}
```

### Cards

```ts
import { MatCardModule } from "@angular/material/card";

@Component({
  standalone: true,
  imports: [MatCardModule],
  template: `
    <mat-card>
      <mat-card-title>Título</mat-card-title>
      <mat-card-content>Conteúdo</mat-card-content>
    </mat-card>
  `,
})
export class CardComponent {}
```

### Snackbar

```ts
import { MatSnackBar } from "@angular/material/snack-bar";

@Component({
  template: `<button (click)="show()">Mostrar</button>`,
})
export class SnackbarComponent {
  constructor(private snackbar: MatSnackBar) {}

  show() {
    this.snackbar.open("Mensagem", "Fechar");
  }
}
```

## Angular CDK

O CDK fornece blocos de construção reutilizáveis para acessibilidade, layout, interações e tabelas.

### Exemplos

#### Drag & Drop

```ts
import { CdkDragDrop, moveItemInArray } from "@angular/cdk/drag-drop";

@Component({
  template: `
    <ul cdkDropList (cdkDropListDropped)="drop($event)">
      <li *ngFor="let item of items" cdkDrag>{{ item }}</li>
    </ul>
  `,
})
export class DragDropComponent {
  items = ["Item 1", "Item 2"];

  drop(event: CdkDragDrop<string[]>) {
    moveItemInArray(this.items, event.previousIndex, event.currentIndex);
  }
}
```

#### Virtual Scroll

```ts
import { CdkVirtualScrollViewport } from "@angular/cdk/scrolling";

@Component({
  template: `
    <cdk-virtual-scroll-viewport itemSize="50" style="height: 400px;">
      <div *cdkVirtualFor="let item of items">{{ item }}</div>
    </cdk-virtual-scroll-viewport>
  `,
})
export class VirtualScrollComponent {
  items = Array.from({ length: 10000 }, (_, i) => i);
}
```

#### BreakpointObserver

```ts
import { BreakpointObserver, Breakpoints } from "@angular/cdk/layout";

@Component({
  template: `<div [ngClass]="{ mobile: isMobile }">Layout</div>`,
})
export class ResponsiveComponent implements OnInit {
  isMobile = false;

  constructor(private breakpoint: BreakpointObserver) {}

  ngOnInit() {
    this.breakpoint
      .observe([Breakpoints.Handset])
      .subscribe((state) => (this.isMobile = state.matches));
  }
}
```

## Novidades no Angular Material 20

- Suporte aprimorado a Material Design 3.
- Melhorias em acessibilidade e performance.
- Migração: Use `ng update @angular/material`.

## Dicas Finais

- Use `color` para temas (primary, accent, warn).
- Garanta acessibilidade com ARIA.
- Teste com Jasmine/Karma.
- Consulte [material.angular.dev](https://material.angular.dev/) para detalhes.

---

## Mudanças do Angular 19 para 20

- **Reatividade**: Estabilização de signals e linkedSignal.
- **Performance**: Zoneless change detection e incremental hydration.
- **Breaking Changes**: Standalone como padrão; depreciação de ngIf/ngFor.
- **Migração**: Use `ng update @angular/core@20`.

## Zoneless no Angular 20

Ative zoneless para performance sem Zone.js:

```ts
// main.ts
import { provideExperimentalZonelessChangeDetection } from "@angular/core";

bootstrapApplication(AppComponent, {
  providers: [provideExperimentalZonelessChangeDetection()],
});
```

Remova `zone.js` do polyfills.ts.

## Integração Zoneless + NgRx

Use `@ngrx/signals` para estado reativo sem Zone.js.

Exemplo básico:

```ts
import { signalStore, withState, withMethods } from "@ngrx/signals";

export const CounterStore = signalStore(
  withState({ count: 0 }),
  withMethods((store) => ({
    increment: () => store.count.update((v) => v + 1),
  })),
);
```
