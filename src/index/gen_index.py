# This is a part of rust-encoding.
# Copyright (c) 2013, Kang Seonghoon.
# See README.md and LICENSE.txt for details.

import urllib
import sys

def write_comma_separated(f, prefix, l, width=80):
    buffered = ''
    for i in l:
        i = str(i)
        if len(prefix) + len(buffered) + len(i) <= width:
            buffered += i
        else:
            print >>f, prefix + buffered.rstrip()
            buffered = i
    if buffered:
        print >>f, prefix + buffered.rstrip()

def generate_single_byte_index(name):
    data = [None] * 128
    comments = []
    for line in urllib.urlopen('http://encoding.spec.whatwg.org/index-%s.txt' % name):
        line = line.strip()
        if not line: continue
        if line.startswith('#'):
            comments.append('//' + line[1:])
            continue
        key, value, _ = line.split(None, 2)
        key = int(key, 0)
        value = int(value, 0)
        assert 0 <= key < 128 and 0 <= value < 0xffff and data[key] is None
        data[key] = value
    with open('%s.rs' % name.replace('-', '_'), 'wb') as f:
        print >>f, '// AUTOGENERATED FROM index-%s.txt, ORIGINAL COMMENT FOLLOWS:' % name
        print >>f, '//'
        for line in comments:
            print >>f, line
        print >>f
        print >>f, "static FORWARD_TABLE: &'static [u16] = &["
        write_comma_separated(f, '    ',
            ['%d, ' % (0xffff if value is None else value) for value in data])
        print >>f, '];'
        print >>f
        print >>f, '#[inline]'
        print >>f, 'pub fn forward(code: u8) -> u16 {'
        print >>f, '    FORWARD_TABLE[code as uint]'
        print >>f, '}'
        print >>f
        print >>f, '#[inline]'
        print >>f, 'pub fn backward(code: u16) -> u8 {'
        print >>f, '    match code {'
        write_comma_separated(f, '        ',
            ['%d => %d, ' % (value, i) for i, value in enumerate(data) if value is not None] +
            ['_ => 255'])
        print >>f, '    }'
        print >>f, '}'
        print >>f
        print >>f, '#[cfg(test)]'
        print >>f, 'mod tests {'
        print >>f, '    use std::u8;'
        print >>f, '    use super::{forward, backward};'
        print >>f
        print >>f, '    #[test]'
        print >>f, '    fn test_correct_table() {'
        print >>f, '        for u8::range(0, 128) |i| {'
        print >>f, '            let j = forward(i);'
        print >>f, '            if j != 0xffff { assert_eq!(backward(j), i); }'
        print >>f, '        }'
        print >>f, '    }'
        print >>f, '}'

