(()=>{var nt={359017:(o,l,t)=>{var e=t(744917),u=t(570097),d=t(969975);l=e(!1);var r=u(d);l.push([o.id,`@font-face {
  font-weight: 400 653;
  font-style: normal;
  font-family: 'Atlassian Sans';
  src: url(`+r+`) format('woff2');
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
  pointer-events: auto;
}
html *,
body *,
#container * {
  font-family: 'Atlassian Sans', ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, system-ui, 'Helvetica Neue', sans-serif;
  outline: unset;
}
.screenshotPreviewWindow {
  height: 100%;
  visibility: hidden;
  -webkit-user-select: none;
  --title-x-padding: 14px;
  --button-color: #f1f1f1;
}
.screenshotPreviewWindowLoaded {
  visibility: visible;
}
.confirmation-container {
  height: 100%;
}
.screenshotImageContainer {
  overflow: hidden;
  box-shadow: 0px 4px 20px 0px rgba(0, 0, 0, 0.15);
  border: 1px solid var(--lns-color-border);
  border-radius: var(--lns-radius-large);
  width: 264px;
  height: 198px;
  background-color: #f1f1f1;
}
.screenshotImageContainerCutCorners {
  border-bottom: none;
  border-radius: var(--lns-radius-large) var(--lns-radius-large) 0 0;
}
.screenshotImageContainer:hover .screenshotImageMoreButtonContainer,
.screenshotImageContainer:hover .screenshotImageCloseButtonContainer,
.screenshotMenuClick .screenshotImageMoreButtonContainer,
.screenshotMenuClick .screenshotImageCloseButtonContainer {
  /* show the more and close buttons when hovering over the container */
  opacity: 1;
}
.screenshotImage {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: left;
  cursor: grab;
}
.screenshotTitleSection {
  width: 264px;
  max-width: 264px;
  height: 36px;
  border: 1px solid var(--lns-color-border);
  border-radius: 0 0 var(--lns-radius-large) var(--lns-radius-large);
  border-top: none;
  background: var(--button-color);
}
.screenshotTitleContainer {
  padding: 9px var(--title-x-padding);
  overflow: hidden;
}
.screenshotTitleLogoLoaderContainer span {
  width: 36px;
  height: 36px;
  margin-left: 10px;
}
.screenshotTitleLogoContainer {
  position: absolute;
  background: var(--button-color);
  width: 42px;
  height: 36px;
  border: 1px solid var(--lns-color-border);
  border-top: none;
  border-right: none;
  border-radius: 0 0 0 var(--lns-radius-large);
  left: 0;
  z-index: 1;
}
.screenshotTitleLogoContainer span {
  margin-left: var(--title-x-padding);
  margin-top: 5px;
}
.screenshotTitleRevertButtonContainer {
  position: absolute;
  background: var(--button-color);
  width: 36px;
  height: 36px;
  padding: 6px;
  border: 1px solid var(--lns-color-border);
  border-top: none;
  border-left: none;
  border-radius: 0 0 var(--lns-radius-large) 0;
  right: 0;
  z-index: 1;
}
.screenshotTitleText {
  width: fit-content;
  margin-left: 28px;
  white-space: nowrap;
  transition: transform var(--translate-duration) linear;
}
.screenshotTitleText.title-fade-in {
  animation: titleFadeIn 0.3s ease;
}
.screenshotTitleText.title-fade-out {
  animation: titleFadeOut 0.3s ease;
}
.screenshotTitleContainer:hover .screenshotTitleText {
  transform: translateX(var(--translate-value, 0));
}
.screenshotPreviewButton {
  box-shadow: 0px 4px 20px 0px rgba(0, 0, 0, 0.15);
  border: 1px solid var(--lns-color-border);
  border-radius: var(--lns-radius-175);
  width: 128px;
  height: 50px;
  padding: 12px 8px 12px 16px;
  background: var(--button-color);
  cursor: pointer;
}
.screenshotPreviewButton:hover {
  background: #d0d0d0;
}
.screenshotImageMoreButtonContainer {
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
  margin-top: 8px;
  margin-left: 38px;
}
.screenshotImageCloseButtonContainer {
  position: absolute;
  right: 0;
  top: 0;
  opacity: 0;
  margin-top: 8px;
  margin-right: 38px;
}
.screenshotImageButton {
  border: none;
  border-radius: var(--lns-radius-100);
  padding: 4px;
  cursor: pointer;
  box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.25);
}
.screenshotImageButton:hover {
  background: #ccc;
}
@keyframes titleFadeOut {
  0% {
    opacity: 1;
    transform: translateY(0);
  }
  100% {
    opacity: 0;
    transform: translateY(10px);
  }
}
@keyframes titleFadeIn {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
`,""]),o.exports=l},730659:(o,l,t)=>{"use strict";var e=t(275271),u=t(230967),d=t(443934),r=t(844589),S=t(282187),E=t.n(S),T=t(172298),a=t(183780),y=t(145385),h=t(230127),b=t(631915),N=t(638554);const L=274,p=308,k=48,V=28,U="start-img-drag",M="edit_mode",Y="open_screenshot_settings";var j=t(819906);const z=({actionConfirmation:n})=>e.createElement(a.xMy,{alignment:"bottomCenter"},e.createElement(a.W20,{backgroundColor:"rgba(241, 241, 241, 1)",radius:"200",width:"264px",height:"50px",marginBottom:"40px",paddingY:"16px",paddingLeft:"16px",paddingRight:"12px"},e.createElement(a.ggW,{justifyContent:"space-between"},e.createElement(a.xvT,{size:"body-sm"},n),e.createElement(a.JO$,{icon:e.createElement(j.l,null),size:"20px"}))));var ae=t(407973),Le=t(779524),J=t(23405),x=t(604822),de=t(987771);const le=(0,x.h)("analytics","\u{1F596}"),Q=()=>r.h?r.h:de.h;function H(n){const s=Q();s?setImmediate(()=>{n(s.dispatch)}):le.warn("Could not run analytics event. Redux store has not been created yet")}function Ue(n,s){H(i=>{i((0,J.Qs)({name:n,props:s}))})}function f(n,s){H(i=>{i((0,J.L9)({name:n,props:s}))})}function Me(n,s){H(i=>{i(identifyEvent({userId:n,traits:s}))})}function Be(){const n=Q();return{anonId:n?n.getState().analytics.anonymous_id:null}}const _e="Desktop Binary Timeout",ue="Desktop Permissions Onboarding",Ee="Desktop Confetti",pe="Desktop Keyboard Shortcuts Updated",Te="Desktop Launch",Se="Desktop Menu Activated",Ce="Desktop Speaker Notes",K="Desktop Screenshot Preview",Re="Desktop Screenshot Shortcut Setup",ge="Desktop Screenshot Try It Ftux",X="System Audio Modal",$="Desktop Quit",Ge="Log Out",we="Pro Tag Clicked",Z="Desktop Used Confetti",q="Uploader User Canceled Failed Retries",Oe="Uploader User Attempted Failed Retries",Ie="Engaged an RBAC restriction",me="Desktop Camera Bubble Rendered",ct="Desktop Critical Error While Recording",st="Desktop Recorder Stop",Ht="Cascading Recorders Modal",it="Desktop Screenshot Capture Shortcut Pressed",rt="Desktop Screenshot Capture Started",at="Desktop Screenshot Capture Completed",je="Desktop Screenshot Capture Failed",dt="Desktop Screenshot Capture Cancelled",lt="Desktop Screenshot Upload Started",xe="Desktop Screenshot Upload Completed",He="Desktop Screenshot Upload Failed",_t="Restart Recording Keyboard Shortcut",ut="Event Recording Restart Prompt Reject",Et="Event Recording Restart Prompt Confirm",pt="App quit during recording",Tt="Desktop SRT successfully received",Ne="Desktop shared auth successful",St="Desktop shared auth initiated",Ct="Desktop shared auth welcome flow triggered",Rt="User app restart on start recording failure",gt="User app quit on start recording failure",Ot="Quit During Recording Prompt",It="Desktop Countdown Paused",mt="Desktop Countdown Unpaused",Nt="Desktop Countdown Skipped",Dt="Desktop Countdown Cancelled",Ke="Desktop Onboarding Started",vt="Desktop Onboarding Step Viewed",yt="Desktop Onboarding Permissions Requested",ht="Received Desktop Notification",ft="Clicked desktop Notification",At="Desktop Notification Permission Prompt Accepted",bt="Desktop Notifications Notification Click",Fe="Start Recording button clicked on canvas",We="Speaker notes toggled",kt="Speaker notes moved",Pt="Speaker notes resized",Lt="Failed video successfully recovered",Ve="desktop_capture_mode_toggle_clicked",Ye="desktop_screenshot_select_area_button_clicked",ze="desktop_screenshot_capture_shortcut_pressed",Je="desktop_screenshot_capture_mode_entered",Qe="desktop_screenshot_capture_cancelled",Xe="desktop_screenshot_capture_completed",De="desktop_screenshot_capture_failed",ve="desktop_screenshot_preview_edit_in_loom_clicked",ye="desktop_screenshot_preview_dragged_to_upload",he="desktop_screenshot_preview_copy_link_clicked",c="desktop_screenshot_preview_kebab_menu_clicked",O="desktop_screenshot_preview_download_clicked",F="desktop_screenshot_preview_copy_image_clicked",ee="desktop_screenshot_preview_retake_image_clicked",te="desktop_screenshot_preview_delete_image_clicked",Ut="desktop_screenshots_keyboard_shortcut_set",Kt="desktop_tooltip_screenshots_button_clicked",bo="desktop_tooltip_screenshots_dismissed",Ft="desktop_screenshots_shortcut_onboarding_step_completed",ko="desktop_screenshots_try_it_ftux_button_clicked",Po="desktop_screenshots_try_it_ftux_dismissed",Wt="desktop_meeting_recording_tab_clicked",Vt="desktop_meeting_recording_record_meeting_clicked",Yt="desktop_meeting_recording_record_now_clicked",zt="desktop_meeting_recording_nudge_notification_shown",Jt="desktop_meeting_recording_nudge_notification_clicked",Qt="desktop_meeting_recording_nudge_notification_button_clicked",Xt="desktop_meeting_recording_nudge_notification_menu_opened",$t="desktop_meeting_recording_nudge_notification_menu_button_clicked",Zt="desktop_meeting_recording_reminders_banner_shown",qt="desktop_meeting_recording_reminders_banner_allow_clicked",en="desktop_meeting_recording_reminders_banner_dismiss_clicked",tn="desktop_meeting_recording_reminders_setting_enabled",nn="desktop_meeting_recording_reminders_setting_disabled",on="desktopMeetingNotes",cn="desktopMeetingTranscript",sn="desktopMeetingAgent",rn="desktopMeetingList",an="desktopMeetingListDisconnectedState",dn="meetingRecordingTranscriptButton",ln="meetingRecordingMeetingNotesButton",_n="meetingRecordingJoinMeetingButton",un="meetingRecordingRecordToggle",En="meetingRecordingRecordNowButton",pn="meetingRecordingFilter",Tn="meetingRecordingFilterOption",Sn="meetingRecordingConnectCalendarButton",Cn="meetingRecordingConfluenceLoginBannerButton",Rn="meetingRecordingConnectConfluenceBanner",gn="meetingRecordingConfluenceLoginBannerSuccess",On="meetingNotesOnboardingButton",In="meetingNotesOnboardingTourShown",mn="meetingRecordingTabDotIndicator",Nn="meetingRecordingTabHoverCard",Dn="meeting_bot_controls_stop_button_clicked",vn="meeting_bot_controls_pause_button_clicked",yn="meeting_bot_controls_resume_button_clicked",hn="meeting_bot_controls_cancel_button_clicked",fn="meeting_bot_controls_cancel_confirmation_cancel_button_clicked",An="meeting_bot_controls_cancel_confirmation_resume_button_clicked",bn="meeting_bot_controls_show_meeting_notes_button_clicked",kn="meeting_bot_controls_hide_meeting_notes_button_clicked",Pn="meeting_bot_controls_manage_on_loom_button_clicked",Ln="meeting_bot_controls_finish_button_clicked",Un="meeting_bot_controls_dismiss_button_clicked",Mn="Clicked Resize Cam Bubble",Bn="Clicked Close Cam Bubble",Gn="Clicked Filter Chevron",wn="Clicked Modify Avatar",jn="Clicked Start Recording Button",xn="Clicked Home Button",Hn="Clicked Edit Profile",Kn="desktop_close_clicked",Fn="desktop_effects_menu_clicked",Wn="desktop_submenu_clicked",Vn="Cancel Recording Dialog Confirm",Yn="Cancel Recording Dialog Reject",zn=[Ve,Ye,ze,Je,Qe,Xe,De,ve,ye,he,c,O,F,ee,te,Ut],Lo=n=>zn.includes(n),Uo={[_e]:{action:"Timeout",actionSubject:"desktopBinary",eventType:"operational"},[ue]:{eventType:"screen"},[Ee]:{eventType:"screen"},[pe]:{action:"Updated",actionSubject:"desktopKeyboardShortcuts",eventType:"track"},[Te]:{action:"Launch",actionSubject:"desktop",eventType:"operational"},[Se]:{action:"Activated",actionSubject:"desktopMenu",eventType:"operational"},[Ce]:{eventType:"screen"},[K]:{eventType:"screen"},[Re]:{eventType:"screen"},[X]:{eventType:"screen"},[$]:{action:"Quit",actionSubject:"desktop",eventType:"operational"},[Ge]:{action:"Log Out",actionSubject:"desktop",eventType:"operational"},[we]:{action:"Clicked",actionSubject:"proTag",eventType:"ui"},[Z]:{action:"Activated",actionSubject:"desktopConfetti",eventType:"track"},[q]:{action:"User Canceled Failed Retries ",actionSubject:"uploader",eventType:"track"},[Oe]:{action:"User Attempted Failed Retries",actionSubject:"uploader",eventType:"track"},[Ie]:{action:"Engaged",actionSubject:"rbacRestriction",eventType:"operational"},[me]:{action:"Rendered",actionSubject:"desktopCameraBubble",eventType:"operational"},[ct]:{action:"Critical Error While Recording",actionSubject:"desktopRecorder",eventType:"operational"},[st]:{action:"Stop",actionSubject:"desktopRecorder",eventType:"operational"},[It]:{action:"Clicked",actionSubject:"desktopCountdown",eventType:"ui"},[mt]:{action:"Clicked",actionSubject:"desktopCountdown",eventType:"ui"},[Nt]:{action:"Clicked",actionSubject:"desktopCountdown",eventType:"ui"},[Dt]:{action:"Clicked",actionSubject:"desktopCountdown",eventType:"ui"},[it]:{action:"Capture Shortcut Pressed",actionSubject:"desktopScreenshot",eventType:"ui"},[rt]:{action:"Capture Started",actionSubject:"desktopScreenshot",eventType:"operational"},[at]:{action:"Capture Completed",actionSubject:"desktopScreenshot",eventType:"operational"},[je]:{action:"Capture Failed",actionSubject:"desktopScreenshot",eventType:"operational"},[dt]:{action:"Capture Cancelled",actionSubject:"desktopScreenshot",eventType:"operational"},[lt]:{action:"Upload Started",actionSubject:"desktopScreenshot",eventType:"operational"},[xe]:{action:"Upload Completed",actionSubject:"desktopScreenshot",eventType:"operational"},[He]:{action:"Upload Failed",actionSubject:"desktopScreenshot",eventType:"operational"},[_t]:{action:"Keyboard Shortcut Used",actionSubject:"restartRecording",eventType:"ui"},[ut]:{action:"Rejected",actionSubject:"desktopRestartPrompt",eventType:"track"},[Et]:{action:"Confirmed",actionSubject:"deskopRestartPrompt",eventType:"track"},[pt]:{action:"Quit During Recording",actionSubject:"desktop",eventType:"operational"},[Tt]:{action:"Received",actionSubject:"desktopSrt",eventType:"operational"},[Ne]:{action:"Shared Auth Successful",actionSubject:"desktop",eventType:"operational"},[St]:{action:"Initiated",actionSubject:"desktopSharedAuth",eventType:"operational"},[Ct]:{action:"Triggered",actionSubject:"desktopSharedAuthWelcomeFlow",eventType:"operational"},[Rt]:{action:"Start Failed User Restart",actionSubject:"desktopRecording",eventType:"track"},[gt]:{action:"Start Failed User Quit",actionSubject:"desktopRecording",eventType:"track"},[Ot]:{action:"Quick During Recording Confirmed",actionSubject:"desktopRecording",eventType:"track"},[Ke]:{action:"Started",actionSubject:"desktopOnboarding",eventType:"operational"},[vt]:{action:"Viewed",actionSubject:"desktopOnboardingStep",eventType:"operational"},[yt]:{action:"Requested",actionSubject:"desktopOnboardingPermissions",eventType:"operational"},[ht]:{action:"Received",actionSubject:"desktopNotification",eventType:"operational"},[ft]:{action:"Clicked",actionSubject:"desktopNotification",eventType:"ui"},[At]:{action:"Permission Prompt Accepted",actionSubject:"desktopNotification",eventType:"track"},[bt]:{action:"Notification Click",actionSubject:"desktopNotification",eventType:"ui"},[Fe]:{action:"Started On Canvas",actionSubject:"desktopRecorder",eventType:"track"},[We]:{action:"Toggled",actionSubject:"speakerNotes",eventType:"track"},[kt]:{action:"Moved",actionSubject:"speakerNotes",eventType:"track"},[Pt]:{action:"Resized",actionSubject:"speakerNotes",eventType:"track"},[Lt]:{action:"Successfully Recovered",actionSubject:"videoRecovery",eventType:"operational"},[Ve]:{action:"Clicked",actionSubject:"captureModeToggle",eventType:"ui"},[Ye]:{action:"Clicked",actionSubject:"selectAreaButton",eventType:"ui"},[ze]:{action:"Pressed",actionSubject:"screenshotCaptureShortcut",eventType:"ui"},[Je]:{action:"Entered",actionSubject:"screenshotCaptureMode",eventType:"track"},[Qe]:{action:"Cancelled",actionSubject:"screenshotCaptureMode",eventType:"track"},[Xe]:{action:"Completed",actionSubject:"screenshotCapture",eventType:"track"},[De]:{action:"Failed",actionSubject:"screenshotCapture",eventType:"track"},[ve]:{action:"Clicked",actionSubject:"screenshotPreviewEditButton",eventType:"ui"},[ye]:{action:"Dragged",actionSubject:"screenshotPreview",eventType:"ui"},[he]:{action:"Clicked",actionSubject:"screenshotCopyLinkButton",eventType:"ui"},[c]:{action:"Clicked",actionSubject:"screenshotPreviewMenuButton",eventType:"ui"},[O]:{action:"Clicked",actionSubject:"screenshotDownloadButton",eventType:"ui"},[F]:{action:"Clicked",actionSubject:"screenshotCopyImageButton",eventType:"ui"},[ee]:{action:"Clicked",actionSubject:"screenshotRetakeButton",eventType:"ui"},[te]:{action:"Clicked",actionSubject:"screenshotDeleteButton",eventType:"ui"},[Ut]:{action:"Set",actionSubject:"screenshotShortcut",eventType:"track"},[Kt]:{action:"Clicked",actionSubject:"screenshotsButtonTooltip",eventType:"ui"},[Ft]:{action:"Completed",actionSubject:"screenshotsShortcutOnboardingStep",eventType:"track"},[Mn]:{action:"Clicked",actionSubject:"resizeCamBubble",eventType:"ui"},[Bn]:{action:"Clicked",actionSubject:"closeCamBubble",eventType:"ui"},[Gn]:{action:"Clicked",actionSubject:"filterChevron",eventType:"ui"},[wn]:{action:"Clicked",actionSubject:"modifyAvatar",eventType:"ui"},[jn]:{action:"Clicked",actionSubject:"startRecordingButton",eventType:"ui"},[xn]:{action:"Clicked",actionSubject:"homeButton",eventType:"ui"},[Hn]:{action:"Clicked",actionSubject:"editProfile",eventType:"ui"},[Kn]:{action:"Clicked",actionSubject:"headerCloseButton",eventType:"ui"},[Fn]:{action:"Clicked",actionSubject:"effectsMenu",eventType:"ui"},[Wn]:{action:"Clicked",actionSubject:"submenu",eventType:"ui"},[Vn]:{action:"Confirmed",actionSubject:"cancelRecordingDialog",eventType:"track"},[Yn]:{action:"Rejected",actionSubject:"cancelRecordingDialog",eventType:"track"},[Wt]:{action:"Clicked",actionSubject:"meetingRecordingsTab",eventType:"ui"},[Vt]:{action:"Clicked",actionSubject:"meetingRecordingsRecordMeetingButton",eventType:"ui"},[Yt]:{action:"Clicked",actionSubject:"meetingRecordingsRecordNowButton",eventType:"ui"},[zt]:{action:"shown",actionSubject:"meetingRecordingsNudgeNotification",eventType:"track"},[Jt]:{action:"clicked",actionSubject:"meetingRecordingsNudgeNotification",eventType:"ui"},[Qt]:{action:"clicked",actionSubject:"meetingRecordingsNudgeNotificationButton",eventType:"ui"},[Zt]:{action:"Shown",actionSubject:"meetingRemindersBanner",eventType:"ui"},[qt]:{action:"Clicked",actionSubject:"meetingRemindersBannerAllowButton",eventType:"ui"},[en]:{action:"Clicked",actionSubject:"meetingRemindersBannerDismissButton",eventType:"ui"},[tn]:{action:"Clicked",actionSubject:"meetingRemindersSettingsToggleOn",eventType:"ui"},[nn]:{action:"Clicked",actionSubject:"meetingRemindersSettingsToggleOff",eventType:"ui"},[Xt]:{action:"opened",actionSubject:"meetingRecordingsNudgeNotificationMenu",eventType:"ui"},[$t]:{action:"clicked",actionSubject:"meetingRecordingsNudgeNotificationMenuButton",eventType:"ui"},[Dn]:{action:"clicked",actionSubject:"meetingRecordingStopButton",eventType:"ui"},[hn]:{action:"clicked",actionSubject:"meetingRecordingCancelButton",eventType:"ui"},[vn]:{action:"clicked",actionSubject:"meetingRecordingPauseButton",eventType:"ui"},[yn]:{action:"clicked",actionSubject:"meetingRecordingResumeButton",eventType:"ui"},[An]:{action:"clicked",actionSubject:"meetingRecordingConfirmationModalResumeButton",eventType:"ui"},[fn]:{action:"clicked",actionSubject:"meetingRecordingConfirmationModalCancelButton",eventType:"ui"},[bn]:{action:"clicked",actionSubject:"meetingRecordingShowMeetingNotesButton",eventType:"ui"},[kn]:{action:"clicked",actionSubject:"meetingRecordingHideMeetingNotesButton",eventType:"ui"},[Pn]:{action:"clicked",actionSubject:"meetingRecordingManageOnLoomButton",eventType:"ui"},[Ln]:{action:"clicked",actionSubject:"meetingRecordingFinishButton",eventType:"ui"},[Un]:{action:"clicked",actionSubject:"meetingRecordingDismissButton",eventType:"ui"},[on]:{eventType:"screen"},[cn]:{eventType:"screen"},[sn]:{eventType:"screen"},[rn]:{eventType:"screen"},[an]:{eventType:"screen"},[dn]:{action:"clicked",actionSubject:"meetingRecordingTranscriptButton",eventType:"ui"},[ln]:{action:"clicked",actionSubject:"meetingRecordingMeetingNotesButton",eventType:"ui"},[un]:{action:"set",actionSubject:"meetingRecordingRecordToggle",eventType:"ui"},[En]:{action:"clicked",actionSubject:"meetingRecordingRecordNowButton",eventType:"ui"},[pn]:{action:"opened",actionSubject:"meetingRecordingFilter",eventType:"ui"},[Tn]:{action:"clicked",actionSubject:"meetingRecordingFilterOption",eventType:"ui"},[Sn]:{action:"clicked",actionSubject:"meetingRecordingConnectCalendarButton",eventType:"ui"},[Rn]:{action:"shown",actionSubject:"meetingRecordingConnectConfluenceBanner",eventType:"track"},[gn]:{action:"success",actionSubject:"confluenceLogin",eventType:"track"},[_n]:{action:"clicked",actionSubject:"meetingRecordingJoinMeetingButton",eventType:"ui"},[Cn]:{action:"clicked",actionSubject:"confluenceLoginBanner",eventType:"ui"},[On]:{action:"clicked",actionSubject:"meetingRecordingOnboardingTour",eventType:"ui"},[In]:{action:"shown",actionSubject:"meetingRecordingOnboardingTour",eventType:"track"},[mn]:{action:"shown",actionSubject:"meetingRecordingTabDotIndicator",eventType:"track"},[Nn]:{action:"shown",actionSubject:"meetingRecordingTabHoverCard",eventType:"track"}};var Jn=t(903285),B=t(377534),$e=t(871861);function Qn(){return(0,d.v9)(n=>n.screenshot.isTakingFullScreenScreenshot)}function Mo(){return useSelector(n=>n.screenshot.originalImgInfo)}function Bo(){const n=useSelector(i=>i.preRecordingPanel.ready_to_show_screenshot_try_it_ftux),s=useSelector(i=>i.preRecordingPanel.ready_to_show_screenshot_shortcut_setup);return n===!0||s===!0}var Ze=t(969178);const Xn=(0,Ze.rp)("save-image-to-local"),Go=(0,Ze.rp)("screenshot-preview-show"),qe=(0,Ze.rp)("screenshot-preview-close"),$n="Link to image copied",Zn="Image copied to clipboard",qn="Image deleted",eo="Image saved to downloads",Mt=2e3,to=40,no=50,oo=80;var wo=t(566149);const co=({screenshotId:n,screenshotTitle:s,screenshotImg:i,safeToDelete:D,onSettingsClick:I,onMenuBtnClick:m,setActionConfirmation:v,onClose:R,shouldDisplaySettings:C=!1})=>{const g=Qn(),Ae=(0,d.I0)(),be=()=>{f(O,{screenshot_id:n}),(0,B.P)(Xn,{originalImageSource:i,filename:s}),v(eo),R({})},ce=()=>{f(F,{screenshot_id:n});const W=T.nativeImage.createFromDataURL(i);T.clipboard.writeImage(W),v(Zn),R({})},P=({skipConfirmation:W})=>{f(te,{screenshot_id:n}),(0,B.P)($e.ae),v(W?"":qn),R({urlToOpen:void 0,skipConfirmation:W})},G=()=>{f(ee,{screenshot_id:n}),(0,B.P)(qe,{withCleanUp:!0}),(0,B.P)($e.ae),Ae((0,Le.yG)({recordingMode:Jn.o_.Screenshot,takeFullScreenScreenshot:g}))};return e.createElement(a.Ltx,{trigger:e.createElement("button",{className:"screenshotImageButton"},e.createElement(a.JO$,{icon:e.createElement(ae.s,null),size:"16px",color:"body"})),onOpenChange:m,options:[{title:"Save to downloads",onClick:be},{title:"Copy image",onClick:ce},{title:"Retake image",onClick:G},{title:"Delete image",onClick:()=>P({skipConfirmation:!1}),disabled:!D},...C?[{title:"Settings",onClick:I}]:[]]})};var ne=t(323055);const oe=n=>n.user,jo=(0,ne.P1)(oe,n=>{var s;return(s=n.current)==null?void 0:s.id}),xo=(0,ne.P1)(oe,n=>{var s;return(s=n.current)==null?void 0:s.aa_id}),Ho=(0,ne.P1)(oe,n=>{var s,i;return(i=(s=n.current)==null?void 0:s.aa_is_mastered)!=null?i:!1}),Ko=(0,ne.P1)(oe,n=>{var s,i;return(i=(s=n.current)==null?void 0:s.avatars)!=null?i:[]}),Fo=(0,ne.P1)(oe,n=>{var s;return(s=n.current)==null?void 0:s.default_workspace_id}),Wo=n=>n.first_name?n.last_name?n.first_name+" "+n.last_name:n.first_name:n.email;function Vo(n){return n==null?null:so(n.first_name,n.last_name)||n.email}const so=(n=null,s=null)=>[n,s].filter(Boolean).map(i=>i?i.charAt(0).toUpperCase()+i.slice(1):"").join(" ").trim();function Yo(){return useSelector(n=>{var s;return(s=n.user.current)==null?void 0:s.id})}function zo(){return useSelector(n=>{var s;return(s=n.user.current)==null?void 0:s.email})}function Jo(){return useSelector(n=>getUserDisplayName(n.user.current))}function Qo(){return useSelector(n=>{var s,i;return(i=(s=n.user)==null?void 0:s.current)==null?void 0:i.avatars[0]})}function Xo(){return useSelector(selectIsAtlassianMastered)}function $o(){return useSelector(n=>n.user.dismissedSystemAudioTip)}function io(n){return(0,d.v9)(s=>{var i,D;return(D=(i=s.user.current)==null?void 0:i.scopes.includes(n))!=null?D:!1})}function Zo(){return useSelector(n=>n.user.current!=null)}function qo(){return useSelector(n=>n.user.initialUserLoad)}function ec(){const n=useSelector(s=>{var i;return(i=s.user.current)==null?void 0:i.videoSettings});return Boolean(n?.noise_suppression)}var Bt=(n=>(n.VideoRecordAccess="VIDEO_RECORD_ACCESS",n.VideoEnhancedRecorderAccess="VIDEO_ENHANCED_RECORDER_ACCESS",n.ImageCaptureAccess="IMAGE_CAPTURE_ACCESS",n.ScreenshotAutoTitle="AI_SCREENSHOT_AUTO_TITLE",n))(Bt||{});function ro(){return(0,d.v9)(n=>n.screenshotPreview)}function ao(){return io(Bt.ScreenshotAutoTitle)}var lo=t(854771);const _o=n=>{var s,i;const D=n?oo:no,I=(s=document.getElementsByClassName("screenshotTitleContainer"))==null?void 0:s[0],m=(i=document.getElementsByClassName("screenshotTitleText"))==null?void 0:i[0];if(I&&m){const v=I.offsetWidth,R=m.scrollWidth,C=Math.max(0,R-v+D);m.style.setProperty("--translate-value",`-${C}px`),m.style.setProperty("--translate-duration",`${C/to}s`)}};var uo=(n,s,i)=>new Promise((D,I)=>{var m=C=>{try{R(i.next(C))}catch(g){I(g)}},v=C=>{try{R(i.throw(C))}catch(g){I(g)}},R=C=>C.done?D(C.value):Promise.resolve(C.value).then(m,v);R((i=i.apply(n,s)).next())});const Eo=({title:n,screenshotId:s,canRevertTitle:i})=>{const[D,I]=(0,e.useState)(!1),[m,v]=(0,e.useState)(!1),R=i&&D,C=()=>{const g=document.getElementsByClassName("screenshotTitleText")[0];!g||m||(g.classList.add("title-fade-out"),v(!0),setTimeout(()=>uo(void 0,null,function*(){yield(0,B.P)($e.us,{screenshotId:s}),g.classList.remove("title-fade-out"),g.classList.add("title-fade-in"),setTimeout(()=>{g.classList.remove("title-fade-in"),v(!1)},300)}),300))};return n?(m||_o(i),e.createElement(a.W20,{position:"relative",onMouseEnter:()=>I(!0),onMouseLeave:()=>I(!1)},e.createElement("div",{className:"screenshotTitleLogoContainer"},e.createElement(a.TRl,{variant:"symbol",maxWidth:3})),R?e.createElement("div",{className:"screenshotTitleRevertButtonContainer"},e.createElement(a.ua7,{content:"Remove AI title",placement:"topLeft"},e.createElement(a.hU,{altText:"Use default title",size:"small",icon:e.createElement(lo.$,null),onClick:C}))):null,e.createElement("div",{className:E()("screenshotTitleSection","screenshotTitleContainer")},e.createElement(a.xvT,{size:"small",className:"screenshotTitleText"},n)))):e.createElement("div",{className:E()("screenshotTitleSection","screenshotTitleLogoLoaderContainer")},e.createElement(a.m9_,null))};var po=(n,s,i)=>new Promise((D,I)=>{var m=C=>{try{R(i.next(C))}catch(g){I(g)}},v=C=>{try{R(i.throw(C))}catch(g){I(g)}},R=C=>C.done?D(C.value):Promise.resolve(C.value).then(m,v);R((i=i.apply(n,s)).next())});function fe(n,s){return n.animate(s,{duration:300,easing:"ease-out",fill:"forwards"}).finished}const To=()=>{const n=(0,e.useRef)(null),[s,i]=(0,e.useState)(!1),[D,I]=(0,e.useState)(!1),[m,v]=(0,e.useState)(!1),[R,C]=(0,e.useState)(""),[g,Ae]=(0,e.useState)(!1),be=(0,e.useRef)(!1),ce=ao(),P=(0,e.useCallback)(A=>po(void 0,[A],function*({urlToOpen:xt,skipConfirmation:fo}){const re=n.current;if(re){if(fo){yield fe(re,[{transform:"translateX(0)"},{transform:"translateX(100vw)"}]),(0,B.P)(qe,{urlToOpen:xt});return}yield fe(re,[{opacity:1},{opacity:0}]),Ae(!0),yield fe(re,[{opacity:0},{opacity:1}]),yield new Promise(Ao=>setTimeout(Ao,Mt)),yield fe(re,[{opacity:1},{opacity:0}]),Ae(!1),C(""),(0,B.P)(qe,{urlToOpen:xt})}}),[]),{screenshotImg:G,thumbnailImg:W,screenshotShareUrl:se,screenshotId:w,safeToDelete:jt,failedToSave:ie,screenshotTitle:et,canRevertTitle:mo}=ro(),No=A=>{A.preventDefault(),f(ye,{screenshot_id:w}),T.ipcRenderer.send(U,{original:G,thumbnail:W,filename:et})},Do=()=>{f(ve,{screenshot_id:w}),P({urlToOpen:se+`?${M}=1`,skipConfirmation:!0})},vo=()=>{T.shell.openExternal(se+`?${Y}=1`),P({skipConfirmation:!0})},yo=()=>{I(!0)},ho=A=>{v(A),f(c,{screenshot_id:w})},tt=(0,e.useCallback)(A=>{se&&(f(he,{screenshot_id:w,action:A?"user_clicked":"auto_copied"}),T.clipboard.writeText(se),be.current=!0,A?(C($n),P({})):(i(!0),setTimeout(()=>{i(!1)},Mt)))},[se,w,P]);(0,e.useEffect)(()=>{if(ie){const A=T.nativeImage.createFromDataURL(G);T.clipboard.writeImage(A)}},[G,ie]),(0,e.useEffect)(()=>{be.current||tt()},[tt]);const ke=!jt||ie;return g&&R?e.createElement("div",{ref:n,className:"confirmation-container"},e.createElement(z,{actionConfirmation:R})):e.createElement("div",{className:E()("screenshotPreviewWindow",{screenshotPreviewWindowLoaded:D}),ref:n},e.createElement(a.ggW,{autoFlow:"row",justifyContent:"center",gap:"medium"},e.createElement(a.W20,null,e.createElement("div",{className:E()("screenshotImageContainer",{screenshotMenuClick:m,screenshotImageContainerCutCorners:ce})},e.createElement("img",{className:"screenshotImage",src:G,alt:"Screenshot Preview",crossOrigin:"anonymous",onDragStart:No,onLoad:yo}),e.createElement("div",{className:"screenshotImageMoreButtonContainer"},e.createElement(co,{screenshotId:w,screenshotTitle:et,screenshotImg:G,safeToDelete:jt,onSettingsClick:vo,onMenuBtnClick:ho,onClose:P,setActionConfirmation:C,shouldDisplaySettings:ce})),e.createElement("div",{className:"screenshotImageCloseButtonContainer",onClick:()=>P({urlToOpen:void 0,skipConfirmation:!0})},e.createElement("button",{className:"screenshotImageButton"},e.createElement(a.JO$,{icon:e.createElement(b.G,null),size:"16px",color:"body"})))),ce?e.createElement(Eo,{title:et,screenshotId:w,canRevertTitle:mo}):null),e.createElement("div",{className:"screenshotPreviewButtonsContainer"},e.createElement(a.ggW,{gap:"small"},e.createElement(a.ua7,{isInline:!1,content:ie?"There was a problem uploading the screenshot, the image has been copied to your clipboard":"Edit in Loom will be available once uploading is complete",isDisabled:!ke},e.createElement("button",{className:"screenshotPreviewButton",onClick:Do,disabled:ke},e.createElement(a.ggW,{justifyContent:"space-between"},e.createElement(a.xvT,null,"Edit in Loom"),e.createElement(a.JO$,{icon:e.createElement(h.n,null),size:"20px"})))),e.createElement(a.ua7,{isInline:!1,content:ie?"There was a problem uploading the screenshot, the image has been copied to your clipboard":"Link will be available once uploading is complete",isDisabled:!ke},e.createElement("button",{className:"screenshotPreviewButton",onClick:()=>tt(!0),disabled:ke},e.createElement(a.ggW,{justifyContent:"space-between"},e.createElement(a.xvT,null,s?"Link copied":"Copy link"),e.createElement(a.JO$,{icon:s?e.createElement(y.U,null):e.createElement(N.w,null),size:"20px"}))))))))};var So=t(474176),Co=t(394473),Ro=t(110720),go=t(239222);(0,Ro.jC)(),(0,Co.FA)("screenshotPreview"),(0,So.u)();const Gt=document.createElement("div"),wt="container";Gt.id=wt,document.body.appendChild(Gt);const Oo=document.getElementById(wt),Io=r.S(go.Q,[]);Ue(K),(n=>(0,u.render)(e.createElement(d.zt,{store:Io},e.createElement(n,null)),Oo))(To)},23405:(o,l,t)=>{"use strict";t.d(l,{L9:()=>T,Qs:()=>a,wo:()=>N});var e=t(346972);const u="track-event",d="identify-event",r="page-event",S="get-anon-id",E="ui-viewed-event",T=(0,e.eH)(u,({name:p,props:k})=>({type:u,payload:{name:p,props:k}})),a=(0,e.eH)(r,({name:p})=>({type:r,payload:{name:p}})),y=(0,e.eH)(d,({userId:p,traits:k})=>({type:d,payload:{userId:p,traits:k}})),h=(0,e.eH)(E,()=>({type:E})),b=(0,e.eH)(S,()=>({type:S})),N="update-analytics-anonymous-id",L=p=>({type:N,payload:{id:p}})},987771:(o,l,t)=>{"use strict";t.d(l,{h:()=>e});let e;function u(r){e=r}function d(r){return new Promise(S=>{const E=e.getState();if(r(E)){S(E);return}const T=e.subscribe(()=>{const a=e.getState();r(a)&&(T(),S(a))})})}},844589:(o,l,t)=>{"use strict";t.d(l,{h:()=>a,S:()=>y});var e=t(346972),u=t(835875),d=t(218417),r=t(251308),S=t(29419),E=t(879741),T=t(110720);let a;const y=(h,b)=>{const N=window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__||u.qC,L=(0,e.mu)(),p=[...E.v9?[S.Z]:[],e.Wp,r.Z,d.ZP,...b];return a=(0,u.MT)(h,L,N((0,u.md)(...p),(0,T.cX)())),(0,e.Id)(a),a}},394473:(o,l,t)=>{"use strict";t.d(l,{FA:()=>S,o7:()=>N});var e=t(172298),u=t.n(e),d=t(510453);let r="renderer";const S=p=>{p&&(r=p)},E=(p="info",k)=>(V,U)=>{const M={};U&&Object.entries(U).forEach(([Y,j])=>{M[Y]=T(j)}),e.ipcRenderer.send(d.u,{logLevel:p,message:V,context:M,windowName:k})};function T(p){return typeof p!="object"?p:a(p)?{message:p.message,name:p.name}:JSON.parse(JSON.stringify(p))}function a(p){return typeof p.message=="string"&&typeof p.name=="string"}const y=E("info",r),h=E("warn",r),b=E("error",r),N=E("debug",r),L=p=>({info:E("info",p),warn:E("warn",p),error:E("error",p),debug:E("debug",p)})},621678:(o,l,t)=>{"use strict";t.d(l,{JW:()=>d,p2:()=>r,NR:()=>S});var e=t(346972);const u="push-back-overlay",d="cropping-window-ready",r="cropping-window-close",S="exit-cropping",E="first-crop",T=()=>({type:d}),a=()=>({type:r}),y=(0,e.eH)(u,()=>({type:u})),h=()=>({type:S}),b=()=>({type:E})},206687:(o,l,t)=>{"use strict";t.d(l,{p4:()=>u,$O:()=>d,JC:()=>r,bk:()=>E,Fh:()=>T,S3:()=>a,p1:()=>y,mB:()=>h,mz:()=>b,Uy:()=>N,M9:()=>L,HX:()=>p,VG:()=>k,MK:()=>V,vV:()=>U,BR:()=>M,l1:()=>j,Qc:()=>z,q6:()=>ae,Hd:()=>Le,UY:()=>J,vc:()=>x,g7:()=>de,L0:()=>le,jA:()=>Q,IL:()=>H,Ju:()=>Ue,$G:()=>f,zJ:()=>Me,zE:()=>Be,Wu:()=>_e,KT:()=>ue,Vs:()=>Ee,n9:()=>pe,gQ:()=>Te,IJ:()=>K,C7:()=>ge,cO:()=>X,th:()=>$,Oh:()=>Ge,zF:()=>Z,WR:()=>q,MT:()=>Oe,D1:()=>je,hr:()=>xe,MQ:()=>He,DD:()=>Ne,L1:()=>Ke,ut:()=>Fe,hY:()=>De});var e=t(346972);const u="add-window-id-to-hide",d="select-video-recording-device",r="set-recording-file-path",S="start-recording-failure",E="start-recording-success",T="update-active-window-title",a="update-all-displays",y="update-recorder-prompt-state",h="update-current-recording-devices",b="update-crop-rect",N="update-current-display",L="update-has-selected-display",p="update-is-cropping",k="update-is-recording",V="update-mic-on",U="update-recording-devices",M="update-recording-type",Y="update-recording-type-selection",j="reset-recording-state",z="update-selected-window",ae="clear-selected-window",Le="update-msg-type-status",J="update-session",x="update-show-selector-window",de="update-starting-recording",le="update-stopping-recording",Q="update-windows",H="show-muted-mic-warn",Ue="hide-muted-mic-warn",f="set-recording-time-elapsed",Me="update-internal-audio-status",Be="update-waiting-on-install",_e="set-start-recording-request-time-ms",ue="set-recording-mode",Ee="set-recording-alert",pe="reset-recording-alert",Te="reset-all-recording-alerts",Se="cancel-recording",Ce="restart-recording",K="error-recording",Re="get-display-screenshots",ge="get-windows",X="select-audio-recording-device",$="start-recording",Ge="select-preferred-video-device",we="after-stop-recording",Z="stop-recording",q="update-recording-paused",Oe="update-recording-cancelled",Ie="get-internal-audio-status",me="install-system-audio",ct=c=>({type:y,payload:{state:c}}),st=c=>({type:u,payload:{candidate:c}}),Ht=c=>({type:_e,payload:{timestampMs:c}}),it=c=>({type:f,payload:{recordingTimeElapsed:c}}),rt=()=>({type:H,payload:{}}),at=(0,e.eH)(X,c=>({type:X})),je=c=>({type:d,payload:{device:c}}),dt=({audioDevice:c,videoDevice:O,selectedAudioDevices:F,selectedVideoDevices:ee,updateStore:te=!0})=>({type:h,payload:{audioDevice:c,videoDevice:O,selectedAudioDevices:F,selectedVideoDevices:ee,updateStore:te}}),lt=({audioDevices:c,videoDevices:O})=>({type:U,payload:{audioDevices:c,videoDevices:O}}),xe=c=>({type:M,payload:{recordingType:c}}),He=c=>({type:Y,payload:{recordingType:c}}),_t=c=>({type:r,payload:{path:c}}),ut=c=>({type:T,payload:{title:c}}),Et=(c,O=!1)=>({type:a,payload:{displays:c},meta:{updatingWithScreenshots:O}}),pt=(c=!1)=>({type:x,payload:{show:c}}),Tt=(c=[])=>({type:Q,payload:{windows:c}}),Ne=(c=null)=>({type:b,payload:{cropRect:c}}),St=c=>({type:J,payload:{session:c}}),Ct=c=>({type:L,payload:{selected:c}}),Rt=c=>({type:p,payload:{isCropping:c}}),gt=c=>({type:k,payload:{isRecording:c}}),Ot=c=>({type:de,payload:{starting:c}}),It=c=>({type:le,payload:{stopping:c}}),mt=c=>({type:Oe,payload:{cancelSource:c}}),Nt=c=>({type:V,payload:{on:c}}),Dt=()=>({type:j}),Ke=()=>({type:ae}),vt=(0,e.eH)(z,(c,O=!1)=>({type:z})),yt=()=>c=>{c(Ne(null)),c(We())},ht=(0,e.eH)(Se,(c=!1,O)=>({type:Se})),ft=(0,e.eH)(Ce,(c=!1)=>({type:Ce})),At=(0,e.eH)(K,(c="unknown recording error")=>({type:K})),bt=(0,e.eH)(ge,(c=!0)=>({type:ge})),Fe=(0,e.eH)(N,(c,O=!1)=>({type:N})),We=(0,e.eH)($,(c=!1,O=!1)=>({type:$})),kt=(0,e.eH)(q,c=>({type:q})),Pt=(0,e.eH)(Z,c=>({type:Z})),Lt=(0,e.eH)(we,(c,O,F)=>({type:"after-recorder-stopped"})),Ve=(0,e.eH)(x,(c=!0)=>({type:x})),Ye=(0,e.eH)(Re,()=>({type:Re})),ze=c=>({type:Me,payload:{installed:c}}),Je=c=>({type:Be,payload:{waiting_on_install:c}}),Qe=(0,e.eH)(Ie,c=>({type:Ie})),Xe=(0,e.eH)(me,(c=!1)=>({type:me})),De=({recordingMode:c,storeValue:O=!0})=>({type:ue,payload:{recordingMode:c,storeValue:O}}),ve=c=>({type:pe,payload:{alert:c}}),ye=()=>({type:Te}),he=c=>({type:Ee,payload:{alert:c}})},871861:(o,l,t)=>{"use strict";t.d(l,{ae:()=>d,us:()=>r,g_:()=>S});var e=t(969178);const u=(0,e.rp)("save-screenshot"),d=(0,e.rp)("delete-screenshot"),r=(0,e.rp)("update-screenshot-title"),S=(0,e.rp)("screenshot-start-select"),E=(0,e.rp)("screenshot-stop-select"),T=(0,e.rp)("play-screenshot-sound")},566149:(o,l,t)=>{var e=t(359017);typeof e=="string"&&(e=[[o.id,e,""]]);var u,d,r={hmr:!0};r.transform=u,r.insertInto=void 0;var S=t(739255)(e,r);e.locals&&(o.exports=e.locals)},439491:o=>{"use strict";o.exports=require("assert")},706113:o=>{"use strict";o.exports=require("crypto")},172298:o=>{"use strict";o.exports=require("electron")},582361:o=>{"use strict";o.exports=require("events")},657147:o=>{"use strict";o.exports=require("fs")},113685:o=>{"use strict";o.exports=require("http")},795687:o=>{"use strict";o.exports=require("https")},822037:o=>{"use strict";o.exports=require("os")},371017:o=>{"use strict";o.exports=require("path")},863477:o=>{"use strict";o.exports=require("querystring")},257310:o=>{"use strict";o.exports=require("url")},473837:o=>{"use strict";o.exports=require("util")}},Pe={};function _(o){var l=Pe[o];if(l!==void 0)return l.exports;var t=Pe[o]={id:o,loaded:!1,exports:{}};return nt[o].call(t.exports,t,t.exports,_),t.loaded=!0,t.exports}_.m=nt,_.c=Pe,(()=>{var o=[];_.O=(l,t,e,u)=>{if(t){u=u||0;for(var d=o.length;d>0&&o[d-1][2]>u;d--)o[d]=o[d-1];o[d]=[t,e,u];return}for(var r=1/0,d=0;d<o.length;d++){for(var[t,e,u]=o[d],S=!0,E=0;E<t.length;E++)(u&!1||r>=u)&&Object.keys(_.O).every(N=>_.O[N](t[E]))?t.splice(E--,1):(S=!1,u<r&&(r=u));if(S){o.splice(d--,1);var T=e();T!==void 0&&(l=T)}}return l}})(),_.n=o=>{var l=o&&o.__esModule?()=>o.default:()=>o;return _.d(l,{a:l}),l},(()=>{var o=Object.getPrototypeOf?t=>Object.getPrototypeOf(t):t=>t.__proto__,l;_.t=function(t,e){if(e&1&&(t=this(t)),e&8||typeof t=="object"&&t&&(e&4&&t.__esModule||e&16&&typeof t.then=="function"))return t;var u=Object.create(null);_.r(u);var d={};l=l||[null,o({}),o([]),o(o)];for(var r=e&2&&t;typeof r=="object"&&!~l.indexOf(r);r=o(r))Object.getOwnPropertyNames(r).forEach(S=>d[S]=()=>t[S]);return d.default=()=>t,_.d(u,d),u}})(),_.d=(o,l)=>{for(var t in l)_.o(l,t)&&!_.o(o,t)&&Object.defineProperty(o,t,{enumerable:!0,get:l[t]})},_.h=()=>"55e5c6a40d444554bfb1",_.hmd=o=>(o=Object.create(o),o.children||(o.children=[]),Object.defineProperty(o,"exports",{enumerable:!0,set:()=>{throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+o.id)}}),o),_.o=(o,l)=>Object.prototype.hasOwnProperty.call(o,l),_.r=o=>{typeof Symbol<"u"&&Symbol.toStringTag&&Object.defineProperty(o,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(o,"__esModule",{value:!0})},_.nmd=o=>(o.paths=[],o.children||(o.children=[]),o),_.p="./",(()=>{var o={8905:0};_.O.j=e=>o[e]===0;var l=(e,u)=>{var[d,r,S]=u,E,T,a=0;if(d.some(h=>o[h]!==0)){for(E in r)_.o(r,E)&&(_.m[E]=r[E]);if(S)var y=S(_)}for(e&&e(u);a<d.length;a++)T=d[a],_.o(o,T)&&o[T]&&o[T][0](),o[d[a]]=0;return _.O(y)},t=global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[];t.forEach(l.bind(null,0)),t.push=l.bind(null,t.push.bind(t))})(),_.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,947,403,2699,7370,1404,3655,816,3322,3792,119],()=>_(_.s=903679)),_.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,947,403,2699,7370,1404,3655,816,3322,3792,119],()=>_(_.s=730659)),_.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,947,403,2699,7370,1404,3655,816,3322,3792,119],()=>_(_.s=639542));var ot=_.O(void 0,[592,6491,8588,7981,719,3823,793,6494,7677,967,947,403,2699,7370,1404,3655,816,3322,3792,119],()=>_(_.s=194383));ot=_.O(ot)})();

//# sourceMappingURL=screenshot_preview.js.map