"use strict";(global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[]).push([[6217],{862953:(Ut,Qe,M)=>{var S;S={value:!0},S=void 0;var ye=i(M(275271)),ft=i(M(774586));function i(ve){return ve&&ve.__esModule?ve:{default:ve}}const m=ve=>ye.default.createElement(ft.default,Object.assign({dangerouslySetGlyph:'<path fill="currentcolor" fill-rule="evenodd" d="M7 2.5a4.5 4.5 0 1 0 0 9 4.5 4.5 0 0 0 0-9M1 7a6 6 0 1 1 10.74 3.68l3.29 3.29-1.06 1.06-3.29-3.29A6 6 0 0 1 1 7" clip-rule="evenodd"/>'},ve));m.displayName="SearchIcon";var bt=S=m},450630:(Ut,Qe,M)=>{M.d(Qe,{Ni:()=>i.T,Xn:()=>i.w,F4:()=>wt});var S=M(908866),ye=M(275271),ft=M(117267),i=M(156052),m=M(908308),bt=M(586997),ve=M(853434),qe=M(669957),je=function(K,Z){var B=arguments;if(Z==null||!hasOwnProperty.call(Z,"css"))return createElement.apply(void 0,B);var P=B.length,X=new Array(P);X[0]=Emotion,X[1]=createEmotionProps(K,Z);for(var G=2;G<P;G++)X[G]=B[G];return createElement.apply(null,X)},Ct=!1,Kt=null,da=function(ae){(0,S.Z)(K,ae);function K(B,P,X){return ae.call(this,B,P,X)||this}var Z=K.prototype;return Z.componentDidMount=function(){this.sheet=new ve.m({key:this.props.cache.key+"-global",nonce:this.props.cache.sheet.nonce,container:this.props.cache.sheet.container});var P=document.querySelector("style[data-emotion-"+this.props.cache.key+'="'+this.props.serialized.name+'"]');P!==null&&this.sheet.tags.push(P),this.props.cache.sheet.tags.length&&(this.sheet.before=this.props.cache.sheet.tags[0]),this.insertStyles()},Z.componentDidUpdate=function(P){P.serialized.name!==this.props.serialized.name&&this.insertStyles()},Z.insertStyles=function(){if(this.props.serialized.next!==void 0&&(0,m.M)(this.props.cache,this.props.serialized.next,!0),this.sheet.tags.length){var P=this.sheet.tags[this.sheet.tags.length-1].nextElementSibling;this.sheet.before=P,this.sheet.flush()}this.props.cache.insert("",this.props.serialized,this.sheet,!1)},Z.componentWillUnmount=function(){this.sheet.flush()},Z.render=function(){return null},K}(ye.Component),wt=function(){var K=qe.Z.apply(void 0,arguments),Z="animation-"+K.name;return{name:Z,styles:"@keyframes "+Z+"{"+K.styles+"}",anim:1,toString:function(){return"_EMO_"+this.name+"_"+this.styles+"_EMO_"}}},yt=function ae(K){for(var Z=K.length,B=0,P="";B<Z;B++){var X=K[B];if(X!=null){var G=void 0;switch(typeof X){case"boolean":break;case"object":{if(Array.isArray(X))G=ae(X);else{G="";for(var $e in X)X[$e]&&$e&&(G&&(G+=" "),G+=$e)}break}default:G=X}G&&(P&&(P+=" "),P+=G)}}return P};function Et(ae,K,Z){var B=[],P=(0,m.f)(ae,B,Z);return B.length<2?Z:P+K(B)}var zt=function(){return null},Gt=(0,i.w)(function(ae,K){return(0,ye.createElement)(i.T.Consumer,null,function(Z){var B=!1,P=function(){for(var o=arguments.length,x=new Array(o),y=0;y<o;y++)x[y]=arguments[y];var Be=(0,bt.O)(x,K.registered);return(0,m.M)(K,Be,!1),K.key+"-"+Be.name},X=function(){for(var o=arguments.length,x=new Array(o),y=0;y<o;y++)x[y]=arguments[y];return Et(K.registered,P,yt(x))},G={css:P,cx:X,theme:Z},$e=ae.children(G);B=!0;var et=(0,ye.createElement)(zt,null);return(0,ye.createElement)(ye.Fragment,null,et,$e)})})},183780:(Ut,Qe,M)=>{M.d(Qe,{Ut4:()=>pr});var S=M(738067),ye=M(66292),ft=M.n(ye),i=M(275271),m=M(992671),bt=M(485800),ve=M(582805),qe=M(66333),je=M(797981),Ct=M(773023),Kt=M(484285),da=M(862953),wt=M(12131),yt=M(566172),Et=M.n(yt),zt=M(407770),Gt=M(306317),ae=M(957530),K=M(230967),Z=M(854831),B=Object.defineProperty,P=Object.defineProperties,X=Object.getOwnPropertyDescriptors,G=Object.getOwnPropertySymbols,$e=Object.prototype.hasOwnProperty,et=Object.prototype.propertyIsEnumerable,tt=(e,t,a)=>t in e?B(e,t,{enumerable:!0,configurable:!0,writable:!0,value:a}):e[t]=a,o=(e,t)=>{for(var a in t||(t={}))$e.call(t,a)&&tt(e,a,t[a]);if(G)for(var a of G(t))et.call(t,a)&&tt(e,a,t[a]);return e},x=(e,t)=>P(e,X(t)),y=(e,t)=>{var a={};for(var r in e)$e.call(e,r)&&t.indexOf(r)<0&&(a[r]=e[r]);if(e!=null&&G)for(var r of G(e))t.indexOf(r)<0&&et.call(e,r)&&(a[r]=e[r]);return a},Be=(e,t)=>Math.round(e*t/100),Yt=(e,t)=>x(o({},e),{l:e.l-Be(e.l,t)}),$i=(e,t)=>x(o({},e),{l:e.l+Be(e.l,t)}),Ri=(e,t)=>x(o({},e),{s:e.s+Be(e.s,t)}),Ne=(e,t)=>x(o({},e),{a:t}),ua=15.8,ha=31.6,ma=.14,va=.46,ga=.9,pa=.8,Xt=.25,fa=.06,ba=.15,Ca=.3,wa=.45,oe={red:{h:4,s:64,l:48,a:1},blurpleLight:{h:214.3,s:91.3,l:95.5,a:1},blurpleMedium:{h:216.5,s:92,l:90.2,a:1},blurple:{h:215.4,s:80,l:47.65,a:1},blurpleDark:{h:215.9,s:79.9,l:41,a:1},blurpleStrong:{h:216.3,s:69.2,l:22.9,a:1},offWhite:{h:0,s:0,l:97.25,a:1},blueLight:{h:216.5,s:92,l:90.2,a:1},blue:{h:215.4,s:80,l:47.65,a:1},blueDark:{h:216.3,s:69.2,l:23,a:1},magenta:{h:323,s:42,l:48,a:1},orangeLight:{h:4,s:100,l:91.2,a:1},orange:{h:11,s:100,l:62.2,a:1},orangeDark:{h:10.9,s:100,l:42.2,a:1},tealLight:{h:155,s:70,l:84,a:1},teal:{h:155,s:62,l:32,a:1},tealDark:{h:155,s:55,l:19,a:1},yellowLight:{h:43,s:93,l:82,a:1},yellow:{h:45.5,s:96,l:57,a:1},yellowDark:{h:39.8,s:100,l:49.4,a:1}},Ue={grey8:{h:228,s:6,l:17,a:1},grey7:{h:223,s:6,l:24.5,a:1},grey6:{h:224,s:5,l:44,a:1},grey5:{h:224,s:5,l:57,a:1},grey4:{h:223,s:5,l:73,a:1},grey3:{h:225,s:6,l:87.5,a:1},grey2:{h:210,s:7,l:94.5,a:1},grey1:{h:0,s:0,l:97.25,a:1},white:{h:0,s:0,l:100,a:1}},Jt={record:oe.orange,recordHover:Yt(oe.orange,ua),recordActive:Yt(oe.orange,ha),backdropDark:Ne(Ue.grey8,ga),backdropTwilight:Ne(oe.blurpleStrong,pa),highlight:Ne(oe.blurple,ba),highlightHover:Ne(oe.blurple,Ca),highlightActive:Ne(oe.blurple,wa),warning:{h:45.5,s:96,l:57,a:1,ads:"--ds-background-warning-bold"}},Ve={light:x(o({primary:oe.blurple,primaryHover:oe.blurpleDark,primaryActive:oe.blurpleStrong,body:{h:228,s:6,l:17,a:1,ads:"--ds-text"},bodyDimmed:{h:224,s:5,l:44,a:1,ads:"--ds-text-subtlest"},bodyInverse:{h:0,s:0,l:100,a:1,ads:"--ds-text-inverse"},background:{h:0,s:0,l:100,a:1,ads:"--ds-surface"},backgroundHover:{h:209,s:75.6,l:8,a:.08,ads:"--ds-background-neutral-subtle-hovered"},backgroundActive:{h:225.5,s:56.9,l:10,a:.14,ads:"--ds-background-neutral-subtle-pressed"},backgroundSecondary:{h:0,s:0,l:97.25,a:1,ads:"--ds-surface-sunken"},backgroundSecondary2:{h:0,s:0,l:97.25,a:1,ads:"--ds-surface-sunken"},backgroundNeutral:{h:209,s:76,l:8,a:.08,ads:"--ds-background-neutral"},backgroundNeutralHover:{h:226,s:57,l:1,a:.14,ads:"--ds-background-neutral-hovered"},backgroundNeutralActive:{h:223,s:61,l:8,a:.28,ads:"--ds-background-neutral-pressed"},backgroundInverse:{h:228,s:6,l:17,a:1,ads:"--ds-background-neutral-bold"},focusRing:{h:216.1,s:81.4,l:60,a:1,ads:"--ds-border-focused"},overlay:{h:0,s:0,l:100,a:1,ads:"--ds-surface-overlay"},overlayHover:Ue.grey2,overlayActive:Ue.grey3,backdrop:{h:224,s:72,l:7,a:va,ads:"--ds-blanket"},border:{h:225.5,s:57,l:10,a:ma,ads:"--ds-border"}},Jt),{info:{h:215,s:80.25,l:47.65,a:1,ads:"--ds-background-information-bold"},success:{h:155,s:62,l:32,a:1,ads:"--ds-background-accent-green-bolder"},danger:{h:4,s:64,l:48,a:1,ads:"--ds-background-danger-bold"},dangerHover:{h:4.3,s:65.7,l:41.2,a:1,ads:"--ds-background-danger-bold-hovered"},dangerActive:{h:4.5,s:56.3,l:23.3,a:1,ads:"--ds-background-danger-bold-pressed"},disabledContent:{h:223,s:5,l:73,a:1,ads:"--ds-text-disabled"},disabledBackground:{h:0,s:0,l:9,a:.03,ads:"--ds-background-disabled"},formFieldBorder:{h:223.6,s:5,l:57,a:1,ads:"--ds-border-input"},formFieldBackground:{h:0,s:0,l:100,a:1,ads:"--ds-background-input"},buttonBorder:{h:252,s:13,l:46,a:Xt,ads:"--ds-border"},tabBackground:{h:209,s:75.6,l:8,a:fa,ads:"--ds-background-neutral"},upgrade:{h:277.5,s:89,l:96.5,a:1,ads:"--ds-background-discovery"},upgradeHover:{h:277,s:86,l:91.6,a:1,ads:"--ds-background-discovery-hovered"},upgradeActive:{h:278.6,s:84.5,l:79.8,a:1,ads:"--ds-background-discovery-pressed"},discoveryBackground:{h:278.6,s:48.4,l:52.2,a:1,ads:"--ds-background-discovery-bold"},discoveryLightBackground:{h:277.5,s:89,l:96.5,a:1,ads:"--ds-background-discovery"},discoveryTitle:{h:228,s:6,l:17,a:1,ads:"--ds-text"},discoveryHighlight:{h:277.5,s:89,l:96.5,a:1,ads:"--ds-background-discovery"}}),dark:x(o({primary:{h:216.3,s:83.2,l:67.3,a:1},primaryHover:{h:216.1,s:85.1,l:76.3,a:1},primaryActive:{h:216.5,s:92,l:90.2,a:1},body:{h:225,s:4.3,l:81.6,a:1,ads:"--ds-text"},bodyDimmed:{h:217.5,s:4,l:60.4,a:1,ads:"--ds-text-subtlest"},bodyInverse:{h:240,s:3,l:12.5,a:1,ads:"--ds-text-inverse"},background:{h:240,s:3,l:12.5,a:1,ads:"--ds-surface"},backgroundHover:{h:240,s:12.6,l:83,a:.07,ads:"--ds-background-neutral-subtle-hovered"},backgroundActive:{h:236,s:36.6,l:92,a:.12,ads:"--ds-background-neutral-subtle-pressed"},backgroundSecondary:{h:210,s:4,l:9.8,a:1,ads:"--ds-surface-sunken"},backgroundSecondary2:{h:210,s:4,l:9.8,a:1,ads:"--ds-surface-sunken"},backgroundNeutral:{h:240,s:12.6,l:83,a:.07,ads:"--ds-background-neutral"},backgroundNeutralHover:{h:236,s:36.6,l:92,a:.12,ads:"--ds-background-neutral-hovered"},backgroundNeutralActive:{h:226,s:49,l:93,a:.25,ads:"--ds-background-neutral-pressed"},backgroundInverse:{h:225,s:4.3,l:81.6,a:1,ads:"--ds-background-neutral-bold"},focusRing:{h:216.1,s:85.1,l:76.3,a:1,ads:"--ds-background-accent-blue-subtle-hovered"},overlay:{h:225,s:4,l:17.6,a:1,ads:"--ds-surface-overlay"},overlayHover:{h:225,s:4,l:19.61,a:1,ads:"--ds-surface-overlay-hovered"},overlayActive:{h:225,s:4.69,l:25.1,a:1,ads:"--ds-surface-overlay-pressed"},backdrop:{h:210,s:11,l:7,a:.6,ads:"--ds-blanket"},border:{h:236,s:36.6,l:92,a:.12,ads:"--ds-border"}},Jt),{info:{h:216.3,s:83,l:67.25,a:1,ads:"--ds-background-information-bold"},success:{h:155,s:57,l:55,a:1,ads:"--ds-background-accent-green-bolder"},danger:{h:3.75,s:91,l:69,a:1,ads:"--ds-background-danger-bold"},dangerHover:{h:4,s:96,l:78,a:1,ads:"--ds-background-danger-bold-hovered"},dangerActive:{h:4,s:100,l:91.2,a:1,ads:"--ds-background-danger-bold-pressed"},disabledContent:{h:225,s:5,l:33,a:1,ads:"--ds-text-disabled"},disabledBackground:{h:0,s:0,l:1,a:.46,ads:"--ds-background-disabled"},formFieldBorder:{h:222,s:4,l:51.4,a:1,ads:"--ds-border-input"},formFieldBackground:{h:225,s:5,l:15,a:1,ads:"--ds-background-input"},buttonBorder:{h:0,s:0,l:100,a:Xt,ads:"--ds-border"},tabBackground:{h:240,s:12.6,l:83,a:.07,ads:"--ds-background-neutral"},upgrade:{h:277.8,s:27.3,l:19.4,a:1,ads:"--ds-background-discovery"},upgradeHover:{h:278,s:44.2,l:25.3,a:1,ads:"--ds-background-discovery-hovered"},upgradeActive:{h:278,s:45,l:44.7,a:1,ads:"--ds-background-discovery-pressed"},discoveryBackground:{h:278.5,s:84.5,l:72.2,a:1,ads:"--ds-background-discovery-bold"},discoveryLightBackground:{h:277.8,s:27.3,l:19.4,a:1,ads:"--ds-background-discovery"},discoveryTitle:{h:225,s:4.3,l:81.6,a:1,ads:"--ds-text"},discoveryHighlight:{h:277.8,s:27.3,l:19.4,a:1,ads:"--ds-background-discovery"}})},te=o(o({},oe),Ue),Qt=[...Object.keys(te),...Object.keys(Ve.light)],ki=(e,t)=>`hsla(${te[e].h},${te[e].s}%,${te[e].l}%,${t})`,Mi=(e,t,a)=>{const r=()=>{if(t==="dark")return te[e].l-te[e].l*a;if(t==="light")return te[e].l+te[e].l*a};return`hsla(${te[e].h},${te[e].s}%,${Math.round(r())}%,${te[e].a})`},c=e=>{if(e)return e in te||e in Ve.light?`var(--lns-color-${e})`:e in or?`var(--lns-gradient-${e})`:e};function ya(e,t,a){const r=React.useCallback(()=>typeof window>"u"?a:t[e.findIndex(s=>matchMedia(s).matches)]||a,[a,e,t]),[l,n]=React.useState(r);return React.useEffect(()=>{const s=_debounce(()=>n(r),150);return window.addEventListener("resize",s),()=>window.removeEventListener("resize",s)},[r]),l}var u=e=>e&&`calc(${e} * var(--lns-unit, ${De}px))`,ce=e=>{if(e in nt)return`var(--lns-space-${e})`;if(e&&isNaN(e))return`${e}`;if(e===0)return"0";if(e)return`${u(e)}`},b=(e,t)=>{if(t||t===0){if(Array.isArray(t)){const a=t.map(r=>`${e}: ${ce(r)}`);return We(a)}if(typeof t=="object"){const a={};return Object.entries(t).forEach(([r,l])=>a[r]=ce(l)),Ke(e,a)}return`${e}: ${ce(t)};`}},qt=(e,t,a)=>`@media(${e}: ${t}){${a}}`,We=e=>{const t=Object.values(Me)[0],a=qt("max-width",t,e[0]),r=e.reduce((l,n,s)=>{const d=`${Object.values(Me)[s]}`;return l+qt("min-width",d,n)},"");return a+r},Ke=(e,t)=>{const a=[];return t.default&&a.push(`${e}: ${t.default};`),delete t.default,Object.entries(t).forEach(([r,l])=>{const n=r in Me?Me[r]:r;a.push(`@media(min-width: ${n}){ ${e}: ${l} }`)}),a.join(" ")},le=(e,t)=>{if(Array.isArray(t)){const a=t.map(r=>`${e}: ${r};`);return We(a)}return typeof t=="object"?Ke(e,t):`${e}: ${t};`},er=(e,t)=>{if(e){if(Array.isArray(e)){const a=[];return e.map(r=>{a.push(t[r])}),le("align-items",a)}return`align-items ${t[e]};`}},Ea=(e,t,a)=>{if(Array.isArray(a)){const r=a.map(l=>{const n=l===!0?t[0]:t[1];return`${e}: ${n};`});return We(r)}return`${e}: ${t[0]};`},tr=(e,t)=>{if(t||t===0){if(Array.isArray(t)){const a=t.map(r=>`${e}: ${r}`);return We(a)}return typeof t=="object"&&!Array.isArray(t)?Ke(e,t):`${e}: ${t};`}},rt=e=>Array.isArray(e)?e.map(t=>ce(t)).join(" "):e,Li=e=>{if(e){if(typeof e=="object"&&!Array.isArray(e)){const t={};return Object.entries(e).forEach(([a,r])=>t[a]=rt(r)),Ke("grid-template-columns",t)}return`grid-template-columns: ${rt(e)};`}},rr=(e,t)=>{if(e){if(typeof e=="object"&&!Array.isArray(e)){const a={};return Object.entries(e).forEach(([r,l])=>a[r]=rt(l)),Ke(`grid-template-${t}`,a)}return`grid-template-${t}: ${rt(e)};`}},Hi=({children:e,queries:t,values:a,defaultValue:r})=>{const l=ya(t,a,r);return e(l)},ge=e=>e&&`
  font-size: var(--lns-fontSize-${e});
  line-height: var(--lns-lineHeight-${e});
  letter-spacing: var(--lns-letterSpacing-${e});
`,Re=e=>e&&`font-weight: var(--lns-fontWeight-${e});`,za=e=>e&&`var(--lns-fontSetting-${e});`,F=e=>e&&`border-radius: var(--lns-radius-${e});`,Ge=e=>e&&`box-shadow: var(--lns-shadow-${e});`,de=(e,t)=>{const a=e||c("focusRing");return`box-shadow:${t||""} 0 0 0 2px ${a};`},at=e=>`
  outline: 2px solid ${e||c("focusRing")};
  outline-offset: 1px;
  `,ar=e=>{if(e==="ol"||e==="ul")return`
      list-style-type: none;
      margin: 0;
      padding: 0
      `},xt=(e,t)=>({center:{bottom:0,top:`calc((100vh - ${e}) / 2)`,position:"relative"},bottom:{bottom:0,top:"unset",position:"absolute"},undefined:{bottom:void 0,top:"15vh",position:"relative"}})[t],lt=e=>e.replace(/([a-z0-9])([A-Z])/g,"$1-$2").replace(/[\s_]+/g,"-").toLowerCase(),De=8,ke={small:{fontSize:1.5,lineHeight:1.5,letterSpacing:"normal"},"body-sm":{fontSize:1.5,lineHeight:1.5,letterSpacing:"normal"},medium:{fontSize:1.75,lineHeight:1.57,letterSpacing:"normal"},"body-md":{fontSize:1.75,lineHeight:1.57,letterSpacing:"normal"},large:{fontSize:2.25,lineHeight:1.44,letterSpacing:"-0.2px"},"body-lg":{fontSize:2.25,lineHeight:1.44,letterSpacing:"-0.2px"},xlarge:{fontSize:3,lineHeight:1.16,letterSpacing:"-0.2px"},"heading-sm":{fontSize:3,lineHeight:1.16,letterSpacing:"-0.2px"},xxlarge:{fontSize:4,lineHeight:1.125,letterSpacing:"-0.5px"},"heading-md":{fontSize:4,lineHeight:1.125,letterSpacing:"-0.5px"},xxxlarge:{fontSize:6,lineHeight:1.16,letterSpacing:"-1.2px"},"heading-lg":{fontSize:6,lineHeight:1.16,letterSpacing:"-1.2px"}},lr={book:400,regular:400,medium:500,bold:653},xa={normal:"'normal'",tnum:"'tnum'"},nr={none:u(0),50:u(.5),100:u(1),medium:u(1),150:u(1.5),175:u(1.75),200:u(2),large:u(2),250:u(2.5),300:u(3),xlarge:u(3),round:u(999),full:u(999)},$t={small:`0 ${u(.5)} ${u(1.25)} hsla(0, 0%, 0%, 0.05)`,medium:`0 ${u(.5)} ${u(1.25)} hsla(0, 0%, 0%, 0.1)`,large:`0 ${u(.75)} ${u(3)} hsla(0, 0%, 0%, 0.1)`},nt={xsmall:.5,small:1,medium:2,large:3,xlarge:5,xxlarge:8},Me={xsmall:"31em",small:"48em",medium:"64em",large:"75em"},or={"ai-primary":"conic-gradient(from 270deg, #0469FF 90deg, #BF63F3 180deg, #FFA900 270deg, #0065FF 360deg)","ai-secondary":"radial-gradient(138.41% 100% at 100% 100%, #E9F2FE 0%, #FFF 100%)"},$a=`Lens: Text prop 'isDimmed' is deprecated, use color="bodyDimmed" instead.`,Rt="Lens: don't apply custom styles to components, learn more: https://lens.loom.dev/guides/development-best-practices/the-risk-of-modifying-components-with-custom-styles.",Ra=null,ir="Lens: Layout component is deprecated. Use Arrange or Split.",ka=.6,kt={body:{size:"body-md",fontWeight:"regular"},title:{size:"body-lg",fontWeight:"bold"},mainTitle:{size:"heading-md",fontWeight:"bold"}},sr=e=>ke[e].fontSize*De,cr=e=>u(ke[e].fontSize),ot=e=>ke[e].fontSize*ke[e].lineHeight*De,dr=(e,t,a,r)=>{const l=(t-e)/(r-a);return`${-a*l+e}px + ${l*100}vw`},Ma=m.Z.span`
  display: ${e=>e.isInline?"inline":"block"};
  ${e=>!e.sizeMinMax&&ge(e.size)};
  ${e=>Re(e.fontWeight)};
  ${e=>e.color&&`color: ${c(e.color)}`};
  ${e=>e.fontSetting&&`font-feature-settings: ${za(e.fontSetting)}`};
  ${e=>e.isDimmed&&`opacity: ${ka}`};
  ${e=>e.alignment&&`text-align: ${e.alignment}`};
  ${e=>e.hasEllipsis&&!e.ellipsisLines&&`
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  `};
  ${e=>e.hasEllipsis&&e.ellipsisLines&&`
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: ${e.ellipsisLines};
  `};
  ${e=>!e.hasEllipsis&&e.noWrap&&"white-space: nowrap; overflow: hidden;"};
  ${e=>e.sizeMinMax&&`
    min-height: 0vw;
    font-size: clamp(
      ${cr(e.sizeMinMax[0])},
      ${dr(sr(e.sizeMinMax[0]),sr(e.sizeMinMax[1]),496,1200)},
      ${cr(e.sizeMinMax[1])}
    );

    line-height: clamp(
      ${ot(e.sizeMinMax[0])}px,
      ${dr(ot(e.sizeMinMax[0]),ot(e.sizeMinMax[1]),496,1200)},
      ${ot(e.sizeMinMax[1])}px
    );
  `}
`,La=e=>{var t=e,{children:a,size:r="body-md",color:l,isInline:n,isDimmed:s,fontWeight:d="regular",hasEllipsis:h,ellipsisLines:v,noWrap:p,variant:g,htmlTag:f="span",alignment:C,sizeMinMax:z,fontSetting:E="normal"}=t,w=y(t,["children","size","color","isInline","isDimmed","fontWeight","hasEllipsis","ellipsisLines","noWrap","variant","htmlTag","alignment","sizeMinMax","fontSetting"]);return s&&console.warn($a),r.includes("heading-")&&(d="bold"),i.createElement(Ma,o({size:g?kt[g].size:r,color:l,isInline:n,isDimmed:s,fontWeight:g?kt[g].fontWeight:d,hasEllipsis:h,ellipsisLines:v,noWrap:p,variant:g,as:f,alignment:C,sizeMinMax:z,fontSetting:E},w),a)},Ha=["left","right","center"],Ee=La,it=["top","bottom","left","right"],ur=o({0:"0"},nt),Mt=o({0:"0",auto:"auto"},nt),_a=Qt.map(e=>({selector:"c",modifier:e,declarations:[{property:"color",value:`var(--lns-color-${e})`}]})),Sa=Qt.map(e=>({selector:"bgc",modifier:e,declarations:[{property:"background-color",value:`var(--lns-color-${e})`}]})),Ia=Object.keys(ke).map(e=>({selector:"text",modifier:e,declarations:[{property:"font-size",value:`var(--lns-fontSize-${e})`},{property:"line-height",value:`var(--lns-lineHeight-${e})`},{property:"letter-spacing",value:`var(--lns-letterSpacing-${e})`},e.includes("heading-")||e.includes("xlarge")?{property:"font-weight",value:"var(--lns-fontWeight-bold)"}:{property:"font-weight",value:"var(--lns-fontWeight-regular)"}]})),Ba=Object.keys(lr).map(e=>({selector:"weight",modifier:e,declarations:[{property:"font-weight",value:`var(--lns-fontWeight-${e})`}]})),Va=Object.entries(kt).map(([e,t])=>({selector:"text",modifier:e,declarations:[{property:"font-size",value:`var(--lns-fontSize-${t.size})`},{property:"line-height",value:`var(--lns-lineHeight-${t.size})`},{property:"font-weight",value:`var(--lns-fontWeight-${t.fontWeight})`}]})),Wa=Ha.map(e=>({selector:"text",modifier:e,declarations:[{property:"text-align",value:e}]})),Da=Object.keys($t).map(e=>({selector:"shadow",modifier:e,declarations:[{property:"box-shadow",value:`var(--lns-shadow-${e})`}]})),Oa=Object.keys(nr).map(e=>({selector:"radius",modifier:e,declarations:[{property:"border-radius",value:`var(--lns-radius-${e})`}]})),Ye=(e,t,a,r)=>{const l=[];return t.map(n=>{const s=r?`${e.charAt(0)}${n.charAt(0)}`:n;Object.keys(a).map(d=>{l.push({selector:s,property:`${e}${n&&e?`-${n}`:n||""}`,modifier:d,value:d==="auto"||d==="0"?d:`var(--lns-space-${d})`})})}),l},Aa=Object.values(Ye("margin",["",...it],Mt,"shortSides")).map(e=>({selector:e.selector,modifier:e.modifier,declarations:[{property:e.property,value:e.value}]})),Pa=Object.values(Ye("margin",["x","y"],Mt,"shortSides")).map(e=>({selector:e.selector,modifier:e.modifier,declarations:[{property:e.property==="margin-x"?"margin-left":"margin-top",value:e.value},{property:e.property==="margin-x"?"margin-right":"margin-bottom",value:e.value}]})),Fa=Object.values(Ye("padding",["",...it],ur,"shortSides")).map(e=>({selector:e.selector,modifier:e.modifier,declarations:[{property:e.property,value:e.value}]})),Ta=Object.values(Ye("padding",["x","y"],ur,"shortSides")).map(e=>({selector:e.selector,modifier:e.modifier,declarations:[{property:e.property==="padding-x"?"padding-left":"padding-top",value:e.value},{property:e.property==="padding-x"?"padding-right":"padding-bottom",value:e.value}]})),Za=["",...it].map(e=>{const t="border"+e.replace(e.charAt(0),e.charAt(0).toUpperCase()),a=`border${e&&`-${e}`}`;return{selector:t,declarations:[{property:a,value:"1px solid var(--lns-color-border)"}]}}),ja=["inline","block","flex","inlineBlock","inlineFlex","none"],Na=ja.map(e=>({selector:e,declarations:[{property:"display",value:lt(e)}]})),Ua=[{selector:"flexWrap",declarations:[{property:"flex-wrap",value:"wrap"}]}],Ka=["column","row"],Ga=Ka.map(e=>({selector:"flexDirection",modifier:e,declarations:[{property:"flex-direction",value:e}]})),Ya=["stretch","center","baseline","flexStart","flexEnd","selfStart","selfEnd"],Xa=Ya.map(e=>({selector:"items",modifier:e,declarations:[{property:"align-items",value:lt(e)}]})),Ja=["flexStart","flexEnd","center","spaceBetween","spaceAround","spaceEvenly"],Qa=Ja.map(e=>({selector:"justify",modifier:e,declarations:[{property:"justify-content",value:lt(e)}]})),qa=["0","1"],el=qa.map(e=>({selector:"grow",modifier:e,declarations:[{property:"flex-grow",value:e}]})),tl=["0","1"],rl=tl.map(e=>({selector:"shrink",modifier:e,declarations:[{property:"flex-shrink",value:e}]})),al=["auto","flexStart","flexEnd","center","baseline","stretch"],ll=al.map(e=>({selector:"self",modifier:e,declarations:[{property:"align-self",value:lt(e)}]})),nl=["hidden","auto"],ol=nl.map(e=>({selector:"overflow",modifier:e,declarations:[{property:"overflow",value:e}]})),il=["relative","absolute","sticky","fixed"],sl=il.map(e=>({selector:e,declarations:[{property:"position",value:e}]})),cl=Object.values(Ye("",it,Mt)).map(e=>({selector:e.selector,modifier:e.modifier,declarations:[{property:e.property,value:e.value}]})),dl=["auto","full","0"],ul=dl.map(e=>({selector:"width",modifier:e,declarations:[{property:"width",value:e==="full"?"100%":e}]})),hl=[{selector:"minWidth",modifier:"0",declarations:[{property:"min-width",value:"0"}]}],ml=["auto","full","0"],vl=ml.map(e=>({selector:"height",modifier:e,declarations:[{property:"height",value:e==="full"?"100%":e}]})),gl=[{selector:"ellipsis",declarations:[{property:"overflow",value:"hidden"},{property:"text-overflow",value:"ellipsis"},{property:"white-space",value:"nowrap"}]}],pl=[{selector:"srOnly",declarations:[{property:"position",value:"absolute"},{property:"width",value:"1px"},{property:"height",value:"1px"},{property:"padding",value:"0"},{property:"margin",value:"-1px"},{property:"overflow",value:"hidden"},{property:"clip",value:"rect(0, 0, 0, 0)"},{property:"white-space",value:"nowrap"},{property:"border-width",value:"0"}]}],fl="\\:",hr=[..._a,...Da,...Oa,...Sa,...Aa,...Pa,...Fa,...Ta,...Ia,...Ba,...Va,...Wa,...Za,...Na,...Ua,...Ga,...Xa,...Qa,...el,...rl,...ll,...ol,...sl,...cl,...ul,...hl,...vl,...gl,...pl],mr=(e,t)=>{const a=[],r=t?`${t}-`:"";return e.map(l=>{const n=[];l.declarations.map(d=>{n.push(`${d.property}:${d.value}`)});const s=`.${r}${l.selector}${l.modifier?fl:""}${l.modifier?l.modifier:""}{${n.join(";")}}`;a.push(s)}),a.join("")},bl={xs:Me.xsmall,sm:Me.small,md:Me.medium,lg:Me.large},Cl=()=>(()=>{const t=[];return t.push(`${mr(hr)}`),Object.entries(bl).map(([a,r])=>{t.push(`@media(min-width:${r}){${mr(hr,a)}}`)}),t.join("")})(),ue=(e,t)=>{const a={};return Object.entries(t).forEach(([r,l])=>{const s=`--lns-${(e?`${e}-`:"")+r}`;a[s]=l}),a},wl=()=>{const e={};return Object.entries(ke).forEach(([t,a])=>{const r={},l={},n={},s=`fontSize-${t}`,d=`lineHeight-${t}`,h=`letterSpacing-${t}`;r[s]=u(a.fontSize),r[d]=a.lineHeight,r[h]=a.letterSpacing,Object.assign(e,r,l,n)}),e},yl=()=>{const e={};return Object.entries(nt).forEach(([t,a])=>{const r=`space-${t}`;e[r]=u(a)}),e},El=()=>{const e={};return Object.keys(o(o({},oe),Ue)).forEach(t=>{const a=t;e[a]=`hsla(${te[t].h},${te[t].s}%,${te[t].l}%,${te[t].a})`}),e},zl=()=>{const e=(t,a)=>Object.keys(t).reduce((r,l)=>{const n=t[l],s=`${a}-color-${l}`;return r[s]=n.ads?`var(${n.ads}, hsla(${n.h},${n.s}%,${n.l}%,${n.a}))`:`hsla(${n.h},${n.s}%,${n.l}%,${n.a})`,r},{});return o(o({},e(Ve.light,"themeLight")),e(Ve.dark,"themeDark"))},xl=ue(void 0,{unit:`${De/16}rem`}),$l=ue("fontWeight",lr),Rl=ue("fontSetting",xa),kl=ue(void 0,wl()),Ml=ue("radius",nr),Ll=ue("shadow",$t),Hl=ue(void 0,yl()),_l=ue(void 0,{formFieldBorderWidth:"1px",formFieldBorderWidthFocus:"2px",formFieldHeight:u(4.5),formFieldRadius:"var(--lns-radius-175)",formFieldHorizontalPadding:u(2),formFieldBorderShadow:`
    inset 0 0 0 var(--lns-formFieldBorderWidth) var(--lns-color-formFieldBorder)
  `,formFieldBorderShadowFocus:`
    inset 0 0 0 var(--lns-formFieldBorderWidthFocus) var(--lns-color-blurple),
    0 0 0 var(--lns-formFieldBorderWidthFocus) var(--lns-color-focusRing)
  `,formFieldBorderShadowError:`
    inset 0 0 0 var(--lns-formFieldBorderWidthFocus) var(--lns-color-danger),
    0 0 0 var(--lns-formFieldBorderWidthFocus) var(--lns-color-orangeLight)
  `}),Sl=ue("color",El()),Il=ue(void 0,zl()),Bl=ue("gradient",or),vr=[xl,kl,Ml,Ll,Hl,_l],Vl=()=>Object.assign({},...vr),Wl=()=>Object.assign({},$l,...vr,Rl),Dl=()=>o(o(o({},Sl),Il),Bl),Ol=()=>Object.keys(Ve.light).map(e=>`--lns-color-${e}: var(--lns-themeLight-color-${e});`),Al=()=>Object.keys(Ve.dark).map(e=>`--lns-color-${e}: var(--lns-themeDark-color-${e});`),gr=(e=":root")=>`
    ${e||":root"},
    .theme-light,
    [data-lens-theme="light"] {
      ${Ol().join("")}
    }

    .theme-dark,
    [data-lens-theme="dark"] {
      ${Al().join("")}
    }
  `,_i=()=>{const e=document.createElement("style");e.innerHTML=gr(),document.head.appendChild(e)},Si=()=>Object.entries(Vl()).map(t=>`${t[0]}:${t[1]};`).join(""),Pl=e=>{const t=[],a=e||":root";return Object.entries(Wl()).forEach(r=>{t.push(`${r[0]}:${r[1]};`)}),Object.entries(Dl()).forEach(r=>{t.push(`${r[0]}:${r[1]};`)}),`
    ${a} {
      ${t.join("")}
    }
  `},Fl=e=>{switch(e){case"orange":return{background:"orangeLight",text:"dangerHover"};case"blue":return{background:"blueLight",text:"blueDark"};case"yellow":return{background:"yellowLight",text:"#9E4C00"};case"teal":return{background:"tealLight",text:"tealDark"};default:return{background:"orangeLight",text:"dangerHover"}}},Tl=e=>`calc(${e} / 2)`,Le=e=>{let t,a;if(e==="medium")t=u(4),a=u(4);else if(e==="large")t=u(7),a=u(7);else{const l=ce(e);t=l,a=l}const r=Tl(t);return{width:t,height:a,fontSize:r}},Zl=m.Z.span`
  display: block;
  color: ${e=>e.color?e.color.startsWith("#")?e.color:`var(--lns-color-${e.color})`:"var(--lns-color-blueLight)"};
  background-color: var(--lns-color-background);
  ${F("full")};
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  font-weight: var(--lns-fontWeight-bold);
  width: ${e=>{const{width:t}=Le(e.size);return t}};
  height: ${e=>{const{height:t}=Le(e.size);return t}};
  font-size: ${e=>{const{fontSize:t}=Le(e.size);return t}};
  position: relative;
  z-index: 0;

  &:after {
    content: '';
    width: 100%;
    height: 100%;
    position: absolute;
    left: 0;
    top: 0;
    z-index: -1;
    background-color: ${e=>e.hasBackgroundColor&&(e.backgroundColor?`var(--lns-color-${e.backgroundColor})`:"var(--lns-color-orange)")};
  }
`,jl=m.Z.img`
  max-width: 100%;
  width: ${e=>{const{width:t}=Le(e.size);return t}};
  height: ${e=>{const{height:t}=Le(e.size);return t}};
  font-size: ${e=>{const{fontSize:t}=Le(e.size);return t}};
`,Ii=e=>{var t=e,{altText:a="",size:r=4,letter:l,imageSrc:n,children:s,themeColor:d="blue"}=t,h=y(t,["altText","size","letter","imageSrc","children","themeColor"]);const v=()=>{if(s)return s;if(n){const f=Le(r).height,C=Le(r).width;return React3.createElement(jl,{size:r,alt:a,src:n,height:f,width:C})}if(l)return a?React3.createElement("span",{"aria-label":a},l):l},p=l&&!n&&!s,g=Fl(d||"blue");return React3.createElement(Zl,o({hasBackgroundColor:p,size:r,backgroundColor:g.background,color:g.text},h),v())},Bi=null,pr=(e=":root",t="body")=>`
    ${e} {
      font-size: 100%;
    }
    ${t} {
      --lns-fontFamily-body: "Atlassian Sans", ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, system-ui, "Helvetica Neue", sans-serif;
      --lns-fontFamily-heading: "Atlassian Sans", ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, system-ui, "Helvetica Neue", sans-serif;
      --lns-fontFamily-code: "Atlassian Mono", ui-monospace, Menlo, "Segoe UI Mono", "Ubuntu Mono", monospace;

      font-family: var(--lns-fontFamily-body);
      color: var(--ds-text, ${c("body")});
      ${ge("body-md")};
    }

    ${t} *,
    ${t} *:before,
    ${t} *:after {
      box-sizing: border-box;
    }

    ${t} * {
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    ${gr(e)}

    ${Pl(e)}

    ${Cl()}
  `,Vi=()=>React4.createElement(Global,{styles:css(pr())}),Wi=null,Nl=3,Ul=m.Z.span`
  display: block;
  color: ${e=>c(e.color)};

  & > svg,
  & > img {
    display: block;
    ${e=>b("width",e.size)};
    ${e=>b("height",e.size)};
  }

  // TODO: remove data-testid once all icons are using ADS
  [data-testid='ads-refreshed-icon'] {
    display: block;
    ${e=>b("width",e.size)};
    ${e=>b("height",e.size)};

    svg {
      padding: 8%;
      height: 100%;
      width: 100%;
    }
  }
`,Kl=e=>{var t=e,{altText:a,icon:r,color:l="body",size:n=Nl}=t,s=y(t,["altText","icon","color","size"]);const d=i.useRef(null);return i.createElement(Ul,o({ref:d,"aria-label":a,color:l,size:n},s),r)},Q=Kl,fr=1,Lt=8,Ht={small:{totalSize:18},medium:{totalSize:24},large:{totalSize:48}},st=e=>Ht[e.size].totalSize/6,_t=e=>Ht[e.size].totalSize,Gl=S.F4`
  50% {
    transform: scale(1);
  }
`,Yl=m.Z.span`
  display: inline-block;
  vertical-align: middle;
  height: ${e=>_t(e)}px;
  width: ${e=>_t(e)}px;
`,Xl=m.Z.span`
  display: grid;
  grid-template-areas: 'stack';
  height: 100%;
  width: 100%;
`,Jl=m.Z.span`
  grid-area: stack;
  place-self: center;
  transform: rotate(${e=>e.position*(360/Lt)}deg)
    translateY(${e=>_t(e)/2-st(e)/2}px);

  &:after {
    content: '';
    height: ${e=>st(e)}px;
    width: ${e=>st(e)}px;
    border-radius: ${e=>st(e)}px;
    background-color: ${e=>c(e.color)};
    display: block;
    transform: scale(0.65);
    animation: ${Gl} ${fr}s
      ${e=>e.position*fr/Lt}s ease-in-out infinite;
  }
`,Ql=({position:e,color:t,size:a})=>i.createElement(Jl,{color:t,position:e,size:a}),ql=e=>{var t=e,{color:a="body",size:r="medium"}=t,l=y(t,["color","size"]);let n;const s=[];for(n=0;n<Lt;n++)s.push(i.createElement(Ql,{color:a,position:n,size:r,key:n}));return i.createElement(Yl,o({size:r},l),i.createElement(Xl,null,s))},Di=Object.keys(Ht),St=ql,ie={small:{height:u(4),textSize:"small",iconSize:2,xSpace:u(1.5),radius:"var(--lns-radius-150)"},medium:{height:u(4.5),textSize:"medium",iconSize:3,xSpace:u(2),radius:"var(--lns-radius-175)"},large:{height:u(7),textSize:"large",iconSize:4,xSpace:u(2.5),radius:"var(--lns-radius-250)"}},It=e=>S.iv`
  ${e.hasLoader&&"display: none"};
`,pe={neutral:{color:c("body"),background:"transparent",borderColor:c("buttonBorder"),hover:c("backgroundHover"),active:c("backgroundActive"),floatingBackground:c("overlay"),floatingHover:c("overlayHover"),floatingActive:c("overlayActive")},neutralSecondary:{color:c("body"),background:c("backgroundNeutral"),borderColor:null,hover:c("backgroundNeutralHover"),active:c("backgroundNeutralActive")},primary:{color:c("white"),background:c("blurple"),borderColor:null,hover:c("primaryHover"),active:c("primaryActive")},secondary:{color:c("primary"),background:c("highlight"),borderColor:null,hover:c("highlightHover"),active:null},record:{color:c("white"),background:c("record"),borderColor:null,hover:c("recordHover"),active:c("recordActive")},upgrade:{color:c("body"),background:c("upgrade"),borderColor:null,hover:c("upgradeHover"),active:c("upgradeActive"),focusRing:de()},danger:{color:c("bodyInverse"),background:c("danger"),borderColor:null,hover:c("dangerHover"),active:c("dangerActive")},ai:{color:c("white"),background:c("ai-primary"),borderColor:null,hover:null,active:null}},br=e=>({enabled:S.iv`
    cursor: pointer;
  `,disabled:S.iv`
    ${e.ariaDisabled&&"aria-disabled: true"};
    pointer-events: none;
    background-color: ${c("disabledBackground")};
    color: ${c("disabledContent")};
    border: none;
  `}),en=e=>({auto:S.iv`
    display: inline-flex;
    min-width: ${ie[e.size].height};
  `,full:S.iv`
    display: flex;
    width: 100%;
  `,maxContent:S.iv`
    display: inline-flex;
    width: max-content;
    min-width: max-content;
  `}),Cr=u(1),tn=m.Z.button`
  appearance: none;
  padding: 0
    ${e=>e.hasChildren?ie[e.size].xSpace:0};
  font: inherit;
  text-decoration: none;
  transition:
    0.6s background,
    0.6s border-color;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  white-space: nowrap;
  ${Re("bold")};
  border-radius: ${e=>ie[e.size].radius};
  // TODO: remove hasFullWidth after deprecation period
  ${e=>e.hasFullWidth?"display: flex; width: 100%":"display: inline-flex"};
  ${e=>en(e)[e.width]};
  height: ${e=>ie[e.size].height};
  ${e=>ge(ie[e.size].textSize)};
  ${e=>e.isFloating&&`box-shadow: ${$t.medium}`};
  ${e=>e.disabled?br(e).disabled:br(e).enabled};
  ${e=>!e.disabled&&`
    border: ${pe[e.variant].borderColor?`1px solid ${pe[e.variant].borderColor}`:"none"};
    background: ${e.isFloating&&e.variant==="neutral"?pe[e.variant].floatingBackground:pe[e.variant].background};
    background-position: left;
    background-size: 125%;
    color: ${pe[e.variant].color};
  `};

  &:hover {
    transition:
      0.3s background,
      0.3s border-color;
    background: ${e=>e.isFloating&&e.variant==="neutral"?pe[e.variant].floatingHover:pe[e.variant].hover};
    background-position: 75% center;
  }

  &:active {
    transition:
      0s background,
      0s border-color;
    background: ${e=>e.isFloating&&e.variant==="neutral"?pe[e.variant].floatingActive:pe[e.variant].active};
    background-position: right;
  }

  &:focus-visible {
    ${e=>e["aria-expanded"]?"outline: none;":at()};
  }

  &::-moz-focus-inner {
    border: 0;
  }
`,wr=m.Z.span`
  ${e=>b("padding-left",e.paddingLeft)};
  ${e=>b("padding-right",e.paddingRight)};
  ${It};
`,rn=m.Z.img`
  max-width: 1.45em;
  max-height: 1.45em;
  height: ${e=>ie[e.size].height};
  width: ${e=>ie[e.size].height};
  ${e=>e.hasSpacing&&"margin-right: 0.57em"};
  ${It};
`,an=m.Z.span`
  position: relative;
  display: flex;
  align-items: center;
`,ln=m.Z.span`
  ${It};
`,Oi=e=>{var t=e,{size:a="medium",children:r,variant:l="neutral",hasFullWidth:n,width:s="auto",icon:d,iconPosition:h="left",iconBefore:v,iconAfter:p,logoSrc:g,hasLoader:f,isDisabled:C,ariaDisabled:z,htmlTag:E="button",interactionName:w,onClick:$,refHandler:_}=t,O=y(t,["size","children","variant","hasFullWidth","width","icon","iconPosition","iconBefore","iconAfter","logoSrc","hasLoader","isDisabled","ariaDisabled","htmlTag","interactionName","onClick","refHandler"]);const L=d&&h==="left"?d:null,j=v||L?React7.createElement(wr,{hasLoader:f,paddingLeft:"0",paddingRight:r?Cr:"0"},React7.createElement(Q,{icon:v||L,color:"currentColor",size:ie[a].iconSize})):null,Y=d&&h==="right"?d:null,V=p||Y?React7.createElement(wr,{hasLoader:f,paddingLeft:r?Cr:"0",paddingRight:"unset"},React7.createElement(Q,{icon:Y||p,color:"currentColor",size:ie[a].iconSize})):null,W=useCallback(A=>{w&&traceUFOPress(w),$?.(A)},[$,w]);return React7.createElement(tn,x(o({size:a,variant:l,hasFullWidth:n,width:s,icon:d,iconPosition:h,logoSrc:g,disabled:C,ariaDisabled:z,as:E,hasChildren:r,ref:A=>_&&_(A)},O),{onClick:w===void 0?$:W}),f&&React7.createElement(an,null,React7.createElement(St,{color:"currentColor"})),j,g&&React7.createElement(rn,{alt:"",hasSpacing:Boolean(r),src:g,size:a,height:ie[a].height,width:ie[a].height,hasLoader:f}),React7.createElement(ln,{hasLoader:f},r),V)},Ai=Object.keys(ie),Pi=Object.keys(pe),Fi=null,nn=m.Z.div`
  display: ${e=>e.isInline?"inline-block":"block"};
  vertical-align: middle;
  ${e=>b("padding",e.all)};
  ${e=>b("padding-top",e.top)};
  ${e=>b("padding-right",e.right)};
  ${e=>b("padding-bottom",e.bottom)};
  ${e=>b("padding-left",e.left)};
`,on=e=>{var t=e,{children:a,all:r,y:l,x:n,top:s,right:d,bottom:h,left:v,isInline:p}=t,g=y(t,["children","all","y","x","top","right","bottom","left","isInline"]);return i.createElement(nn,o({all:r,top:l||s,bottom:l||h,right:n||d,left:n||v,isInline:p},g),a)},ct=on,dt={topLeft:"start",topCenter:"start center",topRight:"start end",centerLeft:"center start",center:"center",centerRight:"center end",bottomLeft:"end start",bottomCenter:"end center",bottomRight:"end"},sn=e=>{if(Array.isArray(e))return e.map(t=>dt[t]);if(typeof e=="object"){const t={};return Object.entries(e).forEach(([a,r])=>t[a]=dt[r]),t}return dt[e]},cn=m.Z.div`
  width: 100%;
  height: 100%;
  display: grid;
  ${e=>le("place-items",sn(e.alignment))};
`,dn=e=>{var t=e,{children:a,alignment:r="center",htmlTag:l="div"}=t,n=y(t,["children","alignment","htmlTag"]);return i.createElement(cn,o({alignment:r,as:l},n),a)},Ti=Object.keys(dt),_e=dn,un=(e,t,a)=>{const r=t||"border",n=`${ce(a)} solid ${c(r)}`;if(e)return e==="all"?`border: ${n};`:`border-${e}: ${n};`},hn=m.Z.div`
  ${e=>e.position&&`position: ${e.position}`};
  ${e=>e.overflow&&`overflow: ${e.overflow}`};
  ${e=>e.backgroundColor&&`background-color: ${c(e.backgroundColor)}`};
  ${e=>e.backgroundImage&&`background-image: ${e.backgroundImage}`}
  ${e=>e.contentColor&&`color: ${c(e.contentColor)}`};
  ${e=>un(e.borderSide,e.borderColor,e.borderWidth)};
  ${e=>F(e.radius)};
  ${e=>Ge(e.shadow)};
  ${e=>b("width",e.width)};
  ${e=>b("height",e.height)};
  ${e=>b("min-width",e.minWidth)};
  ${e=>b("min-height",e.minHeight)};
  ${e=>b("max-width",e.maxWidth)};
  ${e=>b("max-height",e.maxHeight)};
  ${e=>b("padding",e.padding)};
  ${e=>b("padding-top",e.paddingTop)};
  ${e=>b("padding-right",e.paddingRight)};
  ${e=>b("padding-bottom",e.paddingBottom)};
  ${e=>b("padding-left",e.paddingLeft)};
  ${e=>b("margin",e.margin)};
  ${e=>b("margin-top",e.marginTop)};
  ${e=>b("margin-right",e.marginRight)};
  ${e=>b("margin-bottom",e.marginBottom)};
  ${e=>b("margin-left",e.marginLeft)};
  ${e=>b("top",e.top)};
  ${e=>b("right",e.right)};
  ${e=>b("bottom",e.bottom)};
  ${e=>b("left",e.left)};
  ${e=>e.zIndex&&`z-index: ${e.zIndex}`};
`,mn=e=>{var t=e,{children:a,backgroundColor:r,backgroundImage:l,contentColor:n,borderColor:s,radius:d,borderSide:h,borderWidth:v="1px",shadow:p,padding:g,paddingX:f,paddingY:C,paddingLeft:z,paddingRight:E,paddingTop:w,paddingBottom:$,margin:_,marginX:O,marginY:L,marginLeft:j,marginRight:Y,marginTop:V,marginBottom:W,width:A,height:q,minWidth:N,minHeight:T,maxWidth:I,maxHeight:ee,htmlTag:U="div",position:se,overflow:be,zIndex:R,top:J,bottom:Te,left:Ce,right:xe,refHandler:he}=t,k=y(t,["children","backgroundColor","backgroundImage","contentColor","borderColor","radius","borderSide","borderWidth","shadow","padding","paddingX","paddingY","paddingLeft","paddingRight","paddingTop","paddingBottom","margin","marginX","marginY","marginLeft","marginRight","marginTop","marginBottom","width","height","minWidth","minHeight","maxWidth","maxHeight","htmlTag","position","overflow","zIndex","top","bottom","left","right","refHandler"]);return i.createElement(hn,o({backgroundColor:r,backgroundImage:l,contentColor:n,borderColor:s,radius:d,borderSide:h,shadow:p,padding:g,paddingLeft:f||z,paddingRight:f||E,paddingTop:C||w,paddingBottom:C||$,margin:_,marginLeft:O||j,marginRight:O||Y,marginTop:L||V,marginBottom:L||W,width:A,height:q,minWidth:N,minHeight:T,maxWidth:I,maxHeight:ee,as:U,position:se,top:J,bottom:Te,left:Ce,right:xe,overflow:be,zIndex:R,borderWidth:v,ref:H=>he&&he(H)},k),a)},re=mn,ne={small:{height:u(4),width:u(5),iconSize:2,padding:u(1.75),withIconPadding:u(4.5),passwordAdditionalPadding:u(.5),textSize:"small",radius:"var(--lns-radius-150)"},medium:{height:"var(--lns-formFieldHeight)",width:u(6),iconSize:3,padding:"var(--lns-formFieldHorizontalPadding)",withIconPadding:u(5.5),passwordAdditionalPadding:u(.5),textSize:"medium",radius:"var(--lns-radius-175)"},large:{height:u(7),width:u(6),iconSize:3,padding:"var(--lns-formFieldHorizontalPadding)",withIconPadding:u(5.5),passwordAdditionalPadding:u(.5),textSize:"large",radius:"var(--lns-radius-250)"}},vn=e=>{let t=e.addOn?ne[e.inputSize].withIconPadding:ne[e.inputSize].padding;return e.type==="password"&&(t=`calc(${ne[e.inputSize].passwordAdditionalPadding} + ${t})`),t},gn=m.Z.input`
  -webkit-appearance: none;
  font-family: inherit;
  width: 100%;
  height: ${e=>ne[e.inputSize].height};
  border: none;
  color: inherit;
  background-color: ${c("formFieldBackground")};
  transition: 0.3s box-shadow;
  padding-top: 0;
  padding-bottom: 0;
  padding-left: ${e=>e.icon?ne[e.inputSize].withIconPadding:ne[e.inputSize].padding};
  padding-right: ${e=>vn(e)};
  border-radius: ${e=>ne[e.inputSize].radius};
  box-shadow: inset 0 0 0
    ${e=>e.hasError?"var(--lns-formFieldBorderWidthFocus) var(--lns-color-danger)":"var(--lns-formFieldBorderWidth) var(--lns-color-formFieldBorder)"};

  ${e=>ge(ne[e.inputSize].textSize)};

  &:hover {
    box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidthFocus)
      var(--lns-color-blurple);
  }

  &:focus {
    outline: 1px solid transparent;
    box-shadow: var(--lns-formFieldBorderShadowFocus);
  }

  &:disabled {
    color: ${c("disabledContent")};
    background-color: ${c("disabledBackground")};
  }

  &:disabled:hover {
    box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidth)
      var(--lns-color-formFieldBorder);
  }

  &::placeholder {
    color: ${c("bodyDimmed")};
  }
`,pn=m.Z.div`
  position: relative;
  width: 100%;
`,fn=m.Z.div`
  position: absolute;
  pointer-events: none;
  width: ${e=>ne[e.size].width};
  // Width isn't equal to iconPadding because we want more space on the left than the right
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
`,bn=m.Z.img`
  height: 100%;
  width: auto;
  min-width: 100%;
  min-height: 100%;
  object-fit: cover;
  opacity: ${({isDisabled:e})=>e?.5:1};
`,Cn=m.Z.div`
  position: absolute;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  right: 0;
  width: ${e=>ne[e.size].width};
  top: 50%;
  transform: translateY(-50%);
`,Zi=(0,i.forwardRef)((e,t)=>{var a=e,{placeholder:r,onFocus:l,onChange:n,onBlur:s,onKeyDown:d,isDisabled:h,icon:v,type:p="text",value:g,hasError:f,size:C="medium",addOn:z}=a,E=y(a,["placeholder","onFocus","onChange","onBlur","onKeyDown","isDisabled","icon","type","value","hasError","size","addOn"]);const w=i.createElement(gn,o({type:p,placeholder:r,onFocus:l,onChange:n,onBlur:s,onKeyDown:d,disabled:h,icon:v,ref:t,value:g,hasError:f,inputSize:C,addOn:z},E));return v||z?i.createElement(pn,null,v&&i.createElement(fn,{size:C},typeof v=="string"?i.createElement(re,{radius:"50",width:ne[C].iconSize,height:ne[C].iconSize,overflow:"hidden"},i.createElement(_e,{alignment:"center"},i.createElement(bn,{src:v,alt:"",isDisabled:h}))):i.createElement(Q,{icon:v,size:ne[C].iconSize,color:c(h?"disabledContent":"body")})),w,z&&i.createElement(Cn,{size:C},z)):w}),wn=null,yr={start:"flex-start",center:"center",end:"flex-end",stretch:"stretch"},Er=!1,ut=e=>Array.isArray(e)?e:[e],zr=(e,t)=>{if(e.length===t)return e;const a=e[e.length-1];return[...Array(t)].map((r,l)=>e[l]||a)},yn=(e,t)=>{const a=Math.max(ut(e).length,ut(t).length),r=zr(ut(t),a),l=zr(ut(e),a),n="& > * + *",s=r.map((h,v)=>{const p=`${ce(h)} 0 0 0`,g=`0 0 0 ${ce(h)}`,f=l[v]==="column"?p:g;return`${n}{ margin: ${f}; }`}),d=l.map(h=>`flex-direction: ${h}`);return We(s)+We(d)},En=m.Z.div`
  display: flex;
  flex-wrap: wrap;
  ${e=>yn(e.flexDirection,e.gap)};
  ${e=>er(e.flexAlign,yr)};
  ${e=>e.isSpread&&Ea("justify-content",["space-between","initial"],e.isSpread)};

  & > * {
    flex-shrink: 0;
  }
`,ji=e=>{var t=e,{children:a,gap:r,direction:l="row",alignment:n="start",isSpread:s,htmlTag:d="div"}=t,h=y(t,["children","gap","direction","alignment","isSpread","htmlTag"]);return Er||(console.warn(Ra),Er=!0),React12.createElement(En,o({gap:r,flexDirection:l,flexAlign:n,isSpread:s,as:d},h),a)},Ni=Object.keys(yr),Ui=null,zn=m.Z.div`
  display: grid;
  ${e=>le("align-items",e.alignItems)};
  ${e=>le("justify-content",e.justifyContent)};
  ${e=>e.justifyItems&&le("justify-items",e.justifyItems)};
  ${e=>e.alignContent&&le("align-content",e.alignContent)};
  ${e=>!e.columns&&!e.rows&&!e.autoFlow&&"grid-auto-flow: column"};
  ${e=>rr(e.columns,"columns")};
  ${e=>rr(e.rows,"rows")};
  ${e=>b("gap",e.gap)};
  ${e=>b("width",e.width)};
  ${e=>b("height",e.height)};
  ${e=>b("min-width",e.minWidth)};
  ${e=>b("min-height",e.minHeight)};
  ${e=>b("max-width",e.maxWidth)};
  ${e=>b("max-height",e.maxHeight)};

  ${e=>e.autoFlow&&le("grid-auto-flow",e.autoFlow)};
  ${e=>e.columns&&e.autoFlow&&le("grid-auto-flow",e.autoFlow)};
  ${e=>ar(e.as)};
`,xn=e=>{var t=e,{children:a,width:r,height:l,minWidth:n,minHeight:s,maxWidth:d,maxHeight:h,gap:v,columns:p,rows:g,alignItems:f="center",justifyContent:C="start",justifyItems:z,alignContent:E,autoFlow:w,htmlTag:$="div",className:_,style:O}=t,L=y(t,["children","width","height","minWidth","minHeight","maxWidth","maxHeight","gap","columns","rows","alignItems","justifyContent","justifyItems","alignContent","autoFlow","htmlTag","className","style"]);return(_||O)&&console.warn(Rt),i.createElement(zn,o({alignItems:f,as:$,justifyContent:C,justifyItems:z,alignContent:E,gap:v,columns:p,rows:g,width:r,height:l,minWidth:n,minHeight:s,maxWidth:d,maxHeight:h,autoFlow:w},L),a)},Oe=xn;function xr(){return i.createElement(ve.Z,{label:"",testId:"ads-refreshed-icon"})}var $n=m.Z.div`
  position: relative;
  ::before {
    content: '';
    width: calc(100% + var(--lns-space-medium));
    height: calc(100% + var(--lns-space-medium));
    position: absolute;
    top: calc(-1 * var(--lns-space-small));
    left: calc(-1 * var(--lns-space-small));
    outline: 1px solid var(--lns-color-danger);
    border-radius: var(--lns-radius-large);
    pointer-events: none;
  }
`,Ki=({children:e,errorActive:t,errorMessage:a="Oops, that didn't work. Try again."})=>t?React15.createElement($n,null,React15.createElement(Oe,{autoFlow:"row",gap:"small"},e,a?React15.createElement(Oe,{gap:"xsmall"},React15.createElement(Q,{icon:React15.createElement(xr,null),size:2,color:"danger"}),React15.createElement(Ee,{size:"body-sm",color:"danger"},a)):null)):React15.createElement(React15.Fragment,null,e),Gi=null,Rn={start:"flex-start",center:"center",end:"flex-end"},kn=m.Z.div`
  display: flex;
  ${e=>er(e.alignment,Rn)};

  & > * + * {
    ${e=>e.gap&&b("margin-left",e.gap)};
  }
`,Mn=m.Z.div`
  min-width: 0px;
  flex-shrink: 0;
  ${e=>b("width",e.width)};
  ${e=>b("max-width",e.maxWidth)};
  ${e=>e.width?"flex-shrink: 0":"flex: 1 1 0%"};
`,Ln=e=>{var t=e,{width:a,maxWidth:r,children:l}=t,n=y(t,["width","maxWidth","children"]);return console.warn(ir),i.createElement(Mn,o({width:a,maxWidth:r},n),l)},Hn=class extends i.Component{render(){return console.warn(ir),i.createElement(kn,o({},this.props),this.props.children)}};Hn.Section=Ln;var Yi=null,Xe={small:{size:u(3),iconSize:2.25,radius:"var(--lns-radius-100)"},medium:{size:u(4),iconSize:3,radius:"var(--lns-radius-150)"},large:{size:u(5),iconSize:4,radius:"var(--lns-radius-175)"}},_n=m.Z.button`
  background-color: ${e=>c(e.isActive?"backgroundActive":e.backgroundColor)||"transparent"};
  border: none;
  appearance: none;
  cursor: pointer;
  padding: 0;
  width: ${e=>Xe[e.size].size};
  height: ${e=>Xe[e.size].size};
  position: relative;
  outline: 1px solid transparent;
  transition: 0.6s background-color;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  vertical-align: middle;
  border-radius: ${e=>Xe[e.size].radius};
  font: inherit;

  &:hover {
    transition: 0.3s background-color;
    background-color: ${e=>c(e.isActive?"backgroundActive":"backgroundHover")};
  }

  &:active {
    transition: 0s background-color;
    background-color: ${c("backgroundActive")};
  }

  &:disabled {
    color: ${c("disabledContent")};
    pointer-events: none;
  }

  &:before {
    content: '';
    width: 100%;
    height: 100%;
    display: block;
    position: absolute;
    top: 0;
    border-radius: ${e=>Xe[e.size].radius};
  }

  &:focus-visible:before,
  &:focus:before {
    ${de()};
  }

  &:focus::-moz-focus-inner {
    border: 0;
  }
`,$r=i.forwardRef((e,t)=>{var a=e,{altText:r,icon:l,onClick:n,iconColor:s="body",backgroundColor:d,isActive:h,isDisabled:v,size:p="medium"}=a,g=y(a,["altText","icon","onClick","iconColor","backgroundColor","isActive","isDisabled","size"]);return i.createElement(_n,o({"aria-label":r,onClick:n,isActive:h,disabled:v,size:p,backgroundColor:d,ref:t},g),i.createElement(Q,{icon:l,size:Xe[p].iconSize,color:v?"disabledContent":s}))});$r.displayName="IconButton";var Bt=$r,Sn=e=>i.createElement("svg",o({width:12,height:9,viewBox:"0 0 12 9",fill:"none"},e),i.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M11.707.293a1 1 0 010 1.414l-7 7a1 1 0 01-1.414 0l-3-3a1 1 0 011.414-1.414L4 6.586 10.293.293a1 1 0 011.414 0z",fill:"currentColor"})),In=e=>i.createElement("svg",o({width:12,height:2,viewBox:"0 0 12 2",fill:"none"},e),i.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 1a1 1 0 011-1h10a1 1 0 110 2H1a1 1 0 01-1-1z",fill:"currentColor"})),Bn=m.Z.div`
  display: block;
  position: relative;
`,Vn=m.Z.input`
  height: 100%;
  margin: 0;
  opacity: 0;
  position: absolute;
  width: 100%;

  &:not(:disabled) {
    cursor: pointer;

    & ~ .CheckboxBox {
      border: 2px solid ${c("body")};
    }

    &:checked ~ .CheckboxBox,
    &:indeterminate ~ .CheckboxBox {
      background-color: ${c("body")};
    }
  }

  &:disabled,
  &:disabled ~ .CheckboxBox {
    pointer-events: none;
  }

  &:disabled ~ .CheckboxBox {
    background-color: ${c("disabledBackground")};

    .Icon {
      color: ${c("disabledContent")};
    }
  }

  &:focus-visible ~ .CheckboxBox {
    ${de()};
  }

  & ~ .CheckboxBox .Icon {
    display: none;
    color: ${c("background")};
  }

  &:checked ~ .CheckboxBox .IconCheck {
    display: block;
  }

  &:indeterminate ~ .CheckboxBox .IconMinus {
    display: block;
  }
`,Wn=m.Z.span`
  cursor: pointer;
  width: ${u(2.25)};
  height: ${u(2.25)};
  border-radius: ${u(.5)};
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
`,Dn=(0,i.forwardRef)((e,t)=>{var a=e,{isDisabled:r,isChecked:l,isIndeterminate:n,onFocus:s,onChange:d,onBlur:h}=a,v=y(a,["isDisabled","isChecked","isIndeterminate","onFocus","onChange","onBlur"]);const p=(0,i.useRef)(),g=t||p,f=c(r?"disabledContent":"currentColor");return(0,i.useEffect)(()=>{g.current.indeterminate=n}),i.createElement(Bn,null,i.createElement(Vn,o({type:"checkbox",disabled:r,checked:l,onFocus:s,onChange:d,onBlur:h,ref:g,"aria-checked":l},v)),i.createElement(Wn,{className:"CheckboxBox"},i.createElement(In,{className:"Icon IconMinus",color:f}),i.createElement(Sn,{className:"Icon IconCheck",color:f})))}),On=Dn,Ae={small:{textSize:"small",iconSize:2.25,height:u(3),xSpace:u(1),radius:"var(--lns-radius-100)"},medium:{textSize:"medium",iconSize:3,height:u(4),xSpace:u(1.5),radius:"var(--lns-radius-150)"},large:{textSize:"large",iconSize:4,height:u(6),xSpace:u(3),radius:"var(--lns-radius-200)"}},An=m.Z.button`
  background-color: ${e=>e.isActive?c("backgroundActive"):"transparent"};
  display: inline-flex;
  vertical-align: middle;
  align-items: center;
  font: inherit;
  text-decoration: none;
  border: none;
  appearance: none;
  height: ${e=>Ae[e.size].height};
  cursor: pointer;
  transition: 0.6s background-color;
  color: ${e=>c(e.color||"body")};
  ${Re("bold")};
  border-radius: ${e=>Ae[e.size].radius};
  ${e=>ge(Ae[e.size].textSize)};
  padding: 0 ${e=>Ae[e.size].xSpace};
  ${e=>e.offsetSide&&`margin-${e.offsetSide}: calc(-1 * ${Ae[e.size].xSpace})`};

  &:focus,
  &:focus-visible {
    outline: 1px solid transparent;
  }

  &:focus-visible {
    ${de()};
  }

  &::-moz-focus-inner {
    border: 0;
  }

  &:hover {
    transition: 0.3s background-color;
    background-color: ${e=>c(e.isActive?"backgroundActive":"backgroundHover")};
  }

  &:active {
    transition: 0s background-color;
    background-color: ${c("backgroundActive")};
  }

  &:disabled {
    color: ${c("disabledContent")};
    pointer-events: none;
  }
`,Pn=i.forwardRef((e,t)=>{var a=e,{onClick:r,size:l="medium",children:n,icon:s,iconPosition:d="left",isActive:h,isDisabled:v,htmlTag:p,offsetSide:g}=a,f=y(a,["onClick","size","children","icon","iconPosition","isActive","isDisabled","htmlTag","offsetSide"]);const C=i.createElement(re,{paddingLeft:d==="right"&&"small",paddingRight:d==="left"&&"small",htmlTag:"span"},i.createElement(Q,{icon:s,size:Ae[l].iconSize,color:v?"disabledColor":void 0}));return i.createElement(An,o({onClick:r,size:l,icon:s,iconPosition:d,disabled:v,isActive:h,as:p,offsetSide:g,ref:t},f),s&&d==="left"&&C,n,s&&d==="right"&&C)});Pn.displayName="TextButton";var Xi=null,Vt=e=>{var t,a;const r=(a=(t=e?.())==null?void 0:t.getRootNode)==null?void 0:a.call(t);if(String(r)==="[object ShadowRoot]"){r.createElement=(...n)=>r.ownerDocument.createElement(...n);const l=r.createElement("div");return l.id="a11y-status-message",l.style.display="none",r.appendChild(l),{document:r,addEventListener:r.addEventListener.bind(r),removeEventListener:r.removeEventListener.bind(r)}}return typeof window>"u"?null:window},He=e=>typeof e=="string"?e:typeof e=="number"||typeof e=="boolean"||typeof e=="bigint"?e.toString():e==null?"":Fn(e)?Array.from(e).map(He).join(""):typeof e=="object"&&"props"in e&&e.props&&e.props.children!==void 0?He(e.props.children):"",Fn=e=>typeof e[Symbol.iterator]=="function";function Rr(){return i.createElement("span",{"aria-hidden":!0,"data-testid":"ads-refreshed-icon"},i.createElement("svg",{viewBox:"-2 -2 16 16"},i.createElement("path",{fill:"currentColor",fillRule:"evenodd",d:"M2.03 3.97 6 7.94l3.97-3.97 1.06 1.06-4.5 4.5a.75.75 0 0 1-1.06 0l-4.5-4.5z",clipRule:"evenodd"})))}function Tn(){return i.createElement(Kt.Z,{label:"",testId:"ads-refreshed-icon"})}var Wt={left:"bottom-start",right:"bottom-end",topLeft:"top-start",topRight:"top-end",leftSide:"left-start",rightSide:"right-start"},Zn=m.Z.div`
  background-color: ${c("overlay")};
  display: flex;
  flex-direction: column;
  margin: 0;
  ${e=>b("min-width",e.minWidth)};
  ${e=>b("max-width",e.maxWidth)};
  ${e=>b("max-height",e.maxHeight)};
  z-index: ${e=>e.zIndex};
  border: 1px solid ${c("border")};
  ${Ge("medium")};
  ${F("250")};
`,jn=m.Z.ul`
  padding: ${e=>e.search?`0 ${u(1.5)} ${u(1.5)} ${u(1.5)}`:u(1.5)};
  list-style: none;
  overflow: auto;
  margin: 0;
`,Nn=m.Z.li`
  display: ${({hidden:e})=>e?"none":"grid"};
  grid-auto-flow: column;
  grid-template-columns: ${e=>e.columns};
  ${b("grid-gap","small")};
  ${F("175")};
  align-items: center;
  min-height: ${u(5)};
  padding: 0 ${u(2)};
  cursor: ${e=>e.isDisabled?"default":"pointer"};
  &:focus-visible {
    outline: 1px solid transparent;
    ${at()};
  }
  ${e=>e.isHighlighted&&!e.isDisabled&&`
    background-color: ${c("backgroundHover")};
  `};
  ${e=>e.keyboardMove&&e.isHighlighted&&!e.isDisabled&&`
    outline: 1px solid transparent;
    ${at()};
  `};
  ${e=>e.hasDivider&&`
    position: relative;
    margin-top: ${u(3)};
    &:before {
      content: '';
      border-top: 1px solid ${c("border")};
      position: absolute;
      top: ${u(-1.5)};
      left: ${u(-1.5)};
      width: calc(100% + ${u(3)});
    }
  `};
`,Un=m.Z.img`
  height: 100%;
  width: auto;
  min-width: 100%;
  min-height: 100%;
  object-fit: cover;
  opacity: ${({isDisabled:e})=>e?.5:1};
`,Dt=e=>{var t=e,{isDisabled:a,isHighlighted:r,isSelected:l,icon:n,hasDivider:s,children:d,menuItemRole:h,keyboardMove:v}=t,p=y(t,["isDisabled","isHighlighted","isSelected","icon","hasDivider","children","menuItemRole","keyboardMove"]);const C=`${n?"auto":""} 1fr ${l?"auto":""}`,z=a?"disabledContent":void 0,E=h?x(o({},p),{role:h}):p;return i.createElement(Nn,o({isHighlighted:r,isDisabled:a,keyboardMove:v,columns:C,hasDivider:s,tabIndex:a?-1:0,"data-highlighted":r||void 0},E),n&&(typeof n=="string"?i.createElement(re,{radius:"50",width:3,height:3,overflow:"hidden"},i.createElement(_e,{alignment:"center"},i.createElement(Un,{src:n,alt:"",isDisabled:a}))):i.createElement(Q,{icon:n,color:z})),i.createElement(Ee,{color:z,hasEllipsis:!0},d),l&&i.createElement(Q,{icon:i.createElement(Tn,null),color:z}))},Kn=e=>{var t=e,{position:a,zIndex:r,minWidth:l,maxWidth:n,maxHeight:s,children:d,role:h,downshiftMenuProps:v=()=>null,search:p}=t,g=y(t,["position","zIndex","minWidth","maxWidth","maxHeight","children","role","downshiftMenuProps","search"]);const f=h?x(o({},v()),{role:h}):o({},v());return i.createElement(Zn,o(o({minWidth:l,maxWidth:n,maxHeight:s,zIndex:r,position:a},f),g),p&&p,i.createElement(jn,{search:p},d))},Se=Kn;function Gn(){return React24.createElement(SearchIcon,{label:"",testId:"ads-refreshed-icon"})}var Yn=m.Z.div`
  padding: ${u(1.5)} ${u(1.5)} 0;
  margin-bottom: ${u(1.5)};
  position: sticky;
  top: 0;
`,Ji=({ariaLabel:e,placeholder:t,value:a,onChange:r,getInputProps:l})=>React25.createElement(Yn,null,React25.createElement(wn,o({"aria-label":e,icon:React25.createElement(Gn,null)},l({placeholder:t,value:a,onChange:r,type:"text"})))),kr=null,Xn=m.Z.div`
  position: relative;
`,Jn=m.Z.button`
  appearance: none;
  font: inherit;
  text-align: left;
  display: grid;
  grid-auto-flow: column;
  grid-template-columns: ${e=>e.columns};
  ${b("grid-gap","small")};
  align-items: center;
  cursor: pointer;
  width: 100%;
  min-height: ${u(4.5)};
  padding: 0 ${u(1.5)} 0 var(--lns-formFieldHorizontalPadding);
  color: ${c("body")};
  border: none;
  background-color: ${c("formFieldBackground")};
  transition: 0.3s box-shadow;
  border-radius: var(--lns-formFieldRadius);
  box-shadow: inset 0 0 0
    ${e=>e.hasError?"var(--lns-formFieldBorderWidthFocus) var(--lns-color-danger)":"var(--lns-formFieldBorderWidth) var(--lns-color-formFieldBorder)"};

  &:hover:not(:disabled) {
    box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidthFocus)
      ${e=>e.hasError?"var(--lns-color-danger)":"var(--lns-color-blurple)"};
  }

  &:focus {
    outline: 1px solid transparent;
    box-shadow: var(--lns-formFieldBorderShadowFocus);
  }

  &:focus:hover {
    outline: 1px solid transparent;
    box-shadow: var(--lns-formFieldBorderShadowFocus);
  }

  &:disabled {
    color: ${c("disabledContent")};
    background-color: ${c("disabledBackground")};
    cursor: default;
  }
`,Qn=m.Z.img`
  height: 100%;
  width: auto;
  min-width: 100%;
  min-height: 100%;
  object-fit: cover;
  opacity: ${({isDisabled:e})=>e?.5:1};
`,qn=m.Z.ul`
  list-style: none;
  margin: 0;
  padding: 0;
`,e1=m.Z.span`
  color: var(--lns-color-red);
  margin-top: var(--lns-space-xsmall);
  display: block;
  width: 100%;
  grid-column-start: 1;
  grid-column-end: 3;
`,ht=e=>Array.isArray(e)&&e.length>0&&"group"in e[0],Ot=({options:e,selectedOptionValue:t})=>{if(!e||!t)return{icon:null,title:null};if(ht(e))for(const a of e){const r=a.items.find(l=>l.value===t);if(r)return r}else return e.find(r=>r.value===t)||{icon:null,title:null};return{icon:null,title:null}},Mr=({options:e,selectedItem:t,selectedOptionValue:a})=>{if(t)return t.icon;if(a)return Ot({options:e,selectedOptionValue:a}).icon},t1=({options:e,selectedItem:t,selectedOptionValue:a,selectPlaceholder:r})=>t?t.title:a?Ot({options:e,selectedOptionValue:a}).title:r,Lr=({selectedItem:e,getInputProps:t,getToggleButtonProps:a,ariaMenuName:r,isOpen:l})=>{const n=e?`selected value is ${e.title}`:"no value selected",s=a?.()["aria-label"];return{"aria-expanded":l,"aria-activedescendant":t()["aria-activedescendant"],"aria-label":[r,s,n].filter(Boolean).join(", ")}},r1=({getToggleButtonProps:e,inputValue:t,selectedItem:a,selectedOptionValue:r,selectPlaceholder:l,isDisabled:n,options:s,getInputProps:d,ariaMenuName:h,hasError:v,isOpen:p})=>{const g=Mr({options:s,selectedItem:a,selectedOptionValue:r}),f=Boolean(g),C=!r&&!a,E=`${f?"auto":""} 1fr auto`,w=n?"disabledContent":void 0;return React26.createElement(Jn,x(o(o({},e()),Lr({selectedItem:a,getInputProps:d,getToggleButtonProps:e,ariaMenuName:h,isOpen:p})),{hasValue:t||r,disabled:n,columns:E,hasError:v}),f&&(typeof g=="string"?React26.createElement(re,{radius:"50",width:3,height:3,overflow:"hidden"},React26.createElement(_e,{alignment:"center"},React26.createElement(Qn,{src:g,alt:"",isDisabled:n}))):React26.createElement(Q,{icon:Mr({options:s,selectedItem:a,selectedOptionValue:r}),color:w})),React26.createElement(Ee,{hasEllipsis:!0,color:C?"bodyDimmed":"inherit"},t1({options:s,selectedItem:a,selectedOptionValue:r,selectPlaceholder:l})),React26.createElement(Q,{icon:React26.createElement(Rr,null),color:w}))},a1=({selectedOptionValue:e,selectedItem:t,trigger:a,getToggleButtonProps:r,options:l,selectPlaceholder:n,isDisabled:s,getInputProps:d,ariaMenuName:h,hasError:v,errorMessage:p,isOpen:g})=>{const f=()=>o(o({},r()),Lr({selectedItem:t,getInputProps:d,getToggleButtonProps:r,ariaMenuName:h,isOpen:g})),z=x(o({},(()=>{if(t)return t;if(e)return Ot({options:l,selectedOptionValue:e})})()),{placeholder:n,isDisabled:s,hasError:v,errorMessage:p});return a(z,f())},Hr=(e,t)=>{if(ht(t))for(const a of t){const r=a.items.find(l=>l.value===e);if(r)return r}else return t.find(a=>a.value===e)},_r=(e,t,a,r,l,n,s,d)=>{const h=!a&&e.value===r||a&&a.value===e.value;return React26.createElement(Dt,x(o({key:t,getItemProps:n,icon:e.icon,hidden:e.hidden},n({key:`${e.value}-${t}`,index:t,item:e,disabled:e.isDisabled,"aria-selected":h,onMouseMove:()=>{s&&d(!1)}})),{isDisabled:e.isDisabled,hasDivider:e.hasDivider,isHighlighted:l===t,keyboardMove:s&&l===t,isSelected:h}),e.title)},l1=e=>{var t=e,{options:a,selectedItem:r,selectedOptionValue:l,highlightedIndex:n,getItemProps:s,search:d,keyboardMove:h,setKeyboardMove:v}=t,p=y(t,["options","selectedItem","selectedOptionValue","highlightedIndex","getItemProps","search","keyboardMove","setKeyboardMove"]);if(!ht(a))return React26.createElement(Se,o({search:d},p),a.map((f,C)=>_r(f,C,r,l,n,s,h,v)));let g=0;return React26.createElement(Se,o({search:d},p),a.map(f=>{const C=`group-${f.group.replace(/\s+/g,"-")}`;return React26.createElement("li",{key:C},React26.createElement(ct,{left:"medium",top:"small",bottom:"xsmall"},React26.createElement(Ee,{id:C,size:"body-sm",fontWeight:"bold"},f.group)),React26.createElement(qn,{role:"group","aria-labelledby":C},f.items.map(z=>_r(z,g++,r,l,n,s,h,v))))}))},Qi=e=>{var t=e,{container:a,onChange:r,menuZIndex:l=1100,menuMaxWidth:n,menuMaxHeight:s=34,menuMinWidth:d,triggerOffset:h=0,ariaMenuName:v,selectedOptionValue:p,onOuterClick:g,options:f,placeholder:C,menuPosition:z="left",isDisabled:E,onOpenChange:w,trigger:$,hasError:_,errorMessage:O="Oops, that didn't work.",search:L}=t,j=y(t,["container","onChange","menuZIndex","menuMaxWidth","menuMaxHeight","menuMinWidth","triggerOffset","ariaMenuName","selectedOptionValue","onOuterClick","options","placeholder","menuPosition","isDisabled","onOpenChange","trigger","hasError","errorMessage","search"]);const Y=Vt(a),[V,W]=useState(!1),[A,q]=useState(!1),[N,T]=useState(""),I=k=>{const H=k.target.value;T(H)},[ee,U]=useState(Hr(p,f)),be={itemToString:k=>k?k.value:"",onChange:k=>{U(k),r&&r(k||"")},onOuterClick:g,environment:Y,selectedItem:ee,isOpen:V};Y&&(be.environment=Y);const{layerProps:R,triggerProps:J,renderLayer:Te,triggerBounds:Ce}=useLayer({isOpen:V,container:a,ResizeObserver,placement:Wt[z],auto:!0,snap:!0,triggerOffset:h});useEffect2(()=>{const k=Hr(p,f);k?.value!==ee?.value&&U(k)},[p,f,ee]),useEffect2(()=>{w&&w(V)},[V,w]);const xe=(k,H)=>{if(H.isOpen!==void 0){if(H.type===Downshift.stateChangeTypes.keyDownEscape)return W(!1),{isOpen:!1};W(H.isOpen)}return H},he=k=>{switch(k.key){case"ArrowDown":case"ArrowUp":case"ArrowLeft":case"ArrowRight":case"Enter":case" ":case"Tab":case"Escape":q(!0);break;default:break}};return f=useMemo(()=>{if(L){if(ht(f)){let k;return L.searchType==="startsWith"?k=f.map(H=>x(o({},H),{items:H.items.filter(we=>He(we.title).toLowerCase().startsWith(N.toLowerCase()))})):k=f.map(H=>x(o({},H),{items:H.items.filter(we=>He(we.title).toLowerCase().includes(N.toLowerCase()))})),k.reduce((H,we)=>(we.items.length>0&&H.push(we),H),[])}return L.searchType==="startsWith"?f.filter(k=>He(k.title).toLowerCase().startsWith(N.toLowerCase())):f.filter(k=>He(k.title).toLowerCase().includes(N.toLowerCase()))}return f},[f,N,L]),React26.createElement(Xn,o({},j),React26.createElement(Downshift,x(o({},be),{stateReducer:xe}),({getItemProps:k,getInputProps:H,getMenuProps:we,getToggleButtonProps:pt,isOpen:D,inputValue:me,highlightedIndex:Nt,selectedItem:Ze})=>React26.createElement("div",{role:"presentation"},React26.createElement("div",o({},J),$?React26.createElement(a1,{getToggleButtonProps:()=>o({},pt({onKeyDown:he})),selectedItem:Ze,selectedOptionValue:p,selectPlaceholder:C,isDisabled:E,options:f,trigger:$,getInputProps:H,ariaMenuName:v,hasError:_,errorMessage:O,isOpen:D}):React26.createElement(r1,{getToggleButtonProps:()=>o({},pt({onKeyDown:he})),selectedItem:Ze,selectedOptionValue:p,selectPlaceholder:C,options:f,inputValue:me,isDisabled:E,getInputProps:H,ariaMenuName:v,hasError:_,isOpen:D})),V&&D&&Te(React26.createElement("div",x(o({},R),{style:x(o({},R.style),{zIndex:l,width:d?"auto":Ce?.width})}),React26.createElement(l1,{options:f,selectedItem:Ze,selectedOptionValue:p,highlightedIndex:Nt,getItemProps:k,position:z,downshiftMenuProps:()=>we({onKeyDown:he}),maxWidth:n,maxHeight:s,minWidth:d,search:L&&React26.createElement(kr,{ariaLabel:L.searchPlaceholder,placeholder:L.searchPlaceholder,value:N,onChange:I,getInputProps:H}),keyboardMove:A,setKeyboardMove:q}))),_&&!V&&React26.createElement(e1,null,O))))},qi=null;function n1(e,t){const a=document;(0,i.useLayoutEffect)(()=>{const r=a?.documentElement,l=a?.body;if(!(a==null||!r||!l)){if(t){const n=window.innerWidth-r.clientWidth,s=parseInt(window.getComputedStyle(l).getPropertyValue("padding-right"),10)||0;switch(e){case"html":{r.style.position="relative",r.style.overflow="hidden",l.style.paddingRight=`${s+n}px`;break}case"body":{l.style.setProperty("position","relative"),l.style.setProperty("overflow","hidden"),l.style.setProperty("padding-right",`${s+n}px`);break}default:return}}return()=>{switch(e){case"html":{r.style.position="",r.style.overflow="",l.style.paddingRight="";break}case"body":{l.style.removeProperty("position"),l.style.removeProperty("overflow"),l.style.removeProperty("padding-right");break}default:return}}}},[a,t,e])}var Sr=n1,Ir=300,o1=m.Z.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: calc(100vh - calc(100vh - 100%));
  height: 100dvh;
  height: -webkit-fill-available;
  background: ${e=>c(e.backgroundColor)};
  z-index: ${e=>e.zIndex};
  overflow: hidden;
`,i1=m.Z.div`
  overflow: auto;
  height: 100%;
`,Br=i.forwardRef((e,t)=>{var a=e,{children:r,isOpen:l,zIndex:n=1e3,backgroundColor:s="backdropDark"}=a,d=y(a,["children","isOpen","zIndex","backgroundColor"]);const{stage:h,shouldMount:v}=(0,wt.Yz)(l,Ir);return Sr("html",l),i.createElement(i.Fragment,null,v&&i.createElement(o1,o({ref:t,backgroundColor:s,zIndex:n,style:{transition:`opacity ${Ir}ms`,opacity:h==="enter"?1:0}},d),i.createElement(i1,null,r)))});Br.displayName="Backdrop";var s1=Br;function At(){return i.createElement(zt.Z,{label:"",testId:"ads-refreshed-icon"})}var c1="70vh",d1=m.Z.div`
  display: grid;
  grid-template-rows: ${e=>e.rows};
  position: relative;
`,u1=m.Z.dialog`
  top: ${e=>xt(ce(e.maxHeight),e.placement).top};
  background-color: ${c("overlay")};
  color: ${c("body")};
  bottom: ${e=>xt(e.maxHeight,e.placement).bottom};
  ${Ge("large")};
  ${F("xlarge")};
  // Unsets bottom-radius for bottom-aligned modals
  border-bottom-left-radius: ${e=>e.placement==="bottom"?"initial":void 0};
  border-bottom-right-radius: ${e=>e.placement==="bottom"?"initial":void 0};
  ${e=>b("max-height",e.maxHeight)};
  ${e=>b("max-width",e.maxWidth)};
  margin: 0 auto;
  position: ${e=>xt(e.maxHeight,e.placement).position};
  overflow: auto;
  width: 100%;
  // TODO: LNS-150: Bake dialog resets into native resets file
  border: 0;
  padding: 0;
  &::backdrop {
    background: var(--lns-color-overlay);
  }
`,h1=m.Z.div`
  position: absolute;
  top: ${u(1.5)};
  right: ${u(1.5)};
  z-index: 1;
`,m1=m.Z.div`
  margin-left: auto;

  * {
    vertical-align: middle;
  }
`,v1=m.Z.div`
  padding-left: var(--lns-space-xlarge);
  padding-right: var(--lns-space-xlarge);
  padding-top: var(--lns-space-xlarge);
  padding-bottom: ${e=>e.bottom};
  flex-shrink: 0;
`,g1=m.Z.div`
  padding-left: var(--lns-space-xlarge);
  padding-right: var(--lns-space-xlarge);
  padding-bottom: var(--lns-space-xlarge);
  padding-top: ${e=>e.hasDividers?"var(--lns-space-medium)":e.top};
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
`,p1=m.Z.div`
  display: flex;
  flex-direction: column;
  overflow: auto;
  padding-top: ${e=>e.hasTitle&&!e.noPadding?0:!e.hasTitle&&!e.noPadding?"var(--lns-space-xlarge)":0};
  padding-bottom: ${e=>e.hasButtons&&!e.noPadding?0:!e.hasButtons&&!e.noPadding?"var(--lns-space-xlarge)":0};
  padding-left: ${e=>e.noPadding?0:"var(--lns-space-xlarge)"};
  padding-right: ${e=>e.noPadding?0:"var(--lns-space-xlarge)"};
  border-style: solid;
  border-color: ${c("border")};
  border-width: ${e=>e.hasDividers?"1px 0":"0"};
`,f1=m.Z.div`
  overflow: auto;

  ${e=>Vr(e.maxHeight)};

  & > * {
    ${e=>Vr(e.maxHeight)};
  }
`,Vr=e=>typeof e=="number"?b("max-height",e):"max-height: "+e,b1=e=>{var t=e,{children:a,onCloseClick:r,isOpen:l,maxWidth:n=60,maxHeight:s=c1,placement:d="center",ariaLabel:h,ariaModal:v,ariaLabelledBy:p,ref:g,removeClose:f,initialFocus:C}=t,z=y(t,["children","onCloseClick","isOpen","maxWidth","maxHeight","placement","ariaLabel","ariaModal","ariaLabelledBy","ref","removeClose","initialFocus"]);const E=w=>{w.key==="Escape"&&(w.preventDefault(),f||r(w))};return(0,i.useEffect)(()=>(window.addEventListener("keydown",E),()=>{window.removeEventListener("keydown",E)}),[l,r]),Sr("html",l),i.createElement(Et(),{active:l,focusTrapOptions:o({clickOutsideDeactivates:!1,allowOutsideClick:!0},C!==void 0?{initialFocus:C}:{})},i.createElement(u1,o({open:l,maxWidth:n,maxHeight:s,placement:d,onClick:w=>w.stopPropagation(),ref:g,"aria-label":h,"aria-modal":v,"aria-labelledby":p},z),!f&&r&&i.createElement(h1,null,i.createElement(Bt,{altText:"Close",icon:i.createElement(At,null),onClick:r})),i.createElement(f1,x(o({},f?{tabIndex:0}:{tabIndex:-1}),{maxHeight:s}),a)))},e0=i.forwardRef((e,t)=>{var a=e,{children:r,id:l,isOpen:n,mainButton:s,secondaryButton:d,alternativeButton:h,title:v,noPadding:p,onCloseClick:g,onBackgroundClick:f,onKeyDown:C,hasDividers:z,maxHeight:E="70vh",maxWidth:w=60,placement:$="center",zIndex:_=1e3,ariaLabel:O,ariaModal:L=!0,ariaLabelledBy:j,initialFocus:Y}=a,V=y(a,["children","id","isOpen","mainButton","secondaryButton","alternativeButton","title","noPadding","onCloseClick","onBackgroundClick","onKeyDown","hasDividers","maxHeight","maxWidth","placement","zIndex","ariaLabel","ariaModal","ariaLabelledBy","initialFocus"]),W;const A=(0,i.useRef)(null),q=l?`${l}-modal-title`:"modal-title",N=!!(s||d||h),T=I=>{if(f){I.stopPropagation(),f(I);return}g(I)};return(0,i.useEffect)(()=>{if(!n||!A.current)return;const I=A.current.parentElement;return I?(Array.from(I.children).filter(U=>U!==A.current&&U instanceof HTMLElement).forEach(U=>{U.hasAttribute("aria-hidden")||(U.setAttribute("aria-hidden","true"),U.setAttribute("data-lens-modal-hidden","true"))}),()=>{document.querySelectorAll("[data-lens-modal-hidden]").forEach(se=>{se.removeAttribute("aria-hidden"),se.removeAttribute("data-lens-modal-hidden")})}):void 0},[n]),i.createElement(s1,o({ref:A,isOpen:n,zIndex:_},V),i.createElement(re,{height:"100%",onClick:T,onKeyDown:C},i.createElement(b1,{ref:t,id:l,isOpen:n,maxHeight:E,maxWidth:w,placement:$,onCloseClick:g,ariaLabel:O,ariaModal:L,ariaLabelledBy:(W=j??q)!=null?W:void 0,initialFocus:Y},i.createElement(d1,{rows:`${v?"auto ":""} ${r?"1fr ":""} ${N?"auto":""}`},v&&i.createElement(v1,{bottom:r?"var(--lns-space-medium)":"var(--lns-space-xlarge)"},i.createElement(Ee,{htmlTag:"h1",variant:"title",id:q},v)),i.createElement(p1,{noPadding:p,hasDividers:z,hasTitle:Boolean(v),hasButtons:N},r&&r),N&&i.createElement(g1,{top:r?"var(--lns-space-xlarge)":0,hasDividers:z},h,i.createElement(m1,null,d&&i.createElement(ct,{right:"small",isInline:!0},d),s))))))}),t0=null,mt={neutral:{color:c("inherit"),focusRing:de(),underline:"inactive"},primary:{color:c("primary"),focusRing:de(),underline:"inactive"},subtle:{color:c("body"),focusRing:de(),underline:"hover"}},Wr={enabled:S.iv`
    cursor: pointer;
  `,disabled:S.iv`
    pointer-events: none;
    color: ${c("disabledContent")};
  `},C1={isButton:S.iv`
    background: none;
    border: none;
    font: inherit;
  `},w1=m.Z.a`
  ${e=>!e.disabled&&`color: ${mt[e.variant].color}`};
  ${e=>e.disabled?Wr.disabled:Wr.enabled};
  ${e=>e.as==="button"&&C1.isButton};
  ${e=>`text-decoration: ${mt[e.variant].underline==="inactive"?"underline":"none"}`};
  border-radius: 0.28em;
  box-shadow: 0 0 0 1px transparent;
  text-underline-offset: 0.35em;
  transition: 0.3s box-shadow;
  ${e=>e.noWrap&&S.iv`
      white-space: nowrap;
    `}
  &:hover {
    ${e=>`text-decoration: ${mt[e.variant].underline==="hover"?"underline":"none"}`};
  }
  &:focus,
  &:focus-visible {
    outline: 1px solid transparent;
  }
  &:focus-visible {
    ${de()};
  }
  &::-moz-focus-inner {
    border: 0;
  }
`,r0=e=>{var t=e,{children:a,href:r,variant:l="primary",htmlTag:n="a",isDisabled:s,noWrap:d}=t,h=y(t,["children","href","variant","htmlTag","isDisabled","noWrap"]);return React30.createElement(w1,o({href:r,variant:l,as:n,disabled:s,noWrap:d},h),a)},a0=Object.keys(mt),l0=null,Dr={small:{padding:`${u(1.5)} ${u(1.75)}`,textSize:"small"},medium:{padding:`${u(1.5)} var(--lns-formFieldHorizontalPadding)`,textSize:"medium"}},y1=m.Z.textarea`
  width: 100%;
  border: none;
  font-family: inherit;
  color: inherit;
  background-color: ${c("formFieldBackground")};
  transition: 0.3s box-shadow;
  padding: ${e=>Dr[e.size].padding};
  ${F("250")};
  box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidth)
    ${e=>e.error?"var(--lns-color-danger)":"var(--lns-color-formFieldBorder)"};
  ${e=>ge(Dr[e.size].textSize)};
  resize: ${e=>e.resize};

  &:hover {
    box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidthFocus)
      ${e=>e.error?"var(--lns-color-danger)":"var(--lns-color-blurple)"};
  }

  &:focus {
    outline: 1px solid
      ${e=>e.error?"var(--lns-color-orangeLight)":"transparent"};
    box-shadow: ${e=>e.error?"var(--lns-formFieldBorderShadowError)":"var(--lns-formFieldBorderShadowFocus)"};
  }

  &:disabled {
    color: ${c("disabledContent")};
    background-color: ${c("disabledBackground")};
  }

  &:disabled:hover {
    box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidth)
      var(--lns-color-formFieldBorder);
  }

  &::placeholder {
    color: ${c("bodyDimmed")};
  }
