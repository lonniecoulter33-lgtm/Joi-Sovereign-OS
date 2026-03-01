"use strict";(global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[]).push([[5532],{175532:(_,u,e)=>{e.d(u,{h:()=>se});var o=e(992671),r=e(974144),s=e(183780),d=e(808768),n=e(275271),v=e(591705),O=e(416628),E=e(931675),g=e(201038),h=e(873044),a=e(887386),T=e(631915),p=e(744081),C=e(523179),P=e(105500),y=e(95376),A=e(450630),i=e(625507),$=e(670266),N=e(490999),B=e(185335),F=e(756879),U=e(163224),G=e(443934),L=e(257728),V=e(283297);const z=({icon:t,showIndicator:l})=>{const f=(0,n.useRef)(!1);return(0,n.useEffect)(()=>{l&&!f.current&&((0,V.j)(C.ZO),f.current=!0)},[l]),l?n.createElement(s.z$D,null,t):t},H=A.iv`
  background-color: var(--lns-color-background);
  box-shadow: 0px 2px 8px 0px rgba(0, 0, 0, 0.1);
`,w="#bf63f3",Z=o.Z.button`
  appearance: none;
  padding: 0
    calc(
      ${({isMeetingRecordingsV2Enabled:t})=>t?1.5:2.5} * var(--lns-unit, 8px)
    );
  font: inherit;
  text-decoration: none;
  transition:
    0.6s background,
    0.6s border-color,
    0.6s box-shadow;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  white-space: nowrap;
  font-weight: var(--lns-fontWeight-bold);
  display: inline-flex;
  height: calc(5 * var(--lns-unit, 8px));
  min-width: calc(6 * var(--lns-unit, 8px));
  font-size: var(--lns-fontSize-large);
  line-height: var(--lns-lineHeight-large);
  cursor: pointer;
  background: transparent;
  background-position: left;
  background-size: 125%;
  color: var(--lns-color-body);
  border: 0;
  background-color: transparent;
  border-radius: var(--lns-radius-175);

  ${t=>!t.isSelected&&A.iv`
      &:hover {
        background-color: var(--lns-color-backgroundHover);
      }
    `}

  ${t=>t.isBeta&&!t.isSelected&&A.iv`
      &:hover {
        box-shadow: inset 0 0 0 1px ${w};
      }
    `}

  ${t=>t.isSelected&&H}
`,k=t=>{switch(t){case i.s.screenshot:return"Screenshot";case i.s.meetingsV2:return"Meetings - BETA";default:return"Record"}},I=({page:t,icon:l,disabled:f})=>{const c=(0,G.I0)(),D=(0,$.Wo)(),{onActivePageSelect:M,trackEvent:b}=(0,g.z3)(),m=t===D,R=t===i.s.meetingsV2,{nudge:x,contextualOnboarding:K}=(0,F.f)(),re=(0,n.useCallback)(()=>{m||(t!==i.s.meetingsV2&&b(C.ut,{capture_mode:t===i.s.normal?"video":"screenshot"}),t===i.s.meetingsV2&&K?(c((0,B.eY)(!1)),M(t),c((0,U.L)(L.t.MEETING_NOTES)),c((0,U._$)())):(t===i.s.meetingsV2&&x&&c((0,B.eY)(!1)),M(t)))},[m,M,b,t,K,x,c]),ae=(0,n.useCallback)(()=>{t===i.s.meetingsV2&&x&&!m&&c((0,B.RI)(L.t.MEETING_NOTES))},[t,x,c,m]),le=(0,n.useCallback)(()=>{t===i.s.meetingsV2&&x&&!m&&c((0,B.eY)())},[t,x,c,m]),ce=k(t),de=(0,N.Hc)(),ie=x&&t===i.s.meetingsV2&&!m;return n.createElement(s.ua7,{placement:"bottomCenter",content:ce},n.createElement(Z,{isSelected:m,isBeta:R,id:`page-${t}`,onClick:re,onMouseEnter:ae,onMouseLeave:le,"data-isselected":m,"data-testid":"action-button",disabled:f,isMeetingRecordingsV2Enabled:de},n.createElement(z,{icon:l,showIndicator:ie})))};var X=e(382456);const j=o.Z.div`
  width: fit-content;
  display: flex;
  padding-left: var(--lns-space-xsmall);
  padding-right: var(--lns-space-xsmall);
  height: ${E.QA};
  border-radius: var(--lns-radius-200);
  background-color: var(--lns-color-backgroundHover);
  box-shadow: inset 0px 1px 8px 0px rgba(0, 0, 0, 0.1);
`;function S({disabled:t=!1}){const l=(0,N.Hc)();return n.createElement(j,{id:"toggleContainer"},n.createElement(s.ggW,{gap:"xsmall"},n.createElement(I,{disabled:t,page:i.s.normal,icon:n.createElement(y.x,null)}),n.createElement(I,{disabled:t,page:i.s.screenshot,icon:n.createElement(P.M,null)}),l&&n.createElement(I,{disabled:t,page:i.s.meetingsV2,icon:n.createElement(X.c,null)})))}const Y=({onClose:t})=>{const{onClosePreRecordingPanel:l,trackEvent:f}=(0,g.z3)(),c=()=>{f(C.xz),t?t():l()};return n.createElement(s.hU,{onClick:c,icon:n.createElement(T.G,null),altText:"Close"})},J=()=>{const{onMyVideosClick:t}=(0,g.z3)();return n.createElement(s.hU,{onClick:t,icon:n.createElement("img",{src:p}),altText:"Loom"})},Q=({minimal:t=!1,onClose:l,navigationDisabled:f=!1,containerIsScrolled:c=!1,isMeetings:D=!1})=>{const M=()=>t?"0":D?"24px":"20px",b=t?1:3,m=D?2:0,R=c?"var(--lns-color-grey2)":"transparent";return n.createElement(h.h2,null,n.createElement(s.W20,{width:"100%",paddingX:M(),paddingTop:b,borderWidth:"1px",borderSide:"bottom",borderColor:R,paddingBottom:m},n.createElement(s.ggW,{width:"100%",autoFlow:"column",justifyContent:"space-between"},!t&&n.createElement(J,null),!t&&n.createElement(S,{disabled:f}),n.createElement(Y,{onClose:l}))))};var W=e(960922);const q=o.Z.div`
  width: 100%;
  display: flex;
  ${t=>t.containerIsScrolled&&"border-bottom: 1px var(--lns-color-grey2) solid;"}
  justify-content: space-between;
  ${t=>!t.minimal&&"padding: 0 20px;"}
  ${r.is.windows?"":"padding-top: calc(2 * var(--lns-unit));"}
  ${t=>!r.is.windows&&!t.minimal?"padding-top: calc(3 * var(--lns-unit));":""}
  ${t=>t.isMeetings&&(r.is.windows?"padding-bottom: calc(2 * var(--lns-unit));":"padding-bottom: calc(3 * var(--lns-unit));")}
  }
`,ee=o.Z.div`
  display: grid;
  gap: 2px;
  align-self: flex-end;
  grid-auto-flow: column;
`,te=o.Z.button`
  width: 0;
  height: 0;
  border-width: 0;
`,ne=o.Z.div`
  height: ${E.QA};
`;function oe({onClose:t,minimal:l}){return r.is.windows?l?null:n.createElement(W.o,{onClose:t}):n.createElement(W.o,{onClose:t})}const se=({minimal:t=!1,onClose:l,isPermissionModal:f=!1,navigationDisabled:c=!1,containerIsScrolled:D=!1,isMeetings:M=!1})=>{const{onMyVideosClick:b}=(0,g.z3)(),m=x=>{x.preventDefault(),x.target===x.currentTarget&&b()};return(0,v.TW)(O.SS.LOOM_CLIENTS_CLOSE_BUTTON_ON_THE_RIGHT,!1)?n.createElement(Q,{minimal:t,onClose:l,isPermissionModal:f,navigationDisabled:c,containerIsScrolled:D,isMeetings:M}):n.createElement(n.Fragment,null,r.is.windows&&n.createElement(a.P,{minimal:t,onClose:l,isPermissionModal:f}),n.createElement(h.rP,null,n.createElement(q,{minimal:t,isMeetings:M,containerIsScrolled:D},n.createElement(oe,{minimal:t,onClose:l}),!t&&n.createElement(S,{disabled:c}),!t&&n.createElement(ee,null,n.createElement(te,null),n.createElement(ne,null,n.createElement(s.xMy,{alignment:"center"},n.createElement(s.ua7,{content:"Loom.com",placement:"bottomCenter",delay:"long"},n.createElement(s.hU,{onClick:m,altText:"My Videos (loom.com)",icon:n.createElement(d.E,null),"data-id":"home-btn"}))))))))}},960922:(_,u,e)=>{e.d(u,{o:()=>T});var o=e(992671),r=e(183780),s=e(631915),d=e(275271),n=e(974144),v=e.n(n),O=e(201038),E=e(42022),g=e(670266),h=e(523179);const a=o.Z.button`
  ${p=>p.hide&&"opacity: 0"};
  border: none;
  background: none;
  padding-right: 10px;

  &:hover {
    cursor: pointer;
  }
`,T=({onClose:p})=>{const{onClosePreRecordingPanel:C,trackEvent:P}=(0,O.z3)(),y=(0,g.tp)(),A=(0,g.iJ)(),i=()=>{P(h.xz),p?p():C()};return d.createElement(a,{disabled:A===E.o1&&!y,onClick:i,hide:n.is.windows},d.createElement(r.JO$,{size:3,icon:d.createElement(s.G,null)}))}},887386:(_,u,e)=>{e.d(u,{P:()=>h});var o=e(275271),r=e(992671),s=e(450630),d=e(873044),n=e(201038);const v=r.Z.div`
  width: 100%;
  height: 32px;
  justify-content: space-between;
  display: flex;
  padding: 10px 20px 40px;
  background-color: white;
  border-top-right-radius: 32px;
  border-top-left-radius: 32px;

  ${a=>a.minimal&&s.iv`
      padding: 0 20px 30px 0;
    `}
`,O=r.Z.div`
  position: relative;
  top: -10px;
  right: -20px;
`,E=r.Z.button`
  font-family: segoui, sans-serif;
  background: none;
  border: none;
  opacity: 1;
  height: 42px;
  padding-top: 6px;
  width: 48px;
  cursor: pointer;
  -webkit-app-region: no-drag;

  ${a=>a.closeBtn&&s.iv`
      border-top-right-radius: 32px;
      padding-right: 6px;
    `}

  ${a=>a.isPermissionModal&&s.iv`
      margin-top: 6px;
    `}

  &:hover {
    background-color: var(--lns-color-grey3);

    ${a=>a.closeBtn&&s.iv`
        background-color: #e81123;
        color: white;
      `}
  }
`,g=r.Z.div`
  height: 48px;
  padding-top: 5px;
`;function h({minimal:a=!1,onClose:T,isPermissionModal:p=!1}){const{onClosePreRecordingPanel:C}=(0,n.z3)();return o.createElement(d.h2,null,o.createElement(v,{minimal:a},o.createElement(g,null,"Loom"),o.createElement(O,null,o.createElement(E,{closeBtn:!0,isPermissionModal:p,onClick:()=>T?T():C()},o.createElement("span",null,"\u2716")))))}},163224:(_,u,e)=>{e.d(u,{hr:()=>o,so:()=>r,dg:()=>d,Qp:()=>n,QN:()=>v,h0:()=>O,L:()=>E,_$:()=>h});const o="show-contextual-onboarding",r="close-contextual-onboarding",s="update-seen-contextual-onboarding",d="set-contextual-onboarding-feature",n="set-contextual-onboarding-step",v="set-contextual-onboarding-display-bounds",O="reset-contextual-onboarding",E=P=>({type:d,payload:P}),g=P=>({type:n,payload:P}),h=()=>({type:o}),a=()=>({type:r}),T=()=>({type:s}),p=P=>({type:v,payload:P}),C=()=>({type:O})},185335:(_,u,e)=>{e.d(u,{eE:()=>o,Jg:()=>r,RI:()=>s,eY:()=>d});const o="open-feature-nudge",r="close-feature-nudge",s=n=>({type:o,payload:n}),d=(n=!0)=>({type:r,payload:n})},257728:(_,u,e)=>{e.d(u,{t:()=>s,O_:()=>n,Ji:()=>v,U6:()=>O});var o=e(450630),r=e(284558),s=(E=>(E.MEETING_NOTES="meeting-notes",E))(s||{});const d={["meeting-notes"]:r._v},n={nudge:{fadeIn:{seconds:.15,milliseconds:150},fadeOut:{seconds:.15,milliseconds:150}},contextualOnboarding:{fadeIn:{seconds:.4,milliseconds:400},fadeOut:{seconds:.4,milliseconds:400}}},v=o.F4`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`,O=o.F4`
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
`},756879:(_,u,e)=>{e.d(u,{f:()=>O});var o=e(591705),r=e(416628),s=e(59876),d=e(924630),n=e(443934),v=e(950117);function O(){var E;const g=(0,o.TW)(r.SS.MEETING_NOTES_ONBOARDING,!1),h=(0,d.II)(),a=(E=(0,s.u9)(h??""))!=null?E:!1,T=(0,n.v9)(C=>C.preRecordingPanel.has_completed_meeting_notes_onboarding),p=(0,v.fz)().length>0;return{nudge:g&&a&&!T,contextualOnboarding:g&&a&&!T&&p}}},744081:(_,u,e)=>{_.exports=e.p+"assets/img/new-brand-logo.svg"}}]);

//# sourceMappingURL=5532.js.map