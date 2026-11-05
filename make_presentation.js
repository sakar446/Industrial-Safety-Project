const pptxgen = require('pptxgenjs');
const path = require('path');
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Student Project Group';
pptx.subject = 'Atmospheric toxic gas dispersion predictor';
pptx.title = 'ToxiDisp – Atmospheric Toxic Gas Dispersion Predictor';
pptx.company = 'Academic project';
pptx.lang = 'en-IN';
pptx.theme = {
  headFontFace: 'Aptos Display', bodyFontFace: 'Aptos', lang: 'en-IN'
};
pptx.defineSlideMaster({
  title: 'MASTER',
  background: { color: 'F7F9FC' },
  objects: [
    { rect: { x: 0, y: 0, w: 13.333, h: 0.16, line: { color: '17365D', transparency: 100 }, fill: { color: '17365D' } } },
    { text: { text: 'TOXIDISP  |  PROCESS SAFETY PROJECT', options: { x: 0.55, y: 7.16, w: 7.0, h: 0.18, fontFace: 'Aptos', fontSize: 8, color: '708090', margin: 0 } } },
  ],
  slideNumber: { x: 12.35, y: 7.12, w: 0.4, h: 0.2, color: '708090', fontFace: 'Aptos', fontSize: 8 }
});
const C = { navy:'17365D', blue:'2F5597', teal:'14A3A3', sky:'DCEAF7', dark:'233044', muted:'5E6B7A', pale:'EEF3F8', white:'FFFFFF', orange:'E28A3B', green:'368F6A', red:'C94C4C' };
const W=13.333, H=7.5;
function addText(slide, text, x,y,w,h, opts={}) {
  slide.addText(text, { x,y,w,h, fontFace:'Aptos', fontSize:opts.fontSize||16, color:opts.color||C.dark,
    bold:opts.bold||false, margin:opts.margin===undefined?0.04:opts.margin, breakLine: false,
    fit:'shrink', valign:opts.valign||'mid', align:opts.align||'left', italic:opts.italic||false,
    paraSpaceAfterPt: opts.paraSpaceAfterPt||0, bullet: opts.bullet,
    transparency: opts.transparency||0 });
}
function addHeader(slide, title, subtitle='') {
  addText(slide,title,0.62,0.38,12.0,0.48,{fontSize:26,bold:true,color:C.navy});
  if(subtitle) addText(slide,subtitle,0.64,0.91,12.0,0.32,{fontSize:11,color:C.muted});
}
function card(slide,x,y,w,h,title,body,accent=C.teal) {
  slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h,rectRadius:0.12,fill:{color:C.white},line:{color:'DCE3EB',width:1},shadow:{type:'outer',color:'9AA8B8',blur:1,angle:45,distance:1,opacity:0.10}});
  slide.addShape(pptx.ShapeType.rect,{x:x,y:y,w:0.08,h,fill:{color:accent},line:{color:accent,transparency:100}});
  addText(slide,title,x+0.22,y+0.14,w-0.36,0.30,{fontSize:16,bold:true,color:C.navy});
  addText(slide,body,x+0.22,y+0.54,w-0.38,h-0.64,{fontSize:12,color:C.dark,valign:'top'});
}
function pill(slide,txt,x,y,w,color=C.sky,fg=C.navy){
  slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h:0.34,rectRadius:0.12,fill:{color},line:{color,transparency:100}});
  addText(slide,txt,x+0.06,y+0.02,w-0.12,0.27,{fontSize:10,bold:true,color:fg,align:'center'});
}

