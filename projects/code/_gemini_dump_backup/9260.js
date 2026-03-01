"use strict";(global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[]).push([[9260],{175532:(T,u,e)=>{e.d(u,{h:()=>re});var r=e(992671),i=e(974144),s=e(183780),c=e(808768),n=e(275271),v=e(591705),h=e(416628),g=e(931675),l=e(201038),O=e(873044),a=e(887386),o=e(631915),d=e(744081),p=e(523179),P=e(105500),N=e(95376),b=e(450630),f=e(625507),w=e(670266),B=e(490999),y=e(185335),K=e(756879),U=e(163224),$=e(443934),S=e(257728),G=e(283297);const F=({icon:t,showIndicator:E})=>{const M=(0,n.useRef)(!1);return(0,n.useEffect)(()=>{E&&!M.current&&((0,G.j)(p.ZO),M.current=!0)},[E]),E?n.createElement(s.z$D,null,t):t},V=b.iv`
  background-color: var(--lns-color-background);
  box-shadow: 0px 2px 8px 0px rgba(0, 0, 0, 0.1);
`,H="#bf63f3",z=r.Z.button`
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

  ${t=>!t.isSelected&&b.iv`
      &:hover {
        background-color: var(--lns-color-backgroundHover);
      }
    `}

  ${t=>t.isBeta&&!t.isSelected&&b.iv`
      &:hover {
        box-shadow: inset 0 0 0 1px ${H};
      }
    `}

  ${t=>t.isSelected&&V}
`,Z=t=>{switch(t){case f.s.screenshot:return"Screenshot";case f.s.meetingsV2:return"Meetings - BETA";default:return"Record"}},R=({page:t,icon:E,disabled:M})=>{const m=(0,$.I0)(),D=(0,w.Wo)(),{onActivePageSelect:C,trackEvent:I}=(0,l.z3)(),_=t===D,A=t===f.s.meetingsV2,{nudge:x,contextualOnboarding:k}=(0,K.f)(),se=(0,n.useCallback)(()=>{_||(t!==f.s.meetingsV2&&I(p.ut,{capture_mode:t===f.s.normal?"video":"screenshot"}),t===f.s.meetingsV2&&k?(m((0,y.eY)(!1)),C(t),m((0,U.L)(S.t.MEETING_NOTES)),m((0,U._$)())):(t===f.s.meetingsV2&&x&&m((0,y.eY)(!1)),C(t)))},[_,C,I,t,k,x,m]),ae=(0,n.useCallback)(()=>{t===f.s.meetingsV2&&x&&!_&&m((0,y.RI)(S.t.MEETING_NOTES))},[t,x,m,_]),ie=(0,n.useCallback)(()=>{t===f.s.meetingsV2&&x&&!_&&m((0,y.eY)())},[t,x,m,_]),de=Z(t),le=(0,B.Hc)(),ce=x&&t===f.s.meetingsV2&&!_;return n.createElement(s.ua7,{placement:"bottomCenter",content:de},n.createElement(z,{isSelected:_,isBeta:A,id:`page-${t}`,onClick:se,onMouseEnter:ae,onMouseLeave:ie,"data-isselected":_,"data-testid":"action-button",disabled:M,isMeetingRecordingsV2Enabled:le},n.createElement(F,{icon:E,showIndicator:ce})))};var X=e(382456);const j=r.Z.div`
  width: fit-content;
  display: flex;
  padding-left: var(--lns-space-xsmall);
  padding-right: var(--lns-space-xsmall);
  height: ${g.QA};
  border-radius: var(--lns-radius-200);
  background-color: var(--lns-color-backgroundHover);
  box-shadow: inset 0px 1px 8px 0px rgba(0, 0, 0, 0.1);
`;function L({disabled:t=!1}){const E=(0,B.Hc)();return n.createElement(j,{id:"toggleContainer"},n.createElement(s.ggW,{gap:"xsmall"},n.createElement(R,{disabled:t,page:f.s.normal,icon:n.createElement(N.x,null)}),n.createElement(R,{disabled:t,page:f.s.screenshot,icon:n.createElement(P.M,null)}),E&&n.createElement(R,{disabled:t,page:f.s.meetingsV2,icon:n.createElement(X.c,null)})))}const Y=({onClose:t})=>{const{onClosePreRecordingPanel:E,trackEvent:M}=(0,l.z3)(),m=()=>{M(p.xz),t?t():E()};return n.createElement(s.hU,{onClick:m,icon:n.createElement(o.G,null),altText:"Close"})},J=()=>{const{onMyVideosClick:t}=(0,l.z3)();return n.createElement(s.hU,{onClick:t,icon:n.createElement("img",{src:d}),altText:"Loom"})},Q=({minimal:t=!1,onClose:E,navigationDisabled:M=!1,containerIsScrolled:m=!1,isMeetings:D=!1})=>{const C=()=>t?"0":D?"24px":"20px",I=t?1:3,_=D?2:0,A=m?"var(--lns-color-grey2)":"transparent";return n.createElement(O.h2,null,n.createElement(s.W20,{width:"100%",paddingX:C(),paddingTop:I,borderWidth:"1px",borderSide:"bottom",borderColor:A,paddingBottom:_},n.createElement(s.ggW,{width:"100%",autoFlow:"column",justifyContent:"space-between"},!t&&n.createElement(J,null),!t&&n.createElement(L,{disabled:M}),n.createElement(Y,{onClose:E}))))};var W=e(960922);const q=r.Z.div`
  width: 100%;
  display: flex;
  ${t=>t.containerIsScrolled&&"border-bottom: 1px var(--lns-color-grey2) solid;"}
  justify-content: space-between;
  ${t=>!t.minimal&&"padding: 0 20px;"}
  ${i.is.windows?"":"padding-top: calc(2 * var(--lns-unit));"}
  ${t=>!i.is.windows&&!t.minimal?"padding-top: calc(3 * var(--lns-unit));":""}
  ${t=>t.isMeetings&&(i.is.windows?"padding-bottom: calc(2 * var(--lns-unit));":"padding-bottom: calc(3 * var(--lns-unit));")}
  }
`,ee=r.Z.div`
  display: grid;
  gap: 2px;
  align-self: flex-end;
  grid-auto-flow: column;
`,te=r.Z.button`
  width: 0;
  height: 0;
  border-width: 0;
`,ne=r.Z.div`
  height: ${g.QA};
`;function oe({onClose:t,minimal:E}){return i.is.windows?E?null:n.createElement(W.o,{onClose:t}):n.createElement(W.o,{onClose:t})}const re=({minimal:t=!1,onClose:E,isPermissionModal:M=!1,navigationDisabled:m=!1,containerIsScrolled:D=!1,isMeetings:C=!1})=>{const{onMyVideosClick:I}=(0,l.z3)(),_=x=>{x.preventDefault(),x.target===x.currentTarget&&I()};return(0,v.TW)(h.SS.LOOM_CLIENTS_CLOSE_BUTTON_ON_THE_RIGHT,!1)?n.createElement(Q,{minimal:t,onClose:E,isPermissionModal:M,navigationDisabled:m,containerIsScrolled:D,isMeetings:C}):n.createElement(n.Fragment,null,i.is.windows&&n.createElement(a.P,{minimal:t,onClose:E,isPermissionModal:M}),n.createElement(O.rP,null,n.createElement(q,{minimal:t,isMeetings:C,containerIsScrolled:D},n.createElement(oe,{minimal:t,onClose:E}),!t&&n.createElement(L,{disabled:m}),!t&&n.createElement(ee,null,n.createElement(te,null),n.createElement(ne,null,n.createElement(s.xMy,{alignment:"center"},n.createElement(s.ua7,{content:"Loom.com",placement:"bottomCenter",delay:"long"},n.createElement(s.hU,{onClick:_,altText:"My Videos (loom.com)",icon:n.createElement(c.E,null),"data-id":"home-btn"}))))))))}},960922:(T,u,e)=>{e.d(u,{o:()=>o});var r=e(992671),i=e(183780),s=e(631915),c=e(275271),n=e(974144),v=e.n(n),h=e(201038),g=e(42022),l=e(670266),O=e(523179);const a=r.Z.button`
  ${d=>d.hide&&"opacity: 0"};
  border: none;
  background: none;
  padding-right: 10px;

  &:hover {
    cursor: pointer;
  }
`,o=({onClose:d})=>{const{onClosePreRecordingPanel:p,trackEvent:P}=(0,h.z3)(),N=(0,l.tp)(),b=(0,l.iJ)(),f=()=>{P(O.xz),d?d():p()};return c.createElement(a,{disabled:b===g.o1&&!N,onClick:f,hide:n.is.windows},c.createElement(i.JO$,{size:3,icon:c.createElement(s.G,null)}))}},887386:(T,u,e)=>{e.d(u,{P:()=>O});var r=e(275271),i=e(992671),s=e(450630),c=e(873044),n=e(201038);const v=i.Z.div`
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
`,h=i.Z.div`
  position: relative;
  top: -10px;
  right: -20px;
`,g=i.Z.button`
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
`,l=i.Z.div`
  height: 48px;
  padding-top: 5px;
`;function O({minimal:a=!1,onClose:o,isPermissionModal:d=!1}){const{onClosePreRecordingPanel:p}=(0,n.z3)();return r.createElement(c.h2,null,r.createElement(v,{minimal:a},r.createElement(l,null,"Loom"),r.createElement(h,null,r.createElement(g,{closeBtn:!0,isPermissionModal:d,onClick:()=>o?o():p()},r.createElement("span",null,"\u2716")))))}},163224:(T,u,e)=>{e.d(u,{hr:()=>r,so:()=>i,dg:()=>c,Qp:()=>n,QN:()=>v,h0:()=>h,L:()=>g,_$:()=>O});const r="show-contextual-onboarding",i="close-contextual-onboarding",s="update-seen-contextual-onboarding",c="set-contextual-onboarding-feature",n="set-contextual-onboarding-step",v="set-contextual-onboarding-display-bounds",h="reset-contextual-onboarding",g=P=>({type:c,payload:P}),l=P=>({type:n,payload:P}),O=()=>({type:r}),a=()=>({type:i}),o=()=>({type:s}),d=P=>({type:v,payload:P}),p=()=>({type:h})},185335:(T,u,e)=>{e.d(u,{eE:()=>r,Jg:()=>i,RI:()=>s,eY:()=>c});const r="open-feature-nudge",i="close-feature-nudge",s=n=>({type:r,payload:n}),c=(n=!0)=>({type:i,payload:n})},257728:(T,u,e)=>{e.d(u,{t:()=>s,O_:()=>n,Ji:()=>v,U6:()=>h});var r=e(450630),i=e(284558),s=(g=>(g.MEETING_NOTES="meeting-notes",g))(s||{});const c={["meeting-notes"]:i._v},n={nudge:{fadeIn:{seconds:.15,milliseconds:150},fadeOut:{seconds:.15,milliseconds:150}},contextualOnboarding:{fadeIn:{seconds:.4,milliseconds:400},fadeOut:{seconds:.4,milliseconds:400}}},v=r.F4`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`,h=r.F4`
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
`},422607:(T,u,e)=>{},879715:(T,u,e)=>{e.d(u,{L:()=>l});var r=e(706113),i=e.n(r),s=Object.defineProperty,c=Object.getOwnPropertySymbols,n=Object.prototype.hasOwnProperty,v=Object.prototype.propertyIsEnumerable,h=(a,o,d)=>o in a?s(a,o,{enumerable:!0,configurable:!0,writable:!0,value:d}):a[o]=d,g=(a,o)=>{for(var d in o||(o={}))n.call(o,d)&&h(a,d,o[d]);if(c)for(var d of c(o))v.call(o,d)&&h(a,d,o[d]);return a};class l{constructor(o){this.content=o}static generic(o){return new l({kind:"generic",data:o})}static scheduledMeeting(o){return new l({kind:"scheduled-meeting",data:o})}static detectedMeeting(o){return new l({kind:"detected-meeting",data:o})}static failedMeeting(o){return new l({kind:"failed-meeting",data:o})}get id(){switch(this.content.kind){case"scheduled-meeting":return this.content.data.meeting.calendarMeetingGuid;case"failed-meeting":return this.content.data.meetingBotGuid;case"detected-meeting":return O(`${this.kind}:${this.content.data.meetingPlatform}:${this.content.data.url}`);case"generic":return O(`${this.kind}:${this.content.data.title}:${this.content.data.body}`);default:return this.kind}}get kind(){return this.content.kind}get title(){switch(this.content.kind){case"generic":case"failed-meeting":return this.content.data.title;case"scheduled-meeting":return this.content.data.meeting.title;case"detected-meeting":return"Meeting detected";default:return""}}get body(){switch(this.content.kind){case"generic":case"failed-meeting":return this.content.data.body;default:return null}}get url(){switch(this.content.kind){case"generic":case"failed-meeting":return this.content.data.url;default:return}}get meeting(){switch(this.content.kind){case"scheduled-meeting":return this.content.data.meeting;default:return}}get meetingUrl(){switch(this.content.kind){case"scheduled-meeting":return this.content.data.meeting.url;case"detected-meeting":return this.content.data.url;default:return}}get meetingPlatform(){var o;switch(this.content.kind){case"scheduled-meeting":return(o=this.content.data.meeting.platform)!=null?o:void 0;case"detected-meeting":return this.content.data.meetingPlatform;default:return}}get isScheduledMeeting(){return this.kind==="scheduled-meeting"}get isAutoDetectedMeeting(){return this.kind==="detected-meeting"}get isGenericNotification(){return this.kind==="generic"}get isFailedMeeting(){return this.kind==="failed-meeting"}updateMeetingIfNeeded(o){this.content.kind==="scheduled-meeting"&&this.meeting&&this.meeting.calendarMeetingGuid===o.calendarMeetingGuid&&(this.content.data.meeting=g(g({},this.meeting),o))}updateMeetingRecordIfNeeded(o,d){var p;this.content.kind==="scheduled-meeting"&&((p=this.meeting)==null?void 0:p.calendarMeetingGuid)===o&&(this.content.data.meeting.record=d)}get showSecondaryActionsMenu(){return!(this.isGenericNotification||this.isFailedMeeting)}get showTextField(){switch(this.content.kind){case"detected-meeting":return!this.meetingUrl;case"failed-meeting":return this.content.data.inviteUserToSendImpromptuMeetingBot;default:return!1}}get shouldAutoDismissOnMount(){return this.isGenericNotification||this.isFailedMeeting}}const O=a=>i().createHash("md5").update(a).digest("hex")},756879:(T,u,e)=>{e.d(u,{f:()=>h});var r=e(591705),i=e(416628),s=e(59876),c=e(924630),n=e(443934),v=e(950117);function h(){var g;const l=(0,r.TW)(i.SS.MEETING_NOTES_ONBOARDING,!1),O=(0,c.II)(),a=(g=(0,s.u9)(O??""))!=null?g:!1,o=(0,n.v9)(p=>p.preRecordingPanel.has_completed_meeting_notes_onboarding),d=(0,v.fz)().length>0;return{nudge:l&&a&&!o,contextualOnboarding:l&&a&&!o&&d}}},744081:(T,u,e)=>{T.exports=e.p+"assets/img/new-brand-logo.svg"}}]);

//# sourceMappingURL=9260.js.map