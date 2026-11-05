from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.section import WD_SECTION

OUT = '/mnt/data/ToxiDisp_Project/Project_Report.docx'
doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.65)
sec.bottom_margin = Inches(0.65)
sec.left_margin = Inches(0.75)
sec.right_margin = Inches(0.75)

# Base typography
styles = doc.styles
for name in ['Normal', 'Body Text']:
    styles[name].font.name = 'Arial'
    styles[name].font.size = Pt(10)
    styles[name].paragraph_format.space_after = Pt(5)
for name, size, color in [('Title', 26, '17365D'), ('Heading 1', 16, '17365D'), ('Heading 2', 12, '2F5597'), ('Heading 3', 10, '2F5597')]:
    st = styles[name]
    st.font.name = 'Arial'
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = RGBColor.from_string(color)

# Header/footer
header = sec.header.paragraphs[0]
header.text = 'TOXIDISP | ATMOSPHERIC TOXIC GAS DISPERSION PREDICTOR'
header.style = styles['Caption']
header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
for r in header.runs:
    r.font.name = 'Arial'; r.font.size = Pt(8); r.font.color.rgb = RGBColor(110, 110, 110)
footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = footer.add_run('Project report  |  Page ')
run.font.name = 'Arial'; run.font.size = Pt(8)
fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'), 'PAGE'); footer._p.append(fld)


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), fill); tcPr.append(shd)


