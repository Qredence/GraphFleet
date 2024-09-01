# md-utils-ts

Tiny markdown utility functions for Typescript.

## Install

Install with npm:

```bash
$ npm install --save md-utils-ts
```

## Usage

See [Implementation](https://github.com/TomPenguin/md-utils-ts/blob/main/src/index.ts) for details.

```ts
import md, { bold } from "md-utils-ts";

const boldText = bold("some text");
console.log(boldText); // "**some text**"

// Use function from the imported 'md'
const italicText = md.italic("Hello, world!");
console.log(italicText); // "_Hello, world!_"
```

## API

> Note: Table is not supported. You can use [markdown-table](https://github.com/wooorm/markdown-table) as well.

## bold

Make the text bold.

### Parameters:

- `text` (string): The input text.

### Example:

```ts
const result = bold("Hello, world!");
// Output: "**Hello, world!**"
```

## italic

Make the text italic.

### Parameters:

- `text` (string): The input text.

### Example:

```ts
const result = italic("Hello, world!");
// Output: "_Hello, world!_"
```

## del

Add strike-through to the text.

### Parameters:

- `text` (string): The input text.

### Example:

```ts
const result = del("Hello, world!");
// Output: "~~Hello, world!~~"
```

## underline

Add underline to the text.

### Parameters:

- `text` (string): The input text.

### Example:

```ts
const result = underline("Hello, world!");
// Output: "<u>Hello, world!</u>"
```

## anchor

Create an anchor link.

### Parameters:

- `text` (string): The anchor text.
- `href` (string): The URL to link to.

### Example:

```ts
const result = anchor("OpenAI", "https://www.openai.com");
// Output: "[OpenAI](https://www.openai.com)"
```

## code

Create a code block or inline code.

### Parameters:

- `inline` (boolean): Whether the code should be inline or in a block.
- `language` (string): The code language for syntax highlighting.
- `text` (string): The code content.

### Example:

````ts
const tsCodeBlock = code(false)("ts");
const result = tsCodeBlock("console.log('Hello, world!');");
// Output:
// "```ts
// console.log('Hello, world!');
// ```"
````

## inlineCode

Create inline code with optional syntax highlighting.

### Parameters:

- `text` (string): The code content.

### Example:

```ts
const code = inlineCode("console.log('Hello, world!');");
// Output:
// "`console.log('Hello, world!');`"
```

## codeBlock

Create a code block with optional syntax highlighting.

### Parameters:

- `language` (string, optional): The code language for syntax highlighting.
- `text` (string): The code content.

### Example:

````ts
const code = codeBlock("ts")("console.log('Hello, world!');");
// Output:
// "```ts
// console.log('Hello, world!');
// ```"
````

## equation

Create an equation block or inline equation.

### Parameters:

- `inline` (boolean): Whether the equation should be inline or in a block.
- `text` (string): The equation content.

### Example:

```ts
const equationBlock = equation(false)("x^2 + y^2 = z^2");
// Output:
// "$$
// x^2 + y^2 = z^2
// $$"

const inlineEquation = equation(true)("E = mc^2");
// Output: "$E = mc^2$"
```

## inlineEquation

Create inline code with optional syntax highlighting.

### Parameters:

- `text` (string): The equation content.

### Example:

```ts
const result = inlineEquation("E = mc^2");
// Output: "$E = mc^2$"
```

## equationBlock

Create an equation block or inline equation.

### Parameters:

- `text` (string): The equation content.

### Example:

```ts
const result = equationBlock("x^2 + y^2 = z^2");
// Output:
// "$$
// x^2 + y^2 = z^2
// $$"
```

## h

Create a heading with the specified level.

### Parameters:

- `level` (number): The level of the heading (1 to 6).
- `text` (string): The heading text.

### Example:

```ts
const heading = h(2)("Hello, world!");
// Output: "## Hello, world!"
```

## h1

Create a level 1 heading.

### Parameters:

- `text` (string): The heading text.

### Example:

```ts
const heading = h1("Title");
// Output:
// # Title
```

## h2

Create a level 2 heading.

### Parameters:

- `text` (string): The heading text.

### Example:

```ts
const heading = h2("Subtitle");
// Output:
// ## Subtitle
```

## h3

Create a level 3 heading.

### Parameters:

- `text` (string): The heading text.

### Example:

```ts
const heading = h3("Subsection");
// Output:
// ### Subsection
```

## h4

Create a level 4 heading.

### Parameters:

- `text` (string): The heading text.

### Example:

```ts
const heading = h4("Subsubsection");
// Output:
// #### Subsubsection
```

## h5

Create a level 5 heading.

### Parameters:

- `text` (string): The heading text.

### Example:

```ts
const heading = h5("Subsubsubsection");
// Output:
// ##### Subsubsubsection
```

## h6

Create a level 6 heading.

### Parameters:

- `text` (string): The heading text.

### Example:

```ts
const heading = h6("Subsubsubsubsection");
// Output:
// ###### Subsubsubsubsection
```

## quote

Convert text to a blockquote.

### Parameters:

- `text` (string): The input text.

### Example:

```ts
const quotedText = quote("This is a quoted text.");
// Output:
// > This is a quoted text.
```

## bullet

Create a bullet point list item.

### Parameters:

- `text` (string): The content of the bullet point.
- `count` (number, optional): The optional index/count of the bullet point.

### Example:

```ts
const bulletPoint = bullet("List item");
// Output:
// - List item

const numberedBulletPoint = bullet("List item", 1);
// Output:
// 1. List item
```

## todo

Create a todo list item.

### Parameters:

- `text` (string): The content of the todo item.
- `checked` (boolean): Whether the todo item is checked or not.

### Example:

```ts
const uncheckedTodo = todo("Task to be done", false);
// Output:
// - [ ] Task to be done

const checkedTodo = todo("Completed task", true);
// Output:
// - [x] Completed task
```

## image

Create an image element.

### Parameters:

- `alt` (string): The alt text for the image.
- `href` (string): The URL of the image.

### Example:

```ts
const imageElement = image("Description", "https://example.com/image.jpg");
// Output:
// ![Description](https://example.com/image.jpg)
```

## divider

Create a horizontal divider.

### Example:

```ts
const dividerElement = divider();
// Output:
// ---
```

## details

Create a collapsible details element.

### Parameters:

- `summary` (string): The summary text for the details element.
- `details` (string): The details/content of the details element.

### Example:

```ts
const detailsElement = details("Click to expand", "Hidden content");
// Output:
// <details>
// <summary>Click to expand</summary>
//
// Hidden content
// </details>
```

## sup

Create a superscript text.

### Parameters:

- `text` (string): The input text.

### Example:

```ts
const superscriptText = sup("2");
// Output:
// <sup>2</sup>
```

## sub

Create a subscript text.

### Parameters:

- `text` (string): The input text.

### Example:

```ts
const subscriptText = sub("2");
// Output:
// <sub>2</sub>
```

## indent

Indent the text with a specified number of spaces.

### Parameters:

- `space` (number, default: 2): The number of spaces to indent with.
- `text` (string): The input text.
- `level` (number, default: 1): The level of indentation.

### Example:

```ts
const indentedText = indent(4)("Indented text", 2);
// Output:
// "    Indented text"
```
