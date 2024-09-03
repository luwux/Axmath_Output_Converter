    Warning: This program is created by a newbee, so it might be filled with mistakes and non-standard code.

For reasons I don't fully understand, when using Axmath to create TeX content, including equations and descriptions, there is no option to copy your content to the clipboard and paste it directly into LaTeX files with proper compilation. If you do, what you get is just a bunch of things squeezed into one displayed equation.

This is a simple & stupid Python program designed to convert content copied directly from Axmath into a mix of inline and displayed math, depending on what you've written. This allows you to write full paragraphs with text and TeX in Axmath and then use this program to copy and paste those paragraphs into LaTeX documents.

To use it, you can employ something like AutoHotKey to set a keyboard shortcut that toggles this program. It will automatically read the latest content in your system clipboard, convert it, and then place the converted content back into the clipboard. Then you can then simply paste it into a LaTeX document or a Markdown document!
