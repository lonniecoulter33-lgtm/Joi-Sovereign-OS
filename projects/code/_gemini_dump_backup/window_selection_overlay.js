(()=>{"use strict";var x={838527:(e,s,t)=>{var n=t(275271),a=t(230967),o=t(992671),i=t(172298);const c="window-selection-renderer-did-select-window",l="window-selection-renderer-update-app-name",d="window-selection-renderer-paint-complete";var f=t(212612),v=t(974144);const E=v.is.macos?16:8,w=o.Z.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  // Primary at 25% opacity
  background-color: hsla(215.4, 80%, 47.65%, 0.25);
  border: ${({showSelection:p})=>p?"2px dashed var(--lns-color-primary)":"2px solid transparent"};
  box-sizing: border-box;
  pointer-events: none;
  border-radius: ${({showSelection:p})=>p?`${E}px`:"0"};
`,b=o.Z.div`
  position: fixed;
  inset: 0;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
`,y=o.Z.div`
  padding: 16px 64px;
  width: fit-content;
  max-width: calc(100% - 128px);
  background-color: rgba(0, 0, 0, 0.75);
  border-radius: 999px;
  text-align: center;
  white-space: nowrap;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0;

  span {
    color: #fff;
    font-size: 24px;
    font-weight: 600;
  }

  small {
    font-size: 12px;
    font-weight: normal;
    color: rgba(255, 255, 255, 0.5);
  }
`,R=()=>{const[p,j]=(0,n.useState)(null);return(0,n.useEffect)(()=>{const u=()=>{(0,f.A)(()=>{i.ipcRenderer.send(d)})};return window.addEventListener("resize",u),()=>{window.removeEventListener("resize",u)}},[]),(0,n.useEffect)(()=>{const u=(C,g)=>{j(g??null)};return i.ipcRenderer.on(l,u),()=>{i.ipcRenderer.removeListener(l,u)}},[]),n.createElement(n.Fragment,null,n.createElement(w,{showSelection:Boolean(p)}),!p&&n.createElement(b,null,n.createElement(y,null,n.createElement("span",null,"Hover over a window to select"),n.createElement("small",null,"Escape to cancel"))))};var N=t(474176),S=t(110720),I=t(199384);(0,S.jC)(),(0,N.u)();const h=document.createElement("div"),_="container";h.id=_,document.body.appendChild(h),document.title="Loom Window Selection Overlay";const P=document.getElementById(_);(p=>(0,a.render)(n.createElement(n.Fragment,null,n.createElement(I.x,null),n.createElement(p,null)),P))(R)},439491:e=>{e.exports=require("assert")},172298:e=>{e.exports=require("electron")},582361:e=>{e.exports=require("events")},657147:e=>{e.exports=require("fs")},113685:e=>{e.exports=require("http")},795687:e=>{e.exports=require("https")},822037:e=>{e.exports=require("os")},371017:e=>{e.exports=require("path")},863477:e=>{e.exports=require("querystring")},257310:e=>{e.exports=require("url")},473837:e=>{e.exports=require("util")}},m={};function r(e){var s=m[e];if(s!==void 0)return s.exports;var t=m[e]={id:e,loaded:!1,exports:{}};return x[e].call(t.exports,t,t.exports,r),t.loaded=!0,t.exports}r.m=x,r.c=m,(()=>{var e=[];r.O=(s,t,n,a)=>{if(t){a=a||0;for(var o=e.length;o>0&&e[o-1][2]>a;o--)e[o]=e[o-1];e[o]=[t,n,a];return}for(var i=1/0,o=0;o<e.length;o++){for(var[t,n,a]=e[o],c=!0,l=0;l<t.length;l++)(a&!1||i>=a)&&Object.keys(r.O).every(b=>r.O[b](t[l]))?t.splice(l--,1):(c=!1,a<i&&(i=a));if(c){e.splice(o--,1);var d=n();d!==void 0&&(s=d)}}return s}})(),r.n=e=>{var s=e&&e.__esModule?()=>e.default:()=>e;return r.d(s,{a:s}),s},(()=>{var e=Object.getPrototypeOf?t=>Object.getPrototypeOf(t):t=>t.__proto__,s;r.t=function(t,n){if(n&1&&(t=this(t)),n&8||typeof t=="object"&&t&&(n&4&&t.__esModule||n&16&&typeof t.then=="function"))return t;var a=Object.create(null);r.r(a);var o={};s=s||[null,e({}),e([]),e(e)];for(var i=n&2&&t;typeof i=="object"&&!~s.indexOf(i);i=e(i))Object.getOwnPropertyNames(i).forEach(c=>o[c]=()=>t[c]);return o.default=()=>t,r.d(a,o),a}})(),r.d=(e,s)=>{for(var t in s)r.o(s,t)&&!r.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:s[t]})},r.h=()=>"55e5c6a40d444554bfb1",r.hmd=e=>(e=Object.create(e),e.children||(e.children=[]),Object.defineProperty(e,"exports",{enumerable:!0,set:()=>{throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+e.id)}}),e),r.o=(e,s)=>Object.prototype.hasOwnProperty.call(e,s),r.r=e=>{typeof Symbol<"u"&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{var e={4106:0};r.O.j=n=>e[n]===0;var s=(n,a)=>{var[o,i,c]=a,l,d,f=0;if(o.some(E=>e[E]!==0)){for(l in i)r.o(i,l)&&(r.m[l]=i[l]);if(c)var v=c(r)}for(n&&n(a);f<o.length;f++)d=o[f],r.o(e,d)&&e[d]&&e[d][0](),e[o[f]]=0;return r.O(v)},t=global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[];t.forEach(s.bind(null,0)),t.push=s.bind(null,t.push.bind(t))})(),r.O(void 0,[592,6491,7981,719,947,3780,680,2772],()=>r(r.s=903679)),r.O(void 0,[592,6491,7981,719,947,3780,680,2772],()=>r(r.s=838527)),r.O(void 0,[592,6491,7981,719,947,3780,680,2772],()=>r(r.s=639542));var O=r.O(void 0,[592,6491,7981,719,947,3780,680,2772],()=>r(r.s=194383));O=r.O(O)})();

//# sourceMappingURL=window_selection_overlay.js.map