def generate_multi_byte_index(name):
    data = {}
    invdata = {}
    dups = []
    comments = []
    morebits = False
    for line in urllib.urlopen('http://encoding.spec.whatwg.org/index-%s.txt' % name):
        line = line.strip()
        if not line: continue
        if line.startswith('#'):
            comments.append('//' + line[1:])
            continue
        key, value, _ = line.split(None, 2)
        key = int(key, 0)
        value = int(value, 0)
        assert 0 <= key < 0xffff and 0 <= value < 0x110000 and value != 0xffff and key not in data
        if value >= 0x10001:
            assert (value >> 16) == 2
            morebits = True
        data[key] = value
        if value not in invdata:
            invdata[value] = key
        else:
            dups.append(key)

    # generate a trie with a minimal amount of data
    maxvalue = max(data.values()) + 1
    best = 0xffffffff
    besttrie = None
    for triebits in xrange(21):
        lower = [0xffff] * (1<<triebits)
        upper = []
        lowermap = {tuple(lower): 0}
        for i in xrange(0, maxvalue, 1<<triebits):
            blk = [invdata.get(j, 0xffff) for j in xrange(i, i + (1<<triebits))]
            loweridx = lowermap.get(tuple(blk))
            if loweridx is None:
                loweridx = len(lower)
                lowermap[tuple(blk)] = loweridx
                lower += blk
            upper.append(loweridx)
        if len(lower) < 0x10000 and best >= len(lower) + len(upper):
            best = len(lower) + len(upper)
            besttrie = (triebits, lower, upper)

    minkey = min(data)
    maxkey = max(data) + 1
    triebits, lower, upper = besttrie
    with open('%s.rs' % name.replace('-', '_'), 'wb') as f:
        print >>f, '// AUTOGENERATED FROM index-%s.txt, ORIGINAL COMMENT FOLLOWS:' % name
        print >>f, '//'
        for line in comments:
            print >>f, line
        print >>f
        print >>f, "static FORWARD_TABLE: &'static [u16] = &["
        write_comma_separated(f, '    ',
            ['%d, ' % (data.get(key, 0xffff) & 0xffff) for key in xrange(minkey, maxkey)])
        print >>f, '];'
        if morebits:
            print >>f
            print >>f, "static FORWARD_TABLE_MORE: &'static [u32] = &["
            bits = []
            for i in xrange(minkey, maxkey, 32):
                v = 0
                for j in xrange(32):
                    v |= (data.get(i+j, 0) >= 0x10000) << j
                bits.append(v)
            write_comma_separated(f, '    ', ['%d, ' % v for v in bits])
            print >>f, '];'
        print >>f
        print >>f, '#[inline]'
        print >>f, 'pub fn forward(code: u16) -> u32 {'
        if minkey != 0:
            print >>f, '    let code = (code - %d) as uint;' % minkey
        else:
            print >>f, '    let code = code as uint;'
        print >>f, '    if code < %d {' % (maxkey - minkey)
        if morebits:
            print >>f, '        (FORWARD_TABLE[code] as u32) | ' + \
                               '(((FORWARD_TABLE_MORE[code >> 5] >> (code & 31)) & 1) << 17)'
        else:
            print >>f, '        FORWARD_TABLE[code] as u32'
        print >>f, '    } else {'
        print >>f, '        0xffff'
        print >>f, '    }'
        print >>f, '}'
        print >>f
        print >>f, "static BACKWARD_TABLE_LOWER: &'static [u16] = &["
        write_comma_separated(f, '    ', ['%d, ' % v for v in lower])
        print >>f, '];'
        print >>f
        print >>f, "static BACKWARD_TABLE_UPPER: &'static [u16] = &["
        write_comma_separated(f, '    ', ['%d, ' % v for v in upper])
        print >>f, '];'
        print >>f
        print >>f, '#[inline]'
        print >>f, 'pub fn backward(code: u32) -> u16 {'
        print >>f, '    let offset = (code >> %d) as uint;' % triebits
        print >>f, '    let offset = if offset < %d {BACKWARD_TABLE_UPPER[offset] as uint} else {0};' % len(upper)
        print >>f, '    BACKWARD_TABLE_LOWER[offset + ((code & %d) as uint)]' % ((1<<triebits)-1)
        print >>f, '}'
        print >>f
        print >>f, '#[cfg(test)]'
        print >>f, 'mod tests {'
        print >>f, '    use std::u32;'
        print >>f, '    use super::{forward, backward};'
        print >>f
        print >>f, '    #[test]'
        print >>f, '    fn test_correct_table() {'
        print >>f, '        for u32::range(0, 0x10000) |i| {'
        print >>f, '            let i = i as u16;'
        for i in dups:
            print >>f, '            if i == %d { loop; }' % i
        print >>f, '            let j = forward(i);'
        print >>f, '            if j != 0xffff { assert_eq!(backward(j), i); }'
        print >>f, '        }'
        print >>f, '    }'
        print >>f, '}'

INDICES = {
    'ibm866':         generate_single_byte_index,
    'iso-8859-2':     generate_single_byte_index,
    'iso-8859-3':     generate_single_byte_index,
    'iso-8859-4':     generate_single_byte_index,
    'iso-8859-5':     generate_single_byte_index,
    'iso-8859-6':     generate_single_byte_index,
    'iso-8859-7':     generate_single_byte_index,
    'iso-8859-8':     generate_single_byte_index,
    'iso-8859-10':    generate_single_byte_index,
    'iso-8859-13':    generate_single_byte_index,
    'iso-8859-14':    generate_single_byte_index,
    'iso-8859-15':    generate_single_byte_index,
    'iso-8859-16':    generate_single_byte_index,
    'koi8-r':         generate_single_byte_index,
    'koi8-u':         generate_single_byte_index,
    'macintosh':      generate_single_byte_index,
    'windows-874':    generate_single_byte_index,
    'windows-1250':   generate_single_byte_index,
    'windows-1251':   generate_single_byte_index,
    'windows-1252':   generate_single_byte_index,
    'windows-1253':   generate_single_byte_index,
    'windows-1254':   generate_single_byte_index,
    'windows-1255':   generate_single_byte_index,
    'windows-1256':   generate_single_byte_index,
    'windows-1257':   generate_single_byte_index,
    'windows-1258':   generate_single_byte_index,
    'x-mac-cyrillic': generate_single_byte_index,

    'big5':           generate_multi_byte_index,
    'euc-kr':         generate_multi_byte_index,
    'gbk':            generate_multi_byte_index,
    'jis0208':        generate_multi_byte_index,
    'jis0212':        generate_multi_byte_index,
}

if __name__ == '__main__':
    import sys
    filter = sys.argv[1] if len(sys.argv) > 1 else ''
    for index, generate in INDICES.items():
        if filter not in index: continue
        print >>sys.stderr, 'generating index %s...' % index
        generate(index)
