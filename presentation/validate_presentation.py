#!/usr/bin/env python3
"""Check PPTX archive integrity, XML, relationships, slides and speaker notes."""
from pathlib import Path
import posixpath
import zipfile
import xml.etree.ElementTree as ET

path = Path(__file__).resolve().parent / '搜索与检索增强人工智能汇报.pptx'
ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
with zipfile.ZipFile(path) as z:
    assert z.testzip() is None, 'Invalid ZIP entry'
    names = set(z.namelist())
    for name in names:
        tree = ET.fromstring(z.read(name))
        if name.endswith('.rels'):
            base = '' if name == '_rels/.rels' else posixpath.dirname(posixpath.dirname(name))
            for rel in tree:
                if rel.get('TargetMode') != 'External':
                    target = posixpath.normpath(posixpath.join(base, rel.get('Target')))
                    assert target in names, f'Missing relationship target: {target}'
    p = ET.fromstring(z.read('ppt/presentation.xml'))
    count = len(p.findall('p:sldIdLst/p:sldId', ns))
    assert count == 16
    for i in range(1, count+1):
        slide = ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
        notes = ET.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml'))
        assert slide.findall('.//a:t', ns)
        assert notes.findall('.//a:t', ns)
        ids = [n.get('id') for n in slide.findall('.//p:cNvPr', ns)]
        assert len(ids) == len(set(ids)), f'Duplicate shape ID in slide {i}'
        for transform in slide.findall('.//p:spPr/a:xfrm', ns):
            off, extent = transform.find('a:off', ns), transform.find('a:ext', ns)
            assert int(off.get('x')) >= 0 and int(off.get('y')) >= 0
            assert int(off.get('x')) + int(extent.get('cx')) <= 12191700
            assert int(off.get('y')) + int(extent.get('cy')) <= 6858000
    print(f'PASS: {count} slides, 16 notes, XML/ZIP integrity, relationships and shape bounds.')
    print('This structural check does not replace visual review in PowerPoint or WPS.')