`,n0=i.forwardRef((e,t)=>{var a=e,{onChange:r,value:l,rows:n=4,isDisabled:s,placeholder:d,size:h="medium",resize:v="both",error:p=null}=a,g=y(a,["onChange","value","rows","isDisabled","placeholder","size","resize","error"]);return i.createElement(i.Fragment,null,i.createElement(y1,o({disabled:s,onChange:r,placeholder:d,ref:t,rows:n,value:l,size:h,resize:v,error:p},g)),p?i.createElement(i.Fragment,null,i.createElement(ct,{bottom:"xmsall"}),i.createElement(Ee,{color:"danger",fontWeight:"regular",size:"body-md"},p)):null)}),o0=null,E1=m.Z.div`
  position: relative;
`,z1=m.Z.ul`
  list-style: none;
  margin: 0;
  padding: 0;
`,x1=m.Z.span`
  color: var(--lns-color-red);
  margin-top: var(--lns-space-xsmall);
  display: block;
  width: 100%;
  grid-column-start: 1;
  grid-column-end: 3;
`,vt=e=>Array.isArray(e)&&e.length>0&&"group"in e[0],Or=({options:e,selectedOptionValue:t})=>{if(!e||!t)return{icon:null,title:null};if(vt(e))for(const a of e){const r=a.items.find(l=>l.value===t);if(r)return r}else return e.find(r=>r.value===t)||{icon:null,title:null};return{icon:null,title:null}},$1=({options:e,selectedItem:t,selectedOptionValue:a})=>{if(t)return t.icon;if(a)return Or({options:e,selectedOptionValue:a}).icon},R1=({options:e,selectedItem:t,selectedOptionValue:a,placeholder:r})=>t?t.title:a?Or({options:e,selectedOptionValue:a}).title:r,k1=({selectedItem:e,getInputProps:t,ariaMenuName:a})=>{const r=e?`selected value is ${e.title}`:"no value selected";return{"aria-activedescendant":t()["aria-activedescendant"],"aria-label":[a,r].filter(Boolean).join(", ")}},M1=m.Z.button`
  position: relative;
  width: 100%;
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  font: inherit;
  color: inherit;
  cursor: pointer;

  &:disabled {
    cursor: default;
  }