// Slide 1 – title
{
  const s=pptx.addSlide();
  s.background={color:C.navy};
  s.addShape(pptx.ShapeType.rect,{x:0,y:0,w:W,h:H,fill:{color:C.navy},line:{color:C.navy}});
  s.addShape(pptx.ShapeType.ellipse,{x:9.5,y:0.15,w:3.55,h:3.55,fill:{color:'2D527E',transparency:35},line:{color:'2D527E',transparency:100}});
  s.addShape(pptx.ShapeType.ellipse,{x:10.55,y:4.25,w:2.55,h:2.55,fill:{color:C.teal,transparency:45},line:{color:C.teal,transparency:100}});
  s.addShape(pptx.ShapeType.rect,{x:0.8,y:1.18,w:0.12,h:3.7,fill:{color:C.teal},line:{color:C.teal}});
  addText(s,'TOXIDISP',1.22,1.28,7.6,0.9,{fontSize:44,bold:true,color:C.white});
  addText(s,'Atmospheric Toxic Gas\nDispersion Predictor',1.24,2.25,7.9,1.3,{fontSize:27,color:'E4EDF7',valign:'top'});
  addText(s,'Project-Based Assignment  |  Process Safety',1.24,3.82,7.5,0.42,{fontSize:16,bold:true,color:'9FDADA'});
  addText(s,'Group members: [Name 1]  •  [Name 2]  •  [Name 3]  •  [Name 4]',1.24,5.55,9.7,0.35,{fontSize:12,color:'D8E2ED'});
  addText(s,'[Department / Institute]  •  [Faculty name]',1.24,5.95,8.0,0.3,{fontSize:11,color:'AFC0D1'});
  addText(s,'Academic simulation – not for live emergency response',1.24,6.84,8.0,0.24,{fontSize:9,color:'B8C8D9',italic:true});
}

// Slide 2 – Problem and objective
{
  const s=pptx.addSlide('MASTER'); addHeader(s,'The problem: where does a toxic cloud travel?','A release creates a concentration field that changes with location, release type and atmospheric conditions.');
  card(s,0.65,1.55,5.8,2.1,'Accidental release','A process vessel, pipeline or storage system may release a hazardous gas continuously or as a sudden finite mass.',C.orange);
  card(s,6.75,1.55,5.9,2.1,'Project objective','Build software that predicts concentration at a chosen point and maps the region where a user-selected concentration threshold is exceeded.',C.teal);
  // flow
  const flow=[['INPUTS','Release mass/rate\nWind • Stability\nRelease height'],['MODEL','Plume / puff\nEddy diffusivity\nPasquill–Gifford'],['OUTPUTS','C(x,y,z,t)\nContour map\nThreshold zone']];
  const xs=[0.95,4.85,8.75];
  for(let i=0;i<3;i++){
    s.addShape(pptx.ShapeType.roundRect,{x:xs[i],y:4.35,w:3.0,h:1.65,rectRadius:0.12,fill:{color:i===0?'EAF1F8':(i===1?'E6F4F3':'FDF1E6')},line:{color:'D6E0EA',width:1}});
    addText(s,flow[i][0],xs[i]+0.16,4.53,2.68,0.28,{fontSize:14,bold:true,color:C.navy,align:'center'});
    addText(s,flow[i][1],xs[i]+0.16,4.95,2.68,0.85,{fontSize:12,color:C.dark,align:'center',valign:'mid'});
    if(i<2) { s.addShape(pptx.ShapeType.chevron,{x:xs[i]+3.25,y:4.88,w:0.42,h:0.55,fill:{color:C.teal},line:{color:C.teal}}); }
  }
  addText(s,'Deliverable: an interactive Python application with point calculations, contour plots and downloadable data.',0.9,6.35,11.6,0.35,{fontSize:14,bold:true,color:C.blue,align:'center'});
}

