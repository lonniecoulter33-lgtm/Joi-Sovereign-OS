(()=>{"use strict";var O={300514:(e,o,r)=>{var n=r(275271),a=r(230967),s=r(992671),i=r(172298),c=r(183780);const l="window-selection-renderer-did-select-window",d="window-selection-renderer-update-app-name",p="window-selection-renderer-paint-complete";var b=r(212612);const h=s.Z.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  margin: 0;
  padding: 0;
`,y=(0,s.Z)(c.zxk)`
  background-color: var(--lns-color-primary);
  color: white;
  border: none;
  outline: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);

  &:focus {
    outline: none;
  }

  &:hover {
    background-color: var(--lns-color-primary);
  }

  &:active {
    background-color: var(--lns-color-primary);
  }

  &:focus-visible {
    outline: none;
  }

  &:focus-within {
    outline: none;
  }
`,v=()=>{const[u,P]=(0,n.useState)(null);(0,n.useEffect)(()=>{const _=(I,g)=>{P(g??null)};return i.ipcRenderer.on(d,_),()=>{i.ipcRenderer.removeListener(d,_)}},[]),(0,n.useEffect)(()=>{(0,b.A)(()=>{i.ipcRenderer.send(p)})},[u]);const k=()=>{i.ipcRenderer.send(l)},j=u?`Select ${u}`:"Select Window";return n.createElement(h,null,n.createElement(y,{onClick:k},j))};var w=r(474176),S=r(110720),R=r(199384);(0,S.jC)(),(0,w.u)();const E=document.createElement("div"),x="container";E.id=x,document.body.appendChild(E),document.title="Loom Window Selection Overlay Button";const N=document.getElementById(x);(u=>(0,a.render)(n.createElement(n.Fragment,null,n.createElement(R.x,null),n.createElement(u,null)),N))(v)},439491:e=>{e.exports=require("assert")},172298:e=>{e.exports=require("electron")},582361:e=>{e.exports=require("events")},657147:e=>{e.exports=require("fs")},113685:e=>{e.exports=require("http")},795687:e=>{e.exports=require("https")},822037:e=>{e.exports=require("os")},371017:e=>{e.exports=require("path")},863477:e=>{e.exports=require("querystring")},257310:e=>{e.exports=require("url")},473837:e=>{e.exports=require("util")}},f={};function t(e){var o=f[e];if(o!==void 0)return o.exports;var r=f[e]={id:e,loaded:!1,exports:{}};return O[e].call(r.exports,r,r.exports,t),r.loaded=!0,r.exports}t.m=O,t.c=f,(()=>{var e=[];t.O=(o,r,n,a)=>{if(r){a=a||0;for(var s=e.length;s>0&&e[s-1][2]>a;s--)e[s]=e[s-1];e[s]=[r,n,a];return}for(var i=1/0,s=0;s<e.length;s++){for(var[r,n,a]=e[s],c=!0,l=0;l<r.length;l++)(a&!1||i>=a)&&Object.keys(t.O).every(v=>t.O[v](r[l]))?r.splice(l--,1):(c=!1,a<i&&(i=a));if(c){e.splice(s--,1);var d=n();d!==void 0&&(o=d)}}return o}})(),t.n=e=>{var o=e&&e.__esModule?()=>e.default:()=>e;return t.d(o,{a:o}),o},(()=>{var e=Object.getPrototypeOf?r=>Object.getPrototypeOf(r):r=>r.__proto__,o;t.t=function(r,n){if(n&1&&(r=this(r)),n&8||typeof r=="object"&&r&&(n&4&&r.__esModule||n&16&&typeof r.then=="function"))return r;var a=Object.create(null);t.r(a);var s={};o=o||[null,e({}),e([]),e(e)];for(var i=n&2&&r;typeof i=="object"&&!~o.indexOf(i);i=e(i))Object.getOwnPropertyNames(i).forEach(c=>s[c]=()=>r[c]);return s.default=()=>r,t.d(a,s),a}})(),t.d=(e,o)=>{for(var r in o)t.o(o,r)&&!t.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:o[r]})},t.h=()=>"55e5c6a40d444554bfb1",t.hmd=e=>(e=Object.create(e),e.children||(e.children=[]),Object.defineProperty(e,"exports",{enumerable:!0,set:()=>{throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+e.id)}}),e),t.o=(e,o)=>Object.prototype.hasOwnProperty.call(e,o),t.r=e=>{typeof Symbol<"u"&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{var e={3745:0};t.O.j=n=>e[n]===0;var o=(n,a)=>{var[s,i,c]=a,l,d,p=0;if(s.some(h=>e[h]!==0)){for(l in i)t.o(i,l)&&(t.m[l]=i[l]);if(c)var b=c(t)}for(n&&n(a);p<s.length;p++)d=s[p],t.o(e,d)&&e[d]&&e[d][0](),e[s[p]]=0;return t.O(b)},r=global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[];r.forEach(o.bind(null,0)),r.push=o.bind(null,r.push.bind(r))})(),t.O(void 0,[592,6491,7981,719,5800,680,9724,2772],()=>t(t.s=903679)),t.O(void 0,[592,6491,7981,719,5800,680,9724,2772],()=>t(t.s=300514)),t.O(void 0,[592,6491,7981,719,5800,680,9724,2772],()=>t(t.s=639542));var m=t.O(void 0,[592,6491,7981,719,5800,680,9724,2772],()=>t(t.s=194383));m=t.O(m)})();

//# sourceMappingURL=window_selection_overlay_button.js.map