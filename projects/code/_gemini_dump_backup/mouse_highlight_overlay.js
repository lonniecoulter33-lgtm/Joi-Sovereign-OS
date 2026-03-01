(()=>{var A={533400:(e,o,t)=>{var r=t(744917),a=t(570097),c=t(969975);o=r(!1);var u=a(c);o.push([e.id,`@font-face {
  font-weight: 400 653;
  font-style: normal;
  font-family: 'Atlassian Sans';
  src: url(`+u+`) format('woff2');
  font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
.font-tiny-semi-bold {
  font-size: 12px;
  line-height: 18px;
  font-weight: 500;
  font-family: 'Atlassian Sans', ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, system-ui, "Helvetica Neue", sans-serif;
}
.font-tiny {
  font-size: 12px;
  line-height: 18px;
  font-weight: 400;
  font-family: 'Atlassian Sans', ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, system-ui, "Helvetica Neue", sans-serif;
}
.font-small {
  font-size: 14px;
  line-height: 18px;
  font-weight: 400;
  font-family: 'Atlassian Sans', ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, system-ui, "Helvetica Neue", sans-serif;
}
.font-large-bold {
  font-size: 18px;
  line-height: 24px;
  font-weight: 700;
  font-family: 'Atlassian Sans', ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, system-ui, "Helvetica Neue", sans-serif;
}
html,
body,
#container {
  overflow: hidden;
  margin: 0;
  width: 100%;
  height: 100%;
}
.mouse-highlight-circle {
  position: absolute;
  top: 0;
  left: 0;
  transform: translate(-50%, -50%);
  overflow: hidden;
  border-radius: 50%;
  width: 64px;
  height: 64px;
}
.mouse-highlight-click {
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0;
  transform: scale(0);
  border-radius: 50%;
  width: 100%;
  height: 100%;
  background: var(--lns-color-yellow);
  transition: transform 0.2s ease-out, opacity 0.2s ease-out;
  pointer-events: none;
}
.mouse-down .mouse-highlight-click {
  opacity: 0.5;
  transform: scale(1);
}
`,""]),e.exports=o},570097:e=>{"use strict";e.exports=function(o,t){return t||(t={}),o=o&&o.__esModule?o.default:o,typeof o!="string"?o:(/^['"].*['"]$/.test(o)&&(o=o.slice(1,-1)),t.hash&&(o+=t.hash),/["'() \t\n]/.test(o)||t.needQuotes?'"'.concat(o.replace(/"/g,'\\"').replace(/\n/g,"\\n"),'"'):o)}},423647:(e,o,t)=>{"use strict";var r=t(275271),a=t(230967),c=t(659207),u=t(760425),f=t(116629),i=t(587664),l=t(971137),O=t(345966),_=t(326890),C=t(873530),ye=t(359784);function N(n=ReactReduxContext){const d=n===ReactReduxContext?useDefaultReduxContext:createReduxContextHook(n);return function(){const{store:p}=d();return p}}const Ce=null;function Ne(n=ReactReduxContext){const d=n===ReactReduxContext?useDefaultStore:createStoreHook(n);return function(){return d().dispatch}}const Ie=null;var De=t(987045),Te=t(464332);(0,l.Fu)(u.useSyncExternalStoreWithSelector),(0,O.v)(c.useSyncExternalStore),(0,i.F)(f.m);var b=t(844589),P=t(282187),w=t.n(P),g=t(172298),F=t(510453);let R="renderer";const G=n=>{n&&(R=n)},E=(n="info",d)=>(m,p)=>{const S={};p&&Object.entries(p).forEach(([L,M])=>{S[L]=W(M)}),g.ipcRenderer.send(F.u,{logLevel:n,message:m,context:S,windowName:d})};function W(n){return typeof n!="object"?n:H(n)?{message:n.message,name:n.name}:JSON.parse(JSON.stringify(n))}function H(n){return typeof n.message=="string"&&typeof n.name=="string"}const I=E("info",R),Ue=E("warn",R),xe=E("error",R),j=E("debug",R),be=n=>({info:E("info",n),warn:E("warn",n),error:E("error",n),debug:E("debug",n)});var Pe=t(313942);const K="MOUSE_TRACKER:::START_TRACKING_MOUSE",B="MOUSE_TRACKER:::STOP_TRACKING_MOUSE",k="MOUSE_TRACKER:::MOUSE_EVENT_CHANNEL";function V(){const[n,d]=(0,r.useState)(null);return(0,r.useEffect)(()=>{function m(p){d(p)}return I("Starting mouse tracking"),g.ipcRenderer.send(K),g.ipcRenderer.on(k,(p,S)=>{m(S)}),()=>{I("Stopping mouse tracking"),g.ipcRenderer.send(B)}},[]),n}var v=(n=>(n.MOVE="move",n.DOWN="down",n.UP="up",n.DRAG="drag",n))(v||{});function we(){return useSelector(n=>n.recorder.isRecording)}function Fe(){return useSelector(n=>n.recorder.paused)}function Ge(){return useSelector(n=>n.recorder.recordingMode)}function We(){return useSelector(n=>n.recorder.recording_type)}function He(){return useSelector(n=>n.recorder.startingRecording)}function Z(){return(0,l.v9)(n=>n.recorder.display)}function je(){return useSelector(n=>n.recorder.allDisplays)}function Ke(){return useSelector(n=>n.recorder.waiting_on_install)}function Be(){return useSelector(n=>n.recorder.videoDevices)}function Y(){return useSelector(n=>n.recorder.currentVideoDevice)}function ke(){return useSelector(n=>n.recorder.alerts)}function Ve(){return useSelector(n=>n.recorder.audioDevices)}function z(){return useSelector(n=>n.recorder.currentAudioDevice)}function Ze(){return useSelector(n=>n.recorder.windows)}function Ye(){return useSelector(n=>n.recorder.gettingWindows)}function ze(){return useSelector(n=>n.recorder.selectedWindowId)}function Je(){return z()===null}function Xe(){return Y()===null}function Qe(){return useSelector(n=>n.recorder.session?n.recorder.session.id:null)}function $e(){return useSelector(n=>n.recorder.recorderPromptState)}let D=0;const J=()=>{var n;(0,r.useEffect)(()=>{j("mouseHighlight: window loaded")},[]);const d=V(),m=(n=Z())==null?void 0:n.id,[p,S]=(0,r.useState)(!1);(0,r.useEffect)(()=>{const M=d?.type==v.DOWN&&d?.display===m;d?.type==v.UP?(clearTimeout(D),D=setTimeout(()=>{S(!1)},200)):M&&S(!0)},[d,m]);const L={left:d?.x,top:d?.y};return r.createElement("div",{className:w()("mouse-highlight-circle",p&&"mouse-down"),style:L},r.createElement("div",{className:"mouse-highlight-click"}))};var X=t(879741);function Q(){X.v9||(g.webFrame.setZoomFactor(1),g.webFrame.setVisualZoomLevelLimits(1,1))}const $="Loom Analytics Worker",q="Loom Camera",ee="Loom Canvas",te="Loom Confetti",ne="Loom Control Menu",oe="Loom Countdown",re="Loom Cropping",se="Loom Disk Critical",qe="Loom Audio Anomaly",ie="Loom Drawing Overlay",ce="Loom Not Authorized",ae="Loom OAuth",ue="Loom Preferences",le="Loom Recorder",de="Loom Recorder Settings",fe="Loom Screenshot",Oe="Welcome to Loom Desktop \u{1F389}",pe="System Audio Driver Installation",Ee="Loom Window Selector",T="Mouse Highlight Overlay",me="Loom Software Update",Se="Updating Loom",ge="Loom: Recording a Zoom Meeting",et="Loom: Meeting Recording Notes",tt="Loom: Meeting Recording Index",nt="Loom: Meeting Notification",ot="Loom: Contextual Onboarding",rt="Loom: Feature Nudge",Re="Cancel Recording",he="Restart Recording",_e="Screenshot Failed",st="Cancel Meeting Recording",it="Loom: Meeting Recording More Options",ct=[$,q,ee,te,ne,oe,re,ie,ae,se,ce,ue,le,de,fe,Oe,pe,Ee,T,me,Se,ge,Re,he,_e],at=null;var ve=t(110720),Le=t(239222);(0,ve.jC)(),G("mouse"),Q();const U=document.createElement("div"),x="container";U.id=x,document.body.appendChild(U),document.title=T;const Me=document.getElementById(x),Ae=b.S(Le.Q,[]);(n=>(0,a.render)(r.createElement(_.Z,{store:Ae},r.createElement(n,null)),Me))(J)},257728:(e,o,t)=>{"use strict";t.d(o,{O_:()=>f,Ji:()=>i,U6:()=>l});var r=t(450630),a=t(284558),c=(O=>(O.MEETING_NOTES="meeting-notes",O))(c||{});const u={["meeting-notes"]:a._v},f={nudge:{fadeIn:{seconds:.15,milliseconds:150},fadeOut:{seconds:.15,milliseconds:150}},contextualOnboarding:{fadeIn:{seconds:.4,milliseconds:400},fadeOut:{seconds:.4,milliseconds:400}}},i=r.F4`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`,l=r.F4`
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
`},313942:(e,o,t)=>{var r=t(533400);typeof r=="string"&&(r=[[e.id,r,""]]);var a,c,u={hmr:!0};u.transform=a,u.insertInto=void 0;var f=t(739255)(r,u);r.locals&&(e.exports=r.locals)},969975:(e,o,t)=>{"use strict";e.exports=t.p+"assets/fonts/AtlassianSans-latin.woff2"},439491:e=>{"use strict";e.exports=require("assert")},706113:e=>{"use strict";e.exports=require("crypto")},172298:e=>{"use strict";e.exports=require("electron")},582361:e=>{"use strict";e.exports=require("events")},657147:e=>{"use strict";e.exports=require("fs")},113685:e=>{"use strict";e.exports=require("http")},795687:e=>{"use strict";e.exports=require("https")},822037:e=>{"use strict";e.exports=require("os")},371017:e=>{"use strict";e.exports=require("path")},863477:e=>{"use strict";e.exports=require("querystring")},257310:e=>{"use strict";e.exports=require("url")},473837:e=>{"use strict";e.exports=require("util")},282187:(e,o)=>{var t,r;/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/(function(){"use strict";var a={}.hasOwnProperty;function c(){for(var i="",l=0;l<arguments.length;l++){var O=arguments[l];O&&(i=f(i,u(O)))}return i}function u(i){if(typeof i=="string"||typeof i=="number")return i;if(typeof i!="object")return"";if(Array.isArray(i))return c.apply(null,i);if(i.toString!==Object.prototype.toString&&!i.toString.toString().includes("[native code]"))return i.toString();var l="";for(var O in i)a.call(i,O)&&i[O]&&(l=f(l,O));return l}function f(i,l){return l?i?i+" "+l:i+l:i}e.exports?(c.default=c,e.exports=c):(t=[],r=function(){return c}.apply(o,t),r!==void 0&&(e.exports=r))})()}},h={};function s(e){var o=h[e];if(o!==void 0)return o.exports;var t=h[e]={id:e,loaded:!1,exports:{}};return A[e].call(t.exports,t,t.exports,s),t.loaded=!0,t.exports}s.m=A,s.c=h,(()=>{var e=[];s.O=(o,t,r,a)=>{if(t){a=a||0;for(var c=e.length;c>0&&e[c-1][2]>a;c--)e[c]=e[c-1];e[c]=[t,r,a];return}for(var u=1/0,c=0;c<e.length;c++){for(var[t,r,a]=e[c],f=!0,i=0;i<t.length;i++)(a&!1||u>=a)&&Object.keys(s.O).every(N=>s.O[N](t[i]))?t.splice(i--,1):(f=!1,a<u&&(u=a));if(f){e.splice(c--,1);var l=r();l!==void 0&&(o=l)}}return o}})(),s.n=e=>{var o=e&&e.__esModule?()=>e.default:()=>e;return s.d(o,{a:o}),o},(()=>{var e=Object.getPrototypeOf?t=>Object.getPrototypeOf(t):t=>t.__proto__,o;s.t=function(t,r){if(r&1&&(t=this(t)),r&8||typeof t=="object"&&t&&(r&4&&t.__esModule||r&16&&typeof t.then=="function"))return t;var a=Object.create(null);s.r(a);var c={};o=o||[null,e({}),e([]),e(e)];for(var u=r&2&&t;typeof u=="object"&&!~o.indexOf(u);u=e(u))Object.getOwnPropertyNames(u).forEach(f=>c[f]=()=>t[f]);return c.default=()=>t,s.d(a,c),a}})(),s.d=(e,o)=>{for(var t in o)s.o(o,t)&&!s.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:o[t]})},s.h=()=>"55e5c6a40d444554bfb1",s.hmd=e=>(e=Object.create(e),e.children||(e.children=[]),Object.defineProperty(e,"exports",{enumerable:!0,set:()=>{throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+e.id)}}),e),s.o=(e,o)=>Object.prototype.hasOwnProperty.call(e,o),s.r=e=>{typeof Symbol<"u"&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.nmd=e=>(e.paths=[],e.children||(e.children=[]),e),s.p="./",(()=>{var e={9085:0};s.O.j=r=>e[r]===0;var o=(r,a)=>{var[c,u,f]=a,i,l,O=0;if(c.some(C=>e[C]!==0)){for(i in u)s.o(u,i)&&(s.m[i]=u[i]);if(f)var _=f(s)}for(r&&r(a);O<c.length;O++)l=c[O],s.o(e,l)&&e[l]&&e[l][0](),e[c[O]]=0;return s.O(_)},t=global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[];t.forEach(o.bind(null,0)),t.push=o.bind(null,t.push.bind(t))})(),s.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,947,3780,6599,1404,3655,816,3322,4162,6429],()=>s(s.s=903679)),s.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,947,3780,6599,1404,3655,816,3322,4162,6429],()=>s(s.s=423647)),s.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,947,3780,6599,1404,3655,816,3322,4162,6429],()=>s(s.s=639542));var y=s.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,947,3780,6599,1404,3655,816,3322,4162,6429],()=>s(s.s=194383));y=s.O(y)})();

//# sourceMappingURL=mouse_highlight_overlay.js.map