// Slide 3 – plume vs puff
{
  const s=pptx.addSlide('MASTER'); addHeader(s,'Two release modes: plume and puff','The model must match whether the source releases continuously or releases a fixed mass instantaneously.');
  // left plume diagram
  s.addShape(pptx.ShapeType.roundRect,{x:0.65,y:1.52,w:5.95,h:4.9,rectRadius:0.1,fill:{color:'FFFFFF'},line:{color:'DCE3EB',width:1}});
  addText(s,'CONTINUOUS PLUME',0.95,1.75,5.3,0.35,{fontSize:17,bold:true,color:C.navy,align:'center'});
  s.addShape(pptx.ShapeType.rect,{x:1.1,y:4.37,w:0.45,h:1.0,fill:{color:'8A99A8'},line:{color:'657586'}});
  s.addShape(pptx.ShapeType.rect,{x:1.0,y:5.34,w:0.65,h:0.12,fill:{color:'657586'},line:{color:'657586'}});
  // plume elongated translucent shapes
  const plumeShapes=[
    {x:1.5,y:4.15,w:1.25,h:0.5,trans:20},{x:2.15,y:3.96,w:1.8,h:0.88,trans:35},
    {x:3.05,y:3.72,w:2.25,h:1.35,trans:48},{x:4.2,y:3.48,w:1.75,h:1.82,trans:60}
  ];
  plumeShapes.forEach((p,i)=>s.addShape(pptx.ShapeType.ellipse,{x:p.x,y:p.y,w:p.w,h:p.h,fill:{color:i<2?'83C8C1':'A5D8D3',transparency:p.trans},line:{color:'7FBEB7',transparency:100}}));
  s.addShape(pptx.ShapeType.line,{x:1.62,y:3.4,w:4.15,h:0,line:{color:C.teal,width:2,beginArrowType:'none',endArrowType:'triangle'}});
  addText(s,'Constant release rate Q (kg/s)',1.0,5.75,5.25,0.35,{fontSize:12,bold:true,color:C.blue,align:'center'});
  addText(s,'Example: continuous pipeline leak',1.0,6.08,5.25,0.24,{fontSize:10,color:C.muted,align:'center'});
  // right puff diagram
  s.addShape(pptx.ShapeType.roundRect,{x:6.8,y:1.52,w:5.85,h:4.9,rectRadius:0.1,fill:{color:'FFFFFF'},line:{color:'DCE3EB',width:1}});
  addText(s,'INSTANTANEOUS PUFF',7.1,1.75,5.25,0.35,{fontSize:17,bold:true,color:C.navy,align:'center'});
  s.addShape(pptx.ShapeType.rect,{x:7.35,y:4.37,w:0.45,h:1.0,fill:{color:'8A99A8'},line:{color:'657586'}});
  s.addShape(pptx.ShapeType.rect,{x:7.25,y:5.34,w:0.65,h:0.12,fill:{color:'657586'},line:{color:'657586'}});
  s.addShape(pptx.ShapeType.ellipse,{x:9.0,y:3.42,w:2.1,h:2.1,fill:{color:'8ECAC4',transparency:28},line:{color:'68B1A8',width:1.5}});
  s.addShape(pptx.ShapeType.ellipse,{x:9.43,y:3.85,w:1.24,h:1.24,fill:{color:'46A99F',transparency:22},line:{color:'368F86',width:1}});
  s.addShape(pptx.ShapeType.ellipse,{x:9.78,y:4.2,w:0.54,h:0.54,fill:{color:C.teal,transparency:6},line:{color:C.teal,width:1}});
  s.addShape(pptx.ShapeType.line,{x:7.95,y:3.4,w:3.65,h:0,line:{color:C.teal,width:2,endArrowType:'triangle'}});
  addText(s,'Fixed released mass M (kg)',7.08,5.75,5.25,0.35,{fontSize:12,bold:true,color:C.blue,align:'center'});
  addText(s,'Example: sudden vessel rupture',7.08,6.08,5.25,0.24,{fontSize:10,color:C.muted,align:'center'});
}

