# Obfuscated distribution

Based on rjalilocsdg/pasgrd. Super JinX branding, credits, and LICENSE remain applicable.

Deploy with the existing Dockerfile and Railway settings. Environment variables,
URLs, persistent paths, and subscription template data retain their original meanings.

The dashboard and three executable subscription scripts use javascript-obfuscator
4.1.1 with RC4 string arrays, hexadecimal identifiers, control flow flattening,
dead code injection, split strings, and numeric expressions. Global names and
object properties are preserved because subscription scripts share functions and
interact with browser APIs. No source maps are shipped. HTML, CSS, and Jinja markup
retain their original structure. JavaScript is substantially larger and can take
more CPU to initialize; assess it on the devices used by customers.

Python files contain compressed, XOR masked source with portable loaders. During
the Docker build, a separate stage compiles their payloads with the panel image's
Python interpreter and emits compressed marshalled bytecode. The final image
copies only those compiled loaders, avoiding packed Python source in its layers.
Bytecode must be rebuilt if the interpreter version changes. Embedded Python
scripts used for subprocesses remain strings inside that bytecode.

Shell scripts contain compressed payloads launched by Python and executed by Bash.
The payloads are byte for byte identical to the upstream scripts. Nginx configuration
has comments and unnecessary whitespace removed while retaining required syntax.

Obfuscation is reversible. It is not encryption, access control, or secret storage.
The public upstream source remains available. Existing Git history in the working
checkout also contains the originals; the supplied ZIP excludes that history.
Keep an original source copy for maintenance and regenerate from source when updating.
Upstream PasarGuard and Xray binaries and libraries are supplied by their base images.

Checks completed: Python AST equivalence excluding comments/docstrings; Python
loader compilation; packed and compiled path generator behavior for fresh and
legacy installs and repeated runs; dashboard and inline JavaScript syntax;
subscription HTML/CSS/Jinja preservation; shell payload equality and Bash syntax;
Git whitespace checks. Full Docker and browser integration were not checked.
