import { app } from "../../scripts/app.js";

function propKey(inputName) { return `__bv_${inputName}`; }
function getProp(node, k, fallback) {
  node.properties = node.properties || {};
  return Object.prototype.hasOwnProperty.call(node.properties, k) ? node.properties[k] : fallback;
}
function setProp(node, k, v) {
  node.properties = node.properties || {};
  node.properties[k] = v;
}

function roundRect(ctx, x, y, w, h, r) {
  const rr = Math.min(r, h / 2, w / 2);
  ctx.beginPath();
  ctx.moveTo(x + rr, y);
  ctx.lineTo(x + w - rr, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + rr);
  ctx.lineTo(x + w, y + h - rr);
  ctx.quadraticCurveTo(x + w, y + h, x + w - rr, y + h);
  ctx.lineTo(x + rr, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - rr);
  ctx.lineTo(x, y + rr);
  ctx.quadraticCurveTo(x, y, x + rr, y);
  ctx.closePath();
}
function drawBar(ctx, x, y, w, h, t) {
  const r = Math.min(h / 2, 6);
  const tt = Math.max(0, Math.min(1, t));
  ctx.save();
  ctx.fillStyle = "rgba(255,255,255,0.10)";
  roundRect(ctx, x, y, w, h, r);
  ctx.fill();
  const fw = Math.max(r * 2, w * tt);
  ctx.fillStyle = "rgba(255,255,255,0.35)";
  roundRect(ctx, x, y, fw, h, r);
  ctx.fill();
  ctx.restore();
}

function makeEditableHeadingFactory({ fontSize=18, fontWeight=700, color=null, lineHeight=null, paddingY=6, multiline=false, placeholder="" }) {
  return (node, inputName, inputData, _app) => {
    const optsIn = (Array.isArray(inputData) && inputData[1]) ? inputData[1] : (inputData?.options || {});
    const def = optsIn?.default ?? optsIn?.placeholder ?? placeholder;
    const key = propKey(inputName);
    const initial = (node.properties && Object.prototype.hasOwnProperty.call(node.properties, key)) ? node.properties[key] : def;

    const w = node.addWidget("text", inputName, initial, (v) => {
      const val = v ?? "";
      w.value = val;
      setProp(node, key, val);
      node.setDirtyCanvas(true, true);
    }, { serialize:false, multiline, placeholder });

    if (node.properties && Object.prototype.hasOwnProperty.call(node.properties, key)) {
      w.value = node.properties[key];
    }

    w.draw = function draw(ctx, n, widgetWidth, y) {
      const txt = (this.value ?? "").toString();
      const lines = txt.split("\n");
      const lh = lineHeight ?? fontSize + 2;

      ctx.save();
      ctx.font = `${fontWeight} ${fontSize}px Inter, system-ui, sans-serif`;
      ctx.fillStyle = color ?? (n?.fgcolor || "#ddd");
      ctx.textBaseline = "top";

      let yy = y + paddingY;
      for (const line of lines) {
        ctx.fillText(line, 12, yy);
        yy += lh;
      }
      ctx.restore();
    };

    w.computeSize = function computeSize(widgetWidth) {
      const txt = (this.value ?? "").toString();
      const lines = Math.max(1, txt.split("\n").length);
      const lh = lineHeight ?? fontSize + 2;
      return [widgetWidth, paddingY * 2 + lines * lh];
    };

    return { widget: w };
  };
}

function makeDividerFactory() {
  return (node, inputName) => {
    const w = node.addCustomWidget({
      type: "bv_divider",
      name: inputName,
      serialize: false,
      draw: function (ctx, n, widgetWidth, y) {
        ctx.save();
        ctx.strokeStyle = n?.fgcolor || "#999";
        ctx.globalAlpha = 0.4;
        ctx.beginPath();
        ctx.moveTo(8, y + 8);
        ctx.lineTo(widgetWidth - 8, y + 8);
        ctx.stroke();
        ctx.restore();
      },
      computeSize: function (widgetWidth) { return [widgetWidth, 16]; },
    });
    return { widget: w };
  };
}