def set_cell_text(cell, text, bold=False, color=None, size=9):
    cell.text = ''
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(str(text)); r.bold = bold; r.font.name = 'Arial'; r.font.size = Pt(size)
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def add_table(headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    for i, h in enumerate(headers):
        set_cell_text(table.rows[0].cells[i], h, bold=True, color='FFFFFF', size=9)
        shade(table.rows[0].cells[i], '17365D')
    for row in rows:
        cells = table.add_row().cells
        for i, v in enumerate(row):
            set_cell_text(cells[i], v, size=8.5)
    if widths:
        for row in table.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return table


def add_bullet(text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    p.add_run(text)
    return p

# Cover page
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(88)
r = p.add_run('TOXIDISP'); r.bold = True; r.font.name = 'Arial'; r.font.size = Pt(32); r.font.color.rgb = RGBColor(23, 54, 93)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Atmospheric Toxic Gas Dispersion Predictor'); r.font.name = 'Arial'; r.font.size = Pt(17); r.font.color.rgb = RGBColor(70, 70, 70)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(10)
r = p.add_run('Project-Based Assignment'); r.bold = True; r.font.size = Pt(12)

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(55)
for label, value in [
    ('Course / Subject', '[Enter course name]'),
    ('Department', '[Enter department name]'),
    ('Institute', '[Enter institute name]'),
    ('Submitted to', '[Faculty name]'),
    ('Group member 1', '[Name and roll number]'),
    ('Group member 2', '[Name and roll number]'),
    ('Group member 3', '[Name and roll number]'),
    ('Group member 4', '[Name and roll number]'),
    ('Submission date', '[Enter date]'),
]:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(1.0)
    p.paragraph_format.space_after = Pt(7)
    rr = p.add_run(label + ': '); rr.bold = True; rr.font.size = Pt(10)
    rr = p.add_run(value); rr.font.size = Pt(10)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(28)
r = p.add_run('A Python-based educational simulation of continuous plume and instantaneous puff dispersion.'); r.italic = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor(100,100,100)

doc.add_page_break()

# Abstract and intro
doc.add_heading('Abstract', level=1)
doc.add_paragraph(
    'ToxiDisp is a Python-based educational application developed to estimate the atmospheric dispersion of a toxic material following an accidental point release. '
    'The application implements the ten idealised dispersion cases presented in the supplied Process Safety lecture slides, including analytical eddy-diffusivity models and Pasquill–Gifford Gaussian puff and plume models. '
    'A user can enter release conditions, wind speed, atmospheric stability, observation coordinates and a concentration threshold. '
    'The software calculates concentration at a selected point, converts the result into ppmv, displays a ground-level concentration contour and estimates the grid area above the chosen threshold. '
    'The program is intended for classroom demonstration and is not a validated emergency-response tool.'
)

doc.add_heading('1. Introduction and problem statement', level=1)
doc.add_paragraph(
    'An accidental release from a vessel, pipeline or process unit can introduce a toxic material into the atmosphere. '
    'After release, the material is transported by the mean wind and spread by atmospheric turbulence. '
    'The resulting concentration field depends on release rate or released mass, wind speed, atmospheric stability, release height and the surrounding surface conditions. '
    'A dispersion model estimates concentration as a function of position and, for transient releases, time.'
)
doc.add_heading('2. Objectives', level=1)
for item in [
    'Develop a simple software interface to accept release and atmospheric inputs.',
    'Implement the ten dispersion cases presented in Lecture 20 and the Gaussian plume formulation used in Lecture 21.',
    'Calculate concentration at a user-selected coordinate and time where applicable.',
    'Generate ground-level concentration contour plots for a selected simulation domain.',
    'Compare the predicted concentration with a user-entered toxic concentration threshold.',
    'Check the calculations against the SO2 and chlorine worked examples in Lecture 21.'
]: add_bullet(item)

doc.add_page_break()
doc.add_heading('3. Theory and mathematical models', level=1)
doc.add_paragraph(
    'The lecture introduces the advection–dispersion equation. In compact notation, the concentration field C is affected by accumulation, mean wind transport and turbulent diffusion:'
)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('∂C/∂t + ūⱼ ∂C/∂xⱼ = ∂/∂xⱼ (Kⱼ ∂C/∂xⱼ)'); r.bold = True; r.font.name = 'Cambria Math'; r.font.size = Pt(11)
doc.add_paragraph('Here ūⱼ is the mean velocity component, xⱼ is a spatial coordinate and Kⱼ is the eddy diffusivity (m²/s). The idealised lecture cases are grouped below.')

add_table(['Case', 'Release / atmosphere', 'Implemented expression (summary)'], [
    ('1', 'Steady continuous point source; no wind; isotropic K', 'C = Q / (4πKr)'),
    ('2', 'Instantaneous puff; no wind; isotropic K', 'C = M / [8(πKt)^(3/2)] exp[-r²/(4Kt)]'),
    ('3', 'Continuous release started at t = 0; no wind', 'C = Q / (4πKr) erfc[r/(2√(Kt))]'),
    ('4', 'Steady continuous point source; wind; isotropic K', 'C = Q / (4πKr) exp[-u(r−x)/(2K)]'),
    ('5', 'Instantaneous puff with wind; Kx, Ky, Kz', 'Anisotropic Gaussian puff centred at x = ut'),
    ('6', 'Instantaneous ground-level puff; no wind', 'Anisotropic puff with ground-image factor'),
    ('7', 'Steady plume from ground; wind; anisotropic K', 'C = Q/[2πx√(KxKy)] exp{−u[y²/Ky+z²/Kz]/(4x)}'),
    ('8', 'Elevated continuous source; ground reflection', 'Two vertical Gaussian terms for source and image source'),
    ('9', 'Ground-level Gaussian puff; P–G coefficients', '3-D Gaussian puff moving at x = ut; ground-image normalization'),
    ('10', 'Gaussian plume; ground-source Case 10, with elevated-source form in Lecture 21', 'Reflected Gaussian plume; H = 0 gives ground-source Case 10'),
], widths=[0.55, 2.2, 4.1])

doc.add_heading('3.1 Pasquill–Gifford dispersion coefficients', level=2)
doc.add_paragraph(
    'The lecture uses σy and σz to represent crosswind and vertical dispersion. For rural plume calculations, the supplied Table 5-2 correlations are used with downwind distance x in metres. '
    'For example, for stability class D: σy = 0.08x(1 + 0.0001x)^(-1/2), and σz = 0.06x(1 + 0.0015x)^(-1/2). '
    'The puff model uses the separate power-law coefficient table in Lecture 20, Table 5-3; σx is taken equal to σy as indicated in that table.'
)
add_table(['Stability', 'Plume σy (rural)', 'Plume σz (rural)', 'Puff σx = σy', 'Puff σz'], [
    ('A', '0.22x(1+0.0001x)^−0.5', '0.20x', '0.18x^0.92', '0.60x^0.75'),
    ('B', '0.16x(1+0.0001x)^−0.5', '0.12x', '0.14x^0.92', '0.53x^0.73'),
    ('C', '0.11x(1+0.0001x)^−0.5', '0.08x(1+0.0002x)^−0.5', '0.10x^0.92', '0.34x^0.71'),
    ('D', '0.08x(1+0.0001x)^−0.5', '0.06x(1+0.0015x)^−0.5', '0.06x^0.92', '0.15x^0.70'),
    ('E', '0.06x(1+0.0001x)^−0.5', '0.03x(1+0.0003x)^−1', '0.04x^0.92', '0.10x^0.65'),
    ('F', '0.04x(1+0.0001x)^−0.5', '0.016x(1+0.0003x)^−1', '0.02x^0.89', '0.05x^0.61'),
], widths=[0.65, 1.75, 1.75, 1.45, 1.25])

doc.add_heading('3.2 Concentration units and toxic threshold', level=2)
doc.add_paragraph(
    'The dispersion equations return mass concentration in kg/m³. For an ideal gas, the application converts this value to parts per million by volume (ppmv) using:'
)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('ppmv = Cmass × (R T / P) × (10⁶ / MW)'); r.bold = True; r.font.name = 'Cambria Math'; r.font.size = Pt(11)
doc.add_paragraph(
    'where Cmass is in kg/m³, MW is molecular weight in kg/mol, T is absolute temperature in K, P is absolute pressure in Pa and R = 8.314462618 Pa·m³/(mol·K). '
    'The user supplies the toxic concentration threshold. Lecture 21 gives ERPG-1 = 1 ppm for its chlorine example; this value is not treated as a universal threshold for other chemicals.'
)

doc.add_page_break()

doc.add_heading('4. Software design and implementation', level=1)
doc.add_paragraph(
    'The application is written in Python. Streamlit provides the browser-based input interface, NumPy performs array calculations, SciPy supplies the complementary error function for Case 3, Matplotlib draws the concentration contours and Pandas prepares downloadable CSV data.'
)
add_table(['File / module', 'Function'], [
    ('app.py', 'User interface, input validation, selected-point output, contour plot and CSV export.'),
    ('dispersion_models.py', 'Mathematical implementation of Cases 1–10 and the Pasquill–Gifford coefficient correlations.'),
    ('toxicity.py', 'Threshold comparison helper.'),
    ('validation.py', 'Reproduction of the Lecture 21 worked examples.'),
    ('test_models.py', 'Unit tests for coefficient values, example calculations and model output.'),
], widths=[2.0, 5.0])

doc.add_heading('4.1 Input parameters', level=2)
add_table(['Input', 'Meaning', 'Unit'], [
    ('Chemical name and molecular weight', 'Used to label the result and convert mass concentration to ppmv.', 'g/mol for MW'),
    ('Release rate Q', 'Mass discharged continuously for plume/continuous models.', 'g/s entered; converted to kg/s'),
    ('Released mass M', 'Total mass released instantaneously for puff models.', 'kg'),
    ('Wind speed u', 'Mean downwind velocity.', 'm/s'),
    ('Stability class', 'Pasquill–Gifford atmospheric stability class A–F.', '—'),
    ('Release height H', 'Effective source height above ground for elevated plume.', 'm'),
    ('Eddy diffusivity K / Kx, Ky, Kz', 'Turbulent dispersion coefficients for Cases 1–8.', 'm²/s'),
    ('Coordinates x, y, z and time t', 'Location and time at which concentration is requested.', 'm and s'),
    ('Threshold', 'User-defined toxic concentration comparison value.', 'ppmv'),
], widths=[1.8, 4.1, 1.1])

doc.add_heading('4.2 Outputs', level=2)
for item in [
    'Concentration at the selected point in kg/m³, mg/m³ and ppmv.',
    'A comparison indicating whether the entered threshold is exceeded.',
    'A ground-level contour map over the selected downwind and crosswind domain.',
    'A grid-based estimate of the area above the threshold and the farthest affected distance within the plotted domain.',
    'CSV file containing x, y, concentration and threshold flags for further analysis.'
]: add_bullet(item)

doc.add_page_break()
doc.add_heading('5. Validation using Lecture 21 examples', level=1)
doc.add_heading('5.1 Example 1 – continuous SO2 release', level=2)
doc.add_paragraph(
    'Lecture inputs: SO2 release rate 80 g/s, effective stack height 60 m, wind speed 6 m/s, rural terrain, overcast conditions and stability class D. '
    'The plume coefficients at x = 500 m are σy = 39.04 m and σz = 22.68 m. The program calculates the following results:'
)
add_table(['Location', 'Program result', 'Lecture result'], [
    ('500 m downwind, centreline, ground', '1.448 × 10⁻⁴ g/m³', '1.45 × 10⁻⁴ g/m³'),
    ('500 m downwind, 50 m crosswind, ground', '6.374 × 10⁻⁵ g/m³', '6.37 × 10⁻⁵ g/m³'),
    ('Maximum ground-level concentration', 'Lecture analytical estimate: about 4.18 × 10⁻⁴ g/m³ near 1.2 km', '4.18 × 10⁻⁴ g/m³ near 1200 m'),
], widths=[2.5, 2.3, 2.2])
doc.add_paragraph('The first two outputs agree with the lecture within rounding. The third result is quoted from the lecture calculation, which uses σz = Hr/√2 and reads the corresponding downwind coefficient from its dispersion table/figure.')

doc.add_heading('5.2 Example 2 – instantaneous chlorine release', level=2)
doc.add_paragraph(
    'Lecture inputs: 1.0 kg chlorine released instantaneously at ground level, wind speed 2 m/s and a residential area 500 m downwind. '
    'The advective travel-time estimate is t = x/u = 500/2 = 250 s (4.17 min). For stability class F, the puff table gives σx = σy ≈ 5.05 m and σz ≈ 2.21 m at 500 m. '
    'The program calculates a centre concentration of approximately 776 ppmv using the unrounded coefficients. The lecture rounds the coefficients to 5.0 m and 2.2 m before reporting approximately 798 ppm. '
    'The small difference is attributable to rounding of the dispersion coefficients and intermediate values.'
)

doc.add_heading('6. Limitations and safety considerations', level=1)
for item in [
    'Pasquill–Gifford Gaussian models assume neutrally buoyant dispersion dominated by turbulent mixing; they are not dense-gas models. The lecture describes a typical range of about 0.1–10 km and time-averaged predictions.',
    'The implementation uses rural correlations and user-selected stability classes. It does not infer stability from measured weather or account for urban buildings and complex terrain.',
    'Eddy diffusivities are user inputs. The lecture slides do not provide universal values, so the interface starter values are illustrative only.',
    'The application omits chemical reaction, deposition, aerosol/liquid pools, dense-gas slumping, obstacles, changing wind direction and time-varying release rates.',
    'The threshold contour is a classroom screening visualisation, not a public warning, evacuation boundary or safety certification.'
]: add_bullet(item)

doc.add_heading('7. Conclusion and future scope', level=1)
doc.add_paragraph(
    'ToxiDisp translates the lecture equations into an interactive Python tool. It accepts release and atmospheric inputs, calculates point concentrations, plots ground-level contours and compares results with a user-entered threshold. The SO2 example is reproduced closely; the chlorine puff result agrees after accounting for coefficient rounding. Future improvements could include changing wind, urban conditions, dense-gas models and GIS mapping.'
)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(4)
p.paragraph_format.space_after = Pt(0)
r = p.add_run('References: '); r.bold = True; r.font.size = Pt(8)
r = p.add_run('Lecture 19 – Dispersion model.pdf; Lecture 20 – Dispersion model-2.pdf; Lecture 21 – Dispersion model-3.pdf (supplied Process Safety lecture slides).')
r.font.size = Pt(8)

# Document metadata
doc.core_properties.title = 'ToxiDisp – Atmospheric Toxic Gas Dispersion Predictor'
doc.core_properties.subject = 'Project-based assignment report based on Lectures 19–21'
doc.core_properties.author = 'Student project group'
doc.save(OUT)
print(OUT)