`,L1=m.Z.input`
  -webkit-appearance: none;
  font-family: inherit;
  width: 100%;
  height: var(--lns-formFieldHeight);
  border: none;
  color: inherit;
  background-color: ${c("formFieldBackground")};
  transition: 0.3s box-shadow;
  padding-top: 0;
  padding-bottom: 0;
  id: ${e=>e.id};
  padding-left: ${e=>e.hasIcon?u(5.5):"var(--lns-formFieldHorizontalPadding)"};
  padding-right: ${e=>e.hasAddOn?u(5.5):"var(--lns-formFieldHorizontalPadding)"};
  border-radius: var(--lns-formFieldRadius);
  box-shadow: inset 0 0 0
    ${e=>e.hasError?"var(--lns-formFieldBorderWidthFocus) var(--lns-color-danger)":"var(--lns-formFieldBorderWidth) var(--lns-color-formFieldBorder)"};

  ${b("font-size","medium")};

  &:hover:not(:disabled):not(:focus) {
    box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidthFocus)
      ${e=>e.hasError?"var(--lns-color-danger)":"var(--lns-color-blurple)"};
  }

  &:focus {
    outline: 1px solid transparent;
    box-shadow: var(--lns-formFieldBorderShadowFocus);
  }

  &:disabled {
    color: ${c("disabledContent")};
    background-color: ${c("disabledBackground")};
  }

  &:disabled:hover {
    box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidth)
      var(--lns-color-formFieldBorder);
  }

  &::placeholder {
    color: ${c("bodyDimmed")};
  }