function makeSpacerFactory() {
  return (node, inputName) => {
    const w = node.addCustomWidget({
      type: "bv_spacer",
      name: inputName,
      serialize: false,
      draw: function (ctx, _n, widgetWidth, y) {
        ctx.save();
        ctx.fillStyle = "#0000";
        ctx.fillRect(8, y + 8, widgetWidth - 16, 50);
        ctx.restore();
      },
      computeSize: function (widgetWidth) { return [widgetWidth, 50]; },
    });
    return { widget: w };
  };
}

function makeIntSliderFactory() {
  return (node, inputName, inputData, _app) => {
    const defMin=0, defMax=100, defStep=1;
    const kVal  = propKey(`${inputName}_value`);
    const kMin  = propKey(`${inputName}_min`);
    const kMax  = propKey(`${inputName}_max`);
    const kStep = propKey(`${inputName}_step`);
    const kPre  = propKey(`${inputName}_prefix`);
    const kSuf  = propKey(`${inputName}_suffix`);

    const optsIn  = (Array.isArray(inputData) && inputData[1]) ? inputData[1] : (inputData?.options || {});
    const initial = getProp(node, kVal, Number.isFinite(optsIn?.default) ? optsIn.default : 0);

    node.addWidget("number", "min",    getProp(node,kMin, defMin),  v=>{ setProp(node,kMin,  Number.isFinite(v)? Math.floor(v):defMin); node.setDirtyCanvas(true,true); }, {serialize:false, precision:0});
    node.addWidget("number", "max",    getProp(node,kMax, defMax),  v=>{ setProp(node,kMax,  Number.isFinite(v)? Math.floor(v):defMax); node.setDirtyCanvas(true,true); }, {serialize:false, precision:0});
    node.addWidget("number", "step",   getProp(node,kStep,defStep), v=>{ setProp(node,kStep, Number.isFinite(v)? Math.max(1,Math.floor(v)):defStep); node.setDirtyCanvas(true,true); }, {serialize:false, precision:0});
    node.addWidget("text",   "prefix", getProp(node,kPre,""),       v=>{ setProp(node,kPre, v ?? ""); node.setDirtyCanvas(true,true); }, {serialize:false});
    node.addWidget("text",   "suffix", getProp(node,kSuf,""),       v=>{ setProp(node,kSuf, v ?? ""); node.setDirtyCanvas(true,true); }, {serialize:false});

    function snapInt(v){
      const min=getProp(node,kMin,defMin);
      const max=getProp(node,kMax,defMax);
      const step=getProp(node,kStep,defStep);
      let nv = Number(v); if(!Number.isFinite(nv)) nv=0;
      const st = Math.max(1, Math.floor(step));
      nv = Math.round(nv / st) * st;
      nv = Math.min(max, Math.max(min, nv));
      nv = Math.round(nv);
      return { nv, min, max, step: st };
    }

    const { nv:start, min:sMin, max:sMax, step:sStep } = snapInt(initial);

    const wValue = node.addWidget("slider", "value", start, v=>{
      const { nv } = snapInt(v);
      setProp(node,kVal,nv);
      wValue.value = nv;
      node.setDirtyCanvas(true,true);
    }, { serialize:true, min:sMin, max:sMax, step:sStep, precision:0 });

    function applyOptionsFromProps(){
      const { min, max, step } = snapInt(getProp(node,kVal,wValue.value));
      wValue.options.min = min;
      wValue.options.max = max;
      wValue.options.step = step;
      wValue.options.precision = 0;
    }
    applyOptionsFromProps();

    function ensureSynced(){
      const { nv } = snapInt(getProp(node,kVal,wValue.value));
      setProp(node,kVal,nv);
      wValue.value = nv;
      applyOptionsFromProps();
    }

    const prevOnSerialize = node.onSerialize;
    node.onSerialize = function(data){ ensureSynced(); if(prevOnSerialize) prevOnSerialize.call(this,data); };
    wValue.serializeValue = function(){ ensureSynced(); return snapInt(getProp(node,kVal,wValue.value)).nv; };

    const prevOnConfigure = node.onConfigure;
    node.onConfigure = function(o){ applyOptionsFromProps(); if(prevOnConfigure) prevOnConfigure.call(this,o); };

    wValue.draw = function(ctx, n, widgetWidth, y) {
      const h=22, x=6, w=widgetWidth-12;
      const { min, max } = snapInt(getProp(node,kVal,wValue.value));
      const val = Number(getProp(node,kVal,wValue.value));
      const t = (val - min) / Math.max(1e-9, (max - min));
      ctx.save();
      ctx.clearRect(x,y,w,h);
      drawBar(ctx, x, y+2, w, h-4, Math.max(0, Math.min(1, t)));
      const pre = getProp(node,kPre,"");
      const suf = getProp(node,kSuf,"");
      const text = `${pre}${val}${suf}`;
      ctx.font = `600 13px Inter, system-ui, sans-serif`;
      ctx.fillStyle = n?.fgcolor || "#ddd";
      ctx.textBaseline = "middle";
      const tw = ctx.measureText(text).width;
      const tx = Math.max(12, x + (w - tw)/2);
      ctx.fillText(text, tx, y + h/2);
      ctx.restore();
    };

    const prevOnFG = node.onDrawForeground;
    node.onDrawForeground = function(ctx){
      const { nv, min, max, step } = snapInt(getProp(node,kVal,wValue.value));
      if (wValue.value !== nv) wValue.value = nv;
      wValue.options.min = min; wValue.options.max = max; wValue.options.step = step; wValue.options.precision = 0;
      if (prevOnFG) prevOnFG.call(this, ctx);
    };

    return { widget: wValue };
  };
}

