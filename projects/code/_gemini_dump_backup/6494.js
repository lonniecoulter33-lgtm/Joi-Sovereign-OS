"use strict";(global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[]).push([[6494],{426494:(Me,J,m)=>{m.d(J,{backgroundsReducer:()=>Te,framesReducer:()=>Pe});var Ne=m(266794),je=m(275271),c=m(890368),o=m(625723),He=m(414965),Q=m(905019),We=m.n(Q),_=Object.freeze,C=Object.defineProperty,$=Object.defineProperties,q=Object.getOwnPropertyDescriptors,O=Object.getOwnPropertySymbols,ee=Object.prototype.hasOwnProperty,te=Object.prototype.propertyIsEnumerable,y=(t,e,a)=>e in t?C(t,e,{enumerable:!0,configurable:!0,writable:!0,value:a}):t[e]=a,ae=(t,e)=>{for(var a in e||(e={}))ee.call(e,a)&&y(t,a,e[a]);if(O)for(var a of O(e))te.call(e,a)&&y(t,a,e[a]);return t},re=(t,e)=>$(t,q(e)),s=(t,e)=>_(C(t,"raw",{value:_(e||t.slice())})),ne=`  background: none;
color: inherit;
border: none;
padding: 0;
font: inherit;
cursor: pointer;
outline: inherit;`,F,oe=c.Z.button(F||(F=s([`
  `,`
  border-radius: var(--lns-radius-medium);
  &:focus {
    box-shadow: 0 0 0 2px var(--lns-color-focusRing);
  }
  height: max-content;
  `,`;
`])),ne,t=>t.selected?"background-color: var(--lns-color-highlight); color: var(--lns-color-primaryActive)":`&:hover {
      background: var(--lns-color-backgroundHover);
    }`),S,le=c.Z.div(S||(S=s([`
  `,`

  display: grid;
  `,`
  `,`
  grid-template-areas: 'stack';
  & > * {
    grid-area: stack;
  }
`])),t=>t.itemType==="background"?"height: 56px; width: 56px ;":"height: 116px; width: 116px;",t=>t.scale?"transform: scale(".concat(t.scale,");"):"",t=>t.origin?"transform-origin: ".concat(t.origin,";"):""),k,ce=c.Z.div(k||(k=s([`
  `,`
  border-radius: 50%;
  background-color: `,`;
  `,`
  background-position: center;
  background-size: cover;
`])),t=>t.type==="background"?"height: 48px; width: 48px;":"height: 94px; width: 94px;",t=>t.color||"#FFFFFF",t=>t.imageUrl&&`
    background-image: url(`.concat(t.imageUrl,`);
  `)),I,se=c.Z.div(I||(I=s([`
height: 100%;
border-radius: 50%;
border: 1px solid `,`;
}
`])),t=>t.selected?"rgba(21, 14, 216, 0.5)":"var(--lns-color-border)"),ie=t=>t.label?t.label:t.name&&t.name==="None"?t.name:null,x=t=>{const{selected:e,onSelect:a,children:r,type:l,option:n,circleColor:b,circleUrl:v}=t,h=()=>{a()},u=ie(n),g="".concat(l," ").concat(l==="frame"?n.name:n.type),p=l==="frame"&&n.name.replace(/_/g," ");return React.createElement(oe,{role:"button","aria-label":g,tabIndex:0,onClick:h,selected:e},React.createElement(le,{itemType:l,scale:n?.previewScale,origin:n.previewOrigin},React.createElement(Align,{alignment:"center"},React.createElement(ce,{color:b,imageUrl:v,type:l},React.createElement(se,{selected:e}))),u&&!p&&React.createElement(Align,{alignment:"center"},React.createElement(Text,{size:"body-sm",fontWeight:"bold"},u)),r&&React.createElement(Align,{alignment:"center"},r)),p&&React.createElement(Align,{alignment:"center"},React.createElement(Container,{maxWidth:"100px"},React.createElement(Text,{fontWeight:"bold",size:"body-sm"},p),React.createElement(Spacer,{top:"12px"}))))},me=t=>{const{backgroundOption:e,selected:a,onSelect:r}=t;return React2.createElement(x,{option:e,type:"background",onSelect:r,selected:a,circleUrl:e.thumbnailUrl,circleColor:e.color})},B="custom-image",T="custom-blur",w="custom-color",P="custom-brightness",L=[{id:"none",type:"none",label:"None"}],de=[{id:B,type:"image",label:"C Img",useCustom:!0},{id:T,type:"blur",label:"C Blur",useCustom:!0},{id:w,type:"color",label:"C Clr",useCustom:!0},{id:P,type:"brightness",label:"C Brgt",useCustom:!0}],ue=({option:t,settings:e,customSettingChanged:a})=>React3.createElement(Arrange,{gap:2,autoFlow:"row"},React3.createElement(Text2,{size:"body-lg",fontWeight:"bold"},"Custom Settings"),t.id===w&&React3.createElement(FormField,{label:"Background Color"},React3.createElement(TextInput,{value:e.bgColor,onChange:r=>{a("bgColor",r.target.value)}})),t.id===B&&React3.createElement(FormField,{label:"Image url"},React3.createElement(TextInput,{value:e.bgUrl,onChange:r=>{a("bgUrl",r.target.value)}})),t.id===T&&React3.createElement(FormField,{label:"Blur Radius"},React3.createElement(TextInput,{value:e.blurPx,type:"number",onChange:r=>{a("blurPx",parseInt(r.target.value))}})),t.id===P?React3.createElement(FormField,{label:"Brightness Value (0 - 1)"},React3.createElement(TextInput,{value:e.brightness,step:"any",type:"number",onChange:r=>{a("brightness",parseFloat(r.target.value))}})):null,React3.createElement(Arrange,{gap:2},React3.createElement(FormField,{label:"Camera Width"},React3.createElement(TextInput,{value:e.width,type:"number",onChange:r=>{a("width",parseInt(r.target.value))}})),React3.createElement(FormField,{label:"Camera Height"},React3.createElement(TextInput,{value:e.height,type:"number",onChange:r=>{a("height",parseInt(r.target.value))}})))),A,ge=c.Z.div(A||(A=s([`
  position: relative;
  height: 94px;
  width: 94px;
`]))),U,pe=c.Z.img(U||(U=s([`
  position: absolute;
  left: 0;
  width: 50%;
`]))),D,ve=c.Z.img(D||(D=s([`
  position: absolute;
  left: 0;
  bottom: 0;
  width: 50%;
`]))),M,he=c.Z.img(M||(M=s([`
  position: absolute;
  right: 0;
  width: 50%;
`]))),N,be=c.Z.img(N||(N=s([`
  position: absolute;
  right: 0;
  bottom: 0;
  width: 50%;
`]))),fe=t=>{var e,a,r,l;const{frameOption:n}=t;return React4.createElement(ge,{option:n},React4.createElement(pe,{src:n.topLeftImgSrc,style:(e=n.styleOverrides)==null?void 0:e.topLeft}),React4.createElement(ve,{src:n.bottomLeftImgSrc,style:(a=n.styleOverrides)==null?void 0:a.bottomLeft}),React4.createElement(he,{src:n.topRightImgSrc,style:(r=n.styleOverrides)==null?void 0:r.topRight}),React4.createElement(be,{src:n.bottomRightImgSrc,style:(l=n.styleOverrides)==null?void 0:l.bottomRight}))},Ee=t=>{const{frameOption:e,selected:a,onSelect:r}=t;return React5.createElement(x,{option:e,type:"frame",onSelect:r,selected:a},React5.createElement(fe,{frameOption:e}))},j,Re=c.Z.div(j||(j=s([`
  display: flex;
  flex-direction: column;
  padding: 0;
  height: 100%;
`]))),H,_e=c.Z.div(H||(H=s([`
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
`]))),W,Ce=c.Z.div(W||(W=s([`
  overflow: auto;
  flex-grow: 1;
`]))),Oe=t=>React6.createElement(Container2,{width:"100%",radius:"medium",padding:2,maxHeight:"auto",backgroundColor:"backgroundSecondary",borderSide:"all"},React6.createElement(_e,null,t.children)),V=t=>{const{children:e,title:a}=t;return React6.createElement(Arrange2,{justifyContent:"stretch",width:"100%",gap:2,autoFlow:"row",height:"auto"},React6.createElement(Text3,{size:"body-lg",fontWeight:"bold"},a),React6.createElement(Oe,null,e))},ye=t=>{const{backgroundOptions:e,customBackgroundSettings:a,customSettingChanged:r,frameOptions:l,onBackgroundChange:n,onCancel:b,onFrameChange:v,onSave:h,bannerContents:u,selectedBackgroundOption:g,selectedFrameName:p,withFrames:f}=t,i=()=>u?React6.createElement(Container2,{radius:"medium",paddingX:"medium",paddingY:"12px",backgroundColor:"yellowLight"},React6.createElement(React6.Fragment,null,u)):null,E=()=>React6.createElement(V,{title:"Background"},e.map(d=>React6.createElement(me,{onSelect:()=>n(d),key:d.id,backgroundOption:d,selected:g.id===d.id}))),R=()=>React6.createElement(V,{title:"Frame"},l&&Object.entries(l).map(([d,De])=>React6.createElement(Ee,{key:d,onSelect:()=>{v&&v(d)},frameOption:De,selected:d===p}))),Ue=()=>React6.createElement(Container2,{height:"auto",borderSide:"top",paddingX:3,paddingTop:2,paddingBottom:3},React6.createElement(Arrange2,{justifyContent:"end",gap:1},React6.createElement(Button,{onClick:()=>{b()}},"Cancel"),React6.createElement(Button,{onClick:h,variant:"primary"},"Use these settings")));return React6.createElement(Re,null,React6.createElement(Ce,null,React6.createElement(Container2,{paddingX:3,paddingTop:2,paddingBottom:3},React6.createElement(Arrange2,{justifyContent:"stretch",gap:4,autoFlow:"row",height:"auto"},React6.createElement(i,null),React6.createElement(E,null),g.useCustom&&a&&r&&React6.createElement(ue,{settings:a,option:g,customSettingChanged:r}),f&&l&&React6.createElement(R,null)))),React6.createElement(Ue,null))},Ve=()=>React7.createElement(Text4,{fontWeight:"bold"},"This is a beta early access feature."," ",React7.createElement(Text4,{isInline:!0},"It might make your computer explode. We hope not: cross your fingers! \u{1F91E} If it does, it's totally worth it, though.")),Z=(0,o.PH)("set-selected-background"),Fe=(0,o.PH)("set-revert-background"),z=(0,o.PH)("set-background-options"),K=(0,o.PH)("set-custom-settings"),X=(0,o.PH)("set-selected-frame"),Se=(0,o.PH)("set-revert-frame"),Ze=(0,o.PH)("fetch-latest-frames"),G=(0,o.PH)("set-frames-fetching"),Y=(0,o.PH)("set-frames-data"),ke=(0,o.PH)("frames-last-seen-version"),Ie=(0,o.PH)("store-frames-last-seen-version"),xe=(0,o.PH)("frames-current-version"),ze=(0,o.PH)("show-frames-menu"),Ke=t=>{const{onExit:e,allowCustom:a,withFrames:r,bannerContents:l}=t,n=useDispatch(),{backgroundOptions:b,selectedOption:v,customBackgroundSettings:h}=useSelector(i=>i.backgrounds),{frameItems:u,selectedFrame:g}=useSelector(i=>i.frames),p=b.concat(a?de:[]),f=(i,E)=>{const R=re(ae({},h),{[i]:E});n(K(R))};return React8.createElement(ye,{onBackgroundChange:i=>{n(Z(i))},selectedBackgroundOption:v,onCancel:e,onSave:()=>{e()},backgroundOptions:p,frameOptions:u,customBackgroundSettings:h,customSettingChanged:f,selectedFrameName:g,onFrameChange:i=>{n(X(i))},withFrames:r,bannerContents:l})},Be={revertOption:null,selectedOption:L[0],backgroundOptions:L.slice(),customBackgroundSettings:{blurPx:0,bgColor:"#ff0000",bgUrl:"https://cdn.loom.com/assets/camfort/windows_xp.jpeg",brightness:0,width:854,height:480}},Te=(0,o.Lq)(Be,t=>{t.addCase(Z,(e,a)=>{e.selectedOption=a.payload}).addCase(z,(e,a)=>{e.backgroundOptions=a.payload}).addCase(K,(e,a)=>{e.customBackgroundSettings=a.payload}).addCase(Fe,(e,a)=>{e.revertOption=a.payload})}),we={revertFrame:null,selectedFrame:"None",lastSeenFramesVersion:0,latestFramesVersion:0,showNewFramesAlert:!1,fetching:!1,frameItems:{None:{name:"None"}}},Pe=(0,o.Lq)(we,t=>{t.addCase(X,(e,a)=>{e.selectedFrame=a.payload}).addCase(Y,(e,a)=>{e.frameItems=a.payload.frameItems,e.latestFramesVersion=a.payload.latestFramesVersion}).addCase(G,(e,a)=>{e.fetching=a.payload}).addCase(Ie,(e,a)=>{e.lastSeenFramesVersion=a.payload}).addCase(ke,(e,a)=>{e.lastSeenFramesVersion=a.payload}).addCase(xe,(e,a)=>{e.latestFramesVersion=a.payload}).addCase(Se,(e,a)=>{e.revertFrame=a.payload}).addMatcher(()=>!0,e=>{e.showNewFramesAlert=e.latestFramesVersion>e.lastSeenFramesVersion})}),Le=t=>{const e=t?"backgroundOptions.json":"backgroundOptions-stage.json";return"https://cdn.loom.com/assets/camfort/".concat(e)},Xe=t=>e=>{fetch(Le(t)).then(a=>a.json()).then(a=>{e(z(a))}).catch(()=>{}).finally(()=>{})},Ae=t=>{const e=t?"frameOptions.json":"frameOptions-stage.json";return"https://cdn.loom.com/assets/camfort/".concat(e)},Ge=t=>e=>{fetch2(Ae(t)).then(a=>a.json()).then(a=>{e(Y({frameItems:a.frames,latestFramesVersion:a.version}))}).catch(a=>{console.error("\u{1F5BC}\uFE0F Frames: unable to fetch",a)}).finally(()=>{e(G(!1))})}}}]);

//# sourceMappingURL=6494.js.map