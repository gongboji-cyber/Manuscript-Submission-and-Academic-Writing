"""Single-panel styling, conservative layout checks and inspected-file export.

Automatic checks are not a visual or statistical certification. Python 3.10+.
Dependencies: matplotlib, numpy, Pillow, PyMuPDF. No third-party code vendored.
"""
from contextlib import contextmanager
from pathlib import Path
import hashlib
import json
import os
import tempfile
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.text import Text
import numpy as np
from PIL import Image
import fitz

COLORS = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#56B4E9', '#E69F00', '#333333']


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


@contextmanager
def panel_style(font='Arial'):
    available = {item.name for item in font_manager.fontManager.ttflist}
    chosen = next((name for name in [font, 'Arial', 'Helvetica', 'DejaVu Sans'] if name in available), None)
    if chosen is None:
        raise RuntimeError('No supported sans-serif font installed')
    settings = {
        'font.family': chosen, 'font.size': 7, 'axes.labelsize': 7,
        'axes.titlesize': 7, 'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5,
        'legend.fontsize': 6.5, 'axes.linewidth': 0.6, 'lines.linewidth': 1,
        'axes.spines.top': False, 'axes.spines.right': False,
        'xtick.direction': 'out', 'ytick.direction': 'out',
        'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
        'axes.grid': False, 'figure.facecolor': 'white',
        'axes.facecolor': 'white', 'savefig.facecolor': 'white',
        'savefig.transparent': False, 'savefig.bbox': None,
        'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none',
        'text.usetex': False, 'axes.prop_cycle': mpl.cycler(color=COLORS),
    }
    with mpl.rc_context(settings):
        yield {'requested_font': font, 'actual_font': chosen,
               'font_substitution': font != chosen}


def new_panel(width_mm=89, height_mm=70):
    if width_mm <= 0 or height_mm <= 0:
        raise ValueError('Panel dimensions must be positive')
    return plt.subplots(figsize=(width_mm / 25.4, height_mm / 25.4),
                        dpi=120, layout='constrained')


def _draw(fig):
    with warnings.catch_warnings(record=True) as observed:
        warnings.simplefilter('always')
        fig.canvas.draw()
    problems = [str(item.message) for item in observed
                if 'Glyph' in str(item.message) or 'constrained_layout not applied' in str(item.message)]
    if problems:
        raise ValueError('Rendering failure: ' + '; '.join(sorted(set(problems))))


def audit_layout(fig):
    """Find text bbox collisions/overflow and legends entering the plot area.

    Conservative heuristics; rotated text uses rectangular extents. Does not
    certify annotation/data collisions. Every reported exception needs review.
    """
    primary = [ax for ax in fig.axes if ax.get_label() not in ('_colorbar', '<colorbar>', '_panel_auxiliary')]
    if len(primary) != 1:
        raise ValueError('Require one primary plot axis; do not export composite panels')
    _draw(fig)
    renderer = fig.canvas.get_renderer()
    bounds = fig.bbox
    text_items, issues = [], []
    # Matplotlib creates visible=True Text objects for ticks beyond the view
    # limits, but Axis.draw does not paint those ticks. Do not flag phantom text.
    unpainted_ticks = set()
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            lo, hi = sorted(axis.get_view_interval())
            for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                if not lo - 1e-10 <= tick.get_loc() <= hi + 1e-10:
                    unpainted_ticks.update((id(tick.label1), id(tick.label2)))
    for text in fig.findobj(match=Text):
        if id(text) in unpainted_ticks or not text.get_visible() or not text.get_text().strip():
            continue
        box = text.get_window_extent(renderer)
        if box.width <= 0 or box.height <= 0:
            continue
        label = text.get_text()
        if box.x0 < bounds.x0 + 1 or box.y0 < bounds.y0 + 1 or box.x1 > bounds.x1 - 1 or box.y1 > bounds.y1 - 1:
            issues.append({'kind': 'text_outside_canvas', 'text': label})
        if text.axes is not None and text.get_clip_on() and (text.get_clip_box() is not None or text.get_clip_path() is not None):
            issues.append({'kind': 'clipped_text_requires_review', 'text': label})
        for other, other_box in text_items:
            dx = min(box.x1, other_box.x1) - max(box.x0, other_box.x0)
            dy = min(box.y1, other_box.y1) - max(box.y0, other_box.y0)
            if dx > 1 and dy > 1:
                issues.append({'kind': 'text_bbox_overlap', 'texts': [other, label]})
        text_items.append((label, box))
    legends = list(fig.legends) + [ax.get_legend() for ax in fig.axes if ax.get_legend()]
    for legend in legends:
        box = legend.get_window_extent(renderer)
        for ax in primary:
            area = ax.get_window_extent(renderer)
            if min(box.x1, area.x1) > max(box.x0, area.x0) and min(box.y1, area.y1) > max(box.y0, area.y0):
                issues.append({'kind': 'legend_enters_plot_area', 'action': 'Move outside or justify a reviewed exception'})
    return {'issues': issues, 'text_items_checked': len(text_items),
            'scope': 'bbox heuristics only; visual review of both formats required'}


