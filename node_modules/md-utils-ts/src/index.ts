/**
 * Make the text bold.
 * @param text - The input text.
 * @returns The input text wrapped in double asterisks.
 */
export const bold = (text: string) => `**${text}**`;

/**
 * Make the text italic.
 * @param text - The input text.
 * @returns The input text wrapped in underscores.
 */
export const italic = (text: string) => `_${text}_`;

/**
 * Add strike-through to the text.
 * @param text - The input text.
 * @returns The input text wrapped in double tildes.
 */
export const del = (text: string) => `~~${text}~~`;

/**
 * Add underline to the text.
 * @param text - The input text.
 * @returns The input text wrapped in <u> tags.
 */
export const underline = (text: string) => `<u>${text}</u>`;

/**
 * Create an anchor link.
 * @param text - The anchor text.
 * @param href - The URL to link to.
 * @returns An anchor link in markdown format.
 */
export const anchor = (text: string, href: string) => `[${text}](${href})`;

/**
 * Create a code block or inline code.
 * @param inline - Whether the code should be inline or in a block.
 * @param language - The code language for syntax highlighting.
 * @param text - The code content.
 * @returns A code block or inline code in markdown format.
 */
export const code =
  (inline = false) =>
  (language = "") =>
  (text: string) => {
    const signature = inline ? "`" : "```";
    const lang = inline ? "" : language;
    const delimiter = inline ? "" : "\n";
    return [signature + lang, text, signature].join(delimiter);
  };

/**
 * Create inline code with optional syntax highlighting.
 * @param text - The code content.
 * @returns Inline code in markdown format.
 */
export const inlineCode = code(true)();

/**
 * Create a code block with optional syntax highlighting.
 * @param language - The code language for syntax highlighting (optional).
 * @param text - The code content.
 * @returns A code block in markdown format.
 */
export const codeBlock = code();

/**
 * Create an equation block or inline equation.
 * @param inline - Whether the equation should be inline or in a block.
 * @param text - The equation content.
 * @returns An equation block or inline equation in markdown format.
 */
export const equation =
  (inline = false) =>
  (text: string) => {
    const signature = inline ? "$" : "$$";
    const delimiter = inline ? "" : "\n";
    return [signature, text, signature].join(delimiter);
  };

/**
 * Create an inline equation in markdown format.
 * @param text - The equation content.
 * @returns An inline equation enclosed in '$' delimiters.
 */
export const inlineEquation = equation(true);

/**
 * Create an equation block in markdown format.
 * @param text - The equation content.
 * @returns An equation block enclosed in '$$' delimiters.
 */
export const equationBlock = equation();

/**
 * Create a heading with the specified level.
 * @param level - The level of the heading (1 to 6).
 * @param text - The heading text.
 * @returns A heading in markdown format.
 */
export const h =
  (level = 1) =>
  (text: string) =>
    `${"#".repeat(level)} ${text}`;

/**
 * Create a level 1 heading.
 */
export const h1 = h();

/**
 * Create a level 2 heading.
 */
export const h2 = h(2);

/**
 * Create a level 3 heading.
 */
export const h3 = h(3);

/**
 * Create a level 4 heading.
 */
export const h4 = h(4);

/**
 * Create a level 5 heading.
 */
export const h5 = h(5);

/**
 * Create a level 6 heading.
 */
export const h6 = h(6);

/**
 * Alias for creating headings.
 */
export const heading = h;

/**
 * Convert text to a blockquote.
 * @param text - The input text.
 * @returns The input text indented and prefixed with ">".
 */
export const quote = (text: string) =>
  text
    .split("\n")
    .map((line) => `> ${line}`)
    .join("\n");

/**
 * Create a bullet point list item.
 * @param text - The content of the bullet point.
 * @param count - The optional index/count of the bullet point.
 * @returns A bullet point item in markdown format.
 */
export const bullet = (text: string, count?: number) =>
  count ? `${count}. ${text}` : `- ${text}`;

/**
 * Create a todo list item.
 * @param text - The content of the todo item.
 * @param checked - Whether the todo item is checked or not.
 * @returns A todo list item in markdown format.
 */
export const todo = (text: string, checked: boolean) =>
  checked ? `- [x] ${text}` : `- [ ] ${text}`;

/**
 * Create an image element.
 * @param alt - The alt text for the image.
 * @param href - The URL of the image.
 * @returns An image element in markdown format.
 */
export const image = (alt: string, href: string) =>
  href.startsWith("data:")
    ? `![${alt}](data:image/png;base64,${href.split(",").pop()})`
    : `![${alt}](${href})`;

/**
 * Create a horizontal divider.
 * @returns A horizontal divider in markdown format.
 */
export const hr = () => `---`;

/**
 * Create a collapsible details element.
 * @param summary - The summary text for the details element.
 * @param details - The details/content of the details element.
 * @returns A details element in markdown format.
 */
export const details = (summary: string, details: string) => `<details>
<summary>${summary}</summary>

${details}
</details>`;

/**
 * Create a superscript text.
 * @param text - The input text.
 * @returns The input text wrapped in <sup> tags.
 */
export const sup = (text: string) => `<sup>${text}</sup>`;

/**
 * Create a subscript text.
 * @param text - The input text.
 * @returns The input text wrapped in <sub> tags.
 */
export const sub = (text: string) => `<sub>${text}</sub>`;

/**
 * Indent the text with a specified number of spaces.
 * @param space - The number of spaces to indent with.
 * @param text - The input text.
 * @param level - The level of indentation.
 * @returns The input text with added indentation.
 */
export const indent =
  (space = 2) =>
  (text: string, level = 1) => {
    const tab = " ".repeat(space);

    return text
      .split("\n")
      .map((line) => tab.repeat(level) + line)
      .join("\n");
  };
