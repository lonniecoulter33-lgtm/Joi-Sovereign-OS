(()=>{var Ve={308066:(o,_,n)=>{var t=n(744917),r=n(570097),s=n(969975);_=t(!1);var a=r(s);_.push([o.id,`@font-face {
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
`,""]),o.exports=_},994021:(o,_,n)=>{"use strict";var t=n(275271),r=n(230967),s=n(443934),a=n(346972),c=n(835875),l=n(218417),T=n(251308),N=n(29419),g=n(879741),p=n(974144),u=n(78672),O=n(804951),I=n(212849),m=n(206687);const P="0.330.1",k=G();function G(){return{version:P,appArch:process.arch}}var U=n(25334),S=Object.defineProperty,y=Object.getOwnPropertySymbols,h=Object.prototype.hasOwnProperty,B=Object.prototype.propertyIsEnumerable,H=(e,i,E)=>i in e?S(e,i,{enumerable:!0,configurable:!0,writable:!0,value:E}):e[i]=E,j=(e,i)=>{for(var E in i||(i={}))h.call(i,E)&&H(e,E,i[E]);if(y)for(var E of y(i))B.call(i,E)&&H(e,E,i[E]);return e};const A=["ERR_NETWORK_IO_SUSPENDED","ERR_NAME_NOT_RESOLVED","ERR_INTERNET_DISCONNECTED","ERR_NETWORK_CHANGED","ERR_CONNECTION_RESET"],D=.25;let W;const q=e=>{W=e},z=e=>{const i=n(952126),b=`${g.ar?I.Zb:I.zl}@${k.version}`,L=p.is.macos?I.Sd:I.HV;i.init(j({dsn:I.KL,environment:g.Gv,debug:!0,release:`${b}-${L}`,enableUnresponsive:!1,autoSessionTracking:!0,attachStacktrace:!0,sampleRate:D,ignoreErrors:A,beforeSend(K){return(0,U.b5)(K)}},e)),W=i},ee=e=>{W.configureScope(i=>{i.setUser({id:e})})},te=()=>{const e=[m.$G];return u.wS({actionTransformer:E=>e.includes(E.type)?null:{type:E.type},stateTransformer:()=>null})},ne=e=>{W.captureException(e)},pe=(e,...i)=>{log.error("logException",e,...i),ne(e)},le=(e,i,E)=>{if(i instanceof Error){const b=`${e}: ${i.message}`;log.error(b),W.captureMessage(b,"error",{originalException:i})}else log.error(e),W.captureMessage(e,"error")},Te=e=>{W.captureMessage(e)},Oe=e=>{W.addBreadcrumb(e)};let F;const oe=(e,i)=>{const E=window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__||c.qC,b=(0,a.mu)(),L=[...g.v9?[N.Z]:[],a.Wp,T.Z,l.ZP,...i];return F=(0,c.MT)(e,b,E((0,c.md)(...L),te())),(0,a.Id)(F),F};var se=n(239222),re=n(474176),$=n(172298),ie=n(510453);let x="renderer";const X=e=>{e&&(x=e)},M=(e="info",i)=>(E,b)=>{const L={};b&&Object.entries(b).forEach(([K,J])=>{L[K]=Se(J)}),$.ipcRenderer.send(ie.u,{logLevel:e,message:E,context:L,windowName:i})};function Se(e){return typeof e!="object"?e:Re(e)?{message:e.message,name:e.name}:JSON.parse(JSON.stringify(e))}function Re(e){return typeof e.message=="string"&&typeof e.name=="string"}const ce=M("info",x),ae=M("warn",x),Ce=M("error",x),Ne=M("debug",x),de=e=>({info:M("info",e),warn:M("warn",e),error:M("error",e),debug:M("debug",e)}),he="Loom Analytics Worker",be="Loom Camera",Pe="Loom Canvas",R="Loom Confetti",Y="Loom Control Menu",V="Loom Countdown",ze="Loom Cropping",Ze="Loom Disk Critical",Vt="Loom Audio Anomaly",$e="Loom Drawing Overlay",Xe="Loom Not Authorized",Qe="Loom OAuth",Je="Loom Preferences",qe="Loom Recorder",et="Loom Recorder Settings",tt="Loom Screenshot",ve="Welcome to Loom Desktop \u{1F389}",nt="System Audio Driver Installation",ot="Loom Window Selector",st="Mouse Highlight Overlay",rt="Loom Software Update",it="Updating Loom",ct="Loom: Recording a Zoom Meeting",Yt="Loom: Meeting Recording Notes",zt="Loom: Meeting Recording Index",Zt="Loom: Meeting Notification",$t="Loom: Contextual Onboarding",Xt="Loom: Feature Nudge",at="Cancel Recording",Le="Restart Recording",dt="Screenshot Failed",Qt="Cancel Meeting Recording",Jt="Loom: Meeting Recording More Options",qt=[he,be,Pe,R,Y,V,ze,$e,Qe,Ze,Xe,Je,qe,et,tt,ve,nt,ot,st,rt,it,ct,at,Le,dt],_t=null;var f=n(992671),_e=n(599682),Ie=(e=>(e.MediaAnomalyCriticalError="media_anomaly_critical_error",e.MediaRecorderCriticalError="media_recorder_critical_error",e.NativeRecorderFatal="native_recorder_fatal",e.ControlMenuClicked="control_menu_clicked",e.CountdownCancelClicked="countdown_cancel_clicked",e.KeyboardShortcutClicked="keyboard_shortcut_clicked",e.QuitAppConfirmationClicked="quit_app_confirmation_clicked",e.RestartRecordingClicked="restart_recording_clicked",e))(Ie||{}),Ue=n(341592),en=n(910884),me=n(183780),we=(e=>(e.ROLLOUT_DESKTOP_AIRHORN="rollout-desktop-airhorn",e.RECORDING_CLIENTS_BANNER="recording-clients-banner",e.RELEASE_CHANNEL_GROUP="desktop-recorder-release-channel-v2",e.ROLLOUT_STREAM_UPLOADER_MAC="rollout-stream-uploader-mac",e.ROLLOUT_STREAM_UPLOADER_WINDOWS_2="rollout-stream-uploader-windows-2",e.ROLLOUT_CLIENTS_SCREENSHOT_DELAYED_FTUX="rollout-screenshots-delayed-ftux",e.ROLLOUT_CAMSPLIT_ENCODING="rollout-cam-split-encoding",e.DESKTOP_TEST_ONLY="desktop-test-only",e))(we||{}),De=(e=>(e.DESKTOP_MAC_SCK_RESTREAM_REPLAYD_LOGS="desktop-mac-sck-restream-replayd-logs",e.DESKTOP_MAC_SCK_INIT_ON_MAIN_DISPATCH_QUEUE="desktop-mac-sck-init-on-main-dispatch-queue",e.DESKTOP_WINDOWS_HW_SCREEN_RECORDING="desktop-windows-hw-screen-recording",e.DESKTOP_WINDOWS_AUDIO_RECORDING_V2="desktop-windows-audio-recording-v2",e.DESKTOP_WINDOWS_IPP_INTEGRATION="desktop-windows-ipp-integration",e.DESKTOP_MEETING_RECORDINGS="desktop_meeting_recordings",e.CAM_SPLIT_TRUE_BY_DEFAULT="cam-split-true-by-default",e.DESKTOP_S3_FALLBACK_SERVER_VALUES_ENABLED="desktop-s3-fallback-server-values-enabled",e.MR2_ASSISANT_IN_DESKTOP="mr2-assistant-in-desktop",e.LOOM_CLIENTS_CLOSE_BUTTON_ON_THE_RIGHT="loom-clients-close-button-on-the-right",e.AUTO_PAUSE_ON_SILENCE="loom-auto-pause-on-silence",e.PRACTICE_MODE="loom-practice-mode",e.ROLLOUT_DESKTOP_FILTER_EFFECTS="rollout-desktop-filter-effects",e.MR2_MEETING_RECORDING_NOTES_CONFLUENCE="mr2-meeting-recording-notes-confluence",e.CAMERA_BUBBLE_QUALITY_SETTING="camera-bubble-quality-setting",e.LOOM_AI_DESKTOP_CHAT_FEATURES="loom_ai-desktop-chat-features",e.LOOM_AI_DESKTOP_CHAT_HISTORY="loom_ai-desktop-chat-history",e.COUNTDOWN_TIMER_UPDATE_DESKTOP="countdown-timer-update-desktop",e.DESKTOP_FEDERATED_QUERIES="desktop-federated-queries",e.MEETING_NOTES_ONBOARDING="meeting-notes-onboarding",e.EMBEDDED_CONFLUENCE_DELAYED_REF_PLATFORM="embedded_confluence_delayed_ref_platform",e.WINDOWS_CAM_ONLY_NATIVE_RECORDING="windows-cam-only-native-recording",e.DEBUG_LOGS_TICKET_CREATION="debug-logs-ticket-creation",e.COMPLETE_VIDEO_MUTATION="loom-desktop-complete-video-mutation",e.WINDOW_SELECTION_V2="loom-desktop-window-selection-v2",e))(De||{}),ke=(e=>(e.CAM_SPLIT_WITH_AUTO_ZOOM_AND_LOCATION_PICKER="loom_cam_split_with_auto_zoom_and_location_picker",e.AMN_LOOM_IMPROVEMENTS_FY26="amn_loom_improvements_fy26",e))(ke||{}),Me=(e=>(e.DESKTOP_WINDOWS_HW_SCREEN_RECORDING_EXCLUDED_DEVICES="desktop-win-hw-recording-excluded-devices2",e.DESKTOP_MAC_SCK_RESTART_TIMEOUT_SECONDS="desktop-mac-sck-restart-timeout-seconds",e.DESKTOP_WINDOWS_HW_SCREEN_RECORDING_QUEUE_DEPTH="desktop-windows-hw-screen-recording-queue-depth",e.DESKTOP_WINDOWS_IPP_RESIZE_TYPE="desktop-windows-ipp-resize-type",e.DESKTOP_WINDOWS_HW_TEXTURE_POOL_SIZE_TOTAL="desktop-windows-hw-texture-pool-size-total",e.DESKTOP_WINDOWS_HW_TEXTURE_POOL_SIZE_PER_FORMAT="desktop-windows-hw-texture-pool-size-per-format",e.DESKTOP_WINDOWS_RESYNC_ON_RESUME_STRATEGY="desktop-windows-resync-on-resume-strategy",e.CUSTOMER_COMMUNICATION_BANNER="desktop-customer-comms-banner",e.DESKTOP_QUIET_DEVICE_ANOMALY_THRESHOLD_DB="desktop-quiet-device-anomaly-threshold-db",e))(Me||{});const Et=Array.from([...Object.values(we),...Object.values(De),...Object.values(Me),...Object.values(ke)],e=>[e,e]),Ge=new Map;for(const e of Et)Ge.set(e[0],e[1]);function tn(e){return Ge.get(e)}function d(e,i){var E;return(E=w(e))!=null?E:i}function w(e){const i=Ee(e);return typeof i=="string"?i:null}function Be(e){const i=Ee(e);return Array.isArray(i)&&i.length>0&&i.every(E=>typeof E=="string")?i:null}function ge(e,i){var E;return(E=We(e))!=null?E:i}function We(e){const i=Ee(e);return typeof i=="boolean"?i:null}function Js(e,i){var E;return(E=nn(e))!=null?E:i}function nn(e){const i=Ee(e);return typeof i=="number"?i:null}function qs(e){const i=Ee(e);return typeof i=="object"?i:null}function on(){return(0,s.v9)(e=>e.featureFlags.flags)}function Ee(e){const i=on().find(E=>E[0]==e);if(i)return i[1]}function er(){return ge(StatsigFeatureGate.ROLLOUT_DESKTOP_FILTER_EFFECTS,!1)}var Q=n(450630),sn=n(322052),rn=n.n(sn),cn=n(299820);const Z="Recovery",v="Validation",an=[{message:"You got this. Let's record",emoji:"muscle",label:v},{message:"People want to hear what you have to say",emoji:"sunglasses",label:v},{message:"You were born to be on camera",emoji:"video_camera",label:v},{message:"Breathe in...breathe out...Let's record.",emoji:"relieved",label:v},{message:"You can always pause to gather your thoughts",emoji:"thought_balloon",label:Z},{message:"You're a natural at this",emoji:"muscle",label:v},{message:"Don't sweat the ums\u2014we all do 'em!",emoji:"blush",label:v},{message:"Your viewers are gonna love you!",emoji:"heart_eyes",label:v},{message:"Mistakes are human\u2014embrace them!",emoji:"handshake",label:v},{message:"You're the star of the show!",emoji:"sparkles",label:v},{message:"You can cut any mistakes after recording!",emoji:"scissors",label:Z},{message:"You're saving time with fewer meetings!",emoji:"stopwatch",label:v},{message:"Keep up the great work!",emoji:"pray",label:v},{message:"Press Opt+Shift+P to pause your recording",emoji:"double_vertical_bar",label:Z},{message:"'Ums' make you human (not a robot)",emoji:"robot_face",label:v},{message:"We can help you remove 'ums' later",emoji:"wink",label:Z},{message:"Lights, camera, action! You've got this.",emoji:"sparkles",label:v},{message:"Press Cmd+Shift+R to restart your recording",emoji:"arrows_counterclockwise",label:Z},{message:"Keep going, you can edit mistakes later",emoji:"scissors",label:Z},{message:"Lookin' good",emoji:"sunny",label:v},{message:"Your smile is contagious",emoji:"grin",label:v},{message:"If you mess up, just keep going!",emoji:"muscle",label:Z},{message:"Unpolished videos are OK!",emoji:"sparkles",label:v},{message:"Here we go. It's time to record!",emoji:"movie_camera",label:v}],dn=Q.iv`
  @keyframes bounce {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
`,_n=f.Z.div`
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 1;
  ${e=>e.marginTop!==void 0?`margin-top: ${e.marginTop};`:"position: relative; top: -221px;"}
  ${e=>e.count!==0&&`animation: ${dn} 750ms forwards;`}
`;function En(){const[e,i]=(0,t.useState)();return(0,t.useEffect)(()=>{i(rn()(an))},[]),e}const ut=({count:e,marginTop:i})=>{const E=En(),b=E?.message,L=E?.emoji;return t.createElement(_n,{count:e,marginTop:i},t.createElement(me.DRh,{style:{fontSize:"14px"},color:"white",backgroundColor:"grey8"},b," ",(0,cn.Dl)(L)))};var un=n(631915),pn=n(762470),ln=n(152851);const Tn=f.Z.div`
  -webkit-app-region: no-drag;
`,tr=f.Z.div`
  -webkit-app-region: drag;
`,nr=f.Z.div`
  -webkit-app-region: ${e=>e.electronDraggable?"drag":"no-drag"};
`,or=null,On=(0,f.Z)(me.zxk)`
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 1px solid var(--lns-color-grey3);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: white;
  position: relative;
  pointer-events: auto;

  &:hover {
    background-color: rgba(41, 42, 46, 0.5);
  }

  &:hover svg {
    opacity: 0;
  }

  &:hover::after {
    content: '${e=>e.buttonText}';
    position: absolute;
    color: white;
    font-size: 18px;
    font-weight: bold;
    font-family: inherit;
  }
`,Sn=f.Z.div`
  ${e=>e.rotate&&"transform: rotate(180deg);"}
  display: flex;
  align-items: center;
  justify-content: center;

  svg {
    width: 40px;
    height: 40px;
  }
`;function pt({text:e,icon:i,onClick:E,rotateIcon:b=!1}){return t.createElement(Tn,null,t.createElement(On,{onClick:E,title:e,buttonText:e},t.createElement(Sn,{rotate:b},i)))}var lt=n(23405),Rn=n(604822),Cn=n(987771);const Nn=(0,Rn.h)("analytics","\u{1F596}"),Tt=()=>F||Cn.h;function He(e){const i=Tt();i?setImmediate(()=>{e(i.dispatch)}):Nn.warn("Could not run analytics event. Redux store has not been created yet")}function In(e,i){He(E=>{E((0,lt.Qs)({name:e,props:i}))})}function ye(e,i){He(E=>{E((0,lt.L9)({name:e,props:i}))})}function sr(e,i){He(E=>{E(identifyEvent({userId:e,traits:i}))})}function rr(){const e=Tt();return{anonId:e?e.getState().analytics.anonymous_id:null}}const mn="Desktop Binary Timeout",Dn="Desktop Permissions Onboarding",gn="Desktop Confetti",yn="Desktop Keyboard Shortcuts Updated",An="Desktop Launch",fn="Desktop Menu Activated",hn="Desktop Speaker Notes",bn="Desktop Screenshot Preview",Pn="Desktop Screenshot Shortcut Setup",ir="Desktop Screenshot Try It Ftux",vn="System Audio Modal",Ln="Desktop Quit",Un="Log Out",wn="Pro Tag Clicked",kn="Desktop Used Confetti",Mn="Uploader User Canceled Failed Retries",Gn="Uploader User Attempted Failed Retries",Bn="Engaged an RBAC restriction",Wn="Desktop Camera Bubble Rendered",Hn="Desktop Critical Error While Recording",xn="Desktop Recorder Stop",cr="Cascading Recorders Modal",Kn="Desktop Screenshot Capture Shortcut Pressed",jn="Desktop Screenshot Capture Started",Fn="Desktop Screenshot Capture Completed",Vn="Desktop Screenshot Capture Failed",Yn="Desktop Screenshot Capture Cancelled",zn="Desktop Screenshot Upload Started",Zn="Desktop Screenshot Upload Completed",$n="Desktop Screenshot Upload Failed",Xn="Restart Recording Keyboard Shortcut",Qn="Event Recording Restart Prompt Reject",Jn="Event Recording Restart Prompt Confirm",qn="App quit during recording",eo="Desktop SRT successfully received",to="Desktop shared auth successful",no="Desktop shared auth initiated",oo="Desktop shared auth welcome flow triggered",so="User app restart on start recording failure",ro="User app quit on start recording failure",io="Quit During Recording Prompt",Ot="Desktop Countdown Paused",St="Desktop Countdown Unpaused",xe="Desktop Countdown Skipped",Rt="Desktop Countdown Cancelled",co="Desktop Onboarding Started",ao="Desktop Onboarding Step Viewed",_o="Desktop Onboarding Permissions Requested",Eo="Received Desktop Notification",uo="Clicked desktop Notification",po="Desktop Notification Permission Prompt Accepted",lo="Desktop Notifications Notification Click",To="Start Recording button clicked on canvas",Oo="Speaker notes toggled",So="Speaker notes moved",Ro="Speaker notes resized",Co="Failed video successfully recovered",Ct="desktop_capture_mode_toggle_clicked",Nt="desktop_screenshot_select_area_button_clicked",It="desktop_screenshot_capture_shortcut_pressed",mt="desktop_screenshot_capture_mode_entered",Dt="desktop_screenshot_capture_cancelled",gt="desktop_screenshot_capture_completed",yt="desktop_screenshot_capture_failed",At="desktop_screenshot_preview_edit_in_loom_clicked",ft="desktop_screenshot_preview_dragged_to_upload",ht="desktop_screenshot_preview_copy_link_clicked",bt="desktop_screenshot_preview_kebab_menu_clicked",Pt="desktop_screenshot_preview_download_clicked",vt="desktop_screenshot_preview_copy_image_clicked",Lt="desktop_screenshot_preview_retake_image_clicked",Ut="desktop_screenshot_preview_delete_image_clicked",wt="desktop_screenshots_keyboard_shortcut_set",No="desktop_tooltip_screenshots_button_clicked",ar="desktop_tooltip_screenshots_dismissed",Io="desktop_screenshots_shortcut_onboarding_step_completed",dr="desktop_screenshots_try_it_ftux_button_clicked",_r="desktop_screenshots_try_it_ftux_dismissed",mo="desktop_meeting_recording_tab_clicked",Do="desktop_meeting_recording_record_meeting_clicked",go="desktop_meeting_recording_record_now_clicked",yo="desktop_meeting_recording_nudge_notification_shown",Ao="desktop_meeting_recording_nudge_notification_clicked",fo="desktop_meeting_recording_nudge_notification_button_clicked",ho="desktop_meeting_recording_nudge_notification_menu_opened",bo="desktop_meeting_recording_nudge_notification_menu_button_clicked",Po="desktop_meeting_recording_reminders_banner_shown",vo="desktop_meeting_recording_reminders_banner_allow_clicked",Lo="desktop_meeting_recording_reminders_banner_dismiss_clicked",Uo="desktop_meeting_recording_reminders_setting_enabled",wo="desktop_meeting_recording_reminders_setting_disabled",ko="desktopMeetingNotes",Mo="desktopMeetingTranscript",Go="desktopMeetingAgent",Bo="desktopMeetingList",Wo="desktopMeetingListDisconnectedState",Ho="meetingRecordingTranscriptButton",xo="meetingRecordingMeetingNotesButton",Ko="meetingRecordingJoinMeetingButton",jo="meetingRecordingRecordToggle",Fo="meetingRecordingRecordNowButton",Vo="meetingRecordingFilter",Yo="meetingRecordingFilterOption",zo="meetingRecordingConnectCalendarButton",Zo="meetingRecordingConfluenceLoginBannerButton",$o="meetingRecordingConnectConfluenceBanner",Xo="meetingRecordingConfluenceLoginBannerSuccess",Qo="meetingNotesOnboardingButton",Jo="meetingNotesOnboardingTourShown",qo="meetingRecordingTabDotIndicator",es="meetingRecordingTabHoverCard",ts="meeting_bot_controls_stop_button_clicked",ns="meeting_bot_controls_pause_button_clicked",os="meeting_bot_controls_resume_button_clicked",ss="meeting_bot_controls_cancel_button_clicked",rs="meeting_bot_controls_cancel_confirmation_cancel_button_clicked",is="meeting_bot_controls_cancel_confirmation_resume_button_clicked",cs="meeting_bot_controls_show_meeting_notes_button_clicked",as="meeting_bot_controls_hide_meeting_notes_button_clicked",ds="meeting_bot_controls_manage_on_loom_button_clicked",_s="meeting_bot_controls_finish_button_clicked",Es="meeting_bot_controls_dismiss_button_clicked",us="Clicked Resize Cam Bubble",ps="Clicked Close Cam Bubble",ls="Clicked Filter Chevron",Ts="Clicked Modify Avatar",Os="Clicked Start Recording Button",Ss="Clicked Home Button",Rs="Clicked Edit Profile",Cs="desktop_close_clicked",Ns="desktop_effects_menu_clicked",Is="desktop_submenu_clicked",ms="Cancel Recording Dialog Confirm",Ds="Cancel Recording Dialog Reject",gs=[Ct,Nt,It,mt,Dt,gt,yt,At,ft,ht,bt,Pt,vt,Lt,Ut,wt],Er=e=>gs.includes(e),ur={[mn]:{action:"Timeout",actionSubject:"desktopBinary",eventType:"operational"},[Dn]:{eventType:"screen"},[gn]:{eventType:"screen"},[yn]:{action:"Updated",actionSubject:"desktopKeyboardShortcuts",eventType:"track"},[An]:{action:"Launch",actionSubject:"desktop",eventType:"operational"},[fn]:{action:"Activated",actionSubject:"desktopMenu",eventType:"operational"},[hn]:{eventType:"screen"},[bn]:{eventType:"screen"},[Pn]:{eventType:"screen"},[vn]:{eventType:"screen"},[Ln]:{action:"Quit",actionSubject:"desktop",eventType:"operational"},[Un]:{action:"Log Out",actionSubject:"desktop",eventType:"operational"},[wn]:{action:"Clicked",actionSubject:"proTag",eventType:"ui"},[kn]:{action:"Activated",actionSubject:"desktopConfetti",eventType:"track"},[Mn]:{action:"User Canceled Failed Retries ",actionSubject:"uploader",eventType:"track"},[Gn]:{action:"User Attempted Failed Retries",actionSubject:"uploader",eventType:"track"},[Bn]:{action:"Engaged",actionSubject:"rbacRestriction",eventType:"operational"},[Wn]:{action:"Rendered",actionSubject:"desktopCameraBubble",eventType:"operational"},[Hn]:{action:"Critical Error While Recording",actionSubject:"desktopRecorder",eventType:"operational"},[xn]:{action:"Stop",actionSubject:"desktopRecorder",eventType:"operational"},[Ot]:{action:"Clicked",actionSubject:"desktopCountdown",eventType:"ui"},[St]:{action:"Clicked",actionSubject:"desktopCountdown",eventType:"ui"},[xe]:{action:"Clicked",actionSubject:"desktopCountdown",eventType:"ui"},[Rt]:{action:"Clicked",actionSubject:"desktopCountdown",eventType:"ui"},[Kn]:{action:"Capture Shortcut Pressed",actionSubject:"desktopScreenshot",eventType:"ui"},[jn]:{action:"Capture Started",actionSubject:"desktopScreenshot",eventType:"operational"},[Fn]:{action:"Capture Completed",actionSubject:"desktopScreenshot",eventType:"operational"},[Vn]:{action:"Capture Failed",actionSubject:"desktopScreenshot",eventType:"operational"},[Yn]:{action:"Capture Cancelled",actionSubject:"desktopScreenshot",eventType:"operational"},[zn]:{action:"Upload Started",actionSubject:"desktopScreenshot",eventType:"operational"},[Zn]:{action:"Upload Completed",actionSubject:"desktopScreenshot",eventType:"operational"},[$n]:{action:"Upload Failed",actionSubject:"desktopScreenshot",eventType:"operational"},[Xn]:{action:"Keyboard Shortcut Used",actionSubject:"restartRecording",eventType:"ui"},[Qn]:{action:"Rejected",actionSubject:"desktopRestartPrompt",eventType:"track"},[Jn]:{action:"Confirmed",actionSubject:"deskopRestartPrompt",eventType:"track"},[qn]:{action:"Quit During Recording",actionSubject:"desktop",eventType:"operational"},[eo]:{action:"Received",actionSubject:"desktopSrt",eventType:"operational"},[to]:{action:"Shared Auth Successful",actionSubject:"desktop",eventType:"operational"},[no]:{action:"Initiated",actionSubject:"desktopSharedAuth",eventType:"operational"},[oo]:{action:"Triggered",actionSubject:"desktopSharedAuthWelcomeFlow",eventType:"operational"},[so]:{action:"Start Failed User Restart",actionSubject:"desktopRecording",eventType:"track"},[ro]:{action:"Start Failed User Quit",actionSubject:"desktopRecording",eventType:"track"},[io]:{action:"Quick During Recording Confirmed",actionSubject:"desktopRecording",eventType:"track"},[co]:{action:"Started",actionSubject:"desktopOnboarding",eventType:"operational"},[ao]:{action:"Viewed",actionSubject:"desktopOnboardingStep",eventType:"operational"},[_o]:{action:"Requested",actionSubject:"desktopOnboardingPermissions",eventType:"operational"},[Eo]:{action:"Received",actionSubject:"desktopNotification",eventType:"operational"},[uo]:{action:"Clicked",actionSubject:"desktopNotification",eventType:"ui"},[po]:{action:"Permission Prompt Accepted",actionSubject:"desktopNotification",eventType:"track"},[lo]:{action:"Notification Click",actionSubject:"desktopNotification",eventType:"ui"},[To]:{action:"Started On Canvas",actionSubject:"desktopRecorder",eventType:"track"},[Oo]:{action:"Toggled",actionSubject:"speakerNotes",eventType:"track"},[So]:{action:"Moved",actionSubject:"speakerNotes",eventType:"track"},[Ro]:{action:"Resized",actionSubject:"speakerNotes",eventType:"track"},[Co]:{action:"Successfully Recovered",actionSubject:"videoRecovery",eventType:"operational"},[Ct]:{action:"Clicked",actionSubject:"captureModeToggle",eventType:"ui"},[Nt]:{action:"Clicked",actionSubject:"selectAreaButton",eventType:"ui"},[It]:{action:"Pressed",actionSubject:"screenshotCaptureShortcut",eventType:"ui"},[mt]:{action:"Entered",actionSubject:"screenshotCaptureMode",eventType:"track"},[Dt]:{action:"Cancelled",actionSubject:"screenshotCaptureMode",eventType:"track"},[gt]:{action:"Completed",actionSubject:"screenshotCapture",eventType:"track"},[yt]:{action:"Failed",actionSubject:"screenshotCapture",eventType:"track"},[At]:{action:"Clicked",actionSubject:"screenshotPreviewEditButton",eventType:"ui"},[ft]:{action:"Dragged",actionSubject:"screenshotPreview",eventType:"ui"},[ht]:{action:"Clicked",actionSubject:"screenshotCopyLinkButton",eventType:"ui"},[bt]:{action:"Clicked",actionSubject:"screenshotPreviewMenuButton",eventType:"ui"},[Pt]:{action:"Clicked",actionSubject:"screenshotDownloadButton",eventType:"ui"},[vt]:{action:"Clicked",actionSubject:"screenshotCopyImageButton",eventType:"ui"},[Lt]:{action:"Clicked",actionSubject:"screenshotRetakeButton",eventType:"ui"},[Ut]:{action:"Clicked",actionSubject:"screenshotDeleteButton",eventType:"ui"},[wt]:{action:"Set",actionSubject:"screenshotShortcut",eventType:"track"},[No]:{action:"Clicked",actionSubject:"screenshotsButtonTooltip",eventType:"ui"},[Io]:{action:"Completed",actionSubject:"screenshotsShortcutOnboardingStep",eventType:"track"},[us]:{action:"Clicked",actionSubject:"resizeCamBubble",eventType:"ui"},[ps]:{action:"Clicked",actionSubject:"closeCamBubble",eventType:"ui"},[ls]:{action:"Clicked",actionSubject:"filterChevron",eventType:"ui"},[Ts]:{action:"Clicked",actionSubject:"modifyAvatar",eventType:"ui"},[Os]:{action:"Clicked",actionSubject:"startRecordingButton",eventType:"ui"},[Ss]:{action:"Clicked",actionSubject:"homeButton",eventType:"ui"},[Rs]:{action:"Clicked",actionSubject:"editProfile",eventType:"ui"},[Cs]:{action:"Clicked",actionSubject:"headerCloseButton",eventType:"ui"},[Ns]:{action:"Clicked",actionSubject:"effectsMenu",eventType:"ui"},[Is]:{action:"Clicked",actionSubject:"submenu",eventType:"ui"},[ms]:{action:"Confirmed",actionSubject:"cancelRecordingDialog",eventType:"track"},[Ds]:{action:"Rejected",actionSubject:"cancelRecordingDialog",eventType:"track"},[mo]:{action:"Clicked",actionSubject:"meetingRecordingsTab",eventType:"ui"},[Do]:{action:"Clicked",actionSubject:"meetingRecordingsRecordMeetingButton",eventType:"ui"},[go]:{action:"Clicked",actionSubject:"meetingRecordingsRecordNowButton",eventType:"ui"},[yo]:{action:"shown",actionSubject:"meetingRecordingsNudgeNotification",eventType:"track"},[Ao]:{action:"clicked",actionSubject:"meetingRecordingsNudgeNotification",eventType:"ui"},[fo]:{action:"clicked",actionSubject:"meetingRecordingsNudgeNotificationButton",eventType:"ui"},[Po]:{action:"Shown",actionSubject:"meetingRemindersBanner",eventType:"ui"},[vo]:{action:"Clicked",actionSubject:"meetingRemindersBannerAllowButton",eventType:"ui"},[Lo]:{action:"Clicked",actionSubject:"meetingRemindersBannerDismissButton",eventType:"ui"},[Uo]:{action:"Clicked",actionSubject:"meetingRemindersSettingsToggleOn",eventType:"ui"},[wo]:{action:"Clicked",actionSubject:"meetingRemindersSettingsToggleOff",eventType:"ui"},[ho]:{action:"opened",actionSubject:"meetingRecordingsNudgeNotificationMenu",eventType:"ui"},[bo]:{action:"clicked",actionSubject:"meetingRecordingsNudgeNotificationMenuButton",eventType:"ui"},[ts]:{action:"clicked",actionSubject:"meetingRecordingStopButton",eventType:"ui"},[ss]:{action:"clicked",actionSubject:"meetingRecordingCancelButton",eventType:"ui"},[ns]:{action:"clicked",actionSubject:"meetingRecordingPauseButton",eventType:"ui"},[os]:{action:"clicked",actionSubject:"meetingRecordingResumeButton",eventType:"ui"},[is]:{action:"clicked",actionSubject:"meetingRecordingConfirmationModalResumeButton",eventType:"ui"},[rs]:{action:"clicked",actionSubject:"meetingRecordingConfirmationModalCancelButton",eventType:"ui"},[cs]:{action:"clicked",actionSubject:"meetingRecordingShowMeetingNotesButton",eventType:"ui"},[as]:{action:"clicked",actionSubject:"meetingRecordingHideMeetingNotesButton",eventType:"ui"},[ds]:{action:"clicked",actionSubject:"meetingRecordingManageOnLoomButton",eventType:"ui"},[_s]:{action:"clicked",actionSubject:"meetingRecordingFinishButton",eventType:"ui"},[Es]:{action:"clicked",actionSubject:"meetingRecordingDismissButton",eventType:"ui"},[ko]:{eventType:"screen"},[Mo]:{eventType:"screen"},[Go]:{eventType:"screen"},[Bo]:{eventType:"screen"},[Wo]:{eventType:"screen"},[Ho]:{action:"clicked",actionSubject:"meetingRecordingTranscriptButton",eventType:"ui"},[xo]:{action:"clicked",actionSubject:"meetingRecordingMeetingNotesButton",eventType:"ui"},[jo]:{action:"set",actionSubject:"meetingRecordingRecordToggle",eventType:"ui"},[Fo]:{action:"clicked",actionSubject:"meetingRecordingRecordNowButton",eventType:"ui"},[Vo]:{action:"opened",actionSubject:"meetingRecordingFilter",eventType:"ui"},[Yo]:{action:"clicked",actionSubject:"meetingRecordingFilterOption",eventType:"ui"},[zo]:{action:"clicked",actionSubject:"meetingRecordingConnectCalendarButton",eventType:"ui"},[$o]:{action:"shown",actionSubject:"meetingRecordingConnectConfluenceBanner",eventType:"track"},[Xo]:{action:"success",actionSubject:"confluenceLogin",eventType:"track"},[Ko]:{action:"clicked",actionSubject:"meetingRecordingJoinMeetingButton",eventType:"ui"},[Zo]:{action:"clicked",actionSubject:"confluenceLoginBanner",eventType:"ui"},[Qo]:{action:"clicked",actionSubject:"meetingRecordingOnboardingTour",eventType:"ui"},[Jo]:{action:"shown",actionSubject:"meetingRecordingOnboardingTour",eventType:"track"},[qo]:{action:"shown",actionSubject:"meetingRecordingTabDotIndicator",eventType:"track"},[es]:{action:"shown",actionSubject:"meetingRecordingTabHoverCard",eventType:"track"}},ue=190,ys=1200,kt=Q.F4`
    0% {
      transform: scale(0.0);
      opacity: 0;
    }
    100% {
      transform: scale(1.0);
      opacity: 1;
    }
`,As=Q.F4`
    0% {
      opacity: 0;
      filter: blur(5px);
    }
    76% {
      opacity: 1;
      filter: blur(0);
    }
    100% {
      opacity: 0;
      filter: blur(5px);
    }
`,fs=f.Z.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 32px;
  justify-content: center;
  opacity: ${e=>e.fadeOut?0:1};
  transition: opacity 0.5s ease;
  pointer-events: ${e=>e.fadeOut?"none":"auto"};
  visibility: ${e=>e.fadeOut?"hidden":"visible"};
`,hs=f.Z.div`
  opacity: ${e=>e.fadeOut?0:1};
  visibility: ${e=>e.fadeOut?"hidden":"visible"};
`,bs=f.Z.div`
  position: relative;
  display: inline-block;
  width: ${ue}px;
  height: ${ue}px;
  cursor: pointer;

  ${e=>!e.paused&&`
    &:hover .inner-circle {
      opacity: 1;
    }

    &:hover .pause-text {
      opacity: 1;
    }
  `}

  ${e=>e.paused&&`
    .resume-circle {
      opacity: 1 !important;
    }
    .resume-icon {
      opacity: 1 !important;
    }
    .resume-text {
      opacity: 1 !important;
    }
    .countdown-text {
      opacity: 0 !important;
      visibility: hidden !important;
      display: none !important;
    }
  `}
`,Mt=f.Z.div`
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: ${ue/2}px;
  width: ${ue}px;
  height: ${ue}px;
  background: linear-gradient(
    180deg,
    rgba(70, 136, 236, 0.7) 0%,
    rgba(24, 104, 219, 0.7) 100%
  );
  box-shadow:
    0px 2px 2px rgb(147 130 178 / 20%),
    0px 2px 40px rgb(147 130 178 / 20%);
  position: relative;
  cursor: pointer;

  animation: ${kt} 750ms cubic-bezier(0.45, 0, 0.4, 1);
`,Ps=(0,f.Z)(Mt)`
  opacity: 0;
  animation: ${kt} 750ms cubic-bezier(0.45, 0, 0.4, 1) reverse;
  animation-iteration-count: 1;
  animation-fill-mode: forwards;
`,Gt=f.Z.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
`,Ke=(0,f.Z)(Gt)`
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
`,Bt=(0,f.Z)(Gt)`
  opacity: 0;
  font-size: 115px;
  font-weight: 500;
  line-height: 155px;
  color: var(--lns-color-white);
  transition: opacity 0.3s ease;

  animation: none;

  ${e=>e.count===1&&"transform: translate(calc(-50% - 6px), -50%);"}

  &.run-animation-1, &.run-animation-2, &.run-animation-3 {
    animation: ${As};
    animation-duration: ${ys}ms;
    animation-delay: 425ms;
    animation-timing-function: cubic-bezier(0.45, 0, 0.4, 1);
    animation-iteration-count: infinite;
  }
`,Wt=(0,f.Z)(Ke)`
  border-radius: 50%;
  background: linear-gradient(
    180deg,
    rgba(27, 49, 96, 0.8) 0%,
    rgba(12, 52, 110, 0.8) 100%
  );
  box-shadow:
    0px 2px 2px rgb(147 130 178 / 20%),
    0px 2px 40px rgb(147 130 178 / 20%);
`,vs=(0,f.Z)(Wt)`
  width: 160px;
  height: 160px;
`,Ls=(0,f.Z)(Wt)`
  width: 100%;
  height: 100%;
  background: linear-gradient(
    180deg,
    rgba(27, 49, 96, 0.6) 0%,
    rgba(12, 52, 110, 0.6) 100%
  );
`,Ht=(0,f.Z)(Ke)`
  top: 60%;
  transform: translate(-50%, calc(-50% + 40px));
  color: white;
  font-size: 14px;
  font-weight: bold;
  font-family: inherit;
`,Us=(0,f.Z)(Ke)`
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;

  svg {
    width: 80px;
    height: 80px;
    color: white;
  }
`;function ws({count:e,fadeOut:i,paused:E}){const b=(0,s.I0)(),L=()=>{ye(Rt,{countdownValue:e}),setTimeout(()=>{b((0,m.mk)(!0,Ie.KeyboardShortcutClicked))},50)},K=()=>{ye(xe,{countdownValue:e}),b((0,_e.nH)())};if(e===null)return t.createElement(t.Fragment,null);const J=`run-animation-${e}`,Ae=e===0||i;return t.createElement(t.Fragment,null,t.createElement(fs,{fadeOut:i},e>0&&t.createElement(pt,{icon:t.createElement(un.G,null),text:"Cancel",onClick:L}),t.createElement(bs,{paused:E},Ae?t.createElement(Ps,null,t.createElement(Bt,{count:e,paused:E},e)):t.createElement(t.Fragment,null,t.createElement(Mt,null,t.createElement(vs,{className:"inner-circle"}),t.createElement(Ht,{className:"pause-text"},"Pause"),t.createElement(Ls,{className:"resume-circle"}),t.createElement(Us,{className:"resume-icon"},t.createElement(ln.y,null)),t.createElement(Ht,{className:"resume-text"},"Resume")),t.createElement(Bt,{count:e,paused:E,className:`${J} countdown-text`,"data-qa":"countdown-text"},e))),e>0&&t.createElement(pt,{icon:t.createElement(pn.K,null),text:"Skip",onClick:K,rotateIcon:!0})),t.createElement(hs,{fadeOut:Ae},t.createElement(ut,{count:e,marginTop:"24px"})))}const je=190,ks=1200,Fe=Q.F4`
    0% {
      transform: scale(0.0);
      opacity: 0;
    }
    100% {
      transform: scale(1.0);
      opacity: 1;
    }
`,Ms=Q.F4`
    0% {
      opacity: 0;
      filter: blur(5px);
    }
    76% {
      opacity: 1;
      filter: blur(0);
    }
    100% {
      opacity: 0;
      filter: blur(5px);
    }
`,Gs=Q.F4`
  0% {
		transform: rotate(0);
	}
	100% {
		transform: rotate(360deg);
	}
`,xt=f.Z.div`
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: ${je/2}px;
  width: ${je}px;
  height: ${je}px;
  margin-bottom: 60px;
  background: linear-gradient(
    180deg,
    rgba(70, 136, 236, 0.7) 0%,
    rgba(24, 104, 219, 0.7) 100%
  );
  box-shadow:
    0px 2px 2px rgb(147 130 178 / 20%),
    0px 2px 40px rgb(147 130 178 / 20%);

  animation:
    ${Fe} 750ms cubic-bezier(0.45, 0, 0.4, 1),
    ${Gs} 4000ms linear 500ms forwards;
`,Bs=(0,f.Z)(xt)`
  opacity: 0;
  animation: ${Fe} 750ms cubic-bezier(0.45, 0, 0.4, 1) reverse;
  animation-iteration-count: 1;
  animation-fill-mode: forwards;
`,Ws=f.Z.div`
  opacity: 0;
  font-size: 115px;
  font-weight: 500;
  line-height: 155px;
  letter-spacing: 0px;
  color: var(--lns-color-white);
  position: relative;
  top: -245px;

  animation: none;

  ${e=>e.count===1&&"left: -6px;"}

  ${e=>e.paused&&`
    opacity: 1 !important;
    filter: blur(0) !important;
    animation-play-state: paused !important;
  `}

  &.run-animation-1, &.run-animation-2, &.run-animation-3 {
    animation: ${Ms};
    animation-duration: ${ks}ms;
    animation-delay: 425ms;
    animation-timing-function: cubic-bezier(0.45, 0, 0.4, 1);
    animation-iteration-count: infinite;
    animation-play-state: ${e=>e.paused?"paused":"running"};
  }
`,Hs=f.Z.div`
  opacity: 0;
  font-weight: 700;
  letter-spacing: 0px;
  color: var(--lns-color-white);
  position: relative;
  top: -255px;
  cursor: pointer;
  animation: ${Fe} 750ms cubic-bezier(0.45, 0, 0.4, 1) forwards;
`;function xs({count:e,fadeOut:i,paused:E,onSkipClick:b}){if(e===0||i)return t.createElement(Bs,null);const L=E?"":`run-animation-${e}`;return t.createElement(t.Fragment,null,t.createElement(xt,null),t.createElement(Ws,{count:e,paused:E,className:L,"data-qa":"countdown-text"},e),t.createElement(Hs,{onClick:b},"Skip"))}const Ks=f.Z.div`
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.75);
`,js=f.Z.div`
  user-select: none;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  cursor: pointer;
`;function Fs({count:e,fadeOut:i,paused:E,onPauseClick:b,onSkip:L}){const K=ge(De.COUNTDOWN_TIMER_UPDATE_DESKTOP,!1);return t.createElement(Ks,{"data-qa":"countdown-overlay",onClick:b},t.createElement(js,null,K?t.createElement(ws,{count:e,fadeOut:i,paused:E}):t.createElement(t.Fragment,null,e!==null&&t.createElement(xs,{count:e,fadeOut:i,paused:E,onSkipClick:L}),e!==null&&e>0&&t.createElement(ut,{count:e}),e!==null&&e>0&&t.createElement(me.xvT,{size:"body-md",color:"white",fontWeight:"bold",style:{position:"relative",top:"-137px"}},E?"Click anywhere to unpause countdown":"Click anywhere to pause countdown"))))}function Vs(){return(0,s.v9)(e=>({countdown:e.countdown.countdown,visibility:e.countdown.visibility_state,paused:e.countdown.paused}))}function pr(){return useSelector(e=>e.countdown.visibility_state)}const Ys=de("countdown-wrapper"),zs=f.Z.div`
  align-items: center;
  justify-content: center;

  display: flex;

  overflow: hidden;

  margin: 0;
  width: 100%;
  height: 100%;

  cursor: default;

  user-select: none;
  background-color: var(--lns-themeLight-color-bodyDimmed);
  color: var(--lns-color-white);
`;function Zs(){const[e,i]=(0,t.useState)(!1),E=(0,s.I0)(),{countdown:b,visibility:L,paused:K}=Vs(),J=()=>{ye(xe,{countdownValue:b}),i(!0),E((0,_e.nH)()),setTimeout(()=>{i(!1)},500)},Ae=()=>{ye(K?St:Ot,{countdownValue:b}),E((0,_e.Ty)())};return(0,t.useEffect)(()=>{L===Ue.l.Opening&&(Ys.info("countdown-wrapper firing updateCountdownState(OPEN)"),E((0,_e.HP)(Ue.l.Open)))},[E,L]),(0,t.useEffect)(()=>{const Ft=Qs=>{Qs.key==="Escape"&&E((0,m.mk)(!0,Ie.KeyboardShortcutClicked))};return window.addEventListener("keydown",Ft),()=>{window.removeEventListener("keydown",Ft)}},[E]),t.createElement(zs,null,t.createElement(Fs,{count:b,onSkip:J,fadeOut:e,paused:K,onPauseClick:Ae}))}z(),X("countdown"),(0,re.u)();const Kt=document.createElement("div"),jt="container-countdown";Kt.id=jt,document.body.appendChild(Kt),document.title=V;const $s=document.getElementById(jt),Xs=oe(se.Q,[]);In(V),(e=>(0,r.render)(t.createElement(s.zt,{store:Xs},t.createElement(e,null)),$s))(Zs)},974144:(o,_,n)=>{var t=Object.defineProperty,r=Object.getOwnPropertySymbols,s=Object.prototype.hasOwnProperty,a=Object.prototype.propertyIsEnumerable,c=(S,y,h)=>y in S?t(S,y,{enumerable:!0,configurable:!0,writable:!0,value:h}):S[y]=h,l=(S,y)=>{for(var h in y||(y={}))s.call(y,h)&&c(S,h,y[h]);if(r)for(var h of r(y))a.call(y,h)&&c(S,h,y[h]);return S};const T=n(172298),N=n(371017),g="electron"in process.versions,p=process&&process.type==="renderer",u={is:{renderer:p,main:!p,get development(){return p?T.ipcRenderer.sendSync("electron-is-dev"):U()},usingAsar:g&&process.mainModule&&process.mainModule.filename.includes("app.asar")}},O=l(l({},u.is),p?G():k());function I(S){return O.usingAsar?N.join(process.resourcesPath,S):S}function m(){if(!O.main)return;const S=n(657147),y=n(371017),h=n(172298).app,B=y.join(h.getPath("userData"),".electron-util--has-app-launched");if(S.existsSync(B))return!1;try{S.writeFileSync(B,"")}catch(H){if(H.code==="ENOENT")return S.mkdirSync(h.getPath("userData")),m()}return!0}function P(S){S||T.ipcMain.on("electron-is-dev",y=>{y.returnValue=U()})}function k(){const S=process.platform;return{windows:S==="win32",macos:S==="darwin"}}function G(){const S=window.navigator.platform;return{windows:S.match(/win32/i),macos:S.match(/Mac/i)}}function U(){const S="ELECTRON_IS_DEV"in process.env,y=Number.parseInt(process.env.ELECTRON_IS_DEV,10)===1;return S?y:!T.app.isPackaged}P(p),o.exports={is:O,fixPathForAsarUnpack:I,isFirstAppLaunch:m}},23405:(o,_,n)=>{"use strict";n.d(_,{L9:()=>T,Qs:()=>N,wo:()=>O});var t=n(346972);const r="track-event",s="identify-event",a="page-event",c="get-anon-id",l="ui-viewed-event",T=(0,t.eH)(r,({name:m,props:P})=>({type:r,payload:{name:m,props:P}})),N=(0,t.eH)(a,({name:m})=>({type:a,payload:{name:m}})),g=(0,t.eH)(s,({userId:m,traits:P})=>({type:s,payload:{userId:m,traits:P}})),p=(0,t.eH)(l,()=>({type:l})),u=(0,t.eH)(c,()=>({type:c})),O="update-analytics-anonymous-id",I=m=>({type:O,payload:{id:m}})},212849:o=>{o.exports.KL="https://c67368549d804bc989bba1b3cb1a0471@o398470.ingest.sentry.io/5599205",o.exports.Sd="mac",o.exports.HV="win",o.exports.Zb="LoomStaging",o.exports.zl="Loom"},987771:(o,_,n)=>{"use strict";n.d(_,{h:()=>t});let t;function r(a){t=a}function s(a){return new Promise(c=>{const l=t.getState();if(a(l)){c(l);return}const T=t.subscribe(()=>{const N=t.getState();a(N)&&(T(),c(N))})})}},879741:(o,_,n)=>{"use strict";n.d(_,{Gv:()=>a,v9:()=>O,ar:()=>m});var t=n(974144),r=n.n(t);const s="Loom",a="production",c="development",l="production",T="staging",N="desktop",g=a===c,p=a===l,u=a===T,O=a===c||t.is.development,I=a===l&&!t.is.development,m=a===T&&!t.is.development,P=a===l&&t.is.development,k="false"},163224:(o,_,n)=>{"use strict";n.d(_,{hr:()=>t,so:()=>r,dg:()=>a,Qp:()=>c,QN:()=>l,h0:()=>T});const t="show-contextual-onboarding",r="close-contextual-onboarding",s="update-seen-contextual-onboarding",a="set-contextual-onboarding-feature",c="set-contextual-onboarding-step",l="set-contextual-onboarding-display-bounds",T="reset-contextual-onboarding",N=P=>({type:a,payload:P}),g=P=>({type:c,payload:P}),p=()=>({type:t}),u=()=>({type:r}),O=()=>({type:s}),I=P=>({type:l,payload:P}),m=()=>({type:T})},955649:(o,_,n)=>{"use strict";n.d(_,{MC:()=>t,FZ:()=>r,W5:()=>s,XB:()=>a,iC:()=>c,RG:()=>T,si:()=>N,ip:()=>g});const t="enter-drawing-mode",r="exit-drawing-mode",s="show-drawing-tools",a="update-control-menu-placement",c="set-control-menu-size",l="update-control-menu-size",T="update-control-menu-position",N="update-control-menu-id",g="update-current-size",p=S=>({type:N,payload:{windowId:S}}),u=S=>({type:g,payload:{size:S}}),O=({width:S,height:y,sizeType:h})=>({type:c,payload:{width:S,height:y,sizeType:h}}),I=S=>({type:l,payload:{sizeType:S}}),m=()=>({type:t}),P=()=>({type:r}),k=()=>({type:s,payload:{at:Date.now()}}),G=S=>({type:a,payload:{placement:S}}),U=(S,y)=>({type:T,payload:{x:S,y}})},599682:(o,_,n)=>{"use strict";n.d(_,{HB:()=>t,_4:()=>r,G_:()=>s,mi:()=>a,AH:()=>c,Fx:()=>l,HP:()=>T,nH:()=>N,Ty:()=>O});const t="update-countdown-state",r="reset-countdown",s="set-countdown-for-start",a="skip-countdown",c="update-countdown",l="toggle-countdown-pause",T=I=>({type:t,payload:{visibilityState:I}}),N=()=>({type:a}),g=()=>({type:r}),p=I=>({type:c,payload:{countdown:I}}),u=()=>({type:s}),O=()=>({type:l})},621678:(o,_,n)=>{"use strict";n.d(_,{JW:()=>s,p2:()=>a,NR:()=>c});var t=n(346972);const r="push-back-overlay",s="cropping-window-ready",a="cropping-window-close",c="exit-cropping",l="first-crop",T=()=>({type:s}),N=()=>({type:a}),g=(0,t.eH)(r,()=>({type:r})),p=()=>({type:c}),u=()=>({type:l})},858470:(o,_,n)=>{"use strict";n.d(_,{Aw:()=>t,M4:()=>r,dZ:()=>s});const t="drawing-line-start",r="update-brush-size",s="update-drawing-color",a=T=>({type:s,payload:{color:T}}),c=T=>({type:r,payload:{size:T}}),l=()=>({type:t})},185335:(o,_,n)=>{"use strict";n.d(_,{eE:()=>t,Jg:()=>r});const t="open-feature-nudge",r="close-feature-nudge",s=c=>({type:t,payload:c}),a=(c=!0)=>({type:r,payload:c})},257728:(o,_,n)=>{"use strict";n.d(_,{O_:()=>c,Ji:()=>l,U6:()=>T});var t=n(450630),r=n(284558),s=(N=>(N.MEETING_NOTES="meeting-notes",N))(s||{});const a={["meeting-notes"]:r._v},c={nudge:{fadeIn:{seconds:.15,milliseconds:150},fadeOut:{seconds:.15,milliseconds:150}},contextualOnboarding:{fadeIn:{seconds:.4,milliseconds:400},fadeOut:{seconds:.4,milliseconds:400}}},l=t.F4`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`,T=t.F4`
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
`},881863:(o,_,n)=>{"use strict";var t=(r=>(r.LoggedOut="logged-out",r.Minimized="minimized",r.Idle="idle",r.IdleNoScreenshotFtux="idle_no_screenshot_ftux",r.ContextualOnboarding="contextual-onboarding",r.Countdown="countdown",r.Recording="recording",r.Onboarding="onboarding",r.Cropping="cropping",r.Meetings="meetings",r.MeetingsV2="meetings-v2",r.MeetingNotes="meeting-notes",r.MeetingOnboarding="meeting-onboarding",r.SelectingScreenshot="selecting-screenshot",r.MenuSelectScreenshot="menu-select-screenshot",r.ScreenshotShortcutSetup="screenshot-shortcut-setup",r.ScreenshotShortcutSetupCompleted="screenshot-shortcut-setup-completed",r.ScreenshotTryItFtux="screenshot-try-it-ftux",r))(t||{})},826565:(o,_,n)=>{"use strict";var t=n(565327);const r=(0,t.PH)("maestro/set-state")},957023:(o,_,n)=>{"use strict";n.d(_,{Py:()=>c,Zc:()=>l,K3:()=>T,d_:()=>N,Rm:()=>g,OC:()=>p,_Q:()=>u,hv:()=>O,_3:()=>P,c7:()=>k,at:()=>G,Wd:()=>S,Bz:()=>h,H4:()=>B,TU:()=>j,fP:()=>A,xe:()=>D,MP:()=>z,VB:()=>ee});var t=n(206687),r=n(42022),s=n(826565),a=n(881863);const c="update-after-display-page",l="update-pre-recording-panel-visibility-state",T="update-pre-recording-panel-page",N="update-pre-recording-panel-state",g="update-crop-type",p="update-crop-type-data",u="my-videos-hide-tooltip",O="my-videos-video-recorded",I="lower-pre-recording-bar",m="reset-system-tray",P="set-pre-recordging-panel-focus",k="update-pre-recording-panel-location",G="update-pre-recording-panel-bounds",U="check-display-screenshot-shortcut-setup",S="update-ready-to-show-screenshot-shortcut-setup",y="check-display-screenshot-try-it-ftux",h="update-ready-to-show-screenshot-try-it-ftux",B="update-pre-recording-panel-id",H="update-pre-recording-panel-native-window-id",j="update-pre-recording-panel-visibility",A="update-pre-recording-panel-disabled",D="set-window-selection-overlay-active",W=R=>({type:D,payload:{active:R}}),q="set-has-seen-filters-ftux",z="set-has-completed-meeting-notes-onboarding",ee="set-has-queried-recorder-amn-eligibility",te=(R,Y)=>({type:k,payload:{x:R,y:Y}}),ne=R=>({type:G,payload:R}),pe=R=>({type:B,payload:{id:R}}),le=R=>({type:H,payload:{id:R}}),Te=R=>({type:j,payload:{isVisible:R}}),Oe=()=>({type:I}),F=R=>({type:c,payload:{afterDisplayPage:R}}),oe=R=>({type:l,payload:{visibilityState:R}}),se=R=>({type:P,payload:{inFocus:R}}),re=R=>({type:T,payload:{page:R}}),$=R=>({type:N,payload:{state:R}}),ie=R=>({type:p,payload:{type:R}}),x=({msgType:R,active:Y})=>({type:UPDATE_MESSAGE_STATUS,payload:{msgType:R,active:Y}}),X=({readyToShow:R})=>({type:S,payload:{readyToShow:R}}),M=({readyToShow:R})=>({type:h,payload:{readyToShow:R}}),Se=(R,Y=!1)=>V=>{R===SCREEN_CROP.CUSTOM_SIZE&&(V(updateCropRect(null)),V(setMaestroState(MaestroState.Cropping))),V({type:g,payload:{type:R,startAfterCropping:Y}}),R===SCREEN_CROP.FULL_SCREEN&&V(updateCropRect(null))},Re=()=>({type:u}),ce=()=>({type:O}),ae=()=>({type:m}),Ce=()=>({type:U}),Ne=()=>({type:y}),de=(R=!1)=>({type:A,payload:{isDisabled:R}}),he=R=>({type:q,payload:{seen:R}}),be=R=>({type:z,payload:{completed:R}}),Pe=R=>({type:ee,payload:{queried:R}})},42022:(o,_,n)=>{"use strict";n.d(_,{P2:()=>s,bV:()=>l,Br:()=>p,iK:()=>u,bA:()=>U});const t="hidden",r="hiding",s="fresh-launch",a="open",c="opening",l={width:400,height:280},g=["display-selector","window-selector"],p={FULL_SCREEN:"full-screen",WINDOW:"window",CUSTOM_SIZE:"custom-size"},u="back-to-normal",O="to-start-recording",I="to-crop-type",m="to-crop-type-window",P="to-crop-type-custom-size",k="video-tab",G="screenshot-tab";var U=(D=>(D.normalView="normalView",D.normalViewWithMenu="normalViewWithMenu",D.normalViewWithMsgType="normalViewWithMsgType",D.normalViewWithMsgTypeMenu="normalViewWithMsgTypeMenu",D.effectsView="effectsView",D.canvasView="canvasView",D.notificationsView="notificationsView",D.windowSelectorView="windowSelectorView",D.displaySelectorView="displaySelectorView",D.meetingsView="meetingsView",D.settingsView="settingsView",D.aboutView="aboutView",D.updatesView="updatesView",D.alertsView="alertsView",D.loginView="loginView",D))(U||{});const S=D=>D==="normalViewWithMsgType"||D==="normalViewWithMsgTypeMenu",y=D=>D==="normalViewWithMenu"||D==="normalViewWithMsgTypeMenu",A={normalView:{width:320,height:590},normalViewWithMenu:{width:620,height:760},normalViewWithMsgType:{width:320,height:770},normalViewWithMsgTypeMenu:{width:620,height:940},effectsView:{width:400,height:554},canvasView:{width:400,height:520},notificationsView:{width:460,height:600},windowSelectorView:{width:400,height:463},displaySelectorView:{width:400,height:503},settingsView:{width:400,height:700},aboutView:{width:320,height:500},updatesView:{width:320,height:560},alertsView:{width:400,height:490},loginView:{width:400,height:700},meetingsView:{width:440,height:540}}},625507:(o,_,n)=>{"use strict";n.d(_,{s:()=>t,Z:()=>r});var t=(s=>(s.normal="normal",s.displaySelector="display-selector",s.windowSelector="window-selector",s.effects="effects",s.canvas="canvas",s.notifications="notifications",s.screenshot="screenshot",s.speakerNotes="speakerNotes",s.meetings="meetings",s.settings="settings",s.preferences="preferences",s.about="about",s.updates="updates",s.alerts="alerts",s.login="login",s.meetingsV2="meetingsV2",s))(t||{}),r=(s=>(s.WORKSPACE_UNAVAILABLE="workspaceUnavailable",s.NOT_AUTHORIZED_TO_CREATE_VIDEOS="notAuthorizedToCreateVideos",s.RECORD_BUTTON_FAILED="recordButtonFailed",s.OUT_OF_DISK_SPACE="outOfDiskSpace",s.MIC_ISSUE="micIssue",s.DOWNTIME="downtime",s.OS_PERMISSION_ISSUE="osPermissionIssue",s.WINDOWS_NEED_MIC_PERMISSION="windowsNeedMicPermission",s.CAM_ISSUE="camIssue",s.MIC_ISSUE_MUTED="micIssueMuted",s.WEAK_INTERNET_CONNECTION="weakInternetConnection",s.INTERNAL_AUDIO_TIP="internalAudioTip",s.FEATURE_BANNER="featureBanner",s.CUSTOMER_COMMUNICATION="customerCommunication",s.DEVICE_IN_USE="deviceInUse",s))(r||{})},717852:(o,_,n)=>{"use strict";n.d(_,{Sk:()=>t,Gp:()=>r,Qq:()=>s});const t="update-actively-changing",r="update-preferences",s="update-preferences-default",a="report-cam-split-toggle",c="report-camera-bubble-quality-selected",l=u=>({type:t,payload:{changing:u}}),T=(u,O=!0,I=!1)=>({type:r,payload:{preferences:u,storeChange:O,appIsLoading:I}}),N=u=>({type:s,payload:{preferences:u}}),g=u=>({type:a,payload:{value:u}}),p=u=>({type:c,payload:{quality:u}})},206687:(o,_,n)=>{"use strict";n.d(_,{p4:()=>r,$O:()=>s,JC:()=>a,bk:()=>l,Fh:()=>T,S3:()=>N,p1:()=>g,mB:()=>p,mz:()=>u,Uy:()=>O,M9:()=>I,HX:()=>m,VG:()=>P,MK:()=>k,vV:()=>G,BR:()=>U,l1:()=>y,Qc:()=>h,q6:()=>B,Hd:()=>H,UY:()=>j,vc:()=>A,g7:()=>D,L0:()=>W,jA:()=>q,IL:()=>z,Ju:()=>ee,$G:()=>te,zJ:()=>ne,zE:()=>pe,Wu:()=>le,KT:()=>Te,Vs:()=>Oe,n9:()=>F,gQ:()=>oe,IJ:()=>$,C7:()=>x,cO:()=>X,th:()=>M,Oh:()=>Se,zF:()=>ce,WR:()=>ae,MT:()=>Ce,mk:()=>Le});var t=n(346972);const r="add-window-id-to-hide",s="select-video-recording-device",a="set-recording-file-path",c="start-recording-failure",l="start-recording-success",T="update-active-window-title",N="update-all-displays",g="update-recorder-prompt-state",p="update-current-recording-devices",u="update-crop-rect",O="update-current-display",I="update-has-selected-display",m="update-is-cropping",P="update-is-recording",k="update-mic-on",G="update-recording-devices",U="update-recording-type",S="update-recording-type-selection",y="reset-recording-state",h="update-selected-window",B="clear-selected-window",H="update-msg-type-status",j="update-session",A="update-show-selector-window",D="update-starting-recording",W="update-stopping-recording",q="update-windows",z="show-muted-mic-warn",ee="hide-muted-mic-warn",te="set-recording-time-elapsed",ne="update-internal-audio-status",pe="update-waiting-on-install",le="set-start-recording-request-time-ms",Te="set-recording-mode",Oe="set-recording-alert",F="reset-recording-alert",oe="reset-all-recording-alerts",se="cancel-recording",re="restart-recording",$="error-recording",ie="get-display-screenshots",x="get-windows",X="select-audio-recording-device",M="start-recording",Se="select-preferred-video-device",Re="after-stop-recording",ce="stop-recording",ae="update-recording-paused",Ce="update-recording-cancelled",Ne="get-internal-audio-status",de="install-system-audio",he=d=>({type:g,payload:{state:d}}),be=d=>({type:r,payload:{candidate:d}}),Pe=d=>({type:le,payload:{timestampMs:d}}),R=d=>({type:te,payload:{recordingTimeElapsed:d}}),Y=()=>({type:z,payload:{}}),V=(0,t.eH)(X,d=>({type:X})),ze=d=>({type:s,payload:{device:d}}),Ze=({audioDevice:d,videoDevice:w,selectedAudioDevices:Be,selectedVideoDevices:ge,updateStore:We=!0})=>({type:p,payload:{audioDevice:d,videoDevice:w,selectedAudioDevices:Be,selectedVideoDevices:ge,updateStore:We}}),Vt=({audioDevices:d,videoDevices:w})=>({type:G,payload:{audioDevices:d,videoDevices:w}}),$e=d=>({type:U,payload:{recordingType:d}}),Xe=d=>({type:S,payload:{recordingType:d}}),Qe=d=>({type:a,payload:{path:d}}),Je=d=>({type:T,payload:{title:d}}),qe=(d,w=!1)=>({type:N,payload:{displays:d},meta:{updatingWithScreenshots:w}}),et=(d=!1)=>({type:A,payload:{show:d}}),tt=(d=[])=>({type:q,payload:{windows:d}}),ve=(d=null)=>({type:u,payload:{cropRect:d}}),nt=d=>({type:j,payload:{session:d}}),ot=d=>({type:I,payload:{selected:d}}),st=d=>({type:m,payload:{isCropping:d}}),rt=d=>({type:P,payload:{isRecording:d}}),it=d=>({type:D,payload:{starting:d}}),ct=d=>({type:W,payload:{stopping:d}}),Yt=d=>({type:Ce,payload:{cancelSource:d}}),zt=d=>({type:k,payload:{on:d}}),Zt=()=>({type:y}),$t=()=>({type:B}),Xt=(0,t.eH)(h,(d,w=!1)=>({type:h})),at=()=>d=>{d(ve(null)),d(_t())},Le=(0,t.eH)(se,(d=!1,w)=>({type:se})),dt=(0,t.eH)(re,(d=!1)=>({type:re})),Qt=(0,t.eH)($,(d="unknown recording error")=>({type:$})),Jt=(0,t.eH)(x,(d=!0)=>({type:x})),qt=(0,t.eH)(O,(d,w=!1)=>({type:O})),_t=(0,t.eH)(M,(d=!1,w=!1)=>({type:M})),f=(0,t.eH)(ae,d=>({type:ae})),_e=(0,t.eH)(ce,d=>({type:ce})),Ie=(0,t.eH)(Re,(d,w,Be)=>({type:"after-recorder-stopped"})),Ue=(0,t.eH)(A,(d=!0)=>({type:A})),en=(0,t.eH)(ie,()=>({type:ie})),me=d=>({type:ne,payload:{installed:d}}),we=d=>({type:pe,payload:{waiting_on_install:d}}),De=(0,t.eH)(Ne,d=>({type:Ne})),ke=(0,t.eH)(de,(d=!1)=>({type:de})),Me=({recordingMode:d,storeValue:w=!0})=>({type:Te,payload:{recordingMode:d,storeValue:w}}),Et=d=>({type:F,payload:{alert:d}}),Ge=()=>({type:oe}),tn=d=>({type:Oe,payload:{alert:d}})},903285:(o,_,n)=>{"use strict";n.d(_,{yy:()=>t.yyj,o_:()=>r,pC:()=>s});var t=n(390620),r=(c=>(c.FullScreen="fullScreen",c.Window="window",c.CustomSize="customSize",c.CamOnly="camOnly",c.Screenshot="screenshot",c))(r||{}),s=(c=>(c.micMuted="micMuted",c.signIn="signIn",c.needPermissions="needPermissions",c.oldOSVersion="oldOSVersion",c.updateRequired="updateRequired",c.offline="offline",c.diskSpace="diskSpace",c.diskSpaceCritical="diskSpaceCritical",c.verifyEmail="verifyEmail",c.videoLimitReached="videoLimitReached",c.cantWriteToDisk="cantWriteToDisk",c.incorrectMacDownload="incorrectMacDownload",c))(s||{});const a=[t.yyj.ScreenCam,t.yyj.Screen]},645864:(o,_,n)=>{"use strict";n.d(_,{mK:()=>r,mC:()=>s,i:()=>a});var t=n(346972);const r="update-auto-resolution-enabled",s="update-camera-bounds",a="update-recording-resolution",c="update-recording-resolution-alias",l=u=>({type:r,payload:{enabled:u}}),T=u=>({type:s,payload:{bounds:u}}),N=(0,t.eH)(s,()=>({type:s})),g=(u,O=!1)=>({type:a,payload:{resolution:u,selected:O}}),p=(0,t.eH)(c,()=>({type:c}))},477490:(o,_,n)=>{"use strict";n.d(_,{pi:()=>s,Rh:()=>a,dE:()=>l,iC:()=>N,S4:()=>g,Xj:()=>p,_L:()=>u,yi:()=>O});const t="show-speaker-notes",r="hide-speaker-notes",s="update-should-sync-speaker-notes-content",a="update-speaker-notes-ftux-store",c="update-speaker-notes-ftux-persistent",l="update-speaker-notes-content-store",T="update-speaker-notes-content-persistent",N="update-speaker-notes-char-count",g="update-speaker-notes-max-char-count",p="update-speaker-notes-open-state",u="update-speaker-notes-opened-in-recording",O="update-speaker-notes-dimension",I=()=>({type:t}),m=()=>({type:r}),P=A=>({type:s,payload:{shouldSync:A}}),k=A=>({type:a,payload:{showFTUX:A}}),G=A=>({type:c,payload:{showFTUX:A}}),U=A=>({type:l,payload:{speakerNotes:A}}),S=A=>({type:T,payload:{speakerNotes:A}}),y=A=>({type:p,payload:{isOpen:A}}),h=A=>({type:u,payload:{isOpened:A}}),B=A=>({type:N,payload:{count:A}}),H=A=>({type:g,payload:{max_count:A}}),j=(A,D)=>({type:O,payload:{width:A,height:D}})},25334:(o,_,n)=>{"use strict";n.d(_,{PV:()=>l,zF:()=>N,b5:()=>g});const t=["path","email","password","filePath","fileName","currentFile","file","recordingPath","videoPath","dirPath","normalPath","host","hostname","name"],r=[/\/Users\/[^/\s]+/g,/\b[Uu]sers?\/[^/\s]+/g,/[A-Z]:\\Users\\[^\\\s]+/gi],s=[/\beyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\b/g,/\b[a-zA-Z0-9-_]{40,}\b/g,/\b(api[_-]?key|token|secret|password|auth)[_-]?[a-zA-Z0-9]{20,}\b/gi,/\bbearer\s+[a-zA-Z0-9-_]{20,}\b/gi],a=[/(https?:\/\/[^/]+\/[^/]*\/)[a-f0-9]{33,}/g],c=[/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,/\b(?:\d{1,3}\.){3}\d{1,3}\b/g,/\b(user[_-]?id|session[_-]?id|device[_-]?id)\s*[:=]\s*[a-zA-Z0-9-_]{10,}\b/gi],l=p=>{try{if(typeof p!="string")return"";let u=p;return t.forEach(O=>{u=u.replace(new RegExp(`"${O}":"[^"]*"[,]?`,"g"),"")}),r.forEach(O=>{u=u.replace(O,I=>{if(I.startsWith("/Users/"))return"/Users/redacted";if(/^[A-Z]:\\Users\\/i.test(I))return I.replace(/^([A-Z]:\\Users\\)[^\\\s]+/i,"$1redacted");const m=I.split("/");return m.length>=2?m[0]+"/redacted":I})}),c.forEach(O=>{u=u.replace(O,"")}),s.forEach(O=>{u=u.replace(O,"")}),a.forEach(O=>{u=u.replace(O,"$1")}),u}catch{return console.error("Error in sanitizeLogMessage"),""}},T=p=>typeof p=="string"?l(p):Array.isArray(p)?p.map(u=>T(u)):typeof p=="object"&&p!==null?N(p):p,N=p=>{if(p==null)return p;const u={};return Object.entries(p).forEach(([O,I])=>{u[O]=T(I)}),u},g=(p,u=new Set)=>{if(!p||typeof p!="object")return p;if(u.has(p))return"Cyclical Reference";if(u.add(p),Array.isArray(p))return p.map(I=>g(I,u));const O={};return Object.entries(p).forEach(([I,m])=>{t.includes(I)||(typeof m=="string"?O[I]=l(m):typeof m=="object"&&m!==null?O[I]=g(m,u):O[I]=m)}),O}},910884:(o,_,n)=>{var t=n(308066);typeof t=="string"&&(t=[[o.id,t,""]]);var r,s,a={hmr:!0};a.transform=r,a.insertInto=void 0;var c=n(739255)(t,a);t.locals&&(o.exports=t.locals)},969975:(o,_,n)=>{"use strict";o.exports=n.p+"assets/fonts/AtlassianSans-latin.woff2"},439491:o=>{"use strict";o.exports=require("assert")},706113:o=>{"use strict";o.exports=require("crypto")},172298:o=>{"use strict";o.exports=require("electron")},582361:o=>{"use strict";o.exports=require("events")},657147:o=>{"use strict";o.exports=require("fs")},113685:o=>{"use strict";o.exports=require("http")},795687:o=>{"use strict";o.exports=require("https")},822037:o=>{"use strict";o.exports=require("os")},371017:o=>{"use strict";o.exports=require("path")},863477:o=>{"use strict";o.exports=require("querystring")},257310:o=>{"use strict";o.exports=require("url")},473837:o=>{"use strict";o.exports=require("util")}},fe={};function C(o){var _=fe[o];if(_!==void 0)return _.exports;var n=fe[o]={id:o,loaded:!1,exports:{}};return Ve[o].call(n.exports,n,n.exports,C),n.loaded=!0,n.exports}C.m=Ve,C.c=fe,(()=>{var o=[];C.O=(_,n,t,r)=>{if(n){r=r||0;for(var s=o.length;s>0&&o[s-1][2]>r;s--)o[s]=o[s-1];o[s]=[n,t,r];return}for(var a=1/0,s=0;s<o.length;s++){for(var[n,t,r]=o[s],c=!0,l=0;l<n.length;l++)(r&!1||a>=r)&&Object.keys(C.O).every(O=>C.O[O](n[l]))?n.splice(l--,1):(c=!1,r<a&&(a=r));if(c){o.splice(s--,1);var T=t();T!==void 0&&(_=T)}}return _}})(),C.n=o=>{var _=o&&o.__esModule?()=>o.default:()=>o;return C.d(_,{a:_}),_},(()=>{var o=Object.getPrototypeOf?n=>Object.getPrototypeOf(n):n=>n.__proto__,_;C.t=function(n,t){if(t&1&&(n=this(n)),t&8||typeof n=="object"&&n&&(t&4&&n.__esModule||t&16&&typeof n.then=="function"))return n;var r=Object.create(null);C.r(r);var s={};_=_||[null,o({}),o([]),o(o)];for(var a=t&2&&n;typeof a=="object"&&!~_.indexOf(a);a=o(a))Object.getOwnPropertyNames(a).forEach(c=>s[c]=()=>n[c]);return s.default=()=>n,C.d(r,s),r}})(),C.d=(o,_)=>{for(var n in _)C.o(_,n)&&!C.o(o,n)&&Object.defineProperty(o,n,{enumerable:!0,get:_[n]})},C.h=()=>"55e5c6a40d444554bfb1",C.hmd=o=>(o=Object.create(o),o.children||(o.children=[]),Object.defineProperty(o,"exports",{enumerable:!0,set:()=>{throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+o.id)}}),o),C.o=(o,_)=>Object.prototype.hasOwnProperty.call(o,_),C.r=o=>{typeof Symbol<"u"&&Symbol.toStringTag&&Object.defineProperty(o,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(o,"__esModule",{value:!0})},C.nmd=o=>(o.paths=[],o.children||(o.children=[]),o),C.p="./",(()=>{var o={2804:0};C.O.j=t=>o[t]===0;var _=(t,r)=>{var[s,a,c]=r,l,T,N=0;if(s.some(p=>o[p]!==0)){for(l in a)C.o(a,l)&&(C.m[l]=a[l]);if(c)var g=c(C)}for(t&&t(r);N<s.length;N++)T=s[N],C.o(o,T)&&o[T]&&o[T][0](),o[s[N]]=0;return C.O(g)},n=global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[];n.forEach(_.bind(null,0)),n.push=_.bind(null,n.push.bind(n))})(),C.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,5800,8165,1404,3655,816,3322,3376],()=>C(C.s=903679)),C.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,5800,8165,1404,3655,816,3322,3376],()=>C(C.s=994021)),C.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,5800,8165,1404,3655,816,3322,3376],()=>C(C.s=639542));var Ye=C.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,5800,8165,1404,3655,816,3322,3376],()=>C(C.s=194383));Ye=C.O(Ye)})();

//# sourceMappingURL=countdown.js.map