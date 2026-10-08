"""Format classified python-docx objects without rewriting document text.

Import these helpers after deciding paragraph roles and table header boundaries.
Requires python-docx. Does not classify, resize columns, update fields or render.
"""
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt


def child(parent, tag):
    element = parent.find(qn(tag))
    if element is None:
        element = OxmlElement(tag)
        parent.append(element)
    return element


def set_style_fonts(style, latin="Times New Roman", east_asian="SimSun", size_pt=12):
    """Set style defaults only; preserve run-level symbols/italics/superscripts."""
    style.font.name = latin
    style.font.size = Pt(size_pt)
    fonts = child(style.element.get_or_add_rPr(), "w:rFonts")
    for attr, value in (("ascii", latin), ("hAnsi", latin), ("eastAsia", east_asian)):
        fonts.set(qn("w:" + attr), value)
    for attr in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme"):
        fonts.attrib.pop(qn("w:" + attr), None)


def format_body(paragraph, language="en", line_spacing=1.5, before_pt=0,
                after_pt=0, size_pt=12, zh_chars=2, en_inches=0.5):
    """Apply to a verified body paragraph, excluding headings/lists/captions."""
    if language not in ("en", "zh"):
        raise ValueError("language must be en or zh")
    if line_spacing <= 0 or size_pt <= 0 or zh_chars < 0 or en_inches < 0:
        raise ValueError("Spacing and font size must be positive; indents nonnegative")
    pf = paragraph.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.line_spacing = float(line_spacing)
    pf.space_before = Pt(before_pt)
    pf.space_after = Pt(after_pt)
    pf.widow_control = True
    pf.first_line_indent = (Pt(size_pt * zh_chars) if language == "zh"
                            else Inches(en_inches))
    indent = child(paragraph._p.get_or_add_pPr(), "w:ind")
    for attr in ("firstLineChars", "hanging", "hangingChars"):
        indent.attrib.pop(qn("w:" + attr), None)
    if language == "zh":
        indent.set(qn("w:firstLineChars"), str(round(zh_chars * 100)))


def border(parent, edge, width_pt=None):
    element = child(parent, "w:" + edge)
    element.attrib.clear()
    element.set(qn("w:val"), "nil" if width_pt is None else "single")
    if width_pt is not None:
        element.set(qn("w:sz"), str(round(width_pt * 8)))
        element.set(qn("w:color"), "000000")
        element.set(qn("w:space"), "0")


def three_line_table(table, header_rows=1, outer_pt=1.0, header_pt=0.5,
                     line_spacing=1.0, padding_pt=2.0):
    """Set top/header-bottom/bottom rules; handle complex merges manually.

    Caller must inspect merged headers, especially vertical merges crossing the
    header/body boundary. Existing horizontal cell alignment is preserved.
    """
    if not isinstance(header_rows, int) or not 1 <= header_rows < len(table.rows):
        raise ValueError("Need at least one header and one body row")
    if outer_pt <= 0 or header_pt <= 0 or line_spacing <= 0 or padding_pt < 0:
        raise ValueError("Rule widths and line spacing must be positive")
    tb = child(table._tbl.tblPr, "w:tblBorders")
    edges = ("top", "bottom", "left", "right", "start", "end", "insideH", "insideV")
    for edge in edges:
        border(tb, edge)
    seen = set()
    for index, row in enumerate(table.rows):
        trpr = row._tr.get_or_add_trPr()
        for flag in list(trpr.findall(qn("w:tblHeader"))):
            trpr.remove(flag)
        if index < header_rows:
            child(trpr, "w:tblHeader").set(qn("w:val"), "1")
        child(trpr, "w:cantSplit").set(qn("w:val"), "1")
        for height in trpr.findall(qn("w:trHeight")):
            if height.get(qn("w:hRule")) == "exact":
                height.set(qn("w:hRule"), "atLeast")
        for cell in row.cells:
            if cell._tc in seen:
                continue
            seen.add(cell._tc)
            tcpr = cell._tc.get_or_add_tcPr()
            cb = child(tcpr, "w:tcBorders")
            for edge in edges:
                border(cb, edge)
            for shading in list(tcpr.findall(qn("w:shd"))):
                tcpr.remove(shading)
            shading = child(tcpr, "w:shd")
            shading.set(qn("w:val"), "clear")
            shading.set(qn("w:fill"), "FFFFFF")
            shading.set(qn("w:color"), "auto")
            margins = child(tcpr, "w:tcMar")
            for side in ("top", "bottom", "left", "right"):
                margin = child(margins, "w:" + side)
                margin.set(qn("w:w"), str(round(padding_pt * 20)))
                margin.set(qn("w:type"), "dxa")
            for paragraph in cell.paragraphs:
                pf = paragraph.paragraph_format
                pf.first_line_indent = Pt(0)
                pf.space_before = Pt(0)
                pf.space_after = Pt(0)
                pf.line_spacing = float(line_spacing)
                ind = child(paragraph._p.get_or_add_pPr(), "w:ind")
                for attr in ("firstLineChars", "hanging", "hangingChars"):
                    ind.attrib.pop(qn("w:" + attr), None)
    for cell in table.rows[0].cells:
        border(child(cell._tc.get_or_add_tcPr(), "w:tcBorders"), "top", outer_pt)
    for cell in table.rows[header_rows - 1].cells:
        border(child(cell._tc.get_or_add_tcPr(), "w:tcBorders"), "bottom", header_pt)
    for cell in table.rows[-1].cells:
        border(child(cell._tc.get_or_add_tcPr(), "w:tcBorders"), "bottom", outer_pt)
