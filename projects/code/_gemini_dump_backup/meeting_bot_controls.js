(()=>{"use strict";var Kt={439900:(o,s,n)=>{var t=n(275271),i=n(230967),a=n(443934),l=n(844589),R=n(474176),u=n(394473),N=n(110720),A=n(239222),P=n(974144),B=n(924630),S=n(65629),I=Object.defineProperty,b=Object.defineProperties,E=Object.getOwnPropertyDescriptors,U=Object.getOwnPropertySymbols,C=Object.prototype.hasOwnProperty,K=Object.prototype.propertyIsEnumerable,H=(e,c,r)=>c in e?I(e,c,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[c]=r,j=(e,c)=>{for(var r in c||(c={}))C.call(c,r)&&H(e,r,c[r]);if(U)for(var r of U(c))K.call(c,r)&&H(e,r,c[r]);return e},F=(e,c)=>b(e,E(c));const J=e=>(0,a.v9)(c=>c.botControlMenu.botMap[e]),g=()=>(0,a.v9)(e=>e.botControlMenu.showJoinButton),L=()=>(0,a.v9)(e=>e.botControlMenu.inCollapsedView),y=()=>(0,a.v9)(e=>e.botControlMenu.isOverflowMenuOpen),$=e=>{var c,r;const _=(0,B.II)(),O=((c=e?.recorder)==null?void 0:c.id)===_,p=((r=e?.organizer)==null?void 0:r.id)===_;return(0,t.useMemo)(()=>F(j(j(j({},e?.videoMeetingGuid&&{videoMeetingGuid:e.videoMeetingGuid}),e?.calendarMeetingGuid&&{calendarMeetingGuid:e.calendarMeetingGuid}),e?.videoId&&{videoId:e?.videoId}),{isMeetingRecorder:O,isMeetingOrganizer:p}),[e,O,p])},ae=()=>(0,a.v9)(e=>e.botControlMenu.meetingGuids),Re=()=>(0,a.v9)(e=>e.botControlMenu.hideForTransform),Ie=()=>{const e=J(S.Vk).recordingState===S.m3.IDLE,c=g(),r=ae();return!(e&&!c||!r)};var m=n(992671),M=n(450630),T=n(183780);const z="rgba(33, 33, 33, 1.0)",Q="rgba(43, 43, 43, 1.0)",ne="var(--lns-color-white)",_e="rgba(255, 255, 255, 0.1)",me="rgba(107, 110, 118, 0.5)",ge="var(--lns-color-blue)",De="var(--lns-color-blue)",ve="#1558BC",oe=8,Ae=10,ze=8,V=10,fe=2*V,be="#6A9A23",Ee="#C9372C",q="var(--lns-color-bodyDimmed);";var f=n(695610),ce=n(818421);const Pe=(0,m.Z)(T.hU)`
  width: ${f.Fl}px;
  height: ${f.Fl}px;
  border-radius: var(--lns-radius-175);
  background: ${({backgroundColor:e})=>e??"transparent"};
  ${({shouldDisableTransitions:e})=>e&&"transition: none"};

  svg {
    color: ${ne};
  }

  :hover {
    background: ${({hoverBackgroundColor:e})=>e??_e};
  }
`,re=({tooltipText:e,icon:c,onClick:r,backgroundColor:_,hoverBackgroundColor:O,isButtonDisabled:p})=>{const v=L(),[D,G]=(0,t.useState)(!1);return(0,t.useEffect)(()=>{G(!0),setTimeout(()=>G(!1),300)},[v]),t.createElement(ce.iU,null,t.createElement(Pe,{icon:c,altText:e,backgroundColor:_,hoverBackgroundColor:O,shouldDisableTransitions:D,isDisabled:p,onClick:r,size:"small"}))};var h=n(377534),k=n(70002),le=n(390620),Ve=n(143617),Y=n(283297),Z=n(523179),Le=Object.defineProperty,ee=Object.getOwnPropertySymbols,de=Object.prototype.hasOwnProperty,ue=Object.prototype.propertyIsEnumerable,Te=(e,c,r)=>c in e?Le(e,c,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[c]=r,he=(e,c)=>{for(var r in c||(c={}))de.call(c,r)&&Te(e,r,c[r]);if(ee)for(var r of ee(c))ue.call(c,r)&&Te(e,r,c[r]);return e},ye=(e,c)=>{var r={};for(var _ in e)de.call(e,_)&&c.indexOf(_)<0&&(r[_]=e[_]);if(e!=null&&ee)for(var _ of ee(e))c.indexOf(_)<0&&ue.call(e,_)&&(r[_]=e[_]);return r};const ie={medium:{totalSize:(0,T.u)(3),barHeight:(0,T.u)(2.25)}},Oe={medium:{totalSize:(0,T.u)(2.5),barHeight:(0,T.u)(2.25)}},pe={fast:1.2,slow:1.7},Me=["rgba(24, 104, 219, 1)","rgba(130, 181, 54, 1)","rgba(191, 99, 243, 1)","rgba(252, 167, 0, 1)"],ke="linear-gradient(270deg, #565ADD 10.58%, #DC43BE 41.83%, #565ADD 69.23%, #565ADD 96.63%)",Qe=2,Ge=5,qe=4,et=.25,$t=(0,T.u)(et),tt=e=>(e.isTwc?Oe:ie)[e.size||"medium"].barHeight,te=e=>(e.isTwc?Oe:ie)[e.size||"medium"].totalSize,Ue=e=>pe[e.speed||"fast"],nt=()=>`border-radius: ${(0,T.u)(et/2)};`,ot=e=>e?qe:Ge,ct=M.F4`
  0%, 100% {
    transform: scaleY(0.3);
  }
  50% {
    transform: scaleY(1);
  }
`,rt=M.F4`
  0% {
    background-position: 0% center;
  }
  100% {
    background-position: 100% center;
  }
`,it=M.F4`
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
`,st=m.Z.span`
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
  height: ${e=>te(e)};
  width: ${e=>te(e)};
  position: relative;
`,at=m.Z.span`
  width: ${$t};
  height: ${e=>tt(e)};
  background: ${e=>e.color==="ai-primary"?ke:(0,T.RvU)(e.color)};
  background-size: ${e=>te(e)}
    ${e=>te(e)};
  background-position: ${e=>{const r=(e.index+1)/(Ge+1)-.5;return`calc(${te(e)} * ${r}) center`}};
  opacity: 0; /* Ensure it starts invisible */
  transform: scaleY(0.3);
  transform-origin: center;
  animation:
    ${it} 50ms ease-out forwards,
    ${ct} ${e=>Ue(e)}s ease-in-out infinite,
    ${rt} ${Qe}s linear infinite;

  animation-delay: ${e=>-1+e.index*(Ue(e)/Ge)}s;
  position: relative;
  ${e=>e.isTwc&&nt()}
  ${e=>e.stop&&`
    opacity: 1;
    animation: none;
    transform: scaleY(0.1);
  `}
`,_t=e=>{var c=e,{size:r="medium",speed:_="fast",color:O="body",isTwc:p=!1,stop:v=!1}=c,D=ye(c,["size","speed","color","isTwc","stop"]);const G=Array.from({length:ot(p)},(x,W)=>{const X=p?Me[W]:O;return t.createElement(at,{key:W,index:W,size:r,speed:_,color:X,isTwc:p,stop:v})});return t.createElement(st,he({size:r,color:O,isTwc:p},D),G)},zt=Object.keys(ie),Vt=Object.keys(pe),Et=_t;var lt=n(407973),dt=n(433475),ut=n(856555),Tt=n(330075),Ot=n(626031);const pt=m.Z.div`
  display: flex;
  gap: 2px;
  justify-content: space-evenly;
  align-items: center;
  padding: ${oe}px;
  background: ${Q};
`,St=(0,m.Z)(T.W20)`
  display: flex;
  align-items: center;
  z-index: 2;
  opacity: 1;
  margin: 4px 8px 4px 4px;
`,Ct=(0,m.Z)(T.TRl)`
  width: 28px;
  height: 28px;
  margin-right: 4px;
`,Nt=m.Z.img`
  width: 24px;
  height: 24px;
`,Rt=({canShowInCurrentRecordingState:e})=>t.createElement(St,null,t.createElement(Et,{isTwc:!0,stop:!e})),It=(0,m.Z)(T.zxk)`
  color: ${ne};
  background: ${({backgroundColor:e})=>e??"transparent"};

  :hover {
    background: ${({hoverBackgroundColor:e})=>e??_e};
  }
`,Be=t.createElement(Ct,{variant:"symbol",brand:"apptile",symbolColor:"transparent"}),mt=({isCollapsed:e,recordingState:c,analyticsProps:r,pausePressed:_,meeting:O})=>{const p=S.dD.has(c),v=t.createElement(T.aNw,{size:"small",color:"white"}),D=y(),G=S.Wp.has(c);return t.createElement(pt,null,e&&(O?t.createElement(Ot.q,{meeting:O,defaultIcon:Be}):Be),t.createElement(Rt,{canShowInCurrentRecordingState:!_}),p?t.createElement(ce.iU,null,t.createElement(It,{iconBefore:c===S.m3.RESUMING?v:t.createElement(dt.R,null),onClick:()=>{(0,h.P)(k.q8,{action:le.jS1.Resume}),(0,Y.j)(Z.np,r)},isDisabled:G,size:"small",backgroundColor:De,hoverBackgroundColor:ve},"Resume")):t.createElement(re,{icon:c===S.m3.RECORDING?t.createElement(Ve.T,null):v,onClick:()=>{(0,h.P)(k.q8,{action:le.jS1.Pause}),(0,Y.j)(Z.ND,r)},isButtonDisabled:G,backgroundColor:me,hoverBackgroundColor:ge,tooltipText:"Pause Recording"}),t.createElement(re,{icon:t.createElement(lt.s,null),onClick:()=>{D?(0,h.P)(k.A6):(0,h.P)(k.RA)},tooltipText:"More options"}),e&&t.createElement(re,{icon:t.createElement(Nt,{src:ut}),onClick:()=>{e&&((0,h.P)(Tt.FM),(0,Y.j)(Z.i4,r))},tooltipText:e?"Open notes":"Minimize"}))};var gt=n(25894),Dt=n(819906),vt=n(287631),At=n(910491),je=n(631915);const ft=m.Z.button`
  position: absolute;
  top: -4px;
  right: -4px;
  width: 20px;
  height: 20px;
  background-color: ${z};
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  transition: color 0.2s ease-in-out;
  -webkit-app-region: no-drag;
  :hover {
    svg {
      color: white;
    }
  }
`,bt=(0,m.Z)(T.xvT)`
  :hover {
    color: ${q};
    cursor: pointer;
  }
`,We="Dismiss",He=({videoId:e,meetingGuids:c,recordingState:r,setStopFromParticipantsLeft:_,isCollapsed:O,analyticsProps:p})=>{const v=()=>r===S.m3.CANCELLED?{headerText:"Recording deleted",headerIcon:t.createElement(T.JO$,{icon:t.createElement(At.X,null),color:Ee,size:"large"})}:r===S.m3.PARTICIPANTS_LEFT?{headerText:"Meeting ended",headerIcon:t.createElement(T.JO$,{icon:t.createElement(vt.n,null),color:ne,size:"large"})}:r===S.m3.STOPPING?{headerText:"Video uploading",headerIcon:t.createElement(T.aNw,{size:"medium",color:"white"})}:{headerText:"Recording done",headerIcon:t.createElement(T.JO$,{icon:t.createElement(Dt.l,null),color:be,size:"large"})},{headerText:D,headerIcon:G}=v();return t.createElement(T.W20,{padding:`${oe}px`,backgroundColor:Q},t.createElement(T.ggW,{height:`${f.Fl}px`,justifyContent:"center",alignItems:"center",gap:"xsmall"},G,t.createElement(T.xvT,{fontWeight:"bold",size:"body-md",noWrap:!0},D),t.createElement(T.xvT,{color:q},"|"),t.createElement(Pt,{meetingGuids:c,recordingState:r,setStopFromParticipantsLeft:_,isCollapsed:O,analyticsProps:p,videoId:e})),O&&t.createElement(ft,{onClick:()=>(0,h.P)(k.kb,{isCollapsed:O})},t.createElement(T.JO$,{icon:t.createElement(je.G,null),size:"12px",color:"bodyDimmed"})))},Pt=({meetingGuids:e,videoId:c,recordingState:r,setStopFromParticipantsLeft:_,isCollapsed:O,analyticsProps:p})=>{const v=()=>r===S.m3.STOPPED&&c?{ctaText:"Manage on Loom",ctaIcon:t.createElement(T.JO$,{icon:t.createElement(gt.l,null),color:q,size:"medium"}),onClick:()=>{(0,h.P)(k.N1,{meetingGuids:e,videoId:c,isCollapsed:O}),(0,Y.j)(Z.oS,p)}}:r===S.m3.PARTICIPANTS_LEFT?{ctaText:"Finish recording",ctaIcon:null,onClick:()=>{_(!0),(0,h.P)(k.q8,{action:le.jS1.Stop}),(0,Y.j)(Z.dw,p)}}:{ctaText:We,ctaIcon:null,onClick:()=>{(0,h.P)(k.kb,{isCollapsed:O}),(0,Y.j)(Z.iZ,p)}},{ctaText:D,ctaIcon:G,onClick:x}=v();return t.createElement(T.W20,null,t.createElement(T.ggW,{justifyContent:"center",gap:"xsmall"},t.createElement(ce.iU,null,t.createElement(bt,{size:"body-sm",noWrap:!0,onClick:x},D)),G))};var Yt=n(95376),Zt=n(397063),xe=n(997753),Lt=n(995346),we=n(301753);const ht=e=>{switch(e){case"record":return"Record meeting";case"recording-enabled":return"Set to record";case"join-meeting":return"Join meeting";case"open-notes":return"Open notes";case"snooze":return"Snooze for today";case"open-notification-settings":return"Notification settings";default:return""}},yt=(e,c,r,_)=>{if(e.isGenericNotification||e.isFailedMeeting)return null;if(c==="success")return"recording-enabled";const O=e.meeting;return O&&_?"join-meeting":c==="loading"||e.isAutoDetectedMeeting||!O||!O.record?"record":r?"open-notes":"join-meeting"},Mt=M.F4`
  0% {
    opacity: 0.5;
    transform: scale(0.95);
  }
  50% {
    transform: scale(1.025);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
`,kt=m.Z.button`
  background: var(--lns-color-background);
  border: solid 1px var(--lns-color-border);
  border-radius: 8px;
  color: var(--lns-color-body);
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  height: 38px;
  font-size: 12px;
  padding: 0 16px;
  font-weight: bold;
  position: relative;
  z-index: 2;
  transition: all 0.2s ease-in-out;
  animation: ${Mt} 200ms ease-in-out;

  svg {
    transition: all 0.2s ease-in-out;
  }

  &:hover {
    color: var(--lns-color-blue);
    background-color: #e9e9fd80;
    border-color: #8fb8f6; // Extended/Blue/B300

    svg {
      color: var(--lns-color-blue);
    }
  }

  &:active {
    background-color: #cfe1fd;
    border-color: #1558bc; // color/text/accent/blue/default
    color: #1558bc;

    svg {
      color: #1558bc;
    }
  }

  &:disabled {
    opacity: 0.5;
  }
`,Xt=({action:e,notification:c,isDisabled:r,onClick:_})=>{let O=null,p=null,v;const D=actionTitle(e);switch(e){case"record":c.isAutoDetectedMeeting?O=Se(c.meetingPlatform):p=React.createElement(SvgVideoCam,null);break;case"recording-enabled":p=React.createElement(SvgCheckCircleFill,null),v="success";break;case"join-meeting":O=Se(c.meetingPlatform);break;case"open-notes":p=React.createElement(SvgConfluence,null);break;default:break}return React.createElement(kt,{onClick:_,key:e,disabled:r},O&&React.createElement("img",{src:O,style:{width:"16px",height:"16px"}}),p&&React.createElement(Icon,{icon:p,size:"20px",color:v}),D)},Se=e=>{switch(e){case"ZOOM":return xe;case"GOOGLE_MEET":return Lt;case"MICROSOFT_TEAMS":return we;default:return null}};var Ke=n(898228),Gt=n(36048);const Ut=m.Z.button`
  position: absolute;
  top: -4px;
  right: -4px;
  width: 20px;
  height: 20px;
  background-color: ${z};
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  transition: color 0.2s ease-in-out;
  -webkit-app-region: no-drag;
  :hover {
    svg {
      color: var(--lns-color-bodyDimmed);
    }
  }
`,Bt=(0,m.Z)(T.xvT)`
  white-space: nowrap;
  color: white;
  :hover {
    color: var(--lns-color-bodyDimmed);
    cursor: pointer;
  }
`,jt=m.Z.img`
  width: 24px;
  height: 24px;
`,Wt=({meetingUrl:e,meetingPlatform:c})=>{const r=Se(c),[_,O]=(0,t.useState)(!1),p=(0,a.I0)();return e?t.createElement(T.W20,{padding:`${oe}px`,backgroundColor:Q,radius:"250",onMouseEnter:()=>O(!0),onMouseLeave:()=>O(!1)},t.createElement(T.ggW,{height:`${f.Fl}px`,justifyContent:"center",alignItems:"center",gap:"xsmall",onClick:()=>{(0,Gt.m)(p,e,!1),p((0,Ke.RD)(!1))}},r&&t.createElement(jt,{src:r,alt:"Meeting platform icon"}),t.createElement(Bt,{fontWeight:"bold",size:"body-md"},"Join meeting")),_&&t.createElement(Ut,{onClick:()=>{p((0,Ke.RD)(!1))}},t.createElement(T.JO$,{icon:t.createElement(je.G,null),size:"12px",color:"white"}))):null};var Ht=n(950117);const Jt=(e,c,r)=>{const _=Fe(e,c,r);return Math.max(_*1.1+CONTROLS_WINDOW_WIDTH_MARGIN,MIN_CONTROLS_ONLY_WIDTH)},Fe=(e,c,r)=>{const _=!r;return e?f.z9:c&&_?f.ED:_?f.CQ:c?f.r2:f.T0};var Qt=n(330516);const xt="150ms",wt=M.F4`
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
`,sn=M.F4`
  0% {
    transform: scale(1.0);
  }
  10% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
`,an=m.Z.div`
  height: 100%;

  transform-origin: center center;
  ${({state:e})=>{switch(e){case"entering":return M.iv`
          animation: ${sn} ${xt} ease-in-out;
          opacity: 1;
        `;case"entered":return M.iv`
          opacity: 1;
        `;case"exiting":return M.iv`
          animation: ${wt} ${xt} ease-in-out;
          opacity: 0;
        `;case"exited":return M.iv`
          opacity: 0;
        `;default:return}}}
`,qt=({children:e})=>{const c=(0,t.useRef)(null),r=Re();return t.createElement(Qt.uT,{nodeRef:c,in:!r,timeout:150},_=>t.createElement(an,{state:_,className:_,ref:c},e))},_n=(e,c,r)=>M.iv`
  ${M.F4`
  0% {
    transform: translateX(0);
  }
  ${r}% {
    transform: translateX(-${e}px);
  }
  100% {
      transform: translateX(-${e}px);
  }
`} ${c}s linear infinite
`,En=m.Z.div`
  white-space: nowrap;
  overflow: visible;
  vertical-align: middle;
  text-align: center;
  animation: ${({shouldScroll:e,animationDuration:c,textWidthWithSpacing:r,delayStartPercentage:_})=>e?_n(r,c,_):"none"};
  animation-delay: ${f.Ao}s;
  padding-left: ${({shouldScroll:e})=>e?V:0}px;
`,en=m.Z.div`
  position: fixed;
  visibility: hidden;
  white-space: nowrap;
  top: -9999px;
  left: -9999px;
  pointer-events: none;
`,tn=m.Z.span`
  padding-right: 1em;
`,ln=t.forwardRef(({text:e,containerWidth:c,rightShadowPadding:r=0,className:_},O)=>{const[p,v]=(0,t.useState)(0),[D,G]=(0,t.useState)(0),x=(0,t.useRef)(null),W=(0,t.useRef)(null),X=c-r,w=p>X,se=D/f.df+f.Ao,Ce=100-f.Ao*100/se;return(0,t.useEffect)(()=>{x.current&&v(x.current.offsetWidth),W.current&&G(W.current.offsetWidth)},[e]),t.createElement(t.Fragment,null,t.createElement(en,{ref:x},e),t.createElement(en,{ref:W},t.createElement(tn,null,e)),t.createElement(En,{ref:O,shouldScroll:w,animationDuration:se,delayStartPercentage:Ce,textWidthWithSpacing:D,className:_},w?t.createElement(t.Fragment,null,t.createElement(tn,null,e),e):e))}),dn=M.F4`
  0% {
    transform: translate(-50%, 0) scale(1.0);
  }
  10% {
    transform: translate(-50%, 0) scale(1.1);
  }
  100% {
    transform: translate(-50%, 0) scale(1);
  }
`,nn=(0,m.Z)(T.W20)`
  transform: translate(-50%, 0) scale(1);

  &.bounce-animation {
    animation-delay: 0.1s;
    animation: ${dn} 0.3s ease-out;
  }
`,un=(0,m.Z)(T.W20)`
  color: white;
  background-color: ${Q};
  border-radius: var(--lns-radius-250);
  border: 1px solid rgba(255, 255, 255, 0.15);
  overflow: hidden;
  width: ${({width:e})=>e}px;
  -webkit-app-region: ${({shouldDrag:e})=>e?"drag":"no-drag"};
`,Tn=(0,m.Z)(T.W20)`
  background: ${z};
  padding: ${Ae}px 0;
`,On=(0,m.Z)(T.xvT)`
  width: ${({width:e})=>e}px;
`,on=m.Z.div`
  width: 0;
  box-shadow: 0 0 ${V}px ${V}px
    ${z};
  z-index: 2;
`,pn=(0,m.Z)(T.W20)`
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
`,Sn=()=>{var e;const c=L(),[r,_]=(0,t.useState)("");(0,t.useEffect)(()=>{_("bounce-animation");const Ne=setTimeout(()=>_(""),400);return()=>{clearTimeout(Ne)}},[c]);const{recordingState:O,videoId:p}=J(S.Vk),v=ae(),D=(0,Ht.W9)((e=v?.calendarMeetingGuid)!=null?e:void 0),G=$(D),x=g(),W=O===S.m3.IDLE,X=D?.platform||void 0,w=D?.url||void 0,se=D?.title||"Your meeting",Ce=Ie();return(0,t.useEffect)(()=>{(0,h.P)(k.pI,v)},[v]),!Ce||!v?null:W&&x?t.createElement(nn,{position:"absolute",left:"50%",top:`${f.lL}px`},t.createElement(qt,null,t.createElement(Wt,{meetingPlatform:X,meetingUrl:w}))):t.createElement(nn,{position:"absolute",left:"50%",top:`${f.lL}px`,className:r},t.createElement(qt,null,t.createElement(Cn,{recordingState:O,isCollapsed:c,meetingGuids:v,videoId:p,meetingTitle:se,analyticsProps:G,meeting:D})))},Cn=({recordingState:e,isCollapsed:c,meetingGuids:r,videoId:_,meetingTitle:O,analyticsProps:p,meeting:v})=>{const[D,G]=(0,t.useState)(!1),x=e===S.m3.STOPPING&&D,[W,X]=(0,t.useState)(!1),w=S.A_.has(e)||x,se=S.dD.has(e),Ce=c;(0,t.useEffect)(()=>{e===S.m3.PAUSED?X(!0):e!==S.m3.STOPPING&&e!==S.m3.CANCELLING&&e!==S.m3.RESUMING&&X(!1)},[e]),(0,t.useEffect)(()=>{w&&(0,h.P)(k.A6)},[w]),(0,t.useEffect)(()=>{(!S.Wp.has(e)||e===S.m3.STOPPING)&&(P.is.macos?setTimeout(()=>(0,h.P)(k.TZ)):setTimeout(()=>{(0,h.P)(k.TZ)},f.zn))},[e]),(0,t.useEffect)(()=>{P.is.macos?setTimeout(()=>{(0,h.P)(k.TZ)},f.yf):setTimeout(()=>{(0,h.P)(k.TZ)},f.YO)},[c]);const Ne=Fe(w,se,!c),mn=Ne-fe;return t.createElement(un,{width:Ne,shouldDrag:Ce},t.createElement(pn,null,w?t.createElement(He,{recordingState:e,isCollapsed:c,meetingGuids:r,videoId:_,setStopFromParticipantsLeft:G,analyticsProps:p}):t.createElement(mt,{isCollapsed:c,recordingState:e,analyticsProps:p,pausePressed:W,meeting:v}),c&&t.createElement(Tn,null,t.createElement(T.ggW,{autoFlow:"column",justifyContent:"center"},t.createElement(on,null),t.createElement(On,{hasEllipsis:!0,ellipsisLines:1,width:Ne},t.createElement(ln,{text:O,containerWidth:mn,rightShadowPadding:V})),t.createElement(on,null)))))};(0,N.jC)(),(0,u.FA)("botControlsMenu"),(0,R.u)();const cn=document.createElement("div"),rn="container";cn.id=rn,document.body.appendChild(cn);const Nn=document.getElementById(rn),Rn=l.S(A.Q,[]),In=()=>t.createElement(M.xB,{styles:M.iv`
      html,
      body {
        user-select: none;
        overflow: hidden;

        // hack for styling the overflow menu
        // since the implementation is abstracted in lens
        #layers * ul {
          background-color: rgb(25, 25, 25);
          color: white;
          > svg {
            background-color: white;
          }
          > *:hover {
            background-color: var(--lns-color-grey7);
          }
        }
      }
    `});(e=>(0,i.render)(t.createElement(a.zt,{store:Rn},t.createElement(In,null),t.createElement(e,null)),Nn))(Sn)},23405:(o,s,n)=>{n.d(s,{L9:()=>N,wo:()=>I});var t=n(346972);const i="track-event",a="identify-event",l="page-event",R="get-anon-id",u="ui-viewed-event",N=(0,t.eH)(i,({name:E,props:U})=>({type:i,payload:{name:E,props:U}})),A=(0,t.eH)(l,({name:E})=>({type:l,payload:{name:E}})),P=(0,t.eH)(a,({userId:E,traits:U})=>({type:a,payload:{userId:E,traits:U}})),B=(0,t.eH)(u,()=>({type:u})),S=(0,t.eH)(R,()=>({type:R})),I="update-analytics-anonymous-id",b=E=>({type:I,payload:{id:E}})},283297:(o,s,n)=>{n.d(s,{j:()=>P});var t=n(23405),i=n(604822),a=n(987771),l=n(844589);const R=(0,i.h)("analytics","\u{1F596}"),u=()=>l.h?l.h:a.h;function N(I){const b=u();b?setImmediate(()=>{I(b.dispatch)}):R.warn("Could not run analytics event. Redux store has not been created yet")}function A(I,b){N(E=>{E(pageEvent({name:I,props:b}))})}function P(I,b){N(E=>{E((0,t.L9)({name:I,props:b}))})}function B(I,b){N(E=>{E(identifyEvent({userId:I,traits:b}))})}function S(){const I=u();return{anonId:I?I.getState().analytics.anonymous_id:null}}},523179:(o,s,n)=>{n.d(s,{ND:()=>We,np:()=>He,i4:()=>xe,oS:()=>we,dw:()=>ht,iZ:()=>yt});const t="Desktop Binary Timeout",i="Desktop Permissions Onboarding",a="Desktop Confetti",l="Desktop Keyboard Shortcuts Updated",R="Desktop Launch",u="Desktop Menu Activated",N="Desktop Speaker Notes",A="Desktop Screenshot Preview",P="Desktop Screenshot Shortcut Setup",B="Desktop Screenshot Try It Ftux",S="System Audio Modal",I="Desktop Quit",b="Log Out",E="Pro Tag Clicked",U="Desktop Used Confetti",C="Uploader User Canceled Failed Retries",K="Uploader User Attempted Failed Retries",H="Engaged an RBAC restriction",j="Desktop Camera Bubble Rendered",F="Desktop Critical Error While Recording",J="Desktop Recorder Stop",g="Cascading Recorders Modal",L="Desktop Screenshot Capture Shortcut Pressed",y="Desktop Screenshot Capture Started",$="Desktop Screenshot Capture Completed",ae="Desktop Screenshot Capture Failed",Re="Desktop Screenshot Capture Cancelled",Ie="Desktop Screenshot Upload Started",m="Desktop Screenshot Upload Completed",M="Desktop Screenshot Upload Failed",T="Restart Recording Keyboard Shortcut",z="Event Recording Restart Prompt Reject",Q="Event Recording Restart Prompt Confirm",ne="App quit during recording",_e="Desktop SRT successfully received",me="Desktop shared auth successful",ge="Desktop shared auth initiated",De="Desktop shared auth welcome flow triggered",ve="User app restart on start recording failure",oe="User app quit on start recording failure",Ae="Quit During Recording Prompt",ze="Desktop Countdown Paused",V="Desktop Countdown Unpaused",fe="Desktop Countdown Skipped",be="Desktop Countdown Cancelled",Ee="Desktop Onboarding Started",q="Desktop Onboarding Step Viewed",f="Desktop Onboarding Permissions Requested",ce="Received Desktop Notification",Pe="Clicked desktop Notification",re="Desktop Notification Permission Prompt Accepted",h="Desktop Notifications Notification Click",k="Start Recording button clicked on canvas",le="Speaker notes toggled",Ve="Speaker notes moved",Y="Speaker notes resized",Z="Failed video successfully recovered",Le="desktop_capture_mode_toggle_clicked",ee="desktop_screenshot_select_area_button_clicked",de="desktop_screenshot_capture_shortcut_pressed",ue="desktop_screenshot_capture_mode_entered",Te="desktop_screenshot_capture_cancelled",he="desktop_screenshot_capture_completed",ye="desktop_screenshot_capture_failed",ie="desktop_screenshot_preview_edit_in_loom_clicked",Oe="desktop_screenshot_preview_dragged_to_upload",pe="desktop_screenshot_preview_copy_link_clicked",Ye="desktop_screenshot_preview_kebab_menu_clicked",Ze="desktop_screenshot_preview_download_clicked",Xe="desktop_screenshot_preview_copy_image_clicked",Je="desktop_screenshot_preview_retake_image_clicked",Me="desktop_screenshot_preview_delete_image_clicked",ke="desktop_screenshots_keyboard_shortcut_set",Qe="desktop_tooltip_screenshots_button_clicked",Ge="desktop_tooltip_screenshots_dismissed",qe="desktop_screenshots_shortcut_onboarding_step_completed",et="desktop_screenshots_try_it_ftux_button_clicked",$t="desktop_screenshots_try_it_ftux_dismissed",tt="desktop_meeting_recording_tab_clicked",te="desktop_meeting_recording_record_meeting_clicked",Ue="desktop_meeting_recording_record_now_clicked",nt="desktop_meeting_recording_nudge_notification_shown",ot="desktop_meeting_recording_nudge_notification_clicked",ct="desktop_meeting_recording_nudge_notification_button_clicked",rt="desktop_meeting_recording_nudge_notification_menu_opened",it="desktop_meeting_recording_nudge_notification_menu_button_clicked",st="desktop_meeting_recording_reminders_banner_shown",at="desktop_meeting_recording_reminders_banner_allow_clicked",_t="desktop_meeting_recording_reminders_banner_dismiss_clicked",zt="desktop_meeting_recording_reminders_setting_enabled",Vt="desktop_meeting_recording_reminders_setting_disabled",Et="desktopMeetingNotes",lt="desktopMeetingTranscript",dt="desktopMeetingAgent",ut="desktopMeetingList",Tt="desktopMeetingListDisconnectedState",Ot="meetingRecordingTranscriptButton",pt="meetingRecordingMeetingNotesButton",St="meetingRecordingJoinMeetingButton",Ct="meetingRecordingRecordToggle",Nt="meetingRecordingRecordNowButton",Rt="meetingRecordingFilter",It="meetingRecordingFilterOption",Be="meetingRecordingConnectCalendarButton",mt="meetingRecordingConfluenceLoginBannerButton",gt="meetingRecordingConnectConfluenceBanner",Dt="meetingRecordingConfluenceLoginBannerSuccess",vt="meetingNotesOnboardingButton",At="meetingNotesOnboardingTourShown",je="meetingRecordingTabDotIndicator",ft="meetingRecordingTabHoverCard",bt="meeting_bot_controls_stop_button_clicked",We="meeting_bot_controls_pause_button_clicked",He="meeting_bot_controls_resume_button_clicked",Pt="meeting_bot_controls_cancel_button_clicked",Yt="meeting_bot_controls_cancel_confirmation_cancel_button_clicked",Zt="meeting_bot_controls_cancel_confirmation_resume_button_clicked",xe="meeting_bot_controls_show_meeting_notes_button_clicked",Lt="meeting_bot_controls_hide_meeting_notes_button_clicked",we="meeting_bot_controls_manage_on_loom_button_clicked",ht="meeting_bot_controls_finish_button_clicked",yt="meeting_bot_controls_dismiss_button_clicked",Mt="Clicked Resize Cam Bubble",kt="Clicked Close Cam Bubble",Xt="Clicked Filter Chevron",Se="Clicked Modify Avatar",Ke="Clicked Start Recording Button",Gt="Clicked Home Button",Ut="Clicked Edit Profile",Bt="desktop_close_clicked",jt="desktop_effects_menu_clicked",Wt="desktop_submenu_clicked",Ht="Cancel Recording Dialog Confirm",Jt="Cancel Recording Dialog Reject",Fe=[Le,ee,de,ue,Te,he,ye,ie,Oe,pe,Ye,Ze,Xe,Je,Me,ke],Qt=wt=>Fe.includes(wt),xt={[t]:{action:"Timeout",actionSubject:"desktopBinary",eventType:"operational"},[i]:{eventType:"screen"},[a]:{eventType:"screen"},[l]:{action:"Updated",actionSubject:"desktopKeyboardShortcuts",eventType:"track"},[R]:{action:"Launch",actionSubject:"desktop",eventType:"operational"},[u]:{action:"Activated",actionSubject:"desktopMenu",eventType:"operational"},[N]:{eventType:"screen"},[A]:{eventType:"screen"},[P]:{eventType:"screen"},[S]:{eventType:"screen"},[I]:{action:"Quit",actionSubject:"desktop",eventType:"operational"},[b]:{action:"Log Out",actionSubject:"desktop",eventType:"operational"},[E]:{action:"Clicked",actionSubject:"proTag",eventType:"ui"},[U]:{action:"Activated",actionSubject:"desktopConfetti",eventType:"track"},[C]:{action:"User Canceled Failed Retries ",actionSubject:"uploader",eventType:"track"},[K]:{action:"User Attempted Failed Retries",actionSubject:"uploader",eventType:"track"},[H]:{action:"Engaged",actionSubject:"rbacRestriction",eventType:"operational"},[j]:{action:"Rendered",actionSubject:"desktopCameraBubble",eventType:"operational"},[F]:{action:"Critical Error While Recording",actionSubject:"desktopRecorder",eventType:"operational"},[J]:{action:"Stop",actionSubject:"desktopRecorder",eventType:"operational"},[ze]:{action:"Clicked",actionSubject:"desktopCountdown",eventType:"ui"},[V]:{action:"Clicked",actionSubject:"desktopCountdown",eventType:"ui"},[fe]:{action:"Clicked",actionSubject:"desktopCountdown",eventType:"ui"},[be]:{action:"Clicked",actionSubject:"desktopCountdown",eventType:"ui"},[L]:{action:"Capture Shortcut Pressed",actionSubject:"desktopScreenshot",eventType:"ui"},[y]:{action:"Capture Started",actionSubject:"desktopScreenshot",eventType:"operational"},[$]:{action:"Capture Completed",actionSubject:"desktopScreenshot",eventType:"operational"},[ae]:{action:"Capture Failed",actionSubject:"desktopScreenshot",eventType:"operational"},[Re]:{action:"Capture Cancelled",actionSubject:"desktopScreenshot",eventType:"operational"},[Ie]:{action:"Upload Started",actionSubject:"desktopScreenshot",eventType:"operational"},[m]:{action:"Upload Completed",actionSubject:"desktopScreenshot",eventType:"operational"},[M]:{action:"Upload Failed",actionSubject:"desktopScreenshot",eventType:"operational"},[T]:{action:"Keyboard Shortcut Used",actionSubject:"restartRecording",eventType:"ui"},[z]:{action:"Rejected",actionSubject:"desktopRestartPrompt",eventType:"track"},[Q]:{action:"Confirmed",actionSubject:"deskopRestartPrompt",eventType:"track"},[ne]:{action:"Quit During Recording",actionSubject:"desktop",eventType:"operational"},[_e]:{action:"Received",actionSubject:"desktopSrt",eventType:"operational"},[me]:{action:"Shared Auth Successful",actionSubject:"desktop",eventType:"operational"},[ge]:{action:"Initiated",actionSubject:"desktopSharedAuth",eventType:"operational"},[De]:{action:"Triggered",actionSubject:"desktopSharedAuthWelcomeFlow",eventType:"operational"},[ve]:{action:"Start Failed User Restart",actionSubject:"desktopRecording",eventType:"track"},[oe]:{action:"Start Failed User Quit",actionSubject:"desktopRecording",eventType:"track"},[Ae]:{action:"Quick During Recording Confirmed",actionSubject:"desktopRecording",eventType:"track"},[Ee]:{action:"Started",actionSubject:"desktopOnboarding",eventType:"operational"},[q]:{action:"Viewed",actionSubject:"desktopOnboardingStep",eventType:"operational"},[f]:{action:"Requested",actionSubject:"desktopOnboardingPermissions",eventType:"operational"},[ce]:{action:"Received",actionSubject:"desktopNotification",eventType:"operational"},[Pe]:{action:"Clicked",actionSubject:"desktopNotification",eventType:"ui"},[re]:{action:"Permission Prompt Accepted",actionSubject:"desktopNotification",eventType:"track"},[h]:{action:"Notification Click",actionSubject:"desktopNotification",eventType:"ui"},[k]:{action:"Started On Canvas",actionSubject:"desktopRecorder",eventType:"track"},[le]:{action:"Toggled",actionSubject:"speakerNotes",eventType:"track"},[Ve]:{action:"Moved",actionSubject:"speakerNotes",eventType:"track"},[Y]:{action:"Resized",actionSubject:"speakerNotes",eventType:"track"},[Z]:{action:"Successfully Recovered",actionSubject:"videoRecovery",eventType:"operational"},[Le]:{action:"Clicked",actionSubject:"captureModeToggle",eventType:"ui"},[ee]:{action:"Clicked",actionSubject:"selectAreaButton",eventType:"ui"},[de]:{action:"Pressed",actionSubject:"screenshotCaptureShortcut",eventType:"ui"},[ue]:{action:"Entered",actionSubject:"screenshotCaptureMode",eventType:"track"},[Te]:{action:"Cancelled",actionSubject:"screenshotCaptureMode",eventType:"track"},[he]:{action:"Completed",actionSubject:"screenshotCapture",eventType:"track"},[ye]:{action:"Failed",actionSubject:"screenshotCapture",eventType:"track"},[ie]:{action:"Clicked",actionSubject:"screenshotPreviewEditButton",eventType:"ui"},[Oe]:{action:"Dragged",actionSubject:"screenshotPreview",eventType:"ui"},[pe]:{action:"Clicked",actionSubject:"screenshotCopyLinkButton",eventType:"ui"},[Ye]:{action:"Clicked",actionSubject:"screenshotPreviewMenuButton",eventType:"ui"},[Ze]:{action:"Clicked",actionSubject:"screenshotDownloadButton",eventType:"ui"},[Xe]:{action:"Clicked",actionSubject:"screenshotCopyImageButton",eventType:"ui"},[Je]:{action:"Clicked",actionSubject:"screenshotRetakeButton",eventType:"ui"},[Me]:{action:"Clicked",actionSubject:"screenshotDeleteButton",eventType:"ui"},[ke]:{action:"Set",actionSubject:"screenshotShortcut",eventType:"track"},[Qe]:{action:"Clicked",actionSubject:"screenshotsButtonTooltip",eventType:"ui"},[qe]:{action:"Completed",actionSubject:"screenshotsShortcutOnboardingStep",eventType:"track"},[Mt]:{action:"Clicked",actionSubject:"resizeCamBubble",eventType:"ui"},[kt]:{action:"Clicked",actionSubject:"closeCamBubble",eventType:"ui"},[Xt]:{action:"Clicked",actionSubject:"filterChevron",eventType:"ui"},[Se]:{action:"Clicked",actionSubject:"modifyAvatar",eventType:"ui"},[Ke]:{action:"Clicked",actionSubject:"startRecordingButton",eventType:"ui"},[Gt]:{action:"Clicked",actionSubject:"homeButton",eventType:"ui"},[Ut]:{action:"Clicked",actionSubject:"editProfile",eventType:"ui"},[Bt]:{action:"Clicked",actionSubject:"headerCloseButton",eventType:"ui"},[jt]:{action:"Clicked",actionSubject:"effectsMenu",eventType:"ui"},[Wt]:{action:"Clicked",actionSubject:"submenu",eventType:"ui"},[Ht]:{action:"Confirmed",actionSubject:"cancelRecordingDialog",eventType:"track"},[Jt]:{action:"Rejected",actionSubject:"cancelRecordingDialog",eventType:"track"},[tt]:{action:"Clicked",actionSubject:"meetingRecordingsTab",eventType:"ui"},[te]:{action:"Clicked",actionSubject:"meetingRecordingsRecordMeetingButton",eventType:"ui"},[Ue]:{action:"Clicked",actionSubject:"meetingRecordingsRecordNowButton",eventType:"ui"},[nt]:{action:"shown",actionSubject:"meetingRecordingsNudgeNotification",eventType:"track"},[ot]:{action:"clicked",actionSubject:"meetingRecordingsNudgeNotification",eventType:"ui"},[ct]:{action:"clicked",actionSubject:"meetingRecordingsNudgeNotificationButton",eventType:"ui"},[st]:{action:"Shown",actionSubject:"meetingRemindersBanner",eventType:"ui"},[at]:{action:"Clicked",actionSubject:"meetingRemindersBannerAllowButton",eventType:"ui"},[_t]:{action:"Clicked",actionSubject:"meetingRemindersBannerDismissButton",eventType:"ui"},[zt]:{action:"Clicked",actionSubject:"meetingRemindersSettingsToggleOn",eventType:"ui"},[Vt]:{action:"Clicked",actionSubject:"meetingRemindersSettingsToggleOff",eventType:"ui"},[rt]:{action:"opened",actionSubject:"meetingRecordingsNudgeNotificationMenu",eventType:"ui"},[it]:{action:"clicked",actionSubject:"meetingRecordingsNudgeNotificationMenuButton",eventType:"ui"},[bt]:{action:"clicked",actionSubject:"meetingRecordingStopButton",eventType:"ui"},[Pt]:{action:"clicked",actionSubject:"meetingRecordingCancelButton",eventType:"ui"},[We]:{action:"clicked",actionSubject:"meetingRecordingPauseButton",eventType:"ui"},[He]:{action:"clicked",actionSubject:"meetingRecordingResumeButton",eventType:"ui"},[Zt]:{action:"clicked",actionSubject:"meetingRecordingConfirmationModalResumeButton",eventType:"ui"},[Yt]:{action:"clicked",actionSubject:"meetingRecordingConfirmationModalCancelButton",eventType:"ui"},[xe]:{action:"clicked",actionSubject:"meetingRecordingShowMeetingNotesButton",eventType:"ui"},[Lt]:{action:"clicked",actionSubject:"meetingRecordingHideMeetingNotesButton",eventType:"ui"},[we]:{action:"clicked",actionSubject:"meetingRecordingManageOnLoomButton",eventType:"ui"},[ht]:{action:"clicked",actionSubject:"meetingRecordingFinishButton",eventType:"ui"},[yt]:{action:"clicked",actionSubject:"meetingRecordingDismissButton",eventType:"ui"},[Et]:{eventType:"screen"},[lt]:{eventType:"screen"},[dt]:{eventType:"screen"},[ut]:{eventType:"screen"},[Tt]:{eventType:"screen"},[Ot]:{action:"clicked",actionSubject:"meetingRecordingTranscriptButton",eventType:"ui"},[pt]:{action:"clicked",actionSubject:"meetingRecordingMeetingNotesButton",eventType:"ui"},[Ct]:{action:"set",actionSubject:"meetingRecordingRecordToggle",eventType:"ui"},[Nt]:{action:"clicked",actionSubject:"meetingRecordingRecordNowButton",eventType:"ui"},[Rt]:{action:"opened",actionSubject:"meetingRecordingFilter",eventType:"ui"},[It]:{action:"clicked",actionSubject:"meetingRecordingFilterOption",eventType:"ui"},[Be]:{action:"clicked",actionSubject:"meetingRecordingConnectCalendarButton",eventType:"ui"},[gt]:{action:"shown",actionSubject:"meetingRecordingConnectConfluenceBanner",eventType:"track"},[Dt]:{action:"success",actionSubject:"confluenceLogin",eventType:"track"},[St]:{action:"clicked",actionSubject:"meetingRecordingJoinMeetingButton",eventType:"ui"},[mt]:{action:"clicked",actionSubject:"confluenceLoginBanner",eventType:"ui"},[vt]:{action:"clicked",actionSubject:"meetingRecordingOnboardingTour",eventType:"ui"},[At]:{action:"shown",actionSubject:"meetingRecordingOnboardingTour",eventType:"track"},[je]:{action:"shown",actionSubject:"meetingRecordingTabDotIndicator",eventType:"track"},[ft]:{action:"shown",actionSubject:"meetingRecordingTabHoverCard",eventType:"track"}}},394473:(o,s,n)=>{n.d(s,{FA:()=>R,o7:()=>I});var t=n(172298),i=n.n(t),a=n(510453);let l="renderer";const R=E=>{E&&(l=E)},u=(E="info",U)=>(C,K)=>{const H={};K&&Object.entries(K).forEach(([j,F])=>{H[j]=N(F)}),t.ipcRenderer.send(a.u,{logLevel:E,message:C,context:H,windowName:U})};function N(E){return typeof E!="object"?E:A(E)?{message:E.message,name:E.name}:JSON.parse(JSON.stringify(E))}function A(E){return typeof E.message=="string"&&typeof E.name=="string"}const P=u("info",l),B=u("warn",l),S=u("error",l),I=u("debug",l),b=E=>({info:u("info",E),warn:u("warn",E),error:u("error",E),debug:u("debug",E)})},36048:(o,s,n)=>{n.d(s,{m:()=>u});var t=n(394473),i=n(172298),a=n.n(i),l=n(881863),R=n(826565);function u(N,A,P=!0){(0,t.o7)("Opening external url"),i.shell.openExternal(A).then(()=>{P&&N((0,R.r)(l.o.Minimized))})}},881863:(o,s,n)=>{n.d(s,{o:()=>t});var t=(i=>(i.LoggedOut="logged-out",i.Minimized="minimized",i.Idle="idle",i.IdleNoScreenshotFtux="idle_no_screenshot_ftux",i.ContextualOnboarding="contextual-onboarding",i.Countdown="countdown",i.Recording="recording",i.Onboarding="onboarding",i.Cropping="cropping",i.Meetings="meetings",i.MeetingsV2="meetings-v2",i.MeetingNotes="meeting-notes",i.MeetingOnboarding="meeting-onboarding",i.SelectingScreenshot="selecting-screenshot",i.MenuSelectScreenshot="menu-select-screenshot",i.ScreenshotShortcutSetup="screenshot-shortcut-setup",i.ScreenshotShortcutSetupCompleted="screenshot-shortcut-setup-completed",i.ScreenshotTryItFtux="screenshot-try-it-ftux",i))(t||{})},826565:(o,s,n)=>{n.d(s,{r:()=>i});var t=n(565327);const i=(0,t.PH)("maestro/set-state")},898228:(o,s,n)=>{n.d(s,{Lc:()=>N,xB:()=>P,Ag:()=>B,AX:()=>S,L4:()=>I,rl:()=>b,eM:()=>E,RD:()=>j});var t=Object.defineProperty,i=Object.getOwnPropertySymbols,a=Object.prototype.hasOwnProperty,l=Object.prototype.propertyIsEnumerable,R=(g,L,y)=>L in g?t(g,L,{enumerable:!0,configurable:!0,writable:!0,value:y}):g[L]=y,u=(g,L)=>{for(var y in L||(L={}))a.call(L,y)&&R(g,y,L[y]);if(i)for(var y of i(L))l.call(L,y)&&R(g,y,L[y]);return g};const N="update-bot-recording-state",A="update-bot-meeting-info",P="update-in-collapsed-view",B="update-is-overflow-menu-open",S="update-show-join-button",I="update-meeting-guids",b="reset-bot-controls",E="update-hide-for-transform",U=()=>({type:b}),C=(g,L,y,$)=>({type:N,payload:u(u({botId:g,recordingState:L},y&&{actingUser:y}),$&&{videoId:$})}),K=g=>({type:P,payload:{inCollapsedView:g}}),H=g=>({type:B,payload:{isOverflowMenuOpen:g}}),j=g=>({type:S,payload:{showJoinButton:g}}),F=g=>({type:I,payload:{meetingGuids:g}}),J=g=>({type:E,payload:{hideForTransform:g}})},70002:(o,s,n)=>{n.d(s,{q8:()=>i,kb:()=>a,N1:()=>l,pI:()=>u,TZ:()=>N,RA:()=>A,A6:()=>P});var t=n(969178);const i=(0,t.rp)("change-recording-state"),a=(0,t.rp)("hide-meeting-bot-controls"),l=(0,t.rp)("open-meeting-recording-link"),R=(0,t.rp)("open-cancel-meeting-recording-confirmation"),u=(0,t.rp)("log-note-controls-discrepancy"),N=(0,t.rp)("show-bot-controls-after-resize"),A=(0,t.rp)("show-overflow-menu"),P=(0,t.rp)("hide-overflow-menu")},65629:(o,s,n)=>{n.d(s,{Vk:()=>t,m3:()=>a,A_:()=>l,Wp:()=>R,dD:()=>u});const t="all";var i=(C=>(C.CancelRecording="cancelRecording",C.PauseRecording="pauseRecording",C.ResumeRecording="resumeRecording",C.StopRecording="stopRecording",C.ParticipantsLeft="participantsLeft",C))(i||{}),a=(C=>(C.IDLE="IDLE",C.PAUSING="PAUSING",C.PAUSED="PAUSED",C.STOPPING="STOPPING",C.STOPPED="STOPPED",C.CANCELLING="CANCELLING",C.CANCELLED="CANCELLED",C.RESUMING="RESUMING",C.RECORDING="RECORDING",C.PARTICIPANTS_LEFT="PARTICIPANTS_LEFT",C))(a||{});const l=new Set(["STOPPED","CANCELLED","PARTICIPANTS_LEFT"]),R=new Set(["PAUSING","STOPPING","CANCELLING","RESUMING"]),u=new Set(["PAUSED","RESUMING","CANCELLING"]),N=null,A=null,P=5,B=2e3,S=new Set(["PAUSED","RECORDING"]),I=new Set([...S,"PAUSING","RESUMING"]),b=new Set([...I,"STOPPING","CANCELLING"]),E=new Set([...b,"STOPPING","CANCELLING"]);var U=(C=>(C.PAUSE="pause",C.RESUME="resume",C.STOP="stop",C.CANCEL="cancel",C))(U||{})},330075:(o,s,n)=>{n.d(s,{FM:()=>l});var t=n(969178);const i=(0,t.rp)("show-meeting-notes-window"),a=(0,t.rp)("collapse-meeting-notes-window"),l=(0,t.rp)("expand-meeting-notes-window"),R=(0,t.rp)("change-meeting-notes-tab"),u=(0,t.rp)("hide-meeting-notes-window"),N=(0,t.rp)("show-meeting-index-view")},695610:(o,s,n)=>{n.d(s,{lL:()=>A,T0:()=>H,r2:()=>j,CQ:()=>F,ED:()=>J,z9:()=>g,Fl:()=>$,df:()=>T,Ao:()=>z,zn:()=>Ee,YO:()=>q,yf:()=>f});var t=n(230606),i=n(372259);const a=480,l=640,R=610,u=720,N=10,A=10,P=8,B=60+A,S=100+A,I=0,b=200,E=i.jK*2,U=i.jK+i.D9,C=a+E+N,K=l+U,H=124,j=184,F=200,J=260,g=300,L=8,y=160,$=36,ae=400,Re=400,Ie="meetingGuid",m="meetingRendererIpc",M="electronToLoomSurfaceIpc",T=25,z=2,Q=256,ne=30,_e=7,me=7,ge=null,De=292,ve=280,oe=448,Ae=400,ze=!0,V=230,fe=146,be=200,Ee=20,q=100,f=100,ce=20,Pe=30,re=(h,k)=>`https://${LOOM_URI}/confluence-meeting-notes?meeting=${h.calendarMeetingGuid}&workspace=${k}&amn-referral-source=loom-desktop`},856555:(o,s,n)=>{o.exports=n.p+"assets/img/icons/expand.svg"},995346:(o,s,n)=>{o.exports=n.p+"assets/img/icons/google-meet.svg"},301753:(o,s,n)=>{o.exports=n.p+"assets/img/icons/microsoft-teams.svg"},997753:(o,s,n)=>{o.exports=n.p+"assets/img/icons/zoom.svg"},439491:o=>{o.exports=require("assert")},706113:o=>{o.exports=require("crypto")},172298:o=>{o.exports=require("electron")},582361:o=>{o.exports=require("events")},657147:o=>{o.exports=require("fs")},113685:o=>{o.exports=require("http")},795687:o=>{o.exports=require("https")},822037:o=>{o.exports=require("os")},371017:o=>{o.exports=require("path")},863477:o=>{o.exports=require("querystring")},257310:o=>{o.exports=require("url")},473837:o=>{o.exports=require("util")}},$e={};function d(o){var s=$e[o];if(s!==void 0)return s.exports;var n=$e[o]={id:o,loaded:!1,exports:{}};return Kt[o].call(n.exports,n,n.exports,d),n.loaded=!0,n.exports}d.m=Kt,d.c=$e,(()=>{var o=[];d.O=(s,n,t,i)=>{if(n){i=i||0;for(var a=o.length;a>0&&o[a-1][2]>i;a--)o[a]=o[a-1];o[a]=[n,t,i];return}for(var l=1/0,a=0;a<o.length;a++){for(var[n,t,i]=o[a],R=!0,u=0;u<n.length;u++)(i&!1||l>=i)&&Object.keys(d.O).every(I=>d.O[I](n[u]))?n.splice(u--,1):(R=!1,i<l&&(l=i));if(R){o.splice(a--,1);var N=t();N!==void 0&&(s=N)}}return s}})(),d.n=o=>{var s=o&&o.__esModule?()=>o.default:()=>o;return d.d(s,{a:s}),s},(()=>{var o=Object.getPrototypeOf?n=>Object.getPrototypeOf(n):n=>n.__proto__,s;d.t=function(n,t){if(t&1&&(n=this(n)),t&8||typeof n=="object"&&n&&(t&4&&n.__esModule||t&16&&typeof n.then=="function"))return n;var i=Object.create(null);d.r(i);var a={};s=s||[null,o({}),o([]),o(o)];for(var l=t&2&&n;typeof l=="object"&&!~s.indexOf(l);l=o(l))Object.getOwnPropertyNames(l).forEach(R=>a[R]=()=>n[R]);return a.default=()=>n,d.d(i,a),i}})(),d.d=(o,s)=>{for(var n in s)d.o(s,n)&&!d.o(o,n)&&Object.defineProperty(o,n,{enumerable:!0,get:s[n]})},d.h=()=>"55e5c6a40d444554bfb1",d.hmd=o=>(o=Object.create(o),o.children||(o.children=[]),Object.defineProperty(o,"exports",{enumerable:!0,set:()=>{throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+o.id)}}),o),d.o=(o,s)=>Object.prototype.hasOwnProperty.call(o,s),d.r=o=>{typeof Symbol<"u"&&Symbol.toStringTag&&Object.defineProperty(o,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(o,"__esModule",{value:!0})},d.nmd=o=>(o.paths=[],o.children||(o.children=[]),o),d.p="./",(()=>{var o={18:0};d.O.j=t=>o[t]===0;var s=(t,i)=>{var[a,l,R]=i,u,N,A=0;if(a.some(B=>o[B]!==0)){for(u in l)d.o(l,u)&&(d.m[u]=l[u]);if(R)var P=R(d)}for(t&&t(i);A<a.length;A++)N=a[A],d.o(o,N)&&o[N]&&o[N][0](),o[a[A]]=0;return d.O(P)},n=global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[];n.forEach(s.bind(null,0)),n.push=s.bind(null,n.push.bind(n))})(),d.O(void 0,[592,6491,8588,719,3823,793,6494,5800,403,5466,8058,9073,5942,1404,3655,5878,6369,3571,6375],()=>d(d.s=903679)),d.O(void 0,[592,6491,8588,719,3823,793,6494,5800,403,5466,8058,9073,5942,1404,3655,5878,6369,3571,6375],()=>d(d.s=439900)),d.O(void 0,[592,6491,8588,719,3823,793,6494,5800,403,5466,8058,9073,5942,1404,3655,5878,6369,3571,6375],()=>d(d.s=639542));var Ft=d.O(void 0,[592,6491,8588,719,3823,793,6494,5800,403,5466,8058,9073,5942,1404,3655,5878,6369,3571,6375],()=>d(d.s=194383));Ft=d.O(Ft)})();

//# sourceMappingURL=meeting_bot_controls.js.map