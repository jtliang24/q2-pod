"""M1 Plus: test/m1plus/patch.py's top-level checks, one at a time, against patch_gaps.GAPS.

The iPod UI is the M1's only UI (docs/m1plus-ipod-ui.md), but most of it is ported item by item (Phase 4),
and patch.py's checks drive Q2's iPod build: its assets, its hooks and its bars. A check of a feature the M1
doesn't have yet is listed in patch_gaps.GAPS under the item that ports it. It must keep failing; a listed check
that passes, and a check that fails and isn't listed, both fail the run.

A check is a top-level statement of patch.py, named by a hash of its source and its number among identical ones (a change to it unlists it, loudly).
GAPS_DUMP=file writes every failing statement there as JSON, to regenerate the list after a change."""
import ast, hashlib, json, os, sys, traceback


def keys(source):
    """Each top-level statement of source with its key: a hash of its text, and of its number among identical ones."""
    seen, out = {}, []
    lines = ast._splitlines_no_ff(source)  # once: get_source_segment splits the whole file on every call

    def segment(node):  # ast.get_source_segment's text: col offsets are UTF-8 byte offsets
        first, last = node.lineno - 1, node.end_lineno - 1
        if first == last:
            return lines[first].encode()[node.col_offset:node.end_col_offset].decode()
        return ''.join([lines[first].encode()[node.col_offset:].decode(), *lines[first + 1:last],
                        lines[last].encode()[:node.end_col_offset].decode()])
    for node in ast.parse(source).body:
        text = segment(node)
        seen[text] = seen.get(text, 0) + 1
        out.append((node, text, hashlib.sha1(text.encode()).hexdigest()[:10] + (f'.{seen[text]}' if seen[text] > 1 else '')))
    return out


def run(path, g, boot_line, gaps):
    """Execute path's statements after boot_line in g; the failures a check lists in gaps are expected."""
    source = open(path).read()
    lines = source.splitlines()
    failed, expected, unexpected, fixed = [], {}, [], []
    trail, patched = [], []
    for node, text, name in keys(source):
        if node.lineno <= boot_line:
            continue
        if node.lineno < int(os.environ.get('GAPS_FROM', 0)) and 'passed()' in text and not isinstance(node, (ast.FunctionDef, ast.ClassDef)):  # debugging one check: skip the earlier ones
            continue
        if node.lineno == int(os.environ.get('GAPS_TRACE', 0)): trail.clear()
        if os.environ.get('GAPS_PC') and not patched and 'Machine' in g:  # keep each call's last instructions
            from unicorn import UC_HOOK_CODE
            call = g['Machine'].call
            def traced(self, *a, **k):
                if not getattr(self, '_traced', 0):
                    self._traced = 1
                    self.u.hook_add(UC_HOOK_CODE, lambda u, address, size, ud: (trail.append(address), trail[:-20] and trail.__delitem__(slice(0, len(trail) - 20))))
                return call(self, *a, **k)
            g['Machine'].call = traced; patched.append(1)
        if os.environ.get('GAPS_PROGRESS'):
            print(f'CHECK {node.lineno} {name}: {text.splitlines()[0][:100]}', flush=True)
        try:
            exec(compile(ast.Module([node], []), path, 'exec'), g)
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt): raise
            inner = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == path]
            where = f'{inner[-1].lineno}: {inner[-1].line}' if inner else ''
            failed.append(dict(key=name, line=node.lineno, first=lines[node.lineno - 1].strip()[:90],
                               error=f'{type(e).__name__} {e} {where}'[:260]))
            if os.environ.get('GAPS_PC') and type(e).__name__ == 'UcError':  # where the emulated payload stopped
                from unicorn.mips_const import UC_MIPS_REG_PC, UC_MIPS_REG_RA
                u = g['m'].u; pc, ra = u.reg_read(UC_MIPS_REG_PC), u.reg_read(UC_MIPS_REG_RA)
                near = lambda a: max(((v, k) for k, v in g['payload_syms'].items() if v <= a), default=(0, '?'))
                print('  frames:', [(f.lineno, f.line[:60]) for f in inner])
                print('  last pcs:', [hex(a) for a in trail[-14:]])
                print('  last calls:', [c[0] for c in g['m'].calls[-6:]])
                print(f'UcError at patch.py:{node.lineno}: pc {pc:#x} in {near(pc)[1]}+{pc - near(pc)[0]:#x}, ra {ra:#x} in {near(ra)[1]}')
            if os.environ.get('GAPS_PROGRESS'):
                print(f'FAIL {node.lineno} {name}: {failed[-1]["error"]}', flush=True)
            if name in gaps: expected.setdefault(gaps[name], []).append(node.lineno)
            else: unexpected.append((node.lineno, name, failed[-1]['error']))
        else:
            if name in gaps: fixed.append((node.lineno, name, gaps[name]))
    if os.environ.get('GAPS_DUMP'): json.dump(failed, open(os.environ['GAPS_DUMP'], 'w'), indent=1)
    for feature, at in sorted(expected.items()): print(f'KNOWN GAP: {feature}: {len(at)} checks (patch.py line {at[0]}...)')
    problems = [f'patch.py:{n} {k}: fails and is not in patch_gaps.GAPS: {e}' for n, k, e in unexpected]
    problems += [f'patch.py:{n} {k}: passes now; drop it from patch_gaps.GAPS ({f})' for n, k, f in fixed]
    stale = set(gaps) - {k for _, _, k in keys(source)}
    problems += [f'patch_gaps.GAPS {k}: no such check in patch.py' for k in sorted(stale)]
    if problems and not os.environ.get('GAPS_DUMP'): sys.exit('\n'.join(problems))
    print(f'M1 Plus: {sum(map(len, expected.values()))} expected-failure checks in {len(expected)} gaps (test/m1plus/patch_gaps.py).')
