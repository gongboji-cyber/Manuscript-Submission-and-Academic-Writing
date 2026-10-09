"""Format classified python-docx objects without rewriting document text.

Import these helpers after deciding paragraph roles and table header boundaries.
Requires python-docx. Does not classify, resize columns, update fields or render.
"""
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.table import _Cell
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
    """Format a classified data table, then render and inspect every page.

    Horizontal merges and vertical merges within the header/body are preserved.
    Reject nested tables, omitted grid cells and merges crossing the header/body
    boundary before changing anything. Existing horizontal alignment is preserved.
    Clears cell paragraph keep-next so inherited styles cannot chain a long table.
    Long rows and special grouping rules still require individual layout review.
    """
    if not isinstance(header_rows, int) or not 1 <= header_rows < len(table.rows):
        raise ValueError("Need at least one header and one body row")
    if outer_pt <= 0 or header_pt <= 0 or line_spacing <= 0 or padding_pt < 0:
        raise ValueError("Rule widths and line spacing must be positive")
    rows = list(table._tbl.tr_lst)
    for row in rows:
        if row.trPr is not None and any(
                row.trPr.find(qn(tag)) is not None
                for tag in ("w:gridBefore", "w:gridAfter")):
            raise ValueError("Omitted grid cells require manual layout review")
        for tc in row.tc_lst:
            if tc.find(qn("w:tbl")) is not None:
                raise ValueError("Nested tables require manual layout review")
    if any(tc.vMerge == "continue" for tc in rows[header_rows].tc_lst):
        raise ValueError("Vertical merge crosses the header/body boundary")
    tb = child(table._tbl.tblPr, "w:tblBorders")
    edges = ("top", "bottom", "left", "right", "start", "end", "insideH", "insideV")
    for edge in edges:
        border(tb, edge)
    spacing = child(table._tbl.tblPr, "w:tblCellSpacing")
    spacing.set(qn("w:w"), "0")
    spacing.set(qn("w:type"), "dxa")
    for index, row in enumerate(rows):
        # Row exceptions can otherwise revive inherited grid borders/spacing.
        exceptions = row.find(qn("w:tblPrEx"))
        if exceptions is not None:
            for edge in edges:
                border(child(exceptions, "w:tblBorders"), edge)
            spacing = child(exceptions, "w:tblCellSpacing")
            spacing.set(qn("w:w"), "0")
            spacing.set(qn("w:type"), "dxa")
        trpr = row.get_or_add_trPr()
        flags = list(trpr.findall(qn("w:tblHeader")))
        for flag in flags[1:] if index < header_rows else flags:
            trpr.remove(flag)
        if index < header_rows:
            child(trpr, "w:tblHeader").set(qn("w:val"), "1")
        child(trpr, "w:cantSplit").set(qn("w:val"), "1")
        for height in trpr.findall(qn("w:trHeight")):
            if height.get(qn("w:hRule")) == "exact":
                height.set(qn("w:hRule"), "atLeast")
        # row.cells aliases a vertical continuation to the restart cell. Use
        # physical XML cells so header-bottom rules reach the actual last row.
        for tc in row.tc_lst:
            cell = _Cell(tc, table)
            tcpr = tc.get_or_add_tcPr()
            cb = child(tcpr, "w:tcBorders")
            for edge in edges + ("tl2br", "tr2bl"):
                border(cb, edge)
            for shading in list(tcpr.findall(qn("w:shd")))[1:]:
                tcpr.remove(shading)
            shading = child(tcpr, "w:shd")
            shading.attrib.clear()
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
                pf.keep_with_next = False
                ind = child(paragraph._p.get_or_add_pPr(), "w:ind")
                for attr in ("firstLineChars", "hanging", "hangingChars"):
                    ind.attrib.pop(qn("w:" + attr), None)
    for tc in rows[0].tc_lst:
        border(child(tc.get_or_add_tcPr(), "w:tcBorders"), "top", outer_pt)
    for tc in rows[header_rows - 1].tc_lst:
        border(child(tc.get_or_add_tcPr(), "w:tcBorders"), "bottom", header_pt)
    for tc in rows[-1].tc_lst:
        border(child(tc.get_or_add_tcPr(), "w:tcBorders"), "bottom", outer_pt)
