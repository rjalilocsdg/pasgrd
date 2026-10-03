"""Build native extensions from packed inputs using the target Python interpreter."""
import ast
import base64
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zlib
from Cython.Build import cythonize
from setuptools import Extension, setup

inputs = [Path(p).resolve() for p in sys.argv[1:]]
work = inputs[0].parent / 'native-build'
out = inputs[0].parent / 'runtime'
work.mkdir(exist_ok=True)
out.mkdir(exist_ok=True)
extensions = []
credit = '# Super JinX Panel — Copyright (c) 2026 Super JinX. See LICENSE.\n'

def add_module(source):
    name = '_jx_' + hashlib.sha256(source.encode()).hexdigest()[:16]
    path = work / (name + '.pyx')
    path.write_text(source)
    extensions.append(Extension(name, [str(path)], extra_compile_args=['-O2', '-g0']))
    return name

for path in inputs:
    tree = ast.parse(path.read_text())
    values = {n.targets[0].id: n.value.value for n in tree.body
              if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
              and isinstance(n.value, ast.Constant) and n.targets[0].id in ('_p', '_k')}
    key = bytes.fromhex(values['_k'])
    data = base64.b85decode(values['_p'])
    source = zlib.decompress(bytes(v ^ key[i % len(key)] for i, v in enumerate(data))).decode()
    tree = ast.parse(source)
    # Subprocess helpers are compiled too; fresh subprocess imports run their bodies.
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id.endswith('_PY') and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            helper = add_module(node.value.value)
            node.value = ast.Constant('import ' + helper)
    guard = tree.body[-1]
    expected = ast.dump(ast.parse('if __name__ == "__main__":\n    pass').body[0].test)
    if not isinstance(guard, ast.If) or ast.dump(guard.test) != expected:
        raise ValueError('Missing main guard in ' + path.name)
    tree.body[-1] = ast.FunctionDef(name='_entrypoint', args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=guard.body, decorator_list=[])
    module = add_module(ast.unparse(ast.fix_missing_locations(tree)))
    (out / path.name).write_text(credit + 'from ' + module + ' import _entrypoint\nif __name__ == "__main__":\n    _entrypoint()\n')

os.chdir(work)
setup(name='jinx-native', script_args=['build_ext', '--build-lib', str(out), '--build-temp', str(work / 'objects')],
      ext_modules=cythonize(extensions, compiler_directives={'language_level': 3, 'binding': True, 'annotation_typing': False, 'infer_types': False, 'emit_code_comments': False}, quiet=True))
if sys.platform.startswith('linux'):
    for path in out.glob('*.so'):
        subprocess.run(['strip', '--strip-unneeded', str(path)], check=True)
if not list(out.glob('*.so')):
    raise RuntimeError('No native modules were produced')
