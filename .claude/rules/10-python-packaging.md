## Hyphenated package directories aren't importable by their name

The Philosophy
A directory with a hyphen in its name (`util-lib/`) can hold a valid Python
package with an `__init__.py`, but Python identifiers can't contain hyphens, so
`import util-lib` is a syntax error and `import util_lib` finds nothing. The
package works fine when imported by a path-based or aliased name — the hyphen
only blocks the bare-name import, not the package itself. Knowing this up front
avoids a confusing `ModuleNotFoundError` that looks like a broken package.

Do's
- Do import the submodules directly when inside the dir: `from strings import slugify`.
- Do alias the path to an importable name to test package-level imports: symlink
  `util_lib -> util-lib` (or rename) before `import util_lib`.
- Do verify behavior with the interpreter that's actually on PATH (`python3`),
  not the one you assumed.

Don'ts
- Don't assume `import <dirname>` works when the dir name has hyphens — it won't.
- Don't rename a hyphenated dir to fix imports without checking nothing else
  references the hyphenated path.
