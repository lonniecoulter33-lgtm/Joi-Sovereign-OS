"use strict";(global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[]).push([[6773],{818421:(B,g,t)=>{t.d(g,{iU:()=>L});var s=t(992671);const E=s.Z.div`
  -webkit-app-region: no-drag;
`,T=s.Z.div`
  -webkit-app-region: drag;
`,W=s.Z.div`
  -webkit-app-region: ${v=>v.electronDraggable?"drag":"no-drag"};
`,L=E},626031:(B,g,t)=>{t.d(g,{q:()=>p});var s=t(183780),E=t(275271),T=t(797981),W=t(276523),L=t(553346),v=t(195851),S=t(581164),w=t(844589),y=t(333507),K=t(287631),F=t(382456),x=t(59876);const p=({meeting:r,defaultIcon:l})=>{const O=(0,L.U$)(r),R=(0,x.fU)(r.calendarMeetingGuid);if(!r.record)return E.createElement(s.JO$,{icon:E.createElement(K.n,null)});if(O){const{emoji:u,emojiUrl:m}=R??{};return u?E.createElement(s.xvT,{size:"heading-sm"},u):m?E.createElement("img",{src:m,alt:"Emoji",style:{width:32,height:32,objectFit:"contain"}}):l??E.createElement(s.JO$,{size:"32px",icon:E.createElement(y.F,null)})}return l??E.createElement(s.JO$,{size:"30px",icon:E.createElement(F.c,null)})},h=({meeting:r})=>React.createElement(Container,{radius:"medium",width:"32px",height:"32px"},React.createElement(Container,{width:"32px",height:"32px"},React.createElement(Align,{alignment:"center"},React.createElement(p,{meeting:r})))),a=({meeting:r,isPast:l})=>{const O=useWhoIsRecording(r)===IsRecording.NobodyRecording;return l?React.createElement(h,{meeting:r}):React.createElement(ColorBadge,{nobodyRecording:O})},c=({meeting:r})=>{var l;const[O,R]=useHover({}),u=isPastMeeting(r),m=!u&&isMeetingNow(r),U=useWhoIsRecording(r)===IsRecording.CurrentUserRecording,f=selectUserId(store.getState()),C=useNotesAvailableForMeeting(r),P={videoMeetingGuid:r.videoMeetingGuid,calendarMeetingGuid:r.calendarMeetingGuid,isMeetingOrganizer:((l=r?.organizer)==null?void 0:l.id)===f,isMeetingRecorder:U,videoId:r.videoId||void 0};return React.createElement(MeetingContainer,{hoverProps:R,isPast:u},React.createElement(Arrange,{gap:"medium",height:"100%",columns:["auto","1fr","auto"]},React.createElement(NotesEntryButton,{enabled:C,meeting:r,analyticsProps:P},React.createElement(a,{meeting:r,isPast:u}),React.createElement(TextSection,{isHovering:O,meeting:r,meetingIsNow:m,isMinimal:!1,isPast:u,notesAvailable:C})),React.createElement(Arrange,{gap:"medium"},O&&React.createElement(MeetingContextMenu,{meeting:r}),React.createElement(MeetingCTA,{meeting:r,notesAvailable:C,isHovering:O,analyticsProps:P}))))}},333507:(B,g,t)=>{t.d(g,{F:()=>E});var s=t(275271);const E=()=>s.createElement("svg",{width:"32",height:"32",viewBox:"0 0 32 32",fill:"none",xmlns:"http://www.w3.org/2000/svg"},s.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M26.5 9.25H5.5V7H26.5V9.25ZM13 16.75H5.5V14.5H13V16.75ZM13 25H5.5V22.75H13V25Z",fill:"#292A2E"}),s.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M17.0795 14.8295C17.3915 14.5175 17.857 14.4167 18.2701 14.5716L27.27 17.9466C27.7311 18.1195 28.0262 18.5723 27.9982 19.064C27.9702 19.5556 27.6256 19.972 27.1479 20.0914L23.3027 21.0527L22.3414 24.8979C22.222 25.3756 21.8057 25.7202 21.314 25.7482C20.8223 25.7762 20.3695 25.4811 20.1966 25.02L16.8217 16.02C16.6668 15.6069 16.7676 15.1414 17.0795 14.8295Z",fill:"#292A2E"}))},195851:(B,g,t)=>{var s=t(275271),E=t(183780),T=t(407973),W=t(553346),L=t(844589),v=t(892294),S=t(172298),w=t.n(S),y=t(581164),K=t(695610),F=t(276523),x=Object.defineProperty,p=Object.defineProperties,h=Object.getOwnPropertyDescriptors,a=Object.getOwnPropertySymbols,c=Object.prototype.hasOwnProperty,r=Object.prototype.propertyIsEnumerable,l=(n,_,d)=>_ in n?x(n,_,{enumerable:!0,configurable:!0,writable:!0,value:d}):n[_]=d,O=(n,_)=>{for(var d in _||(_={}))c.call(_,d)&&l(n,d,_[d]);if(a)for(var d of a(_))r.call(_,d)&&l(n,d,_[d]);return n},R=(n,_)=>p(n,h(_));const u=n=>({title:"Record meeting",onClick:()=>{store.dispatch(toggleCalendarMeetingRecordingAction({calendarMeetingGuid:n.calendarMeetingGuid,record:!0}))}}),m=n=>({title:"Turn off recording",onClick:()=>{store.dispatch(toggleCalendarMeetingRecordingAction({calendarMeetingGuid:n.calendarMeetingGuid,record:!1}))}}),U=n=>({title:"Meeting settings",onClick:()=>{openMeetingSettings(n)}}),f=n=>({title:"Join meeting",onClick:()=>{joinMeeting(n)}}),C=n=>({title:"Copy notes link",onClick:()=>{clipboard.writeText(n,"selection")}}),P=n=>({title:"View recording",onClick:()=>{viewRecording(n)}}),z=(n,_,d,N)=>{if(isMeetingNow(n))return j(n,_,d,N);const M=[];return isMeetingUpcoming(n,10)&&M.push(f(n)),N&&(M.push(m(n)),M.push(U(n))),d&&M.push(C(_)),M},j=(n,_,d,N)=>{const M=[];return N?(M.push(m(n)),M.push(U(n))):n.record||M.push(u(n)),d&&M.push(C(_)),M},b=(n,_,d)=>d?[P(n),C(_)]:[],k=({meeting:n})=>{const _=useWhoIsRecording(n),d=selectUserCurrentUserDefaultWorkspaceId(store.getState()),N=getMeetingNotesUrl(n,d),M=_===IsRecording.CurrentUserRecording,H=useNotesAvailableForMeeting(n),V=useMemo(()=>n.past?b(n,N,H):z(n,N,H,M),[n,M,N,H]);return V.length>0?React.createElement(Dropdown,{triggerCallback:$=>React.createElement(IconButton,R(O({},$),{onClick:Z=>{var J;Z.stopPropagation(),(J=$.onClick)==null||J.call($,Z)},altText:"Options",size:"small",icon:React.createElement(SvgMoreHoriz,null)})),options:V}):null}},553346:(B,g,t)=>{t.d(g,{U$:()=>ne});var s=t(992671),E=t(183780),T=t(275271),W=t(283297),L=t(523179),v=t(377534),S=t(844589),w=t(36048),y=t(330075),K=t(276523),F=t(581164),x=t(892294),p=t(796402),h=t(70002),a=t(59876),c=Object.defineProperty,r=Object.defineProperties,l=Object.getOwnPropertyDescriptors,O=Object.getOwnPropertySymbols,R=Object.prototype.hasOwnProperty,u=Object.prototype.propertyIsEnumerable,m=(e,o,i)=>o in e?c(e,o,{enumerable:!0,configurable:!0,writable:!0,value:i}):e[o]=i,U=(e,o)=>{for(var i in o||(o={}))R.call(o,i)&&m(e,i,o[i]);if(O)for(var i of O(o))u.call(o,i)&&m(e,i,o[i]);return e},f=(e,o)=>r(e,l(o));const C="https://loom.com/meetings/settings",P=e=>{executeCommand(SHOW_MEETING_NOTES_WINDOW,{meeting:e})},z=e=>{e.url&&openExternalUrl(store.dispatch,e.url,!1)},j=e=>{e.url&&openExternalUrl(store.dispatch,C)},b=e=>{executeCommand(OPEN_MEETING_RECORDING_LINK,{isCollapsed:!1,videoId:e.videoId,meetingGuids:{videoMeetingGuid:e.videoMeetingGuid,calendarMeetingGuid:e.calendarMeetingGuid}})},k=({children:e,hoverProps:o,isPast:i})=>React.createElement($,f(U({},o),{isPast:i}),React.createElement(Container,null,e)),n=s.Z.div`
  button {
    background-color: ${p.$X};
    &:hover {
      background-color: ${p.Ui};
    }

    &:active {
      background-color: ${p.L7};
    }
  }
`,_=({meeting:e,notesAvailable:o,analyticsProps:i,isHovering:I})=>{const D=isPastMeeting(e);return!D&&isMeetingNow(e)?React.createElement(d,{meeting:e,analyticsProps:i}):I?!D&&!e.record?React.createElement(N,{meeting:e}):o?React.createElement(M,{meeting:e,analyticsProps:i}):D&&e.videoId?React.createElement(Button,{variant:"neutral",size:"small",onClick:()=>b(e)},"View recording"):null:null},d=({meeting:e,analyticsProps:o})=>{const i=()=>{z(e),P(e),track(MEETING_RECORDING_TRANSCRIPT_BUTTON_CLICKED,o)};return React.createElement(n,null,React.createElement(Button,{onClick:i,variant:"primary",size:"small"},"Join"))},N=({meeting:e})=>{const o=()=>{store.dispatch(toggleCalendarMeetingRecordingAction({calendarMeetingGuid:e.calendarMeetingGuid,record:!0}))};return React.createElement(Button,{onClick:o,variant:"neutral",size:"small"},"Record meeting")},M=({meeting:e,analyticsProps:o})=>{const i=()=>{P(e),track(MEETING_RECORDING_MEETING_NOTES_BUTTON_CLICKED,o)};return React.createElement(Button,{onClick:i,variant:"neutral",size:"small"},"Notes")},H=s.Z.button`
  all: unset;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: ${e=>e.disabled?"inherit":"pointer"};
  flex: 1;
  width: 100%;
  grid-column: span 2;

  &:focus-visible {
    outline: 2px solid var(--lns-color-blue);
    outline-offset: 2px;
    border-radius: 8px;
  }
`,V=({enabled:e,children:o,meeting:i,analyticsProps:I})=>{const D=()=>{P(i),track(MEETING_RECORDING_MEETING_NOTES_BUTTON_CLICKED,I)};return React.createElement(H,{disabled:!e,onClick:e?D:void 0,type:"button","aria-label":"Open meeting notes"},o)},$=s.Z.div`
  > div {
    width: 100%;
    ${e=>e.isPast?"height: 48px;":"height: 64px;"}
    padding: ${e=>e.isPast?"8px 6px":"12px 16px"};
    border-radius: 16px;

    &:hover {
      background-color: ${e=>e.isPast?"var(--lns-color-grey2)":"var(--lns-color-grey1)"};
    }

    transition: background-color 300ms;
  }
`,Z=s.Z.div`
  height: 32px;
  width: 4px;
  min-width: 4px;

  border-radius: 4px;

  ${e=>e.nobodyRecording?"background-color: var(--lns-color-grey4);":"background-color: var(--lns-color-blue);"}
`,J=({isHovering:e,meeting:o,meetingIsNow:i,isMinimal:I,isPast:D,notesAvailable:A})=>{const G=e&&A;return React.createElement(Arrange,{autoFlow:"row"},React.createElement(Arrange,null,React.createElement(Text,{hasEllipsis:!0,fontWeight:"bold",color:G?"primary":"body"},React.createElement("span",{style:{textDecoration:G?"underline":"none",textUnderlineOffset:"2px"}},o.title))),!D&&React.createElement(te,{meeting:o,meetingIsNow:i,isMinimal:I}))},Q=()=>React.createElement(Text,{color:"recordActive",size:"body-sm"},"Now");var q=(e=>(e[e.CurrentUserRecording=0]="CurrentUserRecording",e[e.OtherUserRecording=1]="OtherUserRecording",e[e.NobodyRecording=2]="NobodyRecording",e))(q||{});const ee=e=>{var o,i,I;const D=selectUserId(store.getState()),A=e.record||e.recorder;return A&&((o=e?.recorder)==null?void 0:o.id)===D?0:A&&((i=e?.recorder)!=null&&i.id)&&((I=e?.recorder)==null?void 0:I.id)!=D?1:2},X=()=>React.createElement(Text,{style:{display:"inline-block",fontSize:"8px",verticalAlign:"text-bottom"}},"\u2022"),te=({meeting:e,meetingIsNow:o,isMinimal:i})=>{const I=new Date(`${e.startTime}`),D=stringifyTime(I);let A;const G=ee(e),Y=G===2?"bodyDimmed":"body";return G===1?A=`${e.recorder?`${e.recorder.first_name} ${e.recorder.last_name}`:""} recording`:G===0?A="You are recording":A="No one recording",o?React.createElement(Arrange,{alignItems:"baseline"},React.createElement(Q,null),!i&&React.createElement(React.Fragment,null,React.createElement(Spacer,{left:"xsmall"}),React.createElement(Text,{hasEllipsis:!0,size:"body-sm",color:Y}," ",React.createElement(X,null)," ",A),React.createElement(Spacer,{left:"xsmall"}))):React.createElement(Text,{hasEllipsis:!0,size:"body-sm"},D," ",React.createElement(Text,{size:"body-sm",isInline:!0,color:Y},React.createElement(X,null)," ",A))},ne=e=>{var o,i;const I=Boolean((0,a.u9)((i=(o=e.recorder)==null?void 0:o.id)!=null?i:"")&&!e.past),D=(0,a.sH)(e.calendarMeetingGuid)&&e.past;return Boolean(e.record&&(I||D))}},969178:(B,g,t)=>{t.d(g,{rp:()=>E});var s=t(377534);function E(v){return{id:v}}let T=null;function W(v){T=v}function L(v,S){T?T.executeCommand(v,S):executeCommandFromRenderer(v,S)}},59876:(B,g,t)=>{t.d(g,{u9:()=>w,sH:()=>y,fU:()=>K});var s=t(443934),E=t(276523),T=t(275271),W=t(892294),L=t(422607),v=t(879715);const S=()=>useSelector(a=>a.meetingRecordings.notifications.map(c=>new CustomNotification(c))),w=a=>(0,s.v9)(c=>c.meetingRecordings.recorderAmnEligibility[a]),y=a=>(0,s.v9)(c=>{var r;return(r=c.meetingRecordings.meetingNotesInfo[a])==null?void 0:r.exists}),K=a=>(0,s.v9)(c=>c.meetingRecordings.meetingNotesInfo[a]),F=a=>{const c=useDispatch(),[r,l]=useState(!1);return{dismissNotification:useCallback(()=>{l(!0);const R=setTimeout(()=>{c(a?removeMeetingNotificationById(a):clearMeetingNotifications())},DISMISS_ANIMATION_DURATION*1e3+100);return()=>{clearTimeout(R)}},[a,l,c]),isDismissed:r}},x=a=>{const[c,r]=useState(""),[l,O]=useState(!1);return useEffect(()=>{if(!a){r(""),O(!1);return}const R=()=>{const m=minutesUntilMeeting(a);m>0?(r(`${m}m`),O(!1)):(r("Now"),O(!0))},u=setInterval(R,1e3);return R(),()=>clearInterval(u)},[a]),{timeRemaining:c,isNow:l}},p=a=>{const[c,r]=useState(100),[l,O]=useState(!1),R=h(l),[u,m]=useState(!1),U=h(u),[f,C]=useState(null);return useEffect(()=>{if(!l||u){C(null);return}if(R===!1&&l===!0){C(Date.now());return}if(U===!0&&u===!1){const P=AUTO_DISMISS_DURATION*(1-c/100);C(Date.now()-P);return}},[l,u,f,U,c,R]),useEffect(()=>{if(!f)return;const P=setInterval(()=>{const j=1-(Date.now()-f)/AUTO_DISMISS_DURATION,b=Math.max(0,j*100);r(b),b<=0&&!u&&(a(),clearInterval(P))},1e3/30);return()=>{clearInterval(P)}},[a,f,u]),{progress:c,isAutoDismissEnabled:l,setAutoDismissEnabled:O,setAutoDismissPaused:m}},h=a=>{const c=useRef(a);return useEffect(()=>{c.current=a},[a]),c.current}},796402:(B,g,t)=>{t.d(g,{$X:()=>x,Ui:()=>p,L7:()=>h});var s=t(450630);const E=48,T=124,W=344,L=420,v=24,S=s.iv`
  rgba(255, 255, 255, 0.3)
`,w=s.iv`
  rgba(0, 0, 0, 0.3)
`,y=s.F4`
from {
  opacity: 0;
} to {
  opacity: 1;
}
`,K=250,F=150,x="var(--lns-color-blue)",p="#1558BC",h="var(--lns-color-blueDark)"},372259:(B,g,t)=>{t.d(g,{jK:()=>E,D9:()=>T});var s=t(625507);const E=10,T=40,W=[s.s.normal,s.s.screenshot,s.s.meetingsV2]}}]);

//# sourceMappingURL=6773.js.map