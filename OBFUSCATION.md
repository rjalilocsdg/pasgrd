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

Python files in this repository contain compressed, XOR masked source with portable
loaders; those repository payloads remain straightforward to decode. During the
Docker build, Cython 3.1.8 compiles their payloads into native extensions using the
panel image's interpreter. Four database subprocess scripts are compiled into
separate native modules, and their source strings are replaced with imports.
The final image copies only native modules and small launchers. Generated C files,
decoded Python source, compiler tools, and packed input files remain in the build
stage. Linux extensions have debugging symbols stripped. Native code raises the
effort required to recover control flow compared with the previous marshalled
bytecode loader; constants and runtime behavior remain inspectable. Rebuild for
each target Python version and architecture.

Shell scripts contain compressed payloads launched by Python and executed by Bash.
The payloads are byte for byte identical to the upstream scripts. Nginx configuration
has comments and unnecessary whitespace removed while retaining required syntax.

Obfuscation is reversible. It is not encryption, access control, or secret storage.
The public upstream source remains available. Existing Git history in the working
checkout also contains the originals; the supplied ZIP excludes that history.
Keep an original source copy for maintenance and regenerate from source when updating.
Upstream PasarGuard and Xray binaries and libraries are supplied by their base images.

The previous checks covered packed source equivalence, path generation, browser
syntax, template preservation, shell payload equality, and Git whitespace. The
native revision passed compilation of six modules on macOS/Python 3.11, native
path generation for fresh/legacy/repeated runs, bootstrap settings comparison,
rate limiting comparison, and compiled helper routing checks. Full Linux Docker,
live database helper execution, and browser integration were not checked.