// Slide 4 – models and stability
{
  const s=pptx.addSlide('MASTER'); addHeader(s,'The model library follows Lectures 19–21','Ten idealised cases are organised by physical assumptions and release type.');
  card(s,0.65,1.52,3.75,2.12,'Cases 1–4  |  Isotropic K','Steady or transient point releases with no wind or a constant wind; one eddy diffusivity K in all directions.',C.blue);
  card(s,4.78,1.52,3.75,2.12,'Cases 5–8  |  Kx, Ky, Kz','Anisotropic puff/plume solutions, ground-level sources and an elevated source with ground reflection.',C.teal);
  card(s,8.9,1.52,3.75,2.12,'Cases 9–10  |  P–G Gaussian','Puff for instantaneous release; plume for continuous release. Use empirical dispersion coefficients σy and σz.',C.orange);
  addText(s,'Pasquill–Gifford atmospheric stability classes',0.8,4.12,6.3,0.32,{fontSize:15,bold:true,color:C.navy});
  const cls=[['A','Extremely unstable'],['B','Moderately unstable'],['C','Slightly unstable'],['D','Neutral'],['E','Slightly stable'],['F','Moderately stable']];
  for(let i=0;i<6;i++){
    const xx=0.82+(i%3)*2.1, yy=4.62+Math.floor(i/3)*0.75;
    pill(s,cls[i][0],xx,yy,0.48,i===3?'DCEAF7':'E8F3F1',C.navy);
    addText(s,cls[i][1],xx+0.58,yy+0.02,1.45,0.26,{fontSize:10,color:C.dark});
  }
  card(s,7.25,4.25,5.35,1.85,'What the Gaussian coefficients mean','σy describes crosswind spread. σz describes vertical spread. Their values depend on downwind distance and stability class.',C.green);
  addText(s,'The supplied P–G coefficient tables are used for rural conditions.',7.5,6.3,4.8,0.28,{fontSize:10,italic:true,color:C.muted,align:'center'});
}

// Slide 5 – system architecture
{
  const s=pptx.addSlide('MASTER'); addHeader(s,'Software workflow and outputs','The application keeps the user interface separate from the mathematical model functions.');
  const steps=[
    {x:0.7,t:'USER INPUTS',b:'Chemical / MW\nQ or M\nWind / stability / height',c:'EAF1F8'},
    {x:3.25,t:'MODEL ENGINE',b:'Cases 1–8\nP–G puff\nP–G plume',c:'E6F4F3'},
    {x:5.8,t:'CONCENTRATION',b:'C(x, y, z, t)\nkg/m³ → ppmv\nPoint calculation',c:'FDF1E6'},
    {x:8.35,t:'IMPACT CHECK',b:'Compare with\nuser-entered\nthreshold',c:'FCEDEE'},
    {x:10.9,t:'VISUALISE',b:'Contour map\nAffected area\nCSV export',c:'EAF3EA'}
  ];
  steps.forEach((st,i)=>{
    s.addShape(pptx.ShapeType.roundRect,{x:st.x,y:2.25,w:1.85,h:2.1,rectRadius:0.1,fill:{color:st.c},line:{color:'D7E0E8',width:1}});
    addText(s,st.t,st.x+0.08,2.48,1.69,0.3,{fontSize:12,bold:true,color:C.navy,align:'center'});
    addText(s,st.b,st.x+0.1,3.0,1.65,1.05,{fontSize:11,color:C.dark,align:'center'});
    if(i<steps.length-1) s.addShape(pptx.ShapeType.chevron,{x:st.x+1.98,y:3.0,w:0.37,h:0.55,fill:{color:C.teal},line:{color:C.teal}});
  });
  card(s,0.85,4.95,5.55,1.2,'Technology','Python • Streamlit • NumPy • SciPy • Matplotlib • Pandas',C.blue);
  card(s,6.85,4.95,5.55,1.2,'User-visible outputs','Point concentration • ppmv • threshold flag • contour • grid-based affected area • CSV',C.teal);
  addText(s,'All models return concentration in kg/m³ internally so that the user sees consistent units.',1.1,6.55,11.1,0.25,{fontSize:11,bold:true,color:C.blue,align:'center'});
}