`,H1=m.Z.div`
  position: absolute;
  pointer-events: none;
  width: ${u(6)};
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  left: 0;
`,_1=m.Z.div`
  position: absolute;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  right: 0;
  width: ${u(6)};
  top: 50%;
  transform: translateY(-50%);
`,S1=m.Z.div`
  position: absolute;
  top: 0;
  left: ${e=>e.hasIcon?u(5.5):"var(--lns-formFieldHorizontalPadding)"};
  right: ${u(5.5)};
  bottom: 0;
  display: flex;
  align-items: center;
  pointer-events: none;
  color: inherit;
`,I1=m.Z.img`
  height: 100%;
  width: auto;
  min-width: 100%;
  min-height: 100%;
  object-fit: cover;
  opacity: ${({isDisabled:e})=>e?.5:1};
`,B1=({selectedItem:e,selectedOptionValue:t,placeholder:a,isDisabled:r,options:l,getInputProps:n,ariaMenuName:s,isOpen:d,onInputFocus:h,hasError:v,hasLoader:p,inputValue:g,handleInputValueChange:f,inputRef:C,id:z})=>{const E=$1({options:l,selectedItem:e,selectedOptionValue:t}),w=Boolean(E),$=r?"disabledContent":void 0,_=()=>{r||h()},O=o(o({role:"combobox","aria-autocomplete":"list","aria-haspopup":"listbox","aria-expanded":d},k1({selectedItem:e,getInputProps:n,ariaMenuName:s})),n({id:z,"aria-labelledby":void 0,disabled:r,onFocus:_,onClick:_,value:g,onBlur:()=>{f("")},onChange:j=>f(j.target.value)})),L=!g&&!t;return i.createElement(M1,{onClick:_,disabled:r},w&&i.createElement(H1,null,typeof E=="string"?i.createElement(re,{radius:"50",width:3,height:3,overflow:"hidden"},i.createElement(_e,{alignment:"center"},i.createElement(I1,{src:E,alt:"",isDisabled:r}))):i.createElement(Q,{icon:E,color:$})),i.createElement(L1,x(o({ref:C},O),{hasIcon:w,hasAddOn:!0,hasError:v,isDisabled:r})),!g&&i.createElement(S1,{hasIcon:w},i.createElement(Ee,{hasEllipsis:!0,color:L?"bodyDimmed":"inherit"},R1({options:l,selectedItem:e,selectedOptionValue:t,placeholder:a}))),i.createElement(_1,null,p?i.createElement(St,{size:"small"}):i.createElement(Q,{icon:i.createElement(Rr,null),color:$})))},Ar=(e,t)=>{var a;if(vt(t))for(const r of t){const l=r.items.find(n=>n.value===e);if(l)return l}else return(a=t.find(r=>r.value===e))!=null?a:null;return null},V1=(e,t)=>(e||null)!=t?.value,Pr=(e,t,a,r,l,n)=>{const s=!a&&e.value===r||a&&a.value===e.value;return i.createElement(Dt,x(o({key:t,getItemProps:n,icon:e.icon,hidden:e.hidden},n({key:`${e.value}-${t}`,index:t,item:e,disabled:e.isDisabled,"aria-selected":s})),{isDisabled:e.isDisabled,hasDivider:e.hasDivider,isHighlighted:l===t,isSelected:s}),e.title)},W1=e=>{var t=e,{options:a,selectedItem:r,selectedOptionValue:l,highlightedIndex:n,getItemProps:s,isLoading:d,loadingMessage:h,emptyResultsMessage:v,hasAvailableOptions:p}=t,g=y(t,["options","selectedItem","selectedOptionValue","highlightedIndex","getItemProps","isLoading","loadingMessage","emptyResultsMessage","hasAvailableOptions"]);const f=h||i.createElement(St,null),C=v||"No results";if(d)return i.createElement(Se,o({as:"div"},g),i.createElement(re,{padding:"large"},i.createElement(_e,{alignment:"center"},f)));if(!p)return i.createElement(Se,o({as:"div"},g),i.createElement(re,{padding:"large"},i.createElement(_e,{alignment:"center"},C)));if(!vt(a))return i.createElement(Se,o({},g),a.map((E,w)=>Pr(E,w,r,l,n,s)));let z=0;return i.createElement(Se,o({},g),a.map(E=>{const w=`group-${E.group.replace(/\s+/g,"-")}`;return i.createElement("li",{key:w},i.createElement(ct,{left:"medium",top:"small",bottom:"xsmall"},i.createElement(Ee,{id:w,size:"body-sm",fontWeight:"bold",htmlTag:E.headingTag||"h2"},E.group)),i.createElement(z1,{role:"group","aria-labelledby":w},E.items.map($=>Pr($,z++,r,l,n,s))))}))},D1=(0,i.forwardRef)((e,t)=>{var a=e,{container:r,onOptionChange:l,onInputValueChange:n,menuZIndex:s=1100,menuMaxWidth:d,menuMaxHeight:h=34,menuMinWidth:v,ariaMenuName:p,selectedOptionValue:g,onOuterClick:f,options:C,placeholder:z,menuPosition:E="left",isDisabled:w,onOpenChange:$,isLoading:_,loadingMessage:O,emptyResultsMessage:L,errorMessage:j,id:Y}=a,V=y(a,["container","onOptionChange","onInputValueChange","menuZIndex","menuMaxWidth","menuMaxHeight","menuMinWidth","ariaMenuName","selectedOptionValue","onOuterClick","options","placeholder","menuPosition","isDisabled","onOpenChange","isLoading","loadingMessage","emptyResultsMessage","errorMessage","id"]);const W=Vt(r),A=(0,i.useRef)(null),q=(0,i.useCallback)(D=>{A.current=D,t&&(typeof t=="function"?t(D):t.current=D)},[t]),[N,T]=(0,i.useState)(""),[I,ee]=(0,i.useState)(!1),[U,se]=(0,i.useState)(Ar(g,C)),[be,R]=(0,i.useState)(U),J=D=>{T(D),n&&n(D)},Ce={itemToString:D=>D?D.value:"",onChange:D=>{const me=D||null;R(me),l&&l(me)},onOuterClick:f,environment:W,selectedItem:be,isOpen:I};W&&(Ce.environment=W);const{layerProps:xe,triggerProps:he,renderLayer:k,triggerBounds:H}=(0,je.sJ)({isOpen:I,container:r,ResizeObserver:Ct.Z,placement:Wt[E],auto:!0,snap:!0});(0,i.useEffect)(()=>{if(V1(g,U)){const D=Ar(g,C);se(D),R(D),T("")}},[g,C,U]),(0,i.useEffect)(()=>{var D;$&&$(I),I||(D=A.current)==null||D.blur()},[I,$]);const we=(0,i.useMemo)(()=>Array.isArray(C)?vt(C)?C.some(D=>D.items.length>0):C.length>0:!1,[C]),pt=(D,me)=>{if(me.isOpen!==void 0){if(me.type===qe.ZP.stateChangeTypes.keyDownEscape)return ee(!1),{isOpen:!1};ee(me.isOpen)}return me};return i.createElement(E1,o({},V),i.createElement(qe.ZP,x(o({},Ce),{stateReducer:pt}),({getItemProps:D,getInputProps:me,getMenuProps:Nt,isOpen:Ze,highlightedIndex:xi,selectedItem:ca})=>i.createElement("div",{role:"presentation"},i.createElement("div",o({},he),i.createElement(B1,{inputRef:q,selectedItem:ca,selectedOptionValue:g,placeholder:z,isDisabled:w,options:C,getInputProps:me,ariaMenuName:p,inputValue:N,handleInputValueChange:J,isOpen:I&&Ze,onInputFocus:()=>{ee(!0)},hasLoader:_,hasError:Boolean(j),id:Y})),I&&Ze&&k(i.createElement("div",x(o({},xe),{style:x(o({},xe.style),{zIndex:s,width:v?"auto":H?.width})}),i.createElement(W1,{options:C,selectedItem:ca,selectedOptionValue:g,hasAvailableOptions:we,highlightedIndex:xi,getItemProps:D,isLoading:_,loadingMessage:O,emptyResultsMessage:L,position:E,downshiftMenuProps:Nt,maxWidth:d,maxHeight:h,minWidth:v}))),Boolean(j)&&!I?i.createElement(x1,null,j):null)))});D1.displayName="Typeahead";var i0=null,O1=({ariaMenuName:e,getInputProps:t,isOpen:a})=>({"aria-activedescendant":t()["aria-activedescendant"],"aria-expanded":a,"aria-label":e||""}),A1=m.Z.div`
  display: inline-block;
  vertical-align: middle;
`,s0=e=>{var t=e,{ariaMenuName:a,menuPosition:r="left",menuZIndex:l=1100,options:n,trigger:s,triggerCallback:d,isOpen:h,menuMinWidth:v=24,menuMaxWidth:p=48,menuMaxHeight:g,container:f,onOuterClick:C,triggerOffset:z=0,onOpenChange:E,search:w,role:$,menuItemRole:_}=t,O=y(t,["ariaMenuName","menuPosition","menuZIndex","options","trigger","triggerCallback","isOpen","menuMinWidth","menuMaxWidth","menuMaxHeight","container","onOuterClick","triggerOffset","onOpenChange","search","role","menuItemRole"]);const L=Vt(f),[j,Y]=useState3(!1),[V,W]=useState3(!1),[A,q]=useState3(""),N=R=>{const J=R.target.value;q(J)},T=R=>{switch(R.key){case"ArrowDown":case"ArrowUp":case"ArrowLeft":case"ArrowRight":case"Enter":case" ":case"Tab":case"Escape":W(!0);break;default:break}},I=h||j,{layerProps:ee,triggerProps:U,renderLayer:se}=useLayer3({isOpen:I,container:f,placement:Wt[r],ResizeObserver:ResizeObserver3,auto:!0,snap:!0,triggerOffset:z});useEffect5(()=>{E&&E(I)},[I,E]);const be=(R,J)=>(J.isOpen!==void 0&&Y(J.isOpen),J);return n=useMemo3(()=>w?w.searchType==="startsWith"?n.filter(R=>He(R.title).toLowerCase().startsWith(A.toLowerCase())):n.filter(R=>He(R.title).toLowerCase().includes(A.toLowerCase())):n,[n,A,w]),React33.createElement(Downshift3,{stateReducer:be,itemToString:R=>R?R.title:"",onSelect:R=>R&&!R.disabled&&R.onClick&&R.onClick(),onOuterClick:C,environment:L},({getInputProps:R,getItemProps:J,getMenuProps:Te,getToggleButtonProps:Ce,highlightedIndex:xe,isOpen:he})=>React33.createElement("div",o(o({},O),d?{role:null,"aria-haspopup":null,"aria-expanded":null,"aria-labelledby":null}:{}),React33.createElement("div",o({},U),d?d(o(o({},Ce({onKeyDown:T})),O1({ariaMenuName:a,getInputProps:R,isOpen:he}))):React33.createElement(A1,o({},Ce({onKeyDown:T,tabIndex:0})),s)),he&&se(React33.createElement("div",x(o({},ee),{style:x(o({},ee.style),{zIndex:l})}),React33.createElement(Se,{position:r,minWidth:v,maxWidth:p,maxHeight:g,downshiftMenuProps:()=>Te({onKeyDown:T}),role:$,search:w&&React33.createElement(kr,{ariaLabel:w.searchPlaceholder,placeholder:w.searchPlaceholder,value:A,onChange:N,getInputProps:R})},n.map((k,H)=>React33.createElement(Dt,o({key:H,isHighlighted:xe===H,keyboardMove:V&&xe===H,isDisabled:k.disabled,isSelected:k.selected,icon:k.icon,hasDivider:k.hasDivider,getItemProps:J,menuItemRole:_,index:H},J({key:H,index:H,item:k,disabled:k.disabled,onMouseMove:()=>{V&&W(!1)}})),k.title)))))))},c0=null,P1=m.Z.label`
  display: block;
  position: relative;

  .RadioBox:after {
    background-color: transparent;
  }
`,F1=m.Z.input`
  position: absolute;
  opacity: 0;

  &:not(:disabled) {
    cursor: pointer;

    & ~ .RadioBox {
      border: 2px solid ${c("body")};
    }

    &:checked ~ .RadioBox {
      border: 2px solid ${c("body")};
    }
  }

  &:disabled,
  &:disabled ~ .RadioBox {
    pointer-events: none;
  }

  &:disabled ~ .RadioBox {
    background-color: ${c("disabledBackground")};
  }

  &:checked {
    & ~ .RadioBox:after {
      background-color: ${c("blurple")};
    }

    &:disabled ~ .RadioBox:after {
      background-color: ${c("disabledContent")};
    }
  }

  &:focus-visible ~ .RadioBox {
    ${de()};
  }
`,T1=m.Z.span`
  cursor: pointer;
  width: ${u(2.25)};
  height: ${u(2.25)};
  ${F("full")};
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;

  &:after {
    content: '';
    width: ${u(1)};
    height: ${u(1)};
    ${F("full")};
    background-color: ${c("white")};
  }
`,Z1=(0,i.forwardRef)((e,t)=>{var a=e,{isDisabled:r,isChecked:l,onFocus:n,onChange:s,onBlur:d}=a,h=y(a,["isDisabled","isChecked","onFocus","onChange","onBlur"]);return i.createElement(P1,{htmlFor:h.id},i.createElement(F1,o({type:"radio",disabled:r,checked:l,onFocus:n,onChange:s,onBlur:d,ref:t},h)),i.createElement(T1,{className:"RadioBox"}))}),j1=Z1,fe={medium:{switchHeight:16,switchWidth:32,knobOffset:2},large:{switchHeight:20,switchWidth:36,knobOffset:2}},Pe={knob:{active:{enabled:c("white"),disabled:c("disabledContent")},inactive:{enabled:c("white"),disabled:c("disabledContent")}},track:{active:{enabled:c("blurple"),disabled:c("disabledBackground")},inactive:{enabled:c("grey6"),disabled:c("disabledBackground")}}},N1=e=>fe[e.switchSize].switchWidth-fe[e.switchSize].switchHeight,Fr=e=>fe[e.switchSize].switchHeight-fe[e.switchSize].knobOffset*2,U1=m.Z.label`
  display: block;
  position: relative;
`,K1=m.Z.input`
  position: absolute;
  opacity: 0;
  cursor: pointer;

  // to overlap SwitchBox and occupy the same space
  z-index: 1;
  margin: 0;
  width: ${e=>fe[e.switchSize].switchWidth}px;
  height: ${e=>fe[e.switchSize].switchHeight}px;

  &:focus-visible ~ .SwitchBox {
    ${at()};
  }
  &:not(:checked) {
    & + .SwitchBox {
      background-color: ${Pe.track.inactive.enabled};
    }
    &:disabled + .SwitchBox {
      background-color: ${Pe.track.inactive.disabled};
    }
  }
  &:checked {
    & + .SwitchBox {
      background-color: ${Pe.track.active.enabled};
    }
    &:disabled + .SwitchBox {
      background-color: ${Pe.track.active.disabled};
    }
    & + .SwitchBox:after {
      transform: translateX(${e=>N1(e)}px);
    }
  }
  &:disabled {
    pointer-events: none;
  }
`,G1=m.Z.div`
  width: ${e=>fe[e.switchSize].switchWidth}px;
  height: ${e=>fe[e.switchSize].switchHeight}px;
  position: relative;
  border-radius: var(--lns-radius-full);
  transition: 0.2s;
  cursor: ${e=>e.isDisabled?"default":"pointer"};
  &:after {
    content: '';
    position: absolute;
    top: ${e=>fe[e.switchSize].knobOffset}px;
    left: ${e=>fe[e.switchSize].knobOffset}px;
    width: ${e=>Fr(e)}px;
    height: ${e=>Fr(e)}px;
    border-radius: var(--lns-radius-full);
    transition: 0.15s;
    background-color: ${e=>e.isDisabled?Pe.knob.active.disabled:Pe.knob.active.enabled};
  }
`,Y1=e=>{var t=e,{isActive:a,isDisabled:r,onChange:l,size:n="medium",ariaLabelledby:s,ariaLabel:d,ariaDescribedby:h}=t,v=y(t,["isActive","isDisabled","onChange","size","ariaLabelledby","ariaLabel","ariaDescribedby"]);if(s&&d)throw new Error("ariaLabelledby and ariaLabel serve the same purpose and therefore cannot be used at the same time. Choose the one that best suites your needs.");return i.createElement(U1,{htmlFor:v.id},i.createElement(K1,x(o({},v),{checked:a,disabled:r,onChange:l,type:"checkbox",switchSize:n,"aria-labelledby":s,"aria-label":d,"aria-describedby":h,"aria-checked":a})),i.createElement(G1,{className:"SwitchBox",isDisabled:r,isActive:a,switchSize:n}))},X1=Y1,Tr={row:{wrapper:{display:"grid",gridTemplateColumns:"auto 1fr",alignItems:"center"},label:{marginLeft:"var(--lns-space-small)"},errorMessage:{marginLeft:"var(--lns-space-small)"}},"row-reverse":{wrapper:{display:"grid",gridTemplateColumns:"1fr auto",alignItems:"center"},label:{}},column:{wrapper:{},label:{marginBottom:"var(--lns-space-xsmall)"}}},J1=m.Z.div`
  ${e=>e.direction&&Tr[e.direction].wrapper};
`,Q1=m.Z.label`
  display: block;
  ${e=>{var t;return e.direction&&((t=Tr[e.direction])==null?void 0:t.label)}};
  ${e=>e.isLabelClickable&&"cursor: pointer"};
`,q1=m.Z.span`
  color: var(--lns-color-red);
  margin-top: var(--lns-space-xsmall);
  display: block;
  width: 100%;
  grid-column-start: 1;
  grid-column-end: 3;
`,eo=[j1,On,X1],to=e=>eo.includes(e),d0=e=>{var t=e,{label:a,children:r,errorMessage:l,labelFor:n,direction:s="column"}=t,d=y(t,["label","children","errorMessage","labelFor","direction"]);const h=React36.Children.toArray(r).some(p=>isValidElement(p)&&typeof p.type!="string"&&to(p.type)),v=a&&React36.createElement(Q1,{direction:s,htmlFor:n,isLabelClickable:h},a);return React36.createElement(J1,o({direction:s},d),s==="row"&&React36.createElement(React36.Fragment,null,r,v),s==="column"&&React36.createElement(React36.Fragment,null,v,r),s==="row-reverse"&&React36.createElement(React36.Fragment,null,v,r),l&&React36.createElement(q1,null,l))},u0=null;function h0(e,t){React37.useEffect(()=>{const a=r=>{!e.current||e.current.contains(r.target)||t(r)};return document.addEventListener("mousedown",a),document.addEventListener("touchstart",a),()=>{document.removeEventListener("mousedown",a),document.removeEventListener("touchstart",a)}},[e,t])}function m0(e){const[t,a]=useState4(!1),r=useCallback3(n=>{const s=e.current;n.type==="focusin"&&n.target===s&&a(!0)},[e]),l=useCallback3(n=>{const s=e.current;n.type==="focusout"&&n.target===s&&a(!1)},[e]);return useEffect6(()=>(document.addEventListener("focusin",r),document.addEventListener("focusout",l),()=>{document.removeEventListener("focusin",r),document.removeEventListener("focusout",l)}),[r,l]),Boolean(t)}function v0(e){const t=document;useLayoutEffect2(()=>{const a=t?.documentElement,r=t?.body;if(!(t==null||!a||!r))return e&&(r.style.setProperty("padding-top","3.25rem"),r.style.setProperty("transition","padding-top 350ms")),()=>{r.style.removeProperty("padding-top")}},[t,e])}var ro=null;function ao(){return i.createElement(Gt.Z,{label:"",testId:"ads-refreshed-icon"})}var lo=e=>i.createElement("svg",o({viewBox:"0 0 24 24",fill:"none"},e),i.createElement("path",{fill:"currentColor",fillRule:"evenodd",clipRule:"evenodd",d:"M7.42 2.293A1 1 0 0 1 8.127 2h7.245a1 1 0 0 1 .708.293l5.127 5.127a1 1 0 0 1 .293.707v7.245a1 1 0 0 1-.293.708l-5.127 5.127a1 1 0 0 1-.707.293H8.128a1 1 0 0 1-.708-.293L2.293 16.08A1 1 0 0 1 2 15.373V8.128a1 1 0 0 1 .293-.708L7.42 2.293ZM8.542 4 4 8.542v6.416L8.542 19.5h6.416l4.542-4.542V8.542L14.958 4H8.542Zm2.208 11.25a1 1 0 0 1 1-1h.009a1 1 0 1 1 0 2h-.009a1 1 0 0 1-1-1Zm2-7a1 1 0 1 0-2 0v3.5a1 1 0 1 0 2 0v-3.5Z"})),Ie={info:{bgColor:"var(--lns-color-blurple)",icon:i.createElement(ao,null),color:"var(--lns-color-white)",fontFamily:"inherit"},warning:{bgColor:"var(--lns-color-warning)",icon:i.createElement(lo,null),color:"var(--lns-color-grey8)",fontFamily:"inherit"},error:{bgColor:"var(--lns-color-danger)",icon:i.createElement(xr,null),color:"var(--lns-color-white)",fontFamily:"inherit"},internal:{icon:i.createElement("span",{role:"img"},"\u{1F514}"),color:"var(--lns-color-tealLight)",bgColor:"var(--lns-color-grey8)",fontFamily:"var(--lns-fontFamily-code)"}},Zr=350,no=m.Z.aside`
  --paddingXOffset: var(--lns-space-large);
  --alignItems: start;

  display: grid;
  align-items: var(--alignItems);
  justify-content: space-between;
  grid-template-columns: 1fr auto;
  ${e=>`background-color: ${Ie[e.severity].bgColor}`};
  ${e=>`font-family: ${Ie[e.severity].fontFamily}`};

  ${e=>`color: ${Ie[e.severity].color}`};
  position: fixed;
  padding: var(--lns-space-medium) var(--paddingXOffset);
  top: 0;
  left: 0;
  transition:
    ${Zr}ms box-shadow,
    ${Zr}ms transform;
  width: 100%;
  box-sizing: border-box;
  z-index: 1100;
  opacity: ${e=>e.isOpen?"1":"0"};
  transform: ${e=>e.isOpen?"translateY(0px)":"translateY(-100%)"};
  @media (min-width: 872px) {
    --alignItems: center;
  }
`,g0=({children:e,onCloseClick:t,isOpen:a,severity:r="info",id:l})=>{var n,s,d;useEffect7(()=>{if(!a)return;const v=p=>{p.key==="Escape"&&(p.preventDefault(),t&&t())};return window.addEventListener("keydown",v),()=>{window.removeEventListener("keydown",v)}},[a,t]),ro(a);const h=r==="internal";return a?React40.createElement(no,{isOpen:a,severity:r,id:l},React40.createElement(Oe,{alignItems:{default:"start",small:"center"},justifyContent:"space-between",autoFlow:h?"column":void 0,columns:h?void 0:["1fr auto"]},React40.createElement(re,{paddingY:{default:"xsmall",xsmall:0},paddingLeft:h?void 0:{default:0,medium:u(3.5)},width:"100%"},React40.createElement(Oe,{autoFlow:"column",gap:h?"medium":"small",justifyContent:"center"},(n=Ie[r])!=null&&n.icon?React40.createElement(_e,{alignment:"topLeft"},React40.createElement(Q,{icon:Ie[r].icon,color:(s=Ie[r].color)!=null?s:"var(--lns-color-white)"})):null," ",e))),t&&React40.createElement(Bt,{iconColor:(d=Ie[r].color)!=null?d:"var(--lns-color-white)",tabIndex:0,altText:"Close",icon:React40.createElement(At,null),onClick:t})):null},p0=null,jr="web-app",Pt="chrome-extension",oo={short:3e3,long:8e3},io=(e,t)=>S.F4`
  0% {
    opacity: 0;
    transform: translate(-50%, ${u(t===Pt?-8:8)});
  }
  // (300 / toastDuration) * 100 evaluates to 10% for short. Longer durations will have the same speed of animation
  ${300/e*100}% {
    opacity: 1;
    transform: translate(-50%, 0);
  }
  // 100 - (300 / toastDuration) * 100 evaluates to 90% for short. Longer durations will have the same speed of animation
  ${100-300/e*100}% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
`,so=e=>{switch(e){case jr:return"unset";case Pt:return u(4);default:return"unset"}},co=e=>{switch(e){case jr:return u(4);case Pt:return"unset";default:return u(4)}},uo=m.Z.div`
  animation: ${e=>io(e.toastDuration,e.platform)}
    ${e=>e.toastDuration}ms forwards;
  background-color: ${c("backgroundInverse")};
  ${F("250")};
  top: ${e=>so(e.platform)};
  bottom: ${e=>co(e.platform)};
  ${Ge("large")};
  color: ${c("bodyInverse")};
  display: grid;
  grid-auto-flow: column;
  gap: var(--lns-space-small);
  justify-content: space-between;
  left: 50%;
  max-width: ${u(50)}; // Fallback when min() function is not supported
  max-width: min(90%, ${u(50)});
  padding: ${u(1.5)} var(--lns-space-medium) ${u(1.5)} var(--lns-space-large);
  position: fixed;
  transform: translateX(-50%);
  width: max-content;
  z-index: ${e=>e.zIndex};
`,ho=m.Z.div`
  align-self: center;
`,f0=({children:e,isOpen:t,onCloseClick:a,zIndex:r=1100,duration:l="short",platform:n="web-app"})=>{const s=oo[l];return useEffect8(()=>{const d=setTimeout(()=>{t&&a()},s);return()=>clearTimeout(d)},[t]),React41.createElement(React41.Fragment,null,t&&React41.createElement(uo,{role:"presentation",onClick:d=>d.stopPropagation(),zIndex:r,isOpen:t,toastDuration:s,platform:n},React41.createElement(ho,{"aria-live":"polite"},e),a&&React41.createElement(Bt,{altText:"Close",icon:React41.createElement(At,null),onClick:a,iconColor:"bodyInverse"})))},b0=null,Nr={topLeft:"top-start",topCenter:"top-center",topRight:"top-end",bottomLeft:"bottom-start",bottomCenter:"bottom-center",bottomRight:"bottom-end",leftTop:"left-start",leftCenter:"left-center",leftBottom:"left-end",rightTop:"right-start",rightCenter:"right-center",rightBottom:"right-end"},mo=4,vo=ke.small.fontSize*ke.small.lineHeight,go=(mo-vo)/2,po=m.Z.div`
  background-color: ${c("backgroundInverse")};
  color: ${c("bodyInverse")};
  ${F("150")};
  ${Re("bold")};
  ${ge("small")};
  ${Ge("medium")};
  ${e=>b("max-width",e.maxWidth)};
  z-index: 1100;
  padding: ${u(go)} ${u(1.5)};
  z-index: ${e=>e.zIndex};
`,fo=m.Z.div`
  background-color: ${c("grey7")};
  border-radius: 3px;
  color: ${c("grey3")};
  ${Re("bold")};
  ${ge("small")};
  padding-left: ${u(.5)};
  padding-right: ${u(.5)};
`,bo=({children:e})=>i.createElement(fo,null,e),Co=e=>{var t=e,{children:a,maxWidth:r,onMouseEnter:l,onMouseLeave:n,layerProps:s,zIndex:d}=t,h=y(t,["children","maxWidth","onMouseEnter","onMouseLeave","layerProps","zIndex"]);return i.createElement(po,o(o({maxWidth:r,onMouseEnter:l,onMouseLeave:n,zIndex:d},s),h),a)},wo=m.Z.div`
  display: ${e=>e.isInline?"inline-block":"block"};
  ${e=>e.verticalAlign&&`vertical-align: ${e.verticalAlign}`};
  &:focus-visible {
    // Note: 0px solid transparent prevents focus rings from disappearing for -ms-high-contrast.
    // TODO(LNS-183): Provide more robust polyfill/support for :focus for older versions of Safari, which don't support :focus-visible
    outline: 0px solid transparent;
    box-shadow: var(--lns-formFieldBorderShadowFocus);
  }
`;function yo(e){switch(e){case"immediate":return 200;case"long":return 800;default:return 200}}var Eo=e=>{var t=e,{ariaLive:a=!1,children:r,content:l,shortcut:n,placement:s="topCenter",keepOpen:d,triggerOffset:h=4,maxWidth:v=26,isInline:p=!0,isDisabled:g,container:f,tabIndex:C=0,zIndex:z=1100,verticalAlign:E="middle",delay:w="immediate",tooltipId:$}=t,_=y(t,["ariaLive","children","content","shortcut","placement","keepOpen","triggerOffset","maxWidth","isInline","isDisabled","container","tabIndex","zIndex","verticalAlign","delay","tooltipId"]);const[O,L]=(0,je.XI)({delayEnter:yo(w),delayLeave:200}),[j,Y]=(0,i.useState)(!1),[V,W]=(0,i.useState)(!1),[A,q]=(0,i.useState)(!1),N=(0,i.useRef)(),T=!l||g;(0,i.useEffect)(()=>{if(T){W(!1);return}const R=j&&d;(O||R)&&W(!0),!O&&!R&&!A&&W(!1)},[l,g,j,T,d,W,O,A]);const I=()=>{q(!1),T||W(!0)},ee=()=>{W(!1),q(!1)};(0,i.useEffect)(()=>{if(!V)return;const R=J=>{J.key==="Escape"&&(J.preventDefault(),ee())};return window.addEventListener("keydown",R),()=>{window.removeEventListener("keydown",R)}},[V,W]);const{layerProps:U,triggerProps:se,renderLayer:be}=(0,je.sJ)({isOpen:V,placement:Nr[s],ResizeObserver:Ct.Z,triggerOffset:h,container:f,auto:!0});return i.createElement(i.Fragment,null,i.createElement(wo,x(o(o({},se),L),{onClick:R=>{R.detail===0&&q(!0)},onFocus:I,onBlur:ee,isInline:p,verticalAlign:E,tabIndex:T?-1:C,ref:(0,je.lq)(se.ref,N)}),r),a&&i.createElement("span",{className:"srOnly","aria-live":"polite"},V&&l),V&&be(i.createElement("div",x(o({},U),{style:x(o({},U.style),{zIndex:z})}),i.createElement(Co,o({maxWidth:v,onMouseEnter:()=>Y(!0),onMouseLeave:()=>Y(!1),role:"tooltip",id:$},_),i.createElement(Oe,{gap:"small"},i.createElement(Ee,{size:"small",fontWeight:"bold"},l),n&&i.createElement(Oe,{gap:"xsmall"},n.map((R,J)=>i.createElement(bo,{key:J},R))))))))},C0=Object.keys(Nr),zo=Eo,Ur=S.iv`
  @media (prefers-reduced-motion: no-preference) {
    animation: shimmer 2s infinite linear;
    background: linear-gradient(
      to right,
      var(--lns-color-disabledBackground) 4%,
      var(--lns-color-backgroundHover) 25%,
      var(--lns-color-disabledBackground) 36%
    );
    background-size: 1000px 100%;
    @keyframes shimmer {
      0% {
        background-position: -1000px 0;
      }
      100% {
        background-position: 1000px 0;
      }
    }
  }
`,xo=m.Z.div`
  ${e=>ge(e.size)};
  color: transparent;
  position: relative;
  &::after {
    content: '';
    position: absolute;
    background-color: var(--lns-color-disabledBackground);
    border-radius: var(--lns-radius-full);
    width: 100%;
    display: block;
    height: 71.45%;
    top: 0.2em;
    ${e=>e.animated&&Ur}
  }

  ${e=>e.lines>1&&`
      &:nth-of-type(3n+1) {
        width: calc(100% - 2.25rem);
      }
      &:nth-of-type(3n) {
        width: calc(100% - 4.125rem);
      }
    }
  `};
`,$o=m.Z.div`
  background-color: var(--lns-color-disabledBackground);
  ${e=>F(e.radius)};
  height: ${e=>e.height};
  width: ${e=>e.width};
  ${e=>e.animated&&Ur}