function makeFixedFloatSliderFactory(FIXED_PREC) {
  return (node, inputName, inputData, _app) => {
    const defMin=0.0, defMax=1.0;
    const defStep = Number((1 / Math.pow(10, FIXED_PREC)).toFixed(FIXED_PREC));

    const kVal  = propKey(`${inputName}_value`);
    const kMin  = propKey(`${inputName}_min`);
    const kMax  = propKey(`${inputName}_max`);
    const kStep = propKey(`${inputName}_step`);
    const kPre  = propKey(`${inputName}_prefix`);
    const kSuf  = propKey(`${inputName}_suffix`);

    const optsIn  = (Array.isArray(inputData) && inputData[1]) ? inputData[1] : (inputData?.options || {});
    const initial = getProp(node, kVal, Number.isFinite(optsIn?.default) ? optsIn.default : 0.0);

    node.addWidget("number","min",  getProp(node,kMin, defMin),  v=>{ setProp(node,kMin, Number.isFinite(v)? v : defMin); node.setDirtyCanvas(true,true); }, {serialize:false});
    node.addWidget("number","max",  getProp(node,kMax, defMax),  v=>{ setProp(node,kMax, Number.isFinite(v)? v : defMax); node.setDirtyCanvas(true,true); }, {serialize:false});
    node.addWidget("number","step", getProp(node,kStep,defStep), v=>{ setProp(node,kStep,(Number.isFinite(v)&&v>0)? v : defStep); node.setDirtyCanvas(true,true); }, {serialize:false});
    node.addWidget("text","prefix", getProp(node,kPre,""),       v=>{ setProp(node,kPre, v ?? ""); node.setDirtyCanvas(true,true); }, {serialize:false});
    node.addWidget("text","suffix", getProp(node,kSuf,""),       v=>{ setProp(node,kSuf, v ?? ""); node.setDirtyCanvas(true,true); }, {serialize:false});

    function quantize(v){
      const min = getProp(node,kMin,defMin);
      const max = getProp(node,kMax,defMax);
      const step = getProp(node,kStep,defStep);
      const scale = Math.pow(10, FIXED_PREC);

      let vi = Math.round(Number(v) * scale);
      const minI  = Math.round(min  * scale);
      const maxI  = Math.round(max  * scale);
      const stepI = Math.max(1, Math.round(step * scale));

      vi = Math.min(maxI, Math.max(minI, vi));
      vi = Math.round((vi - minI) / stepI) * stepI + minI;

      const nv = vi / scale;
      return { nv, min, max, step };
    }

    const { nv:start, min:sMin, max:sMax, step:sStep } = quantize(initial);

    const wValue = node.addWidget("slider", "value", start, v=>{
      const { nv } = quantize(v);
      setProp(node,kVal,nv);
      wValue.value = nv;
      node.setDirtyCanvas(true,true);
    }, { serialize:true, min:sMin, max:sMax, step:sStep, precision: FIXED_PREC });

    function applyOptionsFromProps(){
      const { min, max, step } = quantize(getProp(node,kVal,wValue.value));
      wValue.options.min = min;
      wValue.options.max = max;
      wValue.options.step = step;
      wValue.options.precision = FIXED_PREC;
    }
    applyOptionsFromProps();

    function ensureSynced(){
      const { nv } = quantize(getProp(node,kVal,wValue.value));
      setProp(node,kVal,nv);
      wValue.value = nv;
      applyOptionsFromProps();
    }

    const prevOnSerialize = node.onSerialize;
    node.onSerialize = function(data){ ensureSynced(); if(prevOnSerialize) prevOnSerialize.call(this,data); };
    wValue.serializeValue = function(){ ensureSynced(); return quantize(getProp(node,kVal,wValue.value)).nv; };

    const prevOnConfigure = node.onConfigure;
    node.onConfigure = function(o){ applyOptionsFromProps(); if(prevOnConfigure) prevOnConfigure.call(this,o); };

    wValue.draw = function(ctx, n, widgetWidth, y) {
      const h=22, x=6, w=widgetWidth-12;
      const { min, max } = quantize(getProp(node,kVal,wValue.value));
      const val = Number(getProp(node,kVal,wValue.value));
      const t = (val - min) / Math.max(1e-9, (max - min));

      ctx.save();
      ctx.clearRect(x,y,w,h);
      drawBar(ctx, x, y+2, w, h-4, Math.max(0, Math.min(1, t)));

      const pre = getProp(node,kPre,"");
      const suf = getProp(node,kSuf,"");
      const text = `${pre}${val.toFixed(FIXED_PREC)}${suf}`;
      ctx.font = `600 13px Inter, system-ui, sans-serif`;
      ctx.fillStyle = n?.fgcolor || "#ddd";
      ctx.textBaseline = "middle";
      const tw = ctx.measureText(text).width;
      const tx = Math.max(12, x + (w - tw)/2);
      ctx.fillText(text, tx, y + h/2);
      ctx.restore();
    };

    const prevOnFG = node.onDrawForeground;
    node.onDrawForeground = function(ctx){
      const { nv, min, max, step } = quantize(getProp(node,kVal,wValue.value));
      if (wValue.value !== nv) wValue.value = nv;
      wValue.options.min = min; wValue.options.max = max; wValue.options.step = step; wValue.options.precision = FIXED_PREC;
      if (prevOnFG) prevOnFG.call(this, ctx);
    };

    return { widget: wValue };
  };
}

app.registerExtension({
  name: "bv.subgraph.widgets",
  async getCustomWidgets() {
    return {
      "BV_SUB_TITLE":     makeEditableHeadingFactory({ fontSize: 22, fontWeight: 800, placeholder: "Section Title" }),
      "BV_SUB_HEADING":   makeEditableHeadingFactory({ fontSize: 18, fontWeight: 700, placeholder: "Heading" }),
      "BV_SUB_DIVIDER":   makeDividerFactory(),
      "BV_SUB_SPACER":    makeSpacerFactory(),
      "BV_SUB_INT_SLIDER":    makeIntSliderFactory(),
      "BV_SUB_FLOAT1_SLIDER": makeFixedFloatSliderFactory(1),
      "BV_SUB_FLOAT2_SLIDER": makeFixedFloatSliderFactory(2),
      "BV_SUB_FLOAT3_SLIDER": makeFixedFloatSliderFactory(3),
    };
  },
});