def _export_panel(fig, stem, provenance=None, overwrite=False,
                 reviewed_layout_exceptions=None, allow_mixed_pdf=False):
    """Export fixed-size 800dpi RGB TIFF and one-page PDF, with QA manifest.

    Exceptions are exact issue dictionaries plus a reason, never ignore-all.
    No TIFF upsampling; PDF text/paths stay vector. Visual status remains pending.
    """
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    outputs = [stem.with_suffix(ext) for ext in ('.tiff', '.pdf', '.qa.json')]
    if not overwrite and any(p.exists() for p in outputs):
        raise FileExistsError('Output already exists; use a new version directory')
    layout = audit_layout(fig)
    exceptions = reviewed_layout_exceptions or []
    for entry in exceptions:
        if not isinstance(entry, dict) or not entry.get('reason') or 'issue' not in entry:
            raise ValueError('Each exception requires its exact issue and a reason')
    unresolved = [issue for issue in layout['issues'] if not any(e['issue'] == issue for e in exceptions)]
    if unresolved:
        raise ValueError('Layout requires correction/review: ' + json.dumps(unresolved, ensure_ascii=False))
    if any(getattr(artist, 'get_rasterized', lambda: False)() for artist in fig.findobj()) and not allow_mixed_pdf:
        raise ValueError('Rasterized artist conflicts with full-vector output')
    fig.set_layout_engine('none')  # Freeze the reviewed layout across backends.
    width, height = fig.get_size_inches()
    with mpl.rc_context({'pdf.fonttype': 42, 'ps.fonttype': 42,
                         'savefig.bbox': None, 'text.usetex': False}):
        fig.savefig(outputs[1], format='pdf', bbox_inches=None,
                    facecolor='white', transparent=False, dpi=800)
        old_dpi = fig.dpi
        try:
            fig.set_dpi(800)
            _draw(fig)
            rgba = np.asarray(fig.canvas.buffer_rgba()).copy()
            image = Image.fromarray(rgba).convert('RGB')
            image.save(outputs[0], format='TIFF', compression='tiff_lzw', dpi=(800, 800))
        finally:
            fig.set_dpi(old_dpi)
    with Image.open(outputs[0]) as image:
        dpi = image.info.get('dpi', (0, 0))
        expected = (width * 800, height * 800)
        if image.mode != 'RGB' or any(abs(a-b)>1 for a,b in zip(image.size, expected)) or any(abs(v-800)>0.1 for v in dpi):
            raise ValueError('TIFF dimensions/mode/resolution failed validation')
        compression = image.tag_v2.get(259)
        if compression != 5:
            raise ValueError('Expected LZW TIFF')
        # Pillow TIFF DPI values can be IFDRational, not JSON-native numbers.
        tiff_report = {'pixels': list(image.size), 'dpi': [float(v) for v in dpi], 'mode': image.mode, 'compression': 'LZW'}
    with fitz.open(outputs[1]) as document:
        if len(document) != 1:
            raise ValueError('PDF must contain exactly one page')
        page = document[0]
        if abs(page.rect.width-width*72)>0.1 or abs(page.rect.height-height*72)>0.1:
            raise ValueError('PDF physical dimensions changed')
        fonts = page.get_fonts(full=True)
        if not fonts or any('Type3' in str(font) for font in fonts):
            raise ValueError('PDF requires editable embedded non-Type3 text')
        for font in fonts:
            if font[0] <= 0 or not document.extract_font(font[0])[3]:
                raise ValueError('PDF font is not embedded')
        raster_images = page.get_images(full=True)
        if raster_images and not allow_mixed_pdf:
            raise ValueError('PDF contains raster images; cannot certify full vector')
        paths = len(page.get_drawings())
        if paths == 0:
            raise ValueError('PDF contains no vector drawing paths')
        pdf_report = {'pages': 1, 'size_points': [page.rect.width, page.rect.height],
                      'vector_paths': paths, 'raster_images': len(raster_images),
                      'fonts': [list(font[:7]) for font in fonts],
                      'content_type': 'mixed' if raster_images else 'vector'}
    manifest = {'automatic_status': 'pass_with_reviewed_exceptions' if exceptions else 'pass',
                'visual_review': 'pending', 'width_mm': width*25.4, 'height_mm': height*25.4,
                'layout': layout, 'layout_exceptions': exceptions,
                'tiff': tiff_report, 'pdf': pdf_report, 'provenance': provenance or {},
                'versions': {'matplotlib': mpl.__version__, 'numpy': np.__version__,
                             'pillow': Image.__version__, 'pymupdf': fitz.VersionBind},
                'outputs': {p.name: sha256(p) for p in outputs[:2]}}
    outputs[2].write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    return manifest


def export_panel(fig, stem, provenance=None, overwrite=False,
                 reviewed_layout_exceptions=None, allow_mixed_pdf=False):
    """Validate in a temporary directory before publishing final panel files.

    Each replacement is atomic; the three-file publication is not a transaction.
    No success is reported until TIFF, PDF and QA all validate and are published.
    """
    stem=Path(stem)
    stem.parent.mkdir(parents=True,exist_ok=True)
    outputs=[stem.with_suffix(ext) for ext in ('.tiff','.pdf','.qa.json')]
    if not overwrite and any(path.exists() for path in outputs):
        raise FileExistsError('Output already exists; use a new version directory')
    with tempfile.TemporaryDirectory(prefix='panel-export-',dir=stem.parent) as folder:
        temporary_stem=Path(folder)/stem.name
        manifest=_export_panel(fig,temporary_stem,provenance=provenance,
                               reviewed_layout_exceptions=reviewed_layout_exceptions,
                               allow_mixed_pdf=allow_mixed_pdf)
        for output in outputs:
            os.replace(Path(folder)/output.name,output)
    return manifest