`,w0=({size:e="body-md",lines:t=1,animated:a=!1})=>React43.createElement(React43.Fragment,null,[...Array(t)].map((r,l)=>React43.createElement(xo,{key:l,size:e,lines:t,animated:a},"Loading"))),y0=({animated:e=!1,height:t="40px",radius:a="full",width:r="40px"})=>React43.createElement(React43.Fragment,null,React43.createElement($o,{animated:e,height:t,radius:a,width:r})),Kr=e=>React44.createElement("defs",null,React44.createElement("radialGradient",{id:`ai-logo-${e}-gradient-1`,cx:"50%",cy:"50%",r:"100%",fx:"0%",fy:"0%"},React44.createElement("stop",{offset:"30%",stopColor:"#97ACFD"}),React44.createElement("stop",{offset:"33%",stopColor:"#B3B2F4"}),React44.createElement("stop",{offset:"43%",stopColor:"#DEB0E0"}),React44.createElement("stop",{offset:"50%",stopColor:"#DFC6E5"}),React44.createElement("stop",{offset:"72%",stopColor:"#6663F6"})),React44.createElement("radialGradient",{id:`ai-logo-${e}-gradient-2`,r:"100%",fx:"40%",fy:"72%"},React44.createElement("stop",{offset:"20%",stopColor:"#615CF500"}),React44.createElement("stop",{offset:"32%",stopColor:"#615CF550"}),React44.createElement("stop",{offset:"48%",stopColor:"#6663F6"})),React44.createElement("radialGradient",{id:`ai-logo-${e}-gradient-3`,r:"100%",fx:"0%",fy:"100%"},React44.createElement("stop",{offset:"25%",stopColor:"#6663F6"}),React44.createElement("stop",{offset:"38%",stopColor:"#6E68F450"}),React44.createElement("stop",{offset:"45%",stopColor:"#6E68F400"}))),Gr="M30 15.4433C30 16.6091 29.0933 16.8581 27.9562 16.9301C22.5158 17.2323 16.7962 22.686 16.4795 28.112C16.422 29.2634 16.173 30.1702 15.0072 30.1702C13.8414 30.1702 13.578 29.2634 13.5205 28.0976C13.2038 22.686 7.48416 17.2323 2.05814 16.9301C0.906735 16.8581 0 16.6091 0 15.4433C0 14.2775 0.906735 14.043 2.05814 13.971C7.48416 13.6687 13.2038 7.65433 13.5205 2.22831C13.578 1.0769 13.827 0.170166 15.0072 0.170166C16.1874 0.170166 16.422 1.0769 16.4795 2.22831C16.7962 7.65433 22.5158 13.6687 27.9419 13.971C29.0933 14.043 30 14.2919 30 15.4433Z",Ro=e=>{var t=e,{brand:a,symbolColor:r,customId:l}=t,n=y(t,["brand","symbolColor","customId"]);switch(a){case"ai":return React44.createElement("svg",o({"aria-label":"Loom AI",viewBox:"0 0 30 31",fill:"none"},n),React44.createElement("title",null,"Loom AI"),r?React44.createElement("path",{d:Gr,fill:c(r)}):React44.createElement(React44.Fragment,null,Kr(l),[...Array(3)].map((s,d)=>React44.createElement("path",{key:d,d:Gr,fill:`url(#ai-logo-${l}-gradient-${d+1}`}))));case"apptile":return React44.createElement("svg",o({"aria-label":"Loom",viewBox:"0 0 40 40",fill:"none"},n),React44.createElement("title",null,"Loom"),React44.createElement("path",{d:"M0 12C0 5.37258 5.37258 0 12 0H28C34.6274 0 40 5.37258 40 12V28C40 34.6274 34.6274 40 28 40H12C5.37258 40 0 34.6274 0 28V12Z",fill:c(r||"blurple")}),React44.createElement("path",{d:"M32.3962 18.6213H25.1467L31.4251 14.9965L30.0463 12.6077L23.768 16.2325L27.392 9.95464L25.0032 8.57506L21.3792 14.8529V7.604H18.6215V14.8536L14.9961 8.57506L12.6081 9.95395L16.2327 16.2318L9.95437 12.6077L8.57552 14.9958L14.8539 18.6206H7.60449V21.3784H14.8532L8.57552 25.0032L9.95437 27.392L16.2321 23.7679L12.6074 30.0457L14.9961 31.4246L18.6208 25.1461V32.3957H21.3785V25.1468L25.0025 31.4246L27.3912 30.0457L23.7665 23.7672L30.0449 27.392L31.4238 25.0032L25.1461 21.3791H32.3947V18.6213H32.3962ZM20.0003 23.7505C17.921 23.7505 16.2355 22.0651 16.2355 19.9856C16.2355 17.9062 17.921 16.2207 20.0003 16.2207C22.0797 16.2207 23.7651 17.9062 23.7651 19.9856C23.7651 22.0651 22.0797 23.7505 20.0003 23.7505Z",fill:"white"}));case"product":return React44.createElement("svg",o({"aria-label":"Loom",viewBox:"0 0 40 40",fill:"none"},n),React44.createElement("path",{d:"M0 9.25C0 4.14137 4.14137 0 9.25 0H30.75C35.8586 0 40 4.14137 40 9.25V30.75C40 35.8586 35.8586 40 30.75 40H9.25C4.14137 40 0 35.8586 0 30.75V9.25Z",fill:c(r||"primary")}),React44.createElement("path",{d:"M32.3962 18.6756H25.1467L31.4251 15.0508L30.0463 12.662L23.768 16.2868L27.392 10.009L25.0032 8.62938L21.3792 14.9072V7.65833H18.6215V14.9079L14.9961 8.62938L12.6081 10.0083L16.2327 16.2861L9.95437 12.662L8.57552 15.0501L14.8539 18.6749H7.60449V21.4327H14.8532L8.57552 25.0575L9.95437 27.4463L16.2321 23.8222L12.6074 30.1L14.9961 31.4789L18.6208 25.2004V32.45H21.3785V25.2011L25.0025 31.4789L27.3912 30.1L23.7665 23.8215L30.0449 27.4463L31.4238 25.0575L25.1461 21.4334H32.3947V18.6756H32.3962ZM20.0003 23.8048C17.921 23.8048 16.2355 22.1194 16.2355 20.0399C16.2355 17.9605 17.921 16.275 20.0003 16.275C22.0797 16.275 23.7651 17.9605 23.7651 20.0399C23.7651 22.1194 22.0797 23.8048 20.0003 23.8048Z",fill:"white"}));default:return React44.createElement("svg",o({"aria-label":"Loom",viewBox:"0 0 31 30",fill:"none"},n),React44.createElement("title",null,"Loom"),React44.createElement("path",{d:"M30.01 13.43h-9.142l7.917-4.57-1.57-2.72-7.918 4.57 4.57-7.915-2.72-1.57-4.571 7.913V0h-3.142v9.139L8.863 1.225l-2.721 1.57 4.57 7.913L2.796 6.14 1.225 8.86l7.917 4.57H0v3.141h9.141l-7.916 4.57 1.57 2.72 7.918-4.57-4.571 7.915 2.72 1.57 4.572-7.914V30h3.142v-9.334l4.655 8.06 2.551-1.472-4.656-8.062 8.087 4.668 1.571-2.72-7.916-4.57h9.141v-3.14h.001zm-15.005 5.84a4.271 4.271 0 11-.001-8.542 4.271 4.271 0 01.001 8.542z",fill:c(r||"primary")}))}},ko=e=>{var t=e,{brand:a,wordmarkColor:r}=t,l=y(t,["brand","wordmarkColor"]);switch(a){case"ai":return React44.createElement("svg",o({"aria-label":"Loom AI",viewBox:"0 0 94 23",fill:r},l),React44.createElement("title",null,"Loom AI"),React44.createElement("path",{d:"M4.12637 22.4624H0V0H4.12637V22.4624Z"}),React44.createElement("path",{d:"M13.3999 19.1737C15.4166 19.1737 17.2781 17.7155 17.2781 14.8301C17.2781 11.9448 15.4166 10.4866 13.3999 10.4866C11.3833 10.4866 9.52175 11.9448 9.52175 14.8301C9.52175 17.6845 11.3833 19.1737 13.3999 19.1737ZM13.3999 6.7325C17.9606 6.7325 21.4045 10.1143 21.4045 14.8301C21.4045 19.515 17.9606 22.9277 13.3999 22.9277C8.83919 22.9277 5.39538 19.515 5.39538 14.8301C5.39538 10.1143 8.83919 6.7325 13.3999 6.7325Z"}),React44.createElement("path",{d:"M29.7548 19.1737C31.7714 19.1737 33.6329 17.7155 33.6329 14.8301C33.6329 11.9448 31.7714 10.4866 29.7548 10.4866C27.7381 10.4866 25.8766 11.9448 25.8766 14.8301C25.8766 17.6845 27.7381 19.1737 29.7548 19.1737ZM29.7548 6.7325C34.3155 6.7325 37.7593 10.1143 37.7593 14.8301C37.7593 19.515 34.3155 22.9277 29.7548 22.9277C25.194 22.9277 21.7502 19.515 21.7502 14.8301C21.7502 10.1143 25.194 6.7325 29.7548 6.7325Z"}),React44.createElement("path",{d:"M43.1622 22.4624H39.0358V7.19788H42.976V9.05941C43.8137 7.57019 45.7683 6.76353 47.4437 6.76353C49.5224 6.76353 51.1978 7.66326 51.9734 9.30761C53.1834 7.44609 54.7967 6.76353 56.8134 6.76353C59.6367 6.76353 62.3359 8.46992 62.3359 12.5653V22.4624H58.3336V13.403C58.3336 11.7586 57.5269 10.5176 55.6344 10.5176C53.8659 10.5176 52.8111 11.8827 52.8111 13.5271V22.4624H48.7157V13.403C48.7157 11.7586 47.878 10.5176 46.0165 10.5176C44.2171 10.5176 43.1622 11.8517 43.1622 13.5271V22.4624Z"}),React44.createElement("path",{d:"M84.1324 22.4624L82.3019 17.4363H73.3666L71.5361 22.4624H67.0064L75.4453 0.46538H80.4093L88.7862 22.4624H84.1324ZM77.8342 5.21226L74.7937 13.5271H80.8747L77.8342 5.21226Z"}),React44.createElement("path",{d:"M94 22.4624H89.6565V0.46538H94V22.4624Z"}));case"product":return React44.createElement("svg",o({"aria-label":"Loom",viewBox:"0 0 104 30",fill:"none"},l),React44.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M32.4383 7.29662C34.6059 7.29671 36.4904 7.77257 38.0897 8.72422C39.6888 9.67592 40.9247 11.0053 41.797 12.7102C42.6692 14.402 43.1045 16.3852 43.1045 18.6585C43.1044 20.9186 42.6693 22.9018 41.797 24.6068C40.9247 26.2985 39.6888 27.6207 38.0897 28.5724C36.4904 29.524 34.6059 29.9999 32.4383 30C30.2704 30 28.379 29.5241 26.7664 28.5724C25.1672 27.6208 23.9315 26.2985 23.0591 24.6068C22.1868 22.9018 21.7517 20.9186 21.7516 18.6585C21.7516 16.3851 22.1869 14.402 23.0591 12.7102C23.9315 11.0051 25.1671 9.67594 26.7664 8.72422C28.379 7.77249 30.2704 7.29662 32.4383 7.29662ZM32.4383 11.7584C31.3279 11.7584 30.3954 12.0564 29.642 12.6513C28.902 13.2461 28.3393 14.0587 27.956 15.0895C27.5861 16.1204 27.4009 17.3105 27.4009 18.6585C27.4009 19.9801 27.586 21.163 27.956 22.2071C28.3393 23.238 28.9019 24.0506 29.642 24.6454C30.3954 25.2402 31.3279 25.5382 32.4383 25.5382C33.5351 25.5381 34.4608 25.2401 35.2141 24.6454C35.9673 24.0506 36.53 23.2307 36.9001 22.1867C37.2831 21.1428 37.4733 19.9666 37.4734 18.6585C37.4734 17.324 37.2831 16.1406 36.9001 15.1099C36.5301 14.0661 35.9671 13.246 35.2141 12.6513C34.4608 12.0565 33.5351 11.7585 32.4383 11.7584Z",fill:r}),React44.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M56.9839 7.29662C59.1517 7.29662 61.036 7.77249 62.6354 8.72422C64.2348 9.67596 65.4702 11.005 66.3426 12.7102C67.215 14.4021 67.6524 16.385 67.6524 18.6585C67.6523 20.9186 67.215 22.9018 66.3426 24.6068C65.4702 26.2985 64.2346 27.6208 62.6354 28.5724C61.036 29.524 59.1516 30 56.9839 30C54.8166 29.9999 52.9267 29.5238 51.3143 28.5724C49.7151 27.6208 48.4795 26.2984 47.6071 24.6068C46.7347 22.9018 46.2974 20.9186 46.2973 18.6585C46.2973 16.3849 46.7346 14.4021 47.6071 12.7102C48.4795 11.005 49.7149 9.67596 51.3143 8.72422C52.9267 7.77274 54.8165 7.29671 56.9839 7.29662ZM56.9839 11.7584C55.8739 11.7585 54.9432 12.0566 54.1899 12.6513C53.4497 13.2461 52.8873 14.0585 52.504 15.0895C52.1339 16.1205 51.9488 17.3104 51.9488 18.6585C51.9488 19.9801 52.1339 21.163 52.504 22.2071C52.8873 23.2381 53.4497 24.0506 54.1899 24.6454C54.9431 25.2399 55.874 25.5381 56.9839 25.5382C58.081 25.5382 59.0064 25.2402 59.7598 24.6454C60.5133 24.0505 61.0756 23.231 61.4457 22.1867C61.8289 21.1427 62.0212 19.9667 62.0213 18.6585C62.0213 17.3239 61.8288 16.1407 61.4457 15.1099C61.0756 14.0657 60.5132 13.2461 59.7598 12.6513C59.0063 12.0564 58.081 11.7584 56.9839 11.7584Z",fill:r}),React44.createElement("path",{d:"M5.69001 24.7655H18.7174V29.5445H0V0H5.69001V24.7655Z",fill:r}),React44.createElement("path",{d:"M96.2633 7.2581C97.5984 7.2581 98.7952 7.54891 99.8527 8.13052C100.923 8.71205 101.762 9.56357 102.37 10.6866C102.991 11.8101 103.302 13.1852 103.302 14.8108V29.5445H97.7498V15.7625C97.7497 14.4545 97.3936 13.49 96.6803 12.8688C95.9667 12.2345 95.1007 11.9173 94.0834 11.9171C93.2908 11.9171 92.6027 12.0882 92.0213 12.4315C91.453 12.7751 91.0084 13.2511 90.6911 13.8591C90.3871 14.4671 90.2357 15.176 90.2357 15.9823V29.5445H84.8629V15.5654C84.8629 14.4552 84.5262 13.5682 83.8523 12.9073C83.1781 12.2464 82.3106 11.9171 81.2531 11.9171C80.5396 11.9172 79.8853 12.088 79.2907 12.4315C78.6959 12.7619 78.22 13.2521 77.8631 13.8998C77.5196 14.5343 77.3487 15.3205 77.3487 16.2588V29.5445H71.797V7.61387H77.0111L77.1652 11.7584C77.4644 10.9601 77.8429 10.2729 78.3005 9.69635C78.9746 8.86369 79.7606 8.24832 80.6594 7.8518C81.558 7.45546 82.496 7.25818 83.4738 7.2581C85.0733 7.2581 86.383 7.75323 87.4009 8.74462C88.2044 9.52754 88.8088 10.6088 89.225 11.985C89.5312 11.1783 89.9349 10.4756 90.4351 9.87537C91.1621 9.00295 92.0273 8.34693 93.032 7.91072C94.0364 7.47471 95.1136 7.2581 96.2633 7.2581Z",fill:r}));default:return React44.createElement("svg",o({"aria-label":"Loom",viewBox:"0 0 62 23",fill:r},l),React44.createElement("title",null,"Loom"),React44.createElement("path",{d:"M.109 21.973V.027h4.028v21.946H.109zM38.742 7.059h3.846v1.82c.818-1.456 2.727-2.244 4.362-2.244 2.03 0 3.665.88 4.422 2.485 1.18-1.82 2.756-2.485 4.725-2.485 2.756 0 5.39 1.667 5.39 5.668v9.67h-3.906v-8.851c0-1.607-.788-2.82-2.636-2.82-1.727 0-2.757 1.335-2.757 2.942v8.73h-3.997v-8.852c0-1.607-.817-2.82-2.635-2.82-1.757 0-2.787 1.305-2.787 2.942v8.73h-4.027V7.059zM13.24 22.405c-4.537 0-7.824-3.367-7.824-7.889 0-4.45 3.276-7.896 7.824-7.896 4.57 0 7.824 3.478 7.824 7.896 0 4.49-3.288 7.889-7.824 7.889zm0-12.135a4.25 4.25 0 00-4.244 4.247 4.25 4.25 0 004.244 4.247 4.25 4.25 0 004.243-4.247 4.25 4.25 0 00-4.243-4.247zM29.667 22.405c-4.538 0-7.824-3.367-7.824-7.889 0-4.45 3.276-7.896 7.824-7.896 4.57 0 7.824 3.478 7.824 7.896 0 4.49-3.29 7.889-7.824 7.889zm0-12.186a4.3 4.3 0 00-4.293 4.296 4.3 4.3 0 004.293 4.296 4.3 4.3 0 004.293-4.296 4.3 4.3 0 00-4.293-4.296z"}))}},Yr="M100 7.76427C100 8.35691 99.539 8.48348 98.961 8.52007C96.1953 8.67371 93.2877 11.4461 93.1267 14.2045C93.0975 14.7898 92.9709 15.2508 92.3783 15.2508C91.7856 15.2508 91.6517 14.7898 91.6225 14.1972C91.4615 11.4461 88.5539 8.67371 85.7955 8.52007C85.2102 8.48348 84.7492 8.35691 84.7492 7.76427C84.7492 7.17162 85.2102 7.05237 85.7955 7.01578C88.5539 6.86213 91.4615 3.80464 91.6225 1.04628C91.6517 0.460948 91.7783 0 92.3783 0C92.9782 0 93.0975 0.460948 93.1267 1.04628C93.2877 3.80464 96.1953 6.86213 98.9537 7.01578C99.539 7.05237 100 7.17894 100 7.76427Z",Mo=e=>{var t=e,{brand:a,wordmarkColor:r,symbolColor:l,customId:n}=t,s=y(t,["brand","wordmarkColor","symbolColor","customId"]);switch(a){case"ai":return React44.createElement("svg",o({"aria-label":"Loom AI",viewBox:"0 0 100 30",fill:"none"},s),React44.createElement("title",null,"Loom AI"),l?React44.createElement("path",{d:Yr,fill:c(l)}):React44.createElement(React44.Fragment,null,Kr(n),[...Array(3)].map((d,h)=>React44.createElement("path",{key:h,d:Yr,fill:`url(#ai-logo-${n}-gradient-${h+1}`}))),React44.createElement("g",{fill:r},React44.createElement("path",{d:"M4.1997 29.5909H0.570312V9.83386H4.1997V29.5909Z"}),React44.createElement("path",{d:"M12.3563 26.6983C14.1301 26.6983 15.7674 25.4157 15.7674 22.8778C15.7674 20.34 14.1301 19.0574 12.3563 19.0574C10.5826 19.0574 8.94526 20.34 8.94526 22.8778C8.94526 25.3884 10.5826 26.6983 12.3563 26.6983ZM12.3563 15.7555C16.3678 15.7555 19.3968 18.73 19.3968 22.8778C19.3968 26.9984 16.3678 30.0002 12.3563 30.0002C8.34491 30.0002 5.31587 26.9984 5.31587 22.8778C5.31587 18.73 8.34491 15.7555 12.3563 15.7555Z"}),React44.createElement("path",{d:"M26.7414 26.6983C28.5152 26.6983 30.1525 25.4157 30.1525 22.8778C30.1525 20.34 28.5152 19.0574 26.7414 19.0574C24.9676 19.0574 23.3303 20.34 23.3303 22.8778C23.3303 25.3884 24.9676 26.6983 26.7414 26.6983ZM26.7414 15.7555C30.7528 15.7555 33.7819 18.73 33.7819 22.8778C33.7819 26.9984 30.7528 30.0002 26.7414 30.0002C22.73 30.0002 19.7009 26.9984 19.7009 22.8778C19.7009 18.73 22.73 15.7555 26.7414 15.7555Z"}),React44.createElement("path",{d:"M38.534 29.5909H34.9047V16.1648H38.3703V17.8022C39.1071 16.4923 40.8263 15.7828 42.2999 15.7828C44.1282 15.7828 45.6018 16.5742 46.284 18.0205C47.3483 16.3831 48.7673 15.7828 50.5411 15.7828C53.0243 15.7828 55.3984 17.2837 55.3984 20.8858V29.5909H51.8782V21.6226C51.8782 20.1763 51.1687 19.0847 49.5041 19.0847C47.9486 19.0847 47.0208 20.2854 47.0208 21.7317V29.5909H43.4187V21.6226C43.4187 20.1763 42.6819 19.0847 41.0446 19.0847C39.4619 19.0847 38.534 20.2581 38.534 21.7317V29.5909Z"}),React44.createElement("path",{d:"M74.5698 29.5909L72.9598 25.1701H65.1006L63.4906 29.5909H59.5064L66.929 10.2432H71.2951L78.6631 29.5909H74.5698ZM69.0302 14.4184L66.3559 21.7317H71.7045L69.0302 14.4184Z"}),React44.createElement("path",{d:"M83.249 29.5909H79.4285V10.2432H83.249V29.5909Z"})));case"apptile":return React44.createElement("svg",o({"aria-label":"Loom",viewBox:"0 0 103 40",fill:"none"},s),React44.createElement("title",null,"Loom"),React44.createElement("path",{d:"M0 12C0 5.37258 5.37258 0 12 0H28C34.6274 0 40 5.37258 40 12V28C40 34.6274 34.6274 40 28 40H12C5.37258 40 0 34.6274 0 28V12Z",fill:c(l||"blurple")}),React44.createElement("path",{d:"M32.3962 18.6213H25.1467L31.4251 14.9965L30.0463 12.6077L23.768 16.2325L27.392 9.95464L25.0032 8.57506L21.3792 14.8529V7.604H18.6215V14.8536L14.9961 8.57506L12.6081 9.95395L16.2327 16.2318L9.95437 12.6077L8.57552 14.9958L14.8539 18.6206H7.60449V21.3784H14.8532L8.57552 25.0032L9.95437 27.392L16.2321 23.7679L12.6074 30.0457L14.9961 31.4246L18.6208 25.1461V32.3957H21.3785V25.1468L25.0025 31.4246L27.3912 30.0457L23.7665 23.7672L30.0449 27.392L31.4238 25.0032L25.1461 21.3791H32.3947V18.6213H32.3962ZM20.0003 23.7505C17.921 23.7505 16.2355 22.0651 16.2355 19.9856C16.2355 17.9062 17.921 16.2207 20.0003 16.2207C22.0797 16.2207 23.7651 17.9062 23.7651 19.9856C23.7651 22.0651 22.0797 23.7505 20.0003 23.7505Z",fill:"white"}),React44.createElement("g",{fill:r},React44.createElement("path",{d:"M47.6001 29.5076V10H51.1816V29.5076H47.6001Z"}),React44.createElement("path",{d:"M81.9516 16.2509H85.3718V17.8682C86.0987 16.575 87.7961 15.8739 89.2499 15.8739C91.0549 15.8739 92.5086 16.6556 93.1818 18.0832C94.2314 16.4659 95.633 15.8739 97.3834 15.8739C99.8338 15.8739 102.177 17.356 102.177 20.9122V29.5076H98.7027V21.6402C98.7027 20.2119 98.0019 19.1345 96.3591 19.1345C94.8238 19.1345 93.9079 20.3202 93.9079 21.7485V29.5084H90.3541V21.6402C90.3541 20.2119 89.6272 19.1345 88.0104 19.1345C86.4483 19.1345 85.5323 20.2933 85.5323 21.7485V29.5084H81.9516V16.2509Z"}),React44.createElement("path",{d:"M59.2755 29.8916C55.2407 29.8916 52.3189 26.899 52.3189 22.8795C52.3189 18.9241 55.2312 15.8603 59.2755 15.8603C63.3394 15.8603 66.232 18.9526 66.232 22.8795C66.232 26.8697 63.3086 29.8916 59.2755 29.8916ZM59.2755 19.1051C57.1944 19.1051 55.5018 20.7983 55.5018 22.8803C55.5018 24.9624 57.1944 26.6555 59.2755 26.6555C61.3565 26.6555 63.0484 24.9624 63.0484 22.8803C63.0484 20.7983 61.3565 19.1051 59.2755 19.1051Z"}),React44.createElement("path",{d:"M73.8823 29.8916C69.8476 29.8916 66.9258 26.899 66.9258 22.8795C66.9258 18.9241 69.8381 15.8603 73.8823 15.8603C77.9463 15.8603 80.8389 18.9526 80.8389 22.8795C80.8389 26.8697 77.9139 29.8916 73.8823 29.8916ZM73.8823 19.0601C71.7776 19.0601 70.0652 20.7738 70.0652 22.8788C70.0652 24.9837 71.7776 26.6974 73.8823 26.6974C75.9871 26.6974 77.6995 24.9837 77.6995 22.8788C77.6988 20.7738 75.9863 19.0601 73.8823 19.0601Z"})));case"product":return React44.createElement("svg",o({viewBox:"0 0 112 40",fill:"none","aria-label":"Loom"},s),React44.createElement("path",{d:"M0 9.25C0 4.14137 4.14137 0 9.25 0H30.75C35.8586 0 40 4.14137 40 9.25V30.75C40 35.8586 35.8586 40 30.75 40H9.25C4.14137 40 0 35.8586 0 30.75V9.25Z",fill:c(l||"primary")}),React44.createElement("path",{d:"M32.3962 18.6756H25.1467L31.4251 15.0508L30.0463 12.662L23.768 16.2868L27.392 10.009L25.0032 8.62938L21.3792 14.9072V7.65833H18.6215V14.9079L14.9961 8.62938L12.6081 10.0083L16.2327 16.2861L9.95437 12.662L8.57552 15.0501L14.8539 18.6749H7.60449V21.4327H14.8532L8.57552 25.0575L9.95437 27.4463L16.2321 23.8222L12.6074 30.1L14.9961 31.4789L18.6208 25.2004V32.45H21.3785V25.2011L25.0025 31.4789L27.3912 30.1L23.7665 23.8215L30.0449 27.4463L31.4238 25.0575L25.1461 21.4334H32.3947L32.3962 18.6756ZM20.0003 23.8048C17.921 23.8048 16.2355 22.1194 16.2355 20.0399C16.2355 17.9605 17.921 16.275 20.0003 16.275C22.0797 16.275 23.7651 17.9605 23.7651 20.0399C23.7651 22.1194 22.0797 23.8048 20.0003 23.8048Z",fill:"white"}),React44.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M70.3743 15.1855C71.6352 15.1855 72.7252 15.459 73.6442 16.0059C74.5709 16.5527 75.2848 17.3237 75.7861 18.3187C76.2874 19.3061 76.5381 20.4568 76.5381 21.7708C76.5381 23.0773 76.2874 24.2242 75.7861 25.2116C75.2848 26.199 74.5709 26.9661 73.6442 27.513C72.7252 28.0599 71.6352 28.3333 70.3743 28.3333C69.1135 28.3333 68.0197 28.0599 67.0931 27.513C66.174 26.9661 65.4639 26.199 64.9626 25.2116C64.4613 24.2242 64.2106 23.0773 64.2106 21.7708C64.2106 20.4568 64.4613 19.3061 64.9626 18.3187C65.4639 17.3237 66.174 16.5527 67.0931 16.0059C68.0197 15.459 69.1135 15.1855 70.3743 15.1855ZM70.3743 17.7376C69.7287 17.7376 69.1895 17.9161 68.7565 18.2731C68.3312 18.6225 68.0084 19.101 67.7881 19.7087C67.5754 20.3087 67.4691 20.9923 67.4691 21.7594C67.4691 22.519 67.5754 23.2026 67.7881 23.8102C68.0084 24.4179 68.3312 24.9002 68.7565 25.2572C69.1895 25.6066 69.7287 25.7812 70.3743 25.7812C71.02 25.7812 71.5592 25.6066 71.9922 25.2572C72.4251 24.9002 72.7479 24.4179 72.9606 23.8102C73.1733 23.2026 73.2796 22.519 73.2796 21.7594C73.2796 20.9999 73.1733 20.3163 72.9606 19.7087C72.7479 19.101 72.4251 18.6225 71.9922 18.2731C71.5592 17.9161 71.02 17.7376 70.3743 17.7376Z",fill:r}),React44.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M84.6387 15.1855C85.8995 15.1855 86.9895 15.459 87.9085 16.0059C88.8352 16.5527 89.5491 17.3237 90.0505 18.3187C90.5518 19.3061 90.8024 20.4568 90.8024 21.7708C90.8024 23.0773 90.5518 24.2242 90.0505 25.2116C89.5491 26.199 88.8352 26.9661 87.9085 27.513C86.9895 28.0599 85.8995 28.3333 84.6387 28.3333C83.3778 28.3333 82.2841 28.0599 81.3574 27.513C80.4384 26.9661 79.7282 26.199 79.2269 25.2116C78.7256 24.2242 78.4749 23.0773 78.4749 21.7708C78.4749 20.4568 78.7256 19.3061 79.2269 18.3187C79.7282 17.3237 80.4384 16.5527 81.3574 16.0059C82.2841 15.459 83.3778 15.1855 84.6387 15.1855ZM84.6387 17.7376C83.9931 17.7376 83.4538 17.9161 83.0208 18.2731C82.5955 18.6225 82.2727 19.101 82.0524 19.7087C81.8397 20.3087 81.7334 20.9923 81.7334 21.7594C81.7334 22.519 81.8397 23.2026 82.0524 23.8102C82.2727 24.4179 82.5955 24.9002 83.0208 25.2572C83.4538 25.6066 83.9931 25.7812 84.6387 25.7812C85.2843 25.7812 85.8236 25.6066 86.2565 25.2572C86.6895 24.9002 87.0123 24.4179 87.2249 23.8102C87.4376 23.2026 87.5439 22.519 87.5439 21.7594C87.5439 20.9999 87.4376 20.3163 87.2249 19.7087C87.0123 19.101 86.6895 18.6225 86.2565 18.2731C85.8236 17.9161 85.2843 17.7376 84.6387 17.7376Z",fill:r}),React44.createElement("path",{d:"M54.9365 25.3483H62.3421V28.0827H51.6667V11.1068H54.9365V25.3483Z",fill:r}),React44.createElement("path",{d:"M107.368 15.1514C108.135 15.1514 108.823 15.3185 109.43 15.6527C110.046 15.9869 110.528 16.4768 110.877 17.1224C111.234 17.768 111.413 18.5579 111.413 19.4922V28.0827H108.211V20.0505C108.211 19.2985 108.006 18.744 107.596 18.387C107.186 18.0301 106.688 17.8516 106.104 17.8516C105.655 17.8516 105.264 17.9503 104.93 18.1478C104.603 18.3377 104.349 18.6073 104.167 18.9567C103.992 19.3061 103.905 19.7125 103.905 20.1758V28.0827H100.794V19.9365C100.794 19.2985 100.601 18.7934 100.213 18.4212C99.8334 18.0414 99.3397 17.8516 98.7321 17.8516C98.3143 17.8516 97.9346 17.9465 97.5928 18.1364C97.251 18.3263 96.9813 18.6073 96.7839 18.9795C96.5864 19.3441 96.4876 19.796 96.4876 20.3353V28.0827H93.2747V15.3451H96.2712L96.3786 17.806C96.5512 17.3255 96.7692 16.9151 97.0345 16.5755C97.4219 16.0894 97.8738 15.7324 98.3903 15.5046C98.9068 15.2691 99.4461 15.1514 100.008 15.1514C100.927 15.1514 101.668 15.44 102.23 16.0173C102.677 16.4764 103.023 17.1235 103.273 17.9574C103.451 17.4646 103.688 17.038 103.984 16.6781C104.417 16.1616 104.922 15.778 105.5 15.5273C106.085 15.2767 106.707 15.1514 107.368 15.1514Z",fill:r}));case"marketing":return React44.createElement("svg",o({"aria-label":"Loom",viewBox:"0 0 170 48",fill:"none"},s),React44.createElement("path",{d:"M154.37 25.212V38H150.414V24.108C150.414 19.968 148.758 18.128 144.986 18.128C141.306 18.128 138.776 20.566 138.776 25.212V38H134.82V15H138.776V18.772C140.248 16.058 142.962 14.54 146.044 14.54C149.954 14.54 152.622 16.518 153.772 20.152C155.06 16.61 158.142 14.54 161.96 14.54C167.112 14.54 169.964 18.036 169.964 24.522V38H166.008V25.212C166.008 20.474 164.352 18.128 160.58 18.128C156.9 18.128 154.37 20.566 154.37 25.212Z",fill:r}),React44.createElement("path",{d:"M119.367 38.46C112.467 38.46 108.419 33.354 108.419 26.454C108.419 19.554 112.467 14.54 119.367 14.54C126.221 14.54 130.223 19.554 130.223 26.454C130.223 33.354 126.221 38.46 119.367 38.46ZM119.367 18.22C114.445 18.22 112.283 22.084 112.283 26.454C112.283 30.824 114.445 34.78 119.367 34.78C124.243 34.78 126.359 30.824 126.359 26.454C126.359 22.084 124.243 18.22 119.367 18.22Z",fill:r}),React44.createElement("path",{d:"M94.3452 38.46C87.4452 38.46 83.3972 33.354 83.3972 26.454C83.3972 19.554 87.4452 14.54 94.3452 14.54C101.199 14.54 105.201 19.554 105.201 26.454C105.201 33.354 101.199 38.46 94.3452 38.46ZM94.3452 18.22C89.4232 18.22 87.2612 22.084 87.2612 26.454C87.2612 30.824 89.4232 34.78 94.3452 34.78C99.2212 34.78 101.337 30.824 101.337 26.454C101.337 22.084 99.2212 18.22 94.3452 18.22Z",fill:r}),React44.createElement("path",{d:"M64.094 7.77783H68.234V34.0438H81.942V37.9998H64.094V7.77783Z",fill:r}),React44.createElement("path",{d:"M0 12C0 5.37258 5.37258 0 12 0H36C42.6274 0 48 5.37258 48 12V36C48 42.6274 42.6274 48 36 48H12C5.37258 48 0 42.6274 0 36V12Z",fill:c(l||"primary")}),React44.createElement("g",{clipPath:"url(#clip0_45829_3572)"},React44.createElement("path",{d:"M38.0625 22.9644H29.9846L36.9804 18.9253L35.4441 16.2635L28.4482 20.3026L32.4864 13.3073L29.8246 11.77L25.7864 18.7653V10.688H22.7136V18.7661L18.6738 11.77L16.0129 13.3065L20.0518 20.3018L13.0559 16.2635L11.5195 18.9246L18.5154 22.9636H10.4375V26.0366H18.5146L11.5195 30.0757L13.0559 32.7375L20.0511 28.6991L16.0121 35.6945L18.6738 37.2309L22.7128 30.2349V38.313H25.7857V30.2356L29.8239 37.2309L32.4855 35.6945L28.4466 28.6984L35.4425 32.7375L36.979 30.0757L29.9838 26.0373H38.0609V22.9644H38.0625ZM24.25 28.6798C21.933 28.6798 20.0549 26.8018 20.0549 24.4847C20.0549 22.1676 21.933 20.2895 24.25 20.2895C26.567 20.2895 28.445 22.1676 28.445 24.4847C28.445 26.8018 26.567 28.6798 24.25 28.6798Z",fill:"white"})),React44.createElement("defs",null,React44.createElement("clipPath",{id:"clip0_45829_3572"},React44.createElement("rect",{width:"39",height:"39",fill:"white",transform:"translate(4.75 5)"}))));case"attributed":return React44.createElement("svg",o({"aria-label":"Loom",viewBox:"0 0 232 75",fill:"none"},s),React44.createElement("path",{d:"M181.37 52.212V65H177.414V51.108C177.414 46.968 175.758 45.128 171.986 45.128C168.306 45.128 165.776 47.566 165.776 52.212V65H161.82V42H165.776V45.772C167.248 43.058 169.962 41.54 173.044 41.54C176.954 41.54 179.622 43.518 180.772 47.152C182.06 43.61 185.142 41.54 188.96 41.54C194.112 41.54 196.964 45.036 196.964 51.522V65H193.008V52.212C193.008 47.474 191.352 45.128 187.58 45.128C183.9 45.128 181.37 47.566 181.37 52.212Z",fill:r}),React44.createElement("path",{d:"M146.367 65.46C139.467 65.46 135.419 60.354 135.419 53.454C135.419 46.554 139.467 41.54 146.367 41.54C153.221 41.54 157.223 46.554 157.223 53.454C157.223 60.354 153.221 65.46 146.367 65.46ZM146.367 45.22C141.445 45.22 139.283 49.084 139.283 53.454C139.283 57.824 141.445 61.78 146.367 61.78C151.243 61.78 153.359 57.824 153.359 53.454C153.359 49.084 151.243 45.22 146.367 45.22Z",fill:r}),React44.createElement("path",{d:"M121.345 65.46C114.445 65.46 110.397 60.354 110.397 53.454C110.397 46.554 114.445 41.54 121.345 41.54C128.199 41.54 132.201 46.554 132.201 53.454C132.201 60.354 128.199 65.46 121.345 65.46ZM121.345 45.22C116.423 45.22 114.261 49.084 114.261 53.454C114.261 57.824 116.423 61.78 121.345 61.78C126.221 61.78 128.337 57.824 128.337 53.454C128.337 49.084 126.221 45.22 121.345 45.22Z",fill:r}),React44.createElement("path",{d:"M91.094 34.7778H95.234V61.0438H108.942V64.9998H91.094V34.7778Z",fill:r}),React44.createElement("path",{d:"M155.186 11.9857C155.186 14.5147 156.33 16.5017 160.967 17.4049C163.676 18.007 164.278 18.4285 164.278 19.3316C164.278 20.2348 163.676 20.7767 161.749 20.7767C159.521 20.7767 156.872 19.994 155.126 18.9704V23.0648C156.511 23.7271 158.317 24.5099 161.749 24.5099C166.566 24.5099 168.433 22.3423 168.433 19.2112M168.433 19.2714C168.433 16.2608 166.867 14.8759 162.351 13.9125C159.883 13.3706 159.281 12.8287 159.281 12.046C159.281 11.0826 160.184 10.6611 161.81 10.6611C163.797 10.6611 165.723 11.2632 167.59 12.1062V8.19237C166.265 7.53004 164.278 7.04834 161.93 7.04834C157.474 7.04834 155.186 8.97513 155.186 12.1062",fill:r}),React44.createElement("path",{d:"M216.844 7.16846V24.329H220.517V11.2629L222.022 14.695L227.2 24.329H231.776V7.16846H228.164V18.2475L226.779 14.9961L222.624 7.16846H216.844Z",fill:r}),React44.createElement("path",{d:"M193.602 7.16846H189.628V24.329H193.602V7.16846Z",fill:r}),React44.createElement("path",{d:"M185.052 19.2109C185.052 16.2003 183.486 14.8154 178.97 13.852C176.501 13.3101 175.899 12.7682 175.899 11.9854C175.899 11.022 176.802 10.6005 178.428 10.6005C180.415 10.6005 182.342 11.2027 184.209 12.0456V8.13183C182.884 7.46949 180.897 6.98779 178.549 6.98779C174.093 6.98779 171.805 8.91459 171.805 12.0456C171.805 14.5745 172.949 16.5615 177.585 17.4647C180.295 18.0669 180.897 18.4883 180.897 19.3915C180.897 20.2947 180.295 20.8366 178.368 20.8366C176.14 20.8366 173.491 20.0539 171.745 19.0302V23.1247C173.13 23.787 174.936 24.5698 178.368 24.5698C183.125 24.5698 185.052 22.4021 185.052 19.2109Z",fill:r}),React44.createElement("path",{d:"M124.237 7.16846V24.329H132.426L133.69 20.5958H128.211V7.16846H124.237Z",fill:r}),React44.createElement("path",{d:"M108.04 7.16846V10.8414H112.436V24.329H116.47V10.8414H121.227V7.16846H108.04Z",fill:r}),React44.createElement("path",{d:"M102.199 7.16846H96.961L91 24.329H95.5761L96.4191 21.4388C97.4427 21.7398 98.5265 21.9205 99.6104 21.9205C100.694 21.9205 101.778 21.7398 102.802 21.4388L103.645 24.329H108.221C108.16 24.329 102.199 7.16846 102.199 7.16846ZM99.5501 18.3077C98.7674 18.3077 98.0448 18.1873 97.3825 18.0067L99.5501 10.5403L101.718 18.0067C101.055 18.1873 100.333 18.3077 99.5501 18.3077Z",fill:r}),React44.createElement("path",{d:"M146.576 7.16846H141.337L135.316 24.329H139.892L140.735 21.4388C141.759 21.7398 142.843 21.9205 143.927 21.9205C145.01 21.9205 146.094 21.7398 147.118 21.4388L147.961 24.329H152.537L146.576 7.16846ZM143.927 18.3077C143.144 18.3077 142.421 18.1873 141.759 18.0067L143.927 10.5403L146.094 18.0067C145.432 18.1873 144.709 18.3077 143.927 18.3077Z",fill:r}),React44.createElement("path",{d:"M207.992 7.16846H202.754L196.793 24.329H201.369L202.212 21.4388C203.236 21.7398 204.319 21.9205 205.403 21.9205C206.487 21.9205 207.571 21.7398 208.595 21.4388L209.438 24.329H214.014L207.992 7.16846ZM205.403 18.3077C204.621 18.3077 203.898 18.1873 203.236 18.0067L205.403 10.5403L207.571 18.0067C206.909 18.1873 206.126 18.3077 205.403 18.3077Z",fill:r}),React44.createElement("path",{d:"M0 18.75C0 8.39466 8.39466 0 18.75 0H56.25C66.6053 0 75 8.39466 75 18.75V56.25C75 66.6053 66.6053 75 56.25 75H18.75C8.39466 75 0 66.6053 0 56.25V18.75Z",fill:c(l||"primary")}),React44.createElement("g",{clipPath:"url(#clip0_45829_3571)"},React44.createElement("path",{d:"M59.4729 35.8821H46.8511L57.7822 29.571L55.3817 25.412L44.4506 31.723L50.7602 20.7928L46.6012 18.3909L40.2915 29.3211V16.7002H35.4902V29.3223L29.1781 18.3909L25.0204 20.7916L31.3312 31.7218L20.4001 25.412L17.9995 29.5698L28.9306 35.8809H16.3088V40.6824H28.9294L17.9995 46.9934L20.4001 51.1525L31.33 44.8426L25.0192 55.7728L29.1781 58.1735L35.489 47.2422V59.8643H40.2904V47.2434L46.6 58.1735L50.7589 55.7728L44.4481 44.8415L55.3792 51.1525L57.7799 46.9934L46.85 40.6835H59.4704V35.8821H59.4729ZM37.8909 44.8124C34.2705 44.8124 31.3361 41.878 31.3361 38.2575C31.3361 34.637 34.2705 31.7025 37.8909 31.7025C41.5112 31.7025 44.4456 34.637 44.4456 38.2575C44.4456 41.878 41.5112 44.8124 37.8909 44.8124Z",fill:"white"})),React44.createElement("defs",null,React44.createElement("clipPath",{id:"clip0_45829_3571"},React44.createElement("rect",{width:"60.9375",height:"60.9375",fill:"white",transform:"translate(7.42188 7.8125)"}))));default:return React44.createElement("svg",o({"aria-label":"Loom",viewBox:"0 0 100 30",fill:"none"},s),React44.createElement("title",null,"Loom"),React44.createElement("path",{d:"M30.01 13.43h-9.142l7.917-4.57-1.57-2.72-7.918 4.57 4.57-7.915-2.72-1.57-4.571 7.913V0h-3.142v9.139L8.863 1.225l-2.721 1.57 4.57 7.913L2.796 6.14 1.225 8.86l7.917 4.57H0v3.141h9.141l-7.916 4.57 1.57 2.72 7.918-4.57-4.571 7.915 2.72 1.57 4.572-7.914V30h3.142v-9.334l4.655 8.06 2.551-1.472-4.656-8.062 8.087 4.668 1.571-2.72-7.916-4.57h9.141v-3.14h.001zm-15.005 5.84a4.271 4.271 0 11-.001-8.542 4.271 4.271 0 01.001 8.542z",fill:c(l||"primary")}),React44.createElement("path",{d:"M38.109 25.973V4.027h4.028v21.946h-4.028zM76.742 11.059h3.846v1.82c.818-1.455 2.727-2.244 4.362-2.244 2.03 0 3.665.88 4.422 2.485 1.18-1.82 2.756-2.485 4.725-2.485 2.756 0 5.39 1.667 5.39 5.668v9.67h-3.906v-8.851c0-1.607-.788-2.82-2.636-2.82-1.727 0-2.757 1.335-2.757 2.942v8.73h-3.996v-8.852c0-1.607-.818-2.82-2.636-2.82-1.757 0-2.787 1.305-2.787 2.942v8.73h-4.027V11.059zM51.24 26.405c-4.538 0-7.824-3.367-7.824-7.889 0-4.45 3.276-7.896 7.824-7.896 4.57 0 7.824 3.478 7.824 7.896 0 4.49-3.288 7.889-7.824 7.889zm0-12.135a4.25 4.25 0 00-4.244 4.247 4.25 4.25 0 004.244 4.247 4.25 4.25 0 004.243-4.247 4.25 4.25 0 00-4.243-4.247zM67.667 26.405c-4.538 0-7.824-3.367-7.824-7.889 0-4.45 3.276-7.896 7.824-7.896 4.57 0 7.824 3.478 7.824 7.896 0 4.49-3.29 7.889-7.824 7.889zm0-12.186a4.3 4.3 0 00-4.293 4.296 4.3 4.3 0 004.293 4.296 4.3 4.3 0 004.293-4.296 4.3 4.3 0 00-4.293-4.296z",fill:r}))}},Lo=m.Z.span`
  display: block;
  ${e=>e.maxWidth&&b("max-width",e.maxWidth)};

  & > svg.lns-logoSvg {
    display: block;
    width: 100%;
    height: 100%;
    ${e=>e.maxWidth&&b("max-width",e.maxWidth)};
  }
`,E0=e=>{var t=e,{variant:a="combined",maxWidth:r,symbolColor:l,wordmarkColor:n="body",brand:s="loom",customId:d=""}=t,h=y(t,["variant","maxWidth","symbolColor","wordmarkColor","brand","customId"]);return React44.createElement(Lo,o({variant:a,maxWidth:r},h),a==="combined"&&React44.createElement(Mo,{brand:s,symbolColor:l,wordmarkColor:c(n),customId:d,className:"lns-logoSvg"}),a==="symbol"&&React44.createElement(Ro,{brand:s,symbolColor:l,customId:d,className:"lns-logoSvg"}),a==="wordmark"&&React44.createElement(ko,{brand:s,wordmarkColor:c(n),className:"lns-logoSvg"}))},z0=null,Ho="https://cdn.loom.com/assets/lens",Xr={small:"40px",medium:"80px"},_o=m.Z.span`
  animation: ${e=>e.animation};
  background-image: url(${Ho}/${e=>e.brand}-loader.svg);
  background-size: cover;
  background-position: left center;
  display: block;
  height: ${e=>Xr[e.size]};
  width: ${e=>Xr[e.size]};

  @keyframes spin {
    100% {
      background-position: right center;
    }
  }
`,x0=({animation:e="spin 2s infinite steps(49) forwards",brand:t="loom",size:a="medium"})=>React45.createElement(_o,{animation:e,brand:t,size:a}),$0=null,Ft="/* emotion-disable-server-rendering-unsafe-selector-warning-please-do-not-use-this-the-warning-exists-for-a-reason */",So={border:S.iv`
    .ListRowWrapper:last-child {
      border-bottom: 1px solid ${c("border")};
    }

    .ListRowWrapper,
    .ListRowWrapper:first-child ${Ft} {
      border-top: 1px solid ${c("border")};
    }
  `,stripe:S.iv`
    .ListRowWrapper {
      &:nth-child(odd) ${Ft} {
        background-color: ${c("backgroundSecondary")};
      }
    }

    .ListRowWrapper {
      ${F("medium")};
    }
  `,clear:S.iv``},Io=m.Z.div`
  .ListRowWrapper {
    grid-template-columns: ${e=>e.columns&&e.columns};
    ${e=>b("gap",e.gap)};
  }

  ${e=>So[e.variant]};
`,Bo=m.Z.div`
  display: grid;
  align-items: center;
  text-decoration: none;
  color: inherit;

  ${e=>b("height",e.height)};
  ${e=>b("min-height",e.minHeight)};
  ${e=>b("max-height",e.maxHeight)};
  ${e=>b("padding",e.padding)};
  ${e=>b("padding-top",e.paddingTop)};
  ${e=>b("padding-bottom",e.paddingBottom)};
  ${e=>b("padding-left",e.paddingLeft)};
  ${e=>b("padding-right",e.paddingRight)};

  ${e=>e.paddingY&&`
    ${b("padding-top",e.paddingY)}
    ${b("padding-bottom",e.paddingY)}
    `};

  ${e=>e.paddingX&&`
    ${b("padding-left",e.paddingX)}
    ${b("padding-right",e.paddingX)}
    `};

  ${e=>(e.onClick||e.href)&&"cursor: pointer;"};

  &.ListRowWrapper:nth-child(even),
  &.ListRowWrapper:nth-child(odd) ${Ft} {
    ${e=>e.backgroundColor&&`background-color: ${c(e.backgroundColor)}`};

    &:hover {
      ${e=>(e.onClick||e.href)&&`
      background-color: ${c("backgroundHover")};
      border-color: transparent;
      ${F("medium")};
    `};
    }
  }
`,Vo=e=>{var t=e,{children:a,htmlTag:r="li",className:l,backgroundColor:n,onClick:s,href:d,role:h}=t,v=y(t,["children","htmlTag","className","backgroundColor","onClick","href","role"]);const p=l?` ${l}`:"",g=["div","span","p","h1","h2","h3","h4","h5","h6","section","article","header","footer","main","aside","nav"],f=!r&&s;let C=!1;const z=r||"div";f||(C=g.includes(z));const E=!C||f?{onClick:s,onKeyDown:w=>{w.key==="Enter"&&(w.preventDefault(),s?.(w))}}:{};return React46.createElement(Bo,o(o({role:h||(r==="li"?"listitem":void 0),className:`ListRowWrapper${p}`,as:r,backgroundColor:n,href:d},E),v),a)},Wo=e=>e.map(t=>ce(t)).join(" "),R0=e=>{var t=e,{children:a,columns:r,gap:l,variant:n="stripe",htmlTag:s="ul"}=t,d=y(t,["children","columns","gap","variant","htmlTag"]);let h=a;return s==="ul"&&(h=React46.Children.map(a,v=>React46.isValidElement(v)&&v.type===Vo?React46.cloneElement(v,{htmlTag:"li"}):v)),React46.createElement(Io,o({as:s,columns:r&&Wo(r),gap:l,variant:n,role:s==="ul"?"list":void 0},d),h)},k0=null,gt=i.createContext({}),Do=e=>`calc(-1 * ${ce(e)})`,Jr=m.Z.div`
  ${e=>e.scrollOffset&&`margin: 0 ${Do(e.scrollOffset)};
  `};
`,Qr=m.Z.div`
  --activeIndicatorHeight: 3px;

  display: flex;
  overflow: auto;
  -ms-overflow-style: none;
  scrollbar-width: none;

  ${e=>e.hasBottomBorder&&"border-bottom: 1px solid var(--lns-color-border)"}

  ${e=>e.scrollOffset&&b("padding-left",e.scrollOffset)};

  &::-webkit-scrollbar {
    display: none;
  }

  > * {
    ${e=>e.hasFullTabs&&"flex: 1 0"};
    &:not(:first-of-type) {
      margin-left: 1rem;
    }
  }

  button {
    ${e=>e.hasFullTabs&&"width: 100%;"};
  }

  ::after {
    content: '';
    flex-shrink: 0;
    ${e=>e.scrollOffset&&b("width",e.scrollOffset)};
  }
`,qr=m.Z.div`
  ${F("200")};
  background-color: var(--lns-color-backgroundSecondary);

  padding: var(--lns-space-xsmall);

  display: flex;
  overflow: auto;
  -ms-overflow-style: none;
  scrollbar-width: none;
  ${e=>e.scrollOffset&&b("padding-left",e.scrollOffset)};

  &::-webkit-scrollbar {
    display: none;
  }

  > * {
    flex: 1 0;
  }

  button {
    width: 100%;
  }

  ::after {
    content: '';
    flex-shrink: 0;
    ${e=>e.scrollOffset&&b("width",e.scrollOffset)};
  }
`,ea=m.Z.button`
  appearance: none;
  font: inherit;
  background: transparent;
  border: 0;
  ${F("medium")};
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  padding: 0 0 calc(var(--lns-space-small) + var(--activeIndicatorHeight)) 0;
  position: relative;
  color: inherit;
  text-decoration: none;
  flex-shrink: 0;
  ${Re("bold")};
  transition: 0.6s color;
  white-space: nowrap;
  color: ${e=>c(e.isActive?"body":e.disabled?"disabledContent":"bodyDimmed")};
  ${e=>e.isActive&&`border-color: ${c("primary")};
  `};

  &:focus,
  &:focus-visible {
    outline: 1px solid transparent;
  }

  &:focus-visible {
    ${de(void 0,"inset")};
  }

  &:hover:not(:disabled) {
    color: ${c("body")};
    transition: 0.3s color;
  }

  &::after {
    bottom: 0;
    ${F("medium")};
    content: '';
    height: var(--activeIndicatorHeight);
    position: absolute;
    width: 100%;
    ${e=>e.isActive&&`background-color: ${c("primary")}`};
  }
`,ta=m.Z.button`
  padding: ${u(1)} 0;

  appearance: none;
  font: inherit;
  background: transparent;
  border: none;
  ${F("175")};
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  position: relative;
  color: inherit;
  text-decoration: none;
  flex-shrink: 0;
  ${Re("bold")};

  transition: 0.6s color;
  white-space: nowrap;
  color: ${e=>c(e.isActive?"body":e.disabled?"disabledContent":"bodyDimmed")};
  ${e=>e.isActive&&`background-color: ${c("background")};
     color: ${c("primary")};
  `};

  &:focus,
  &:focus-visible {
    outline: 1px solid transparent;
  }

  &:focus-visible {
    ${de(void 0,"inset")};
  }

  &:hover:not(:disabled) {
    color: ${c("primary")};
    transition: 0.3s color;
  }
`,M0=e=>{var t=e,{children:a,isActive:r,htmlTag:l="button",icon:n,isDisabled:s=!1}=t,d=y(t,["children","isActive","htmlTag","icon","isDisabled"]);const{isPilledDesign:h}=React47.useContext(gt);return h?React47.createElement(ta,o({as:l,isActive:r,icon:n,role:"tab","aria-selected":r,disabled:s},d),n&&React47.createElement(re,{htmlTag:"span",paddingRight:a&&"small"},React47.createElement(Q,{icon:n,color:"currentColor"})),a):React47.createElement(ea,o({as:l,isActive:r,icon:n,role:"tab","aria-selected":r,disabled:s},d),n&&React47.createElement(re,{htmlTag:"span",paddingRight:a&&"small"},React47.createElement(Q,{icon:n,color:"currentColor"})),a)},Oo=e=>{var t=e,{children:a,scrollOffset:r,hasFullTabs:l,isPilledDesign:n,hasBottomBorder:s=!1}=t,d=y(t,["children","scrollOffset","hasFullTabs","isPilledDesign","hasBottomBorder"]);const h=n?React47.createElement(qr,o({hasFullTabs:l,scrollOffset:r,role:"tablist"},d),a):React47.createElement(Qr,o({hasFullTabs:l,scrollOffset:r,hasBottomBorder:s,role:"tablist"},d),a);return r?React47.createElement(Jr,{scrollOffset:r},h):React47.createElement(gt.Provider,{value:{isPilledDesign:n}},h)},Ao=({tooltipProps:e,children:t,tooltipId:a})=>e?i.createElement(zo,x(o({},e),{tooltipId:a,tabIndex:-1}),t):t,ra=i.forwardRef((e,t)=>{var a=e,{tabContent:r,tooltipProps:l,isActive:n,htmlTag:s="button",icon:d,isDisabled:h=!1,onKeyDown:v,onClick:p}=a,g=y(a,["tabContent","tooltipProps","isActive","htmlTag","icon","isDisabled","onKeyDown","onClick"]);const{isPilledDesign:f}=i.useContext(gt),C=(0,i.useId)(),z=o({as:s,isActive:n,icon:d,role:"tab","aria-selected":n,disabled:h,tabIndex:n?0:-1,"aria-describedby":l?C:void 0,onKeyDown:v,onClick:p,ref:t},g);return i.createElement(Ao,{tooltipProps:l,tooltipId:C},f?i.createElement(ta,o({},z),d?i.createElement(re,{htmlTag:"span",paddingRight:r&&"small"},i.createElement(Q,{icon:d,color:"currentColor"})):null,r):i.createElement(ea,o({},z),d?i.createElement(re,{htmlTag:"span",paddingRight:r&&"small"},i.createElement(Q,{icon:d,color:"currentColor"})):null,r))});ra.displayName="TabNew";var Po=e=>{var t=e,{tabs:a,scrollOffset:r,hasFullTabs:l,isPilledDesign:n,hasBottomBorder:s=!1}=t,d=y(t,["tabs","scrollOffset","hasFullTabs","isPilledDesign","hasBottomBorder"]);const h=useRef5({}),v=useCallback4((z,E)=>{var w;let $=E;switch(z.key){case"ArrowLeft":z.preventDefault(),$=E>0?E-1:a.length-1;break;case"ArrowRight":z.preventDefault(),$=E<a.length-1?E+1:0;break;case"Home":z.preventDefault(),$=0;break;case"End":z.preventDefault(),$=a.length-1;break;default:return}(w=h.current[$])==null||w.focus()},[a.length]),p=useCallback4(z=>E=>{h.current[z]=E},[]),g=useMemo4(()=>a.map((z,E)=>React47.createElement(ra,o({key:E,ref:p(E),onKeyDown:w=>v(w,E)},z))),[a,v,p]),f=useMemo4(()=>n?React47.createElement(qr,o({hasFullTabs:l,scrollOffset:r,role:"tablist"},d),g):React47.createElement(Qr,o({hasFullTabs:l,scrollOffset:r,hasBottomBorder:s,role:"tablist"},d),g),[g,l,r,s,n,d]),C=React47.createElement(gt.Provider,{value:{isPilledDesign:n}},f);return r?React47.createElement(Jr,{scrollOffset:r},C):C},L0=e=>{var t=e,{children:a,tabs:r}=t,l=y(t,["children","tabs"]);return a&&r&&console.warn("Both children and tabs props are provided. Please use only one of them."),!a&&!r?(console.error("Either children or tabs must be provided."),null):a?React47.createElement(Oo,o({},l),a):React47.createElement(Po,o({tabs:r},l))},H0=null,Fo=m.Z.div`
  display: inline-grid;
  grid-auto-flow: column;
  align-items: center;
  vertical-align: middle;
  padding: 0 ${u(1.5)};
  min-height: ${u(3.25)};
  color: ${e=>c(e.color)};
  background-color: ${e=>c(e.backgroundColor)};
  ${F("100")};
  ${ge("small")};
  ${Re("bold")};
  ${b("gap","xsmall")};
`,_0=e=>{var t=e,{color:a,backgroundColor:r,children:l,icon:n,iconPosition:s="left"}=t,d=y(t,["color","backgroundColor","children","icon","iconPosition"]);const h=React48.createElement(re,{htmlTag:"span",paddingLeft:s==="right"&&"xsmall",paddingRight:s==="left"&&"xsmall"},React48.createElement(Q,{icon:n,color:"currentColor",size:2}));return React48.createElement(Fo,o({color:a,backgroundColor:r},d),n&&s==="left"&&h,l,n&&s==="right"&&h)},S0=null,To={topLeft:"top-start",topCenter:"top",topRight:"top-end",bottomLeft:"bottom-start",bottomCenter:"bottom",bottomRight:"bottom-end",leftTop:"left-start",leftCenter:"left",leftBottom:"left-end",rightTop:"right-start",rightCenter:"right",rightBottom:"right-end"},Zo=m.Z.div`
  position: relative;
  width: fit-content;
  // transform forces the popover to calculate the position from the trigger instead of the viewport
  transform: translate(0);
  z-index: ${e=>e.childrenZIndex};
`,aa=m.Z.div`
  ${e=>e.zIndex&&`z-index: ${e.zIndex}`};
`,I0=e=>{var t=e,{children:a,content:r,offset:l=.5,boundaryOffset:n=.5,isOpen:s,zIndex:d=500,childrenZIndex:h=1,placement:v="topCenter",rootId:p,boundaryElement:g="body",transitionDuration:f=0,transitionDelay:C=0}=t,z=y(t,["children","content","offset","boundaryOffset","isOpen","zIndex","childrenZIndex","placement","rootId","boundaryElement","transitionDuration","transitionDelay"]);const E=l*De,w=n*De,$=typeof window<"u",_=p&&$?document.getElementById(p):void 0,{stage:O,shouldMount:L}=useTransition2(s,f+C),j=()=>g==="body"&&$?document.body:g,{x:Y,y:V,reference:W,floating:A,strategy:q,update:N,refs:T}=useFloating({placement:To[v],middleware:[shift({padding:w,boundary:g?j():void 0,limiter:limitShift()}),flip({fallbackPlacements:["top","bottom"],fallbackStrategy:"initialPlacement"}),floatingUiOffset(E)],strategy:"fixed"});useEffect10(()=>{if(!(!T.reference.current||!T.floating.current))return autoUpdate(T.reference.current,T.floating.current,N)},[T.reference,T.floating,N,L]);const I={zIndex:d,ref:A,style:{position:q,top:V??"",left:Y??"",transition:`opacity ${f}ms ${C}ms`,opacity:O==="enter"?1:0}};return React49.createElement(Zo,x(o({ref:W},z),{childrenZIndex:h}),a,L&&React49.createElement(React49.Fragment,null,!_&&React49.createElement(aa,o({},I),r),_&&ReactDOM.createPortal(React49.createElement(aa,o({},I),r),_)))},B0=null,jo=m.Z.span`
  display: block;
  color: ${e=>e.color?c(e.color):c("grey8")};
  ${e=>e.size&&b("width",e.size)};
  ${e=>e.size&&b("height",e.size)};

  svg {
    display: block;
    width: 100%;
    height: 100%;
  }
`,V0=e=>{var t=e,{altText:a,illustration:r,color:l="orange",size:n=12}=t,s=y(t,["altText","illustration","color","size"]);return React50.createElement(jo,o({"aria-hidden":"true","aria-label":a,color:l,size:n},s),r)},W0=null,la=e=>S.iv`
  ${b("width",e.width)};
  ${b("height",e.height)};
  ${b("min-width",e.minWidth)};
  ${b("min-height",e.minHeight)};
  ${b("max-width",e.maxWidth)};
  ${b("max-height",e.maxHeight)};
`,No=m.Z.div`
  display: flex;
  ${e=>le("align-items",e.alignItems)};
  ${e=>e.justifyContent&&le("justify-content",e.justifyContent)};
  ${e=>e.alignContent&&le("align-content",e.alignContent)};
  ${e=>le("flex-wrap",e.wrap)};
  ${e=>e.direction&&le("flex-direction",e.direction)};
  ${e=>e.gap&&b("gap",e.gap)};
  ${e=>e.rowGap&&b("row-gap",e.rowGap)};
  ${e=>e.columnGap&&b("column-gap",e.columnGap)};
  ${e=>la(e)};
  ${e=>ar(e.as)};
`,Uo=m.Z.div`
  ${e=>tr("flex-grow",e.grow)};
  ${e=>tr("flex-shrink",e.shrink)};
  ${e=>e.basis&&b("flex-basis",e.basis)};
  ${e=>la(e)};
`,Ko=e=>{var t=e,{children:a,grow:r,shrink:l,basis:n,width:s,height:d,minWidth:h,minHeight:v,maxWidth:p,maxHeight:g,htmlTag:f="div",className:C,style:z}=t,E=y(t,["children","grow","shrink","basis","width","height","minWidth","minHeight","maxWidth","maxHeight","htmlTag","className","style"]);return(C||z)&&console.warn(Rt),React51.createElement(Uo,o({as:f,grow:r,shrink:l,basis:n,width:s,height:d,minWidth:h,minHeight:v,maxWidth:p,maxHeight:g},E),a)},Go=e=>{var t=e,{children:a,gap:r="initial",rowGap:l,columnGap:n,alignItems:s="center",justifyContent:d,alignContent:h,wrap:v="wrap",width:p,height:g,minWidth:f,minHeight:C,maxWidth:z,maxHeight:E,htmlTag:w="div",className:$,style:_}=t,O=y(t,["children","gap","rowGap","columnGap","alignItems","justifyContent","alignContent","wrap","width","height","minWidth","minHeight","maxWidth","maxHeight","htmlTag","className","style"]);return($||_)&&console.warn(Rt),React51.createElement(No,o({as:w,gap:r,rowGap:l,columnGap:n,alignItems:s,justifyContent:d,alignContent:h,wrap:v,width:p,height:g,minWidth:f,minHeight:C,maxWidth:z,maxHeight:E},O),w==="ul"||w==="ol"?Children.map(a,L=>L.type===Ko||L.type===Go?cloneElement(L,{htmlTag:"li"}):L):a)},D0=null,Yo=m.Z.div`
  padding: var(--lns-space-medium);
  & .react-colorful {
    width: auto;
    height: auto;
  }
  & .react-colorful__saturation {
    height: ${u(14)};
    border-bottom: none;
    box-shadow: inset 0 0 0 1px var(--lns-color-border);
    ${F(100)};
    margin-bottom: var(--lns-space-small);
  }

  & .react-colorful__hue {
    height: ${u(2)};
    width: 100%;
    box-shadow: inset 0 0 0 1px var(--lns-color-border);
    ${F("50")};
    margin-bottom: var(--lns-space-medium);
  }

  & .react-colorful__saturation-pointer {
    width: ${u(1)};
    height: ${u(1)};
    cursor: pointer;
    border: 2px solid white;
    box-shadow: 0 0 0 3px var(--lns-color-border);
    border-radius: var(--lns-radius-medium);
  }
  & .react-colorful__hue-pointer {
    width: ${u(1)};
    height: ${u(2.5)};
    border-radius: 2px;
    box-shadow: 0 0 0 2px var(--lns-color-border);
    cursor: pointer;
    border: 2px solid white;
  }
`,Xo=m.Z.div`
  position: relative;
  width: ${u(31)};
  background-color: var(--lns-color-overlay);
  ${F("250")};
  box-shadow:
    0 0 0 1px var(--lns-color-border),
    var(--lns-shadow-medium);
`,Jo=m.Z.div`
  position: relative;
  width: 100%;

  input {
    padding: 0 0 0 ${u(4)};
    height: ${u(4)};
    width: 100%;
    font: inherit;
    font-size: var(--lns-fontSize-small);
    border: none;
    box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidth)
      var(--lns-color-formFieldBorder);
    ${F("150")};
    transition: 0.3s box-shadow;
    background-color: var(--lns-color-overlay);
    color: var(--lns-color-body);

    &:hover {
      box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidthFocus)
        var(--lns-color-blurple);
    }

    &:focus {
      outline: 1px solid transparent;
      box-shadow: var(--lns-formFieldBorderShadowFocus);
    }
  }
