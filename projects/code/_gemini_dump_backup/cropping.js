(()=>{var Ze={694919:(n,c,o)=>{var e=o(744917),l=o(570097),s=o(969975);c=e(!1);var i=l(s);c.push([n.id,`@font-face {
  font-weight: 400 653;
  font-style: normal;
  font-family: 'Atlassian Sans';
  src: url(`+i+`) format('woff2');
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
`,""]),n.exports=c},255347:(n,c,o)=>{"use strict";var e=o(275271),l=o(230967),s=o(443934),i=o(844589),_=o(621678),p=o(206687),O=o(42022),E=o(992671),g=o(450630),w=o(394473),v=(t=>(t[t.Video=0]="Video",t[t.Screenshot=1]="Screenshot",t))(v||{}),I=o(183780),H=o(295579);const u="320px",L={[v.Video]:{title:"Custom size recording",description:"Drag to select an area."},[v.Screenshot]:{title:"Screenshot",description:"Drag to select an area or click to capture your full screen."}},z=E.Z.div`
  z-index: 3;
  box-shadow: var(--lns-shadow-medium);
  position: absolute;
  display: flex;
  flex-direction: column;
  left: calc(50% - ${u} / 2);
  top: calc(50% - ${u} / 2);
  background-color: var(--lns-color-body);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  width: ${u};
  overflow: hidden;

  ${t=>!t.show&&g.iv`
      display: none;
    `}
`,$=E.Z.div`
  padding: 20px;
  display: flex;
  padding-bottom: 35px;
  flex-direction: column;
  position: relative;
`,B=E.Z.div`
  background-color: var(--lns-color-blueDark);
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: auto;
`,Q=E.Z.div`
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
`,Y=(0,E.Z)(I.JO$)`
  color: white;
`,q=(0,E.Z)(I.xvT)`
  color: white;
  font-size: var(--lns-fontSize-body-md);
  font-weight: var(--lns-fontWeight-book);
`,de=E.Z.div`
  text-decoration: underline;

  font-size: var(--lns-fontSize-medium);
  font-weight: var(--lns-fontWeight-book);
  color: var(--lns-color-grey5);

  cursor: pointer;
`,Ae=(0,E.Z)(de)`
  position: absolute;
  color: white;
  padding: 12px 20px;
  bottom: 0;
  right: 0;
  margin: 0;
`;function le({isCropping:t,cropType:h,cropMode:S,onNoCropClick:b,onCroppingEscape:F}){return e.createElement(z,{show:!t&&h==="custom-size",onClick:R=>{R.preventDefault(),R.stopPropagation(),b()},onMouseUp:R=>{R.preventDefault(),R.stopPropagation()},onMouseDown:R=>{R.preventDefault(),R.stopPropagation()}},e.createElement($,null,e.createElement(I.xvT,{size:"body-lg",fontWeight:"bold",color:"white"},L[S].title),e.createElement(I.LZC,{top:"8px",bottom:"8px"},e.createElement(I.xvT,{size:"body-md",fontWeight:"book",color:"grey5"},L[S].description)),e.createElement(Ae,{onClick:R=>{R.preventDefault(),R.stopPropagation(),F()}},"Cancel")),e.createElement(B,null,e.createElement(Q,null,e.createElement(Y,{icon:e.createElement(H.M,null),size:"medium"})),e.createElement(q,null,"Minimum area supported is 250 x 250")))}var j=Object.defineProperty,ue=Object.defineProperties,pe=Object.getOwnPropertyDescriptors,ee=Object.getOwnPropertySymbols,Ee=Object.prototype.hasOwnProperty,Ce=Object.prototype.propertyIsEnumerable,te=(t,h,S)=>h in t?j(t,h,{enumerable:!0,configurable:!0,writable:!0,value:S}):t[h]=S,x=(t,h)=>{for(var S in h||(h={}))Ee.call(h,S)&&te(t,S,h[S]);if(ee)for(var S of ee(h))Ce.call(h,S)&&te(t,S,h[S]);return t},P=(t,h)=>ue(t,pe(h)),_e=(t=>(t.topLeft="top-left",t.topCenter="top-center",t.topRight="top-right",t.middleLeft="middle-left",t.middleRight="middle-right",t.bottomLeft="bottom-left",t.bottomCenter="bottom-center",t.bottomRight="bottom-right",t.middle="middle",t.none="none",t))(_e||{});const fe="1px",k="2px",K=12,D=`${K/2+2}px`,oe={["top-left"]:g.iv`
    top: -${D};
    left: -${D};
  `,["top-center"]:g.iv`
    top: -${D};
    left: calc(50% - ${D});
  `,["top-right"]:g.iv`
    top: -${D};
    right: -${D};
  `,["middle-left"]:g.iv`
    left: -${D};
    top: calc(50% - ${D});
  `,["middle-right"]:g.iv`
    right: -${D};
    top: calc(50% - ${D});
  `,["bottom-left"]:g.iv`
    bottom: -${D};
    left: -${D};
  `,["bottom-center"]:g.iv`
    bottom: -${D};
    left: calc(50% - ${D});
  `,["bottom-right"]:g.iv`
    bottom: -${D};
    right: -${D};
  `,middle:g.iv``,none:g.iv``},ge=E.Z.div`
  background-color: hsla(0, 0%, 13%, 0.6);

  user-select: none;
  -webkit-user-select: none;

  will-change: transform, width, height, border-radius;

  position: absolute;
`,ne=E.Z.div`
  &:before {
    content: '';

    position: absolute;
    top: 4px;
    bottom: 4px;
    left: 4px;
    right: 4px;
  }

  ${t=>oe[t.cornerLocation]}

  position: absolute;
  border: 2px solid rgba(0, 0, 0, 0.25);
  border-radius: 50%;
  width: ${K}px;
  height: ${K}px;

  background: #fff;
  box-sizing: content-box;
  background-clip: content-box;
`,re=E.Z.div`
  width: 100%;
  height: 100%;
  position: relative;
  cursor: crosshair;
`,se=E.Z.div`
  position: relative;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;

  display: flex;
  z-index: 4;

  :active,
  :hover {
    cursor: grab;
  }

  ${t=>t.canEditSelection?g.iv`
          display: flex;
        `:g.iv`
          display: none;
        `}

  ${t=>!t.show&&g.iv`
      display: none;
    `}
`,he=E.Z.div`
  font-size: var(--lns-fontSize-small);

  position: absolute;
  top: calc(100% + 8px);
  right: 0;

  transition: 150ms opacity ease;

  border-radius: 6px;
  padding: 4px 8px;

  background: var(--lns-color-body);

  color: #fff;

  pointer-events: none;

  ${t=>t.isWiggling&&g.iv`
      animation: wiggle 0.5s ease-in-out;
    `}

  @keyframes wiggle {
    0%,
    100% {
      transform: translateX(0);
    }
    25% {
      transform: translateX(-3px);
    }
    75% {
      transform: translateX(3px);
    }
  }
`,Me=E.Z.div`
  position: relative;
`,ie=E.Z.div`
  position: absolute;
  z-index: 3;

  width: calc(100% + ${k});
  height: calc(100% + ${k});
  display: flex;
  justify-content: center;
  align-items: center;

  border: ${fe} dashed white;
  box-sizing: content-box;
  top: -${k};
  left: -${k};
`,V=t=>{t.preventDefault(),t.stopPropagation()},W=()=>{},Oe={x:0,y:0,width:0,height:0},Re=({cropType:t,cropMode:h=v.Video,initialCropSize:S=Oe,canEditSelection:b,children:F,minCropSize:R=250,onCroppingEscape:ce=W,onFirstCrop:ye=W,onCroppingUpdate:Se=W,onCroppingChange:X=W,onNoCropClick:Fe=W,recordingMode:$e})=>{const[Be,J]=(0,e.useState)(!1),[G,De]=(0,e.useState)(!1),[St,Jt]=(0,e.useState)(!1),[Qt,Dt]=(0,e.useState)(!1),Ie=(0,e.useRef)(!1),U=(0,e.useRef)({x:0,y:0}),Z=(0,e.useRef)("none"),ke=(0,e.useRef)(),Ve=(0,e.useRef)(),[a,N]=(0,e.useState)(S),It=(m,y)=>{const A={x:m,y,width:R,height:R};N(A),De(!0),ye(A),X(!1),Se(A)};(0,e.useEffect)(()=>{const m=y=>{y.key==="Escape"&&((0,w.PN)("User hit the escape key "),ce())};return window.addEventListener("click",V),window.addEventListener("keydown",m),()=>{window.removeEventListener("click",V),window.removeEventListener("keydown",m),ae()}},[ce]);const ae=()=>{ke.current&&clearTimeout(ke.current),Ve.current&&clearTimeout(Ve.current)},Tt=()=>{ae(),Dt(!0),Ve.current=setTimeout(()=>Dt(!1),500)},qt={width:"100%",height:`${a.y}px`},eo={width:"100%",height:"auto",top:`${a.y+a.height}px`,bottom:0},to={width:`${a.x}px`,height:`${a.height}px`,top:`${a.y}px`},oo={left:`${a.x+a.width}px`,width:"auto",right:0,height:`${a.height}px`,top:`${a.y}px`},no={left:a.x,top:a.y,width:a.width,height:a.height},ro=m=>{t!==O.Br.WINDOW&&b&&(X(!0),Ie.current=!0,Z.current="none",St||Jt(!0),ae(),J(!0),De(!1),U.current.x=m.clientX,U.current.y=m.clientY,N({x:m.clientX,y:m.clientY,width:0,height:0}))},so=()=>{if(t===O.Br.WINDOW||!b)return;if(Ie.current=!1,a.width===0&&a.height===0){It(a.x,a.y),Tt();return}if(!(a.width>=R&&a.height>=R)){It(a.x,a.y),Tt();return}ye(a),ae(),ke.current=setTimeout(()=>{J(!1)},2e3),X(!1),Se(a)},io=m=>{if(!Ie.current)return;G&&De(!1);const{clientX:y,clientY:A}=m;if(Z.current==="none"){const f=y-U.current.x,T=A-U.current.y,C=f<0?y:U.current.x,po=T<0?A:U.current.y;N({x:C,y:po,width:Math.abs(f),height:Math.abs(T)})}const vt={middle:()=>{const f=y-U.current.x,T=A-U.current.y;U.current.x=y,U.current.y=A,N(C=>P(x({},C),{x:C.x+f,y:C.y+T}))},["top-left"]:()=>{const f=A-a.y,T=y-a.x;N(C=>({x:y,y:A,width:Math.max(0,C.width-T),height:Math.max(0,C.height-f)}))},["top-center"]:()=>{const f=A-a.y;N(T=>P(x({},T),{y:A,height:Math.max(0,T.height-f)}))},["top-right"]:()=>{const f=A-a.y,T=y-a.x;N(C=>P(x({},C),{y:A,width:Math.max(0,T),height:Math.max(0,C.height-f)}))},["middle-right"]:()=>{N(f=>P(x({},f),{width:Math.max(0,y-f.x)}))},["middle-left"]:()=>{const f=y-a.x;N(T=>P(x({},T),{x:y,width:Math.max(0,T.width-f)}))},["bottom-left"]:()=>{const f=A-a.y,T=y-a.x;N(C=>({x:y,y:C.y,width:Math.max(0,C.width-T),height:Math.max(0,f)}))},["bottom-center"]:()=>{N(f=>P(x({},f),{height:Math.max(0,A-f.y)}))},["bottom-right"]:()=>{N(f=>P(x({},f),{width:Math.max(0,y-f.x),height:Math.max(0,A-f.y)}))},none:()=>W};vt[Z.current]&&vt[Z.current](),Z.current!=="none"&&Z.current!=="middle"&&N(f=>{const T=Math.max(f.width,R),C=Math.max(f.height,R);return f.width<R&&f.height<R&&De(!0),P(x({},f),{width:T,height:C})})},At=(m,y)=>{m.stopPropagation(),Ie.current=!0,Z.current=y,X(!0),ae(),J(!0),y==="middle"&&(U.current={x:m.clientX,y:m.clientY})},co=h===v.Video,Ct=a.width!==0&&a.height!==0,ao=a.width===0&&a.height===0&&!St,lo=co&&!G,uo=a.width>=R&&a.height>=R;return e.createElement(re,{onMouseDown:ro,onMouseMove:io,onMouseUp:so,recordingMode:$e},lo&&ao&&e.createElement(le,{cropMode:h,isCropping:Ct,cropType:t,onCroppingEscape:ce,onNoCropClick:Fe}),[qt,eo,to,oo].map((m,y)=>e.createElement(ge,{style:m,key:y})),e.createElement(Me,{style:no},h===v.Video&&e.createElement(se,{show:Ct,canEditSelection:b,onMouseDown:m=>At(m,"middle")},b&&e.createElement(e.Fragment,null,["top-left","top-center","top-right","middle-left","middle-right","bottom-left","bottom-center","bottom-right"].map(m=>e.createElement(ne,{key:m,cornerLocation:m,onClick:V,onMouseDown:y=>At(y,m)})))),uo&&e.createElement(ie,null,F),Be&&e.createElement(he,null,a.width,"x",a.height),G&&e.createElement(he,{isWiggling:Qt},"Minimum size is 250 x 250 px")))};var Ye=o(903285),wt=o(104656);function je(){return(0,s.v9)(t=>t.recorder.isRecording)}function Mt(){return useSelector(t=>t.recorder.paused)}function Ke(){return(0,s.v9)(t=>t.recorder.recordingMode)}function Nt(){return useSelector(t=>t.recorder.recording_type)}function Ne(){return(0,s.v9)(t=>t.recorder.startingRecording)}function Lt(){return useSelector(t=>t.recorder.display)}function xt(){return useSelector(t=>t.recorder.allDisplays)}function Xe(){return useSelector(t=>t.recorder.waiting_on_install)}function Je(){return useSelector(t=>t.recorder.videoDevices)}function Qe(){return useSelector(t=>t.recorder.currentVideoDevice)}function Pt(){return useSelector(t=>t.recorder.alerts)}function Ut(){return useSelector(t=>t.recorder.audioDevices)}function qe(){return useSelector(t=>t.recorder.currentAudioDevice)}function bt(){return useSelector(t=>t.recorder.windows)}function Le(){return useSelector(t=>t.recorder.gettingWindows)}function Wt(){return useSelector(t=>t.recorder.selectedWindowId)}function Gt(){return qe()===null}function et(){return Qe()===null}function Ht(){return useSelector(t=>t.recorder.session?t.recorder.session.id:null)}function Ft(){return useSelector(t=>t.recorder.recorderPromptState)}function tt(){const t=je(),h=Ke(),S=Ne(),b=ot();return(0,s.v9)(F=>({isRecording:t,cropType:F.preRecordingPanel.screen_crop_type,startingRecording:S,cropRect:b,recordingMode:h}))}function ot(){return(0,s.v9)(t=>t.recorder.crop_rect)}function $t(){return useSelector(t=>t.recorder.is_cropping)}var nt=o(957023),xe=o(625507),rt=o(779524);const st=()=>e.createElement(g.xB,{styles:g.iv`
        html {
          height: 100%;

          user-select: none;
        }

        html,
        body {
          width: 100%;
          height: 100%;
          margin: 0;
          overflow: hidden;
        }

        #container {
          position: relative;
          display: flex;
          height: 100%;
        }
      `}),it=()=>{const t=(0,s.I0)(),{cropType:h,isRecording:S,startingRecording:b,cropRect:F,recordingMode:R}=tt(),ce=!S&&!b&&h===O.Br.CUSTOM_SIZE,ye=()=>{S||((0,w.PN)(`user hit escape key to exit ${h}`),t((0,_.mU)()))},Se=G=>{t((0,p.DD)(G)),t((0,_.D0)())},X=G=>{Se(G)},Fe=G=>t((0,p.I8)(G)),$e=()=>{t((0,_.mU)()),t((0,nt.O4)(xe.s.normal)),t((0,rt.yG)({recordingMode:Ye.o_.FullScreen}))},Be=()=>t((0,_.vh)());let J;return h===O.Br.WINDOW&&F&&(J=F),e.createElement(e.Fragment,null,e.createElement(st,null),e.createElement(Re,{cropType:h,initialCropSize:J,onCroppingChange:Fe,onCroppingUpdate:X,canEditSelection:ce,onCroppingEscape:ye,onFirstCrop:Be,recordingMode:R,onNoCropClick:$e}))};var ct=o(239222),at=o(474176);const dt="Loom Analytics Worker",Pe="Loom Camera",Ue="Loom Canvas",lt="Loom Confetti",ut="Loom Control Menu",pt="Loom Countdown",be="Loom Cropping",Et="Loom Disk Critical",Bt="Loom Audio Anomaly",_t="Loom Drawing Overlay",ft="Loom Not Authorized",gt="Loom OAuth",We="Loom Preferences",ht="Loom Recorder",Ot="Loom Recorder Settings",Rt="Loom Screenshot",r="Welcome to Loom Desktop \u{1F389}",M="System Audio Driver Installation",me="Loom Window Selector",Ge="Mouse Highlight Overlay",He="Loom Software Update",kt="Updating Loom",Vt="Loom: Recording a Zoom Meeting",Eo="Loom: Meeting Recording Notes",_o="Loom: Meeting Recording Index",fo="Loom: Meeting Notification",go="Loom: Contextual Onboarding",ho="Loom: Feature Nudge",Zt="Cancel Recording",zt="Restart Recording",Yt="Screenshot Failed",Oo="Cancel Meeting Recording",Ro="Loom: Meeting Recording More Options",mo=[dt,Pe,Ue,lt,ut,pt,be,_t,gt,Et,ft,We,ht,Ot,Rt,r,M,me,Ge,He,kt,Vt,Zt,zt,Yt],yo=null;var jt=o(110720);(0,jt.jC)(),(0,w.FA)("crop"),(0,at.u)();const mt=document.createElement("div"),yt="container";mt.id=yt,document.body.appendChild(mt),document.title=be;const Kt=document.getElementById(yt),Xt=i.S(ct.Q,[]);(t=>(0,l.render)(e.createElement(s.zt,{store:Xt},e.createElement(t,null)),Kt))(it)},23405:(n,c,o)=>{"use strict";o.d(c,{wo:()=>I});var e=o(346972);const l="track-event",s="identify-event",i="page-event",_="get-anon-id",p="ui-viewed-event",O=(0,e.eH)(l,({name:u,props:L})=>({type:l,payload:{name:u,props:L}})),E=(0,e.eH)(i,({name:u})=>({type:i,payload:{name:u}})),g=(0,e.eH)(s,({userId:u,traits:L})=>({type:s,payload:{userId:u,traits:L}})),w=(0,e.eH)(p,()=>({type:p})),v=(0,e.eH)(_,()=>({type:_})),I="update-analytics-anonymous-id",H=u=>({type:I,payload:{id:u}})},987771:(n,c,o)=>{"use strict";let e;function l(i){e=i}function s(i){return new Promise(_=>{const p=e.getState();if(i(p)){_(p);return}const O=e.subscribe(()=>{const E=e.getState();i(E)&&(O(),_(E))})})}},844589:(n,c,o)=>{"use strict";o.d(c,{S:()=>g});var e=o(346972),l=o(835875),s=o(218417),i=o(251308),_=o(29419),p=o(879741),O=o(110720);let E;const g=(w,v)=>{const I=window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__||l.qC,H=(0,e.mu)(),u=[...p.v9?[_.Z]:[],e.Wp,i.Z,s.ZP,...v];return E=(0,l.MT)(w,H,I((0,l.md)(...u),(0,O.cX)())),(0,e.Id)(E),E}},394473:(n,c,o)=>{"use strict";o.d(c,{FA:()=>_,PN:()=>g,o7:()=>I});var e=o(172298),l=o.n(e),s=o(510453);let i="renderer";const _=u=>{u&&(i=u)},p=(u="info",L)=>(z,$)=>{const B={};$&&Object.entries($).forEach(([Q,Y])=>{B[Q]=O(Y)}),e.ipcRenderer.send(s.u,{logLevel:u,message:z,context:B,windowName:L})};function O(u){return typeof u!="object"?u:E(u)?{message:u.message,name:u.name}:JSON.parse(JSON.stringify(u))}function E(u){return typeof u.message=="string"&&typeof u.name=="string"}const g=p("info",i),w=p("warn",i),v=p("error",i),I=p("debug",i),H=u=>({info:p("info",u),warn:p("warn",u),error:p("error",u),debug:p("debug",u)})},621678:(n,c,o)=>{"use strict";o.d(c,{JW:()=>s,p2:()=>i,NR:()=>_,D0:()=>g,mU:()=>w,vh:()=>v});var e=o(346972);const l="push-back-overlay",s="cropping-window-ready",i="cropping-window-close",_="exit-cropping",p="first-crop",O=()=>({type:s}),E=()=>({type:i}),g=(0,e.eH)(l,()=>({type:l})),w=()=>({type:_}),v=()=>({type:p})},206687:(n,c,o)=>{"use strict";o.d(c,{p4:()=>l,$O:()=>s,JC:()=>i,bk:()=>p,Fh:()=>O,S3:()=>E,p1:()=>g,mB:()=>w,mz:()=>v,Uy:()=>I,M9:()=>H,HX:()=>u,VG:()=>L,MK:()=>z,vV:()=>$,BR:()=>B,l1:()=>Y,Qc:()=>q,q6:()=>de,Hd:()=>Ae,UY:()=>le,vc:()=>j,g7:()=>ue,L0:()=>pe,jA:()=>ee,IL:()=>Ee,Ju:()=>Ce,$G:()=>te,zJ:()=>x,zE:()=>P,Wu:()=>_e,KT:()=>fe,Vs:()=>k,n9:()=>K,gQ:()=>ve,IJ:()=>oe,C7:()=>ne,cO:()=>re,th:()=>se,Oh:()=>he,zF:()=>ie,WR:()=>V,MT:()=>W,D1:()=>Ne,hr:()=>Xe,MQ:()=>Je,DD:()=>Le,I8:()=>et,L1:()=>xe,ut:()=>Pe,hY:()=>We});var e=o(346972);const l="add-window-id-to-hide",s="select-video-recording-device",i="set-recording-file-path",_="start-recording-failure",p="start-recording-success",O="update-active-window-title",E="update-all-displays",g="update-recorder-prompt-state",w="update-current-recording-devices",v="update-crop-rect",I="update-current-display",H="update-has-selected-display",u="update-is-cropping",L="update-is-recording",z="update-mic-on",$="update-recording-devices",B="update-recording-type",Q="update-recording-type-selection",Y="reset-recording-state",q="update-selected-window",de="clear-selected-window",Ae="update-msg-type-status",le="update-session",j="update-show-selector-window",ue="update-starting-recording",pe="update-stopping-recording",ee="update-windows",Ee="show-muted-mic-warn",Ce="hide-muted-mic-warn",te="set-recording-time-elapsed",x="update-internal-audio-status",P="update-waiting-on-install",_e="set-start-recording-request-time-ms",fe="set-recording-mode",k="set-recording-alert",K="reset-recording-alert",ve="reset-all-recording-alerts",we="cancel-recording",D="restart-recording",oe="error-recording",ge="get-display-screenshots",ne="get-windows",re="select-audio-recording-device",se="start-recording",he="select-preferred-video-device",Me="after-stop-recording",ie="stop-recording",V="update-recording-paused",W="update-recording-cancelled",Oe="get-internal-audio-status",Re="install-system-audio",Ye=r=>({type:g,payload:{state:r}}),wt=r=>({type:l,payload:{candidate:r}}),je=r=>({type:_e,payload:{timestampMs:r}}),Mt=r=>({type:te,payload:{recordingTimeElapsed:r}}),Ke=()=>({type:Ee,payload:{}}),Nt=(0,e.eH)(re,r=>({type:re})),Ne=r=>({type:s,payload:{device:r}}),Lt=({audioDevice:r,videoDevice:M,selectedAudioDevices:me,selectedVideoDevices:Ge,updateStore:He=!0})=>({type:w,payload:{audioDevice:r,videoDevice:M,selectedAudioDevices:me,selectedVideoDevices:Ge,updateStore:He}}),xt=({audioDevices:r,videoDevices:M})=>({type:$,payload:{audioDevices:r,videoDevices:M}}),Xe=r=>({type:B,payload:{recordingType:r}}),Je=r=>({type:Q,payload:{recordingType:r}}),Qe=r=>({type:i,payload:{path:r}}),Pt=r=>({type:O,payload:{title:r}}),Ut=(r,M=!1)=>({type:E,payload:{displays:r},meta:{updatingWithScreenshots:M}}),qe=(r=!1)=>({type:j,payload:{show:r}}),bt=(r=[])=>({type:ee,payload:{windows:r}}),Le=(r=null)=>({type:v,payload:{cropRect:r}}),Wt=r=>({type:le,payload:{session:r}}),Gt=r=>({type:H,payload:{selected:r}}),et=r=>({type:u,payload:{isCropping:r}}),Ht=r=>({type:L,payload:{isRecording:r}}),Ft=r=>({type:ue,payload:{starting:r}}),tt=r=>({type:pe,payload:{stopping:r}}),ot=r=>({type:W,payload:{cancelSource:r}}),$t=r=>({type:z,payload:{on:r}}),nt=()=>({type:Y}),xe=()=>({type:de}),rt=(0,e.eH)(q,(r,M=!1)=>({type:q})),st=()=>r=>{r(Le(null)),r(Ue())},it=(0,e.eH)(we,(r=!1,M)=>({type:we})),ct=(0,e.eH)(D,(r=!1)=>({type:D})),at=(0,e.eH)(oe,(r="unknown recording error")=>({type:oe})),dt=(0,e.eH)(ne,(r=!0)=>({type:ne})),Pe=(0,e.eH)(I,(r,M=!1)=>({type:I})),Ue=(0,e.eH)(se,(r=!1,M=!1)=>({type:se})),lt=(0,e.eH)(V,r=>({type:V})),ut=(0,e.eH)(ie,r=>({type:ie})),pt=(0,e.eH)(Me,(r,M,me)=>({type:"after-recorder-stopped"})),be=(0,e.eH)(j,(r=!0)=>({type:j})),Et=(0,e.eH)(ge,()=>({type:ge})),Bt=r=>({type:x,payload:{installed:r}}),_t=r=>({type:P,payload:{waiting_on_install:r}}),ft=(0,e.eH)(Oe,r=>({type:Oe})),gt=(0,e.eH)(Re,(r=!1)=>({type:Re})),We=({recordingMode:r,storeValue:M=!0})=>({type:fe,payload:{recordingMode:r,storeValue:M}}),ht=r=>({type:K,payload:{alert:r}}),Ot=()=>({type:ve}),Rt=r=>({type:k,payload:{alert:r}})},871861:(n,c,o)=>{"use strict";o.d(c,{g_:()=>_});var e=o(969178);const l=(0,e.rp)("save-screenshot"),s=(0,e.rp)("delete-screenshot"),i=(0,e.rp)("update-screenshot-title"),_=(0,e.rp)("screenshot-start-select"),p=(0,e.rp)("screenshot-stop-select"),O=(0,e.rp)("play-screenshot-sound")},104656:(n,c,o)=>{var e=o(694919);typeof e=="string"&&(e=[[n.id,e,""]]);var l,s,i={hmr:!0};i.transform=l,i.insertInto=void 0;var _=o(739255)(e,i);e.locals&&(n.exports=e.locals)},439491:n=>{"use strict";n.exports=require("assert")},706113:n=>{"use strict";n.exports=require("crypto")},172298:n=>{"use strict";n.exports=require("electron")},582361:n=>{"use strict";n.exports=require("events")},657147:n=>{"use strict";n.exports=require("fs")},113685:n=>{"use strict";n.exports=require("http")},795687:n=>{"use strict";n.exports=require("https")},822037:n=>{"use strict";n.exports=require("os")},371017:n=>{"use strict";n.exports=require("path")},863477:n=>{"use strict";n.exports=require("querystring")},257310:n=>{"use strict";n.exports=require("url")},473837:n=>{"use strict";n.exports=require("util")}},Te={};function d(n){var c=Te[n];if(c!==void 0)return c.exports;var o=Te[n]={id:n,loaded:!1,exports:{}};return Ze[n].call(o.exports,o,o.exports,d),o.loaded=!0,o.exports}d.m=Ze,d.c=Te,(()=>{var n=[];d.O=(c,o,e,l)=>{if(o){l=l||0;for(var s=n.length;s>0&&n[s-1][2]>l;s--)n[s]=n[s-1];n[s]=[o,e,l];return}for(var i=1/0,s=0;s<n.length;s++){for(var[o,e,l]=n[s],_=!0,p=0;p<o.length;p++)(l&!1||i>=l)&&Object.keys(d.O).every(I=>d.O[I](o[p]))?o.splice(p--,1):(_=!1,l<i&&(i=l));if(_){n.splice(s--,1);var O=e();O!==void 0&&(c=O)}}return c}})(),d.n=n=>{var c=n&&n.__esModule?()=>n.default:()=>n;return d.d(c,{a:c}),c},(()=>{var n=Object.getPrototypeOf?o=>Object.getPrototypeOf(o):o=>o.__proto__,c;d.t=function(o,e){if(e&1&&(o=this(o)),e&8||typeof o=="object"&&o&&(e&4&&o.__esModule||e&16&&typeof o.then=="function"))return o;var l=Object.create(null);d.r(l);var s={};c=c||[null,n({}),n([]),n(n)];for(var i=e&2&&o;typeof i=="object"&&!~c.indexOf(i);i=n(i))Object.getOwnPropertyNames(i).forEach(_=>s[_]=()=>o[_]);return s.default=()=>o,d.d(l,s),l}})(),d.d=(n,c)=>{for(var o in c)d.o(c,o)&&!d.o(n,o)&&Object.defineProperty(n,o,{enumerable:!0,get:c[o]})},d.h=()=>"55e5c6a40d444554bfb1",d.hmd=n=>(n=Object.create(n),n.children||(n.children=[]),Object.defineProperty(n,"exports",{enumerable:!0,set:()=>{throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+n.id)}}),n),d.o=(n,c)=>Object.prototype.hasOwnProperty.call(n,c),d.r=n=>{typeof Symbol<"u"&&Symbol.toStringTag&&Object.defineProperty(n,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(n,"__esModule",{value:!0})},d.nmd=n=>(n.paths=[],n.children||(n.children=[]),n),d.p="./",(()=>{var n={6222:0};d.O.j=e=>n[e]===0;var c=(e,l)=>{var[s,i,_]=l,p,O,E=0;if(s.some(w=>n[w]!==0)){for(p in i)d.o(i,p)&&(d.m[p]=i[p]);if(_)var g=_(d)}for(e&&e(l);E<s.length;E++)O=s[E],d.o(n,O)&&n[O]&&n[O][0](),n[s[E]]=0;return d.O(g)},o=global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[];o.forEach(c.bind(null,0)),o.push=c.bind(null,o.push.bind(o))})(),d.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,947,403,2699,4576,1404,3655,816,3322,3792,119],()=>d(d.s=903679)),d.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,947,403,2699,4576,1404,3655,816,3322,3792,119],()=>d(d.s=255347)),d.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,947,403,2699,4576,1404,3655,816,3322,3792,119],()=>d(d.s=639542));var ze=d.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,947,403,2699,4576,1404,3655,816,3322,3792,119],()=>d(d.s=194383));ze=d.O(ze)})();

//# sourceMappingURL=cropping.js.map