// Slide 6 – SO2 validation
{
  const s=pptx.addSlide('MASTER'); addHeader(s,'Validation 1: continuous SO₂ release','Lecture 21, Example 1 – elevated continuous release under rural, neutral (class D) conditions.');
  card(s,0.65,1.45,3.5,2.1,'Inputs','Q = 80 g/s\nH = 60 m\nu = 6 m/s\nx = 500 m\ny = 0 and 50 m\nStability = D',C.blue);
  addText(s,'Program vs lecture',0.78,3.86,3.1,0.3,{fontSize:15,bold:true,color:C.navy});
  addText(s,'Centreline at 500 m\n1.448 × 10⁻⁴ g/m³\nLecture: 1.45 × 10⁻⁴ g/m³\n\n50 m crosswind\n6.374 × 10⁻⁵ g/m³\nLecture: 6.37 × 10⁻⁵ g/m³',0.8,4.25,3.2,1.78,{fontSize:13,color:C.dark,valign:'top'});
  s.addImage({path:path.join(__dirname,'assets/so2_profile.png'),x:4.4,y:1.55,w:8.2,h:4.6});
  addText(s,'The lecture estimates a maximum ground-level concentration of about 4.18 × 10⁻⁴ g/m³ near 1200 m.',4.5,6.32,7.8,0.32,{fontSize:11,bold:true,color:C.blue,align:'center'});
}

// Slide 7 – chlorine puff
{
  const s=pptx.addSlide('MASTER'); addHeader(s,'Validation 2: instantaneous chlorine release','Lecture 21, Example 2 – ground-level puff and the time required to reach a residential area.');
  card(s,0.65,1.5,3.45,1.78,'Inputs','M = 1.0 kg\nu = 2 m/s\nDistance = 500 m\nStability = F\nERPG-1 example = 1 ppm',C.orange);
  card(s,0.65,3.55,3.45,1.58,'Arrival time','t = x/u = 500/2\n= 250 s = 4.17 min',C.teal);
  addText(s,'Model centre estimate',0.82,5.45,3.0,0.28,{fontSize:14,bold:true,color:C.navy});
  addText(s,'≈ 776 ppmv using unrounded coefficients. The lecture rounds σx = σy to 5.0 m and σz to 2.2 m and reports ≈ 798 ppm.',0.82,5.79,3.1,0.82,{fontSize:11,color:C.dark,valign:'top'});
  s.addImage({path:path.join(__dirname,'assets/chlorine_puff_contour.png'),x:4.35,y:1.5,w:8.35,h:4.7});
  addText(s,'Puff centre at x = ut = 500 m when t = 250 s.',4.6,6.32,7.8,0.3,{fontSize:11,bold:true,color:C.blue,align:'center'});
}

// Slide 8 – limitations and conclusion
{
  const s=pptx.addSlide('MASTER'); addHeader(s,'Conclusion, limitations and next steps','A useful educational demonstration – with assumptions that must be made explicit.');
  card(s,0.68,1.5,5.85,2.18,'What the project delivers','• Ten lecture dispersion cases\n• Concentration at a selected point\n• Ground-level concentration contours\n• User-defined threshold comparison\n• Estimated threshold-exceedance area',C.green);
  card(s,6.8,1.5,5.85,2.18,'Important limitations','• Neutrally buoyant Gaussian assumption\n• Rural P–G correlations\n• No dense-gas slumping / CFD\n• No complex buildings or changing wind\n• Not for live emergency response',C.orange);
  addText(s,'Future scope',0.85,4.15,3.0,0.34,{fontSize:16,bold:true,color:C.navy});
  const fut=['Changing wind direction','Urban / terrain effects','Dense-gas model','GIS-based mapping','Verified toxicity database'];
  fut.forEach((t,i)=>pill(s,t,0.85+i*2.38,4.72,2.15,'E8F0F7',C.blue));
  s.addShape(pptx.ShapeType.roundRect,{x:1.0,y:5.65,w:11.35,h:0.78,rectRadius:0.12,fill:{color:C.navy},line:{color:C.navy}});
  addText(s,'ToxiDisp connects chemical-process safety theory with mathematical modelling and Python-based visualisation.',1.25,5.84,10.85,0.38,{fontSize:16,bold:true,color:C.white,align:'center'});
  addText(s,'References: supplied Lecture 19, Lecture 20 and Lecture 21 dispersion-model slides.',1.1,6.63,11.1,0.25,{fontSize:9,color:C.muted,align:'center'});
}

pptx.writeFile({ fileName: path.join(__dirname,'ToxiDisp_Presentation.pptx') });
