(global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[]).push([[915],{688969:(u,g,t)=>{var o=t(744917),d=t(570097),f=t(969975);g=o(!1);var a=d(f);g.push([u.id,`@font-face {
  font-weight: 400 653;
  font-style: normal;
  font-family: 'Atlassian Sans';
  src: url(`+a+`) format('woff2');
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
.tag-input-container {
  position: relative;
  align-items: center;
  flex-direction: row;
  flex-shrink: 0;
  justify-content: space-between;
  display: flex;
  overflow: hidden;
  border: 1px solid var(--lns-color-grey3);
  border-radius: var(--lns-radius-medium);
  width: 140px;
  height: 36px;
  padding: 0 0.5rem;
}
.tags-container,
.tag-input {
  height: 100%;
}
.tags-container {
  align-items: center;
  flex-direction: row;
  flex-shrink: 0;
  justify-content: flex-start;
  display: flex;
  cursor: text;
}
.tag-input-tag {
  margin-left: 4px;
  border: 1px solid var(--lns-color-grey5);
  border-radius: 4px;
  height: 16px;
  padding-right: 4px;
  padding-left: 4px;
  background-color: var(--lns-color-grey1);
  font-size: 10px;
  line-height: 16px;
  font-weight: 500;
  color: var(--lns-color-grey7);
  text-align: center;
}
.tag-input-tag:first-child {
  margin-left: 0;
}
.tags-container-empty {
  background: var(--lns-color-grey1);
}
.tags-container-empty:before {
  content: 'Type shortcut';
  font-size: 12px;
  line-height: 18px;
  font-weight: 400;
  font-family: 'Atlassian Sans', ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, system-ui, "Helvetica Neue", sans-serif;
  position: absolute;
  padding: 0 0.5rem;
  pointer-events: none;
}
.tags-container-empty .backspace-button {
  display: none;
}
.tag-input {
  position: absolute;
  left: 0;
  opacity: 0.5;
  box-shadow: none;
  border: none;
  width: 75%;
  padding-left: 0.5rem;
  background-color: transparent;
  background-image: none;
  font-size: 18px;
  line-height: 32px;
  font-weight: 500;
  color: var(--lns-color-grey7);
}
.tag-input:focus {
  outline: none;
}
.backspace-button {
  cursor: pointer;
}
`,""]),u.exports=g},974144:(u,g,t)=>{var o=Object.defineProperty,d=Object.getOwnPropertySymbols,f=Object.prototype.hasOwnProperty,a=Object.prototype.propertyIsEnumerable,y=(n,_,m)=>_ in n?o(n,_,{enumerable:!0,configurable:!0,writable:!0,value:m}):n[_]=m,E=(n,_)=>{for(var m in _||(_={}))f.call(_,m)&&y(n,m,_[m]);if(d)for(var m of d(_))a.call(_,m)&&y(n,m,_[m]);return n};const c=t(172298),S=t(371017),P="electron"in process.versions,e=process&&process.type==="renderer",s={is:{renderer:e,main:!e,get development(){return e?c.ipcRenderer.sendSync("electron-is-dev"):U()},usingAsar:P&&process.mainModule&&process.mainModule.filename.includes("app.asar")}},i=E(E({},s.is),e?C():A());function p(n){return i.usingAsar?S.join(process.resourcesPath,n):n}function O(){if(!i.main)return;const n=t(657147),_=t(371017),m=t(172298).app,D=_.join(m.getPath("userData"),".electron-util--has-app-launched");if(n.existsSync(D))return!1;try{n.writeFileSync(D,"")}catch(w){if(w.code==="ENOENT")return n.mkdirSync(m.getPath("userData")),O()}return!0}function R(n){n||c.ipcMain.on("electron-is-dev",_=>{_.returnValue=U()})}function A(){const n=process.platform;return{windows:n==="win32",macos:n==="darwin"}}function C(){const n=window.navigator.platform;return{windows:n.match(/win32/i),macos:n.match(/Mac/i)}}function U(){const n="ELECTRON_IS_DEV"in process.env,_=Number.parseInt(process.env.ELECTRON_IS_DEV,10)===1;return n?_:!c.app.isPackaged}R(e),u.exports={is:i,fixPathForAsarUnpack:p,isFirstAppLaunch:O}},110720:(u,g,t)=>{"use strict";t.d(g,{jC:()=>m,cX:()=>w});var o=t(974144),d=t.n(o),f=t(78672),a=t(804951),y=t.n(a),E=t(879741),c=t(212849),S=t(206687),P=t(355617),e=t(25334),s=Object.defineProperty,i=Object.getOwnPropertySymbols,p=Object.prototype.hasOwnProperty,O=Object.prototype.propertyIsEnumerable,R=(r,l,h)=>l in r?s(r,l,{enumerable:!0,configurable:!0,writable:!0,value:h}):r[l]=h,A=(r,l)=>{for(var h in l||(l={}))p.call(l,h)&&R(r,h,l[h]);if(i)for(var h of i(l))O.call(l,h)&&R(r,h,l[h]);return r};const C=["ERR_NETWORK_IO_SUSPENDED","ERR_NAME_NOT_RESOLVED","ERR_INTERNET_DISCONNECTED","ERR_NETWORK_CHANGED","ERR_CONNECTION_RESET"],U=.25;let n;const _=r=>{n=r},m=r=>{const l=t(952126),T=`${E.ar?c.Zb:c.zl}@${P.m.version}`,N=o.is.macos?c.Sd:c.HV;l.init(A({dsn:c.KL,environment:E.Gv,debug:!0,release:`${T}-${N}`,enableUnresponsive:!1,autoSessionTracking:!0,attachStacktrace:!0,sampleRate:U,ignoreErrors:C,beforeSend(M){return(0,e.b5)(M)}},r)),n=l},D=r=>{n.configureScope(l=>{l.setUser({id:r})})},w=()=>{const r=[S.$G];return f.wS({actionTransformer:h=>r.includes(h.type)?null:{type:h.type},stateTransformer:()=>null})},b=r=>{n.captureException(r)},x=(r,...l)=>{log.error("logException",r,...l),b(r)},I=(r,l,h)=>{if(l instanceof Error){const T=`${r}: ${l.message}`;log.error(T),n.captureMessage(T,"error",{originalException:l})}else log.error(r),n.captureMessage(r,"error")},v=r=>{n.captureMessage(r)},L=r=>{n.addBreadcrumb(r)}},212849:u=>{u.exports.KL="https://c67368549d804bc989bba1b3cb1a0471@o398470.ingest.sentry.io/5599205",u.exports.Sd="mac",u.exports.HV="win",u.exports.Zb="LoomStaging",u.exports.zl="Loom"},987771:(u,g,t)=>{"use strict";t.d(g,{h:()=>o});let o;function d(a){o=a}function f(a){return new Promise(y=>{const E=o.getState();if(a(E)){y(E);return}const c=o.subscribe(()=>{const S=o.getState();a(S)&&(c(),y(S))})})}},955649:(u,g,t)=>{"use strict";t.d(g,{MC:()=>o,FZ:()=>d,W5:()=>f,XB:()=>a,iC:()=>y,RG:()=>c,si:()=>S,ip:()=>P});const o="enter-drawing-mode",d="exit-drawing-mode",f="show-drawing-tools",a="update-control-menu-placement",y="set-control-menu-size",E="update-control-menu-size",c="update-control-menu-position",S="update-control-menu-id",P="update-current-size",e=n=>({type:S,payload:{windowId:n}}),s=n=>({type:P,payload:{size:n}}),i=({width:n,height:_,sizeType:m})=>({type:y,payload:{width:n,height:_,sizeType:m}}),p=n=>({type:E,payload:{sizeType:n}}),O=()=>({type:o}),R=()=>({type:d}),A=()=>({type:f,payload:{at:Date.now()}}),C=n=>({type:a,payload:{placement:n}}),U=(n,_)=>({type:c,payload:{x:n,y:_}})},599682:(u,g,t)=>{"use strict";t.d(g,{HB:()=>o,_4:()=>d,G_:()=>f,mi:()=>a,AH:()=>y,Fx:()=>E});const o="update-countdown-state",d="reset-countdown",f="set-countdown-for-start",a="skip-countdown",y="update-countdown",E="toggle-countdown-pause",c=p=>({type:o,payload:{visibilityState:p}}),S=()=>({type:a}),P=()=>({type:d}),e=p=>({type:y,payload:{countdown:p}}),s=()=>({type:f}),i=()=>({type:E})},621678:(u,g,t)=>{"use strict";t.d(g,{JW:()=>f,p2:()=>a,NR:()=>y});var o=t(346972);const d="push-back-overlay",f="cropping-window-ready",a="cropping-window-close",y="exit-cropping",E="first-crop",c=()=>({type:f}),S=()=>({type:a}),P=(0,o.eH)(d,()=>({type:d})),e=()=>({type:y}),s=()=>({type:E})},858470:(u,g,t)=>{"use strict";t.d(g,{Aw:()=>o,M4:()=>d,dZ:()=>f});const o="drawing-line-start",d="update-brush-size",f="update-drawing-color",a=c=>({type:f,payload:{color:c}}),y=c=>({type:d,payload:{size:c}}),E=()=>({type:o})},25334:(u,g,t)=>{"use strict";t.d(g,{PV:()=>E,zF:()=>S,b5:()=>P});const o=["path","email","password","filePath","fileName","currentFile","file","recordingPath","videoPath","dirPath","normalPath","host","hostname","name"],d=[/\/Users\/[^/\s]+/g,/\b[Uu]sers?\/[^/\s]+/g,/[A-Z]:\\Users\\[^\\\s]+/gi],f=[/\beyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\b/g,/\b[a-zA-Z0-9-_]{40,}\b/g,/\b(api[_-]?key|token|secret|password|auth)[_-]?[a-zA-Z0-9]{20,}\b/gi,/\bbearer\s+[a-zA-Z0-9-_]{20,}\b/gi],a=[/(https?:\/\/[^/]+\/[^/]*\/)[a-f0-9]{33,}/g],y=[/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,/\b(?:\d{1,3}\.){3}\d{1,3}\b/g,/\b(user[_-]?id|session[_-]?id|device[_-]?id)\s*[:=]\s*[a-zA-Z0-9-_]{10,}\b/gi],E=e=>{try{if(typeof e!="string")return"";let s=e;return o.forEach(i=>{s=s.replace(new RegExp(`"${i}":"[^"]*"[,]?`,"g"),"")}),d.forEach(i=>{s=s.replace(i,p=>{if(p.startsWith("/Users/"))return"/Users/redacted";if(/^[A-Z]:\\Users\\/i.test(p))return p.replace(/^([A-Z]:\\Users\\)[^\\\s]+/i,"$1redacted");const O=p.split("/");return O.length>=2?O[0]+"/redacted":p})}),y.forEach(i=>{s=s.replace(i,"")}),f.forEach(i=>{s=s.replace(i,"")}),a.forEach(i=>{s=s.replace(i,"$1")}),s}catch{return console.error("Error in sanitizeLogMessage"),""}},c=e=>typeof e=="string"?E(e):Array.isArray(e)?e.map(s=>c(s)):typeof e=="object"&&e!==null?S(e):e,S=e=>{if(e==null)return e;const s={};return Object.entries(e).forEach(([i,p])=>{s[i]=c(p)}),s},P=(e,s=new Set)=>{if(!e||typeof e!="object")return e;if(s.has(e))return"Cyclical Reference";if(s.add(e),Array.isArray(e))return e.map(p=>P(p,s));const i={};return Object.entries(e).forEach(([p,O])=>{o.includes(p)||(typeof O=="string"?i[p]=E(O):typeof O=="object"&&O!==null?i[p]=P(O,s):i[p]=O)}),i}},955761:(u,g,t)=>{var o=t(688969);typeof o=="string"&&(o=[[u.id,o,""]]);var d,f,a={hmr:!0};a.transform=d,a.insertInto=void 0;var y=t(739255)(o,a);o.locals&&(u.exports=o.locals)},969975:(u,g,t)=>{"use strict";u.exports=t.p+"assets/fonts/AtlassianSans-latin.woff2"}}]);

//# sourceMappingURL=915.js.map