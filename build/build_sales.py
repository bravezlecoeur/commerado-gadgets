# Builds commerado-gadgets/sales-today.js from the dashboard photo file (images.js JSON export).
import json, re, base64, io, sys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
t = json.load(open(src))['text']
I = dict(re.findall(r'"([0-9a-f]{8})":"(data:image/[^"]+)"', t))
S = json.loads('{' + re.search(r'S=\{(.*?)\}', t).group(1) + '}')
img = {}
for k, v in I.items():
    if k not in S.values():
        continue
    im = Image.open(io.BytesIO(base64.b64decode(v.split(',', 1)[1]))).convert('RGB')
    im.thumbnail((48, 48)); b = io.BytesIO(); im.save(b, 'JPEG', quality=55, optimize=True)
    img[k] = base64.b64encode(b.getvalue()).decode()
skus = {s: k for s, k in S.items() if k in img}
css = r"""
.cg{font-family:'Outfit',system-ui,sans-serif;background:#FCFBF7;border:1px solid #ECE6D8;border-radius:24px;overflow:hidden;color:#232220}
.cg .h{background:#232220;padding:14px 18px;display:flex;align-items:center;gap:12px}
.cg .m{width:34px;height:34px;border-radius:10px;background:#F2CE5C;display:grid;place-items:center;font-weight:700;font-size:18px;color:#232220}
.cg .t{flex:1;color:#F3EFE4;font-weight:600;font-size:16px}.cg .t small{display:block;color:#9C968A;font-size:12.5px;font-weight:400}
.cg .b{padding:16px 18px 14px;border-bottom:1px solid #E6E0D2}.cg .l{font-size:13px;color:#6E6A60}
.cg .big{font-size:34px;font-weight:700}.cg .big span{font-size:15px;font-weight:500;color:#6E6A60;margin-left:4px}
.cg .sub{font-size:13px;color:#6E6A60;margin-top:2px}.cg .sub b{color:#232220;font-weight:600}
.cg summary{list-style:none;cursor:pointer}.cg summary::-webkit-details-marker{display:none}
.cg .r{display:flex;align-items:center;gap:10px;padding:11px 18px;border-bottom:1px solid #F0EBE0}.cg .r>div:first-child{flex:1}
.cg .r b{font-size:15px;font-weight:600}.cg .r i{display:block;height:6px;border-radius:3px;background:#F1EBDA;margin-top:6px}
.cg .r i u{display:block;height:100%;border-radius:3px;background:#F2CE5C}
.cg .v{text-align:right;font-size:15px;font-weight:600;white-space:nowrap}.cg .v em{display:block;font-size:12.5px;font-style:normal;color:#6E6A60;font-weight:400}
.cg .c{color:#9C968A;font-size:20px;transition:transform .2s}.cg details[open] .c{transform:rotate(90deg)}
.cg .x{background:#F5F2EA;margin:8px 12px;border-radius:14px;padding:4px 0}
.cg .s{display:flex;align-items:center;gap:10px;padding:8px 12px;border-bottom:1px solid #ECE6D8}.cg .s:last-child{border-bottom:0}
.cg .s>div:nth-child(2){flex:1;min-width:0}.cg .s b{font-size:14px;font-weight:600;overflow-wrap:anywhere}
.cg .ph{width:40px;height:40px;border-radius:10px;background:#fff center/cover no-repeat;border:1px solid #ECE6D8;flex:none}
.cg .n{background:#FDF0CC;color:#8E6512;font-size:12.5px;padding:10px 18px}
"""
js = """/* Commerado gadgets - Sales card (v%(v)s). Template only: no sales data lives here.
   Use: <div id="cg"></div><script>window.CG_DATA={...}</script><script src=".../sales-today.js"></script>
   Data: {title, subtitle, total, refunds, net, note, mk:[{name, amount, units, skus:[[sku, amount, units], ...]}]}
   Built from the Commerado dashboard photo file by build/build_sales.py. */
(function(){
var IMG=%(img)s, SKU=%(sku)s;
var CSS=%(css)s;
function f(n){return Math.round(n).toLocaleString('en-US');}
function e(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function u(n){return f(n)+(Math.round(n)===1?' unit':' units');}
function ph(s){var k=SKU[s];return k?' style="background-image:url(data:image/jpeg;base64,'+IMG[k]+')"':'';}
function sales(id,d){
  var el=typeof id==='string'?document.getElementById(id):id; if(!el)return;
  if(!document.getElementById('cg-css')){var st=document.createElement('style');st.id='cg-css';st.textContent=CSS;document.head.appendChild(st);
    var ln=document.createElement('link');ln.rel='stylesheet';ln.href='https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap';document.head.appendChild(ln);}
  var mx=Math.max.apply(null,(d.mk||[]).map(function(m){return m.amount;}).concat([1]));
  var h='<div class="cg"><div class="h"><div class="m">C</div><div class="t">'+e(d.title||'Sales')+'<small>'+e(d.subtitle||'')+'</small></div></div>'+
    '<div class="b"><div class="l">Sales</div><div class="big">'+f(d.total)+'<span>AED</span></div>'+
    '<div class="sub">Refunds <b>'+f(d.refunds||0)+'</b> &middot; Net sales <b>'+f(d.net!=null?d.net:d.total-(d.refunds||0))+'</b></div></div>';
  (d.mk||[]).forEach(function(m){
    h+='<details><summary class="r"><div><b>'+e(m.name)+'</b><i><u style="width:'+Math.round(m.amount/mx*100)+'%%"></u></i></div>'+
      '<div class="v">'+f(m.amount)+'<em>'+u(m.units)+'</em></div><span class="c">&rsaquo;</span></summary><div class="x">';
    (m.skus||[]).forEach(function(s){h+='<div class="s"><span class="ph"'+ph(s[0])+'></span><div><b>'+e(String(s[0]).replace(/^PEGANT_/,''))+'</b></div><div class="v">'+f(s[1])+'<em>'+u(s[2])+'</em></div></div>';});
    h+='</div></details>';});
  if(d.note)h+='<div class="n">'+e(d.note)+'</div>';
  el.innerHTML=h+'</div>';
}
window.CG=window.CG||{}; window.CG.sales=sales; window.CG.version='%(v)s';
if(window.CG_DATA)sales(window.CG_DATA.el||'cg',window.CG_DATA);
})();
""" % {'v': '1', 'img': json.dumps(img, separators=(',', ':')), 'sku': json.dumps(skus, separators=(',', ':')), 'css': json.dumps(css.strip())}
open(out, 'w').write(js)
print(len(img), 'photos,', len(skus), 'SKUs,', len(js), 'bytes')
