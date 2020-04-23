# WellsFargoStatements
Scripts that make it easier to download Wells Fargo statements online in bulk (rather than one at a time) and export them into an easy-to-read format.

This script is based on the following thread: https://gist.github.com/binary1230/7cfa0524d0fae7c320e3b15fc1f4f64c


# How to Use These Scripts
### Bulk downloads

To use it, follow these steps:

*Note: If you are using AdBlock or a similar extension, make sure to turn it off before running through these steps.*
 1) In Chrome browser, navigate to your Wells Fargo Statement Viewer and pull up the set of PDFs you want to view.
 2) Press F12 to open the developer tools and click the tab at the bottom that says 'Console'.
 3) In the developer console, paste the code that is shown under "Create the functions" section.  Then press ENTER.
 4) Select the calendar year for which you want to download statements.  *(Note: You may get a type error if you miss this step.)*
 5) Type this command in the developer console: openAll(lastResponse);
 6) Press ENTER.  You'll know you were successful when a bunch of browser tabs open up.
 7) Download the PDF files.  Name them and put them all in the same directory.  *(It might make later steps easier if you follow this naming convention: "yyyy-mm.pdf".)*
 8) Repeat steps 4-6 as needed.
