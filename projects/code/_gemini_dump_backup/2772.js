(global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[]).push([[2772],{199384:(D,y,t)=>{"use strict";t.d(y,{x:()=>h});var r=t(275271),u=t(450630);const h=()=>r.createElement(u.xB,{styles:u.iv`
      html,
      body {
        user-select: none;
        margin: 0;
        padding: 0;
        // Needed to prevent scrollbars from appearing
        overflow: hidden;
        width: 100%;
        height: 100%;
      }
    `})},194383:(D,y,t)=>{"use strict";var r=t(183780);const u=document.createElement("style");u.innerHTML=(0,r.Ut4)()+`:root {
    --lns-color-red: #C9372C;
    --lns-color-offWhite: #F8F8F8;
    --lns-color-blueLight: #CFE1FD;
    --lns-color-blue: #1868DB;
    --lns-color-blueDark: #123263;
    --lns-color-orangeLight: #FFD5D2;
    --lns-color-orangeDark: #D72700;
    --lns-color-tealLight: #BAF3DB;
    --lns-color-teal: #1F845A;
    --lns-color-tealDark: #164B35;
    --lns-color-yellowLight: #FCE4A6;
    --lns-color-yellow: #FBC828;
    --lns-color-yellowDark: #FCA700;

    --lns-color-blurpleLight: #E9F2FE;
    --lns-color-blurpleMedium: #CFE1FD;
    --lns-color-blurple: #1868DB;
    --lns-color-blurpleDark: #1558BC;
    --lns-color-blurpleStrong: #123263;

    --lns-color-grey1: #F8F8F8;
    --lns-color-grey2: #F0F1F2;
    --lns-color-grey3: #DDDEE1;
    --lns-color-grey4: #B7B9BE;
    --lns-color-grey5: #8C8F97;
    --lns-color-grey6: #6B6E76;
    --lns-color-grey7: #3B3D42;
    --lns-color-grey8: #292A2E;

    --lns-color-primary: #1868DB;
    --lns-color-primaryHover: #1558BC;
    --lns-color-primaryActive: #123263;
    --lns-color-backdropDark: #292A2EE5;
    --lns-color-backdropTwilight: hsla(216, 69%, 23%, 0.8);
    --lns-color-highlight: hsla(215, 80%, 48%, 0.15);
    --lns-color-focusRing: #4688EC;

    --ds-text: #292A2E;
    --ds-text-subtlest: #6B6E76;
    --ds-text-disabled: #080F2147;
    --ds-text-inverse: #FFFFFF;
    --ds-background-information-bold: #1868DB;
    --ds-background-accent-green-bolder: #1F845A;
    --ds-background-accent-orange: #FF623E;
    --ds-background-accent-orange-hovered: var(--lns-color-orangeDark);
    --ds-background-warning-bold: #FBC828;
    --ds-background-danger-bold: #C9372C;
    --ds-background-danger-bold-hovered: #AE2E24;
    --ds-background-danger-bold-pressed: #5D1F1A;
    --ds-background-discovery: #F8EEFE;
    --ds-background-discovery-hovered: #EED7FC;
    --ds-background-discovery-pressed: #D8A0F7;
    --ds-surface: #FFFFFF;
    --ds-background-neutral-subtle-hovered: #0515240F;
    --ds-background-neutral-subtle-pressed: #0B122824;
    --ds-surface-sunken: #F8F8F8;
    --ds-background-disabled: #17171708;
    --ds-background-neutral-bold: #292A2E;
    --ds-surface-overlay: #FFFFFF;
    --ds-background-input: #FFFFFF;
    --ds-background-neutral: #0515240F;
    --ds-background-discovery-bold: #964AC0;
    --ds-blanket: #050C1F75;
    --ds-border: #0B122824;
    --ds-border-input: #8C8F97;

    --lns-themeLight-color-body: var(--ds-text);
    --lns-themeLight-color-bodyDimmed: var(--ds-text-subtlest);
    --lns-themeLight-color-disabledContent: var(--ds-text-disabled);
    --lns-themeLight-color-discoveryTitle: var(--ds-text);
    --lns-themeLight-color-bodyInverse: var(--ds-text-inverse);
    --lns-themeLight-color-info: var(--ds-background-information-bold);
    --lns-themeLight-color-success: var(--ds-background-accent-green-bolder);
    --lns-themeLight-color-warning: var(--ds-background-warning-bold);
    --lns-themeLight-color-danger: var(--ds-background-danger-bold);
    --lns-themeLight-color-dangerHover: var(--ds-background-danger-bold-hovered);
    --lns-themeLight-color-dangerActive: var(--ds-background-danger-bold-pressed);
    --lns-themeLight-color-upgrade: var(--ds-background-discovery);
    --lns-themeLight-color-upgradeHover: var(--ds-background-discovery-hovered);
    --lns-themeLight-color-upgradeActive: var(--ds-background-discovery-pressed);
    --lns-themeLight-color-background: var(--ds-surface);
    --lns-themeLight-color-backgroundHover: var(--ds-background-neutral-subtle-hovered);
    --lns-themeLight-color-backgroundActive: var(--ds-background-neutral-subtle-pressed);
    --lns-themeLight-color-backgroundSecondary: var(--ds-surface-sunken);
    --lns-themeLight-color-backgroundSecondary2: var(--ds-surface-sunken);
    --lns-themeLight-color-disabledBackground: var(--ds-background-disabled);
    --lns-themeLight-color-backgroundInverse: var(--ds-background-neutral-bold);
    --lns-themeLight-color-overlay: var(--ds-surface-overlay);
    --lns-themeLight-color-formFieldBackground: var(--ds-background-input);
    --lns-themeLight-color-tabBackground: var(--ds-background-neutral);
    --lns-themeLight-color-discoveryBackground: var(--ds-background-discovery-bold);
    --lns-themeLight-color-discoveryLightBackground: var(--ds-background-discovery);
    --lns-themeLight-color-backdrop: var(--ds-blanket);
    --lns-themeLight-color-discoveryHighlight: var(--ds-background-discovery);
    --lns-themeLight-color-border: var(--ds-border);
    --lns-themeLight-color-formFieldBorder: var(--ds-border-input);
    --lns-themeLight-color-buttonBorder: var(--ds-border);
    --lns-themeLight-color-interactiveRecord: var(--ds-background-accent-orange);

  }
`,document.head.appendChild(u)},974144:(D,y,t)=>{var r=Object.defineProperty,u=Object.getOwnPropertySymbols,h=Object.prototype.hasOwnProperty,p=Object.prototype.propertyIsEnumerable,O=(n,i,E)=>i in n?r(n,i,{enumerable:!0,configurable:!0,writable:!0,value:E}):n[i]=E,A=(n,i)=>{for(var E in i||(i={}))h.call(i,E)&&O(n,E,i[E]);if(u)for(var E of u(i))p.call(i,E)&&O(n,E,i[E]);return n};const g=t(172298),S=t(371017),T="electron"in process.versions,o=process&&process.type==="renderer",c={is:{renderer:o,main:!o,get development(){return o?g.ipcRenderer.sendSync("electron-is-dev"):v()},usingAsar:T&&process.mainModule&&process.mainModule.filename.includes("app.asar")}},a=A(A({},c.is),o?P():b());function l(n){return a.usingAsar?S.join(process.resourcesPath,n):n}function _(){if(!a.main)return;const n=t(657147),i=t(371017),E=t(172298).app,C=i.join(E.getPath("userData"),".electron-util--has-app-launched");if(n.existsSync(C))return!1;try{n.writeFileSync(C,"")}catch(N){if(N.code==="ENOENT")return n.mkdirSync(E.getPath("userData")),_()}return!0}function I(n){n||g.ipcMain.on("electron-is-dev",i=>{i.returnValue=v()})}function b(){const n=process.platform;return{windows:n==="win32",macos:n==="darwin"}}function P(){const n=window.navigator.platform;return{windows:n.match(/win32/i),macos:n.match(/Mac/i)}}function v(){const n="ELECTRON_IS_DEV"in process.env,i=Number.parseInt(process.env.ELECTRON_IS_DEV,10)===1;return n?i:!g.app.isPackaged}I(o),D.exports={is:a,fixPathForAsarUnpack:l,isFirstAppLaunch:_}},110720:(D,y,t)=>{"use strict";t.d(y,{jC:()=>E});var r=t(974144),u=t.n(r),h=t(78672),p=t(804951),O=t.n(p),A=t(879741),g=t(212849),S=t(206687),T=t(355617),o=t(25334),c=Object.defineProperty,a=Object.getOwnPropertySymbols,l=Object.prototype.hasOwnProperty,_=Object.prototype.propertyIsEnumerable,I=(s,d,R)=>d in s?c(s,d,{enumerable:!0,configurable:!0,writable:!0,value:R}):s[d]=R,b=(s,d)=>{for(var R in d||(d={}))l.call(d,R)&&I(s,R,d[R]);if(a)for(var R of a(d))_.call(d,R)&&I(s,R,d[R]);return s};const P=["ERR_NETWORK_IO_SUSPENDED","ERR_NAME_NOT_RESOLVED","ERR_INTERNET_DISCONNECTED","ERR_NETWORK_CHANGED","ERR_CONNECTION_RESET"],v=.25;let n;const i=s=>{n=s},E=s=>{const d=t(952126),f=`${A.ar?g.Zb:g.zl}@${T.m.version}`,M=r.is.macos?g.Sd:g.HV;d.init(b({dsn:g.KL,environment:A.Gv,debug:!0,release:`${f}-${M}`,enableUnresponsive:!1,autoSessionTracking:!0,attachStacktrace:!0,sampleRate:v,ignoreErrors:P,beforeSend(U){return(0,o.b5)(U)}},s)),n=d},C=s=>{n.configureScope(d=>{d.setUser({id:s})})},N=()=>{const s=[recorderActions.SET_RECORDING_TIME_ELAPSED];return SentryReact.createReduxEnhancer({actionTransformer:R=>s.includes(R.type)?null:{type:R.type},stateTransformer:()=>null})},F=s=>{n.captureException(s)},L=(s,...d)=>{log.error("logException",s,...d),F(s)},k=(s,d,R)=>{if(d instanceof Error){const f=`${s}: ${d.message}`;log.error(f),n.captureMessage(f,"error",{originalException:d})}else log.error(s),n.captureMessage(s,"error")},w=s=>{n.captureMessage(s)},W=s=>{n.addBreadcrumb(s)}},212849:D=>{D.exports.KL="https://c67368549d804bc989bba1b3cb1a0471@o398470.ingest.sentry.io/5599205",D.exports.Sd="mac",D.exports.HV="win",D.exports.Zb="LoomStaging",D.exports.zl="Loom"},474176:(D,y,t)=>{"use strict";t.d(y,{u:()=>p});var r=t(172298),u=t.n(r),h=t(879741);function p(){h.v9||(r.webFrame.setZoomFactor(1),r.webFrame.setVisualZoomLevelLimits(1,1))}},355617:(D,y,t)=>{"use strict";t.d(y,{m:()=>u});const r="0.330.1",u=h();function h(){return{version:r,appArch:process.arch}}},879741:(D,y,t)=>{"use strict";t.d(y,{Gv:()=>p,v9:()=>a,ar:()=>_});var r=t(974144),u=t.n(r);const h="Loom",p="production",O="development",A="production",g="staging",S="desktop",T=p===O,o=p===A,c=p===g,a=p===O||r.is.development,l=p===A&&!r.is.development,_=p===g&&!r.is.development,I=p===A&&r.is.development,b="false"},206687:(D,y,t)=>{"use strict";var r=t(346972);const u="add-window-id-to-hide",h="select-video-recording-device",p="set-recording-file-path",O="start-recording-failure",A="start-recording-success",g="update-active-window-title",S="update-all-displays",T="update-recorder-prompt-state",o="update-current-recording-devices",c="update-crop-rect",a="update-current-display",l="update-has-selected-display",_="update-is-cropping",I="update-is-recording",b="update-mic-on",P="update-recording-devices",v="update-recording-type",n="update-recording-type-selection",i="reset-recording-state",E="update-selected-window",C="clear-selected-window",N="update-msg-type-status",F="update-session",L="update-show-selector-window",k="update-starting-recording",w="update-stopping-recording",W="update-windows",s="show-muted-mic-warn",d="hide-muted-mic-warn",R="set-recording-time-elapsed",f="update-internal-audio-status",M="update-waiting-on-install",U="set-start-recording-request-time-ms",B="set-recording-mode",X="set-recording-alert",q="reset-recording-alert",ee="reset-all-recording-alerts",G="cancel-recording",x="restart-recording",H="error-recording",V="get-display-screenshots",K="get-windows",z="select-audio-recording-device",Z="start-recording",ae="select-preferred-video-device",te="after-stop-recording",j="stop-recording",$="update-recording-paused",re="update-recording-cancelled",Y="get-internal-audio-status",J="install-system-audio",de=e=>({type:T,payload:{state:e}}),le=e=>({type:u,payload:{candidate:e}}),ie=e=>({type:U,payload:{timestampMs:e}}),ue=e=>({type:R,payload:{recordingTimeElapsed:e}}),pe=()=>({type:s,payload:{}}),_e=(0,r.eH)(z,e=>({type:z})),Ee=e=>({type:h,payload:{device:e}}),ge=({audioDevice:e,videoDevice:m,selectedAudioDevices:Q,selectedVideoDevices:se,updateStore:ce=!0})=>({type:o,payload:{audioDevice:e,videoDevice:m,selectedAudioDevices:Q,selectedVideoDevices:se,updateStore:ce}}),Re=({audioDevices:e,videoDevices:m})=>({type:P,payload:{audioDevices:e,videoDevices:m}}),De=e=>({type:v,payload:{recordingType:e}}),ye=e=>({type:n,payload:{recordingType:e}}),he=e=>({type:p,payload:{path:e}}),Ae=e=>({type:g,payload:{title:e}}),me=(e,m=!1)=>({type:S,payload:{displays:e},meta:{updatingWithScreenshots:m}}),Te=(e=!1)=>({type:L,payload:{show:e}}),Oe=(e=[])=>({type:W,payload:{windows:e}}),oe=(e=null)=>({type:c,payload:{cropRect:e}}),Se=e=>({type:F,payload:{session:e}}),Ie=e=>({type:l,payload:{selected:e}}),be=e=>({type:_,payload:{isCropping:e}}),ve=e=>({type:I,payload:{isRecording:e}}),fe=e=>({type:k,payload:{starting:e}}),Pe=e=>({type:w,payload:{stopping:e}}),Ce=e=>({type:re,payload:{cancelSource:e}}),Le=e=>({type:b,payload:{on:e}}),Ne=()=>({type:i}),Fe=()=>({type:C}),Me=(0,r.eH)(E,(e,m=!1)=>({type:E})),Ue=()=>e=>{e(oe(null)),e(ne())},ke=(0,r.eH)(G,(e=!1,m)=>({type:G})),we=(0,r.eH)(x,(e=!1)=>({type:x})),We=(0,r.eH)(H,(e="unknown recording error")=>({type:H})),Be=(0,r.eH)(K,(e=!0)=>({type:K})),Ge=(0,r.eH)(a,(e,m=!1)=>({type:a})),ne=(0,r.eH)(Z,(e=!1,m=!1)=>({type:Z})),xe=(0,r.eH)($,e=>({type:$})),He=(0,r.eH)(j,e=>({type:j})),Ve=(0,r.eH)(te,(e,m,Q)=>({type:"after-recorder-stopped"})),Ke=(0,r.eH)(L,(e=!0)=>({type:L})),ze=(0,r.eH)(V,()=>({type:V})),Ze=e=>({type:f,payload:{installed:e}}),je=e=>({type:M,payload:{waiting_on_install:e}}),$e=(0,r.eH)(Y,e=>({type:Y})),Ye=(0,r.eH)(J,(e=!1)=>({type:J})),Je=({recordingMode:e,storeValue:m=!0})=>({type:B,payload:{recordingMode:e,storeValue:m}}),Qe=e=>({type:q,payload:{alert:e}}),Xe=()=>({type:ee}),qe=e=>({type:X,payload:{alert:e}})},212612:(D,y,t)=>{"use strict";t.d(y,{A:()=>r});function r(u){requestAnimationFrame(()=>{requestAnimationFrame(u)})}},25334:(D,y,t)=>{"use strict";t.d(y,{b5:()=>T});const r=["path","email","password","filePath","fileName","currentFile","file","recordingPath","videoPath","dirPath","normalPath","host","hostname","name"],u=[/\/Users\/[^/\s]+/g,/\b[Uu]sers?\/[^/\s]+/g,/[A-Z]:\\Users\\[^\\\s]+/gi],h=[/\beyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\b/g,/\b[a-zA-Z0-9-_]{40,}\b/g,/\b(api[_-]?key|token|secret|password|auth)[_-]?[a-zA-Z0-9]{20,}\b/gi,/\bbearer\s+[a-zA-Z0-9-_]{20,}\b/gi],p=[/(https?:\/\/[^/]+\/[^/]*\/)[a-f0-9]{33,}/g],O=[/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,/\b(?:\d{1,3}\.){3}\d{1,3}\b/g,/\b(user[_-]?id|session[_-]?id|device[_-]?id)\s*[:=]\s*[a-zA-Z0-9-_]{10,}\b/gi],A=o=>{try{if(typeof o!="string")return"";let c=o;return r.forEach(a=>{c=c.replace(new RegExp(`"${a}":"[^"]*"[,]?`,"g"),"")}),u.forEach(a=>{c=c.replace(a,l=>{if(l.startsWith("/Users/"))return"/Users/redacted";if(/^[A-Z]:\\Users\\/i.test(l))return l.replace(/^([A-Z]:\\Users\\)[^\\\s]+/i,"$1redacted");const _=l.split("/");return _.length>=2?_[0]+"/redacted":l})}),O.forEach(a=>{c=c.replace(a,"")}),h.forEach(a=>{c=c.replace(a,"")}),p.forEach(a=>{c=c.replace(a,"$1")}),c}catch{return console.error("Error in sanitizeLogMessage"),""}},g=o=>typeof o=="string"?A(o):Array.isArray(o)?o.map(c=>g(c)):typeof o=="object"&&o!==null?S(o):o,S=o=>{if(o==null)return o;const c={};return Object.entries(o).forEach(([a,l])=>{c[a]=g(l)}),c},T=(o,c=new Set)=>{if(!o||typeof o!="object")return o;if(c.has(o))return"Cyclical Reference";if(c.add(o),Array.isArray(o))return o.map(l=>T(l,c));const a={};return Object.entries(o).forEach(([l,_])=>{r.includes(l)||(typeof _=="string"?a[l]=A(_):typeof _=="object"&&_!==null?a[l]=T(_,c):a[l]=_)}),a}}}]);

//# sourceMappingURL=2772.js.map