`,Qo=m.Z.div`
  position: absolute;
  width: ${u(3)};
  height: ${u(3)};
  left: var(--lns-space-xsmall);
  top: var(--lns-space-xsmall);
  border: 1px solid rgba(0, 0, 0, 0.1);
  ${F("100")};
  background-color: ${e=>e.color};
`,qo=m.Z.div`
  position: relative;
  border-radius: var(--lns-radius-medium);
  padding: 0 var(--lns-space-medium) var(--lns-space-medium)
    var(--lns-space-medium);
`,ei=m.Z.div`
  display: grid;
  grid-template-columns: repeat(7, ${u(3)});
  gap: ${u(1)} ${u(1)};
  border-bottom: 1px solid var(--lns-color-border);
  padding: var(--lns-space-medium);
`,ti=m.Z.div`
  cursor: pointer;
  width: ${u(3)};
  height: ${u(3)};
  ${F("100")};
  background-color: ${e=>e.color};
  border: ${e=>e.selected===e.color?"1px solid white":"1px solid var(--lns-color-border)"};
  box-shadow: ${e=>e.selected===e.color&&"0 0 0 2px var(--lns-color-focusRing)"};
`,ri=({swatches:e,currentColor:t,onSwatchClick:a})=>{const r=e.includes(t)&&t;return React52.createElement(ei,null,e.map(l=>React52.createElement(ti,{key:l,color:l,selected:r,onClick:()=>a(l),role:"button",tabIndex:0,onKeyDown:n=>{n.key==="Enter"&&(n.preventDefault(),a(l))}})))},ai=({color:e,setColor:t})=>React52.createElement(Yo,null,React52.createElement(HexColorPicker,{color:e,onChange:t}),React52.createElement(Jo,null,React52.createElement(HexColorInput,{prefixed:!0,color:e,onChange:t}),React52.createElement(Qo,{color:e}))),O0=e=>{var t=e,{defaultColor:a="#ffffff",confirmButton:r,swatches:l,onChange:n}=t,s=y(t,["defaultColor","confirmButton","swatches","onChange"]);const[d,h]=useState6(a||"#FFFFFF"),v=g=>{h(g),n(g)},p=g=>{v(g)};return React52.createElement(Xo,o({},s),l&&React52.createElement(ri,{swatches:l,currentColor:d,onSwatchClick:p}),React52.createElement(ai,{color:d,setColor:v}),r&&React52.createElement(qo,null,r))},A0=null,li=2,Fe={small:{totalSize:u(2.25),height:u(.5625),dotSize:u(.375),gap:u(.25)},medium:{totalSize:u(3),height:u(.75),dotSize:u(.5),gap:u(.375)},large:{totalSize:u(6),height:u(1.5),dotSize:u(1),gap:u(.75)}},ni=e=>Fe[e.size].totalSize,oi=e=>Fe[e.size].height,na=e=>Fe[e.size].dotSize,ii=e=>Fe[e.size].gap,si=e=>Fe[e.size].dotSize,ci=e=>S.F4`
  0%, 40%, 100% {
    transform: translateY(50%);
  }
  20% {
    transform: translateY(calc(50% - ${e}));
  }
