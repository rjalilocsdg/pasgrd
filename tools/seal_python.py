"""Compile packed Python with the container interpreter; emit only packed bytecode."""
import ast
import base64
import marshal
from pathlib import Path
import sys
import zlib

for filename in sys.argv[1:]:
    path = Path(filename)
    tree = ast.parse(path.read_text())
    values = {node.targets[0].id: ast.literal_eval(node.value)
              for node in tree.body if isinstance(node, ast.Assign)
              and isinstance(node.targets[0], ast.Name)
              and isinstance(node.value, ast.Constant)
              and node.targets[0].id in ('_p', '_k')}
    key = bytes.fromhex(values['_k'])
    data = base64.b85decode(values['_p'])
    source = zlib.decompress(bytes(v ^ key[i % len(key)] for i, v in enumerate(data)))
    code = compile(source, '<protected>', 'exec', optimize=2)
    payload = base64.b85encode(zlib.compress(marshal.dumps(code), 9)).decode('ascii')
    path.write_text('# Super JinX Panel — Copyright (c) 2026 Super JinX. See LICENSE.\n'
                    'import base64 as _b,marshal as _m,zlib as _z\n'
                    'exec(_m.loads(_z.decompress(_b.b85decode(' + repr(payload) + '))),globals())\n')
