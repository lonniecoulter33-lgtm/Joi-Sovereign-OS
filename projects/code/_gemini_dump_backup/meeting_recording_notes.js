(()=>{"use strict";var ee={191798:(t,i,e)=>{var o=e(844589),r=e(443934),n=e(275271),a=e(394473),E=e(110720),_=e(230967),O=e(239222);const u="Loom Analytics Worker",d="Loom Camera",p="Loom Canvas",N="Loom Confetti",S="Loom Control Menu",I="Loom Countdown",m="Loom Cropping",A="Loom Disk Critical",H="Loom Audio Anomaly",w="Loom Drawing Overlay",R="Loom Not Authorized",x="Loom OAuth",P="Loom Preferences",V="Loom Recorder",K="Loom Recorder Settings",j="Loom Screenshot",Y="Welcome to Loom Desktop \u{1F389}",$="System Audio Driver Installation",T="Loom Window Selector",ne="Mouse Highlight Overlay",oe="Loom Software Update",se="Updating Loom",re="Loom: Recording a Zoom Meeting",ae="Loom: Meeting Recording Notes",De="Loom: Meeting Recording Index",Le="Loom: Meeting Notification",Ce="Loom: Contextual Onboarding",be="Loom: Feature Nudge",ie="Cancel Recording",ce="Restart Recording",le="Screenshot Failed",we="Cancel Meeting Recording",ve="Loom: Meeting Recording More Options",ye=[u,d,p,N,S,I,m,w,x,A,R,P,V,K,j,Y,$,T,ne,oe,se,re,ie,ce,le],xe=null;var f=e(183780),ue=e(747177),_e=e(827292),X=e(450630),M=e(992671);const z="www.loom.com",h="https://www.loom.com",Pe="loom.com",Ge="@*LOOM_WS_RECORDER_URI*@",de="wss://www.loom.com",Ee="https://packages.loom.com/desktop-version/minversion.json",Dt="",Lt="https://cdn.loom.com",Ct="http://support.loom.com",bt=`${h}/desktop`,wt=`${h}/pricing?from_desktop=true`,vt=`${h}/reset-password`,yt=`${h}/terms`,xt=`${h}/privacy-policy`,Pt=`${h}/welcome?recorded=false`,Gt=`${h}/welcome?newStyle=1&desktop=1`,Wt=`${h}/account-settings`,Ut=`${h}/settings/workspace#members`,Ht=`${h}/settings/workspace#plans`,Ft="https://chrome.google.com/webstore/detail/liecbddmkiiihnedobmlmillhodjkdmb",kt=`${h}/my-videos`,Bt=`${h}/profile`,Vt=`${h}/settings/workspace#members`,Kt="loomDesktop",jt="https://support.loom.com/hc/en-us/articles/360002241177-Using-Custom-Recording-Size-",Yt="https://support.loom.com/hc/en-us/articles/360002244718-Record-in-HD-with-Loom-Pro",$t=`${h}/canvas?platform=desktop`,Xt=`${h}/opensource/desktop`,zt=`${h}/download`;var v=e(416628);function Zt(s,l){var g;return(g=We(s))!=null?g:l}function We(s){const l=W(s);return typeof l=="string"?l:null}function Jt(s){const l=W(s);return Array.isArray(l)&&l.length>0&&l.every(g=>typeof g=="string")?l:null}function G(s,l){var g;return(g=Ue(s))!=null?g:l}function Ue(s){const l=W(s);return typeof l=="boolean"?l:null}function Qt(s,l){var g;return(g=He(s))!=null?g:l}function He(s){const l=W(s);return typeof l=="number"?l:null}function qt(s){const l=W(s);return typeof l=="object"?l:null}function Fe(){return(0,r.v9)(s=>s.featureFlags.flags)}function W(s){const l=Fe().find(g=>g[0]==s);if(l)return l[1]}function en(){return G(StatsigFeatureGate.ROLLOUT_DESKTOP_FILTER_EFFECTS,!1)}function ke(){return(0,r.v9)(s=>s.meetingRecordings.userShouldSeeMr2Features)}function tn(){return useBooleanFeatureFlag(StatsigFeatureGate.DESKTOP_MEETING_RECORDINGS,!1)}function nn(){return useUserShouldSeeMr2Features()}function on(){return useUserShouldSeeMr2Features()}function Oe(){return G(v.SS.LOOM_AI_DESKTOP_CHAT_FEATURES,!1)}var sn=e(974144);const rn=280,an="calc(6 * var(--lns-unit, 8px))",cn=0,ln=.5,un=.005,_n=null,dn=null,En="highlight_mouse_clicks",On="countdown",gn="flip_camera",pn="system_audio",mn="force_sw_recorder",Tn="enable_sck_screen_capture",fn="record_in_mono",Nn="persist_camera_bubble_location",hn="download_updates_in_bg",Sn="launch_at_startup";function Be(){return useSelector(s=>s.preferences)}function An(){const s=Be();return is.macos?!s[ENABLE_SCK_SCREEN_CAPTURE_KEY]:!1}var In=e(182261);function Mn(){return useSelector(s=>s.meetingRecordings)}const Rn=()=>useSelector(s=>s.meetingRecordings.notificationsSnoozedAt),Dn=()=>{const s=usePreferences(),l=useMeetingCustomNotifications(),g=s[MEETING_DETECTOR_ENABLED_KEY];return l&&g!==!1||!l&&g===!0},Ve=s=>(0,r.v9)(l=>s?l.meetingRecordings.meetings.find(D=>D.calendarMeetingGuid===s):void 0),Ln=()=>useSelector(s=>s.meetingRecordings.atlassianCloudDetails),Cn=()=>useSelector(s=>s.meetingRecordings.confluenceAuthStatus),bn=()=>useSelector(s=>s.meetingRecordings.confluenceLastSuccessfulAuthStatus),wn=()=>useSelector(s=>s.meetingRecordings.confluenceLastSuccessfulAuthAt),vn=()=>useSelector(s=>s.meetingRecordings.calendars);var Ke=e(581164);function ge(){return(0,r.v9)(s=>s.meetingViewReducer.tab)}function je(){return(0,r.v9)(s=>s.meetingViewReducer.calendarMeetingGuid)}function Ye(){return(0,r.v9)(s=>s.meetingViewReducer.videoMeetingGuid)}const $e=()=>(0,r.v9)(s=>s.meetingViewReducer.pageUrl),yn=()=>useSelector(s=>s.meetingViewReducer.scrollPosition);function Xe(){return(0,r.v9)(s=>s.meetingViewReducer.seenAgentTabFtux)}var Z=e(377534),J=e(330075),ze=e(171439);const Ze=M.Z.div`
  position: absolute;
  display: flex;
  width: 335px;
  margin-top: 4px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  right: 0;
  padding: 10px;
  z-index: 100;
  background-color: #1f1f21;
  border-radius: var(--lns-radius-250);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.65);
  overflow: hidden;
`,Je=M.Z.img`
  width: 100%;
  display: block;
`,pe=M.Z.span`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 2px;
  border-radius: 4px;
  background-color: var(--lns-color-grey7);
  font-weight: bold;
  color: var(--lns-color-grey3);
`,Qe=()=>n.createElement(Ze,null,n.createElement(Je,{src:ze,alt:"Agent Tab Ftux"}),n.createElement(f.xvT,{size:"body-lg",fontWeight:"bold",color:"white",style:{marginTop:12,marginBottom:6}},"Too late to ask? Try meeting agent"),n.createElement(f.xvT,{size:"body-md",color:"grey4",style:{marginBottom:12}},"Type ",n.createElement(pe,null,"/")," ",n.createElement(pe,null,"A")," for quick recaps, in-meeting context, and acronym definitions."));var qe=e(453440),et=e(797981),tt=Object.defineProperty,me=Object.getOwnPropertySymbols,nt=Object.prototype.hasOwnProperty,ot=Object.prototype.propertyIsEnumerable,Te=(s,l,g)=>l in s?tt(s,l,{enumerable:!0,configurable:!0,writable:!0,value:g}):s[l]=g,st=(s,l)=>{for(var g in l||(l={}))nt.call(l,g)&&Te(s,g,l[g]);if(me)for(var g of me(l))ot.call(l,g)&&Te(s,g,l[g]);return s};const fe=40,Ne=760,he=24,rt=M.Z.div`
  padding: var(--lns-space-xsmall);
  margin: 0 ${he}px;
  height: ${fe}px;
  border-radius: var(--lns-radius-200);
  background-color: var(--lns-color-backgroundHover);
  box-shadow: 0 1px 8px 0 rgba(0, 0, 0, 0.1) inset;
  overflow: visible;

  @media (width >= ${Ne+he*2}px) {
    width: 100%;
    max-width: ${Ne}px;
    margin: 0 auto;
  }
`,at="conic-gradient(from 270deg, #AF59E0 0deg 167.5deg, #FCA700 167.5deg 182.5deg, #6A9A23 182.5deg 340deg, #1868DB 340deg 360deg)",it=M.Z.div`
  position: relative;
`,ct=M.Z.button`
  width: 100%;
  height: ${fe-8}px;
  display: block;

  border: none;
  user-select: none;
  cursor: pointer;
  border-radius: var(--lns-radius-175);
  transition: all 0.2s ease-in-out;

  ${s=>s.withAgentFtuxStyling&&`
      position: relative;
      padding: 1px;
      background: #FFFFFF;
      box-shadow:
        -8px -4px 20px 4px rgba(175, 89, 224, 0.2),
        8px -4px 20px 4px rgba(252, 167, 0, 0.17),
        8px 4px 20px 4px rgba(106, 154, 35, 0.15),
        -8px 4px 20px 4px rgba(24, 104, 219, 0.17);

      &::after {
        content: '';
        position: absolute;
        inset: 0;
        background: ${at};
        border-radius: var(--lns-radius-175);
        opacity: 0;
        transition: opacity 0.2s ease-in-out;
        z-index: 0;
      }

      &::before {
        content: '';
        position: absolute;
        inset: 1px;
        background: #FFFFFF;
        border-radius: var(--lns-radius-175);
        z-index: 1;
      }

      &:hover::after {
        opacity: 1;
      }

      & > * {
        position: relative;
        z-index: 2;
      }
    `}

  ${s=>s.withAgentFtuxStyling&&s.isActive&&`
      box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.10);

      &::after {
        opacity: 0;
      }

      &:hover::after {
        opacity: 0;
      }
    `}

  ${s=>s.isActive&&!s.withAgentFtuxStyling&&`
      background-color: var(--lns-color-background);
      box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.10);
    `};
`,Q=({tab:s})=>{const[l,g]=(0,et.XI)(),D=(0,r.I0)(),F=ge(),y=Xe(),L=F===s,C=s==="assistant",b=Oe(),U=G(v.SS.LOOM_AI_DESKTOP_CHAT_HISTORY,!1),k=()=>{C&&b&&!y&&U&&D((0,qe.Ee)(!0)),(0,Z.P)(J.Zy,{tab:s})},q=(()=>{switch(s){case"notes":return"Notes";case"transcript":return"Transcript";case"assistant":return"Agent";default:return""}})();return n.createElement(it,st({},g),n.createElement(ct,{isActive:L,onClick:k,withAgentFtuxStyling:C&&U},n.createElement(f.xvT,{size:"body-md",fontWeight:"bold",color:L?"primary":"bodyDimmed"},q)),C&&l&&b&&!y&&U&&n.createElement(Qe,null))},lt=()=>{const s=Oe(),l=ke(),g=s&&l;return n.createElement(rt,null,n.createElement(f.ggW,{gap:"xsmall",autoFlow:"column",columns:["1fr","1fr",g?"1fr":"auto"]},n.createElement(Q,{tab:"notes"}),n.createElement(Q,{tab:"transcript"}),g&&n.createElement(Q,{tab:"assistant"})))};var Se=e(818421),ut=e(565067),_t=e(382456),dt=e(631915),Et=e(626031);const Ot=M.Z.div`
  padding: 16px 16px 0px 16px;
  height: 64px;
  -webkit-app-region: drag;
`,gt="#505258",pt=()=>n.createElement(f.hU,{altText:"close",icon:n.createElement(dt.G,null),onClick:()=>(0,Z.P)(J.Ee,{})},"Close"),mt=({meeting:s})=>n.createElement(Ot,null,n.createElement(f.ggW,{autoFlow:"row",justifyContent:"stretch",height:"100%"},n.createElement(f.ggW,{columns:["100px, 1fr, 100px"],height:"100%",autoFlow:"column",justifyContent:"space-between"},n.createElement(Se.iU,null,n.createElement(f.hU,{altText:"back",icon:n.createElement(ut.C,null),onClick:()=>{(0,Z.P)(J.u3)}},"close")),n.createElement(f.ggW,{autoFlow:"column",gap:"small"},s&&n.createElement(Et.q,{meeting:s,defaultIcon:n.createElement(f.JO$,{icon:n.createElement(_t.c,null),color:gt})}),n.createElement(f.xvT,{size:"body-md",fontWeight:"bold",color:"body"},s?.title)),n.createElement(Se.iU,null,n.createElement(pt,null))))),Tt=M.Z.div`
  background-color: var(--lns-color-grey1);
  height: 100vh;
`,ft=M.Z.iframe`
  width: 100%;
  height: 100%;
  border: none;
`,Nt=M.Z.iframe`
  width: 100%;
  height: 100%;
  border: none;
`,ht=()=>{const s=ge(),l=s==="notes",g=s==="assistant",[D,F]=(0,n.useState)(l),y=$e(),L=Ye(),C=je(),b=Ve(C??void 0),U=(0,Ke.sO)(o.h.getState()),k=b?.startTime?`?start=${encodeURIComponent(b.startTime)}`:"",q=`https://${z}/meetings/${L}/embed-transcript${k}`,It=`https://${z}/meetings/${L}/embed-assistant${k}`,Me={"loom-external-open":{route:`/confluence-meeting-notes?meeting=${C}&workspace=${U}&amn-referral-source=loom-desktop`}};(0,ue.h)(Re=>Re===v.SS.MR2_MEETING_RECORDING_NOTES_CONFLUENCE?Mt:Re===v.SS.EMBEDDED_CONFLUENCE_DELAYED_REF_PLATFORM?Rt:!1);const Mt=G(v.SS.MR2_MEETING_RECORDING_NOTES_CONFLUENCE,!1),Rt=G(v.SS.EMBEDDED_CONFLUENCE_DELAYED_REF_PLATFORM,!1);return(0,n.useEffect)(()=>{F(!1)},[y]),(0,n.useEffect)(()=>{l&&!D&&F(!0)},[l,D]),n.createElement(Tt,null,n.createElement(X.xB,{styles:X.iv`
          html,
          body {
            margin: 0;
          }
        `}),n.createElement(f.W20,{height:"100%"},n.createElement(f.W20,{height:"100%",overflow:"hidden",backgroundColor:"white"},n.createElement(f.ggW,{width:"100%",height:"100%",autoFlow:"row",justifyContent:"stretch",rows:["auto","auto","1fr"]},n.createElement(mt,{meeting:b}),n.createElement(lt,null),n.createElement(f.W20,{style:{display:l?"block":"none"},height:"100%"},y&&D&&n.createElement(f.ggW,{height:"100%",width:"100%",alignItems:"center",justifyContent:"stretch"},n.createElement(_e.T3,{url:y,allowedFeatures:{view:["modern-header","disable-help-button","disable-title-toolbar",Me],edit:["disable-publish-close-buttons",Me]},showFooter:!1,themeState:{colorMode:"light"},parentProduct:"loom"}))),n.createElement(f.W20,{style:{display:l||g?"none":"block"},height:"100%"},L?n.createElement(ft,{src:q}):n.createElement(f.aNw,{size:"large",color:"grey7"})),n.createElement(f.W20,{style:{display:g?"block":"none"},height:"100%"},L?n.createElement(Nt,{src:It,allow:"clipboard-write"}):n.createElement(f.aNw,{size:"large",color:"grey7"}))))))};(0,E.jC)(),(0,a.FA)("meetingNotes");const Ae=document.createElement("div"),Ie="container";Ae.id=Ie,document.body.appendChild(Ae),document.title=ae;const St=document.getElementById(Ie),At=o.S(O.Q,[]);(s=>(0,_.render)(n.createElement(r.zt,{store:At},n.createElement(s,null)),St))(ht)},987771:(t,i,e)=>{let o;function r(a){o=a}function n(a){return new Promise(E=>{const _=o.getState();if(a(_)){E(_);return}const O=o.subscribe(()=>{const u=o.getState();a(u)&&(O(),E(u))})})}},394473:(t,i,e)=>{e.d(i,{FA:()=>E,o7:()=>S});var o=e(172298),r=e.n(o),n=e(510453);let a="renderer";const E=m=>{m&&(a=m)},_=(m="info",A)=>(H,w)=>{const R={};w&&Object.entries(w).forEach(([x,P])=>{R[x]=O(P)}),o.ipcRenderer.send(n.u,{logLevel:m,message:H,context:R,windowName:A})};function O(m){return typeof m!="object"?m:u(m)?{message:m.message,name:m.name}:JSON.parse(JSON.stringify(m))}function u(m){return typeof m.message=="string"&&typeof m.name=="string"}const d=_("info",a),p=_("warn",a),N=_("error",a),S=_("debug",a),I=m=>({info:_("info",m),warn:_("warn",m),error:_("error",m),debug:_("debug",m)})},36048:(t,i,e)=>{var o=e(394473),r=e(172298),n=e.n(r),a=e(881863),E=e(826565);function _(O,u,d=!0){logDebug("Opening external url"),shell.openExternal(u).then(()=>{d&&O(setMaestroState(MaestroState.Minimized))})}},163224:(t,i,e)=>{e.d(i,{hr:()=>o,so:()=>r,dg:()=>a,Qp:()=>E,QN:()=>_,h0:()=>O});const o="show-contextual-onboarding",r="close-contextual-onboarding",n="update-seen-contextual-onboarding",a="set-contextual-onboarding-feature",E="set-contextual-onboarding-step",_="set-contextual-onboarding-display-bounds",O="reset-contextual-onboarding",u=A=>({type:a,payload:A}),d=A=>({type:E,payload:A}),p=()=>({type:o}),N=()=>({type:r}),S=()=>({type:n}),I=A=>({type:_,payload:A}),m=()=>({type:O})},185335:(t,i,e)=>{e.d(i,{eE:()=>o,Jg:()=>r});const o="open-feature-nudge",r="close-feature-nudge",n=E=>({type:o,payload:E}),a=(E=!0)=>({type:r,payload:E})},257728:(t,i,e)=>{e.d(i,{O_:()=>E,Ji:()=>_,U6:()=>O});var o=e(450630),r=e(284558),n=(u=>(u.MEETING_NOTES="meeting-notes",u))(n||{});const a={["meeting-notes"]:r._v},E={nudge:{fadeIn:{seconds:.15,milliseconds:150},fadeOut:{seconds:.15,milliseconds:150}},contextualOnboarding:{fadeIn:{seconds:.4,milliseconds:400},fadeOut:{seconds:.4,milliseconds:400}}},_=o.F4`
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
`},881863:(t,i,e)=>{var o=(r=>(r.LoggedOut="logged-out",r.Minimized="minimized",r.Idle="idle",r.IdleNoScreenshotFtux="idle_no_screenshot_ftux",r.ContextualOnboarding="contextual-onboarding",r.Countdown="countdown",r.Recording="recording",r.Onboarding="onboarding",r.Cropping="cropping",r.Meetings="meetings",r.MeetingsV2="meetings-v2",r.MeetingNotes="meeting-notes",r.MeetingOnboarding="meeting-onboarding",r.SelectingScreenshot="selecting-screenshot",r.MenuSelectScreenshot="menu-select-screenshot",r.ScreenshotShortcutSetup="screenshot-shortcut-setup",r.ScreenshotShortcutSetupCompleted="screenshot-shortcut-setup-completed",r.ScreenshotTryItFtux="screenshot-try-it-ftux",r))(o||{})},826565:(t,i,e)=>{var o=e(565327);const r=(0,o.PH)("maestro/set-state")},70002:(t,i,e)=>{var o=e(969178);const r=(0,o.rp)("change-recording-state"),n=(0,o.rp)("hide-meeting-bot-controls"),a=(0,o.rp)("open-meeting-recording-link"),E=(0,o.rp)("open-cancel-meeting-recording-confirmation"),_=(0,o.rp)("log-note-controls-discrepancy"),O=(0,o.rp)("show-bot-controls-after-resize"),u=(0,o.rp)("show-overflow-menu"),d=(0,o.rp)("hide-overflow-menu")},453440:(t,i,e)=>{e.d(i,{Ee:()=>E,Ws:()=>u});var o=e(565327);const r=(0,o.PH)("meeting-view-update-view-state"),n=(0,o.PH)("meeting-view-update-tab"),a=(0,o.PH)("meeting-view-set-scroll-position"),E=(0,o.PH)("meeting-view-set-seen-agent-tab-ftux"),_=(0,o.PH)("meeting-view-reset-state"),O=Object.freeze({tab:"notes",calendarMeetingGuid:null,videoMeetingGuid:null,pageUrl:null,scrollPosition:0,seenAgentTabFtux:!1}),u=(0,o.Lq)(O,d=>{d.addCase(r,(p,N)=>{var S,I,m;p.tab=N.payload.tab,p.calendarMeetingGuid=(S=N.payload.calendarMeetingGuid)!=null?S:null,p.videoMeetingGuid=(I=N.payload.videoMeetingGuid)!=null?I:null,p.pageUrl=(m=N.payload.pageUrl)!=null?m:null}),d.addCase(n,(p,N)=>{p.tab=N.payload}),d.addCase(a,(p,N)=>{p.scrollPosition=N.payload}),d.addCase(E,(p,N)=>{p.seenAgentTabFtux=N.payload}),d.addCase(_,p=>{Object.assign(p,O)})})},330075:(t,i,e)=>{e.d(i,{Zy:()=>E,Ee:()=>_,u3:()=>O});var o=e(969178);const r=(0,o.rp)("show-meeting-notes-window"),n=(0,o.rp)("collapse-meeting-notes-window"),a=(0,o.rp)("expand-meeting-notes-window"),E=(0,o.rp)("change-meeting-notes-tab"),_=(0,o.rp)("hide-meeting-notes-window"),O=(0,o.rp)("show-meeting-index-view")},695610:(t,i,e)=>{var o=e(230606),r=e(372259);const n=480,a=640,E=610,_=720,O=10,u=10,d=8,p=60+u,N=100+u,S=0,I=200,m=r.jK*2,A=r.jK+r.D9,H=n+m+O,w=a+A,R=124,x=184,P=200,V=260,K=300,j=8,Y=160,$=36,T=400,ne=400,oe="meetingGuid",se="meetingRendererIpc",re="electronToLoomSurfaceIpc",ae=25,De=2,Le=256,Ce=30,be=7,ie=7,ce=null,le=292,we=280,ve=448,ye=400,xe=!0,f=230,ue=146,_e=200,X=20,M=100,z=100,h=20,Pe=30,Ge=(de,Ee)=>`https://${LOOM_URI}/confluence-meeting-notes?meeting=${de.calendarMeetingGuid}&workspace=${Ee}&amn-referral-source=loom-desktop`},42022:(t,i,e)=>{e.d(i,{P2:()=>n,bV:()=>_,Br:()=>p,iK:()=>N,bA:()=>R});const o="hidden",r="hiding",n="fresh-launch",a="open",E="opening",_={width:400,height:280},d=["display-selector","window-selector"],p={FULL_SCREEN:"full-screen",WINDOW:"window",CUSTOM_SIZE:"custom-size"},N="back-to-normal",S="to-start-recording",I="to-crop-type",m="to-crop-type-window",A="to-crop-type-custom-size",H="video-tab",w="screenshot-tab";var R=(T=>(T.normalView="normalView",T.normalViewWithMenu="normalViewWithMenu",T.normalViewWithMsgType="normalViewWithMsgType",T.normalViewWithMsgTypeMenu="normalViewWithMsgTypeMenu",T.effectsView="effectsView",T.canvasView="canvasView",T.notificationsView="notificationsView",T.windowSelectorView="windowSelectorView",T.displaySelectorView="displaySelectorView",T.meetingsView="meetingsView",T.settingsView="settingsView",T.aboutView="aboutView",T.updatesView="updatesView",T.alertsView="alertsView",T.loginView="loginView",T))(R||{});const x=T=>T==="normalViewWithMsgType"||T==="normalViewWithMsgTypeMenu",P=T=>T==="normalViewWithMenu"||T==="normalViewWithMsgTypeMenu",$={normalView:{width:320,height:590},normalViewWithMenu:{width:620,height:760},normalViewWithMsgType:{width:320,height:770},normalViewWithMsgTypeMenu:{width:620,height:940},effectsView:{width:400,height:554},canvasView:{width:400,height:520},notificationsView:{width:460,height:600},windowSelectorView:{width:400,height:463},displaySelectorView:{width:400,height:503},settingsView:{width:400,height:700},aboutView:{width:320,height:500},updatesView:{width:320,height:560},alertsView:{width:400,height:490},loginView:{width:400,height:700},meetingsView:{width:440,height:540}}},15708:(t,i,e)=>{e.d(i,{N5:()=>O,Pm:()=>p});var o=e(565327);const r=(0,o.PH)("show-screenshot-shortcut-setup-entry-point"),n=(0,o.PH)("reposition-screenshot-shortcut-setup-entry-point"),a=(0,o.PH)("close-screenshot-shortcut-setup-entry-point"),E=(0,o.PH)("start-screenshot-shortcut-setup"),_=(0,o.PH)("screenshot-shortcut-setup-advance-to-next-step"),O=(0,o.PH)("mark-screenshot-setup-flow-completed"),u=(0,o.PH)("start-screenshot-shortcut-setup-from-preference"),d=(0,o.PH)("mark-screenshot-shortcut-setup-as-seen"),p=(0,o.PH)("update-setup-step")},581164:(t,i,e)=>{e.d(i,{sO:()=>O});var o=e(323055);const r=u=>u.user,n=(0,o.P1)(r,u=>{var d;return(d=u.current)==null?void 0:d.id}),a=(0,o.P1)(r,u=>{var d;return(d=u.current)==null?void 0:d.aa_id}),E=(0,o.P1)(r,u=>{var d,p;return(p=(d=u.current)==null?void 0:d.aa_is_mastered)!=null?p:!1}),_=(0,o.P1)(r,u=>{var d,p;return(p=(d=u.current)==null?void 0:d.avatars)!=null?p:[]}),O=(0,o.P1)(r,u=>{var d;return(d=u.current)==null?void 0:d.default_workspace_id})},171439:(t,i,e)=>{t.exports=e.p+"assets/img/contextual-onboarding/meeting-notes/with-agent/meeting_agent_ftux.png"},439491:t=>{t.exports=require("assert")},706113:t=>{t.exports=require("crypto")},172298:t=>{t.exports=require("electron")},582361:t=>{t.exports=require("events")},657147:t=>{t.exports=require("fs")},113685:t=>{t.exports=require("http")},795687:t=>{t.exports=require("https")},822037:t=>{t.exports=require("os")},371017:t=>{t.exports=require("path")},863477:t=>{t.exports=require("querystring")},257310:t=>{t.exports=require("url")},473837:t=>{t.exports=require("util")}},B={};function c(t){var i=B[t];if(i!==void 0)return i.exports;var e=B[t]={id:t,loaded:!1,exports:{}};return ee[t].call(e.exports,e,e.exports,c),e.loaded=!0,e.exports}c.m=ee,c.c=B,(()=>{var t=[];c.O=(i,e,o,r)=>{if(e){r=r||0;for(var n=t.length;n>0&&t[n-1][2]>r;n--)t[n]=t[n-1];t[n]=[e,o,r];return}for(var a=1/0,n=0;n<t.length;n++){for(var[e,o,r]=t[n],E=!0,_=0;_<e.length;_++)(r&!1||a>=r)&&Object.keys(c.O).every(S=>c.O[S](e[_]))?e.splice(_--,1):(E=!1,r<a&&(a=r));if(E){t.splice(n--,1);var O=o();O!==void 0&&(i=O)}}return i}})(),c.n=t=>{var i=t&&t.__esModule?()=>t.default:()=>t;return c.d(i,{a:i}),i},(()=>{var t=Object.getPrototypeOf?e=>Object.getPrototypeOf(e):e=>e.__proto__,i;c.t=function(e,o){if(o&1&&(e=this(e)),o&8||typeof e=="object"&&e&&(o&4&&e.__esModule||o&16&&typeof e.then=="function"))return e;var r=Object.create(null);c.r(r);var n={};i=i||[null,t({}),t([]),t(t)];for(var a=o&2&&e;typeof a=="object"&&!~i.indexOf(a);a=t(a))Object.getOwnPropertyNames(a).forEach(E=>n[E]=()=>e[E]);return n.default=()=>e,c.d(r,n),r}})(),c.d=(t,i)=>{for(var e in i)c.o(i,e)&&!c.o(t,e)&&Object.defineProperty(t,e,{enumerable:!0,get:i[e]})},c.f={},c.e=t=>Promise.all(Object.keys(c.f).reduce((i,e)=>(c.f[e](t,i),i),[])),c.u=t=>"js/"+({17:"@atlaskit-internal_embedded-confluence-view-page",152:"tti-polyfill",153:"@atlaskit-internal_embedded-confluence-i18n-fi",214:"@atlaskit-internal_atlassian-legacy-dark",262:"@atlaskit-internal_embedded-confluence-i18n-uk",334:"@atlaskit-internal_atlassian-light",448:"@atlaskit-internal_embedded-confluence-page",551:"@atlaskit-internal_embedded-confluence-i18n-da",631:"@atlaskit-internal_atlassian-light-increased-contrast",1025:"@atlaskit-internal_atlassian-legacy-light",1261:"@atlaskit-internal_atlassian-typography-adg3",1589:"@atlaskit-internal_atlassian-typography-refreshed",1889:"@atlaskit-internal_embedded-confluence-whiteboard",1915:"@atlaskit-internal_embedded-confluence-i18n-pt_BR",2630:"@atlaskit-internal_atlassian-typography-modernized",2909:"@atlaskit-internal_embedded-confluence-i18n-sv",3647:"@atlaskit-internal_embedded-confluence-embedded-content-panel",3742:"@atlaskit-internal_embedded-confluence-i18n-hu",4119:"@atlaskit-internal_embedded-confluence-i18n-en_GB",4292:"@atlaskit-internal_embedded-confluence-i18n-it",4338:"@atlaskit-internal_atlassian-light-future",4389:"@atlaskit-internal_atlassian-custom-theme",4636:"@atlaskit-internal_embedded-confluence-i18n-th",4840:"@atlaskit-internal_embedded-confluence-i18n-vi",5041:"@atlaskit-internal_embedded-confluence-i18n-zh",5089:"@atlaskit-internal_embedded-confluence-i18n-tr",5282:"@atlaskit-internal_embedded-confluence-i18n-es",5826:"@atlaskit-internal_embedded-confluence-embedded-content-modal",6117:"@atlaskit-internal_embedded-confluence-i18n-fr",6136:"@atlaskit-internal_embedded-confluence-i18n-zh_TW",6210:"@atlaskit-internal_atlassian-shape",6270:"@atlaskit-internal_inernal-embedded-confluence-entrypoint",6328:"web-vitals",6409:"@atlaskit-internal_embedded-confluence-i18n-en",6428:"@atlaskit-internal_embedded-confluence-i18n-pl",6632:"@atlaskit-internal_embedded-confluence-i18n-ru",6715:"@atlaskit-internal_embedded-confluence-i18n-de",6903:"@atlaskit-internal_atlassian-dark",7039:"@atlaskit-internal_embedded-confluence-i18n-ko",7131:"@atlaskit-internal_embedded-confluence-i18n-cs",7154:"@atlaskit-internal_embedded-confluence-i18n-nb",7468:"@atlaskit-internal_embedded-confluence-i18n-en_ZZ",7983:"@atlaskit-internal_atlassian-dark-future",8555:"@atlaskit-internal_atlassian-dark-increased-contrast",9211:"@atlaskit-internal_atlassian-typography",9436:"@atlaskit-internal_atlassian-spacing",9613:"@atlaskit-internal_embedded-confluence-edit-page",9682:"@atlaskit-internal_embedded-confluence-i18n-nl",9982:"@atlaskit-internal_embedded-confluence-i18n-ja"}[t]||t)+".js",c.h=()=>"55e5c6a40d444554bfb1",c.hmd=t=>(t=Object.create(t),t.children||(t.children=[]),Object.defineProperty(t,"exports",{enumerable:!0,set:()=>{throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+t.id)}}),t),c.o=(t,i)=>Object.prototype.hasOwnProperty.call(t,i),(()=>{var t={},i="@loomhq-desktop/monorepo:";c.l=(e,o,r,n)=>{if(t[e]){t[e].push(o);return}var a,E;if(r!==void 0)for(var _=document.getElementsByTagName("script"),O=0;O<_.length;O++){var u=_[O];if(u.getAttribute("src")==e||u.getAttribute("data-webpack")==i+r){a=u;break}}a||(E=!0,a=document.createElement("script"),a.charset="utf-8",a.timeout=120,c.nc&&a.setAttribute("nonce",c.nc),a.setAttribute("data-webpack",i+r),a.src=e),t[e]=[o];var d=(N,S)=>{a.onerror=a.onload=null,clearTimeout(p);var I=t[e];if(delete t[e],a.parentNode&&a.parentNode.removeChild(a),I&&I.forEach(m=>m(S)),N)return N(S)},p=setTimeout(d.bind(null,void 0,{type:"timeout",target:a}),12e4);a.onerror=d.bind(null,a.onerror),a.onload=d.bind(null,a.onload),E&&document.head.appendChild(a)}})(),c.r=t=>{typeof Symbol<"u"&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},c.nmd=t=>(t.paths=[],t.children||(t.children=[]),t),c.p="./",(()=>{var t={9275:0};c.f.j=(o,r)=>{var n=c.o(t,o)?t[o]:void 0;if(n!==0)if(n)r.push(n[2]);else{var a=new Promise((u,d)=>n=t[o]=[u,d]);r.push(n[2]=a);var E=c.p+c.u(o),_=new Error,O=u=>{if(c.o(t,o)&&(n=t[o],n!==0&&(t[o]=void 0),n)){var d=u&&(u.type==="load"?"missing":u.type),p=u&&u.target&&u.target.src;_.message="Loading chunk "+o+` failed.
(`+d+": "+p+")",_.name="ChunkLoadError",_.type=d,_.request=p,n[1](_)}};c.l(E,O,"chunk-"+o,o)}},c.O.j=o=>t[o]===0;var i=(o,r)=>{var[n,a,E]=r,_,O,u=0;if(n.some(p=>t[p]!==0)){for(_ in a)c.o(a,_)&&(c.m[_]=a[_]);if(E)var d=E(c)}for(o&&o(r);u<n.length;u++)O=n[u],c.o(t,O)&&t[O]&&t[O][0](),t[n[u]]=0;return c.O(d)},e=global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[];e.forEach(i.bind(null,0)),e.push=i.bind(null,e.push.bind(e))})(),c.O(void 0,[592,8588,719,3823,793,6494,947,5466,8058,390,9073,8224,7348,1404,3655,816,5878,6369,6375,1709],()=>c(c.s=903679)),c.O(void 0,[592,8588,719,3823,793,6494,947,5466,8058,390,9073,8224,7348,1404,3655,816,5878,6369,6375,1709],()=>c(c.s=191798)),c.O(void 0,[592,8588,719,3823,793,6494,947,5466,8058,390,9073,8224,7348,1404,3655,816,5878,6369,6375,1709],()=>c(c.s=639542));var te=c.O(void 0,[592,8588,719,3823,793,6494,947,5466,8058,390,9073,8224,7348,1404,3655,816,5878,6369,6375,1709],()=>c(c.s=194383));te=c.O(te)})();

//# sourceMappingURL=meeting_recording_notes.js.map