`,di=m.Z.span`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: ${e=>oi(e)};
  width: ${e=>ni(e)};
  gap: ${e=>ii(e)};
`,Tt=m.Z.span`
  width: ${e=>na(e)};
  height: ${e=>na(e)};
  border-radius: 50%;
  background-color: ${e=>c(e.color)};
  transform: translateY(50%);
  animation: ${e=>ci(si(e))} ${li}s
    ease-in-out infinite;
  animation-fill-mode: both;
  animation-delay: ${e=>e.delay}s;
`,P0=e=>{var t=e,{color:a="body",size:r="medium"}=t,l=y(t,["color","size"]);return React53.createElement(di,o({size:r},l),React53.createElement(Tt,{color:a,size:r,delay:0}),React53.createElement(Tt,{color:a,size:r,delay:.2}),React53.createElement(Tt,{color:a,size:r,delay:.4}))},F0=Object.keys(Fe),T0=null,Zt={medium:{totalSize:u(3),barHeight:u(2.25)}},oa={fast:1.2,slow:1.7},ui="linear-gradient(270deg, #565ADD 10.58%, #DC43BE 41.83%, #565ADD 69.23%, #565ADD 96.63%)",hi=2,jt=5,mi=u(.25),vi=e=>Zt[e.size||"medium"].barHeight,Je=e=>Zt[e.size||"medium"].totalSize,ia=e=>oa[e.speed||"fast"],gi=S.F4`
  0%, 100% {
    transform: scaleY(0.3);
  }
  50% {
    transform: scaleY(1);
  }
`,pi=S.F4`
  0% {
    background-position: 0% center;
  }
  100% {
    background-position: 100% center;
  }
`,fi=S.F4`
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
`,bi=m.Z.span`
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
  height: ${e=>Je(e)};
  width: ${e=>Je(e)};
  position: relative;
`,Ci=m.Z.span`
  width: ${mi};
  height: ${e=>vi(e)};
  background: ${e=>e.color==="ai-primary"?ui:c(e.color)};
  background-size: ${e=>Je(e)}
    ${e=>Je(e)};
  background-position: ${e=>{const a=(e.index+1)/(jt+1)-.5;return`calc(${Je(e)} * ${a}) center`}};
  opacity: 0; /* Ensure it starts invisible */
  transform: scaleY(0.3);
  transform-origin: center;
  animation:
    ${fi} 50ms ease-out forwards,
    ${gi} ${e=>ia(e)}s ease-in-out infinite,
    ${pi} ${hi}s linear infinite;

  animation-delay: ${e=>-1+e.index*(ia(e)/jt)}s;
  position: relative;
