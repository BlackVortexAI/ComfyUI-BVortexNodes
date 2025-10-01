import { app } from "../../scripts/app.js";

function getKey(inputName) {
  // stabiler, eindeutiger Property-Key je Eingabename
  return `__bv_${inputName}`;
}

function makeEditableHeadingFactory({
  fontSize = 18,
  fontWeight = 700,
  color = null,
  lineHeight = null,
  paddingY = 6,
  multiline = false,
  placeholder = ""
}) {
  return (node, inputName, inputData, _app) => {
    const optsIn = (Array.isArray(inputData) && inputData[1])
      ? inputData[1]
      : (inputData?.options || {});
    const def = optsIn?.default ?? optsIn?.placeholder ?? placeholder;

    const key = getKey(inputName);
    const initial = (node.properties && Object.prototype.hasOwnProperty.call(node.properties, key))
      ? node.properties[key]
      : def;

    const w = node.addWidget("text", inputName, initial, (v) => {
      const val = v ?? "";
      w.value = val;
      node.properties = node.properties || {};
      node.properties[key] = val;
      node?.setDirtyCanvas(true, true);
    }, {
      serialize: false,
      multiline,
      placeholder
    });

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
      type: "rv_divider",
      name: inputName,
      serialize: false, // nichts speichern
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
      computeSize: function (widgetWidth) {
        return [widgetWidth, 16];
      },
    });
    return { widget: w };
  };
}

function makeSpacerFactory() {
  return (node, inputName) => {
    const w = node.addCustomWidget({
      type: "rv_spacer",
      name: inputName,
      serialize: false,
      draw: function (ctx, _n, widgetWidth, y) {
        ctx.save();
        ctx.fillStyle = "#00000000";
        ctx.fillRect(8, y + 8, widgetWidth - 16, 50);
        ctx.restore();
      },
      computeSize: function (widgetWidth) {
        return [widgetWidth, 50];
      },
    });
    return { widget: w };
  };
}

app.registerExtension({
  name: "bv.subgraph.widgets",
  async getCustomWidgets() {
    return {
      "BV_SUB_TITLE":   makeEditableHeadingFactory({ fontSize: 22, fontWeight: 800, placeholder: "Section Title" }),
      "BV_SUB_HEADING": makeEditableHeadingFactory({ fontSize: 18, fontWeight: 700,  placeholder: "Heading" }),
      "BV_SUB_DIVIDER": makeDividerFactory(),
      "BV_SUB_SPACER":  makeSpacerFactory(),
    };
  },
});