`,Z0=e=>{var t=e,{size:a="medium",speed:r="fast",color:l="body"}=t,n=y(t,["size","speed","color"]);const s=Array.from({length:jt},(d,h)=>React54.createElement(Ci,{key:h,index:h,size:a,speed:r,color:l}));return React54.createElement(bi,o({size:a,color:l},n),s)},j0=Object.keys(Zt),N0=Object.keys(oa),U0=null,wi=S.F4`
  0% {
    transform: scale(1);
    opacity: 0;
  }
  50% {
    transform: scale(1.6);
    opacity: 0.4;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
`,ze={dot:{size:"8px",borderWidth:"1px",borderColor:c("background")},positioning:{top:"-2px",right:"-2px"},animation:{duration:"2s",timing:"ease-out",iteration:"infinite"}},sa={blue:c("blue"),orange:c("orange")},yi=m.Z.span`
  position: relative;
  display: inline-block;
`,Ei=m.Z.span`
  position: absolute;
  height: ${ze.dot.size};
  width: ${ze.dot.size};
  top: ${ze.positioning.top};
  right: ${ze.positioning.right};
`,zi=m.Z.span`
  position: absolute;
  height: 100%;
  width: 100%;
  border-radius: var(--lns-radius-full);
  background-color: ${e=>sa[e.color||"blue"]};
  border: ${ze.dot.borderWidth} solid
    ${ze.dot.borderColor};

  &::after {
    content: '';
    position: absolute;
    height: 100%;
    width: 100%;
    border-radius: var(--lns-radius-full);
    background-color: ${e=>sa[e.color||"blue"]};
    opacity: 0;
    animation: ${e=>e.withPulse?wi:"none"}
      ${ze.animation.duration} ${ze.animation.timing}
      ${ze.animation.iteration};
    display: ${e=>e.withPulse?"block":"none"};
  }
`,K0=e=>{var t=e,{withPulse:a=!0,color:r="blue",children:l}=t,n=y(t,["withPulse","color","children"]);const s=React55.createElement(zi,{withPulse:a,color:r});return React55.createElement(yi,o({},n),l,React55.createElement(Ei,null,s))},G0=null;function Y0(e){return React56.createElement("svg",o({viewBox:"0 0 102 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React56.createElement("path",{d:"M96.072 5.826H5.928v90.145h90.144V5.826z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React56.createElement("path",{d:"M69.38 59.21c14.74 0 26.691-11.95 26.691-26.692S84.121 5.826 69.38 5.826c-14.741 0-26.692 11.95-26.692 26.692S54.638 59.21 69.38 59.21zM1 95.973h100M1 77.28h100M1 59.213h100M5.928 1v58.213M24.605 1v58.213M42.674 1v58.213",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}))}var X0=null;function J0(e){return React57.createElement("svg",o({viewBox:"0 0 100 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React57.createElement("path",{d:"M50.028 25.007A24.999 24.999 0 0034.586 1.905a25.022 25.022 0 00-27.26 5.42 25.002 25.002 0 0017.688 42.687V25.007h25.014z",fill:"currentColor"}),React57.createElement("path",{d:"M74.986 50.012a25.02 25.02 0 0023.11-15.436 24.993 24.993 0 00-5.422-27.25 25.017 25.017 0 00-42.702 17.681h25.014v25.005z",fill:"currentColor"}),React57.createElement("path",{d:"M49.972 74.99a25 25 0 0015.442 23.102 25.025 25.025 0 0027.26-5.42 25.002 25.002 0 00-17.688-42.687V74.99H49.972z",fill:"currentColor"}),React57.createElement("path",{d:"M25.014 100.003a25.003 25.003 0 0023.103-15.44 25.017 25.017 0 00-5.42-27.259A25.005 25.005 0 00.006 74.991h25.007v25.012z",fill:"currentColor"}))}var Q0=null;function q0(e){return React58.createElement("svg",o({viewBox:"0 0 100 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React58.createElement("path",{d:"M0 .002v100h100v-100H0zm90 90H10v-80h80v80z",fill:"currentColor"}),React58.createElement("path",{d:"M87 13.002H53.68c8.41 1.53 15 8.2 16.46 16.63H87v-16.63zM46.32 13.002H13v16.63h16.86c1.45-8.43 8.05-15.1 16.46-16.63zM13 32.632v15.87h18.19c3.12-7.32 10.35-12.47 18.81-12.47 8.46 0 15.69 5.15 18.81 12.47H87v-15.87H13zM13 67.372h20.4c3.71-5.15 9.76-8.52 16.59-8.52 6.84 0 12.88 3.36 16.59 8.52H87v-15.87H13v15.87zM13 87.002h23.47c3.61-3.18 8.34-5.12 13.53-5.12 5.19 0 9.92 1.93 13.53 5.12H87v-16.63H13v16.63z",fill:"currentColor"}))}var e2=null;function t2(e){return React59.createElement("svg",o({viewBox:"0 0 110 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React59.createElement("path",{d:"M55 100.888a54.867 54.867 0 0031.361-9.8H23.64a54.867 54.867 0 0031.361 9.8zM20.482 88.728h69.025a54.887 54.887 0 008.8-8.911H11.682a56.245 56.245 0 008.8 8.911zM9.262 76.492h91.476a54.95 54.95 0 004.411-7.957H4.851a54.95 54.95 0 004.41 7.957zM3.124 64.255h103.752a54.896 54.896 0 001.969-7.002H1.166a53.117 53.117 0 001.958 7.002zM0 46.015c0 2.03.121 4.039.33 6.003h109.34c.22-1.975.33-3.973.33-6.003v-.033H0v.033zM.363 39.782h109.274a54.71 54.71 0 00-.814-5.07H1.177a55.308 55.308 0 00-.814 5.07zM3.2 27.556H106.8a58.547 58.547 0 00-1.672-4.115H4.873A51.945 51.945 0 003.2 27.556zM9.405 15.32h91.19a59.831 59.831 0 00-2.321-3.161H11.726a59.814 59.814 0 00-2.321 3.16zM23.716.888a57.211 57.211 0 00-2.959 2.195h68.475A52.837 52.837 0 0086.273.888H23.716z",fill:"currentColor"}))}var r2=null;function a2(e){return React60.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React60.createElement("path",{d:"M100 38.086V0H61.914v9.93h21.132L54.963 38.013V16.88h-9.93v21.132L16.951 9.93h21.135V0H0v38.086h9.93V16.951l28.083 28.082H16.88v9.93h21.132L9.93 83.046V61.914H0V100h38.086v-9.93H16.951l28.082-28.086v21.135h9.93V61.984L83.046 90.07H61.914V100H100V61.914h-9.93v21.132L61.987 54.963H83.12v-9.93H61.987L90.07 16.951v21.135H100z",fill:"currentColor"}))}var l2=null;function n2(e){return React61.createElement("svg",o({viewBox:"0 0 142 142",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React61.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M19.945 50.767l50.766 50.766 50.765-50.766 19.944 19.944-51.672 51.673c-10.514 10.514-27.56 10.514-38.075 0L.001 70.711l19.944-19.944z",fill:"currentColor"}),React61.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M70.509 55.733l-27.901-27.63L23.57 47.14l28.354 28.084c10.264 10.264 26.904 10.264 37.168 0l28.48-28.362-19.038-19.037L70.51 55.733z",fill:"currentColor"}),React61.createElement("circle",{cx:70.71,cy:24.88,transform:"rotate(-45 70.71 24.88)",fill:"currentColor",r:17.592}))}var o2=null;function i2(e){return React62.createElement("svg",o({viewBox:"0 0 101 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React62.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M47.333 0H0v47.333h47.333V0zM74 0H52.667v21.333H74V0zM52.667 26H74v21.333H52.667V26zm-5.333 26.667H0V100h47.333V52.667zm52.666 0H52.667V100H100V52.667zM78.667 26H100v21.333H78.667V26zm3-10.333h2.667v2.666h-2.667v-2.666zm-3 5.666v-8.666h8.667v8.666h-8.667zM84.334 3h-2.667v2.667h2.667V3zm-5.667-3v8.667h8.667V0h-8.667zm15.668 15.667H97v2.666h-2.666v-2.666zm-3 5.666v-8.666H100v8.666h-8.666zM97 3h-2.666v2.667H97V3zm-5.666-3v8.667H100V0h-8.666z",fill:"currentColor"}))}var s2=null;function c2(e){return React63.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React63.createElement("path",{d:"M0 12.288L12.287 0v87.71h37.706L37.706 100H0v-87.71zM49.994 63.743l12.287-12.276v36.245h37.72L87.714 100h-37.72V63.743zM49.994 33.336l12.287-12.288v18.129h37.72L87.714 51.465h-37.72V33.336z",fill:"currentColor"}),React63.createElement("path",{d:"M49.993 12.288L62.28 0v9.064H100L87.713 21.353h-37.72v-9.065z",fill:"currentColor"}))}var d2=null;function u2(e){return React64.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React64.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 0h100v100H0V0zm17.12 10.344h-6.54v6.54h6.54v-6.54zm6.392-.61l6.396 1.364-1.364 6.396-6.397-1.365 1.365-6.396zM17.89 23.208l-6.396-1.365-1.365 6.396 6.396 1.365 1.365-6.396zM50.496 8.99l4.507 4.74-4.74 4.507-4.507-4.74 4.74-4.507zm-32.25 41.271l-4.507-4.74L9 50.03l4.507 4.74 4.74-4.508zm18.708-41.1l5.702 3.204-3.203 5.702-5.702-3.204 3.203-5.702zM17.906 36.999l-5.702-3.204L9 39.497l5.702 3.204 3.204-5.702zm46.62-27.57l2.216 6.153L60.59 17.8l-2.216-6.154 6.153-2.216zm-46.12 53.986l-3.69-5.4-5.4 3.69 3.69 5.4 5.4-3.69zM77.57 9.96l.82 6.488-6.489.82-.82-6.488 6.489-.82zM17.577 77.17l-1.733-6.306-6.307 1.733 1.733 6.306 6.307-1.733zm7.303-55.86l5.627 3.334-3.333 5.627-5.627-3.333 3.333-5.627zm29.716 6.384l-2.311-6.118-6.119 2.311 2.312 6.118 6.118-2.31zm-15.582-6.457l3.744 5.363-5.363 3.744-3.744-5.363 5.363-3.744zm27.458 7.017l-1.45-6.378-6.378 1.451 1.45 6.377 6.378-1.45zm11.731-5.521l-.411 6.527-6.527-.411.41-6.527 6.528.41zm-47.559 15.49l-4.362-4.873-4.873 4.362 4.362 4.873 4.873-4.361zm22.144-4.204l1.542 6.356-6.356 1.541-1.542-6.355 6.356-1.542zm-10.132 5.2l-3.201-5.703-5.704 3.2 3.201 5.704 5.704-3.201zm23.253-4.438l-.165 6.538-6.538-.165.165-6.538 6.538.165zm12.84.891l-6.31-1.72-1.719 6.31 6.31 1.72 1.72-6.31zm-51.5 10.013l3.238 5.683-5.683 3.237-3.238-5.683 5.683-3.237zm26.346 7.784l.11-6.539-6.54-.11-.11 6.54 6.54.11zm-13.008-7.287l1.58 6.347-6.347 1.58-1.58-6.348 6.347-1.58zM66.6 47.896l-6.29-1.793-1.792 6.29 6.29 1.793 1.792-6.29zm6.863-2.197l5.718 3.174-3.174 5.718-5.719-3.174 3.175-5.718zM28.985 58.767l-6.513.598.598 6.513 6.513-.598-.598-6.513zm19.734-.761l5.978 2.654-2.655 5.978-5.977-2.655 2.654-5.977zm-7.014 1.293l-6.523-.477-.478 6.522 6.523.478.478-6.523zm20.341-1.573l5.108 4.084-4.084 5.108-5.108-4.084 4.084-5.108zm17.236 5.44l-3.703-5.39-5.391 3.702 3.703 5.391 5.39-3.703zm-55.967 7.587l6.458 1.034-1.034 6.458-6.458-1.034 1.034-6.458zm31.473 2.343l-5.81-3.004-3.003 5.81 5.81 3.004 3.003-5.81zm-19.53-2.16l6.51.615-.615 6.512-6.512-.616.616-6.511zm31.919 3.807l-4.375-4.862-4.862 4.374 4.374 4.862 4.863-4.374zm8.616-4.746l3.444 5.56-5.56 3.444-3.444-5.56 5.56-3.444zM17.121 83.406h-6.54v6.54h6.54v-6.54zm7.036-1.184l6.1 2.356-2.356 6.101-6.1-2.356 2.356-6.101zm30.846 4.345l-4.507-4.74-4.74 4.508 4.508 4.739 4.739-4.507zm-18.049-4.57l5.702 3.205-3.203 5.701L33.75 87.7l3.203-5.702zm29.788 6.422l-2.216-6.154-6.153 2.217 2.216 6.153 6.153-2.216zm10.827-5.623l.82 6.489-6.489.82-.82-6.489 6.489-.82zm12.605-72.452h-6.54v6.54h6.54v-6.54zm-5.627 11.5l6.396 1.365-1.365 6.396-6.396-1.365 1.365-6.396zm6.752 28.417l-4.507-4.74-4.739 4.508 4.507 4.74 4.74-4.508zm-6.044-16.466L90.957 37l-3.204 5.702-5.701-3.204 3.203-5.702zm6.205 29.62l-3.69-5.4-5.4 3.69 3.69 5.4 5.4-3.69zm-2.563 7.449l1.733 6.306-6.306 1.733-1.734-6.306 6.307-1.733zm1.276 12.542h-6.54v6.54h6.54v-6.54z",fill:"currentColor"}))}var h2=null;function m2(e){return React65.createElement("svg",o({viewBox:"0 0 101 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React65.createElement("path",{fill:"currentColor",d:"M.001 53.596h47.333v47.333H.001zM52.667 53.596H100v47.333H52.667zM52.667 26.929H74v21.333H52.667zM52.667.929H74v21.333H52.667zM78.667 26.929H100v21.333H78.667zM78.667 13.596h8.667v8.667h-8.667zM78.667.929h8.667v8.667h-8.667zM91.335 13.596h8.667v8.667h-8.667zM91.335.929h8.667v8.667h-8.667zM0 .929h47.333v47.333H0z"}))}var v2=null;function g2(e){return React66.createElement("svg",o({viewBox:"0 0 101 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React66.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M62.467 36.689c5.566-3.544 9.253-9.73 9.253-16.769C71.72 8.92 62.713 0 51.603 0c-8.12 0-15.118 4.766-18.295 11.627a17.717 17.717 0 00-15.593-9.231C7.942 2.396.02 10.241.02 19.919c0 7.906 5.286 14.589 12.55 16.77C5.296 38.874 0 45.565 0 53.48c0 8.41 5.977 15.439 13.954 17.146-5.396 1.6-9.329 6.554-9.329 12.419 0 7.158 5.86 12.96 13.089 12.96s13.089-5.802 13.089-12.96c0-5.865-3.933-10.819-9.33-12.419a17.725 17.725 0 0011.834-8.813 20.078 20.078 0 007.207 8.31c-3.692 3.111-6.034 7.745-6.034 12.92 0 9.365 7.667 16.957 17.124 16.957 9.457 0 17.123-7.592 17.123-16.956 0-5.176-2.342-9.81-6.033-12.92 4.51-2.953 7.75-7.655 8.733-13.13 1.583 6.234 7.282 10.85 14.069 10.85 8.011 0 14.505-6.431 14.505-14.364 0-7.934-6.494-14.365-14.505-14.365-6.787 0-12.486 4.616-14.069 10.85-1-5.566-4.332-10.334-8.96-13.276zm-29.16 8.458a20.083 20.083 0 017.433-8.458 20.063 20.063 0 01-7.433-8.477A17.705 17.705 0 0122.86 36.69a17.725 17.725 0 0110.447 8.457zM59.671 19.92c0 4.413-3.612 7.99-8.069 7.99-4.456 0-8.069-3.577-8.069-7.99s3.613-7.99 8.07-7.99c4.456 0 8.069 3.577 8.069 7.99zm4.036 33.56c0 6.619-5.42 11.985-12.104 11.985-6.685 0-12.104-5.366-12.104-11.986 0-6.619 5.42-11.985 12.104-11.985 6.685 0 12.104 5.366 12.104 11.986zm-41.96.001c0 2.207-1.806 3.995-4.034 3.995-2.228 0-4.034-1.788-4.034-3.995 0-2.206 1.806-3.995 4.034-3.995 2.228 0 4.035 1.789 4.035 3.995zm61.309 29.562c0-1.335 1.092-2.416 2.44-2.416 1.347 0 2.439 1.081 2.439 2.416 0 1.334-1.092 2.415-2.44 2.415-1.347 0-2.44-1.081-2.44-2.415zm2.44-10.37c-5.784 0-10.472 4.643-10.472 10.37 0 5.726 4.688 10.368 10.471 10.368s10.472-4.642 10.472-10.368c0-5.727-4.689-10.37-10.472-10.37zm.345-55.186c-1.347 0-2.44 1.081-2.44 2.416 0 1.334 1.093 2.415 2.44 2.415s2.44-1.081 2.44-2.415c0-1.335-1.093-2.416-2.44-2.416zm-10.47 2.416c0-5.727 4.687-10.37 10.47-10.37s10.471 4.643 10.471 10.37c0 5.726-4.688 10.368-10.47 10.368-5.784 0-10.472-4.642-10.472-10.368zM44.52 83.043c0-3.873 3.171-7.014 7.084-7.014 3.912 0 7.084 3.14 7.084 7.015 0 3.874-3.172 7.014-7.084 7.014-3.913 0-7.084-3.14-7.084-7.014zm-26.806-3.018c-1.684 0-3.05 1.352-3.05 3.02 0 1.667 1.366 3.02 3.05 3.02 1.684 0 3.05-1.353 3.05-3.02 0-1.668-1.366-3.02-3.05-3.02zm-6.398-60.106c0-3.5 2.865-6.337 6.4-6.337 3.533 0 6.398 2.837 6.398 6.337 0 3.5-2.865 6.337-6.399 6.337s-6.399-2.837-6.399-6.337zm74.18 27.15c-3.576 0-6.474 2.87-6.474 6.41 0 3.541 2.898 6.411 6.474 6.411 3.575 0 6.474-2.87 6.474-6.41 0-3.541-2.899-6.411-6.474-6.411zM27.397 53.48c0 5.296-4.335 9.589-9.683 9.589-5.347 0-9.682-4.293-9.682-9.589 0-5.295 4.335-9.588 9.682-9.588 5.348 0 9.683 4.293 9.683 9.588z",fill:"currentColor"}))}var p2=null;function f2(e){return React67.createElement("svg",o({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React67.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M48 8.727C26.31 8.727 8.727 26.31 8.727 48c0 6.558 1.608 12.74 4.45 18.175a35.829 35.829 0 01-.462-5.749c0-19.647 15.927-35.573 35.574-35.573 19.646 0 35.573 15.926 35.573 35.573 0 1.395-.08 2.77-.236 4.123a39.123 39.123 0 003.647-16.55C87.273 26.31 69.69 8.728 48 8.728zm.708 78.539c.328-.006.655-.016.98-.03a27 27 0 001.832-.156c6.84-1.128 12.056-7.069 12.056-14.227 0-7.964-6.456-14.42-14.42-14.42-7.964 0-14.42 6.456-14.42 14.42 0 7.814 6.215 14.176 13.972 14.413zM26.177 75.655a23.374 23.374 0 01-.168-2.802c0-12.784 10.363-23.148 23.147-23.148 12.648 0 22.928 10.145 23.144 22.742a26.734 26.734 0 002.835-12.02c0-14.828-12.02-26.847-26.846-26.847-14.827 0-26.847 12.02-26.847 26.846a26.722 26.722 0 004.735 15.229zm22.58 20.342a36.51 36.51 0 01-.635.002H48C21.49 96 0 74.51 0 48 0 21.49 21.49 0 48 0s48 21.49 48 48c0 25.236-19.475 45.923-44.216 47.853a23.393 23.393 0 01-3.027.144z",fill:"currentColor"}))}var b2=null;function C2(e){return React68.createElement("svg",o({viewBox:"0 0 100 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React68.createElement("path",{d:"M49.027 25.443a24.514 24.514 0 10-24.513 24.513V25.443h24.513zM75.486 49.956a24.513 24.513 0 10-24.513-24.513h24.513v24.513zM50.973 76.415a24.514 24.514 0 1024.513-24.513v24.513H50.973zM24.514 51.902a24.513 24.513 0 1024.513 24.513H24.514V51.902z",fill:"currentColor"}))}var w2=null;function y2(e){return React69.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React69.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 0h100v100H0V0zm10 10h80v80H10V10zm10 10h60v10H20V20zm30 27h22c-2.57-9.778-11.443-17-22.008-17C39.411 30 30.554 37.222 28 47h22zm0 0c9.389 0 17 7.387 17 16.5S59.389 80 50 80s-17-7.387-17-16.5S40.611 47 50 47z",fill:"currentColor"}))}var E2=null;function z2(e){return React70.createElement("svg",o({viewBox:"0 0 110 111",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React70.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M55 110.929c30.376 0 55-24.624 55-55s-24.624-55-55-55-55 24.624-55 55 24.624 55 55 55zm-6.108-79.595l6.11-24.877 6.09 24.877h-12.2zm-18.63-18.26l7.149 24.595 10.563-6.091-17.711-18.504zm.387 35.831L12.145 31.194l24.595 7.148-6.091 10.563zM5.528 55.93l24.877 6.092V49.82L5.528 55.93zM36.74 73.498l-24.595 7.148L30.65 62.935l6.091 10.563zm-6.477 25.266l17.711-18.503-10.563-6.092-7.148 24.595zm30.83-18.257L55 105.384l-6.109-24.877h12.2zm18.622 18.257L72.567 74.17l-10.563 6.092 17.711 18.503zm-.383-35.829l18.503 17.711-24.595-7.148 6.092-10.563zm25.121-7.005l-24.877-6.11v12.202l24.877-6.092zM73.24 38.342l24.595-7.148-18.503 17.711-6.092-10.563zm6.475-25.268L62.004 31.578l10.563 6.091 7.148-24.595zM52.271 44.978l2.73-11.092 2.71 11.091h-5.44zm-8.293-8.136l3.187 10.95 4.7-2.71-7.887-8.24zm.177 15.953l-8.24-7.888 10.951 3.187-2.711 4.7zm-11.198 3.134l11.092 2.712V53.2l-11.092 2.728zm13.91 7.816l-10.952 3.187 8.24-7.888 2.711 4.7zm-2.889 11.252l7.888-8.24-4.7-2.711-3.188 10.95zm13.734-8.12L55 77.951l-2.728-11.074h5.44zm8.293 8.12l-3.187-10.951-4.7 2.711 7.887 8.24zm-.18-15.953l8.24 7.888-10.95-3.187 2.71-4.7zm11.202-3.115L65.953 53.2v5.44l11.074-2.71zm-13.912-7.835l10.95-3.187-8.24 7.888-2.71-4.7zm2.89-11.252l-7.888 8.24 4.701 2.71 3.187-10.95z",fill:"currentColor"}))}var x2=null;function $2(e){return React71.createElement("svg",o({viewBox:"0 0 134 134",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React71.createElement("path",{d:"M64.657 63.942L19.983 19.267l-.708.707 44.708 44.708L9.227 33.067l-.5.866L63.4 65.5h-.063L2.407 49.176l-.26.966L59.475 65.5H0v3h55.604L1.889 82.89l.776 2.898 53.719-14.391L8.227 99.2l1.5 2.598 48.184-27.82-39.343 39.343.709.708-.002.001.708.708v-.002l.707.706 39.298-39.299-27.787 48.128 2.598 1.5 27.83-48.202-14.404 53.764 2.898.776L65.5 78.447V134h3V78.395l14.39 53.715.98-.262v.002l.966-.258v-.003l.953-.255-14.392-53.719L99.2 125.772l2.598-1.5-27.803-48.154 39.326 39.325.711-.711.007.007.707-.708-.007-.007.703-.702-39.325-39.326 48.154 27.803 1.5-2.598-48.157-27.804 53.719 14.391.776-2.897L78.395 68.5H134v-3H74.525l57.326-15.358-.259-.966L70.661 65.5h-.064l54.674-31.567-.5-.866-54.697 31.58 44.673-44.673-.707-.707-44.728 44.728 31.621-54.768-.866-.5-31.576 54.69 16.345-61.01-.966-.26L67.5 63.252V0h-1v63.15L50.157 2.148l-.966.258 16.368 61.098L33.933 8.727l-.866.5 31.59 54.715z",fill:"currentColor"}))}var R2=null;function k2(e){return React72.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React72.createElement("g",{clipPath:"url(#Record_svg__clip0)",fill:"currentColor"},React72.createElement("path",{d:"M79.819 62.343c6.818-16.462-.999-35.334-17.46-42.153-16.463-6.82-35.336.998-42.155 17.46-6.819 16.462.998 35.335 17.46 42.154 16.463 6.819 35.335-.999 42.154-17.46zM53.659 0h-7.303v8.763h7.303V0zM40.498.773l-6.87 1.84 2.268 8.465 6.87-1.84L40.498.772zM28.003 4.978l-5.996 3.46 4.38 7.59 5.996-3.46-4.38-7.59zM17.048 12.274l-4.761 4.76 6.196 6.197 4.761-4.76-6.196-6.197zM8.34 22.174L5.07 27.84l7.588 4.381 3.271-5.666-7.588-4.381zM2.522 33.984L.878 40.121l8.464 2.268 1.644-6.137-8.464-2.268zM8.763 46.926H0v6.163h8.763v-6.163zM9.362 57.697L.898 59.965l1.595 5.953 8.464-2.268-1.595-5.953zM12.806 68.033l-7.589 4.382 2.987 5.173 7.589-4.382-2.987-5.173zM18.811 77.097l-6.196 6.197 4.09 4.09 6.196-6.197-4.09-4.09zM26.969 84.311L22.587 91.9l4.844 2.797 4.382-7.59-4.844-2.796zM36.721 89.14l-2.27 8.464 5.22 1.4 2.27-8.464-5.22-1.4zM52.607 91.237h-5.214V100h5.214v-8.763zM63.083 89.192l-4.839 1.296 2.268 8.464 4.839-1.296-2.268-8.464zM72.698 84.501l-4.173 2.41 4.381 7.59 4.174-2.41-4.382-7.59zM80.772 77.506L77.5 80.78l6.196 6.196 3.274-3.274-6.197-6.196zM86.813 68.694l-2.22 3.845 7.59 4.382 2.22-3.845-7.59-4.382zM90.385 58.633l-1.1 4.105 8.464 2.268 1.1-4.105-8.464-2.268zM100 47.962h-8.763v4.06H100v-4.06zM97.796 35.184l-8.464 2.267 1.002 3.739 8.464-2.268-1.002-3.738zM92.37 23.41l-7.589 4.381 1.84 3.188 7.59-4.382-1.84-3.187zM84.1 13.424l-6.197 6.195 2.467 2.469 6.198-6.195-2.467-2.469zM73.564 5.885l-4.383 7.588 2.858 1.65 4.383-7.587-2.858-1.651zM61.446 1.297l-2.27 8.465 3.005.805 2.27-8.464-3.005-.806z"})),React72.createElement("defs",null,React72.createElement("clipPath",{id:"Record_svg__clip0"},React72.createElement("path",{fill:"#fff",d:"M0 0h100v100H0z"}))))}var M2=null;function L2(e){return React73.createElement("svg",o({viewBox:"0 0 134 134",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React73.createElement("path",{d:"M64.676 50.418L55.95.916l-1.164.207 8.727 49.502c.195-.042.384-.083.58-.119.194-.035.39-.059.584-.088zM44.664 3.828l-1.158.42L60.694 51.48c.378-.153.768-.29 1.158-.42L44.664 3.829zM34.058 8.656l-1.11.644 25.128 43.528c.36-.225.733-.443 1.111-.644L34.058 8.656zM24.444 15.243l-1.022.856L55.73 54.606c.33-.302.668-.586 1.022-.857L24.444 15.243zM16.117 23.403l-.892 1.058L53.73 56.769c.283-.366.579-.715.892-1.058L16.117 23.403zM9.336 32.88l-.715 1.241 43.534 25.135c.225-.425.461-.839.715-1.247L9.336 32.88zM4.295 43.387l-.508 1.394 47.24 17.194c.147-.473.318-.94.507-1.394L4.295 43.387zM1.153 54.606l-.266 1.519 49.502 8.727c.065-.509.153-1.017.266-1.513L1.153 54.606zM0 66.205v1.59h50.27a15.808 15.808 0 010-1.59H0zM50.375 69.076L.867 77.803l.296 1.66 49.508-8.726c-.066-.272-.119-.55-.166-.828a13.631 13.631 0 01-.13-.833zM3.746 89.102l.597 1.636 47.245-17.194a16.817 16.817 0 01-.591-1.636L3.747 89.102zM8.525 99.725l.893 1.548 43.534-25.135a16.699 16.699 0 01-.892-1.548L8.525 99.725zM15.086 109.361l1.182 1.413 38.518-32.32c-.42-.45-.816-.916-1.182-1.406L15.086 109.36zM23.207 117.715l1.448 1.217 32.32-38.518c-.503-.378-.993-.78-1.454-1.211l-32.314 38.512zM32.662 124.54l1.678.969 25.141-43.54c-.579-.29-1.14-.62-1.678-.975l-25.14 43.546zM43.152 129.623l1.873.679 17.2-47.25c-.638-.19-1.264-.42-1.873-.68l-17.2 47.251zM54.36 132.807l2.008.355 8.733-49.52a16.216 16.216 0 01-2.009-.354l-8.733 49.519zM65.951 134h2.092V83.718c-.703.047-1.4.042-2.092 0V134zM68.846 83.646l8.733 49.525 2.109-.372-8.733-49.525c-.343.082-.697.16-1.052.224-.348.06-.703.107-1.057.148zM88.883 130.337l2.063-.751-17.2-47.25c-.662.29-1.353.543-2.062.75l17.2 47.251zM99.528 125.585l1.944-1.123L76.325 80.91a16.63 16.63 0 01-1.944 1.123l25.147 43.552zM109.189 119.063l1.761-1.477-32.326-38.523c-.55.531-1.14 1.022-1.76 1.477l32.325 38.523zM117.575 110.967l1.506-1.796-38.53-32.332a16.83 16.83 0 01-1.506 1.797l38.53 32.331zM124.423 101.539l1.2-2.074-43.558-25.147a16.44 16.44 0 01-1.2 2.074l43.558 25.147zM129.54 91.069l.839-2.299-47.257-17.2c-.224.792-.508 1.56-.839 2.299l47.257 17.2zM132.764 79.867l.431-2.458-49.531-8.733c-.083.839-.23 1.66-.432 2.458l49.532 8.733zM133.999 68.272v-2.546h-50.3c.065.857.065 1.707.006 2.546H134zM83.666 65.383l49.543-8.732-.449-2.559-49.543 8.733a15.696 15.696 0 01.45 2.558zM130.415 45.33l-.904-2.493-47.269 17.205c.36.798.662 1.631.904 2.494l47.269-17.206zM125.7 34.671l-1.353-2.34-43.564 25.153a16.98 16.98 0 011.353 2.34L125.7 34.671zM119.213 24.988l-1.767-2.11-38.542 32.338c.644.65 1.235 1.353 1.773 2.103l38.536-32.331zM111.141 16.573l-2.145-1.802-32.338 38.542a17.328 17.328 0 012.145 1.802l32.338-38.542zM101.732 9.69l-2.47-1.424-25.159 43.576c.863.407 1.69.88 2.47 1.424L101.732 9.69zM74.07 51.817L91.28 4.537l-2.73-.993-17.188 47.227-.011.053c.939.255 1.849.585 2.718.993z",fill:"currentColor"}),React73.createElement("path",{d:"M71.346 50.825l.017-.047 8.728-49.496-2.908-.514-8.662 49.1v.455a16.15 16.15 0 012.825.502z",fill:"currentColor"}),React73.createElement("path",{d:"M71.354 50.825l.011-.053-.017.047c0 .006.006.006.006.006zM68.522 49.868V0h-3.043v50.323a16.573 16.573 0 012.966-.012l.077-.443z",fill:"currentColor"}),React73.createElement("path",{d:"M68.52 50.317v-.449l-.077.444c.024 0 .053.005.077.005z",fill:"currentColor"}))}var H2=null;function _2(e){return React74.createElement("svg",o({viewBox:"0 0 110 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React74.createElement("path",{d:"M55 105c27.615 0 50-22.386 50-50S82.615 5 55 5C27.386 5 5 27.386 5 55s22.386 50 50 50z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React74.createElement("path",{d:"M60.849 5.33c13.693 12.157 22.34 29.89 22.34 49.653 0 19.744-8.63 37.495-22.322 49.652M49.131 5.33c-13.693 12.157-22.34 29.89-22.34 49.653 0 19.744 8.629 37.495 22.322 49.652",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React74.createElement("path",{d:"M97.467 26.024C86.589 36.9 71.58 43.61 54.999 43.61c-16.07 0-30.658-6.307-41.444-16.6M97.467 83.958C86.589 73.08 71.58 66.37 54.999 66.37c-16.07 0-30.658 6.307-41.444 16.6M104.981 55H5M55 104.982V5",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}))}var S2=null;function I2(e){return React75.createElement("svg",o({viewBox:"0 0 110 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React75.createElement("path",{d:"M55 0C24.626 0 0 24.626 0 55s24.626 55 55 55 55-24.626 55-55S85.374 0 55 0zm0 109.525L.49 55 55 .49l54.525 54.525L55 109.525z",fill:"currentColor"}),React75.createElement("path",{d:"M27.923 27.923v54.139H82.06V27.923H27.923zm27.076 52.074c-13.798 0-24.982-11.184-24.982-24.982S41.201 30.032 55 30.032c13.799 0 24.983 11.185 24.983 24.983 0 13.783-11.184 24.982-24.983 24.982z",fill:"currentColor"}))}var B2=null;function V2(e){return React76.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React76.createElement("path",{d:"M100 100H0V0h100v100zM10 90h80V10H10v80z",fill:"currentColor"}),React76.createElement("path",{d:"M50.008 39.806L80 54v-9.806L50.008 30 20 44.194V54l30.008-14.194zM80 20H20v10h60V20z",fill:"currentColor"}))}var W2=null;function D2(e){return React77.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React77.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 0h100v100H0V0zm32.854 35.063L10.163 10h79.674L67.146 35.063h22.691L63.96 53.295h25.877L61.804 66.97h28.033l-25.895 9.357h25.895l-23.902 6.477h23.902L50 90l-39.837-7.197h23.902l-23.902-6.477h25.895l-25.895-9.357h28.033L10.163 53.295H36.04L10.163 35.063h22.691z",fill:"currentColor"}))}var O2=null;function A2(e){return React78.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React78.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M100 0H0v100h100V0zM10 17.071V90h72.929L64.594 71.665v8.412h-10V54.594h25.434v10h-8.363L90 82.929V10H17.071l18.43 18.43.07-8.546 9.999.08-.204 25.443H19.973v-10h8.363L10 17.07zm19.745 37.701h-10v25.483H45.18v-10h-8.365l33.44-33.452v8.425h10V19.745H54.822v10h8.35L29.745 63.18v-8.409z",fill:"currentColor"}))}var P2=null;function F2(e){return React79.createElement("svg",o({viewBox:"0 0 110 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React79.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M50.028 9.658C27.178 12.136 9.39 31.491 9.39 55c0 8.832 2.51 17.078 6.857 24.063-2.302-8.325-2.151-17.035.801-24.035l-.015-.03.245-.498a25.44 25.44 0 01.81-1.65c6.717-13.595 20.721-22.947 36.91-22.948 12.318-.013 23.354 5.414 30.887 13.98.329-5.954-1.19-12.893-4.87-19.106-5.552-9.378-15.74-16.548-30.987-15.116v-.002zm42.655 45.894l.272-.551-.017-.034c2.956-7.012 3.1-15.739.787-24.075A45.397 45.397 0 01100.61 55c0 23.515-17.795 42.873-40.654 45.344v-.004c-15.246 1.431-25.435-5.739-30.987-15.117-3.678-6.212-5.198-13.148-4.87-19.102 7.534 8.562 18.582 13.976 30.902 13.976 16.2 0 30.185-9.394 36.896-22.95.28-.52.542-1.052.786-1.595zM55 0C24.624 0 0 24.624 0 55s24.624 55 55 55 55-24.624 55-55S85.376 0 55 0zm27.39 54.998c-3.929-6.688-10.221-11.812-17.719-14.21 4.53 3.092 7.504 8.297 7.504 14.195 0 5.93-3.012 11.157-7.582 14.243 7.533-2.393 13.855-7.527 17.798-14.228zM27.592 55c3.927-6.69 10.223-11.806 17.728-14.205-4.525 3.093-7.494 8.294-7.494 14.188 0 5.934 3.01 11.165 7.585 14.25C37.858 66.845 31.527 61.71 27.591 55zM55 47.198a7.785 7.785 0 000 15.57c4.287 0 7.784-3.49 7.784-7.785A7.785 7.785 0 0055 47.198z",fill:"currentColor"}))}var T2=null;function Z2(e){return React80.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React80.createElement("g",{clipPath:"url(#Share_with_Your_Team_(Team_Library)_svg__clip0)",fill:"currentColor"},React80.createElement("path",{d:"M33.33 24.946V8.384L24.946 0v24.946H0l8.384 8.384H33.33v-8.384zM58.286 33.33h8.385V8.384L58.286 0v24.946H33.331l8.394 8.384h16.561z"}),React80.createElement("path",{d:"M100 8.384L91.614 0v24.946H66.67l8.385 8.384H100V8.384zM33.33 58.286V41.724l-8.384-8.394v24.956H0l8.384 8.384H33.33v-8.384zM33.33 58.286l8.395 8.384H66.67V41.724l-8.385-8.394v24.956H33.331zM66.67 58.286l8.384 8.384H100V41.724l-8.385-8.394v24.956H66.67zM24.946 66.67v24.946H0L8.384 100H33.33V75.054l-8.384-8.384zM58.286 66.67v24.946H33.331L41.725 100H66.67V75.054l-8.385-8.384zM66.67 91.616L75.053 100h24.945V75.054l-8.384-8.384v24.946H66.67z"})),React80.createElement("defs",null,React80.createElement("clipPath",{id:"Share_with_Your_Team_(Team_Library)_svg__clip0"},React80.createElement("path",{fill:"#fff",d:"M0 0h100v100H0z"}))))}var j2=null;function N2(e){return React81.createElement("svg",o({viewBox:"0 0 101 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React81.createElement("path",{fill:"currentColor",d:"M.001 52.667h47.333V100H.001zM52.667 52.667H100V100H52.667zM52.667 26H74v21.333H52.667zM52.667 0H74v21.333H52.667zM78.667 26H100v21.333H78.667zM78.667 12.667h8.667v8.667h-8.667zM78.667 0h8.667v8.667h-8.667zM91.335 12.667h8.667v8.667h-8.667zM91.335 0h8.667v8.667h-8.667zM0 0h47.333v47.333H0z"}))}var U2=null;function K2(e){return React82.createElement("svg",o({viewBox:"0 0 100 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React82.createElement("path",{d:"M34.27 50.002v15.73H50c-8.69 0-15.73-7.04-15.73-15.73zM65.73 50.002v-15.73H50c8.69 0 15.73 7.04 15.73 15.73zM50 34.272H34.27v15.73c0-8.69 7.04-15.73 15.73-15.73z",fill:"currentColor"}),React82.createElement("path",{d:"M50 65.732h15.73v-15.73c0 8.69-7.04 15.73-15.73 15.73z",fill:"currentColor"}),React82.createElement("path",{d:"M0 .002v100h100v-100H0zm81.46 10c3.48 1.79 6.2 4.84 7.57 8.54h-7.57v-8.54zm-15.73 0c6.1 0 11.38 3.47 13.99 8.54H65.73v-8.54zm-15.73 0c6.1 0 11.38 3.47 13.99 8.54H36.01c2.61-5.07 7.89-8.54 13.99-8.54zm-15.73 0v8.54H20.28c2.61-5.07 7.89-8.54 13.99-8.54zm-15.73 80c-3.48-1.79-6.2-4.84-7.57-8.54h7.57v8.54zm0-10.28c-5.07-2.61-8.54-7.89-8.54-13.99h8.54v13.99zm0-15.73c-5.07-2.61-8.54-7.89-8.54-13.99 0-6.1 3.47-11.38 8.54-13.99v27.98zm0-29.72H10c0-6.1 3.47-11.38 8.54-13.99v13.99zm0-15.73h-7.57c1.37-3.7 4.09-6.75 7.57-8.54v8.54zm62.92 71.46v-8.54h7.57c-1.37 3.7-4.09 6.75-7.57 8.54zm0-10.28v-13.99H90c0 6.1-3.47 11.38-8.54 13.99zm0-29.72v-13.99c5.07 2.61 8.54 7.89 8.54 13.99 0 6.1-3.47 11.38-8.54 13.99v-13.99c0 8.69-7.04 15.73-15.73 15.73h15.73c0 8.69-7.04 15.73-15.73 15.73h13.99c-2.61 5.07-7.89 8.54-13.99 8.54v-8.54-15.73c0 8.69-7.04 15.73-15.73 15.73h13.99c-2.61 5.07-7.89 8.54-13.99 8.54-6.1 0-11.38-3.47-13.99-8.54H50c-8.69 0-15.73-7.04-15.73-15.73v24.27c-6.1 0-11.38-3.47-13.99-8.54h13.99c-8.69 0-15.73-7.04-15.73-15.73h15.73c-8.69 0-15.73-7.04-15.73-15.73 0-8.69 7.04-15.73 15.73-15.73H18.54c0-8.69 7.04-15.73 15.73-15.73v15.73c0-8.69 7.04-15.73 15.73-15.73 8.69 0 15.73 7.04 15.73 15.73v-15.73c8.69 0 15.73 7.04 15.73 15.73v-13.99c5.07 2.61 8.54 7.89 8.54 13.99H65.73c8.69 0 15.73 7.04 15.73 15.73z",fill:"currentColor"}))}var G2=null;function Y2(e){return React83.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React83.createElement("path",{d:"M50 70c11.046 0 20-8.954 20-20s-8.954-20-20-20-20 8.954-20 20 8.954 20 20 20z",fill:"currentColor"}),React83.createElement("path",{d:"M31 50V0H0v100h99.999V69H31V50z",fill:"currentColor"}),React83.createElement("path",{d:"M100 66V0H34v31h35v35h31z",fill:"currentColor"}))}var X2=null;function J2(e){return React84.createElement("svg",o({viewBox:"0 0 101 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React84.createElement("path",{d:"M38.963 0C17.45 0 0 18.136 0 40.495v8.507h9.444C30.967 49.002 48 30.41 48 8.05V.002L38.963 0zM100.002 38.965c0-21.513-18.136-38.963-40.495-38.963H51v9.444c0 21.523 18.592 38.556 40.951 38.556H100l.002-9.037zM61.039 100.004c21.513 0 38.963-18.136 38.963-40.495v-8.507h-9.444c-21.523 0-38.556 18.592-38.556 40.951v8.049l9.037.002zM0 61.039c0 21.513 18.136 38.963 40.495 38.963h8.507v-9.444c0-21.523-18.592-38.556-40.952-38.556H.002L0 61.039z",fill:"currentColor"}))}var Q2=null;function q2(e){return React85.createElement("svg",o({viewBox:"0 0 110 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React85.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M55 10c-24.853 0-45 20.147-45 45s20.147 45 45 45 45-20.147 45-45-20.147-45-45-45zM0 55C0 24.624 24.624 0 55 0s55 24.624 55 55-24.624 55-55 55S0 85.376 0 55zm33.8-35.64H76v10H43.8v20.19h11.75v-9.87c14.131 0 25.59 11.459 25.59 25.59S69.681 90.86 55.55 90.86 29.96 79.401 29.96 65.27h10c0 8.609 6.981 15.59 15.59 15.59s15.59-6.981 15.59-15.59c0-8.535-6.863-15.47-15.37-15.588v9.868H33.8V19.36z",fill:"currentColor"}))}var e5=null;function t5(e){return React86.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React86.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M55.666 3h15.333v15.333H55.666V3zm-3 18.333V0h21.333v21.333H52.666zM70.999 29H55.666v15.333h15.333V29zm-18.333-3v21.333h21.333V26H52.666zm-5.333 26.667H0V100h47.333V52.667zm52.666 0H52.666V100h47.333V52.667zM97 29H81.668v15.333H97V29zm-18.332-3v21.333H100V26H78.666zm3-10.333h2.666v2.666h-2.666v-2.666zm-3 5.666v-8.666h8.666v8.666h-8.666zM84.332 3h-2.666v2.667h2.666V3zm-5.666-3v8.667h8.666V0h-8.666zm15.667 15.667h2.667v2.666h-2.667v-2.666zm-3 5.666v-8.666h8.667v8.666h-8.667zM97.001 3h-2.667v2.667h2.667V3zm-5.667-3v8.667h8.667V0h-8.667zm-44 0H0v47.333h47.333V0z",fill:"currentColor"}))}var r5=null;function a5(e){return React87.createElement("svg",o({viewBox:"0 0 106 106",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React87.createElement("path",{d:"M53 101c26.51 0 48-21.49 48-48S79.51 5 53 5 5 26.49 5 53s21.49 48 48 48z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React87.createElement("path",{d:"M53 100.986c26.51 0 48-14.563 48-32.527 0-17.965-21.49-32.528-48-32.528S5 50.494 5 68.46c0 17.964 21.49 32.527 48 32.527z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React87.createElement("path",{d:"M53 100.998c26.51 0 48-8.682 48-19.39 0-10.71-21.49-19.391-48-19.391S5 70.898 5 81.607c0 10.71 21.49 19.391 48 19.391z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React87.createElement("path",{d:"M53 100.984c26.51 0 48-3.908 48-8.728S79.51 83.53 53 83.53 5 87.436 5 92.256s21.49 8.728 48 8.728z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}))}var l5=null;function n5(e){return React88.createElement("svg",o({viewBox:"0 0 111 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React88.createElement("path",{d:"M.223 57.064l-.208-.356a55.069 55.069 0 002.244 13.991l44.404-40.904-46.44 27.27zM3.27 73.804C10.953 94.924 31.208 110 55 110c23.926 0 44.285-15.269 51.865-36.582l-51.582-47.53L3.27 73.804zm88.867-9.358v24.36L64.838 63.584v39.003a1.49 1.49 0 01-1.486 1.486H47.287a1.49 1.49 0 01-1.486-1.486V63.585l-27.388 25.22V64.446l36.914-33.983 36.81 33.983zM107.861 70.299a54.916 54.916 0 002.125-13.442L63.873 29.78 107.861 70.3zM63.115 25.873l46.886 27.537c-.148-5.228-1.01-10.293-2.526-15.06l-44.36-12.477zM2.482 38.543C.966 43.356.119 48.465 0 53.753l47.436-27.864L2.482 38.543z",fill:"currentColor"}),React88.createElement("path",{d:"M106.241 34.934C98.216 14.482 78.302 0 55.001 0 31.625 0 11.68 14.57 3.7 35.112l51.582-14.511 50.958 14.333z",fill:"currentColor"}))}var o5=null;function i5(e){return React89.createElement("svg",o({viewBox:"0 0 104 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React89.createElement("path",{d:"M98.75 100.001c0-25.889-20.986-46.876-46.874-46.876C25.987 53.125 5 74.112 5 100.001",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React89.createElement("path",{d:"M16.704 100.001c0-19.416 15.74-35.171 35.172-35.171 19.43 0 35.171 15.74 35.171 35.171",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React89.createElement("path",{d:"M28.213 100.001c0-13.07 10.593-23.648 23.648-23.648 13.054 0 23.662 10.579 23.662 23.648",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React89.createElement("path",{d:"M39.736 100c0-6.692 5.432-12.124 12.124-12.124 6.693 0 12.124 5.432 12.124 12.124M5 0c0 25.889 20.987 46.875 46.875 46.875C77.764 46.875 98.751 25.89 98.751 0",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React89.createElement("path",{d:"M87.047 0c0 19.416-15.74 35.171-35.172 35.171-19.43 0-35.171-15.74-35.171-35.171",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React89.createElement("path",{d:"M75.538 0c0 13.07-10.593 23.648-23.648 23.648-13.054 0-23.662-10.579-23.662-23.648",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React89.createElement("path",{d:"M64.015 0c0 6.693-5.432 12.124-12.124 12.124S39.767 6.693 39.767.002",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}))}var s5=null;function c5(e){return React90.createElement("svg",o({viewBox:"0 0 110 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React90.createElement("path",{d:"M5 55h99.984c0 27.61-22.375 50-50 50S5 82.61 5 55z",fill:"currentColor",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React90.createElement("path",{d:"M55 105c27.614 0 50-22.386 50-50S82.614 5 55 5 5 27.386 5 55s22.386 50 50 50z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React90.createElement("path",{d:"M23.534 55C23.534 37.62 37.62 23.534 55 23.534c17.382 0 31.466 14.085 31.466 31.466",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React90.createElement("path",{d:"M42.053 55c0-7.138 5.794-12.932 12.932-12.932 7.138 0 12.932 5.794 12.932 12.932",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}))}var d5=null;function u5(e){return React91.createElement("svg",o({viewBox:"0 0 100 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React91.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M100 .929H0v100h100v-100zm-54.528 18.32v4.298l9.051-4.299h-9.05zm0 14.937v-5.883h9.051l-9.05 5.883zm0 3.166v7.467l9.051-7.467h-9.05zm0 18.1V46.4h9.051l-9.05 9.05zm0 1.586v7.467l9.051-7.467h-9.05zm0 16.517v-5.883h9.051l-9.05 5.883zm0 4.75v4.3l9.051-4.3h-9.05zM88.01 91.66v-2.715h2.715l-2.715 2.715zm0-13.354v4.3l2.715-4.3H88.01zm0-4.75v-5.883h2.715l-2.715 5.883zm0-16.517v7.467l2.715-7.467H88.01zm0-1.586V46.4h2.715l-2.715 9.05zm0-18.1v7.467l2.715-7.467H88.01zm0-3.166v-5.883h2.715l-2.715 5.883zm0-14.938v4.3l2.715-4.3H88.01zm0-6.334V10.2h2.715l-2.715 2.716zm-10.633 76.03v2.715l4.3-2.715h-4.3zm0-6.34v-4.299h4.3l-4.3 4.3zm0-14.932v5.883l4.3-5.883h-4.3zm0-3.167v-7.467h4.3l-4.3 7.467zm0-18.104v9.05l4.3-9.05h-4.3zm0-1.582v-7.467h4.3l-4.3 7.467zm0-16.516v5.883l4.3-5.883h-4.3zm0-4.756v-4.299h4.3l-4.3 4.3zm0-13.348v2.716l4.3-2.716h-4.3zM66.741 91.66v-2.715h5.883l-5.883 2.715zm0-13.354v4.3l5.883-4.3h-5.883zm0-4.75v-5.883h5.883l-5.883 5.883zm0-16.517v7.467l5.883-7.467h-5.883zm0-1.586V46.4h5.883l-5.883 9.05zm0-18.1v7.467l5.883-7.467h-5.883zm0-3.166v-5.883h5.883l-5.883 5.883zm0-14.938v4.3l5.883-4.3h-5.883zm0-6.334V10.2h5.883l-5.883 2.716zm-10.634 76.03v2.715l7.467-2.715h-7.467zm0-6.339v-4.3h7.467l-7.467 4.3zm0-14.932v5.883l7.467-5.883h-7.467zm0-3.168v-7.467h7.467l-7.467 7.467zm0-18.104v9.051l7.467-9.05h-7.467zm0-1.582v-7.467h7.467l-7.467 7.467zm0-16.516v5.883l7.467-5.883h-7.467zm0-4.755v-4.3h7.467l-7.467 4.3zm.001-13.348v2.715l7.467-2.715h-7.467zm-10.636 2.715v-2.716h9.051l-9.05 2.716zm-9.051 76.029v2.715l7.467-2.715H36.42zm0-6.34v-4.299h7.467l-7.467 4.3zm0-14.932v5.883l7.467-5.883H36.42zm0-3.167v-7.467h7.467l-7.467 7.467zm0-18.104v9.05l7.467-9.05H36.42zm0-1.582v-7.467h7.467l-7.467 7.467zm0-16.516v5.883l7.467-5.883H36.42zm0-4.756v-4.299h7.467l-7.467 4.3zm0-13.348v2.716l7.467-2.716H36.42zm-9.05 81.46v-2.715h5.883l-5.883 2.715zm0-13.354v4.3l5.883-4.3h-5.883zm0-4.75v-5.883h5.883l-5.883 5.883zm0-16.517v7.467l5.883-7.467h-5.883zm0-1.586V46.4h5.883l-5.883 9.05zm0-18.1v7.467l5.883-7.467h-5.883zm0-3.166v-5.883h5.883l-5.883 5.883zm0-14.938v4.3l5.883-4.3h-5.883zm0-6.334V10.2h5.883l-5.883 2.716zm-9.05 76.03v2.715l4.299-2.715h-4.3zm0-6.34v-4.299h4.299l-4.3 4.3zm0-14.932v5.883l4.299-5.883h-4.3zm0-3.167v-7.467h4.299l-4.3 7.467zm0-18.104v9.05l4.299-9.05h-4.3zm0-1.582v-7.467h4.299l-4.3 7.467zm0-16.516v5.883l4.299-5.883h-4.3zm0-4.756v-4.299h4.299l-4.3 4.3zm0-13.348v2.716l4.299-2.716h-4.3zm27.151 81.46v-2.715h9.051l-9.05 2.715zM9.27 88.944v2.715l2.715-2.715H9.27zm0-6.34v-4.299h2.715l-2.715 4.3zm0-14.932v5.883l2.715-5.883H9.27zm0-3.167v-7.467h2.715L9.27 64.505zm0-18.104v9.05l2.715-9.05H9.27zm0-1.582v-7.467h2.715L9.27 44.819zm0-16.516v5.883l2.715-5.883H9.27zm0-4.756v-4.299h2.715l-2.715 4.3zm0-13.348v2.715l2.716-2.715H9.268z",fill:"currentColor"}))}var h5=null;function m5(e){return React92.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React92.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M100 100H0V0h100v100zM67.146 64.937L89.837 90H10.163l22.691-25.063H10.163L36.04 46.705H10.163L38.196 33.03H10.163l25.895-9.357H10.163l23.902-6.477H10.163L50 10l39.837 7.197H65.935l23.902 6.477H63.942l25.895 9.357H61.804l28.033 13.674H63.96l25.877 18.232H67.146z",fill:"currentColor"}))}var v5=null;function g5(e){return React93.createElement("svg",o({viewBox:"0 0 110 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React93.createElement("path",{d:"M61.125 97.536H48.768v12.373h12.357V97.536zM81.608 88.743l-10.701 6.179 6.186 10.714 10.701-6.178-6.186-10.715zM94.92 70.897l-6.178 10.7 10.715 6.187 6.178-10.701-10.714-6.186zM89.445 61.127V48.77H78.014l9.91-5.724-6.178-10.71-9.895 5.724 5.724-9.895-10.71-6.179-5.724 9.895V20.45H48.769V31.88l-5.724-9.895-10.71 6.179 5.723 9.91-9.91-5.723-6.179 10.71 9.91 5.724H20.45v12.356h11.43l-9.91 5.724 6.179 10.71 9.91-5.723-5.723 9.91 10.71 6.178 5.724-9.91v11.431h12.356V78.032l5.724 9.91 10.71-6.178-5.724-9.895 9.895 5.724 6.179-10.71-9.91-5.724h11.447v-.031zM54.947 71.413c-9.095 0-16.465-7.37-16.465-16.465 0-9.095 7.37-16.465 16.465-16.465 9.095 0 16.465 7.37 16.465 16.465 0 9.095-7.37 16.465-16.465 16.465zM109.91 48.77H97.538v12.356h12.372V48.77zM99.46 22.114l-10.714 6.187L94.925 39l10.714-6.186-6.178-10.7zM77.082 4.276L70.896 14.99l10.701 6.179 6.186-10.715-10.7-6.178zM61.125 0H48.768v12.373h12.357V0zM32.825 4.281L22.124 10.46l6.186 10.714 10.701-6.178-6.186-10.715zM10.449 22.127L4.27 32.828l10.714 6.186 6.178-10.7-10.714-6.187zM12.373 48.77H0v12.356h12.373V48.77zM14.99 70.881L4.274 77.067l6.178 10.701 10.715-6.186-6.179-10.7zM28.311 88.746L22.125 99.46l10.701 6.179 6.186-10.715-10.7-6.178z",fill:"currentColor"}))}var p5=null;function f5(e){return React94.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React94.createElement("path",{d:"M100 38.086V0H61.914v9.93h21.132L54.963 38.013V16.88h-9.93v21.132L16.951 9.93h21.135V0H0v38.086h9.93V16.951l28.083 28.082H16.88v9.93h21.132L9.93 83.046V61.914H0V100h38.086v-9.93H16.951l28.082-28.086v21.135h9.93V61.984L83.046 90.07H61.914V100H100V61.914h-9.93v21.132L61.987 54.963H83.12v-9.93H61.987L90.07 16.951v21.135H100z",fill:"currentColor"}))}var b5=null;function C5(e){return React95.createElement("svg",o({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React95.createElement("path",{d:"M0 0v100h100V0H0zm90 90H61.91l20.87-12.52L90 89.52V90zm0-71.25H29.01L90 26.56v8.82l-42.3-5.42L90 42.3v9.12l-27.61-8.05L90 56.78v9.73l-15.29-7.42L90 71.34v11.22L76.02 71.35 61.06 90H49.84l24.82-30.94-8.62-4.19L48.98 90h-9.73l22.71-46.76-9.21-2.68L38.34 90h-9.12l17.53-60.15-10.48-1.35L28.4 90h-8.82l9.12-71.25h-9.94V90H10V10h80v8.75z",fill:"currentColor"}))}var w5=null;function y5(e){return React96.createElement("svg",o({viewBox:"0 0 134 134",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React96.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M67.59 60.288V0h-1.175v60.292L55.941.914l-1.157.204 10.474 59.374L44.636 3.841l-1.104.401 20.622 56.651L34.01 8.681l-1.017.588 30.144 52.213-38.752-46.184-.9.755 38.753 46.185-46.185-38.752-.755.9 46.184 38.752L9.27 32.993 8.68 34.01l52.212 30.144-56.65-20.622-.403 1.104 56.652 20.622L1.118 54.785l-.204 1.157 59.377 10.473H0v1.175h60.288L.914 78.058l.204 1.157 59.374-10.468L3.84 89.364l.402 1.104 56.651-20.617L8.681 99.99l.588 1.017 52.213-30.14-46.184 38.747.755.9 46.186-38.747-38.753 46.18.9.755 38.751-46.178-30.144 52.207 1.017.588 30.144-52.207-20.622 56.645 1.104.402 20.622-56.646-10.473 59.369 1.156.204 10.474-59.373V134h1.175V73.717l10.468 59.369 1.157-.204-10.468-59.37 20.617 56.647 1.104-.401-20.617-56.646 30.139 52.206 1.017-.587-30.14-52.208 38.747 46.179.9-.755-38.747-46.18 46.18 38.747.755-.9-46.179-38.746 52.208 30.139.588-1.017L73.112 69.85l56.646 20.617.401-1.104-56.646-20.617 59.369 10.468.204-1.157-59.37-10.468H134v-1.175H73.714l59.372-10.474-.204-1.156-59.369 10.473 56.646-20.622-.401-1.104-56.646 20.622 52.207-30.144-.588-1.017-52.208 30.144 46.179-38.752-.755-.9-46.18 38.753 38.747-46.185-.9-.755-38.746 46.184L101.007 9.27 99.99 8.68 69.85 60.893l20.617-56.65-1.104-.402-20.617 56.651L79.215 1.118 78.058.914 67.59 60.288z",fill:"currentColor"}))}var E5=null;function z5(e){return React97.createElement("svg",o({viewBox:"0 0 100 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React97.createElement("path",{d:"M66.667.929a33.333 33.333 0 010 66.666V.93zM0 34.263a33.333 33.333 0 0166.667 0H0zM33.333 100.929a33.338 33.338 0 01-23.57-9.763 33.333 33.333 0 0123.57-56.903v66.666z",fill:"currentColor"}),React97.createElement("path",{d:"M99.999 67.596a33.332 33.332 0 01-64.13 12.756 33.332 33.332 0 01-2.537-12.756h66.667zM33.334.93H.001v33.333h33.333z",fill:"currentColor"}),React97.createElement("path",{fill:"currentColor",d:"M100 67.595H66.667v33.333H100z"}))}var x5=null;function $5(e){return React98.createElement("svg",o({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React98.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M96 0H0v96h96V0zM84 12H12v72h72V12z",fill:"currentColor"}),React98.createElement("path",{fill:"currentColor",d:"M19.2 19.2h57.6v12H19.2zM19.2 38.4h57.6v12H19.2zM19.2 57.6h31.2v12H19.2z"}))}var R5=null;function k5(e){return React99.createElement("svg",o({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React99.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 67.2V96h96V0H67.2v67.2H0z",fill:"currentColor"}),React99.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 28.8V60h28.8V28.8H60V0H0v28.8z",fill:"currentColor"}))}var M5=null;function L5(e){return React100.createElement("svg",o({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React100.createElement("path",{d:"M22.8 12c5.965 0 10.8 4.835 10.8 10.8 0 .254-.008.505-.026.754C38.542 16.58 46.912 12 56.4 12 71.643 12 84 23.82 84 38.4c0 14.58-12.357 26.4-27.6 26.4-5.744 0-11.078-1.678-15.496-4.55A15.527 15.527 0 0143.2 68.4c0 8.616-6.984 15.6-15.6 15.6C18.985 84 12 77.016 12 68.4s6.985-15.6 15.6-15.6c2.444 0 4.757.562 6.816 1.564C30.892 49.93 28.8 44.399 28.8 38.4c0-2.6.393-5.11 1.125-7.483A10.76 10.76 0 0122.8 33.6c-5.964 0-10.8-4.835-10.8-10.8C12 16.835 16.836 12 22.8 12z",fill:"currentColor"}),React100.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 0h96v96H0V0zm12 12v72h72V12H12z",fill:"currentColor"}))}var H5=null;function _5(e){return React101.createElement("svg",o({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React101.createElement("path",{d:"M96 0H0v96h96V0zM84 12v72H12V12h72z",fill:"currentColor"}),React101.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M85.023 48.341L48.341 11.66 11.66 48.341 48.34 85.023l36.682-36.682zm-56.69 0L48.34 28.333 28.333 48.34zm20.842 19.175L68.35 48.34 49.175 29.167v38.349z",fill:"currentColor"}))}var S5=null;function I5(e){return React102.createElement("svg",o({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React102.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 0h96v28.704H47.844V12L12 48l35.844 36V67.305H96V96H0V0z",fill:"currentColor"}))}var B5=null;function V5(e){return React103.createElement("svg",o({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React103.createElement("circle",{cx:15.84,cy:15.84,r:11.04,stroke:"currentColor",strokeWidth:9.6}),React103.createElement("path",{d:"M59.52 15.84c0 5.963-5.022 11.04-11.52 11.04-6.498 0-11.52-5.077-11.52-11.04C36.48 9.877 41.502 4.8 48 4.8c6.498 0 11.52 5.077 11.52 11.04z",stroke:"currentColor",strokeWidth:9.6}),React103.createElement("circle",{cx:80.16,cy:15.84,r:15.84,fill:"currentColor"}),React103.createElement("path",{d:"M26.88 48c0 6.498-5.077 11.52-11.04 11.52C9.877 59.52 4.8 54.498 4.8 48c0-6.498 5.077-11.52 11.04-11.52 5.963 0 11.04 5.022 11.04 11.52z",stroke:"currentColor",strokeWidth:9.6}),React103.createElement("circle",{cx:48,cy:48,r:11.52,stroke:"currentColor",strokeWidth:9.6}),React103.createElement("path",{d:"M91.2 48c0 6.498-5.077 11.52-11.04 11.52-5.963 0-11.04-5.022-11.04-11.52 0-6.498 5.077-11.52 11.04-11.52 5.963 0 11.04 5.022 11.04 11.52z",stroke:"currentColor",strokeWidth:9.6}),React103.createElement("circle",{cx:15.84,cy:80.16,r:11.04,stroke:"currentColor",strokeWidth:9.6}),React103.createElement("path",{d:"M59.52 80.16c0 5.963-5.022 11.04-11.52 11.04-6.498 0-11.52-5.077-11.52-11.04 0-5.963 5.022-11.04 11.52-11.04 6.498 0 11.52 5.077 11.52 11.04z",stroke:"currentColor",strokeWidth:9.6}),React103.createElement("circle",{cx:80.16,cy:80.16,r:11.04,stroke:"currentColor",strokeWidth:9.6}))}var W5=null}}]);

//# sourceMappingURL=6217.js.map