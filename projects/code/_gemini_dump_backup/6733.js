"use strict";(global.webpackChunk_loomhq_desktop_monorepo=global.webpackChunk_loomhq_desktop_monorepo||[]).push([[6733,3780,1994,7557,4460,5810,9724],{862953:(me,A,g)=>{var z;z={value:!0},A.Z=void 0;var R=n(g(275271)),K=n(g(774586));function n(D){return D&&D.__esModule?D:{default:D}}const h=D=>R.default.createElement(K.default,Object.assign({dangerouslySetGlyph:'<path fill="currentcolor" fill-rule="evenodd" d="M7 2.5a4.5 4.5 0 1 0 0 9 4.5 4.5 0 0 0 0-9M1 7a6 6 0 1 1 10.74 3.68l3.29 3.29-1.06 1.06-3.29-3.29A6 6 0 0 1 1 7" clip-rule="evenodd"/>'},D));h.displayName="SearchIcon";var de=A.Z=h},85128:(me,A,g)=>{var z;z={value:!0},A.Z=void 0;var R=n(g(275271)),K=n(g(774586));function n(D){return D&&D.__esModule?D:{default:D}}const h=D=>R.default.createElement(K.default,Object.assign({dangerouslySetGlyph:'<path fill="currentcolor" fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m12.326-2.52-1.152-.96L6.75 9.828 4.826 7.52l-1.152.96 2.5 3a.75.75 0 0 0 1.152 0z" clip-rule="evenodd"/>'},D));h.displayName="SuccessIcon";var de=A.Z=h},249640:(me,A,g)=>{var z;z={value:!0},A.Z=void 0;var R=n(g(275271)),K=n(g(774586));function n(D){return D&&D.__esModule?D:{default:D}}const h=D=>R.default.createElement(K.default,Object.assign({dangerouslySetGlyph:'<path fill="currentcolor" fill-rule="evenodd" d="M2 4a.5.5 0 0 0-.5.5v7a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5v-7A.5.5 0 0 0 10 4zm-2 .5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v.218l2.137-1.203A1.25 1.25 0 0 1 16 4.605v6.79a1.25 1.25 0 0 1-1.863 1.09L12 11.282v.218a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm12 5.061 2.5 1.407V5.032L12 6.44z" clip-rule="evenodd"/>'},D));h.displayName="VideoIcon";var de=A.Z=h},450630:(me,A,g)=>{g.d(A,{Ni:()=>n.T,Xn:()=>n.w,iv:()=>fe.Z,xB:()=>W,F4:()=>S});var z=g(908866),R=g(275271),K=g(117267),n=g(156052),h=g(908308),de=g(586997),D=g(853434),fe=g(669957),He=function(k,_){var H=arguments;if(_==null||!hasOwnProperty.call(_,"css"))return createElement.apply(void 0,H);var V=H.length,j=new Array(V);j[0]=Emotion,j[1]=createEmotionProps(k,_);for(var J=2;J<V;J++)j[J]=H[J];return createElement.apply(null,j)},ve=!1,W=(0,n.w)(function(T,k){var _=T.styles;if(typeof _=="function")return(0,R.createElement)(n.T.Consumer,null,function(V){var j=(0,de.O)([_(V)]);return(0,R.createElement)(M,{serialized:j,cache:k})});var H=(0,de.O)([_]);return(0,R.createElement)(M,{serialized:H,cache:k})}),M=function(T){(0,z.Z)(k,T);function k(H,V,j){return T.call(this,H,V,j)||this}var _=k.prototype;return _.componentDidMount=function(){this.sheet=new D.m({key:this.props.cache.key+"-global",nonce:this.props.cache.sheet.nonce,container:this.props.cache.sheet.container});var V=document.querySelector("style[data-emotion-"+this.props.cache.key+'="'+this.props.serialized.name+'"]');V!==null&&this.sheet.tags.push(V),this.props.cache.sheet.tags.length&&(this.sheet.before=this.props.cache.sheet.tags[0]),this.insertStyles()},_.componentDidUpdate=function(V){V.serialized.name!==this.props.serialized.name&&this.insertStyles()},_.insertStyles=function(){if(this.props.serialized.next!==void 0&&(0,h.M)(this.props.cache,this.props.serialized.next,!0),this.sheet.tags.length){var V=this.sheet.tags[this.sheet.tags.length-1].nextElementSibling;this.sheet.before=V,this.sheet.flush()}this.props.cache.insert("",this.props.serialized,this.sheet,!1)},_.componentWillUnmount=function(){this.sheet.flush()},_.render=function(){return null},k}(R.Component),S=function(){var k=fe.Z.apply(void 0,arguments),_="animation-"+k.name;return{name:_,styles:"@keyframes "+_+"{"+k.styles+"}",anim:1,toString:function(){return"_EMO_"+this.name+"_"+this.styles+"_EMO_"}}},F=function T(k){for(var _=k.length,H=0,V="";H<_;H++){var j=k[H];if(j!=null){var J=void 0;switch(typeof j){case"boolean":break;case"object":{if(Array.isArray(j))J=T(j);else{J="";for(var Ce in j)j[Ce]&&Ce&&(J&&(J+=" "),J+=Ce)}break}default:J=j}J&&(V&&(V+=" "),V+=J)}}return V};function ge(T,k,_){var H=[],V=(0,h.f)(T,H,_);return H.length<2?_:V+k(H)}var oe=function(){return null},be=(0,n.w)(function(T,k){return(0,R.createElement)(n.T.Consumer,null,function(_){var H=!1,V=function(){for(var i=arguments.length,L=new Array(i),E=0;E<i;E++)L[E]=arguments[E];var $e=(0,de.O)(L,k.registered);return(0,h.M)(k,$e,!1),k.key+"-"+$e.name},j=function(){for(var i=arguments.length,L=new Array(i),E=0;E<i;E++)L[E]=arguments[E];return ge(k.registered,V,F(L))},J={css:V,cx:j,theme:_},Ce=T.children(J);H=!0;var Te=(0,R.createElement)(oe,null);return(0,R.createElement)(R.Fragment,null,Te,Ce)})})},819906:(me,A,g)=>{g.d(A,{l:()=>K});var z=g(85128),R=g(275271);function K(){return R.createElement(z.Z,{label:"",testId:"ads-refreshed-icon"})}var n=g(182560)},896542:(me,A,g)=>{g.d(A,{u:()=>R});var z=g(275271);function R(){return z.createElement("span",{"aria-hidden":!0,"data-testid":"ads-refreshed-icon"},z.createElement("svg",{viewBox:"-2 -2 16 16"},z.createElement("path",{fill:"currentColor",fillRule:"evenodd",d:"M2.03 3.97 6 7.94l3.97-3.97 1.06 1.06-4.5 4.5a.75.75 0 0 1-1.06 0l-4.5-4.5z",clipRule:"evenodd"})))}var K=g(182560)},182560:(me,A,g)=>{var z=Object.defineProperty,R=Object.defineProperties,K=Object.getOwnPropertyDescriptors,n=Object.getOwnPropertySymbols,h=Object.prototype.hasOwnProperty,de=Object.prototype.propertyIsEnumerable,D=(ve,W,M)=>W in ve?z(ve,W,{enumerable:!0,configurable:!0,writable:!0,value:M}):ve[W]=M,fe=(ve,W)=>{for(var M in W||(W={}))h.call(W,M)&&D(ve,M,W[M]);if(n)for(var M of n(W))de.call(W,M)&&D(ve,M,W[M]);return ve},He=(ve,W)=>R(ve,K(W))},631915:(me,A,g)=>{g.d(A,{G:()=>K});var z=g(407770),R=g(275271);function K(){return R.createElement(z.Z,{label:"",testId:"ads-refreshed-icon"})}var n=g(182560)},397063:(me,A,g)=>{g.d(A,{M:()=>R});var z=g(275271);function R(){return z.createElement("span",{"aria-hidden":!0,"data-testid":"ads-refreshed-icon"},z.createElement("svg",{viewBox:"0 0 24 24"},z.createElement("path",{d:"M0 6C0 2.68629 2.68629 0 6 0H18C21.3137 0 24 2.68629 24 6V18C24 21.3137 21.3137 24 18 24H6C2.68629 24 0 21.3137 0 18V6Z",fill:"#1868DB"}),z.createElement("path",{d:"M17.8878 14.4612C13.8492 12.5084 12.6693 12.2166 10.9676 12.2166C8.97101 12.2166 7.26933 13.0471 5.74916 15.3815L5.49958 15.7631C5.29538 16.0773 5.25 16.1896 5.25 16.3242C5.25 16.4589 5.31807 16.5712 5.56765 16.7283L8.13151 18.322C8.26765 18.4117 8.38109 18.4566 8.49454 18.4566C8.63067 18.4566 8.72143 18.3893 8.85756 18.1873L9.26597 17.5588C9.90126 16.5936 10.4685 16.2794 11.1945 16.2794C11.8298 16.2794 12.5786 16.4589 13.5088 16.9078L16.1861 18.1648C16.4584 18.2995 16.7534 18.2322 16.8895 17.9179L18.1601 15.1346C18.2962 14.8203 18.2055 14.6183 17.8878 14.4612ZM6.11218 9.54548C10.1508 11.4983 11.3307 11.7901 13.0324 11.7901C15.029 11.7901 16.7307 10.9596 18.2508 8.62518L18.5004 8.2436C18.7046 7.92935 18.75 7.81712 18.75 7.68244C18.75 7.54776 18.6819 7.43553 18.4324 7.27841L15.8685 5.68473C15.7324 5.59494 15.6189 5.55005 15.5055 5.55005C15.3693 5.55005 15.2786 5.61739 15.1424 5.8194L14.734 6.4479C14.0987 7.41309 13.5315 7.72733 12.8055 7.72733C12.1702 7.72733 11.4214 7.54776 10.4912 7.09884L7.81387 5.84185C7.5416 5.70717 7.24664 5.77451 7.1105 6.08876L5.83992 8.87209C5.70378 9.18634 5.79454 9.38836 6.11218 9.54548Z",fill:"white"})))}var K=g(182560)},95376:(me,A,g)=>{g.d(A,{x:()=>K});var z=g(249640),R=g(275271);function K(){return R.createElement(z.Z,{label:"",testId:"ads-refreshed-icon"})}var n=g(182560)},183780:(me,A,g)=>{g.d(A,{ggW:()=>Ge,Ltx:()=>Nl,JO$:()=>ie,hU:()=>$t,TRl:()=>Vo,xvT:()=>Ie,oil:()=>xr,Ut4:()=>Cr});var z=g(738067),R=g(66292),K=g.n(R),n=g(275271),h=g(992671),de=g(485800),D=g(582805),fe=g(66333),He=g(797981),ve=g(773023),W=g(484285),M=g(862953),S=g(12131),F=g(566172),ge=g.n(F),oe=g(407770),be=g(306317),T=g(957530),k=g(230967),_=g(854831),H=Object.defineProperty,V=Object.defineProperties,j=Object.getOwnPropertyDescriptors,J=Object.getOwnPropertySymbols,Ce=Object.prototype.hasOwnProperty,Te=Object.prototype.propertyIsEnumerable,Je=(e,t,a)=>t in e?H(e,t,{enumerable:!0,configurable:!0,writable:!0,value:a}):e[t]=a,i=(e,t)=>{for(var a in t||(t={}))Ce.call(t,a)&&Je(e,a,t[a]);if(J)for(var a of J(t))Te.call(t,a)&&Je(e,a,t[a]);return e},L=(e,t)=>V(e,j(t)),E=(e,t)=>{var a={};for(var r in e)Ce.call(e,r)&&t.indexOf(r)<0&&(a[r]=e[r]);if(e!=null&&J)for(var r of J(e))t.indexOf(r)<0&&Te.call(e,r)&&(a[r]=e[r]);return a},$e=(e,t)=>Math.round(e*t/100),ot=(e,t)=>L(i({},e),{l:e.l-$e(e.l,t)}),Qt=(e,t)=>L(i({},e),{l:e.l+$e(e.l,t)}),vt=(e,t)=>L(i({},e),{s:e.s+$e(e.s,t)}),it=(e,t)=>L(i({},e),{a:t}),va=15.8,ga=31.6,pa=.14,fa=.46,ba=.9,Ca=.8,qt=.25,wa=.06,Ea=.15,ya=.3,za=.45,ye={red:{h:4,s:64,l:48,a:1},blurpleLight:{h:214.3,s:91.3,l:95.5,a:1},blurpleMedium:{h:216.5,s:92,l:90.2,a:1},blurple:{h:215.4,s:80,l:47.65,a:1},blurpleDark:{h:215.9,s:79.9,l:41,a:1},blurpleStrong:{h:216.3,s:69.2,l:22.9,a:1},offWhite:{h:0,s:0,l:97.25,a:1},blueLight:{h:216.5,s:92,l:90.2,a:1},blue:{h:215.4,s:80,l:47.65,a:1},blueDark:{h:216.3,s:69.2,l:23,a:1},magenta:{h:323,s:42,l:48,a:1},orangeLight:{h:4,s:100,l:91.2,a:1},orange:{h:11,s:100,l:62.2,a:1},orangeDark:{h:10.9,s:100,l:42.2,a:1},tealLight:{h:155,s:70,l:84,a:1},teal:{h:155,s:62,l:32,a:1},tealDark:{h:155,s:55,l:19,a:1},yellowLight:{h:43,s:93,l:82,a:1},yellow:{h:45.5,s:96,l:57,a:1},yellowDark:{h:39.8,s:100,l:49.4,a:1}},st={grey8:{h:228,s:6,l:17,a:1},grey7:{h:223,s:6,l:24.5,a:1},grey6:{h:224,s:5,l:44,a:1},grey5:{h:224,s:5,l:57,a:1},grey4:{h:223,s:5,l:73,a:1},grey3:{h:225,s:6,l:87.5,a:1},grey2:{h:210,s:7,l:94.5,a:1},grey1:{h:0,s:0,l:97.25,a:1},white:{h:0,s:0,l:100,a:1}},er={record:ye.orange,recordHover:ot(ye.orange,va),recordActive:ot(ye.orange,ga),backdropDark:it(st.grey8,ba),backdropTwilight:it(ye.blurpleStrong,Ca),highlight:it(ye.blurple,Ea),highlightHover:it(ye.blurple,ya),highlightActive:it(ye.blurple,za),warning:{h:45.5,s:96,l:57,a:1,ads:"--ds-background-warning-bold"}},Qe={light:L(i({primary:ye.blurple,primaryHover:ye.blurpleDark,primaryActive:ye.blurpleStrong,body:{h:228,s:6,l:17,a:1,ads:"--ds-text"},bodyDimmed:{h:224,s:5,l:44,a:1,ads:"--ds-text-subtlest"},bodyInverse:{h:0,s:0,l:100,a:1,ads:"--ds-text-inverse"},background:{h:0,s:0,l:100,a:1,ads:"--ds-surface"},backgroundHover:{h:209,s:75.6,l:8,a:.08,ads:"--ds-background-neutral-subtle-hovered"},backgroundActive:{h:225.5,s:56.9,l:10,a:.14,ads:"--ds-background-neutral-subtle-pressed"},backgroundSecondary:{h:0,s:0,l:97.25,a:1,ads:"--ds-surface-sunken"},backgroundSecondary2:{h:0,s:0,l:97.25,a:1,ads:"--ds-surface-sunken"},backgroundNeutral:{h:209,s:76,l:8,a:.08,ads:"--ds-background-neutral"},backgroundNeutralHover:{h:226,s:57,l:1,a:.14,ads:"--ds-background-neutral-hovered"},backgroundNeutralActive:{h:223,s:61,l:8,a:.28,ads:"--ds-background-neutral-pressed"},backgroundInverse:{h:228,s:6,l:17,a:1,ads:"--ds-background-neutral-bold"},focusRing:{h:216.1,s:81.4,l:60,a:1,ads:"--ds-border-focused"},overlay:{h:0,s:0,l:100,a:1,ads:"--ds-surface-overlay"},overlayHover:st.grey2,overlayActive:st.grey3,backdrop:{h:224,s:72,l:7,a:fa,ads:"--ds-blanket"},border:{h:225.5,s:57,l:10,a:pa,ads:"--ds-border"}},er),{info:{h:215,s:80.25,l:47.65,a:1,ads:"--ds-background-information-bold"},success:{h:155,s:62,l:32,a:1,ads:"--ds-background-accent-green-bolder"},danger:{h:4,s:64,l:48,a:1,ads:"--ds-background-danger-bold"},dangerHover:{h:4.3,s:65.7,l:41.2,a:1,ads:"--ds-background-danger-bold-hovered"},dangerActive:{h:4.5,s:56.3,l:23.3,a:1,ads:"--ds-background-danger-bold-pressed"},disabledContent:{h:223,s:5,l:73,a:1,ads:"--ds-text-disabled"},disabledBackground:{h:0,s:0,l:9,a:.03,ads:"--ds-background-disabled"},formFieldBorder:{h:223.6,s:5,l:57,a:1,ads:"--ds-border-input"},formFieldBackground:{h:0,s:0,l:100,a:1,ads:"--ds-background-input"},buttonBorder:{h:252,s:13,l:46,a:qt,ads:"--ds-border"},tabBackground:{h:209,s:75.6,l:8,a:wa,ads:"--ds-background-neutral"},upgrade:{h:277.5,s:89,l:96.5,a:1,ads:"--ds-background-discovery"},upgradeHover:{h:277,s:86,l:91.6,a:1,ads:"--ds-background-discovery-hovered"},upgradeActive:{h:278.6,s:84.5,l:79.8,a:1,ads:"--ds-background-discovery-pressed"},discoveryBackground:{h:278.6,s:48.4,l:52.2,a:1,ads:"--ds-background-discovery-bold"},discoveryLightBackground:{h:277.5,s:89,l:96.5,a:1,ads:"--ds-background-discovery"},discoveryTitle:{h:228,s:6,l:17,a:1,ads:"--ds-text"},discoveryHighlight:{h:277.5,s:89,l:96.5,a:1,ads:"--ds-background-discovery"}}),dark:L(i({primary:{h:216.3,s:83.2,l:67.3,a:1},primaryHover:{h:216.1,s:85.1,l:76.3,a:1},primaryActive:{h:216.5,s:92,l:90.2,a:1},body:{h:225,s:4.3,l:81.6,a:1,ads:"--ds-text"},bodyDimmed:{h:217.5,s:4,l:60.4,a:1,ads:"--ds-text-subtlest"},bodyInverse:{h:240,s:3,l:12.5,a:1,ads:"--ds-text-inverse"},background:{h:240,s:3,l:12.5,a:1,ads:"--ds-surface"},backgroundHover:{h:240,s:12.6,l:83,a:.07,ads:"--ds-background-neutral-subtle-hovered"},backgroundActive:{h:236,s:36.6,l:92,a:.12,ads:"--ds-background-neutral-subtle-pressed"},backgroundSecondary:{h:210,s:4,l:9.8,a:1,ads:"--ds-surface-sunken"},backgroundSecondary2:{h:210,s:4,l:9.8,a:1,ads:"--ds-surface-sunken"},backgroundNeutral:{h:240,s:12.6,l:83,a:.07,ads:"--ds-background-neutral"},backgroundNeutralHover:{h:236,s:36.6,l:92,a:.12,ads:"--ds-background-neutral-hovered"},backgroundNeutralActive:{h:226,s:49,l:93,a:.25,ads:"--ds-background-neutral-pressed"},backgroundInverse:{h:225,s:4.3,l:81.6,a:1,ads:"--ds-background-neutral-bold"},focusRing:{h:216.1,s:85.1,l:76.3,a:1,ads:"--ds-background-accent-blue-subtle-hovered"},overlay:{h:225,s:4,l:17.6,a:1,ads:"--ds-surface-overlay"},overlayHover:{h:225,s:4,l:19.61,a:1,ads:"--ds-surface-overlay-hovered"},overlayActive:{h:225,s:4.69,l:25.1,a:1,ads:"--ds-surface-overlay-pressed"},backdrop:{h:210,s:11,l:7,a:.6,ads:"--ds-blanket"},border:{h:236,s:36.6,l:92,a:.12,ads:"--ds-border"}},er),{info:{h:216.3,s:83,l:67.25,a:1,ads:"--ds-background-information-bold"},success:{h:155,s:57,l:55,a:1,ads:"--ds-background-accent-green-bolder"},danger:{h:3.75,s:91,l:69,a:1,ads:"--ds-background-danger-bold"},dangerHover:{h:4,s:96,l:78,a:1,ads:"--ds-background-danger-bold-hovered"},dangerActive:{h:4,s:100,l:91.2,a:1,ads:"--ds-background-danger-bold-pressed"},disabledContent:{h:225,s:5,l:33,a:1,ads:"--ds-text-disabled"},disabledBackground:{h:0,s:0,l:1,a:.46,ads:"--ds-background-disabled"},formFieldBorder:{h:222,s:4,l:51.4,a:1,ads:"--ds-border-input"},formFieldBackground:{h:225,s:5,l:15,a:1,ads:"--ds-background-input"},buttonBorder:{h:0,s:0,l:100,a:qt,ads:"--ds-border"},tabBackground:{h:240,s:12.6,l:83,a:.07,ads:"--ds-background-neutral"},upgrade:{h:277.8,s:27.3,l:19.4,a:1,ads:"--ds-background-discovery"},upgradeHover:{h:278,s:44.2,l:25.3,a:1,ads:"--ds-background-discovery-hovered"},upgradeActive:{h:278,s:45,l:44.7,a:1,ads:"--ds-background-discovery-pressed"},discoveryBackground:{h:278.5,s:84.5,l:72.2,a:1,ads:"--ds-background-discovery-bold"},discoveryLightBackground:{h:277.8,s:27.3,l:19.4,a:1,ads:"--ds-background-discovery"},discoveryTitle:{h:225,s:4.3,l:81.6,a:1,ads:"--ds-text"},discoveryHighlight:{h:277.8,s:27.3,l:19.4,a:1,ads:"--ds-background-discovery"}})},he=i(i({},ye),st),tr=[...Object.keys(he),...Object.keys(Qe.light)],Ii=(e,t)=>`hsla(${he[e].h},${he[e].s}%,${he[e].l}%,${t})`,Bi=(e,t,a)=>{const r=()=>{if(t==="dark")return he[e].l-he[e].l*a;if(t==="light")return he[e].l+he[e].l*a};return`hsla(${he[e].h},${he[e].s}%,${Math.round(r())}%,${he[e].a})`},d=e=>{if(e)return e in he||e in Qe.light?`var(--lns-color-${e})`:e in dr?`var(--lns-gradient-${e})`:e};function xa(e,t,a){const r=React.useCallback(()=>typeof window>"u"?a:t[e.findIndex(s=>matchMedia(s).matches)]||a,[a,e,t]),[l,o]=React.useState(r);return React.useEffect(()=>{const s=_debounce(()=>o(r),150);return window.addEventListener("resize",s),()=>window.removeEventListener("resize",s)},[r]),l}var u=e=>e&&`calc(${e} * var(--lns-unit, ${et}px))`,Me=e=>{if(e in bt)return`var(--lns-space-${e})`;if(e&&isNaN(e))return`${e}`;if(e===0)return"0";if(e)return`${u(e)}`},C=(e,t)=>{if(t||t===0){if(Array.isArray(t)){const a=t.map(r=>`${e}: ${Me(r)}`);return qe(a)}if(typeof t=="object"){const a={};return Object.entries(t).forEach(([r,l])=>a[r]=Me(l)),dt(e,a)}return`${e}: ${Me(t)};`}},rr=(e,t,a)=>`@media(${e}: ${t}){${a}}`,qe=e=>{const t=Object.values(je)[0],a=rr("max-width",t,e[0]),r=e.reduce((l,o,s)=>{const c=`${Object.values(je)[s]}`;return l+rr("min-width",c,o)},"");return a+r},dt=(e,t)=>{const a=[];return t.default&&a.push(`${e}: ${t.default};`),delete t.default,Object.entries(t).forEach(([r,l])=>{const o=r in je?je[r]:r;a.push(`@media(min-width: ${o}){ ${e}: ${l} }`)}),a.join(" ")},we=(e,t)=>{if(Array.isArray(t)){const a=t.map(r=>`${e}: ${r};`);return qe(a)}return typeof t=="object"?dt(e,t):`${e}: ${t};`},ar=(e,t)=>{if(e){if(Array.isArray(e)){const a=[];return e.map(r=>{a.push(t[r])}),we("align-items",a)}return`align-items ${t[e]};`}},$a=(e,t,a)=>{if(Array.isArray(a)){const r=a.map(l=>{const o=l===!0?t[0]:t[1];return`${e}: ${o};`});return qe(r)}return`${e}: ${t[0]};`},nr=(e,t)=>{if(t||t===0){if(Array.isArray(t)){const a=t.map(r=>`${e}: ${r}`);return qe(a)}return typeof t=="object"&&!Array.isArray(t)?dt(e,t):`${e}: ${t};`}},gt=e=>Array.isArray(e)?e.map(t=>Me(t)).join(" "):e,Oi=e=>{if(e){if(typeof e=="object"&&!Array.isArray(e)){const t={};return Object.entries(e).forEach(([a,r])=>t[a]=gt(r)),dt("grid-template-columns",t)}return`grid-template-columns: ${gt(e)};`}},lr=(e,t)=>{if(e){if(typeof e=="object"&&!Array.isArray(e)){const a={};return Object.entries(e).forEach(([r,l])=>a[r]=gt(l)),dt(`grid-template-${t}`,a)}return`grid-template-${t}: ${gt(e)};`}},Di=({children:e,queries:t,values:a,defaultValue:r})=>{const l=xa(t,a,r);return e(l)},Se=e=>e&&`
  font-size: var(--lns-fontSize-${e});
  line-height: var(--lns-lineHeight-${e});
  letter-spacing: var(--lns-letterSpacing-${e});
`,Fe=e=>e&&`font-weight: var(--lns-fontWeight-${e});`,Ma=e=>e&&`var(--lns-fontSetting-${e});`,ee=e=>e&&`border-radius: var(--lns-radius-${e});`,ct=e=>e&&`box-shadow: var(--lns-shadow-${e});`,ke=(e,t)=>{const a=e||d("focusRing");return`box-shadow:${t||""} 0 0 0 2px ${a};`},pt=e=>`
  outline: 2px solid ${e||d("focusRing")};
  outline-offset: 1px;
  `,or=e=>{if(e==="ol"||e==="ul")return`
      list-style-type: none;
      margin: 0;
      padding: 0
      `},Ht=(e,t)=>({center:{bottom:0,top:`calc((100vh - ${e}) / 2)`,position:"relative"},bottom:{bottom:0,top:"unset",position:"absolute"},undefined:{bottom:void 0,top:"15vh",position:"relative"}})[t],ft=e=>e.replace(/([a-z0-9])([A-Z])/g,"$1-$2").replace(/[\s_]+/g,"-").toLowerCase(),et=8,Ze={small:{fontSize:1.5,lineHeight:1.5,letterSpacing:"normal"},"body-sm":{fontSize:1.5,lineHeight:1.5,letterSpacing:"normal"},medium:{fontSize:1.75,lineHeight:1.57,letterSpacing:"normal"},"body-md":{fontSize:1.75,lineHeight:1.57,letterSpacing:"normal"},large:{fontSize:2.25,lineHeight:1.44,letterSpacing:"-0.2px"},"body-lg":{fontSize:2.25,lineHeight:1.44,letterSpacing:"-0.2px"},xlarge:{fontSize:3,lineHeight:1.16,letterSpacing:"-0.2px"},"heading-sm":{fontSize:3,lineHeight:1.16,letterSpacing:"-0.2px"},xxlarge:{fontSize:4,lineHeight:1.125,letterSpacing:"-0.5px"},"heading-md":{fontSize:4,lineHeight:1.125,letterSpacing:"-0.5px"},xxxlarge:{fontSize:6,lineHeight:1.16,letterSpacing:"-1.2px"},"heading-lg":{fontSize:6,lineHeight:1.16,letterSpacing:"-1.2px"}},ir={book:400,regular:400,medium:500,bold:653},ka={normal:"'normal'",tnum:"'tnum'"},sr={none:u(0),50:u(.5),100:u(1),medium:u(1),150:u(1.5),175:u(1.75),200:u(2),large:u(2),250:u(2.5),300:u(3),xlarge:u(3),round:u(999),full:u(999)},St={small:`0 ${u(.5)} ${u(1.25)} hsla(0, 0%, 0%, 0.05)`,medium:`0 ${u(.5)} ${u(1.25)} hsla(0, 0%, 0%, 0.1)`,large:`0 ${u(.75)} ${u(3)} hsla(0, 0%, 0%, 0.1)`},bt={xsmall:.5,small:1,medium:2,large:3,xlarge:5,xxlarge:8},je={xsmall:"31em",small:"48em",medium:"64em",large:"75em"},dr={"ai-primary":"conic-gradient(from 270deg, #0469FF 90deg, #BF63F3 180deg, #FFA900 270deg, #0065FF 360deg)","ai-secondary":"radial-gradient(138.41% 100% at 100% 100%, #E9F2FE 0%, #FFF 100%)"},La=`Lens: Text prop 'isDimmed' is deprecated, use color="bodyDimmed" instead.`,It="Lens: don't apply custom styles to components, learn more: https://lens.loom.dev/guides/development-best-practices/the-risk-of-modifying-components-with-custom-styles.",Ra=null,cr="Lens: Layout component is deprecated. Use Arrange or Split.",_a=.6,Bt={body:{size:"body-md",fontWeight:"regular"},title:{size:"body-lg",fontWeight:"bold"},mainTitle:{size:"heading-md",fontWeight:"bold"}},ur=e=>Ze[e].fontSize*et,hr=e=>u(Ze[e].fontSize),Ct=e=>Ze[e].fontSize*Ze[e].lineHeight*et,mr=(e,t,a,r)=>{const l=(t-e)/(r-a);return`${-a*l+e}px + ${l*100}vw`},Ha=h.Z.span`
  display: ${e=>e.isInline?"inline":"block"};
  ${e=>!e.sizeMinMax&&Se(e.size)};
  ${e=>Fe(e.fontWeight)};
  ${e=>e.color&&`color: ${d(e.color)}`};
  ${e=>e.fontSetting&&`font-feature-settings: ${Ma(e.fontSetting)}`};
  ${e=>e.isDimmed&&`opacity: ${_a}`};
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
      ${hr(e.sizeMinMax[0])},
      ${mr(ur(e.sizeMinMax[0]),ur(e.sizeMinMax[1]),496,1200)},
      ${hr(e.sizeMinMax[1])}
    );

    line-height: clamp(
      ${Ct(e.sizeMinMax[0])}px,
      ${mr(Ct(e.sizeMinMax[0]),Ct(e.sizeMinMax[1]),496,1200)},
      ${Ct(e.sizeMinMax[1])}px
    );
  `}
`,Sa=e=>{var t=e,{children:a,size:r="body-md",color:l,isInline:o,isDimmed:s,fontWeight:c="regular",hasEllipsis:m,ellipsisLines:v,noWrap:f,variant:p,htmlTag:b="span",alignment:w,sizeMinMax:$,fontSetting:x="normal"}=t,y=E(t,["children","size","color","isInline","isDimmed","fontWeight","hasEllipsis","ellipsisLines","noWrap","variant","htmlTag","alignment","sizeMinMax","fontSetting"]);return s&&console.warn(La),r.includes("heading-")&&(c="bold"),n.createElement(Ha,i({size:p?Bt[p].size:r,color:l,isInline:o,isDimmed:s,fontWeight:p?Bt[p].fontWeight:c,hasEllipsis:m,ellipsisLines:v,noWrap:f,variant:p,as:b,alignment:w,sizeMinMax:$,fontSetting:x},y),a)},Ia=["left","right","center"],Ie=Sa,wt=["top","bottom","left","right"],vr=i({0:"0"},bt),Ot=i({0:"0",auto:"auto"},bt),Ba=tr.map(e=>({selector:"c",modifier:e,declarations:[{property:"color",value:`var(--lns-color-${e})`}]})),Oa=tr.map(e=>({selector:"bgc",modifier:e,declarations:[{property:"background-color",value:`var(--lns-color-${e})`}]})),Da=Object.keys(Ze).map(e=>({selector:"text",modifier:e,declarations:[{property:"font-size",value:`var(--lns-fontSize-${e})`},{property:"line-height",value:`var(--lns-lineHeight-${e})`},{property:"letter-spacing",value:`var(--lns-letterSpacing-${e})`},e.includes("heading-")||e.includes("xlarge")?{property:"font-weight",value:"var(--lns-fontWeight-bold)"}:{property:"font-weight",value:"var(--lns-fontWeight-regular)"}]})),Va=Object.keys(ir).map(e=>({selector:"weight",modifier:e,declarations:[{property:"font-weight",value:`var(--lns-fontWeight-${e})`}]})),Wa=Object.entries(Bt).map(([e,t])=>({selector:"text",modifier:e,declarations:[{property:"font-size",value:`var(--lns-fontSize-${t.size})`},{property:"line-height",value:`var(--lns-lineHeight-${t.size})`},{property:"font-weight",value:`var(--lns-fontWeight-${t.fontWeight})`}]})),Aa=Ia.map(e=>({selector:"text",modifier:e,declarations:[{property:"text-align",value:e}]})),Pa=Object.keys(St).map(e=>({selector:"shadow",modifier:e,declarations:[{property:"box-shadow",value:`var(--lns-shadow-${e})`}]})),Ta=Object.keys(sr).map(e=>({selector:"radius",modifier:e,declarations:[{property:"border-radius",value:`var(--lns-radius-${e})`}]})),ut=(e,t,a,r)=>{const l=[];return t.map(o=>{const s=r?`${e.charAt(0)}${o.charAt(0)}`:o;Object.keys(a).map(c=>{l.push({selector:s,property:`${e}${o&&e?`-${o}`:o||""}`,modifier:c,value:c==="auto"||c==="0"?c:`var(--lns-space-${c})`})})}),l},Fa=Object.values(ut("margin",["",...wt],Ot,"shortSides")).map(e=>({selector:e.selector,modifier:e.modifier,declarations:[{property:e.property,value:e.value}]})),Za=Object.values(ut("margin",["x","y"],Ot,"shortSides")).map(e=>({selector:e.selector,modifier:e.modifier,declarations:[{property:e.property==="margin-x"?"margin-left":"margin-top",value:e.value},{property:e.property==="margin-x"?"margin-right":"margin-bottom",value:e.value}]})),ja=Object.values(ut("padding",["",...wt],vr,"shortSides")).map(e=>({selector:e.selector,modifier:e.modifier,declarations:[{property:e.property,value:e.value}]})),Na=Object.values(ut("padding",["x","y"],vr,"shortSides")).map(e=>({selector:e.selector,modifier:e.modifier,declarations:[{property:e.property==="padding-x"?"padding-left":"padding-top",value:e.value},{property:e.property==="padding-x"?"padding-right":"padding-bottom",value:e.value}]})),Ua=["",...wt].map(e=>{const t="border"+e.replace(e.charAt(0),e.charAt(0).toUpperCase()),a=`border${e&&`-${e}`}`;return{selector:t,declarations:[{property:a,value:"1px solid var(--lns-color-border)"}]}}),Ka=["inline","block","flex","inlineBlock","inlineFlex","none"],Ga=Ka.map(e=>({selector:e,declarations:[{property:"display",value:ft(e)}]})),Ya=[{selector:"flexWrap",declarations:[{property:"flex-wrap",value:"wrap"}]}],Xa=["column","row"],Ja=Xa.map(e=>({selector:"flexDirection",modifier:e,declarations:[{property:"flex-direction",value:e}]})),Qa=["stretch","center","baseline","flexStart","flexEnd","selfStart","selfEnd"],qa=Qa.map(e=>({selector:"items",modifier:e,declarations:[{property:"align-items",value:ft(e)}]})),en=["flexStart","flexEnd","center","spaceBetween","spaceAround","spaceEvenly"],tn=en.map(e=>({selector:"justify",modifier:e,declarations:[{property:"justify-content",value:ft(e)}]})),rn=["0","1"],an=rn.map(e=>({selector:"grow",modifier:e,declarations:[{property:"flex-grow",value:e}]})),nn=["0","1"],ln=nn.map(e=>({selector:"shrink",modifier:e,declarations:[{property:"flex-shrink",value:e}]})),on=["auto","flexStart","flexEnd","center","baseline","stretch"],sn=on.map(e=>({selector:"self",modifier:e,declarations:[{property:"align-self",value:ft(e)}]})),dn=["hidden","auto"],cn=dn.map(e=>({selector:"overflow",modifier:e,declarations:[{property:"overflow",value:e}]})),un=["relative","absolute","sticky","fixed"],hn=un.map(e=>({selector:e,declarations:[{property:"position",value:e}]})),mn=Object.values(ut("",wt,Ot)).map(e=>({selector:e.selector,modifier:e.modifier,declarations:[{property:e.property,value:e.value}]})),vn=["auto","full","0"],gn=vn.map(e=>({selector:"width",modifier:e,declarations:[{property:"width",value:e==="full"?"100%":e}]})),pn=[{selector:"minWidth",modifier:"0",declarations:[{property:"min-width",value:"0"}]}],fn=["auto","full","0"],bn=fn.map(e=>({selector:"height",modifier:e,declarations:[{property:"height",value:e==="full"?"100%":e}]})),Cn=[{selector:"ellipsis",declarations:[{property:"overflow",value:"hidden"},{property:"text-overflow",value:"ellipsis"},{property:"white-space",value:"nowrap"}]}],wn=[{selector:"srOnly",declarations:[{property:"position",value:"absolute"},{property:"width",value:"1px"},{property:"height",value:"1px"},{property:"padding",value:"0"},{property:"margin",value:"-1px"},{property:"overflow",value:"hidden"},{property:"clip",value:"rect(0, 0, 0, 0)"},{property:"white-space",value:"nowrap"},{property:"border-width",value:"0"}]}],En="\\:",gr=[...Ba,...Pa,...Ta,...Oa,...Fa,...Za,...ja,...Na,...Da,...Va,...Wa,...Aa,...Ua,...Ga,...Ya,...Ja,...qa,...tn,...an,...ln,...sn,...cn,...hn,...mn,...gn,...pn,...bn,...Cn,...wn],pr=(e,t)=>{const a=[],r=t?`${t}-`:"";return e.map(l=>{const o=[];l.declarations.map(c=>{o.push(`${c.property}:${c.value}`)});const s=`.${r}${l.selector}${l.modifier?En:""}${l.modifier?l.modifier:""}{${o.join(";")}}`;a.push(s)}),a.join("")},yn={xs:je.xsmall,sm:je.small,md:je.medium,lg:je.large},zn=()=>(()=>{const t=[];return t.push(`${pr(gr)}`),Object.entries(yn).map(([a,r])=>{t.push(`@media(min-width:${r}){${pr(gr,a)}}`)}),t.join("")})(),Le=(e,t)=>{const a={};return Object.entries(t).forEach(([r,l])=>{const s=`--lns-${(e?`${e}-`:"")+r}`;a[s]=l}),a},xn=()=>{const e={};return Object.entries(Ze).forEach(([t,a])=>{const r={},l={},o={},s=`fontSize-${t}`,c=`lineHeight-${t}`,m=`letterSpacing-${t}`;r[s]=u(a.fontSize),r[c]=a.lineHeight,r[m]=a.letterSpacing,Object.assign(e,r,l,o)}),e},$n=()=>{const e={};return Object.entries(bt).forEach(([t,a])=>{const r=`space-${t}`;e[r]=u(a)}),e},Mn=()=>{const e={};return Object.keys(i(i({},ye),st)).forEach(t=>{const a=t;e[a]=`hsla(${he[t].h},${he[t].s}%,${he[t].l}%,${he[t].a})`}),e},kn=()=>{const e=(t,a)=>Object.keys(t).reduce((r,l)=>{const o=t[l],s=`${a}-color-${l}`;return r[s]=o.ads?`var(${o.ads}, hsla(${o.h},${o.s}%,${o.l}%,${o.a}))`:`hsla(${o.h},${o.s}%,${o.l}%,${o.a})`,r},{});return i(i({},e(Qe.light,"themeLight")),e(Qe.dark,"themeDark"))},Ln=Le(void 0,{unit:`${et/16}rem`}),Rn=Le("fontWeight",ir),_n=Le("fontSetting",ka),Hn=Le(void 0,xn()),Sn=Le("radius",sr),In=Le("shadow",St),Bn=Le(void 0,$n()),On=Le(void 0,{formFieldBorderWidth:"1px",formFieldBorderWidthFocus:"2px",formFieldHeight:u(4.5),formFieldRadius:"var(--lns-radius-175)",formFieldHorizontalPadding:u(2),formFieldBorderShadow:`
    inset 0 0 0 var(--lns-formFieldBorderWidth) var(--lns-color-formFieldBorder)
  `,formFieldBorderShadowFocus:`
    inset 0 0 0 var(--lns-formFieldBorderWidthFocus) var(--lns-color-blurple),
    0 0 0 var(--lns-formFieldBorderWidthFocus) var(--lns-color-focusRing)
  `,formFieldBorderShadowError:`
    inset 0 0 0 var(--lns-formFieldBorderWidthFocus) var(--lns-color-danger),
    0 0 0 var(--lns-formFieldBorderWidthFocus) var(--lns-color-orangeLight)
  `}),Dn=Le("color",Mn()),Vn=Le(void 0,kn()),Wn=Le("gradient",dr),fr=[Ln,Hn,Sn,In,Bn,On],An=()=>Object.assign({},...fr),Pn=()=>Object.assign({},Rn,...fr,_n),Tn=()=>i(i(i({},Dn),Vn),Wn),Fn=()=>Object.keys(Qe.light).map(e=>`--lns-color-${e}: var(--lns-themeLight-color-${e});`),Zn=()=>Object.keys(Qe.dark).map(e=>`--lns-color-${e}: var(--lns-themeDark-color-${e});`),br=(e=":root")=>`
    ${e||":root"},
    .theme-light,
    [data-lens-theme="light"] {
      ${Fn().join("")}
    }

    .theme-dark,
    [data-lens-theme="dark"] {
      ${Zn().join("")}
    }
  `,Vi=()=>{const e=document.createElement("style");e.innerHTML=br(),document.head.appendChild(e)},Wi=()=>Object.entries(An()).map(t=>`${t[0]}:${t[1]};`).join(""),jn=e=>{const t=[],a=e||":root";return Object.entries(Pn()).forEach(r=>{t.push(`${r[0]}:${r[1]};`)}),Object.entries(Tn()).forEach(r=>{t.push(`${r[0]}:${r[1]};`)}),`
    ${a} {
      ${t.join("")}
    }
  `},Nn=e=>{switch(e){case"orange":return{background:"orangeLight",text:"dangerHover"};case"blue":return{background:"blueLight",text:"blueDark"};case"yellow":return{background:"yellowLight",text:"#9E4C00"};case"teal":return{background:"tealLight",text:"tealDark"};default:return{background:"orangeLight",text:"dangerHover"}}},Un=e=>`calc(${e} / 2)`,Ne=e=>{let t,a;if(e==="medium")t=u(4),a=u(4);else if(e==="large")t=u(7),a=u(7);else{const l=Me(e);t=l,a=l}const r=Un(t);return{width:t,height:a,fontSize:r}},Kn=h.Z.span`
  display: block;
  color: ${e=>e.color?e.color.startsWith("#")?e.color:`var(--lns-color-${e.color})`:"var(--lns-color-blueLight)"};
  background-color: var(--lns-color-background);
  ${ee("full")};
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  font-weight: var(--lns-fontWeight-bold);
  width: ${e=>{const{width:t}=Ne(e.size);return t}};
  height: ${e=>{const{height:t}=Ne(e.size);return t}};
  font-size: ${e=>{const{fontSize:t}=Ne(e.size);return t}};
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
`,Gn=h.Z.img`
  max-width: 100%;
  width: ${e=>{const{width:t}=Ne(e.size);return t}};
  height: ${e=>{const{height:t}=Ne(e.size);return t}};
  font-size: ${e=>{const{fontSize:t}=Ne(e.size);return t}};
`,Ai=e=>{var t=e,{altText:a="",size:r=4,letter:l,imageSrc:o,children:s,themeColor:c="blue"}=t,m=E(t,["altText","size","letter","imageSrc","children","themeColor"]);const v=()=>{if(s)return s;if(o){const b=Ne(r).height,w=Ne(r).width;return React3.createElement(Gn,{size:r,alt:a,src:o,height:b,width:w})}if(l)return a?React3.createElement("span",{"aria-label":a},l):l},f=l&&!o&&!s,p=Nn(c||"blue");return React3.createElement(Kn,i({hasBackgroundColor:f,size:r,backgroundColor:p.background,color:p.text},m),v())},Pi=null,Cr=(e=":root",t="body")=>`
    ${e} {
      font-size: 100%;
    }
    ${t} {
      --lns-fontFamily-body: "Atlassian Sans", ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, system-ui, "Helvetica Neue", sans-serif;
      --lns-fontFamily-heading: "Atlassian Sans", ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, system-ui, "Helvetica Neue", sans-serif;
      --lns-fontFamily-code: "Atlassian Mono", ui-monospace, Menlo, "Segoe UI Mono", "Ubuntu Mono", monospace;

      font-family: var(--lns-fontFamily-body);
      color: var(--ds-text, ${d("body")});
      ${Se("body-md")};
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

    ${br(e)}

    ${jn(e)}

    ${zn()}
  `,Ti=()=>React4.createElement(Global,{styles:css(Cr())}),Fi=null,Yn=3,Xn=h.Z.span`
  display: block;
  color: ${e=>d(e.color)};

  & > svg,
  & > img {
    display: block;
    ${e=>C("width",e.size)};
    ${e=>C("height",e.size)};
  }

  // TODO: remove data-testid once all icons are using ADS
  [data-testid='ads-refreshed-icon'] {
    display: block;
    ${e=>C("width",e.size)};
    ${e=>C("height",e.size)};

    svg {
      padding: 8%;
      height: 100%;
      width: 100%;
    }
  }
`,Jn=e=>{var t=e,{altText:a,icon:r,color:l="body",size:o=Yn}=t,s=E(t,["altText","icon","color","size"]);const c=n.useRef(null);return n.createElement(Xn,i({ref:c,"aria-label":a,color:l,size:o},s),r)},ie=Jn,wr=1,Dt=8,Vt={small:{totalSize:18},medium:{totalSize:24},large:{totalSize:48}},Et=e=>Vt[e.size].totalSize/6,Wt=e=>Vt[e.size].totalSize,Qn=z.F4`
  50% {
    transform: scale(1);
  }
`,qn=h.Z.span`
  display: inline-block;
  vertical-align: middle;
  height: ${e=>Wt(e)}px;
  width: ${e=>Wt(e)}px;
`,e1=h.Z.span`
  display: grid;
  grid-template-areas: 'stack';
  height: 100%;
  width: 100%;
`,t1=h.Z.span`
  grid-area: stack;
  place-self: center;
  transform: rotate(${e=>e.position*(360/Dt)}deg)
    translateY(${e=>Wt(e)/2-Et(e)/2}px);

  &:after {
    content: '';
    height: ${e=>Et(e)}px;
    width: ${e=>Et(e)}px;
    border-radius: ${e=>Et(e)}px;
    background-color: ${e=>d(e.color)};
    display: block;
    transform: scale(0.65);
    animation: ${Qn} ${wr}s
      ${e=>e.position*wr/Dt}s ease-in-out infinite;
  }
`,r1=({position:e,color:t,size:a})=>n.createElement(t1,{color:t,position:e,size:a}),a1=e=>{var t=e,{color:a="body",size:r="medium"}=t,l=E(t,["color","size"]);let o;const s=[];for(o=0;o<Dt;o++)s.push(n.createElement(r1,{color:a,position:o,size:r,key:o}));return n.createElement(qn,i({size:r},l),n.createElement(e1,null,s))},Zi=Object.keys(Vt),At=a1,ze={small:{height:u(4),textSize:"small",iconSize:2,xSpace:u(1.5),radius:"var(--lns-radius-150)"},medium:{height:u(4.5),textSize:"medium",iconSize:3,xSpace:u(2),radius:"var(--lns-radius-175)"},large:{height:u(7),textSize:"large",iconSize:4,xSpace:u(2.5),radius:"var(--lns-radius-250)"}},Pt=e=>z.iv`
  ${e.hasLoader&&"display: none"};
`,Be={neutral:{color:d("body"),background:"transparent",borderColor:d("buttonBorder"),hover:d("backgroundHover"),active:d("backgroundActive"),floatingBackground:d("overlay"),floatingHover:d("overlayHover"),floatingActive:d("overlayActive")},neutralSecondary:{color:d("body"),background:d("backgroundNeutral"),borderColor:null,hover:d("backgroundNeutralHover"),active:d("backgroundNeutralActive")},primary:{color:d("white"),background:d("blurple"),borderColor:null,hover:d("primaryHover"),active:d("primaryActive")},secondary:{color:d("primary"),background:d("highlight"),borderColor:null,hover:d("highlightHover"),active:null},record:{color:d("white"),background:d("record"),borderColor:null,hover:d("recordHover"),active:d("recordActive")},upgrade:{color:d("body"),background:d("upgrade"),borderColor:null,hover:d("upgradeHover"),active:d("upgradeActive"),focusRing:ke()},danger:{color:d("bodyInverse"),background:d("danger"),borderColor:null,hover:d("dangerHover"),active:d("dangerActive")},ai:{color:d("white"),background:d("ai-primary"),borderColor:null,hover:null,active:null}},Er=e=>({enabled:z.iv`
    cursor: pointer;
  `,disabled:z.iv`
    ${e.ariaDisabled&&"aria-disabled: true"};
    pointer-events: none;
    background-color: ${d("disabledBackground")};
    color: ${d("disabledContent")};
    border: none;
  `}),n1=e=>({auto:z.iv`
    display: inline-flex;
    min-width: ${ze[e.size].height};
  `,full:z.iv`
    display: flex;
    width: 100%;
  `,maxContent:z.iv`
    display: inline-flex;
    width: max-content;
    min-width: max-content;
  `}),yr=u(1),l1=h.Z.button`
  appearance: none;
  padding: 0
    ${e=>e.hasChildren?ze[e.size].xSpace:0};
  font: inherit;
  text-decoration: none;
  transition:
    0.6s background,
    0.6s border-color;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  white-space: nowrap;
  ${Fe("bold")};
  border-radius: ${e=>ze[e.size].radius};
  // TODO: remove hasFullWidth after deprecation period
  ${e=>e.hasFullWidth?"display: flex; width: 100%":"display: inline-flex"};
  ${e=>n1(e)[e.width]};
  height: ${e=>ze[e.size].height};
  ${e=>Se(ze[e.size].textSize)};
  ${e=>e.isFloating&&`box-shadow: ${St.medium}`};
  ${e=>e.disabled?Er(e).disabled:Er(e).enabled};
  ${e=>!e.disabled&&`
    border: ${Be[e.variant].borderColor?`1px solid ${Be[e.variant].borderColor}`:"none"};
    background: ${e.isFloating&&e.variant==="neutral"?Be[e.variant].floatingBackground:Be[e.variant].background};
    background-position: left;
    background-size: 125%;
    color: ${Be[e.variant].color};
  `};

  &:hover {
    transition:
      0.3s background,
      0.3s border-color;
    background: ${e=>e.isFloating&&e.variant==="neutral"?Be[e.variant].floatingHover:Be[e.variant].hover};
    background-position: 75% center;
  }

  &:active {
    transition:
      0s background,
      0s border-color;
    background: ${e=>e.isFloating&&e.variant==="neutral"?Be[e.variant].floatingActive:Be[e.variant].active};
    background-position: right;
  }

  &:focus-visible {
    ${e=>e["aria-expanded"]?"outline: none;":pt()};
  }

  &::-moz-focus-inner {
    border: 0;
  }
`,zr=h.Z.span`
  ${e=>C("padding-left",e.paddingLeft)};
  ${e=>C("padding-right",e.paddingRight)};
  ${Pt};
`,o1=h.Z.img`
  max-width: 1.45em;
  max-height: 1.45em;
  height: ${e=>ze[e.size].height};
  width: ${e=>ze[e.size].height};
  ${e=>e.hasSpacing&&"margin-right: 0.57em"};
  ${Pt};
`,i1=h.Z.span`
  position: relative;
  display: flex;
  align-items: center;
`,s1=h.Z.span`
  ${Pt};
`,ji=e=>{var t=e,{size:a="medium",children:r,variant:l="neutral",hasFullWidth:o,width:s="auto",icon:c,iconPosition:m="left",iconBefore:v,iconAfter:f,logoSrc:p,hasLoader:b,isDisabled:w,ariaDisabled:$,htmlTag:x="button",interactionName:y,onClick:I,refHandler:N}=t,Q=E(t,["size","children","variant","hasFullWidth","width","icon","iconPosition","iconBefore","iconAfter","logoSrc","hasLoader","isDisabled","ariaDisabled","htmlTag","interactionName","onClick","refHandler"]);const P=c&&m==="left"?c:null,re=v||P?React7.createElement(zr,{hasLoader:b,paddingLeft:"0",paddingRight:r?yr:"0"},React7.createElement(ie,{icon:v||P,color:"currentColor",size:ze[a].iconSize})):null,le=c&&m==="right"?c:null,G=f||le?React7.createElement(zr,{hasLoader:b,paddingLeft:r?yr:"0",paddingRight:"unset"},React7.createElement(ie,{icon:le||f,color:"currentColor",size:ze[a].iconSize})):null,Y=useCallback(q=>{y&&traceUFOPress(y),I?.(q)},[I,y]);return React7.createElement(l1,L(i({size:a,variant:l,hasFullWidth:o,width:s,icon:c,iconPosition:m,logoSrc:p,disabled:w,ariaDisabled:$,as:x,hasChildren:r,ref:q=>N&&N(q)},Q),{onClick:y===void 0?I:Y}),b&&React7.createElement(i1,null,React7.createElement(At,{color:"currentColor"})),re,p&&React7.createElement(o1,{alt:"",hasSpacing:Boolean(r),src:p,size:a,height:ze[a].height,width:ze[a].height,hasLoader:b}),React7.createElement(s1,{hasLoader:b},r),G)},Ni=Object.keys(ze),Ui=Object.keys(Be),Ki=null,d1=h.Z.div`
  display: ${e=>e.isInline?"inline-block":"block"};
  vertical-align: middle;
  ${e=>C("padding",e.all)};
  ${e=>C("padding-top",e.top)};
  ${e=>C("padding-right",e.right)};
  ${e=>C("padding-bottom",e.bottom)};
  ${e=>C("padding-left",e.left)};
`,c1=e=>{var t=e,{children:a,all:r,y:l,x:o,top:s,right:c,bottom:m,left:v,isInline:f}=t,p=E(t,["children","all","y","x","top","right","bottom","left","isInline"]);return n.createElement(d1,i({all:r,top:l||s,bottom:l||m,right:o||c,left:o||v,isInline:f},p),a)},yt=c1,zt={topLeft:"start",topCenter:"start center",topRight:"start end",centerLeft:"center start",center:"center",centerRight:"center end",bottomLeft:"end start",bottomCenter:"end center",bottomRight:"end"},u1=e=>{if(Array.isArray(e))return e.map(t=>zt[t]);if(typeof e=="object"){const t={};return Object.entries(e).forEach(([a,r])=>t[a]=zt[r]),t}return zt[e]},h1=h.Z.div`
  width: 100%;
  height: 100%;
  display: grid;
  ${e=>we("place-items",u1(e.alignment))};
`,m1=e=>{var t=e,{children:a,alignment:r="center",htmlTag:l="div"}=t,o=E(t,["children","alignment","htmlTag"]);return n.createElement(h1,i({alignment:r,as:l},o),a)},Gi=Object.keys(zt),Ke=m1,v1=(e,t,a)=>{const r=t||"border",o=`${Me(a)} solid ${d(r)}`;if(e)return e==="all"?`border: ${o};`:`border-${e}: ${o};`},g1=h.Z.div`
  ${e=>e.position&&`position: ${e.position}`};
  ${e=>e.overflow&&`overflow: ${e.overflow}`};
  ${e=>e.backgroundColor&&`background-color: ${d(e.backgroundColor)}`};
  ${e=>e.backgroundImage&&`background-image: ${e.backgroundImage}`}
  ${e=>e.contentColor&&`color: ${d(e.contentColor)}`};
  ${e=>v1(e.borderSide,e.borderColor,e.borderWidth)};
  ${e=>ee(e.radius)};
  ${e=>ct(e.shadow)};
  ${e=>C("width",e.width)};
  ${e=>C("height",e.height)};
  ${e=>C("min-width",e.minWidth)};
  ${e=>C("min-height",e.minHeight)};
  ${e=>C("max-width",e.maxWidth)};
  ${e=>C("max-height",e.maxHeight)};
  ${e=>C("padding",e.padding)};
  ${e=>C("padding-top",e.paddingTop)};
  ${e=>C("padding-right",e.paddingRight)};
  ${e=>C("padding-bottom",e.paddingBottom)};
  ${e=>C("padding-left",e.paddingLeft)};
  ${e=>C("margin",e.margin)};
  ${e=>C("margin-top",e.marginTop)};
  ${e=>C("margin-right",e.marginRight)};
  ${e=>C("margin-bottom",e.marginBottom)};
  ${e=>C("margin-left",e.marginLeft)};
  ${e=>C("top",e.top)};
  ${e=>C("right",e.right)};
  ${e=>C("bottom",e.bottom)};
  ${e=>C("left",e.left)};
  ${e=>e.zIndex&&`z-index: ${e.zIndex}`};
`,p1=e=>{var t=e,{children:a,backgroundColor:r,backgroundImage:l,contentColor:o,borderColor:s,radius:c,borderSide:m,borderWidth:v="1px",shadow:f,padding:p,paddingX:b,paddingY:w,paddingLeft:$,paddingRight:x,paddingTop:y,paddingBottom:I,margin:N,marginX:Q,marginY:P,marginLeft:re,marginRight:le,marginTop:G,marginBottom:Y,width:q,height:ce,minWidth:ae,minHeight:te,maxWidth:U,maxHeight:ue,htmlTag:ne="div",position:xe,overflow:De,zIndex:B,top:se,bottom:nt,left:Ve,right:Pe,refHandler:Re}=t,O=E(t,["children","backgroundColor","backgroundImage","contentColor","borderColor","radius","borderSide","borderWidth","shadow","padding","paddingX","paddingY","paddingLeft","paddingRight","paddingTop","paddingBottom","margin","marginX","marginY","marginLeft","marginRight","marginTop","marginBottom","width","height","minWidth","minHeight","maxWidth","maxHeight","htmlTag","position","overflow","zIndex","top","bottom","left","right","refHandler"]);return n.createElement(g1,i({backgroundColor:r,backgroundImage:l,contentColor:o,borderColor:s,radius:c,borderSide:m,shadow:f,padding:p,paddingLeft:b||$,paddingRight:b||x,paddingTop:w||y,paddingBottom:w||I,margin:N,marginLeft:Q||re,marginRight:Q||le,marginTop:P||G,marginBottom:P||Y,width:q,height:ce,minWidth:ae,minHeight:te,maxWidth:U,maxHeight:ue,as:ne,position:xe,top:se,bottom:nt,left:Ve,right:Pe,overflow:De,zIndex:B,borderWidth:v,ref:Z=>Re&&Re(Z)},O),a)},pe=p1,Ee={small:{height:u(4),width:u(5),iconSize:2,padding:u(1.75),withIconPadding:u(4.5),passwordAdditionalPadding:u(.5),textSize:"small",radius:"var(--lns-radius-150)"},medium:{height:"var(--lns-formFieldHeight)",width:u(6),iconSize:3,padding:"var(--lns-formFieldHorizontalPadding)",withIconPadding:u(5.5),passwordAdditionalPadding:u(.5),textSize:"medium",radius:"var(--lns-radius-175)"},large:{height:u(7),width:u(6),iconSize:3,padding:"var(--lns-formFieldHorizontalPadding)",withIconPadding:u(5.5),passwordAdditionalPadding:u(.5),textSize:"large",radius:"var(--lns-radius-250)"}},f1=e=>{let t=e.addOn?Ee[e.inputSize].withIconPadding:Ee[e.inputSize].padding;return e.type==="password"&&(t=`calc(${Ee[e.inputSize].passwordAdditionalPadding} + ${t})`),t},b1=h.Z.input`
  -webkit-appearance: none;
  font-family: inherit;
  width: 100%;
  height: ${e=>Ee[e.inputSize].height};
  border: none;
  color: inherit;
  background-color: ${d("formFieldBackground")};
  transition: 0.3s box-shadow;
  padding-top: 0;
  padding-bottom: 0;
  padding-left: ${e=>e.icon?Ee[e.inputSize].withIconPadding:Ee[e.inputSize].padding};
  padding-right: ${e=>f1(e)};
  border-radius: ${e=>Ee[e.inputSize].radius};
  box-shadow: inset 0 0 0
    ${e=>e.hasError?"var(--lns-formFieldBorderWidthFocus) var(--lns-color-danger)":"var(--lns-formFieldBorderWidth) var(--lns-color-formFieldBorder)"};

  ${e=>Se(Ee[e.inputSize].textSize)};

  &:hover {
    box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidthFocus)
      var(--lns-color-blurple);
  }

  &:focus {
    outline: 1px solid transparent;
    box-shadow: var(--lns-formFieldBorderShadowFocus);
  }

  &:disabled {
    color: ${d("disabledContent")};
    background-color: ${d("disabledBackground")};
  }

  &:disabled:hover {
    box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidth)
      var(--lns-color-formFieldBorder);
  }

  &::placeholder {
    color: ${d("bodyDimmed")};
  }
`,C1=h.Z.div`
  position: relative;
  width: 100%;
`,w1=h.Z.div`
  position: absolute;
  pointer-events: none;
  width: ${e=>Ee[e.size].width};
  // Width isn't equal to iconPadding because we want more space on the left than the right
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
`,E1=h.Z.img`
  height: 100%;
  width: auto;
  min-width: 100%;
  min-height: 100%;
  object-fit: cover;
  opacity: ${({isDisabled:e})=>e?.5:1};
`,y1=h.Z.div`
  position: absolute;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  right: 0;
  width: ${e=>Ee[e.size].width};
  top: 50%;
  transform: translateY(-50%);
`,z1=(0,n.forwardRef)((e,t)=>{var a=e,{placeholder:r,onFocus:l,onChange:o,onBlur:s,onKeyDown:c,isDisabled:m,icon:v,type:f="text",value:p,hasError:b,size:w="medium",addOn:$}=a,x=E(a,["placeholder","onFocus","onChange","onBlur","onKeyDown","isDisabled","icon","type","value","hasError","size","addOn"]);const y=n.createElement(b1,i({type:f,placeholder:r,onFocus:l,onChange:o,onBlur:s,onKeyDown:c,disabled:m,icon:v,ref:t,value:p,hasError:b,inputSize:w,addOn:$},x));return v||$?n.createElement(C1,null,v&&n.createElement(w1,{size:w},typeof v=="string"?n.createElement(pe,{radius:"50",width:Ee[w].iconSize,height:Ee[w].iconSize,overflow:"hidden"},n.createElement(Ke,{alignment:"center"},n.createElement(E1,{src:v,alt:"",isDisabled:m}))):n.createElement(ie,{icon:v,size:Ee[w].iconSize,color:d(m?"disabledContent":"body")})),y,$&&n.createElement(y1,{size:w},$)):y}),xr=z1,$r={start:"flex-start",center:"center",end:"flex-end",stretch:"stretch"},Mr=!1,xt=e=>Array.isArray(e)?e:[e],kr=(e,t)=>{if(e.length===t)return e;const a=e[e.length-1];return[...Array(t)].map((r,l)=>e[l]||a)},x1=(e,t)=>{const a=Math.max(xt(e).length,xt(t).length),r=kr(xt(t),a),l=kr(xt(e),a),o="& > * + *",s=r.map((m,v)=>{const f=`${Me(m)} 0 0 0`,p=`0 0 0 ${Me(m)}`,b=l[v]==="column"?f:p;return`${o}{ margin: ${b}; }`}),c=l.map(m=>`flex-direction: ${m}`);return qe(s)+qe(c)},$1=h.Z.div`
  display: flex;
  flex-wrap: wrap;
  ${e=>x1(e.flexDirection,e.gap)};
  ${e=>ar(e.flexAlign,$r)};
  ${e=>e.isSpread&&$a("justify-content",["space-between","initial"],e.isSpread)};

  & > * {
    flex-shrink: 0;
  }
`,Yi=e=>{var t=e,{children:a,gap:r,direction:l="row",alignment:o="start",isSpread:s,htmlTag:c="div"}=t,m=E(t,["children","gap","direction","alignment","isSpread","htmlTag"]);return Mr||(console.warn(Ra),Mr=!0),React12.createElement($1,i({gap:r,flexDirection:l,flexAlign:o,isSpread:s,as:c},m),a)},Xi=Object.keys($r),Ji=null,M1=h.Z.div`
  display: grid;
  ${e=>we("align-items",e.alignItems)};
  ${e=>we("justify-content",e.justifyContent)};
  ${e=>e.justifyItems&&we("justify-items",e.justifyItems)};
  ${e=>e.alignContent&&we("align-content",e.alignContent)};
  ${e=>!e.columns&&!e.rows&&!e.autoFlow&&"grid-auto-flow: column"};
  ${e=>lr(e.columns,"columns")};
  ${e=>lr(e.rows,"rows")};
  ${e=>C("gap",e.gap)};
  ${e=>C("width",e.width)};
  ${e=>C("height",e.height)};
  ${e=>C("min-width",e.minWidth)};
  ${e=>C("min-height",e.minHeight)};
  ${e=>C("max-width",e.maxWidth)};
  ${e=>C("max-height",e.maxHeight)};

  ${e=>e.autoFlow&&we("grid-auto-flow",e.autoFlow)};
  ${e=>e.columns&&e.autoFlow&&we("grid-auto-flow",e.autoFlow)};
  ${e=>or(e.as)};
`,k1=e=>{var t=e,{children:a,width:r,height:l,minWidth:o,minHeight:s,maxWidth:c,maxHeight:m,gap:v,columns:f,rows:p,alignItems:b="center",justifyContent:w="start",justifyItems:$,alignContent:x,autoFlow:y,htmlTag:I="div",className:N,style:Q}=t,P=E(t,["children","width","height","minWidth","minHeight","maxWidth","maxHeight","gap","columns","rows","alignItems","justifyContent","justifyItems","alignContent","autoFlow","htmlTag","className","style"]);return(N||Q)&&console.warn(It),n.createElement(M1,i({alignItems:b,as:I,justifyContent:w,justifyItems:$,alignContent:x,gap:v,columns:f,rows:p,width:r,height:l,minWidth:o,minHeight:s,maxWidth:c,maxHeight:m,autoFlow:y},P),a)},Ge=k1;function Lr(){return n.createElement(D.Z,{label:"",testId:"ads-refreshed-icon"})}var L1=h.Z.div`
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
`,Qi=({children:e,errorActive:t,errorMessage:a="Oops, that didn't work. Try again."})=>t?React15.createElement(L1,null,React15.createElement(Ge,{autoFlow:"row",gap:"small"},e,a?React15.createElement(Ge,{gap:"xsmall"},React15.createElement(ie,{icon:React15.createElement(Lr,null),size:2,color:"danger"}),React15.createElement(Ie,{size:"body-sm",color:"danger"},a)):null)):React15.createElement(React15.Fragment,null,e),qi=null,R1={start:"flex-start",center:"center",end:"flex-end"},_1=h.Z.div`
  display: flex;
  ${e=>ar(e.alignment,R1)};

  & > * + * {
    ${e=>e.gap&&C("margin-left",e.gap)};
  }
`,H1=h.Z.div`
  min-width: 0px;
  flex-shrink: 0;
  ${e=>C("width",e.width)};
  ${e=>C("max-width",e.maxWidth)};
  ${e=>e.width?"flex-shrink: 0":"flex: 1 1 0%"};
`,S1=e=>{var t=e,{width:a,maxWidth:r,children:l}=t,o=E(t,["width","maxWidth","children"]);return console.warn(cr),n.createElement(H1,i({width:a,maxWidth:r},o),l)},I1=class extends n.Component{render(){return console.warn(cr),n.createElement(_1,i({},this.props),this.props.children)}};I1.Section=S1;var e0=null,ht={small:{size:u(3),iconSize:2.25,radius:"var(--lns-radius-100)"},medium:{size:u(4),iconSize:3,radius:"var(--lns-radius-150)"},large:{size:u(5),iconSize:4,radius:"var(--lns-radius-175)"}},B1=h.Z.button`
  background-color: ${e=>d(e.isActive?"backgroundActive":e.backgroundColor)||"transparent"};
  border: none;
  appearance: none;
  cursor: pointer;
  padding: 0;
  width: ${e=>ht[e.size].size};
  height: ${e=>ht[e.size].size};
  position: relative;
  outline: 1px solid transparent;
  transition: 0.6s background-color;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  vertical-align: middle;
  border-radius: ${e=>ht[e.size].radius};
  font: inherit;

  &:hover {
    transition: 0.3s background-color;
    background-color: ${e=>d(e.isActive?"backgroundActive":"backgroundHover")};
  }

  &:active {
    transition: 0s background-color;
    background-color: ${d("backgroundActive")};
  }

  &:disabled {
    color: ${d("disabledContent")};
    pointer-events: none;
  }

  &:before {
    content: '';
    width: 100%;
    height: 100%;
    display: block;
    position: absolute;
    top: 0;
    border-radius: ${e=>ht[e.size].radius};
  }

  &:focus-visible:before,
  &:focus:before {
    ${ke()};
  }

  &:focus::-moz-focus-inner {
    border: 0;
  }
`,Rr=n.forwardRef((e,t)=>{var a=e,{altText:r,icon:l,onClick:o,iconColor:s="body",backgroundColor:c,isActive:m,isDisabled:v,size:f="medium"}=a,p=E(a,["altText","icon","onClick","iconColor","backgroundColor","isActive","isDisabled","size"]);return n.createElement(B1,i({"aria-label":r,onClick:o,isActive:m,disabled:v,size:f,backgroundColor:c,ref:t},p),n.createElement(ie,{icon:l,size:ht[f].iconSize,color:v?"disabledContent":s}))});Rr.displayName="IconButton";var $t=Rr,O1=e=>n.createElement("svg",i({width:12,height:9,viewBox:"0 0 12 9",fill:"none"},e),n.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M11.707.293a1 1 0 010 1.414l-7 7a1 1 0 01-1.414 0l-3-3a1 1 0 011.414-1.414L4 6.586 10.293.293a1 1 0 011.414 0z",fill:"currentColor"})),D1=e=>n.createElement("svg",i({width:12,height:2,viewBox:"0 0 12 2",fill:"none"},e),n.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 1a1 1 0 011-1h10a1 1 0 110 2H1a1 1 0 01-1-1z",fill:"currentColor"})),V1=h.Z.div`
  display: block;
  position: relative;
`,W1=h.Z.input`
  height: 100%;
  margin: 0;
  opacity: 0;
  position: absolute;
  width: 100%;

  &:not(:disabled) {
    cursor: pointer;

    & ~ .CheckboxBox {
      border: 2px solid ${d("body")};
    }

    &:checked ~ .CheckboxBox,
    &:indeterminate ~ .CheckboxBox {
      background-color: ${d("body")};
    }
  }

  &:disabled,
  &:disabled ~ .CheckboxBox {
    pointer-events: none;
  }

  &:disabled ~ .CheckboxBox {
    background-color: ${d("disabledBackground")};

    .Icon {
      color: ${d("disabledContent")};
    }
  }

  &:focus-visible ~ .CheckboxBox {
    ${ke()};
  }

  & ~ .CheckboxBox .Icon {
    display: none;
    color: ${d("background")};
  }

  &:checked ~ .CheckboxBox .IconCheck {
    display: block;
  }

  &:indeterminate ~ .CheckboxBox .IconMinus {
    display: block;
  }
`,A1=h.Z.span`
  cursor: pointer;
  width: ${u(2.25)};
  height: ${u(2.25)};
  border-radius: ${u(.5)};
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
`,P1=(0,n.forwardRef)((e,t)=>{var a=e,{isDisabled:r,isChecked:l,isIndeterminate:o,onFocus:s,onChange:c,onBlur:m}=a,v=E(a,["isDisabled","isChecked","isIndeterminate","onFocus","onChange","onBlur"]);const f=(0,n.useRef)(),p=t||f,b=d(r?"disabledContent":"currentColor");return(0,n.useEffect)(()=>{p.current.indeterminate=o}),n.createElement(V1,null,n.createElement(W1,i({type:"checkbox",disabled:r,checked:l,onFocus:s,onChange:c,onBlur:m,ref:p,"aria-checked":l},v)),n.createElement(A1,{className:"CheckboxBox"},n.createElement(D1,{className:"Icon IconMinus",color:b}),n.createElement(O1,{className:"Icon IconCheck",color:b})))}),T1=P1,tt={small:{textSize:"small",iconSize:2.25,height:u(3),xSpace:u(1),radius:"var(--lns-radius-100)"},medium:{textSize:"medium",iconSize:3,height:u(4),xSpace:u(1.5),radius:"var(--lns-radius-150)"},large:{textSize:"large",iconSize:4,height:u(6),xSpace:u(3),radius:"var(--lns-radius-200)"}},F1=h.Z.button`
  background-color: ${e=>e.isActive?d("backgroundActive"):"transparent"};
  display: inline-flex;
  vertical-align: middle;
  align-items: center;
  font: inherit;
  text-decoration: none;
  border: none;
  appearance: none;
  height: ${e=>tt[e.size].height};
  cursor: pointer;
  transition: 0.6s background-color;
  color: ${e=>d(e.color||"body")};
  ${Fe("bold")};
  border-radius: ${e=>tt[e.size].radius};
  ${e=>Se(tt[e.size].textSize)};
  padding: 0 ${e=>tt[e.size].xSpace};
  ${e=>e.offsetSide&&`margin-${e.offsetSide}: calc(-1 * ${tt[e.size].xSpace})`};

  &:focus,
  &:focus-visible {
    outline: 1px solid transparent;
  }

  &:focus-visible {
    ${ke()};
  }

  &::-moz-focus-inner {
    border: 0;
  }

  &:hover {
    transition: 0.3s background-color;
    background-color: ${e=>d(e.isActive?"backgroundActive":"backgroundHover")};
  }

  &:active {
    transition: 0s background-color;
    background-color: ${d("backgroundActive")};
  }

  &:disabled {
    color: ${d("disabledContent")};
    pointer-events: none;
  }
`,Z1=n.forwardRef((e,t)=>{var a=e,{onClick:r,size:l="medium",children:o,icon:s,iconPosition:c="left",isActive:m,isDisabled:v,htmlTag:f,offsetSide:p}=a,b=E(a,["onClick","size","children","icon","iconPosition","isActive","isDisabled","htmlTag","offsetSide"]);const w=n.createElement(pe,{paddingLeft:c==="right"&&"small",paddingRight:c==="left"&&"small",htmlTag:"span"},n.createElement(ie,{icon:s,size:tt[l].iconSize,color:v?"disabledColor":void 0}));return n.createElement(F1,i({onClick:r,size:l,icon:s,iconPosition:c,disabled:v,isActive:m,as:f,offsetSide:p,ref:t},b),s&&c==="left"&&w,o,s&&c==="right"&&w)});Z1.displayName="TextButton";var t0=null,Tt=e=>{var t,a;const r=(a=(t=e?.())==null?void 0:t.getRootNode)==null?void 0:a.call(t);if(String(r)==="[object ShadowRoot]"){r.createElement=(...o)=>r.ownerDocument.createElement(...o);const l=r.createElement("div");return l.id="a11y-status-message",l.style.display="none",r.appendChild(l),{document:r,addEventListener:r.addEventListener.bind(r),removeEventListener:r.removeEventListener.bind(r)}}return typeof window>"u"?null:window},Ue=e=>typeof e=="string"?e:typeof e=="number"||typeof e=="boolean"||typeof e=="bigint"?e.toString():e==null?"":j1(e)?Array.from(e).map(Ue).join(""):typeof e=="object"&&"props"in e&&e.props&&e.props.children!==void 0?Ue(e.props.children):"",j1=e=>typeof e[Symbol.iterator]=="function";function _r(){return n.createElement("span",{"aria-hidden":!0,"data-testid":"ads-refreshed-icon"},n.createElement("svg",{viewBox:"-2 -2 16 16"},n.createElement("path",{fill:"currentColor",fillRule:"evenodd",d:"M2.03 3.97 6 7.94l3.97-3.97 1.06 1.06-4.5 4.5a.75.75 0 0 1-1.06 0l-4.5-4.5z",clipRule:"evenodd"})))}function N1(){return n.createElement(W.Z,{label:"",testId:"ads-refreshed-icon"})}var Ft={left:"bottom-start",right:"bottom-end",topLeft:"top-start",topRight:"top-end",leftSide:"left-start",rightSide:"right-start"},U1=h.Z.div`
  background-color: ${d("overlay")};
  display: flex;
  flex-direction: column;
  margin: 0;
  ${e=>C("min-width",e.minWidth)};
  ${e=>C("max-width",e.maxWidth)};
  ${e=>C("max-height",e.maxHeight)};
  z-index: ${e=>e.zIndex};
  border: 1px solid ${d("border")};
  ${ct("medium")};
  ${ee("250")};
`,K1=h.Z.ul`
  padding: ${e=>e.search?`0 ${u(1.5)} ${u(1.5)} ${u(1.5)}`:u(1.5)};
  list-style: none;
  overflow: auto;
  margin: 0;
`,G1=h.Z.li`
  display: ${({hidden:e})=>e?"none":"grid"};
  grid-auto-flow: column;
  grid-template-columns: ${e=>e.columns};
  ${C("grid-gap","small")};
  ${ee("175")};
  align-items: center;
  min-height: ${u(5)};
  padding: 0 ${u(2)};
  cursor: ${e=>e.isDisabled?"default":"pointer"};
  &:focus-visible {
    outline: 1px solid transparent;
    ${pt()};
  }
  ${e=>e.isHighlighted&&!e.isDisabled&&`
    background-color: ${d("backgroundHover")};
  `};
  ${e=>e.keyboardMove&&e.isHighlighted&&!e.isDisabled&&`
    outline: 1px solid transparent;
    ${pt()};
  `};
  ${e=>e.hasDivider&&`
    position: relative;
    margin-top: ${u(3)};
    &:before {
      content: '';
      border-top: 1px solid ${d("border")};
      position: absolute;
      top: ${u(-1.5)};
      left: ${u(-1.5)};
      width: calc(100% + ${u(3)});
    }
  `};
`,Y1=h.Z.img`
  height: 100%;
  width: auto;
  min-width: 100%;
  min-height: 100%;
  object-fit: cover;
  opacity: ${({isDisabled:e})=>e?.5:1};
`,Zt=e=>{var t=e,{isDisabled:a,isHighlighted:r,isSelected:l,icon:o,hasDivider:s,children:c,menuItemRole:m,keyboardMove:v}=t,f=E(t,["isDisabled","isHighlighted","isSelected","icon","hasDivider","children","menuItemRole","keyboardMove"]);const w=`${o?"auto":""} 1fr ${l?"auto":""}`,$=a?"disabledContent":void 0,x=m?L(i({},f),{role:m}):f;return n.createElement(G1,i({isHighlighted:r,isDisabled:a,keyboardMove:v,columns:w,hasDivider:s,tabIndex:a?-1:0,"data-highlighted":r||void 0},x),o&&(typeof o=="string"?n.createElement(pe,{radius:"50",width:3,height:3,overflow:"hidden"},n.createElement(Ke,{alignment:"center"},n.createElement(Y1,{src:o,alt:"",isDisabled:a}))):n.createElement(ie,{icon:o,color:$})),n.createElement(Ie,{color:$,hasEllipsis:!0},c),l&&n.createElement(ie,{icon:n.createElement(N1,null),color:$}))},X1=e=>{var t=e,{position:a,zIndex:r,minWidth:l,maxWidth:o,maxHeight:s,children:c,role:m,downshiftMenuProps:v=()=>null,search:f}=t,p=E(t,["position","zIndex","minWidth","maxWidth","maxHeight","children","role","downshiftMenuProps","search"]);const b=m?L(i({},v()),{role:m}):i({},v());return n.createElement(U1,i(i({minWidth:l,maxWidth:o,maxHeight:s,zIndex:r,position:a},b),p),f&&f,n.createElement(K1,{search:f},c))},Ye=X1;function J1(){return n.createElement(M.Z,{label:"",testId:"ads-refreshed-icon"})}var Q1=h.Z.div`
  padding: ${u(1.5)} ${u(1.5)} 0;
  margin-bottom: ${u(1.5)};
  position: sticky;
  top: 0;
`,q1=({ariaLabel:e,placeholder:t,value:a,onChange:r,getInputProps:l})=>n.createElement(Q1,null,n.createElement(xr,i({"aria-label":e,icon:n.createElement(J1,null)},l({placeholder:t,value:a,onChange:r,type:"text"})))),Hr=q1,el=h.Z.div`
  position: relative;
`,tl=h.Z.button`
  appearance: none;
  font: inherit;
  text-align: left;
  display: grid;
  grid-auto-flow: column;
  grid-template-columns: ${e=>e.columns};
  ${C("grid-gap","small")};
  align-items: center;
  cursor: pointer;
  width: 100%;
  min-height: ${u(4.5)};
  padding: 0 ${u(1.5)} 0 var(--lns-formFieldHorizontalPadding);
  color: ${d("body")};
  border: none;
  background-color: ${d("formFieldBackground")};
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
    color: ${d("disabledContent")};
    background-color: ${d("disabledBackground")};
    cursor: default;
  }
`,rl=h.Z.img`
  height: 100%;
  width: auto;
  min-width: 100%;
  min-height: 100%;
  object-fit: cover;
  opacity: ${({isDisabled:e})=>e?.5:1};
`,al=h.Z.ul`
  list-style: none;
  margin: 0;
  padding: 0;
`,nl=h.Z.span`
  color: var(--lns-color-red);
  margin-top: var(--lns-space-xsmall);
  display: block;
  width: 100%;
  grid-column-start: 1;
  grid-column-end: 3;
`,Mt=e=>Array.isArray(e)&&e.length>0&&"group"in e[0],jt=({options:e,selectedOptionValue:t})=>{if(!e||!t)return{icon:null,title:null};if(Mt(e))for(const a of e){const r=a.items.find(l=>l.value===t);if(r)return r}else return e.find(r=>r.value===t)||{icon:null,title:null};return{icon:null,title:null}},Sr=({options:e,selectedItem:t,selectedOptionValue:a})=>{if(t)return t.icon;if(a)return jt({options:e,selectedOptionValue:a}).icon},ll=({options:e,selectedItem:t,selectedOptionValue:a,selectPlaceholder:r})=>t?t.title:a?jt({options:e,selectedOptionValue:a}).title:r,Ir=({selectedItem:e,getInputProps:t,getToggleButtonProps:a,ariaMenuName:r,isOpen:l})=>{const o=e?`selected value is ${e.title}`:"no value selected",s=a?.()["aria-label"];return{"aria-expanded":l,"aria-activedescendant":t()["aria-activedescendant"],"aria-label":[r,s,o].filter(Boolean).join(", ")}},ol=({getToggleButtonProps:e,inputValue:t,selectedItem:a,selectedOptionValue:r,selectPlaceholder:l,isDisabled:o,options:s,getInputProps:c,ariaMenuName:m,hasError:v,isOpen:f})=>{const p=Sr({options:s,selectedItem:a,selectedOptionValue:r}),b=Boolean(p),w=!r&&!a,x=`${b?"auto":""} 1fr auto`,y=o?"disabledContent":void 0;return React26.createElement(tl,L(i(i({},e()),Ir({selectedItem:a,getInputProps:c,getToggleButtonProps:e,ariaMenuName:m,isOpen:f})),{hasValue:t||r,disabled:o,columns:x,hasError:v}),b&&(typeof p=="string"?React26.createElement(pe,{radius:"50",width:3,height:3,overflow:"hidden"},React26.createElement(Ke,{alignment:"center"},React26.createElement(rl,{src:p,alt:"",isDisabled:o}))):React26.createElement(ie,{icon:Sr({options:s,selectedItem:a,selectedOptionValue:r}),color:y})),React26.createElement(Ie,{hasEllipsis:!0,color:w?"bodyDimmed":"inherit"},ll({options:s,selectedItem:a,selectedOptionValue:r,selectPlaceholder:l})),React26.createElement(ie,{icon:React26.createElement(_r,null),color:y}))},il=({selectedOptionValue:e,selectedItem:t,trigger:a,getToggleButtonProps:r,options:l,selectPlaceholder:o,isDisabled:s,getInputProps:c,ariaMenuName:m,hasError:v,errorMessage:f,isOpen:p})=>{const b=()=>i(i({},r()),Ir({selectedItem:t,getInputProps:c,getToggleButtonProps:r,ariaMenuName:m,isOpen:p})),$=L(i({},(()=>{if(t)return t;if(e)return jt({options:l,selectedOptionValue:e})})()),{placeholder:o,isDisabled:s,hasError:v,errorMessage:f});return a($,b())},Br=(e,t)=>{if(Mt(t))for(const a of t){const r=a.items.find(l=>l.value===e);if(r)return r}else return t.find(a=>a.value===e)},Or=(e,t,a,r,l,o,s,c)=>{const m=!a&&e.value===r||a&&a.value===e.value;return React26.createElement(Zt,L(i({key:t,getItemProps:o,icon:e.icon,hidden:e.hidden},o({key:`${e.value}-${t}`,index:t,item:e,disabled:e.isDisabled,"aria-selected":m,onMouseMove:()=>{s&&c(!1)}})),{isDisabled:e.isDisabled,hasDivider:e.hasDivider,isHighlighted:l===t,keyboardMove:s&&l===t,isSelected:m}),e.title)},sl=e=>{var t=e,{options:a,selectedItem:r,selectedOptionValue:l,highlightedIndex:o,getItemProps:s,search:c,keyboardMove:m,setKeyboardMove:v}=t,f=E(t,["options","selectedItem","selectedOptionValue","highlightedIndex","getItemProps","search","keyboardMove","setKeyboardMove"]);if(!Mt(a))return React26.createElement(Ye,i({search:c},f),a.map((b,w)=>Or(b,w,r,l,o,s,m,v)));let p=0;return React26.createElement(Ye,i({search:c},f),a.map(b=>{const w=`group-${b.group.replace(/\s+/g,"-")}`;return React26.createElement("li",{key:w},React26.createElement(yt,{left:"medium",top:"small",bottom:"xsmall"},React26.createElement(Ie,{id:w,size:"body-sm",fontWeight:"bold"},b.group)),React26.createElement(al,{role:"group","aria-labelledby":w},b.items.map($=>Or($,p++,r,l,o,s,m,v))))}))},r0=e=>{var t=e,{container:a,onChange:r,menuZIndex:l=1100,menuMaxWidth:o,menuMaxHeight:s=34,menuMinWidth:c,triggerOffset:m=0,ariaMenuName:v,selectedOptionValue:f,onOuterClick:p,options:b,placeholder:w,menuPosition:$="left",isDisabled:x,onOpenChange:y,trigger:I,hasError:N,errorMessage:Q="Oops, that didn't work.",search:P}=t,re=E(t,["container","onChange","menuZIndex","menuMaxWidth","menuMaxHeight","menuMinWidth","triggerOffset","ariaMenuName","selectedOptionValue","onOuterClick","options","placeholder","menuPosition","isDisabled","onOpenChange","trigger","hasError","errorMessage","search"]);const le=Tt(a),[G,Y]=useState(!1),[q,ce]=useState(!1),[ae,te]=useState(""),U=O=>{const Z=O.target.value;te(Z)},[ue,ne]=useState(Br(f,b)),De={itemToString:O=>O?O.value:"",onChange:O=>{ne(O),r&&r(O||"")},onOuterClick:p,environment:le,selectedItem:ue,isOpen:G};le&&(De.environment=le);const{layerProps:B,triggerProps:se,renderLayer:nt,triggerBounds:Ve}=useLayer({isOpen:G,container:a,ResizeObserver,placement:Ft[$],auto:!0,snap:!0,triggerOffset:m});useEffect2(()=>{const O=Br(f,b);O?.value!==ue?.value&&ne(O)},[f,b,ue]),useEffect2(()=>{y&&y(G)},[G,y]);const Pe=(O,Z)=>{if(Z.isOpen!==void 0){if(Z.type===Downshift.stateChangeTypes.keyDownEscape)return Y(!1),{isOpen:!1};Y(Z.isOpen)}return Z},Re=O=>{switch(O.key){case"ArrowDown":case"ArrowUp":case"ArrowLeft":case"ArrowRight":case"Enter":case" ":case"Tab":case"Escape":ce(!0);break;default:break}};return b=useMemo(()=>{if(P){if(Mt(b)){let O;return P.searchType==="startsWith"?O=b.map(Z=>L(i({},Z),{items:Z.items.filter(We=>Ue(We.title).toLowerCase().startsWith(ae.toLowerCase()))})):O=b.map(Z=>L(i({},Z),{items:Z.items.filter(We=>Ue(We.title).toLowerCase().includes(ae.toLowerCase()))})),O.reduce((Z,We)=>(We.items.length>0&&Z.push(We),Z),[])}return P.searchType==="startsWith"?b.filter(O=>Ue(O.title).toLowerCase().startsWith(ae.toLowerCase())):b.filter(O=>Ue(O.title).toLowerCase().includes(ae.toLowerCase()))}return b},[b,ae,P]),React26.createElement(el,i({},re),React26.createElement(Downshift,L(i({},De),{stateReducer:Pe}),({getItemProps:O,getInputProps:Z,getMenuProps:We,getToggleButtonProps:_t,isOpen:X,inputValue:_e,highlightedIndex:Jt,selectedItem:lt})=>React26.createElement("div",{role:"presentation"},React26.createElement("div",i({},se),I?React26.createElement(il,{getToggleButtonProps:()=>i({},_t({onKeyDown:Re})),selectedItem:lt,selectedOptionValue:f,selectPlaceholder:w,isDisabled:x,options:b,trigger:I,getInputProps:Z,ariaMenuName:v,hasError:N,errorMessage:Q,isOpen:X}):React26.createElement(ol,{getToggleButtonProps:()=>i({},_t({onKeyDown:Re})),selectedItem:lt,selectedOptionValue:f,selectPlaceholder:w,options:b,inputValue:_e,isDisabled:x,getInputProps:Z,ariaMenuName:v,hasError:N,isOpen:X})),G&&X&&nt(React26.createElement("div",L(i({},B),{style:L(i({},B.style),{zIndex:l,width:c?"auto":Ve?.width})}),React26.createElement(sl,{options:b,selectedItem:lt,selectedOptionValue:f,highlightedIndex:Jt,getItemProps:O,position:$,downshiftMenuProps:()=>We({onKeyDown:Re}),maxWidth:o,maxHeight:s,minWidth:c,search:P&&React26.createElement(Hr,{ariaLabel:P.searchPlaceholder,placeholder:P.searchPlaceholder,value:ae,onChange:U,getInputProps:Z}),keyboardMove:q,setKeyboardMove:ce}))),N&&!G&&React26.createElement(nl,null,Q))))},a0=null;function dl(e,t){const a=document;(0,n.useLayoutEffect)(()=>{const r=a?.documentElement,l=a?.body;if(!(a==null||!r||!l)){if(t){const o=window.innerWidth-r.clientWidth,s=parseInt(window.getComputedStyle(l).getPropertyValue("padding-right"),10)||0;switch(e){case"html":{r.style.position="relative",r.style.overflow="hidden",l.style.paddingRight=`${s+o}px`;break}case"body":{l.style.setProperty("position","relative"),l.style.setProperty("overflow","hidden"),l.style.setProperty("padding-right",`${s+o}px`);break}default:return}}return()=>{switch(e){case"html":{r.style.position="",r.style.overflow="",l.style.paddingRight="";break}case"body":{l.style.removeProperty("position"),l.style.removeProperty("overflow"),l.style.removeProperty("padding-right");break}default:return}}}},[a,t,e])}var Dr=dl,Vr=300,cl=h.Z.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: calc(100vh - calc(100vh - 100%));
  height: 100dvh;
  height: -webkit-fill-available;
  background: ${e=>d(e.backgroundColor)};
  z-index: ${e=>e.zIndex};
  overflow: hidden;
`,ul=h.Z.div`
  overflow: auto;
  height: 100%;
`,Wr=n.forwardRef((e,t)=>{var a=e,{children:r,isOpen:l,zIndex:o=1e3,backgroundColor:s="backdropDark"}=a,c=E(a,["children","isOpen","zIndex","backgroundColor"]);const{stage:m,shouldMount:v}=(0,S.Yz)(l,Vr);return Dr("html",l),n.createElement(n.Fragment,null,v&&n.createElement(cl,i({ref:t,backgroundColor:s,zIndex:o,style:{transition:`opacity ${Vr}ms`,opacity:m==="enter"?1:0}},c),n.createElement(ul,null,r)))});Wr.displayName="Backdrop";var hl=Wr;function Nt(){return n.createElement(oe.Z,{label:"",testId:"ads-refreshed-icon"})}var ml="70vh",vl=h.Z.div`
  display: grid;
  grid-template-rows: ${e=>e.rows};
  position: relative;
`,gl=h.Z.dialog`
  top: ${e=>Ht(Me(e.maxHeight),e.placement).top};
  background-color: ${d("overlay")};
  color: ${d("body")};
  bottom: ${e=>Ht(e.maxHeight,e.placement).bottom};
  ${ct("large")};
  ${ee("xlarge")};
  // Unsets bottom-radius for bottom-aligned modals
  border-bottom-left-radius: ${e=>e.placement==="bottom"?"initial":void 0};
  border-bottom-right-radius: ${e=>e.placement==="bottom"?"initial":void 0};
  ${e=>C("max-height",e.maxHeight)};
  ${e=>C("max-width",e.maxWidth)};
  margin: 0 auto;
  position: ${e=>Ht(e.maxHeight,e.placement).position};
  overflow: auto;
  width: 100%;
  // TODO: LNS-150: Bake dialog resets into native resets file
  border: 0;
  padding: 0;
  &::backdrop {
    background: var(--lns-color-overlay);
  }
`,pl=h.Z.div`
  position: absolute;
  top: ${u(1.5)};
  right: ${u(1.5)};
  z-index: 1;
`,fl=h.Z.div`
  margin-left: auto;

  * {
    vertical-align: middle;
  }
`,bl=h.Z.div`
  padding-left: var(--lns-space-xlarge);
  padding-right: var(--lns-space-xlarge);
  padding-top: var(--lns-space-xlarge);
  padding-bottom: ${e=>e.bottom};
  flex-shrink: 0;
`,Cl=h.Z.div`
  padding-left: var(--lns-space-xlarge);
  padding-right: var(--lns-space-xlarge);
  padding-bottom: var(--lns-space-xlarge);
  padding-top: ${e=>e.hasDividers?"var(--lns-space-medium)":e.top};
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
`,wl=h.Z.div`
  display: flex;
  flex-direction: column;
  overflow: auto;
  padding-top: ${e=>e.hasTitle&&!e.noPadding?0:!e.hasTitle&&!e.noPadding?"var(--lns-space-xlarge)":0};
  padding-bottom: ${e=>e.hasButtons&&!e.noPadding?0:!e.hasButtons&&!e.noPadding?"var(--lns-space-xlarge)":0};
  padding-left: ${e=>e.noPadding?0:"var(--lns-space-xlarge)"};
  padding-right: ${e=>e.noPadding?0:"var(--lns-space-xlarge)"};
  border-style: solid;
  border-color: ${d("border")};
  border-width: ${e=>e.hasDividers?"1px 0":"0"};
`,El=h.Z.div`
  overflow: auto;

  ${e=>Ar(e.maxHeight)};

  & > * {
    ${e=>Ar(e.maxHeight)};
  }
`,Ar=e=>typeof e=="number"?C("max-height",e):"max-height: "+e,yl=e=>{var t=e,{children:a,onCloseClick:r,isOpen:l,maxWidth:o=60,maxHeight:s=ml,placement:c="center",ariaLabel:m,ariaModal:v,ariaLabelledBy:f,ref:p,removeClose:b,initialFocus:w}=t,$=E(t,["children","onCloseClick","isOpen","maxWidth","maxHeight","placement","ariaLabel","ariaModal","ariaLabelledBy","ref","removeClose","initialFocus"]);const x=y=>{y.key==="Escape"&&(y.preventDefault(),b||r(y))};return(0,n.useEffect)(()=>(window.addEventListener("keydown",x),()=>{window.removeEventListener("keydown",x)}),[l,r]),Dr("html",l),n.createElement(ge(),{active:l,focusTrapOptions:i({clickOutsideDeactivates:!1,allowOutsideClick:!0},w!==void 0?{initialFocus:w}:{})},n.createElement(gl,i({open:l,maxWidth:o,maxHeight:s,placement:c,onClick:y=>y.stopPropagation(),ref:p,"aria-label":m,"aria-modal":v,"aria-labelledby":f},$),!b&&r&&n.createElement(pl,null,n.createElement($t,{altText:"Close",icon:n.createElement(Nt,null),onClick:r})),n.createElement(El,L(i({},b?{tabIndex:0}:{tabIndex:-1}),{maxHeight:s}),a)))},n0=n.forwardRef((e,t)=>{var a=e,{children:r,id:l,isOpen:o,mainButton:s,secondaryButton:c,alternativeButton:m,title:v,noPadding:f,onCloseClick:p,onBackgroundClick:b,onKeyDown:w,hasDividers:$,maxHeight:x="70vh",maxWidth:y=60,placement:I="center",zIndex:N=1e3,ariaLabel:Q,ariaModal:P=!0,ariaLabelledBy:re,initialFocus:le}=a,G=E(a,["children","id","isOpen","mainButton","secondaryButton","alternativeButton","title","noPadding","onCloseClick","onBackgroundClick","onKeyDown","hasDividers","maxHeight","maxWidth","placement","zIndex","ariaLabel","ariaModal","ariaLabelledBy","initialFocus"]),Y;const q=(0,n.useRef)(null),ce=l?`${l}-modal-title`:"modal-title",ae=!!(s||c||m),te=U=>{if(b){U.stopPropagation(),b(U);return}p(U)};return(0,n.useEffect)(()=>{if(!o||!q.current)return;const U=q.current.parentElement;return U?(Array.from(U.children).filter(ne=>ne!==q.current&&ne instanceof HTMLElement).forEach(ne=>{ne.hasAttribute("aria-hidden")||(ne.setAttribute("aria-hidden","true"),ne.setAttribute("data-lens-modal-hidden","true"))}),()=>{document.querySelectorAll("[data-lens-modal-hidden]").forEach(xe=>{xe.removeAttribute("aria-hidden"),xe.removeAttribute("data-lens-modal-hidden")})}):void 0},[o]),n.createElement(hl,i({ref:q,isOpen:o,zIndex:N},G),n.createElement(pe,{height:"100%",onClick:te,onKeyDown:w},n.createElement(yl,{ref:t,id:l,isOpen:o,maxHeight:x,maxWidth:y,placement:I,onCloseClick:p,ariaLabel:Q,ariaModal:P,ariaLabelledBy:(Y=re??ce)!=null?Y:void 0,initialFocus:le},n.createElement(vl,{rows:`${v?"auto ":""} ${r?"1fr ":""} ${ae?"auto":""}`},v&&n.createElement(bl,{bottom:r?"var(--lns-space-medium)":"var(--lns-space-xlarge)"},n.createElement(Ie,{htmlTag:"h1",variant:"title",id:ce},v)),n.createElement(wl,{noPadding:f,hasDividers:$,hasTitle:Boolean(v),hasButtons:ae},r&&r),ae&&n.createElement(Cl,{top:r?"var(--lns-space-xlarge)":0,hasDividers:$},m,n.createElement(fl,null,c&&n.createElement(yt,{right:"small",isInline:!0},c),s))))))}),l0=null,kt={neutral:{color:d("inherit"),focusRing:ke(),underline:"inactive"},primary:{color:d("primary"),focusRing:ke(),underline:"inactive"},subtle:{color:d("body"),focusRing:ke(),underline:"hover"}},Pr={enabled:z.iv`
    cursor: pointer;
  `,disabled:z.iv`
    pointer-events: none;
    color: ${d("disabledContent")};
  `},zl={isButton:z.iv`
    background: none;
    border: none;
    font: inherit;
  `},xl=h.Z.a`
  ${e=>!e.disabled&&`color: ${kt[e.variant].color}`};
  ${e=>e.disabled?Pr.disabled:Pr.enabled};
  ${e=>e.as==="button"&&zl.isButton};
  ${e=>`text-decoration: ${kt[e.variant].underline==="inactive"?"underline":"none"}`};
  border-radius: 0.28em;
  box-shadow: 0 0 0 1px transparent;
  text-underline-offset: 0.35em;
  transition: 0.3s box-shadow;
  ${e=>e.noWrap&&z.iv`
      white-space: nowrap;
    `}
  &:hover {
    ${e=>`text-decoration: ${kt[e.variant].underline==="hover"?"underline":"none"}`};
  }
  &:focus,
  &:focus-visible {
    outline: 1px solid transparent;
  }
  &:focus-visible {
    ${ke()};
  }
  &::-moz-focus-inner {
    border: 0;
  }
`,o0=e=>{var t=e,{children:a,href:r,variant:l="primary",htmlTag:o="a",isDisabled:s,noWrap:c}=t,m=E(t,["children","href","variant","htmlTag","isDisabled","noWrap"]);return React30.createElement(xl,i({href:r,variant:l,as:o,disabled:s,noWrap:c},m),a)},i0=Object.keys(kt),s0=null,Tr={small:{padding:`${u(1.5)} ${u(1.75)}`,textSize:"small"},medium:{padding:`${u(1.5)} var(--lns-formFieldHorizontalPadding)`,textSize:"medium"}},$l=h.Z.textarea`
  width: 100%;
  border: none;
  font-family: inherit;
  color: inherit;
  background-color: ${d("formFieldBackground")};
  transition: 0.3s box-shadow;
  padding: ${e=>Tr[e.size].padding};
  ${ee("250")};
  box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidth)
    ${e=>e.error?"var(--lns-color-danger)":"var(--lns-color-formFieldBorder)"};
  ${e=>Se(Tr[e.size].textSize)};
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
    color: ${d("disabledContent")};
    background-color: ${d("disabledBackground")};
  }

  &:disabled:hover {
    box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidth)
      var(--lns-color-formFieldBorder);
  }

  &::placeholder {
    color: ${d("bodyDimmed")};
  }
`,d0=n.forwardRef((e,t)=>{var a=e,{onChange:r,value:l,rows:o=4,isDisabled:s,placeholder:c,size:m="medium",resize:v="both",error:f=null}=a,p=E(a,["onChange","value","rows","isDisabled","placeholder","size","resize","error"]);return n.createElement(n.Fragment,null,n.createElement($l,i({disabled:s,onChange:r,placeholder:c,ref:t,rows:o,value:l,size:m,resize:v,error:f},p)),f?n.createElement(n.Fragment,null,n.createElement(yt,{bottom:"xmsall"}),n.createElement(Ie,{color:"danger",fontWeight:"regular",size:"body-md"},f)):null)}),c0=null,Ml=h.Z.div`
  position: relative;
`,kl=h.Z.ul`
  list-style: none;
  margin: 0;
  padding: 0;
`,Ll=h.Z.span`
  color: var(--lns-color-red);
  margin-top: var(--lns-space-xsmall);
  display: block;
  width: 100%;
  grid-column-start: 1;
  grid-column-end: 3;
`,Lt=e=>Array.isArray(e)&&e.length>0&&"group"in e[0],Fr=({options:e,selectedOptionValue:t})=>{if(!e||!t)return{icon:null,title:null};if(Lt(e))for(const a of e){const r=a.items.find(l=>l.value===t);if(r)return r}else return e.find(r=>r.value===t)||{icon:null,title:null};return{icon:null,title:null}},Rl=({options:e,selectedItem:t,selectedOptionValue:a})=>{if(t)return t.icon;if(a)return Fr({options:e,selectedOptionValue:a}).icon},_l=({options:e,selectedItem:t,selectedOptionValue:a,placeholder:r})=>t?t.title:a?Fr({options:e,selectedOptionValue:a}).title:r,Hl=({selectedItem:e,getInputProps:t,ariaMenuName:a})=>{const r=e?`selected value is ${e.title}`:"no value selected";return{"aria-activedescendant":t()["aria-activedescendant"],"aria-label":[a,r].filter(Boolean).join(", ")}},Sl=h.Z.button`
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
`,Il=h.Z.input`
  -webkit-appearance: none;
  font-family: inherit;
  width: 100%;
  height: var(--lns-formFieldHeight);
  border: none;
  color: inherit;
  background-color: ${d("formFieldBackground")};
  transition: 0.3s box-shadow;
  padding-top: 0;
  padding-bottom: 0;
  id: ${e=>e.id};
  padding-left: ${e=>e.hasIcon?u(5.5):"var(--lns-formFieldHorizontalPadding)"};
  padding-right: ${e=>e.hasAddOn?u(5.5):"var(--lns-formFieldHorizontalPadding)"};
  border-radius: var(--lns-formFieldRadius);
  box-shadow: inset 0 0 0
    ${e=>e.hasError?"var(--lns-formFieldBorderWidthFocus) var(--lns-color-danger)":"var(--lns-formFieldBorderWidth) var(--lns-color-formFieldBorder)"};

  ${C("font-size","medium")};

  &:hover:not(:disabled):not(:focus) {
    box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidthFocus)
      ${e=>e.hasError?"var(--lns-color-danger)":"var(--lns-color-blurple)"};
  }

  &:focus {
    outline: 1px solid transparent;
    box-shadow: var(--lns-formFieldBorderShadowFocus);
  }

  &:disabled {
    color: ${d("disabledContent")};
    background-color: ${d("disabledBackground")};
  }

  &:disabled:hover {
    box-shadow: inset 0 0 0 var(--lns-formFieldBorderWidth)
      var(--lns-color-formFieldBorder);
  }

  &::placeholder {
    color: ${d("bodyDimmed")};
  }
`,Bl=h.Z.div`
  position: absolute;
  pointer-events: none;
  width: ${u(6)};
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  left: 0;
`,Ol=h.Z.div`
  position: absolute;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  right: 0;
  width: ${u(6)};
  top: 50%;
  transform: translateY(-50%);
`,Dl=h.Z.div`
  position: absolute;
  top: 0;
  left: ${e=>e.hasIcon?u(5.5):"var(--lns-formFieldHorizontalPadding)"};
  right: ${u(5.5)};
  bottom: 0;
  display: flex;
  align-items: center;
  pointer-events: none;
  color: inherit;
`,Vl=h.Z.img`
  height: 100%;
  width: auto;
  min-width: 100%;
  min-height: 100%;
  object-fit: cover;
  opacity: ${({isDisabled:e})=>e?.5:1};
`,Wl=({selectedItem:e,selectedOptionValue:t,placeholder:a,isDisabled:r,options:l,getInputProps:o,ariaMenuName:s,isOpen:c,onInputFocus:m,hasError:v,hasLoader:f,inputValue:p,handleInputValueChange:b,inputRef:w,id:$})=>{const x=Rl({options:l,selectedItem:e,selectedOptionValue:t}),y=Boolean(x),I=r?"disabledContent":void 0,N=()=>{r||m()},Q=i(i({role:"combobox","aria-autocomplete":"list","aria-haspopup":"listbox","aria-expanded":c},Hl({selectedItem:e,getInputProps:o,ariaMenuName:s})),o({id:$,"aria-labelledby":void 0,disabled:r,onFocus:N,onClick:N,value:p,onBlur:()=>{b("")},onChange:re=>b(re.target.value)})),P=!p&&!t;return n.createElement(Sl,{onClick:N,disabled:r},y&&n.createElement(Bl,null,typeof x=="string"?n.createElement(pe,{radius:"50",width:3,height:3,overflow:"hidden"},n.createElement(Ke,{alignment:"center"},n.createElement(Vl,{src:x,alt:"",isDisabled:r}))):n.createElement(ie,{icon:x,color:I})),n.createElement(Il,L(i({ref:w},Q),{hasIcon:y,hasAddOn:!0,hasError:v,isDisabled:r})),!p&&n.createElement(Dl,{hasIcon:y},n.createElement(Ie,{hasEllipsis:!0,color:P?"bodyDimmed":"inherit"},_l({options:l,selectedItem:e,selectedOptionValue:t,placeholder:a}))),n.createElement(Ol,null,f?n.createElement(At,{size:"small"}):n.createElement(ie,{icon:n.createElement(_r,null),color:I})))},Zr=(e,t)=>{var a;if(Lt(t))for(const r of t){const l=r.items.find(o=>o.value===e);if(l)return l}else return(a=t.find(r=>r.value===e))!=null?a:null;return null},Al=(e,t)=>(e||null)!=t?.value,jr=(e,t,a,r,l,o)=>{const s=!a&&e.value===r||a&&a.value===e.value;return n.createElement(Zt,L(i({key:t,getItemProps:o,icon:e.icon,hidden:e.hidden},o({key:`${e.value}-${t}`,index:t,item:e,disabled:e.isDisabled,"aria-selected":s})),{isDisabled:e.isDisabled,hasDivider:e.hasDivider,isHighlighted:l===t,isSelected:s}),e.title)},Pl=e=>{var t=e,{options:a,selectedItem:r,selectedOptionValue:l,highlightedIndex:o,getItemProps:s,isLoading:c,loadingMessage:m,emptyResultsMessage:v,hasAvailableOptions:f}=t,p=E(t,["options","selectedItem","selectedOptionValue","highlightedIndex","getItemProps","isLoading","loadingMessage","emptyResultsMessage","hasAvailableOptions"]);const b=m||n.createElement(At,null),w=v||"No results";if(c)return n.createElement(Ye,i({as:"div"},p),n.createElement(pe,{padding:"large"},n.createElement(Ke,{alignment:"center"},b)));if(!f)return n.createElement(Ye,i({as:"div"},p),n.createElement(pe,{padding:"large"},n.createElement(Ke,{alignment:"center"},w)));if(!Lt(a))return n.createElement(Ye,i({},p),a.map((x,y)=>jr(x,y,r,l,o,s)));let $=0;return n.createElement(Ye,i({},p),a.map(x=>{const y=`group-${x.group.replace(/\s+/g,"-")}`;return n.createElement("li",{key:y},n.createElement(yt,{left:"medium",top:"small",bottom:"xsmall"},n.createElement(Ie,{id:y,size:"body-sm",fontWeight:"bold",htmlTag:x.headingTag||"h2"},x.group)),n.createElement(kl,{role:"group","aria-labelledby":y},x.items.map(I=>jr(I,$++,r,l,o,s))))}))},Tl=(0,n.forwardRef)((e,t)=>{var a=e,{container:r,onOptionChange:l,onInputValueChange:o,menuZIndex:s=1100,menuMaxWidth:c,menuMaxHeight:m=34,menuMinWidth:v,ariaMenuName:f,selectedOptionValue:p,onOuterClick:b,options:w,placeholder:$,menuPosition:x="left",isDisabled:y,onOpenChange:I,isLoading:N,loadingMessage:Q,emptyResultsMessage:P,errorMessage:re,id:le}=a,G=E(a,["container","onOptionChange","onInputValueChange","menuZIndex","menuMaxWidth","menuMaxHeight","menuMinWidth","ariaMenuName","selectedOptionValue","onOuterClick","options","placeholder","menuPosition","isDisabled","onOpenChange","isLoading","loadingMessage","emptyResultsMessage","errorMessage","id"]);const Y=Tt(r),q=(0,n.useRef)(null),ce=(0,n.useCallback)(X=>{q.current=X,t&&(typeof t=="function"?t(X):t.current=X)},[t]),[ae,te]=(0,n.useState)(""),[U,ue]=(0,n.useState)(!1),[ne,xe]=(0,n.useState)(Zr(p,w)),[De,B]=(0,n.useState)(ne),se=X=>{te(X),o&&o(X)},Ve={itemToString:X=>X?X.value:"",onChange:X=>{const _e=X||null;B(_e),l&&l(_e)},onOuterClick:b,environment:Y,selectedItem:De,isOpen:U};Y&&(Ve.environment=Y);const{layerProps:Pe,triggerProps:Re,renderLayer:O,triggerBounds:Z}=(0,He.sJ)({isOpen:U,container:r,ResizeObserver:ve.Z,placement:Ft[x],auto:!0,snap:!0});(0,n.useEffect)(()=>{if(Al(p,ne)){const X=Zr(p,w);xe(X),B(X),te("")}},[p,w,ne]),(0,n.useEffect)(()=>{var X;I&&I(U),U||(X=q.current)==null||X.blur()},[U,I]);const We=(0,n.useMemo)(()=>Array.isArray(w)?Lt(w)?w.some(X=>X.items.length>0):w.length>0:!1,[w]),_t=(X,_e)=>{if(_e.isOpen!==void 0){if(_e.type===fe.ZP.stateChangeTypes.keyDownEscape)return ue(!1),{isOpen:!1};ue(_e.isOpen)}return _e};return n.createElement(Ml,i({},G),n.createElement(fe.ZP,L(i({},Ve),{stateReducer:_t}),({getItemProps:X,getInputProps:_e,getMenuProps:Jt,isOpen:lt,highlightedIndex:Si,selectedItem:ma})=>n.createElement("div",{role:"presentation"},n.createElement("div",i({},Re),n.createElement(Wl,{inputRef:ce,selectedItem:ma,selectedOptionValue:p,placeholder:$,isDisabled:y,options:w,getInputProps:_e,ariaMenuName:f,inputValue:ae,handleInputValueChange:se,isOpen:U&&lt,onInputFocus:()=>{ue(!0)},hasLoader:N,hasError:Boolean(re),id:le})),U&&lt&&O(n.createElement("div",L(i({},Pe),{style:L(i({},Pe.style),{zIndex:s,width:v?"auto":Z?.width})}),n.createElement(Pl,{options:w,selectedItem:ma,selectedOptionValue:p,hasAvailableOptions:We,highlightedIndex:Si,getItemProps:X,isLoading:N,loadingMessage:Q,emptyResultsMessage:P,position:x,downshiftMenuProps:Jt,maxWidth:c,maxHeight:m,minWidth:v}))),Boolean(re)&&!U?n.createElement(Ll,null,re):null)))});Tl.displayName="Typeahead";var u0=null,Fl=({ariaMenuName:e,getInputProps:t,isOpen:a})=>({"aria-activedescendant":t()["aria-activedescendant"],"aria-expanded":a,"aria-label":e||""}),Zl=h.Z.div`
  display: inline-block;
  vertical-align: middle;
`,jl=e=>{var t=e,{ariaMenuName:a,menuPosition:r="left",menuZIndex:l=1100,options:o,trigger:s,triggerCallback:c,isOpen:m,menuMinWidth:v=24,menuMaxWidth:f=48,menuMaxHeight:p,container:b,onOuterClick:w,triggerOffset:$=0,onOpenChange:x,search:y,role:I,menuItemRole:N}=t,Q=E(t,["ariaMenuName","menuPosition","menuZIndex","options","trigger","triggerCallback","isOpen","menuMinWidth","menuMaxWidth","menuMaxHeight","container","onOuterClick","triggerOffset","onOpenChange","search","role","menuItemRole"]);const P=Tt(b),[re,le]=(0,n.useState)(!1),[G,Y]=(0,n.useState)(!1),[q,ce]=(0,n.useState)(""),ae=B=>{const se=B.target.value;ce(se)},te=B=>{switch(B.key){case"ArrowDown":case"ArrowUp":case"ArrowLeft":case"ArrowRight":case"Enter":case" ":case"Tab":case"Escape":Y(!0);break;default:break}},U=m||re,{layerProps:ue,triggerProps:ne,renderLayer:xe}=(0,He.sJ)({isOpen:U,container:b,placement:Ft[r],ResizeObserver:ve.Z,auto:!0,snap:!0,triggerOffset:$});(0,n.useEffect)(()=>{x&&x(U)},[U,x]);const De=(B,se)=>(se.isOpen!==void 0&&le(se.isOpen),se);return o=(0,n.useMemo)(()=>y?y.searchType==="startsWith"?o.filter(B=>Ue(B.title).toLowerCase().startsWith(q.toLowerCase())):o.filter(B=>Ue(B.title).toLowerCase().includes(q.toLowerCase())):o,[o,q,y]),n.createElement(fe.ZP,{stateReducer:De,itemToString:B=>B?B.title:"",onSelect:B=>B&&!B.disabled&&B.onClick&&B.onClick(),onOuterClick:w,environment:P},({getInputProps:B,getItemProps:se,getMenuProps:nt,getToggleButtonProps:Ve,highlightedIndex:Pe,isOpen:Re})=>n.createElement("div",i(i({},Q),c?{role:null,"aria-haspopup":null,"aria-expanded":null,"aria-labelledby":null}:{}),n.createElement("div",i({},ne),c?c(i(i({},Ve({onKeyDown:te})),Fl({ariaMenuName:a,getInputProps:B,isOpen:Re}))):n.createElement(Zl,i({},Ve({onKeyDown:te,tabIndex:0})),s)),Re&&xe(n.createElement("div",L(i({},ue),{style:L(i({},ue.style),{zIndex:l})}),n.createElement(Ye,{position:r,minWidth:v,maxWidth:f,maxHeight:p,downshiftMenuProps:()=>nt({onKeyDown:te}),role:I,search:y&&n.createElement(Hr,{ariaLabel:y.searchPlaceholder,placeholder:y.searchPlaceholder,value:q,onChange:ae,getInputProps:B})},o.map((O,Z)=>n.createElement(Zt,i({key:Z,isHighlighted:Pe===Z,keyboardMove:G&&Pe===Z,isDisabled:O.disabled,isSelected:O.selected,icon:O.icon,hasDivider:O.hasDivider,getItemProps:se,menuItemRole:N,index:Z},se({key:Z,index:Z,item:O,disabled:O.disabled,onMouseMove:()=>{G&&Y(!1)}})),O.title)))))))},Nl=jl,Ul=h.Z.label`
  display: block;
  position: relative;

  .RadioBox:after {
    background-color: transparent;
  }
`,Kl=h.Z.input`
  position: absolute;
  opacity: 0;

  &:not(:disabled) {
    cursor: pointer;

    & ~ .RadioBox {
      border: 2px solid ${d("body")};
    }

    &:checked ~ .RadioBox {
      border: 2px solid ${d("body")};
    }
  }

  &:disabled,
  &:disabled ~ .RadioBox {
    pointer-events: none;
  }

  &:disabled ~ .RadioBox {
    background-color: ${d("disabledBackground")};
  }

  &:checked {
    & ~ .RadioBox:after {
      background-color: ${d("blurple")};
    }

    &:disabled ~ .RadioBox:after {
      background-color: ${d("disabledContent")};
    }
  }

  &:focus-visible ~ .RadioBox {
    ${ke()};
  }
`,Gl=h.Z.span`
  cursor: pointer;
  width: ${u(2.25)};
  height: ${u(2.25)};
  ${ee("full")};
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;

  &:after {
    content: '';
    width: ${u(1)};
    height: ${u(1)};
    ${ee("full")};
    background-color: ${d("white")};
  }
`,Yl=(0,n.forwardRef)((e,t)=>{var a=e,{isDisabled:r,isChecked:l,onFocus:o,onChange:s,onBlur:c}=a,m=E(a,["isDisabled","isChecked","onFocus","onChange","onBlur"]);return n.createElement(Ul,{htmlFor:m.id},n.createElement(Kl,i({type:"radio",disabled:r,checked:l,onFocus:o,onChange:s,onBlur:c,ref:t},m)),n.createElement(Gl,{className:"RadioBox"}))}),Xl=Yl,Oe={medium:{switchHeight:16,switchWidth:32,knobOffset:2},large:{switchHeight:20,switchWidth:36,knobOffset:2}},rt={knob:{active:{enabled:d("white"),disabled:d("disabledContent")},inactive:{enabled:d("white"),disabled:d("disabledContent")}},track:{active:{enabled:d("blurple"),disabled:d("disabledBackground")},inactive:{enabled:d("grey6"),disabled:d("disabledBackground")}}},Jl=e=>Oe[e.switchSize].switchWidth-Oe[e.switchSize].switchHeight,Nr=e=>Oe[e.switchSize].switchHeight-Oe[e.switchSize].knobOffset*2,Ql=h.Z.label`
  display: block;
  position: relative;
`,ql=h.Z.input`
  position: absolute;
  opacity: 0;
  cursor: pointer;

  // to overlap SwitchBox and occupy the same space
  z-index: 1;
  margin: 0;
  width: ${e=>Oe[e.switchSize].switchWidth}px;
  height: ${e=>Oe[e.switchSize].switchHeight}px;

  &:focus-visible ~ .SwitchBox {
    ${pt()};
  }
  &:not(:checked) {
    & + .SwitchBox {
      background-color: ${rt.track.inactive.enabled};
    }
    &:disabled + .SwitchBox {
      background-color: ${rt.track.inactive.disabled};
    }
  }
  &:checked {
    & + .SwitchBox {
      background-color: ${rt.track.active.enabled};
    }
    &:disabled + .SwitchBox {
      background-color: ${rt.track.active.disabled};
    }
    & + .SwitchBox:after {
      transform: translateX(${e=>Jl(e)}px);
    }
  }
  &:disabled {
    pointer-events: none;
  }
`,eo=h.Z.div`
  width: ${e=>Oe[e.switchSize].switchWidth}px;
  height: ${e=>Oe[e.switchSize].switchHeight}px;
  position: relative;
  border-radius: var(--lns-radius-full);
  transition: 0.2s;
  cursor: ${e=>e.isDisabled?"default":"pointer"};
  &:after {
    content: '';
    position: absolute;
    top: ${e=>Oe[e.switchSize].knobOffset}px;
    left: ${e=>Oe[e.switchSize].knobOffset}px;
    width: ${e=>Nr(e)}px;
    height: ${e=>Nr(e)}px;
    border-radius: var(--lns-radius-full);
    transition: 0.15s;
    background-color: ${e=>e.isDisabled?rt.knob.active.disabled:rt.knob.active.enabled};
  }
`,to=e=>{var t=e,{isActive:a,isDisabled:r,onChange:l,size:o="medium",ariaLabelledby:s,ariaLabel:c,ariaDescribedby:m}=t,v=E(t,["isActive","isDisabled","onChange","size","ariaLabelledby","ariaLabel","ariaDescribedby"]);if(s&&c)throw new Error("ariaLabelledby and ariaLabel serve the same purpose and therefore cannot be used at the same time. Choose the one that best suites your needs.");return n.createElement(Ql,{htmlFor:v.id},n.createElement(ql,L(i({},v),{checked:a,disabled:r,onChange:l,type:"checkbox",switchSize:o,"aria-labelledby":s,"aria-label":c,"aria-describedby":m,"aria-checked":a})),n.createElement(eo,{className:"SwitchBox",isDisabled:r,isActive:a,switchSize:o}))},ro=to,Ur={row:{wrapper:{display:"grid",gridTemplateColumns:"auto 1fr",alignItems:"center"},label:{marginLeft:"var(--lns-space-small)"},errorMessage:{marginLeft:"var(--lns-space-small)"}},"row-reverse":{wrapper:{display:"grid",gridTemplateColumns:"1fr auto",alignItems:"center"},label:{}},column:{wrapper:{},label:{marginBottom:"var(--lns-space-xsmall)"}}},ao=h.Z.div`
  ${e=>e.direction&&Ur[e.direction].wrapper};
`,no=h.Z.label`
  display: block;
  ${e=>{var t;return e.direction&&((t=Ur[e.direction])==null?void 0:t.label)}};
  ${e=>e.isLabelClickable&&"cursor: pointer"};
`,lo=h.Z.span`
  color: var(--lns-color-red);
  margin-top: var(--lns-space-xsmall);
  display: block;
  width: 100%;
  grid-column-start: 1;
  grid-column-end: 3;
`,oo=[Xl,T1,ro],io=e=>oo.includes(e),h0=e=>{var t=e,{label:a,children:r,errorMessage:l,labelFor:o,direction:s="column"}=t,c=E(t,["label","children","errorMessage","labelFor","direction"]);const m=React36.Children.toArray(r).some(f=>isValidElement(f)&&typeof f.type!="string"&&io(f.type)),v=a&&React36.createElement(no,{direction:s,htmlFor:o,isLabelClickable:m},a);return React36.createElement(ao,i({direction:s},c),s==="row"&&React36.createElement(React36.Fragment,null,r,v),s==="column"&&React36.createElement(React36.Fragment,null,v,r),s==="row-reverse"&&React36.createElement(React36.Fragment,null,v,r),l&&React36.createElement(lo,null,l))},m0=null;function v0(e,t){React37.useEffect(()=>{const a=r=>{!e.current||e.current.contains(r.target)||t(r)};return document.addEventListener("mousedown",a),document.addEventListener("touchstart",a),()=>{document.removeEventListener("mousedown",a),document.removeEventListener("touchstart",a)}},[e,t])}function g0(e){const[t,a]=useState4(!1),r=useCallback3(o=>{const s=e.current;o.type==="focusin"&&o.target===s&&a(!0)},[e]),l=useCallback3(o=>{const s=e.current;o.type==="focusout"&&o.target===s&&a(!1)},[e]);return useEffect6(()=>(document.addEventListener("focusin",r),document.addEventListener("focusout",l),()=>{document.removeEventListener("focusin",r),document.removeEventListener("focusout",l)}),[r,l]),Boolean(t)}function p0(e){const t=document;useLayoutEffect2(()=>{const a=t?.documentElement,r=t?.body;if(!(t==null||!a||!r))return e&&(r.style.setProperty("padding-top","3.25rem"),r.style.setProperty("transition","padding-top 350ms")),()=>{r.style.removeProperty("padding-top")}},[t,e])}var so=null;function co(){return n.createElement(be.Z,{label:"",testId:"ads-refreshed-icon"})}var uo=e=>n.createElement("svg",i({viewBox:"0 0 24 24",fill:"none"},e),n.createElement("path",{fill:"currentColor",fillRule:"evenodd",clipRule:"evenodd",d:"M7.42 2.293A1 1 0 0 1 8.127 2h7.245a1 1 0 0 1 .708.293l5.127 5.127a1 1 0 0 1 .293.707v7.245a1 1 0 0 1-.293.708l-5.127 5.127a1 1 0 0 1-.707.293H8.128a1 1 0 0 1-.708-.293L2.293 16.08A1 1 0 0 1 2 15.373V8.128a1 1 0 0 1 .293-.708L7.42 2.293ZM8.542 4 4 8.542v6.416L8.542 19.5h6.416l4.542-4.542V8.542L14.958 4H8.542Zm2.208 11.25a1 1 0 0 1 1-1h.009a1 1 0 1 1 0 2h-.009a1 1 0 0 1-1-1Zm2-7a1 1 0 1 0-2 0v3.5a1 1 0 1 0 2 0v-3.5Z"})),Xe={info:{bgColor:"var(--lns-color-blurple)",icon:n.createElement(co,null),color:"var(--lns-color-white)",fontFamily:"inherit"},warning:{bgColor:"var(--lns-color-warning)",icon:n.createElement(uo,null),color:"var(--lns-color-grey8)",fontFamily:"inherit"},error:{bgColor:"var(--lns-color-danger)",icon:n.createElement(Lr,null),color:"var(--lns-color-white)",fontFamily:"inherit"},internal:{icon:n.createElement("span",{role:"img"},"\u{1F514}"),color:"var(--lns-color-tealLight)",bgColor:"var(--lns-color-grey8)",fontFamily:"var(--lns-fontFamily-code)"}},Kr=350,ho=h.Z.aside`
  --paddingXOffset: var(--lns-space-large);
  --alignItems: start;

  display: grid;
  align-items: var(--alignItems);
  justify-content: space-between;
  grid-template-columns: 1fr auto;
  ${e=>`background-color: ${Xe[e.severity].bgColor}`};
  ${e=>`font-family: ${Xe[e.severity].fontFamily}`};

  ${e=>`color: ${Xe[e.severity].color}`};
  position: fixed;
  padding: var(--lns-space-medium) var(--paddingXOffset);
  top: 0;
  left: 0;
  transition:
    ${Kr}ms box-shadow,
    ${Kr}ms transform;
  width: 100%;
  box-sizing: border-box;
  z-index: 1100;
  opacity: ${e=>e.isOpen?"1":"0"};
  transform: ${e=>e.isOpen?"translateY(0px)":"translateY(-100%)"};
  @media (min-width: 872px) {
    --alignItems: center;
  }
`,f0=({children:e,onCloseClick:t,isOpen:a,severity:r="info",id:l})=>{var o,s,c;useEffect7(()=>{if(!a)return;const v=f=>{f.key==="Escape"&&(f.preventDefault(),t&&t())};return window.addEventListener("keydown",v),()=>{window.removeEventListener("keydown",v)}},[a,t]),so(a);const m=r==="internal";return a?React40.createElement(ho,{isOpen:a,severity:r,id:l},React40.createElement(Ge,{alignItems:{default:"start",small:"center"},justifyContent:"space-between",autoFlow:m?"column":void 0,columns:m?void 0:["1fr auto"]},React40.createElement(pe,{paddingY:{default:"xsmall",xsmall:0},paddingLeft:m?void 0:{default:0,medium:u(3.5)},width:"100%"},React40.createElement(Ge,{autoFlow:"column",gap:m?"medium":"small",justifyContent:"center"},(o=Xe[r])!=null&&o.icon?React40.createElement(Ke,{alignment:"topLeft"},React40.createElement(ie,{icon:Xe[r].icon,color:(s=Xe[r].color)!=null?s:"var(--lns-color-white)"})):null," ",e))),t&&React40.createElement($t,{iconColor:(c=Xe[r].color)!=null?c:"var(--lns-color-white)",tabIndex:0,altText:"Close",icon:React40.createElement(Nt,null),onClick:t})):null},b0=null,Gr="web-app",Ut="chrome-extension",mo={short:3e3,long:8e3},vo=(e,t)=>z.F4`
  0% {
    opacity: 0;
    transform: translate(-50%, ${u(t===Ut?-8:8)});
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
`,go=e=>{switch(e){case Gr:return"unset";case Ut:return u(4);default:return"unset"}},po=e=>{switch(e){case Gr:return u(4);case Ut:return"unset";default:return u(4)}},fo=h.Z.div`
  animation: ${e=>vo(e.toastDuration,e.platform)}
    ${e=>e.toastDuration}ms forwards;
  background-color: ${d("backgroundInverse")};
  ${ee("250")};
  top: ${e=>go(e.platform)};
  bottom: ${e=>po(e.platform)};
  ${ct("large")};
  color: ${d("bodyInverse")};
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
`,bo=h.Z.div`
  align-self: center;
`,C0=({children:e,isOpen:t,onCloseClick:a,zIndex:r=1100,duration:l="short",platform:o="web-app"})=>{const s=mo[l];return useEffect8(()=>{const c=setTimeout(()=>{t&&a()},s);return()=>clearTimeout(c)},[t]),React41.createElement(React41.Fragment,null,t&&React41.createElement(fo,{role:"presentation",onClick:c=>c.stopPropagation(),zIndex:r,isOpen:t,toastDuration:s,platform:o},React41.createElement(bo,{"aria-live":"polite"},e),a&&React41.createElement($t,{altText:"Close",icon:React41.createElement(Nt,null),onClick:a,iconColor:"bodyInverse"})))},w0=null,Yr={topLeft:"top-start",topCenter:"top-center",topRight:"top-end",bottomLeft:"bottom-start",bottomCenter:"bottom-center",bottomRight:"bottom-end",leftTop:"left-start",leftCenter:"left-center",leftBottom:"left-end",rightTop:"right-start",rightCenter:"right-center",rightBottom:"right-end"},Co=4,wo=Ze.small.fontSize*Ze.small.lineHeight,Eo=(Co-wo)/2,yo=h.Z.div`
  background-color: ${d("backgroundInverse")};
  color: ${d("bodyInverse")};
  ${ee("150")};
  ${Fe("bold")};
  ${Se("small")};
  ${ct("medium")};
  ${e=>C("max-width",e.maxWidth)};
  z-index: 1100;
  padding: ${u(Eo)} ${u(1.5)};
  z-index: ${e=>e.zIndex};
`,zo=h.Z.div`
  background-color: ${d("grey7")};
  border-radius: 3px;
  color: ${d("grey3")};
  ${Fe("bold")};
  ${Se("small")};
  padding-left: ${u(.5)};
  padding-right: ${u(.5)};
`,xo=({children:e})=>n.createElement(zo,null,e),$o=e=>{var t=e,{children:a,maxWidth:r,onMouseEnter:l,onMouseLeave:o,layerProps:s,zIndex:c}=t,m=E(t,["children","maxWidth","onMouseEnter","onMouseLeave","layerProps","zIndex"]);return n.createElement(yo,i(i({maxWidth:r,onMouseEnter:l,onMouseLeave:o,zIndex:c},s),m),a)},Mo=h.Z.div`
  display: ${e=>e.isInline?"inline-block":"block"};
  ${e=>e.verticalAlign&&`vertical-align: ${e.verticalAlign}`};
  &:focus-visible {
    // Note: 0px solid transparent prevents focus rings from disappearing for -ms-high-contrast.
    // TODO(LNS-183): Provide more robust polyfill/support for :focus for older versions of Safari, which don't support :focus-visible
    outline: 0px solid transparent;
    box-shadow: var(--lns-formFieldBorderShadowFocus);
  }
`;function ko(e){switch(e){case"immediate":return 200;case"long":return 800;default:return 200}}var Lo=e=>{var t=e,{ariaLive:a=!1,children:r,content:l,shortcut:o,placement:s="topCenter",keepOpen:c,triggerOffset:m=4,maxWidth:v=26,isInline:f=!0,isDisabled:p,container:b,tabIndex:w=0,zIndex:$=1100,verticalAlign:x="middle",delay:y="immediate",tooltipId:I}=t,N=E(t,["ariaLive","children","content","shortcut","placement","keepOpen","triggerOffset","maxWidth","isInline","isDisabled","container","tabIndex","zIndex","verticalAlign","delay","tooltipId"]);const[Q,P]=(0,He.XI)({delayEnter:ko(y),delayLeave:200}),[re,le]=(0,n.useState)(!1),[G,Y]=(0,n.useState)(!1),[q,ce]=(0,n.useState)(!1),ae=(0,n.useRef)(),te=!l||p;(0,n.useEffect)(()=>{if(te){Y(!1);return}const B=re&&c;(Q||B)&&Y(!0),!Q&&!B&&!q&&Y(!1)},[l,p,re,te,c,Y,Q,q]);const U=()=>{ce(!1),te||Y(!0)},ue=()=>{Y(!1),ce(!1)};(0,n.useEffect)(()=>{if(!G)return;const B=se=>{se.key==="Escape"&&(se.preventDefault(),ue())};return window.addEventListener("keydown",B),()=>{window.removeEventListener("keydown",B)}},[G,Y]);const{layerProps:ne,triggerProps:xe,renderLayer:De}=(0,He.sJ)({isOpen:G,placement:Yr[s],ResizeObserver:ve.Z,triggerOffset:m,container:b,auto:!0});return n.createElement(n.Fragment,null,n.createElement(Mo,L(i(i({},xe),P),{onClick:B=>{B.detail===0&&ce(!0)},onFocus:U,onBlur:ue,isInline:f,verticalAlign:x,tabIndex:te?-1:w,ref:(0,He.lq)(xe.ref,ae)}),r),a&&n.createElement("span",{className:"srOnly","aria-live":"polite"},G&&l),G&&De(n.createElement("div",L(i({},ne),{style:L(i({},ne.style),{zIndex:$})}),n.createElement($o,i({maxWidth:v,onMouseEnter:()=>le(!0),onMouseLeave:()=>le(!1),role:"tooltip",id:I},N),n.createElement(Ge,{gap:"small"},n.createElement(Ie,{size:"small",fontWeight:"bold"},l),o&&n.createElement(Ge,{gap:"xsmall"},o.map((B,se)=>n.createElement(xo,{key:se},B))))))))},E0=Object.keys(Yr),Ro=Lo,Xr=z.iv`
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
`,_o=h.Z.div`
  ${e=>Se(e.size)};
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
    ${e=>e.animated&&Xr}
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
`,Ho=h.Z.div`
  background-color: var(--lns-color-disabledBackground);
  ${e=>ee(e.radius)};
  height: ${e=>e.height};
  width: ${e=>e.width};
  ${e=>e.animated&&Xr}
`,y0=({size:e="body-md",lines:t=1,animated:a=!1})=>React43.createElement(React43.Fragment,null,[...Array(t)].map((r,l)=>React43.createElement(_o,{key:l,size:e,lines:t,animated:a},"Loading"))),z0=({animated:e=!1,height:t="40px",radius:a="full",width:r="40px"})=>React43.createElement(React43.Fragment,null,React43.createElement(Ho,{animated:e,height:t,radius:a,width:r})),Jr=e=>n.createElement("defs",null,n.createElement("radialGradient",{id:`ai-logo-${e}-gradient-1`,cx:"50%",cy:"50%",r:"100%",fx:"0%",fy:"0%"},n.createElement("stop",{offset:"30%",stopColor:"#97ACFD"}),n.createElement("stop",{offset:"33%",stopColor:"#B3B2F4"}),n.createElement("stop",{offset:"43%",stopColor:"#DEB0E0"}),n.createElement("stop",{offset:"50%",stopColor:"#DFC6E5"}),n.createElement("stop",{offset:"72%",stopColor:"#6663F6"})),n.createElement("radialGradient",{id:`ai-logo-${e}-gradient-2`,r:"100%",fx:"40%",fy:"72%"},n.createElement("stop",{offset:"20%",stopColor:"#615CF500"}),n.createElement("stop",{offset:"32%",stopColor:"#615CF550"}),n.createElement("stop",{offset:"48%",stopColor:"#6663F6"})),n.createElement("radialGradient",{id:`ai-logo-${e}-gradient-3`,r:"100%",fx:"0%",fy:"100%"},n.createElement("stop",{offset:"25%",stopColor:"#6663F6"}),n.createElement("stop",{offset:"38%",stopColor:"#6E68F450"}),n.createElement("stop",{offset:"45%",stopColor:"#6E68F400"}))),Qr="M30 15.4433C30 16.6091 29.0933 16.8581 27.9562 16.9301C22.5158 17.2323 16.7962 22.686 16.4795 28.112C16.422 29.2634 16.173 30.1702 15.0072 30.1702C13.8414 30.1702 13.578 29.2634 13.5205 28.0976C13.2038 22.686 7.48416 17.2323 2.05814 16.9301C0.906735 16.8581 0 16.6091 0 15.4433C0 14.2775 0.906735 14.043 2.05814 13.971C7.48416 13.6687 13.2038 7.65433 13.5205 2.22831C13.578 1.0769 13.827 0.170166 15.0072 0.170166C16.1874 0.170166 16.422 1.0769 16.4795 2.22831C16.7962 7.65433 22.5158 13.6687 27.9419 13.971C29.0933 14.043 30 14.2919 30 15.4433Z",So=e=>{var t=e,{brand:a,symbolColor:r,customId:l}=t,o=E(t,["brand","symbolColor","customId"]);switch(a){case"ai":return n.createElement("svg",i({"aria-label":"Loom AI",viewBox:"0 0 30 31",fill:"none"},o),n.createElement("title",null,"Loom AI"),r?n.createElement("path",{d:Qr,fill:d(r)}):n.createElement(n.Fragment,null,Jr(l),[...Array(3)].map((s,c)=>n.createElement("path",{key:c,d:Qr,fill:`url(#ai-logo-${l}-gradient-${c+1}`}))));case"apptile":return n.createElement("svg",i({"aria-label":"Loom",viewBox:"0 0 40 40",fill:"none"},o),n.createElement("title",null,"Loom"),n.createElement("path",{d:"M0 12C0 5.37258 5.37258 0 12 0H28C34.6274 0 40 5.37258 40 12V28C40 34.6274 34.6274 40 28 40H12C5.37258 40 0 34.6274 0 28V12Z",fill:d(r||"blurple")}),n.createElement("path",{d:"M32.3962 18.6213H25.1467L31.4251 14.9965L30.0463 12.6077L23.768 16.2325L27.392 9.95464L25.0032 8.57506L21.3792 14.8529V7.604H18.6215V14.8536L14.9961 8.57506L12.6081 9.95395L16.2327 16.2318L9.95437 12.6077L8.57552 14.9958L14.8539 18.6206H7.60449V21.3784H14.8532L8.57552 25.0032L9.95437 27.392L16.2321 23.7679L12.6074 30.0457L14.9961 31.4246L18.6208 25.1461V32.3957H21.3785V25.1468L25.0025 31.4246L27.3912 30.0457L23.7665 23.7672L30.0449 27.392L31.4238 25.0032L25.1461 21.3791H32.3947V18.6213H32.3962ZM20.0003 23.7505C17.921 23.7505 16.2355 22.0651 16.2355 19.9856C16.2355 17.9062 17.921 16.2207 20.0003 16.2207C22.0797 16.2207 23.7651 17.9062 23.7651 19.9856C23.7651 22.0651 22.0797 23.7505 20.0003 23.7505Z",fill:"white"}));case"product":return n.createElement("svg",i({"aria-label":"Loom",viewBox:"0 0 40 40",fill:"none"},o),n.createElement("path",{d:"M0 9.25C0 4.14137 4.14137 0 9.25 0H30.75C35.8586 0 40 4.14137 40 9.25V30.75C40 35.8586 35.8586 40 30.75 40H9.25C4.14137 40 0 35.8586 0 30.75V9.25Z",fill:d(r||"primary")}),n.createElement("path",{d:"M32.3962 18.6756H25.1467L31.4251 15.0508L30.0463 12.662L23.768 16.2868L27.392 10.009L25.0032 8.62938L21.3792 14.9072V7.65833H18.6215V14.9079L14.9961 8.62938L12.6081 10.0083L16.2327 16.2861L9.95437 12.662L8.57552 15.0501L14.8539 18.6749H7.60449V21.4327H14.8532L8.57552 25.0575L9.95437 27.4463L16.2321 23.8222L12.6074 30.1L14.9961 31.4789L18.6208 25.2004V32.45H21.3785V25.2011L25.0025 31.4789L27.3912 30.1L23.7665 23.8215L30.0449 27.4463L31.4238 25.0575L25.1461 21.4334H32.3947V18.6756H32.3962ZM20.0003 23.8048C17.921 23.8048 16.2355 22.1194 16.2355 20.0399C16.2355 17.9605 17.921 16.275 20.0003 16.275C22.0797 16.275 23.7651 17.9605 23.7651 20.0399C23.7651 22.1194 22.0797 23.8048 20.0003 23.8048Z",fill:"white"}));default:return n.createElement("svg",i({"aria-label":"Loom",viewBox:"0 0 31 30",fill:"none"},o),n.createElement("title",null,"Loom"),n.createElement("path",{d:"M30.01 13.43h-9.142l7.917-4.57-1.57-2.72-7.918 4.57 4.57-7.915-2.72-1.57-4.571 7.913V0h-3.142v9.139L8.863 1.225l-2.721 1.57 4.57 7.913L2.796 6.14 1.225 8.86l7.917 4.57H0v3.141h9.141l-7.916 4.57 1.57 2.72 7.918-4.57-4.571 7.915 2.72 1.57 4.572-7.914V30h3.142v-9.334l4.655 8.06 2.551-1.472-4.656-8.062 8.087 4.668 1.571-2.72-7.916-4.57h9.141v-3.14h.001zm-15.005 5.84a4.271 4.271 0 11-.001-8.542 4.271 4.271 0 01.001 8.542z",fill:d(r||"primary")}))}},Io=e=>{var t=e,{brand:a,wordmarkColor:r}=t,l=E(t,["brand","wordmarkColor"]);switch(a){case"ai":return n.createElement("svg",i({"aria-label":"Loom AI",viewBox:"0 0 94 23",fill:r},l),n.createElement("title",null,"Loom AI"),n.createElement("path",{d:"M4.12637 22.4624H0V0H4.12637V22.4624Z"}),n.createElement("path",{d:"M13.3999 19.1737C15.4166 19.1737 17.2781 17.7155 17.2781 14.8301C17.2781 11.9448 15.4166 10.4866 13.3999 10.4866C11.3833 10.4866 9.52175 11.9448 9.52175 14.8301C9.52175 17.6845 11.3833 19.1737 13.3999 19.1737ZM13.3999 6.7325C17.9606 6.7325 21.4045 10.1143 21.4045 14.8301C21.4045 19.515 17.9606 22.9277 13.3999 22.9277C8.83919 22.9277 5.39538 19.515 5.39538 14.8301C5.39538 10.1143 8.83919 6.7325 13.3999 6.7325Z"}),n.createElement("path",{d:"M29.7548 19.1737C31.7714 19.1737 33.6329 17.7155 33.6329 14.8301C33.6329 11.9448 31.7714 10.4866 29.7548 10.4866C27.7381 10.4866 25.8766 11.9448 25.8766 14.8301C25.8766 17.6845 27.7381 19.1737 29.7548 19.1737ZM29.7548 6.7325C34.3155 6.7325 37.7593 10.1143 37.7593 14.8301C37.7593 19.515 34.3155 22.9277 29.7548 22.9277C25.194 22.9277 21.7502 19.515 21.7502 14.8301C21.7502 10.1143 25.194 6.7325 29.7548 6.7325Z"}),n.createElement("path",{d:"M43.1622 22.4624H39.0358V7.19788H42.976V9.05941C43.8137 7.57019 45.7683 6.76353 47.4437 6.76353C49.5224 6.76353 51.1978 7.66326 51.9734 9.30761C53.1834 7.44609 54.7967 6.76353 56.8134 6.76353C59.6367 6.76353 62.3359 8.46992 62.3359 12.5653V22.4624H58.3336V13.403C58.3336 11.7586 57.5269 10.5176 55.6344 10.5176C53.8659 10.5176 52.8111 11.8827 52.8111 13.5271V22.4624H48.7157V13.403C48.7157 11.7586 47.878 10.5176 46.0165 10.5176C44.2171 10.5176 43.1622 11.8517 43.1622 13.5271V22.4624Z"}),n.createElement("path",{d:"M84.1324 22.4624L82.3019 17.4363H73.3666L71.5361 22.4624H67.0064L75.4453 0.46538H80.4093L88.7862 22.4624H84.1324ZM77.8342 5.21226L74.7937 13.5271H80.8747L77.8342 5.21226Z"}),n.createElement("path",{d:"M94 22.4624H89.6565V0.46538H94V22.4624Z"}));case"product":return n.createElement("svg",i({"aria-label":"Loom",viewBox:"0 0 104 30",fill:"none"},l),n.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M32.4383 7.29662C34.6059 7.29671 36.4904 7.77257 38.0897 8.72422C39.6888 9.67592 40.9247 11.0053 41.797 12.7102C42.6692 14.402 43.1045 16.3852 43.1045 18.6585C43.1044 20.9186 42.6693 22.9018 41.797 24.6068C40.9247 26.2985 39.6888 27.6207 38.0897 28.5724C36.4904 29.524 34.6059 29.9999 32.4383 30C30.2704 30 28.379 29.5241 26.7664 28.5724C25.1672 27.6208 23.9315 26.2985 23.0591 24.6068C22.1868 22.9018 21.7517 20.9186 21.7516 18.6585C21.7516 16.3851 22.1869 14.402 23.0591 12.7102C23.9315 11.0051 25.1671 9.67594 26.7664 8.72422C28.379 7.77249 30.2704 7.29662 32.4383 7.29662ZM32.4383 11.7584C31.3279 11.7584 30.3954 12.0564 29.642 12.6513C28.902 13.2461 28.3393 14.0587 27.956 15.0895C27.5861 16.1204 27.4009 17.3105 27.4009 18.6585C27.4009 19.9801 27.586 21.163 27.956 22.2071C28.3393 23.238 28.9019 24.0506 29.642 24.6454C30.3954 25.2402 31.3279 25.5382 32.4383 25.5382C33.5351 25.5381 34.4608 25.2401 35.2141 24.6454C35.9673 24.0506 36.53 23.2307 36.9001 22.1867C37.2831 21.1428 37.4733 19.9666 37.4734 18.6585C37.4734 17.324 37.2831 16.1406 36.9001 15.1099C36.5301 14.0661 35.9671 13.246 35.2141 12.6513C34.4608 12.0565 33.5351 11.7585 32.4383 11.7584Z",fill:r}),n.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M56.9839 7.29662C59.1517 7.29662 61.036 7.77249 62.6354 8.72422C64.2348 9.67596 65.4702 11.005 66.3426 12.7102C67.215 14.4021 67.6524 16.385 67.6524 18.6585C67.6523 20.9186 67.215 22.9018 66.3426 24.6068C65.4702 26.2985 64.2346 27.6208 62.6354 28.5724C61.036 29.524 59.1516 30 56.9839 30C54.8166 29.9999 52.9267 29.5238 51.3143 28.5724C49.7151 27.6208 48.4795 26.2984 47.6071 24.6068C46.7347 22.9018 46.2974 20.9186 46.2973 18.6585C46.2973 16.3849 46.7346 14.4021 47.6071 12.7102C48.4795 11.005 49.7149 9.67596 51.3143 8.72422C52.9267 7.77274 54.8165 7.29671 56.9839 7.29662ZM56.9839 11.7584C55.8739 11.7585 54.9432 12.0566 54.1899 12.6513C53.4497 13.2461 52.8873 14.0585 52.504 15.0895C52.1339 16.1205 51.9488 17.3104 51.9488 18.6585C51.9488 19.9801 52.1339 21.163 52.504 22.2071C52.8873 23.2381 53.4497 24.0506 54.1899 24.6454C54.9431 25.2399 55.874 25.5381 56.9839 25.5382C58.081 25.5382 59.0064 25.2402 59.7598 24.6454C60.5133 24.0505 61.0756 23.231 61.4457 22.1867C61.8289 21.1427 62.0212 19.9667 62.0213 18.6585C62.0213 17.3239 61.8288 16.1407 61.4457 15.1099C61.0756 14.0657 60.5132 13.2461 59.7598 12.6513C59.0063 12.0564 58.081 11.7584 56.9839 11.7584Z",fill:r}),n.createElement("path",{d:"M5.69001 24.7655H18.7174V29.5445H0V0H5.69001V24.7655Z",fill:r}),n.createElement("path",{d:"M96.2633 7.2581C97.5984 7.2581 98.7952 7.54891 99.8527 8.13052C100.923 8.71205 101.762 9.56357 102.37 10.6866C102.991 11.8101 103.302 13.1852 103.302 14.8108V29.5445H97.7498V15.7625C97.7497 14.4545 97.3936 13.49 96.6803 12.8688C95.9667 12.2345 95.1007 11.9173 94.0834 11.9171C93.2908 11.9171 92.6027 12.0882 92.0213 12.4315C91.453 12.7751 91.0084 13.2511 90.6911 13.8591C90.3871 14.4671 90.2357 15.176 90.2357 15.9823V29.5445H84.8629V15.5654C84.8629 14.4552 84.5262 13.5682 83.8523 12.9073C83.1781 12.2464 82.3106 11.9171 81.2531 11.9171C80.5396 11.9172 79.8853 12.088 79.2907 12.4315C78.6959 12.7619 78.22 13.2521 77.8631 13.8998C77.5196 14.5343 77.3487 15.3205 77.3487 16.2588V29.5445H71.797V7.61387H77.0111L77.1652 11.7584C77.4644 10.9601 77.8429 10.2729 78.3005 9.69635C78.9746 8.86369 79.7606 8.24832 80.6594 7.8518C81.558 7.45546 82.496 7.25818 83.4738 7.2581C85.0733 7.2581 86.383 7.75323 87.4009 8.74462C88.2044 9.52754 88.8088 10.6088 89.225 11.985C89.5312 11.1783 89.9349 10.4756 90.4351 9.87537C91.1621 9.00295 92.0273 8.34693 93.032 7.91072C94.0364 7.47471 95.1136 7.2581 96.2633 7.2581Z",fill:r}));default:return n.createElement("svg",i({"aria-label":"Loom",viewBox:"0 0 62 23",fill:r},l),n.createElement("title",null,"Loom"),n.createElement("path",{d:"M.109 21.973V.027h4.028v21.946H.109zM38.742 7.059h3.846v1.82c.818-1.456 2.727-2.244 4.362-2.244 2.03 0 3.665.88 4.422 2.485 1.18-1.82 2.756-2.485 4.725-2.485 2.756 0 5.39 1.667 5.39 5.668v9.67h-3.906v-8.851c0-1.607-.788-2.82-2.636-2.82-1.727 0-2.757 1.335-2.757 2.942v8.73h-3.997v-8.852c0-1.607-.817-2.82-2.635-2.82-1.757 0-2.787 1.305-2.787 2.942v8.73h-4.027V7.059zM13.24 22.405c-4.537 0-7.824-3.367-7.824-7.889 0-4.45 3.276-7.896 7.824-7.896 4.57 0 7.824 3.478 7.824 7.896 0 4.49-3.288 7.889-7.824 7.889zm0-12.135a4.25 4.25 0 00-4.244 4.247 4.25 4.25 0 004.244 4.247 4.25 4.25 0 004.243-4.247 4.25 4.25 0 00-4.243-4.247zM29.667 22.405c-4.538 0-7.824-3.367-7.824-7.889 0-4.45 3.276-7.896 7.824-7.896 4.57 0 7.824 3.478 7.824 7.896 0 4.49-3.29 7.889-7.824 7.889zm0-12.186a4.3 4.3 0 00-4.293 4.296 4.3 4.3 0 004.293 4.296 4.3 4.3 0 004.293-4.296 4.3 4.3 0 00-4.293-4.296z"}))}},qr="M100 7.76427C100 8.35691 99.539 8.48348 98.961 8.52007C96.1953 8.67371 93.2877 11.4461 93.1267 14.2045C93.0975 14.7898 92.9709 15.2508 92.3783 15.2508C91.7856 15.2508 91.6517 14.7898 91.6225 14.1972C91.4615 11.4461 88.5539 8.67371 85.7955 8.52007C85.2102 8.48348 84.7492 8.35691 84.7492 7.76427C84.7492 7.17162 85.2102 7.05237 85.7955 7.01578C88.5539 6.86213 91.4615 3.80464 91.6225 1.04628C91.6517 0.460948 91.7783 0 92.3783 0C92.9782 0 93.0975 0.460948 93.1267 1.04628C93.2877 3.80464 96.1953 6.86213 98.9537 7.01578C99.539 7.05237 100 7.17894 100 7.76427Z",Bo=e=>{var t=e,{brand:a,wordmarkColor:r,symbolColor:l,customId:o}=t,s=E(t,["brand","wordmarkColor","symbolColor","customId"]);switch(a){case"ai":return n.createElement("svg",i({"aria-label":"Loom AI",viewBox:"0 0 100 30",fill:"none"},s),n.createElement("title",null,"Loom AI"),l?n.createElement("path",{d:qr,fill:d(l)}):n.createElement(n.Fragment,null,Jr(o),[...Array(3)].map((c,m)=>n.createElement("path",{key:m,d:qr,fill:`url(#ai-logo-${o}-gradient-${m+1}`}))),n.createElement("g",{fill:r},n.createElement("path",{d:"M4.1997 29.5909H0.570312V9.83386H4.1997V29.5909Z"}),n.createElement("path",{d:"M12.3563 26.6983C14.1301 26.6983 15.7674 25.4157 15.7674 22.8778C15.7674 20.34 14.1301 19.0574 12.3563 19.0574C10.5826 19.0574 8.94526 20.34 8.94526 22.8778C8.94526 25.3884 10.5826 26.6983 12.3563 26.6983ZM12.3563 15.7555C16.3678 15.7555 19.3968 18.73 19.3968 22.8778C19.3968 26.9984 16.3678 30.0002 12.3563 30.0002C8.34491 30.0002 5.31587 26.9984 5.31587 22.8778C5.31587 18.73 8.34491 15.7555 12.3563 15.7555Z"}),n.createElement("path",{d:"M26.7414 26.6983C28.5152 26.6983 30.1525 25.4157 30.1525 22.8778C30.1525 20.34 28.5152 19.0574 26.7414 19.0574C24.9676 19.0574 23.3303 20.34 23.3303 22.8778C23.3303 25.3884 24.9676 26.6983 26.7414 26.6983ZM26.7414 15.7555C30.7528 15.7555 33.7819 18.73 33.7819 22.8778C33.7819 26.9984 30.7528 30.0002 26.7414 30.0002C22.73 30.0002 19.7009 26.9984 19.7009 22.8778C19.7009 18.73 22.73 15.7555 26.7414 15.7555Z"}),n.createElement("path",{d:"M38.534 29.5909H34.9047V16.1648H38.3703V17.8022C39.1071 16.4923 40.8263 15.7828 42.2999 15.7828C44.1282 15.7828 45.6018 16.5742 46.284 18.0205C47.3483 16.3831 48.7673 15.7828 50.5411 15.7828C53.0243 15.7828 55.3984 17.2837 55.3984 20.8858V29.5909H51.8782V21.6226C51.8782 20.1763 51.1687 19.0847 49.5041 19.0847C47.9486 19.0847 47.0208 20.2854 47.0208 21.7317V29.5909H43.4187V21.6226C43.4187 20.1763 42.6819 19.0847 41.0446 19.0847C39.4619 19.0847 38.534 20.2581 38.534 21.7317V29.5909Z"}),n.createElement("path",{d:"M74.5698 29.5909L72.9598 25.1701H65.1006L63.4906 29.5909H59.5064L66.929 10.2432H71.2951L78.6631 29.5909H74.5698ZM69.0302 14.4184L66.3559 21.7317H71.7045L69.0302 14.4184Z"}),n.createElement("path",{d:"M83.249 29.5909H79.4285V10.2432H83.249V29.5909Z"})));case"apptile":return n.createElement("svg",i({"aria-label":"Loom",viewBox:"0 0 103 40",fill:"none"},s),n.createElement("title",null,"Loom"),n.createElement("path",{d:"M0 12C0 5.37258 5.37258 0 12 0H28C34.6274 0 40 5.37258 40 12V28C40 34.6274 34.6274 40 28 40H12C5.37258 40 0 34.6274 0 28V12Z",fill:d(l||"blurple")}),n.createElement("path",{d:"M32.3962 18.6213H25.1467L31.4251 14.9965L30.0463 12.6077L23.768 16.2325L27.392 9.95464L25.0032 8.57506L21.3792 14.8529V7.604H18.6215V14.8536L14.9961 8.57506L12.6081 9.95395L16.2327 16.2318L9.95437 12.6077L8.57552 14.9958L14.8539 18.6206H7.60449V21.3784H14.8532L8.57552 25.0032L9.95437 27.392L16.2321 23.7679L12.6074 30.0457L14.9961 31.4246L18.6208 25.1461V32.3957H21.3785V25.1468L25.0025 31.4246L27.3912 30.0457L23.7665 23.7672L30.0449 27.392L31.4238 25.0032L25.1461 21.3791H32.3947V18.6213H32.3962ZM20.0003 23.7505C17.921 23.7505 16.2355 22.0651 16.2355 19.9856C16.2355 17.9062 17.921 16.2207 20.0003 16.2207C22.0797 16.2207 23.7651 17.9062 23.7651 19.9856C23.7651 22.0651 22.0797 23.7505 20.0003 23.7505Z",fill:"white"}),n.createElement("g",{fill:r},n.createElement("path",{d:"M47.6001 29.5076V10H51.1816V29.5076H47.6001Z"}),n.createElement("path",{d:"M81.9516 16.2509H85.3718V17.8682C86.0987 16.575 87.7961 15.8739 89.2499 15.8739C91.0549 15.8739 92.5086 16.6556 93.1818 18.0832C94.2314 16.4659 95.633 15.8739 97.3834 15.8739C99.8338 15.8739 102.177 17.356 102.177 20.9122V29.5076H98.7027V21.6402C98.7027 20.2119 98.0019 19.1345 96.3591 19.1345C94.8238 19.1345 93.9079 20.3202 93.9079 21.7485V29.5084H90.3541V21.6402C90.3541 20.2119 89.6272 19.1345 88.0104 19.1345C86.4483 19.1345 85.5323 20.2933 85.5323 21.7485V29.5084H81.9516V16.2509Z"}),n.createElement("path",{d:"M59.2755 29.8916C55.2407 29.8916 52.3189 26.899 52.3189 22.8795C52.3189 18.9241 55.2312 15.8603 59.2755 15.8603C63.3394 15.8603 66.232 18.9526 66.232 22.8795C66.232 26.8697 63.3086 29.8916 59.2755 29.8916ZM59.2755 19.1051C57.1944 19.1051 55.5018 20.7983 55.5018 22.8803C55.5018 24.9624 57.1944 26.6555 59.2755 26.6555C61.3565 26.6555 63.0484 24.9624 63.0484 22.8803C63.0484 20.7983 61.3565 19.1051 59.2755 19.1051Z"}),n.createElement("path",{d:"M73.8823 29.8916C69.8476 29.8916 66.9258 26.899 66.9258 22.8795C66.9258 18.9241 69.8381 15.8603 73.8823 15.8603C77.9463 15.8603 80.8389 18.9526 80.8389 22.8795C80.8389 26.8697 77.9139 29.8916 73.8823 29.8916ZM73.8823 19.0601C71.7776 19.0601 70.0652 20.7738 70.0652 22.8788C70.0652 24.9837 71.7776 26.6974 73.8823 26.6974C75.9871 26.6974 77.6995 24.9837 77.6995 22.8788C77.6988 20.7738 75.9863 19.0601 73.8823 19.0601Z"})));case"product":return n.createElement("svg",i({viewBox:"0 0 112 40",fill:"none","aria-label":"Loom"},s),n.createElement("path",{d:"M0 9.25C0 4.14137 4.14137 0 9.25 0H30.75C35.8586 0 40 4.14137 40 9.25V30.75C40 35.8586 35.8586 40 30.75 40H9.25C4.14137 40 0 35.8586 0 30.75V9.25Z",fill:d(l||"primary")}),n.createElement("path",{d:"M32.3962 18.6756H25.1467L31.4251 15.0508L30.0463 12.662L23.768 16.2868L27.392 10.009L25.0032 8.62938L21.3792 14.9072V7.65833H18.6215V14.9079L14.9961 8.62938L12.6081 10.0083L16.2327 16.2861L9.95437 12.662L8.57552 15.0501L14.8539 18.6749H7.60449V21.4327H14.8532L8.57552 25.0575L9.95437 27.4463L16.2321 23.8222L12.6074 30.1L14.9961 31.4789L18.6208 25.2004V32.45H21.3785V25.2011L25.0025 31.4789L27.3912 30.1L23.7665 23.8215L30.0449 27.4463L31.4238 25.0575L25.1461 21.4334H32.3947L32.3962 18.6756ZM20.0003 23.8048C17.921 23.8048 16.2355 22.1194 16.2355 20.0399C16.2355 17.9605 17.921 16.275 20.0003 16.275C22.0797 16.275 23.7651 17.9605 23.7651 20.0399C23.7651 22.1194 22.0797 23.8048 20.0003 23.8048Z",fill:"white"}),n.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M70.3743 15.1855C71.6352 15.1855 72.7252 15.459 73.6442 16.0059C74.5709 16.5527 75.2848 17.3237 75.7861 18.3187C76.2874 19.3061 76.5381 20.4568 76.5381 21.7708C76.5381 23.0773 76.2874 24.2242 75.7861 25.2116C75.2848 26.199 74.5709 26.9661 73.6442 27.513C72.7252 28.0599 71.6352 28.3333 70.3743 28.3333C69.1135 28.3333 68.0197 28.0599 67.0931 27.513C66.174 26.9661 65.4639 26.199 64.9626 25.2116C64.4613 24.2242 64.2106 23.0773 64.2106 21.7708C64.2106 20.4568 64.4613 19.3061 64.9626 18.3187C65.4639 17.3237 66.174 16.5527 67.0931 16.0059C68.0197 15.459 69.1135 15.1855 70.3743 15.1855ZM70.3743 17.7376C69.7287 17.7376 69.1895 17.9161 68.7565 18.2731C68.3312 18.6225 68.0084 19.101 67.7881 19.7087C67.5754 20.3087 67.4691 20.9923 67.4691 21.7594C67.4691 22.519 67.5754 23.2026 67.7881 23.8102C68.0084 24.4179 68.3312 24.9002 68.7565 25.2572C69.1895 25.6066 69.7287 25.7812 70.3743 25.7812C71.02 25.7812 71.5592 25.6066 71.9922 25.2572C72.4251 24.9002 72.7479 24.4179 72.9606 23.8102C73.1733 23.2026 73.2796 22.519 73.2796 21.7594C73.2796 20.9999 73.1733 20.3163 72.9606 19.7087C72.7479 19.101 72.4251 18.6225 71.9922 18.2731C71.5592 17.9161 71.02 17.7376 70.3743 17.7376Z",fill:r}),n.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M84.6387 15.1855C85.8995 15.1855 86.9895 15.459 87.9085 16.0059C88.8352 16.5527 89.5491 17.3237 90.0505 18.3187C90.5518 19.3061 90.8024 20.4568 90.8024 21.7708C90.8024 23.0773 90.5518 24.2242 90.0505 25.2116C89.5491 26.199 88.8352 26.9661 87.9085 27.513C86.9895 28.0599 85.8995 28.3333 84.6387 28.3333C83.3778 28.3333 82.2841 28.0599 81.3574 27.513C80.4384 26.9661 79.7282 26.199 79.2269 25.2116C78.7256 24.2242 78.4749 23.0773 78.4749 21.7708C78.4749 20.4568 78.7256 19.3061 79.2269 18.3187C79.7282 17.3237 80.4384 16.5527 81.3574 16.0059C82.2841 15.459 83.3778 15.1855 84.6387 15.1855ZM84.6387 17.7376C83.9931 17.7376 83.4538 17.9161 83.0208 18.2731C82.5955 18.6225 82.2727 19.101 82.0524 19.7087C81.8397 20.3087 81.7334 20.9923 81.7334 21.7594C81.7334 22.519 81.8397 23.2026 82.0524 23.8102C82.2727 24.4179 82.5955 24.9002 83.0208 25.2572C83.4538 25.6066 83.9931 25.7812 84.6387 25.7812C85.2843 25.7812 85.8236 25.6066 86.2565 25.2572C86.6895 24.9002 87.0123 24.4179 87.2249 23.8102C87.4376 23.2026 87.5439 22.519 87.5439 21.7594C87.5439 20.9999 87.4376 20.3163 87.2249 19.7087C87.0123 19.101 86.6895 18.6225 86.2565 18.2731C85.8236 17.9161 85.2843 17.7376 84.6387 17.7376Z",fill:r}),n.createElement("path",{d:"M54.9365 25.3483H62.3421V28.0827H51.6667V11.1068H54.9365V25.3483Z",fill:r}),n.createElement("path",{d:"M107.368 15.1514C108.135 15.1514 108.823 15.3185 109.43 15.6527C110.046 15.9869 110.528 16.4768 110.877 17.1224C111.234 17.768 111.413 18.5579 111.413 19.4922V28.0827H108.211V20.0505C108.211 19.2985 108.006 18.744 107.596 18.387C107.186 18.0301 106.688 17.8516 106.104 17.8516C105.655 17.8516 105.264 17.9503 104.93 18.1478C104.603 18.3377 104.349 18.6073 104.167 18.9567C103.992 19.3061 103.905 19.7125 103.905 20.1758V28.0827H100.794V19.9365C100.794 19.2985 100.601 18.7934 100.213 18.4212C99.8334 18.0414 99.3397 17.8516 98.7321 17.8516C98.3143 17.8516 97.9346 17.9465 97.5928 18.1364C97.251 18.3263 96.9813 18.6073 96.7839 18.9795C96.5864 19.3441 96.4876 19.796 96.4876 20.3353V28.0827H93.2747V15.3451H96.2712L96.3786 17.806C96.5512 17.3255 96.7692 16.9151 97.0345 16.5755C97.4219 16.0894 97.8738 15.7324 98.3903 15.5046C98.9068 15.2691 99.4461 15.1514 100.008 15.1514C100.927 15.1514 101.668 15.44 102.23 16.0173C102.677 16.4764 103.023 17.1235 103.273 17.9574C103.451 17.4646 103.688 17.038 103.984 16.6781C104.417 16.1616 104.922 15.778 105.5 15.5273C106.085 15.2767 106.707 15.1514 107.368 15.1514Z",fill:r}));case"marketing":return n.createElement("svg",i({"aria-label":"Loom",viewBox:"0 0 170 48",fill:"none"},s),n.createElement("path",{d:"M154.37 25.212V38H150.414V24.108C150.414 19.968 148.758 18.128 144.986 18.128C141.306 18.128 138.776 20.566 138.776 25.212V38H134.82V15H138.776V18.772C140.248 16.058 142.962 14.54 146.044 14.54C149.954 14.54 152.622 16.518 153.772 20.152C155.06 16.61 158.142 14.54 161.96 14.54C167.112 14.54 169.964 18.036 169.964 24.522V38H166.008V25.212C166.008 20.474 164.352 18.128 160.58 18.128C156.9 18.128 154.37 20.566 154.37 25.212Z",fill:r}),n.createElement("path",{d:"M119.367 38.46C112.467 38.46 108.419 33.354 108.419 26.454C108.419 19.554 112.467 14.54 119.367 14.54C126.221 14.54 130.223 19.554 130.223 26.454C130.223 33.354 126.221 38.46 119.367 38.46ZM119.367 18.22C114.445 18.22 112.283 22.084 112.283 26.454C112.283 30.824 114.445 34.78 119.367 34.78C124.243 34.78 126.359 30.824 126.359 26.454C126.359 22.084 124.243 18.22 119.367 18.22Z",fill:r}),n.createElement("path",{d:"M94.3452 38.46C87.4452 38.46 83.3972 33.354 83.3972 26.454C83.3972 19.554 87.4452 14.54 94.3452 14.54C101.199 14.54 105.201 19.554 105.201 26.454C105.201 33.354 101.199 38.46 94.3452 38.46ZM94.3452 18.22C89.4232 18.22 87.2612 22.084 87.2612 26.454C87.2612 30.824 89.4232 34.78 94.3452 34.78C99.2212 34.78 101.337 30.824 101.337 26.454C101.337 22.084 99.2212 18.22 94.3452 18.22Z",fill:r}),n.createElement("path",{d:"M64.094 7.77783H68.234V34.0438H81.942V37.9998H64.094V7.77783Z",fill:r}),n.createElement("path",{d:"M0 12C0 5.37258 5.37258 0 12 0H36C42.6274 0 48 5.37258 48 12V36C48 42.6274 42.6274 48 36 48H12C5.37258 48 0 42.6274 0 36V12Z",fill:d(l||"primary")}),n.createElement("g",{clipPath:"url(#clip0_45829_3572)"},n.createElement("path",{d:"M38.0625 22.9644H29.9846L36.9804 18.9253L35.4441 16.2635L28.4482 20.3026L32.4864 13.3073L29.8246 11.77L25.7864 18.7653V10.688H22.7136V18.7661L18.6738 11.77L16.0129 13.3065L20.0518 20.3018L13.0559 16.2635L11.5195 18.9246L18.5154 22.9636H10.4375V26.0366H18.5146L11.5195 30.0757L13.0559 32.7375L20.0511 28.6991L16.0121 35.6945L18.6738 37.2309L22.7128 30.2349V38.313H25.7857V30.2356L29.8239 37.2309L32.4855 35.6945L28.4466 28.6984L35.4425 32.7375L36.979 30.0757L29.9838 26.0373H38.0609V22.9644H38.0625ZM24.25 28.6798C21.933 28.6798 20.0549 26.8018 20.0549 24.4847C20.0549 22.1676 21.933 20.2895 24.25 20.2895C26.567 20.2895 28.445 22.1676 28.445 24.4847C28.445 26.8018 26.567 28.6798 24.25 28.6798Z",fill:"white"})),n.createElement("defs",null,n.createElement("clipPath",{id:"clip0_45829_3572"},n.createElement("rect",{width:"39",height:"39",fill:"white",transform:"translate(4.75 5)"}))));case"attributed":return n.createElement("svg",i({"aria-label":"Loom",viewBox:"0 0 232 75",fill:"none"},s),n.createElement("path",{d:"M181.37 52.212V65H177.414V51.108C177.414 46.968 175.758 45.128 171.986 45.128C168.306 45.128 165.776 47.566 165.776 52.212V65H161.82V42H165.776V45.772C167.248 43.058 169.962 41.54 173.044 41.54C176.954 41.54 179.622 43.518 180.772 47.152C182.06 43.61 185.142 41.54 188.96 41.54C194.112 41.54 196.964 45.036 196.964 51.522V65H193.008V52.212C193.008 47.474 191.352 45.128 187.58 45.128C183.9 45.128 181.37 47.566 181.37 52.212Z",fill:r}),n.createElement("path",{d:"M146.367 65.46C139.467 65.46 135.419 60.354 135.419 53.454C135.419 46.554 139.467 41.54 146.367 41.54C153.221 41.54 157.223 46.554 157.223 53.454C157.223 60.354 153.221 65.46 146.367 65.46ZM146.367 45.22C141.445 45.22 139.283 49.084 139.283 53.454C139.283 57.824 141.445 61.78 146.367 61.78C151.243 61.78 153.359 57.824 153.359 53.454C153.359 49.084 151.243 45.22 146.367 45.22Z",fill:r}),n.createElement("path",{d:"M121.345 65.46C114.445 65.46 110.397 60.354 110.397 53.454C110.397 46.554 114.445 41.54 121.345 41.54C128.199 41.54 132.201 46.554 132.201 53.454C132.201 60.354 128.199 65.46 121.345 65.46ZM121.345 45.22C116.423 45.22 114.261 49.084 114.261 53.454C114.261 57.824 116.423 61.78 121.345 61.78C126.221 61.78 128.337 57.824 128.337 53.454C128.337 49.084 126.221 45.22 121.345 45.22Z",fill:r}),n.createElement("path",{d:"M91.094 34.7778H95.234V61.0438H108.942V64.9998H91.094V34.7778Z",fill:r}),n.createElement("path",{d:"M155.186 11.9857C155.186 14.5147 156.33 16.5017 160.967 17.4049C163.676 18.007 164.278 18.4285 164.278 19.3316C164.278 20.2348 163.676 20.7767 161.749 20.7767C159.521 20.7767 156.872 19.994 155.126 18.9704V23.0648C156.511 23.7271 158.317 24.5099 161.749 24.5099C166.566 24.5099 168.433 22.3423 168.433 19.2112M168.433 19.2714C168.433 16.2608 166.867 14.8759 162.351 13.9125C159.883 13.3706 159.281 12.8287 159.281 12.046C159.281 11.0826 160.184 10.6611 161.81 10.6611C163.797 10.6611 165.723 11.2632 167.59 12.1062V8.19237C166.265 7.53004 164.278 7.04834 161.93 7.04834C157.474 7.04834 155.186 8.97513 155.186 12.1062",fill:r}),n.createElement("path",{d:"M216.844 7.16846V24.329H220.517V11.2629L222.022 14.695L227.2 24.329H231.776V7.16846H228.164V18.2475L226.779 14.9961L222.624 7.16846H216.844Z",fill:r}),n.createElement("path",{d:"M193.602 7.16846H189.628V24.329H193.602V7.16846Z",fill:r}),n.createElement("path",{d:"M185.052 19.2109C185.052 16.2003 183.486 14.8154 178.97 13.852C176.501 13.3101 175.899 12.7682 175.899 11.9854C175.899 11.022 176.802 10.6005 178.428 10.6005C180.415 10.6005 182.342 11.2027 184.209 12.0456V8.13183C182.884 7.46949 180.897 6.98779 178.549 6.98779C174.093 6.98779 171.805 8.91459 171.805 12.0456C171.805 14.5745 172.949 16.5615 177.585 17.4647C180.295 18.0669 180.897 18.4883 180.897 19.3915C180.897 20.2947 180.295 20.8366 178.368 20.8366C176.14 20.8366 173.491 20.0539 171.745 19.0302V23.1247C173.13 23.787 174.936 24.5698 178.368 24.5698C183.125 24.5698 185.052 22.4021 185.052 19.2109Z",fill:r}),n.createElement("path",{d:"M124.237 7.16846V24.329H132.426L133.69 20.5958H128.211V7.16846H124.237Z",fill:r}),n.createElement("path",{d:"M108.04 7.16846V10.8414H112.436V24.329H116.47V10.8414H121.227V7.16846H108.04Z",fill:r}),n.createElement("path",{d:"M102.199 7.16846H96.961L91 24.329H95.5761L96.4191 21.4388C97.4427 21.7398 98.5265 21.9205 99.6104 21.9205C100.694 21.9205 101.778 21.7398 102.802 21.4388L103.645 24.329H108.221C108.16 24.329 102.199 7.16846 102.199 7.16846ZM99.5501 18.3077C98.7674 18.3077 98.0448 18.1873 97.3825 18.0067L99.5501 10.5403L101.718 18.0067C101.055 18.1873 100.333 18.3077 99.5501 18.3077Z",fill:r}),n.createElement("path",{d:"M146.576 7.16846H141.337L135.316 24.329H139.892L140.735 21.4388C141.759 21.7398 142.843 21.9205 143.927 21.9205C145.01 21.9205 146.094 21.7398 147.118 21.4388L147.961 24.329H152.537L146.576 7.16846ZM143.927 18.3077C143.144 18.3077 142.421 18.1873 141.759 18.0067L143.927 10.5403L146.094 18.0067C145.432 18.1873 144.709 18.3077 143.927 18.3077Z",fill:r}),n.createElement("path",{d:"M207.992 7.16846H202.754L196.793 24.329H201.369L202.212 21.4388C203.236 21.7398 204.319 21.9205 205.403 21.9205C206.487 21.9205 207.571 21.7398 208.595 21.4388L209.438 24.329H214.014L207.992 7.16846ZM205.403 18.3077C204.621 18.3077 203.898 18.1873 203.236 18.0067L205.403 10.5403L207.571 18.0067C206.909 18.1873 206.126 18.3077 205.403 18.3077Z",fill:r}),n.createElement("path",{d:"M0 18.75C0 8.39466 8.39466 0 18.75 0H56.25C66.6053 0 75 8.39466 75 18.75V56.25C75 66.6053 66.6053 75 56.25 75H18.75C8.39466 75 0 66.6053 0 56.25V18.75Z",fill:d(l||"primary")}),n.createElement("g",{clipPath:"url(#clip0_45829_3571)"},n.createElement("path",{d:"M59.4729 35.8821H46.8511L57.7822 29.571L55.3817 25.412L44.4506 31.723L50.7602 20.7928L46.6012 18.3909L40.2915 29.3211V16.7002H35.4902V29.3223L29.1781 18.3909L25.0204 20.7916L31.3312 31.7218L20.4001 25.412L17.9995 29.5698L28.9306 35.8809H16.3088V40.6824H28.9294L17.9995 46.9934L20.4001 51.1525L31.33 44.8426L25.0192 55.7728L29.1781 58.1735L35.489 47.2422V59.8643H40.2904V47.2434L46.6 58.1735L50.7589 55.7728L44.4481 44.8415L55.3792 51.1525L57.7799 46.9934L46.85 40.6835H59.4704V35.8821H59.4729ZM37.8909 44.8124C34.2705 44.8124 31.3361 41.878 31.3361 38.2575C31.3361 34.637 34.2705 31.7025 37.8909 31.7025C41.5112 31.7025 44.4456 34.637 44.4456 38.2575C44.4456 41.878 41.5112 44.8124 37.8909 44.8124Z",fill:"white"})),n.createElement("defs",null,n.createElement("clipPath",{id:"clip0_45829_3571"},n.createElement("rect",{width:"60.9375",height:"60.9375",fill:"white",transform:"translate(7.42188 7.8125)"}))));default:return n.createElement("svg",i({"aria-label":"Loom",viewBox:"0 0 100 30",fill:"none"},s),n.createElement("title",null,"Loom"),n.createElement("path",{d:"M30.01 13.43h-9.142l7.917-4.57-1.57-2.72-7.918 4.57 4.57-7.915-2.72-1.57-4.571 7.913V0h-3.142v9.139L8.863 1.225l-2.721 1.57 4.57 7.913L2.796 6.14 1.225 8.86l7.917 4.57H0v3.141h9.141l-7.916 4.57 1.57 2.72 7.918-4.57-4.571 7.915 2.72 1.57 4.572-7.914V30h3.142v-9.334l4.655 8.06 2.551-1.472-4.656-8.062 8.087 4.668 1.571-2.72-7.916-4.57h9.141v-3.14h.001zm-15.005 5.84a4.271 4.271 0 11-.001-8.542 4.271 4.271 0 01.001 8.542z",fill:d(l||"primary")}),n.createElement("path",{d:"M38.109 25.973V4.027h4.028v21.946h-4.028zM76.742 11.059h3.846v1.82c.818-1.455 2.727-2.244 4.362-2.244 2.03 0 3.665.88 4.422 2.485 1.18-1.82 2.756-2.485 4.725-2.485 2.756 0 5.39 1.667 5.39 5.668v9.67h-3.906v-8.851c0-1.607-.788-2.82-2.636-2.82-1.727 0-2.757 1.335-2.757 2.942v8.73h-3.996v-8.852c0-1.607-.818-2.82-2.636-2.82-1.757 0-2.787 1.305-2.787 2.942v8.73h-4.027V11.059zM51.24 26.405c-4.538 0-7.824-3.367-7.824-7.889 0-4.45 3.276-7.896 7.824-7.896 4.57 0 7.824 3.478 7.824 7.896 0 4.49-3.288 7.889-7.824 7.889zm0-12.135a4.25 4.25 0 00-4.244 4.247 4.25 4.25 0 004.244 4.247 4.25 4.25 0 004.243-4.247 4.25 4.25 0 00-4.243-4.247zM67.667 26.405c-4.538 0-7.824-3.367-7.824-7.889 0-4.45 3.276-7.896 7.824-7.896 4.57 0 7.824 3.478 7.824 7.896 0 4.49-3.29 7.889-7.824 7.889zm0-12.186a4.3 4.3 0 00-4.293 4.296 4.3 4.3 0 004.293 4.296 4.3 4.3 0 004.293-4.296 4.3 4.3 0 00-4.293-4.296z",fill:r}))}},Oo=h.Z.span`
  display: block;
  ${e=>e.maxWidth&&C("max-width",e.maxWidth)};

  & > svg.lns-logoSvg {
    display: block;
    width: 100%;
    height: 100%;
    ${e=>e.maxWidth&&C("max-width",e.maxWidth)};
  }
`,Do=e=>{var t=e,{variant:a="combined",maxWidth:r,symbolColor:l,wordmarkColor:o="body",brand:s="loom",customId:c=""}=t,m=E(t,["variant","maxWidth","symbolColor","wordmarkColor","brand","customId"]);return n.createElement(Oo,i({variant:a,maxWidth:r},m),a==="combined"&&n.createElement(Bo,{brand:s,symbolColor:l,wordmarkColor:d(o),customId:c,className:"lns-logoSvg"}),a==="symbol"&&n.createElement(So,{brand:s,symbolColor:l,customId:c,className:"lns-logoSvg"}),a==="wordmark"&&n.createElement(Io,{brand:s,wordmarkColor:d(o),className:"lns-logoSvg"}))},Vo=Do,Wo="https://cdn.loom.com/assets/lens",ea={small:"40px",medium:"80px"},Ao=h.Z.span`
  animation: ${e=>e.animation};
  background-image: url(${Wo}/${e=>e.brand}-loader.svg);
  background-size: cover;
  background-position: left center;
  display: block;
  height: ${e=>ea[e.size]};
  width: ${e=>ea[e.size]};

  @keyframes spin {
    100% {
      background-position: right center;
    }
  }
`,x0=({animation:e="spin 2s infinite steps(49) forwards",brand:t="loom",size:a="medium"})=>React45.createElement(Ao,{animation:e,brand:t,size:a}),$0=null,Kt="/* emotion-disable-server-rendering-unsafe-selector-warning-please-do-not-use-this-the-warning-exists-for-a-reason */",Po={border:z.iv`
    .ListRowWrapper:last-child {
      border-bottom: 1px solid ${d("border")};
    }

    .ListRowWrapper,
    .ListRowWrapper:first-child ${Kt} {
      border-top: 1px solid ${d("border")};
    }
  `,stripe:z.iv`
    .ListRowWrapper {
      &:nth-child(odd) ${Kt} {
        background-color: ${d("backgroundSecondary")};
      }
    }

    .ListRowWrapper {
      ${ee("medium")};
    }
  `,clear:z.iv``},To=h.Z.div`
  .ListRowWrapper {
    grid-template-columns: ${e=>e.columns&&e.columns};
    ${e=>C("gap",e.gap)};
  }

  ${e=>Po[e.variant]};
`,Fo=h.Z.div`
  display: grid;
  align-items: center;
  text-decoration: none;
  color: inherit;

  ${e=>C("height",e.height)};
  ${e=>C("min-height",e.minHeight)};
  ${e=>C("max-height",e.maxHeight)};
  ${e=>C("padding",e.padding)};
  ${e=>C("padding-top",e.paddingTop)};
  ${e=>C("padding-bottom",e.paddingBottom)};
  ${e=>C("padding-left",e.paddingLeft)};
  ${e=>C("padding-right",e.paddingRight)};

  ${e=>e.paddingY&&`
    ${C("padding-top",e.paddingY)}
    ${C("padding-bottom",e.paddingY)}
    `};

  ${e=>e.paddingX&&`
    ${C("padding-left",e.paddingX)}
    ${C("padding-right",e.paddingX)}
    `};

  ${e=>(e.onClick||e.href)&&"cursor: pointer;"};

  &.ListRowWrapper:nth-child(even),
  &.ListRowWrapper:nth-child(odd) ${Kt} {
    ${e=>e.backgroundColor&&`background-color: ${d(e.backgroundColor)}`};

    &:hover {
      ${e=>(e.onClick||e.href)&&`
      background-color: ${d("backgroundHover")};
      border-color: transparent;
      ${ee("medium")};
    `};
    }
  }
`,Zo=e=>{var t=e,{children:a,htmlTag:r="li",className:l,backgroundColor:o,onClick:s,href:c,role:m}=t,v=E(t,["children","htmlTag","className","backgroundColor","onClick","href","role"]);const f=l?` ${l}`:"",p=["div","span","p","h1","h2","h3","h4","h5","h6","section","article","header","footer","main","aside","nav"],b=!r&&s;let w=!1;const $=r||"div";b||(w=p.includes($));const x=!w||b?{onClick:s,onKeyDown:y=>{y.key==="Enter"&&(y.preventDefault(),s?.(y))}}:{};return React46.createElement(Fo,i(i({role:m||(r==="li"?"listitem":void 0),className:`ListRowWrapper${f}`,as:r,backgroundColor:o,href:c},x),v),a)},jo=e=>e.map(t=>Me(t)).join(" "),M0=e=>{var t=e,{children:a,columns:r,gap:l,variant:o="stripe",htmlTag:s="ul"}=t,c=E(t,["children","columns","gap","variant","htmlTag"]);let m=a;return s==="ul"&&(m=React46.Children.map(a,v=>React46.isValidElement(v)&&v.type===Zo?React46.cloneElement(v,{htmlTag:"li"}):v)),React46.createElement(To,i({as:s,columns:r&&jo(r),gap:l,variant:o,role:s==="ul"?"list":void 0},c),m)},k0=null,Rt=n.createContext({}),No=e=>`calc(-1 * ${Me(e)})`,ta=h.Z.div`
  ${e=>e.scrollOffset&&`margin: 0 ${No(e.scrollOffset)};
  `};
`,ra=h.Z.div`
  --activeIndicatorHeight: 3px;

  display: flex;
  overflow: auto;
  -ms-overflow-style: none;
  scrollbar-width: none;

  ${e=>e.hasBottomBorder&&"border-bottom: 1px solid var(--lns-color-border)"}

  ${e=>e.scrollOffset&&C("padding-left",e.scrollOffset)};

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
    ${e=>e.scrollOffset&&C("width",e.scrollOffset)};
  }
`,aa=h.Z.div`
  ${ee("200")};
  background-color: var(--lns-color-backgroundSecondary);

  padding: var(--lns-space-xsmall);

  display: flex;
  overflow: auto;
  -ms-overflow-style: none;
  scrollbar-width: none;
  ${e=>e.scrollOffset&&C("padding-left",e.scrollOffset)};

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
    ${e=>e.scrollOffset&&C("width",e.scrollOffset)};
  }
`,na=h.Z.button`
  appearance: none;
  font: inherit;
  background: transparent;
  border: 0;
  ${ee("medium")};
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
  ${Fe("bold")};
  transition: 0.6s color;
  white-space: nowrap;
  color: ${e=>d(e.isActive?"body":e.disabled?"disabledContent":"bodyDimmed")};
  ${e=>e.isActive&&`border-color: ${d("primary")};
  `};

  &:focus,
  &:focus-visible {
    outline: 1px solid transparent;
  }

  &:focus-visible {
    ${ke(void 0,"inset")};
  }

  &:hover:not(:disabled) {
    color: ${d("body")};
    transition: 0.3s color;
  }

  &::after {
    bottom: 0;
    ${ee("medium")};
    content: '';
    height: var(--activeIndicatorHeight);
    position: absolute;
    width: 100%;
    ${e=>e.isActive&&`background-color: ${d("primary")}`};
  }
`,la=h.Z.button`
  padding: ${u(1)} 0;

  appearance: none;
  font: inherit;
  background: transparent;
  border: none;
  ${ee("175")};
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  position: relative;
  color: inherit;
  text-decoration: none;
  flex-shrink: 0;
  ${Fe("bold")};

  transition: 0.6s color;
  white-space: nowrap;
  color: ${e=>d(e.isActive?"body":e.disabled?"disabledContent":"bodyDimmed")};
  ${e=>e.isActive&&`background-color: ${d("background")};
     color: ${d("primary")};
  `};

  &:focus,
  &:focus-visible {
    outline: 1px solid transparent;
  }

  &:focus-visible {
    ${ke(void 0,"inset")};
  }

  &:hover:not(:disabled) {
    color: ${d("primary")};
    transition: 0.3s color;
  }
`,L0=e=>{var t=e,{children:a,isActive:r,htmlTag:l="button",icon:o,isDisabled:s=!1}=t,c=E(t,["children","isActive","htmlTag","icon","isDisabled"]);const{isPilledDesign:m}=React47.useContext(Rt);return m?React47.createElement(la,i({as:l,isActive:r,icon:o,role:"tab","aria-selected":r,disabled:s},c),o&&React47.createElement(pe,{htmlTag:"span",paddingRight:a&&"small"},React47.createElement(ie,{icon:o,color:"currentColor"})),a):React47.createElement(na,i({as:l,isActive:r,icon:o,role:"tab","aria-selected":r,disabled:s},c),o&&React47.createElement(pe,{htmlTag:"span",paddingRight:a&&"small"},React47.createElement(ie,{icon:o,color:"currentColor"})),a)},Uo=e=>{var t=e,{children:a,scrollOffset:r,hasFullTabs:l,isPilledDesign:o,hasBottomBorder:s=!1}=t,c=E(t,["children","scrollOffset","hasFullTabs","isPilledDesign","hasBottomBorder"]);const m=o?React47.createElement(aa,i({hasFullTabs:l,scrollOffset:r,role:"tablist"},c),a):React47.createElement(ra,i({hasFullTabs:l,scrollOffset:r,hasBottomBorder:s,role:"tablist"},c),a);return r?React47.createElement(ta,{scrollOffset:r},m):React47.createElement(Rt.Provider,{value:{isPilledDesign:o}},m)},Ko=({tooltipProps:e,children:t,tooltipId:a})=>e?n.createElement(Ro,L(i({},e),{tooltipId:a,tabIndex:-1}),t):t,oa=n.forwardRef((e,t)=>{var a=e,{tabContent:r,tooltipProps:l,isActive:o,htmlTag:s="button",icon:c,isDisabled:m=!1,onKeyDown:v,onClick:f}=a,p=E(a,["tabContent","tooltipProps","isActive","htmlTag","icon","isDisabled","onKeyDown","onClick"]);const{isPilledDesign:b}=n.useContext(Rt),w=(0,n.useId)(),$=i({as:s,isActive:o,icon:c,role:"tab","aria-selected":o,disabled:m,tabIndex:o?0:-1,"aria-describedby":l?w:void 0,onKeyDown:v,onClick:f,ref:t},p);return n.createElement(Ko,{tooltipProps:l,tooltipId:w},b?n.createElement(la,i({},$),c?n.createElement(pe,{htmlTag:"span",paddingRight:r&&"small"},n.createElement(ie,{icon:c,color:"currentColor"})):null,r):n.createElement(na,i({},$),c?n.createElement(pe,{htmlTag:"span",paddingRight:r&&"small"},n.createElement(ie,{icon:c,color:"currentColor"})):null,r))});oa.displayName="TabNew";var Go=e=>{var t=e,{tabs:a,scrollOffset:r,hasFullTabs:l,isPilledDesign:o,hasBottomBorder:s=!1}=t,c=E(t,["tabs","scrollOffset","hasFullTabs","isPilledDesign","hasBottomBorder"]);const m=useRef5({}),v=useCallback4(($,x)=>{var y;let I=x;switch($.key){case"ArrowLeft":$.preventDefault(),I=x>0?x-1:a.length-1;break;case"ArrowRight":$.preventDefault(),I=x<a.length-1?x+1:0;break;case"Home":$.preventDefault(),I=0;break;case"End":$.preventDefault(),I=a.length-1;break;default:return}(y=m.current[I])==null||y.focus()},[a.length]),f=useCallback4($=>x=>{m.current[$]=x},[]),p=useMemo4(()=>a.map(($,x)=>React47.createElement(oa,i({key:x,ref:f(x),onKeyDown:y=>v(y,x)},$))),[a,v,f]),b=useMemo4(()=>o?React47.createElement(aa,i({hasFullTabs:l,scrollOffset:r,role:"tablist"},c),p):React47.createElement(ra,i({hasFullTabs:l,scrollOffset:r,hasBottomBorder:s,role:"tablist"},c),p),[p,l,r,s,o,c]),w=React47.createElement(Rt.Provider,{value:{isPilledDesign:o}},b);return r?React47.createElement(ta,{scrollOffset:r},w):w},R0=e=>{var t=e,{children:a,tabs:r}=t,l=E(t,["children","tabs"]);return a&&r&&console.warn("Both children and tabs props are provided. Please use only one of them."),!a&&!r?(console.error("Either children or tabs must be provided."),null):a?React47.createElement(Uo,i({},l),a):React47.createElement(Go,i({tabs:r},l))},_0=null,Yo=h.Z.div`
  display: inline-grid;
  grid-auto-flow: column;
  align-items: center;
  vertical-align: middle;
  padding: 0 ${u(1.5)};
  min-height: ${u(3.25)};
  color: ${e=>d(e.color)};
  background-color: ${e=>d(e.backgroundColor)};
  ${ee("100")};
  ${Se("small")};
  ${Fe("bold")};
  ${C("gap","xsmall")};
`,H0=e=>{var t=e,{color:a,backgroundColor:r,children:l,icon:o,iconPosition:s="left"}=t,c=E(t,["color","backgroundColor","children","icon","iconPosition"]);const m=React48.createElement(pe,{htmlTag:"span",paddingLeft:s==="right"&&"xsmall",paddingRight:s==="left"&&"xsmall"},React48.createElement(ie,{icon:o,color:"currentColor",size:2}));return React48.createElement(Yo,i({color:a,backgroundColor:r},c),o&&s==="left"&&m,l,o&&s==="right"&&m)},S0=null,Xo={topLeft:"top-start",topCenter:"top",topRight:"top-end",bottomLeft:"bottom-start",bottomCenter:"bottom",bottomRight:"bottom-end",leftTop:"left-start",leftCenter:"left",leftBottom:"left-end",rightTop:"right-start",rightCenter:"right",rightBottom:"right-end"},Jo=h.Z.div`
  position: relative;
  width: fit-content;
  // transform forces the popover to calculate the position from the trigger instead of the viewport
  transform: translate(0);
  z-index: ${e=>e.childrenZIndex};
`,ia=h.Z.div`
  ${e=>e.zIndex&&`z-index: ${e.zIndex}`};
`,I0=e=>{var t=e,{children:a,content:r,offset:l=.5,boundaryOffset:o=.5,isOpen:s,zIndex:c=500,childrenZIndex:m=1,placement:v="topCenter",rootId:f,boundaryElement:p="body",transitionDuration:b=0,transitionDelay:w=0}=t,$=E(t,["children","content","offset","boundaryOffset","isOpen","zIndex","childrenZIndex","placement","rootId","boundaryElement","transitionDuration","transitionDelay"]);const x=l*et,y=o*et,I=typeof window<"u",N=f&&I?document.getElementById(f):void 0,{stage:Q,shouldMount:P}=useTransition2(s,b+w),re=()=>p==="body"&&I?document.body:p,{x:le,y:G,reference:Y,floating:q,strategy:ce,update:ae,refs:te}=useFloating({placement:Xo[v],middleware:[shift({padding:y,boundary:p?re():void 0,limiter:limitShift()}),flip({fallbackPlacements:["top","bottom"],fallbackStrategy:"initialPlacement"}),floatingUiOffset(x)],strategy:"fixed"});useEffect10(()=>{if(!(!te.reference.current||!te.floating.current))return autoUpdate(te.reference.current,te.floating.current,ae)},[te.reference,te.floating,ae,P]);const U={zIndex:c,ref:q,style:{position:ce,top:G??"",left:le??"",transition:`opacity ${b}ms ${w}ms`,opacity:Q==="enter"?1:0}};return React49.createElement(Jo,L(i({ref:Y},$),{childrenZIndex:m}),a,P&&React49.createElement(React49.Fragment,null,!N&&React49.createElement(ia,i({},U),r),N&&ReactDOM.createPortal(React49.createElement(ia,i({},U),r),N)))},B0=null,Qo=h.Z.span`
  display: block;
  color: ${e=>e.color?d(e.color):d("grey8")};
  ${e=>e.size&&C("width",e.size)};
  ${e=>e.size&&C("height",e.size)};

  svg {
    display: block;
    width: 100%;
    height: 100%;
  }
`,O0=e=>{var t=e,{altText:a,illustration:r,color:l="orange",size:o=12}=t,s=E(t,["altText","illustration","color","size"]);return React50.createElement(Qo,i({"aria-hidden":"true","aria-label":a,color:l,size:o},s),r)},D0=null,sa=e=>z.iv`
  ${C("width",e.width)};
  ${C("height",e.height)};
  ${C("min-width",e.minWidth)};
  ${C("min-height",e.minHeight)};
  ${C("max-width",e.maxWidth)};
  ${C("max-height",e.maxHeight)};
`,qo=h.Z.div`
  display: flex;
  ${e=>we("align-items",e.alignItems)};
  ${e=>e.justifyContent&&we("justify-content",e.justifyContent)};
  ${e=>e.alignContent&&we("align-content",e.alignContent)};
  ${e=>we("flex-wrap",e.wrap)};
  ${e=>e.direction&&we("flex-direction",e.direction)};
  ${e=>e.gap&&C("gap",e.gap)};
  ${e=>e.rowGap&&C("row-gap",e.rowGap)};
  ${e=>e.columnGap&&C("column-gap",e.columnGap)};
  ${e=>sa(e)};
  ${e=>or(e.as)};
`,ei=h.Z.div`
  ${e=>nr("flex-grow",e.grow)};
  ${e=>nr("flex-shrink",e.shrink)};
  ${e=>e.basis&&C("flex-basis",e.basis)};
  ${e=>sa(e)};
`,ti=e=>{var t=e,{children:a,grow:r,shrink:l,basis:o,width:s,height:c,minWidth:m,minHeight:v,maxWidth:f,maxHeight:p,htmlTag:b="div",className:w,style:$}=t,x=E(t,["children","grow","shrink","basis","width","height","minWidth","minHeight","maxWidth","maxHeight","htmlTag","className","style"]);return(w||$)&&console.warn(It),React51.createElement(ei,i({as:b,grow:r,shrink:l,basis:o,width:s,height:c,minWidth:m,minHeight:v,maxWidth:f,maxHeight:p},x),a)},ri=e=>{var t=e,{children:a,gap:r="initial",rowGap:l,columnGap:o,alignItems:s="center",justifyContent:c,alignContent:m,wrap:v="wrap",width:f,height:p,minWidth:b,minHeight:w,maxWidth:$,maxHeight:x,htmlTag:y="div",className:I,style:N}=t,Q=E(t,["children","gap","rowGap","columnGap","alignItems","justifyContent","alignContent","wrap","width","height","minWidth","minHeight","maxWidth","maxHeight","htmlTag","className","style"]);return(I||N)&&console.warn(It),React51.createElement(qo,i({as:y,gap:r,rowGap:l,columnGap:o,alignItems:s,justifyContent:c,alignContent:m,wrap:v,width:f,height:p,minWidth:b,minHeight:w,maxWidth:$,maxHeight:x},Q),y==="ul"||y==="ol"?Children.map(a,P=>P.type===ti||P.type===ri?cloneElement(P,{htmlTag:"li"}):P):a)},V0=null,ai=h.Z.div`
  padding: var(--lns-space-medium);
  & .react-colorful {
    width: auto;
    height: auto;
  }
  & .react-colorful__saturation {
    height: ${u(14)};
    border-bottom: none;
    box-shadow: inset 0 0 0 1px var(--lns-color-border);
    ${ee(100)};
    margin-bottom: var(--lns-space-small);
  }

  & .react-colorful__hue {
    height: ${u(2)};
    width: 100%;
    box-shadow: inset 0 0 0 1px var(--lns-color-border);
    ${ee("50")};
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
`,ni=h.Z.div`
  position: relative;
  width: ${u(31)};
  background-color: var(--lns-color-overlay);
  ${ee("250")};
  box-shadow:
    0 0 0 1px var(--lns-color-border),
    var(--lns-shadow-medium);
`,li=h.Z.div`
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
    ${ee("150")};
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
`,oi=h.Z.div`
  position: absolute;
  width: ${u(3)};
  height: ${u(3)};
  left: var(--lns-space-xsmall);
  top: var(--lns-space-xsmall);
  border: 1px solid rgba(0, 0, 0, 0.1);
  ${ee("100")};
  background-color: ${e=>e.color};
`,ii=h.Z.div`
  position: relative;
  border-radius: var(--lns-radius-medium);
  padding: 0 var(--lns-space-medium) var(--lns-space-medium)
    var(--lns-space-medium);
`,si=h.Z.div`
  display: grid;
  grid-template-columns: repeat(7, ${u(3)});
  gap: ${u(1)} ${u(1)};
  border-bottom: 1px solid var(--lns-color-border);
  padding: var(--lns-space-medium);
`,di=h.Z.div`
  cursor: pointer;
  width: ${u(3)};
  height: ${u(3)};
  ${ee("100")};
  background-color: ${e=>e.color};
  border: ${e=>e.selected===e.color?"1px solid white":"1px solid var(--lns-color-border)"};
  box-shadow: ${e=>e.selected===e.color&&"0 0 0 2px var(--lns-color-focusRing)"};
`,ci=({swatches:e,currentColor:t,onSwatchClick:a})=>{const r=e.includes(t)&&t;return React52.createElement(si,null,e.map(l=>React52.createElement(di,{key:l,color:l,selected:r,onClick:()=>a(l),role:"button",tabIndex:0,onKeyDown:o=>{o.key==="Enter"&&(o.preventDefault(),a(l))}})))},ui=({color:e,setColor:t})=>React52.createElement(ai,null,React52.createElement(HexColorPicker,{color:e,onChange:t}),React52.createElement(li,null,React52.createElement(HexColorInput,{prefixed:!0,color:e,onChange:t}),React52.createElement(oi,{color:e}))),W0=e=>{var t=e,{defaultColor:a="#ffffff",confirmButton:r,swatches:l,onChange:o}=t,s=E(t,["defaultColor","confirmButton","swatches","onChange"]);const[c,m]=useState6(a||"#FFFFFF"),v=p=>{m(p),o(p)},f=p=>{v(p)};return React52.createElement(ni,i({},s),l&&React52.createElement(ci,{swatches:l,currentColor:c,onSwatchClick:f}),React52.createElement(ui,{color:c,setColor:v}),r&&React52.createElement(ii,null,r))},A0=null,hi=2,at={small:{totalSize:u(2.25),height:u(.5625),dotSize:u(.375),gap:u(.25)},medium:{totalSize:u(3),height:u(.75),dotSize:u(.5),gap:u(.375)},large:{totalSize:u(6),height:u(1.5),dotSize:u(1),gap:u(.75)}},mi=e=>at[e.size].totalSize,vi=e=>at[e.size].height,da=e=>at[e.size].dotSize,gi=e=>at[e.size].gap,pi=e=>at[e.size].dotSize,fi=e=>z.F4`
  0%, 40%, 100% {
    transform: translateY(50%);
  }
  20% {
    transform: translateY(calc(50% - ${e}));
  }
`,bi=h.Z.span`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: ${e=>vi(e)};
  width: ${e=>mi(e)};
  gap: ${e=>gi(e)};
`,Gt=h.Z.span`
  width: ${e=>da(e)};
  height: ${e=>da(e)};
  border-radius: 50%;
  background-color: ${e=>d(e.color)};
  transform: translateY(50%);
  animation: ${e=>fi(pi(e))} ${hi}s
    ease-in-out infinite;
  animation-fill-mode: both;
  animation-delay: ${e=>e.delay}s;
`,P0=e=>{var t=e,{color:a="body",size:r="medium"}=t,l=E(t,["color","size"]);return React53.createElement(bi,i({size:r},l),React53.createElement(Gt,{color:a,size:r,delay:0}),React53.createElement(Gt,{color:a,size:r,delay:.2}),React53.createElement(Gt,{color:a,size:r,delay:.4}))},T0=Object.keys(at),F0=null,Yt={medium:{totalSize:u(3),barHeight:u(2.25)}},ca={fast:1.2,slow:1.7},Ci="linear-gradient(270deg, #565ADD 10.58%, #DC43BE 41.83%, #565ADD 69.23%, #565ADD 96.63%)",wi=2,Xt=5,Ei=u(.25),yi=e=>Yt[e.size||"medium"].barHeight,mt=e=>Yt[e.size||"medium"].totalSize,ua=e=>ca[e.speed||"fast"],zi=z.F4`
  0%, 100% {
    transform: scaleY(0.3);
  }
  50% {
    transform: scaleY(1);
  }
`,xi=z.F4`
  0% {
    background-position: 0% center;
  }
  100% {
    background-position: 100% center;
  }
`,$i=z.F4`
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
`,Mi=h.Z.span`
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
  height: ${e=>mt(e)};
  width: ${e=>mt(e)};
  position: relative;
`,ki=h.Z.span`
  width: ${Ei};
  height: ${e=>yi(e)};
  background: ${e=>e.color==="ai-primary"?Ci:d(e.color)};
  background-size: ${e=>mt(e)}
    ${e=>mt(e)};
  background-position: ${e=>{const a=(e.index+1)/(Xt+1)-.5;return`calc(${mt(e)} * ${a}) center`}};
  opacity: 0; /* Ensure it starts invisible */
  transform: scaleY(0.3);
  transform-origin: center;
  animation:
    ${$i} 50ms ease-out forwards,
    ${zi} ${e=>ua(e)}s ease-in-out infinite,
    ${xi} ${wi}s linear infinite;

  animation-delay: ${e=>-1+e.index*(ua(e)/Xt)}s;
  position: relative;
`,Z0=e=>{var t=e,{size:a="medium",speed:r="fast",color:l="body"}=t,o=E(t,["size","speed","color"]);const s=Array.from({length:Xt},(c,m)=>React54.createElement(ki,{key:m,index:m,size:a,speed:r,color:l}));return React54.createElement(Mi,i({size:a,color:l},o),s)},j0=Object.keys(Yt),N0=Object.keys(ca),U0=null,Li=z.F4`
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
`,Ae={dot:{size:"8px",borderWidth:"1px",borderColor:d("background")},positioning:{top:"-2px",right:"-2px"},animation:{duration:"2s",timing:"ease-out",iteration:"infinite"}},ha={blue:d("blue"),orange:d("orange")},Ri=h.Z.span`
  position: relative;
  display: inline-block;
`,_i=h.Z.span`
  position: absolute;
  height: ${Ae.dot.size};
  width: ${Ae.dot.size};
  top: ${Ae.positioning.top};
  right: ${Ae.positioning.right};
`,Hi=h.Z.span`
  position: absolute;
  height: 100%;
  width: 100%;
  border-radius: var(--lns-radius-full);
  background-color: ${e=>ha[e.color||"blue"]};
  border: ${Ae.dot.borderWidth} solid
    ${Ae.dot.borderColor};

  &::after {
    content: '';
    position: absolute;
    height: 100%;
    width: 100%;
    border-radius: var(--lns-radius-full);
    background-color: ${e=>ha[e.color||"blue"]};
    opacity: 0;
    animation: ${e=>e.withPulse?Li:"none"}
      ${Ae.animation.duration} ${Ae.animation.timing}
      ${Ae.animation.iteration};
    display: ${e=>e.withPulse?"block":"none"};
  }
`,K0=e=>{var t=e,{withPulse:a=!0,color:r="blue",children:l}=t,o=E(t,["withPulse","color","children"]);const s=React55.createElement(Hi,{withPulse:a,color:r});return React55.createElement(Ri,i({},o),l,React55.createElement(_i,null,s))},G0=null;function Y0(e){return React56.createElement("svg",i({viewBox:"0 0 102 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React56.createElement("path",{d:"M96.072 5.826H5.928v90.145h90.144V5.826z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React56.createElement("path",{d:"M69.38 59.21c14.74 0 26.691-11.95 26.691-26.692S84.121 5.826 69.38 5.826c-14.741 0-26.692 11.95-26.692 26.692S54.638 59.21 69.38 59.21zM1 95.973h100M1 77.28h100M1 59.213h100M5.928 1v58.213M24.605 1v58.213M42.674 1v58.213",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}))}var X0=null;function J0(e){return React57.createElement("svg",i({viewBox:"0 0 100 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React57.createElement("path",{d:"M50.028 25.007A24.999 24.999 0 0034.586 1.905a25.022 25.022 0 00-27.26 5.42 25.002 25.002 0 0017.688 42.687V25.007h25.014z",fill:"currentColor"}),React57.createElement("path",{d:"M74.986 50.012a25.02 25.02 0 0023.11-15.436 24.993 24.993 0 00-5.422-27.25 25.017 25.017 0 00-42.702 17.681h25.014v25.005z",fill:"currentColor"}),React57.createElement("path",{d:"M49.972 74.99a25 25 0 0015.442 23.102 25.025 25.025 0 0027.26-5.42 25.002 25.002 0 00-17.688-42.687V74.99H49.972z",fill:"currentColor"}),React57.createElement("path",{d:"M25.014 100.003a25.003 25.003 0 0023.103-15.44 25.017 25.017 0 00-5.42-27.259A25.005 25.005 0 00.006 74.991h25.007v25.012z",fill:"currentColor"}))}var Q0=null;function q0(e){return React58.createElement("svg",i({viewBox:"0 0 100 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React58.createElement("path",{d:"M0 .002v100h100v-100H0zm90 90H10v-80h80v80z",fill:"currentColor"}),React58.createElement("path",{d:"M87 13.002H53.68c8.41 1.53 15 8.2 16.46 16.63H87v-16.63zM46.32 13.002H13v16.63h16.86c1.45-8.43 8.05-15.1 16.46-16.63zM13 32.632v15.87h18.19c3.12-7.32 10.35-12.47 18.81-12.47 8.46 0 15.69 5.15 18.81 12.47H87v-15.87H13zM13 67.372h20.4c3.71-5.15 9.76-8.52 16.59-8.52 6.84 0 12.88 3.36 16.59 8.52H87v-15.87H13v15.87zM13 87.002h23.47c3.61-3.18 8.34-5.12 13.53-5.12 5.19 0 9.92 1.93 13.53 5.12H87v-16.63H13v16.63z",fill:"currentColor"}))}var e2=null;function t2(e){return React59.createElement("svg",i({viewBox:"0 0 110 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React59.createElement("path",{d:"M55 100.888a54.867 54.867 0 0031.361-9.8H23.64a54.867 54.867 0 0031.361 9.8zM20.482 88.728h69.025a54.887 54.887 0 008.8-8.911H11.682a56.245 56.245 0 008.8 8.911zM9.262 76.492h91.476a54.95 54.95 0 004.411-7.957H4.851a54.95 54.95 0 004.41 7.957zM3.124 64.255h103.752a54.896 54.896 0 001.969-7.002H1.166a53.117 53.117 0 001.958 7.002zM0 46.015c0 2.03.121 4.039.33 6.003h109.34c.22-1.975.33-3.973.33-6.003v-.033H0v.033zM.363 39.782h109.274a54.71 54.71 0 00-.814-5.07H1.177a55.308 55.308 0 00-.814 5.07zM3.2 27.556H106.8a58.547 58.547 0 00-1.672-4.115H4.873A51.945 51.945 0 003.2 27.556zM9.405 15.32h91.19a59.831 59.831 0 00-2.321-3.161H11.726a59.814 59.814 0 00-2.321 3.16zM23.716.888a57.211 57.211 0 00-2.959 2.195h68.475A52.837 52.837 0 0086.273.888H23.716z",fill:"currentColor"}))}var r2=null;function a2(e){return React60.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React60.createElement("path",{d:"M100 38.086V0H61.914v9.93h21.132L54.963 38.013V16.88h-9.93v21.132L16.951 9.93h21.135V0H0v38.086h9.93V16.951l28.083 28.082H16.88v9.93h21.132L9.93 83.046V61.914H0V100h38.086v-9.93H16.951l28.082-28.086v21.135h9.93V61.984L83.046 90.07H61.914V100H100V61.914h-9.93v21.132L61.987 54.963H83.12v-9.93H61.987L90.07 16.951v21.135H100z",fill:"currentColor"}))}var n2=null;function l2(e){return React61.createElement("svg",i({viewBox:"0 0 142 142",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React61.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M19.945 50.767l50.766 50.766 50.765-50.766 19.944 19.944-51.672 51.673c-10.514 10.514-27.56 10.514-38.075 0L.001 70.711l19.944-19.944z",fill:"currentColor"}),React61.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M70.509 55.733l-27.901-27.63L23.57 47.14l28.354 28.084c10.264 10.264 26.904 10.264 37.168 0l28.48-28.362-19.038-19.037L70.51 55.733z",fill:"currentColor"}),React61.createElement("circle",{cx:70.71,cy:24.88,transform:"rotate(-45 70.71 24.88)",fill:"currentColor",r:17.592}))}var o2=null;function i2(e){return React62.createElement("svg",i({viewBox:"0 0 101 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React62.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M47.333 0H0v47.333h47.333V0zM74 0H52.667v21.333H74V0zM52.667 26H74v21.333H52.667V26zm-5.333 26.667H0V100h47.333V52.667zm52.666 0H52.667V100H100V52.667zM78.667 26H100v21.333H78.667V26zm3-10.333h2.667v2.666h-2.667v-2.666zm-3 5.666v-8.666h8.667v8.666h-8.667zM84.334 3h-2.667v2.667h2.667V3zm-5.667-3v8.667h8.667V0h-8.667zm15.668 15.667H97v2.666h-2.666v-2.666zm-3 5.666v-8.666H100v8.666h-8.666zM97 3h-2.666v2.667H97V3zm-5.666-3v8.667H100V0h-8.666z",fill:"currentColor"}))}var s2=null;function d2(e){return React63.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React63.createElement("path",{d:"M0 12.288L12.287 0v87.71h37.706L37.706 100H0v-87.71zM49.994 63.743l12.287-12.276v36.245h37.72L87.714 100h-37.72V63.743zM49.994 33.336l12.287-12.288v18.129h37.72L87.714 51.465h-37.72V33.336z",fill:"currentColor"}),React63.createElement("path",{d:"M49.993 12.288L62.28 0v9.064H100L87.713 21.353h-37.72v-9.065z",fill:"currentColor"}))}var c2=null;function u2(e){return React64.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React64.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 0h100v100H0V0zm17.12 10.344h-6.54v6.54h6.54v-6.54zm6.392-.61l6.396 1.364-1.364 6.396-6.397-1.365 1.365-6.396zM17.89 23.208l-6.396-1.365-1.365 6.396 6.396 1.365 1.365-6.396zM50.496 8.99l4.507 4.74-4.74 4.507-4.507-4.74 4.74-4.507zm-32.25 41.271l-4.507-4.74L9 50.03l4.507 4.74 4.74-4.508zm18.708-41.1l5.702 3.204-3.203 5.702-5.702-3.204 3.203-5.702zM17.906 36.999l-5.702-3.204L9 39.497l5.702 3.204 3.204-5.702zm46.62-27.57l2.216 6.153L60.59 17.8l-2.216-6.154 6.153-2.216zm-46.12 53.986l-3.69-5.4-5.4 3.69 3.69 5.4 5.4-3.69zM77.57 9.96l.82 6.488-6.489.82-.82-6.488 6.489-.82zM17.577 77.17l-1.733-6.306-6.307 1.733 1.733 6.306 6.307-1.733zm7.303-55.86l5.627 3.334-3.333 5.627-5.627-3.333 3.333-5.627zm29.716 6.384l-2.311-6.118-6.119 2.311 2.312 6.118 6.118-2.31zm-15.582-6.457l3.744 5.363-5.363 3.744-3.744-5.363 5.363-3.744zm27.458 7.017l-1.45-6.378-6.378 1.451 1.45 6.377 6.378-1.45zm11.731-5.521l-.411 6.527-6.527-.411.41-6.527 6.528.41zm-47.559 15.49l-4.362-4.873-4.873 4.362 4.362 4.873 4.873-4.361zm22.144-4.204l1.542 6.356-6.356 1.541-1.542-6.355 6.356-1.542zm-10.132 5.2l-3.201-5.703-5.704 3.2 3.201 5.704 5.704-3.201zm23.253-4.438l-.165 6.538-6.538-.165.165-6.538 6.538.165zm12.84.891l-6.31-1.72-1.719 6.31 6.31 1.72 1.72-6.31zm-51.5 10.013l3.238 5.683-5.683 3.237-3.238-5.683 5.683-3.237zm26.346 7.784l.11-6.539-6.54-.11-.11 6.54 6.54.11zm-13.008-7.287l1.58 6.347-6.347 1.58-1.58-6.348 6.347-1.58zM66.6 47.896l-6.29-1.793-1.792 6.29 6.29 1.793 1.792-6.29zm6.863-2.197l5.718 3.174-3.174 5.718-5.719-3.174 3.175-5.718zM28.985 58.767l-6.513.598.598 6.513 6.513-.598-.598-6.513zm19.734-.761l5.978 2.654-2.655 5.978-5.977-2.655 2.654-5.977zm-7.014 1.293l-6.523-.477-.478 6.522 6.523.478.478-6.523zm20.341-1.573l5.108 4.084-4.084 5.108-5.108-4.084 4.084-5.108zm17.236 5.44l-3.703-5.39-5.391 3.702 3.703 5.391 5.39-3.703zm-55.967 7.587l6.458 1.034-1.034 6.458-6.458-1.034 1.034-6.458zm31.473 2.343l-5.81-3.004-3.003 5.81 5.81 3.004 3.003-5.81zm-19.53-2.16l6.51.615-.615 6.512-6.512-.616.616-6.511zm31.919 3.807l-4.375-4.862-4.862 4.374 4.374 4.862 4.863-4.374zm8.616-4.746l3.444 5.56-5.56 3.444-3.444-5.56 5.56-3.444zM17.121 83.406h-6.54v6.54h6.54v-6.54zm7.036-1.184l6.1 2.356-2.356 6.101-6.1-2.356 2.356-6.101zm30.846 4.345l-4.507-4.74-4.74 4.508 4.508 4.739 4.739-4.507zm-18.049-4.57l5.702 3.205-3.203 5.701L33.75 87.7l3.203-5.702zm29.788 6.422l-2.216-6.154-6.153 2.217 2.216 6.153 6.153-2.216zm10.827-5.623l.82 6.489-6.489.82-.82-6.489 6.489-.82zm12.605-72.452h-6.54v6.54h6.54v-6.54zm-5.627 11.5l6.396 1.365-1.365 6.396-6.396-1.365 1.365-6.396zm6.752 28.417l-4.507-4.74-4.739 4.508 4.507 4.74 4.74-4.508zm-6.044-16.466L90.957 37l-3.204 5.702-5.701-3.204 3.203-5.702zm6.205 29.62l-3.69-5.4-5.4 3.69 3.69 5.4 5.4-3.69zm-2.563 7.449l1.733 6.306-6.306 1.733-1.734-6.306 6.307-1.733zm1.276 12.542h-6.54v6.54h6.54v-6.54z",fill:"currentColor"}))}var h2=null;function m2(e){return React65.createElement("svg",i({viewBox:"0 0 101 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React65.createElement("path",{fill:"currentColor",d:"M.001 53.596h47.333v47.333H.001zM52.667 53.596H100v47.333H52.667zM52.667 26.929H74v21.333H52.667zM52.667.929H74v21.333H52.667zM78.667 26.929H100v21.333H78.667zM78.667 13.596h8.667v8.667h-8.667zM78.667.929h8.667v8.667h-8.667zM91.335 13.596h8.667v8.667h-8.667zM91.335.929h8.667v8.667h-8.667zM0 .929h47.333v47.333H0z"}))}var v2=null;function g2(e){return React66.createElement("svg",i({viewBox:"0 0 101 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React66.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M62.467 36.689c5.566-3.544 9.253-9.73 9.253-16.769C71.72 8.92 62.713 0 51.603 0c-8.12 0-15.118 4.766-18.295 11.627a17.717 17.717 0 00-15.593-9.231C7.942 2.396.02 10.241.02 19.919c0 7.906 5.286 14.589 12.55 16.77C5.296 38.874 0 45.565 0 53.48c0 8.41 5.977 15.439 13.954 17.146-5.396 1.6-9.329 6.554-9.329 12.419 0 7.158 5.86 12.96 13.089 12.96s13.089-5.802 13.089-12.96c0-5.865-3.933-10.819-9.33-12.419a17.725 17.725 0 0011.834-8.813 20.078 20.078 0 007.207 8.31c-3.692 3.111-6.034 7.745-6.034 12.92 0 9.365 7.667 16.957 17.124 16.957 9.457 0 17.123-7.592 17.123-16.956 0-5.176-2.342-9.81-6.033-12.92 4.51-2.953 7.75-7.655 8.733-13.13 1.583 6.234 7.282 10.85 14.069 10.85 8.011 0 14.505-6.431 14.505-14.364 0-7.934-6.494-14.365-14.505-14.365-6.787 0-12.486 4.616-14.069 10.85-1-5.566-4.332-10.334-8.96-13.276zm-29.16 8.458a20.083 20.083 0 017.433-8.458 20.063 20.063 0 01-7.433-8.477A17.705 17.705 0 0122.86 36.69a17.725 17.725 0 0110.447 8.457zM59.671 19.92c0 4.413-3.612 7.99-8.069 7.99-4.456 0-8.069-3.577-8.069-7.99s3.613-7.99 8.07-7.99c4.456 0 8.069 3.577 8.069 7.99zm4.036 33.56c0 6.619-5.42 11.985-12.104 11.985-6.685 0-12.104-5.366-12.104-11.986 0-6.619 5.42-11.985 12.104-11.985 6.685 0 12.104 5.366 12.104 11.986zm-41.96.001c0 2.207-1.806 3.995-4.034 3.995-2.228 0-4.034-1.788-4.034-3.995 0-2.206 1.806-3.995 4.034-3.995 2.228 0 4.035 1.789 4.035 3.995zm61.309 29.562c0-1.335 1.092-2.416 2.44-2.416 1.347 0 2.439 1.081 2.439 2.416 0 1.334-1.092 2.415-2.44 2.415-1.347 0-2.44-1.081-2.44-2.415zm2.44-10.37c-5.784 0-10.472 4.643-10.472 10.37 0 5.726 4.688 10.368 10.471 10.368s10.472-4.642 10.472-10.368c0-5.727-4.689-10.37-10.472-10.37zm.345-55.186c-1.347 0-2.44 1.081-2.44 2.416 0 1.334 1.093 2.415 2.44 2.415s2.44-1.081 2.44-2.415c0-1.335-1.093-2.416-2.44-2.416zm-10.47 2.416c0-5.727 4.687-10.37 10.47-10.37s10.471 4.643 10.471 10.37c0 5.726-4.688 10.368-10.47 10.368-5.784 0-10.472-4.642-10.472-10.368zM44.52 83.043c0-3.873 3.171-7.014 7.084-7.014 3.912 0 7.084 3.14 7.084 7.015 0 3.874-3.172 7.014-7.084 7.014-3.913 0-7.084-3.14-7.084-7.014zm-26.806-3.018c-1.684 0-3.05 1.352-3.05 3.02 0 1.667 1.366 3.02 3.05 3.02 1.684 0 3.05-1.353 3.05-3.02 0-1.668-1.366-3.02-3.05-3.02zm-6.398-60.106c0-3.5 2.865-6.337 6.4-6.337 3.533 0 6.398 2.837 6.398 6.337 0 3.5-2.865 6.337-6.399 6.337s-6.399-2.837-6.399-6.337zm74.18 27.15c-3.576 0-6.474 2.87-6.474 6.41 0 3.541 2.898 6.411 6.474 6.411 3.575 0 6.474-2.87 6.474-6.41 0-3.541-2.899-6.411-6.474-6.411zM27.397 53.48c0 5.296-4.335 9.589-9.683 9.589-5.347 0-9.682-4.293-9.682-9.589 0-5.295 4.335-9.588 9.682-9.588 5.348 0 9.683 4.293 9.683 9.588z",fill:"currentColor"}))}var p2=null;function f2(e){return React67.createElement("svg",i({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React67.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M48 8.727C26.31 8.727 8.727 26.31 8.727 48c0 6.558 1.608 12.74 4.45 18.175a35.829 35.829 0 01-.462-5.749c0-19.647 15.927-35.573 35.574-35.573 19.646 0 35.573 15.926 35.573 35.573 0 1.395-.08 2.77-.236 4.123a39.123 39.123 0 003.647-16.55C87.273 26.31 69.69 8.728 48 8.728zm.708 78.539c.328-.006.655-.016.98-.03a27 27 0 001.832-.156c6.84-1.128 12.056-7.069 12.056-14.227 0-7.964-6.456-14.42-14.42-14.42-7.964 0-14.42 6.456-14.42 14.42 0 7.814 6.215 14.176 13.972 14.413zM26.177 75.655a23.374 23.374 0 01-.168-2.802c0-12.784 10.363-23.148 23.147-23.148 12.648 0 22.928 10.145 23.144 22.742a26.734 26.734 0 002.835-12.02c0-14.828-12.02-26.847-26.846-26.847-14.827 0-26.847 12.02-26.847 26.846a26.722 26.722 0 004.735 15.229zm22.58 20.342a36.51 36.51 0 01-.635.002H48C21.49 96 0 74.51 0 48 0 21.49 21.49 0 48 0s48 21.49 48 48c0 25.236-19.475 45.923-44.216 47.853a23.393 23.393 0 01-3.027.144z",fill:"currentColor"}))}var b2=null;function C2(e){return React68.createElement("svg",i({viewBox:"0 0 100 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React68.createElement("path",{d:"M49.027 25.443a24.514 24.514 0 10-24.513 24.513V25.443h24.513zM75.486 49.956a24.513 24.513 0 10-24.513-24.513h24.513v24.513zM50.973 76.415a24.514 24.514 0 1024.513-24.513v24.513H50.973zM24.514 51.902a24.513 24.513 0 1024.513 24.513H24.514V51.902z",fill:"currentColor"}))}var w2=null;function E2(e){return React69.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React69.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 0h100v100H0V0zm10 10h80v80H10V10zm10 10h60v10H20V20zm30 27h22c-2.57-9.778-11.443-17-22.008-17C39.411 30 30.554 37.222 28 47h22zm0 0c9.389 0 17 7.387 17 16.5S59.389 80 50 80s-17-7.387-17-16.5S40.611 47 50 47z",fill:"currentColor"}))}var y2=null;function z2(e){return React70.createElement("svg",i({viewBox:"0 0 110 111",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React70.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M55 110.929c30.376 0 55-24.624 55-55s-24.624-55-55-55-55 24.624-55 55 24.624 55 55 55zm-6.108-79.595l6.11-24.877 6.09 24.877h-12.2zm-18.63-18.26l7.149 24.595 10.563-6.091-17.711-18.504zm.387 35.831L12.145 31.194l24.595 7.148-6.091 10.563zM5.528 55.93l24.877 6.092V49.82L5.528 55.93zM36.74 73.498l-24.595 7.148L30.65 62.935l6.091 10.563zm-6.477 25.266l17.711-18.503-10.563-6.092-7.148 24.595zm30.83-18.257L55 105.384l-6.109-24.877h12.2zm18.622 18.257L72.567 74.17l-10.563 6.092 17.711 18.503zm-.383-35.829l18.503 17.711-24.595-7.148 6.092-10.563zm25.121-7.005l-24.877-6.11v12.202l24.877-6.092zM73.24 38.342l24.595-7.148-18.503 17.711-6.092-10.563zm6.475-25.268L62.004 31.578l10.563 6.091 7.148-24.595zM52.271 44.978l2.73-11.092 2.71 11.091h-5.44zm-8.293-8.136l3.187 10.95 4.7-2.71-7.887-8.24zm.177 15.953l-8.24-7.888 10.951 3.187-2.711 4.7zm-11.198 3.134l11.092 2.712V53.2l-11.092 2.728zm13.91 7.816l-10.952 3.187 8.24-7.888 2.711 4.7zm-2.889 11.252l7.888-8.24-4.7-2.711-3.188 10.95zm13.734-8.12L55 77.951l-2.728-11.074h5.44zm8.293 8.12l-3.187-10.951-4.7 2.711 7.887 8.24zm-.18-15.953l8.24 7.888-10.95-3.187 2.71-4.7zm11.202-3.115L65.953 53.2v5.44l11.074-2.71zm-13.912-7.835l10.95-3.187-8.24 7.888-2.71-4.7zm2.89-11.252l-7.888 8.24 4.701 2.71 3.187-10.95z",fill:"currentColor"}))}var x2=null;function $2(e){return React71.createElement("svg",i({viewBox:"0 0 134 134",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React71.createElement("path",{d:"M64.657 63.942L19.983 19.267l-.708.707 44.708 44.708L9.227 33.067l-.5.866L63.4 65.5h-.063L2.407 49.176l-.26.966L59.475 65.5H0v3h55.604L1.889 82.89l.776 2.898 53.719-14.391L8.227 99.2l1.5 2.598 48.184-27.82-39.343 39.343.709.708-.002.001.708.708v-.002l.707.706 39.298-39.299-27.787 48.128 2.598 1.5 27.83-48.202-14.404 53.764 2.898.776L65.5 78.447V134h3V78.395l14.39 53.715.98-.262v.002l.966-.258v-.003l.953-.255-14.392-53.719L99.2 125.772l2.598-1.5-27.803-48.154 39.326 39.325.711-.711.007.007.707-.708-.007-.007.703-.702-39.325-39.326 48.154 27.803 1.5-2.598-48.157-27.804 53.719 14.391.776-2.897L78.395 68.5H134v-3H74.525l57.326-15.358-.259-.966L70.661 65.5h-.064l54.674-31.567-.5-.866-54.697 31.58 44.673-44.673-.707-.707-44.728 44.728 31.621-54.768-.866-.5-31.576 54.69 16.345-61.01-.966-.26L67.5 63.252V0h-1v63.15L50.157 2.148l-.966.258 16.368 61.098L33.933 8.727l-.866.5 31.59 54.715z",fill:"currentColor"}))}var M2=null;function k2(e){return React72.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React72.createElement("g",{clipPath:"url(#Record_svg__clip0)",fill:"currentColor"},React72.createElement("path",{d:"M79.819 62.343c6.818-16.462-.999-35.334-17.46-42.153-16.463-6.82-35.336.998-42.155 17.46-6.819 16.462.998 35.335 17.46 42.154 16.463 6.819 35.335-.999 42.154-17.46zM53.659 0h-7.303v8.763h7.303V0zM40.498.773l-6.87 1.84 2.268 8.465 6.87-1.84L40.498.772zM28.003 4.978l-5.996 3.46 4.38 7.59 5.996-3.46-4.38-7.59zM17.048 12.274l-4.761 4.76 6.196 6.197 4.761-4.76-6.196-6.197zM8.34 22.174L5.07 27.84l7.588 4.381 3.271-5.666-7.588-4.381zM2.522 33.984L.878 40.121l8.464 2.268 1.644-6.137-8.464-2.268zM8.763 46.926H0v6.163h8.763v-6.163zM9.362 57.697L.898 59.965l1.595 5.953 8.464-2.268-1.595-5.953zM12.806 68.033l-7.589 4.382 2.987 5.173 7.589-4.382-2.987-5.173zM18.811 77.097l-6.196 6.197 4.09 4.09 6.196-6.197-4.09-4.09zM26.969 84.311L22.587 91.9l4.844 2.797 4.382-7.59-4.844-2.796zM36.721 89.14l-2.27 8.464 5.22 1.4 2.27-8.464-5.22-1.4zM52.607 91.237h-5.214V100h5.214v-8.763zM63.083 89.192l-4.839 1.296 2.268 8.464 4.839-1.296-2.268-8.464zM72.698 84.501l-4.173 2.41 4.381 7.59 4.174-2.41-4.382-7.59zM80.772 77.506L77.5 80.78l6.196 6.196 3.274-3.274-6.197-6.196zM86.813 68.694l-2.22 3.845 7.59 4.382 2.22-3.845-7.59-4.382zM90.385 58.633l-1.1 4.105 8.464 2.268 1.1-4.105-8.464-2.268zM100 47.962h-8.763v4.06H100v-4.06zM97.796 35.184l-8.464 2.267 1.002 3.739 8.464-2.268-1.002-3.738zM92.37 23.41l-7.589 4.381 1.84 3.188 7.59-4.382-1.84-3.187zM84.1 13.424l-6.197 6.195 2.467 2.469 6.198-6.195-2.467-2.469zM73.564 5.885l-4.383 7.588 2.858 1.65 4.383-7.587-2.858-1.651zM61.446 1.297l-2.27 8.465 3.005.805 2.27-8.464-3.005-.806z"})),React72.createElement("defs",null,React72.createElement("clipPath",{id:"Record_svg__clip0"},React72.createElement("path",{fill:"#fff",d:"M0 0h100v100H0z"}))))}var L2=null;function R2(e){return React73.createElement("svg",i({viewBox:"0 0 134 134",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React73.createElement("path",{d:"M64.676 50.418L55.95.916l-1.164.207 8.727 49.502c.195-.042.384-.083.58-.119.194-.035.39-.059.584-.088zM44.664 3.828l-1.158.42L60.694 51.48c.378-.153.768-.29 1.158-.42L44.664 3.829zM34.058 8.656l-1.11.644 25.128 43.528c.36-.225.733-.443 1.111-.644L34.058 8.656zM24.444 15.243l-1.022.856L55.73 54.606c.33-.302.668-.586 1.022-.857L24.444 15.243zM16.117 23.403l-.892 1.058L53.73 56.769c.283-.366.579-.715.892-1.058L16.117 23.403zM9.336 32.88l-.715 1.241 43.534 25.135c.225-.425.461-.839.715-1.247L9.336 32.88zM4.295 43.387l-.508 1.394 47.24 17.194c.147-.473.318-.94.507-1.394L4.295 43.387zM1.153 54.606l-.266 1.519 49.502 8.727c.065-.509.153-1.017.266-1.513L1.153 54.606zM0 66.205v1.59h50.27a15.808 15.808 0 010-1.59H0zM50.375 69.076L.867 77.803l.296 1.66 49.508-8.726c-.066-.272-.119-.55-.166-.828a13.631 13.631 0 01-.13-.833zM3.746 89.102l.597 1.636 47.245-17.194a16.817 16.817 0 01-.591-1.636L3.747 89.102zM8.525 99.725l.893 1.548 43.534-25.135a16.699 16.699 0 01-.892-1.548L8.525 99.725zM15.086 109.361l1.182 1.413 38.518-32.32c-.42-.45-.816-.916-1.182-1.406L15.086 109.36zM23.207 117.715l1.448 1.217 32.32-38.518c-.503-.378-.993-.78-1.454-1.211l-32.314 38.512zM32.662 124.54l1.678.969 25.141-43.54c-.579-.29-1.14-.62-1.678-.975l-25.14 43.546zM43.152 129.623l1.873.679 17.2-47.25c-.638-.19-1.264-.42-1.873-.68l-17.2 47.251zM54.36 132.807l2.008.355 8.733-49.52a16.216 16.216 0 01-2.009-.354l-8.733 49.519zM65.951 134h2.092V83.718c-.703.047-1.4.042-2.092 0V134zM68.846 83.646l8.733 49.525 2.109-.372-8.733-49.525c-.343.082-.697.16-1.052.224-.348.06-.703.107-1.057.148zM88.883 130.337l2.063-.751-17.2-47.25c-.662.29-1.353.543-2.062.75l17.2 47.251zM99.528 125.585l1.944-1.123L76.325 80.91a16.63 16.63 0 01-1.944 1.123l25.147 43.552zM109.189 119.063l1.761-1.477-32.326-38.523c-.55.531-1.14 1.022-1.76 1.477l32.325 38.523zM117.575 110.967l1.506-1.796-38.53-32.332a16.83 16.83 0 01-1.506 1.797l38.53 32.331zM124.423 101.539l1.2-2.074-43.558-25.147a16.44 16.44 0 01-1.2 2.074l43.558 25.147zM129.54 91.069l.839-2.299-47.257-17.2c-.224.792-.508 1.56-.839 2.299l47.257 17.2zM132.764 79.867l.431-2.458-49.531-8.733c-.083.839-.23 1.66-.432 2.458l49.532 8.733zM133.999 68.272v-2.546h-50.3c.065.857.065 1.707.006 2.546H134zM83.666 65.383l49.543-8.732-.449-2.559-49.543 8.733a15.696 15.696 0 01.45 2.558zM130.415 45.33l-.904-2.493-47.269 17.205c.36.798.662 1.631.904 2.494l47.269-17.206zM125.7 34.671l-1.353-2.34-43.564 25.153a16.98 16.98 0 011.353 2.34L125.7 34.671zM119.213 24.988l-1.767-2.11-38.542 32.338c.644.65 1.235 1.353 1.773 2.103l38.536-32.331zM111.141 16.573l-2.145-1.802-32.338 38.542a17.328 17.328 0 012.145 1.802l32.338-38.542zM101.732 9.69l-2.47-1.424-25.159 43.576c.863.407 1.69.88 2.47 1.424L101.732 9.69zM74.07 51.817L91.28 4.537l-2.73-.993-17.188 47.227-.011.053c.939.255 1.849.585 2.718.993z",fill:"currentColor"}),React73.createElement("path",{d:"M71.346 50.825l.017-.047 8.728-49.496-2.908-.514-8.662 49.1v.455a16.15 16.15 0 012.825.502z",fill:"currentColor"}),React73.createElement("path",{d:"M71.354 50.825l.011-.053-.017.047c0 .006.006.006.006.006zM68.522 49.868V0h-3.043v50.323a16.573 16.573 0 012.966-.012l.077-.443z",fill:"currentColor"}),React73.createElement("path",{d:"M68.52 50.317v-.449l-.077.444c.024 0 .053.005.077.005z",fill:"currentColor"}))}var _2=null;function H2(e){return React74.createElement("svg",i({viewBox:"0 0 110 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React74.createElement("path",{d:"M55 105c27.615 0 50-22.386 50-50S82.615 5 55 5C27.386 5 5 27.386 5 55s22.386 50 50 50z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React74.createElement("path",{d:"M60.849 5.33c13.693 12.157 22.34 29.89 22.34 49.653 0 19.744-8.63 37.495-22.322 49.652M49.131 5.33c-13.693 12.157-22.34 29.89-22.34 49.653 0 19.744 8.629 37.495 22.322 49.652",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React74.createElement("path",{d:"M97.467 26.024C86.589 36.9 71.58 43.61 54.999 43.61c-16.07 0-30.658-6.307-41.444-16.6M97.467 83.958C86.589 73.08 71.58 66.37 54.999 66.37c-16.07 0-30.658 6.307-41.444 16.6M104.981 55H5M55 104.982V5",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}))}var S2=null;function I2(e){return React75.createElement("svg",i({viewBox:"0 0 110 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React75.createElement("path",{d:"M55 0C24.626 0 0 24.626 0 55s24.626 55 55 55 55-24.626 55-55S85.374 0 55 0zm0 109.525L.49 55 55 .49l54.525 54.525L55 109.525z",fill:"currentColor"}),React75.createElement("path",{d:"M27.923 27.923v54.139H82.06V27.923H27.923zm27.076 52.074c-13.798 0-24.982-11.184-24.982-24.982S41.201 30.032 55 30.032c13.799 0 24.983 11.185 24.983 24.983 0 13.783-11.184 24.982-24.983 24.982z",fill:"currentColor"}))}var B2=null;function O2(e){return React76.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React76.createElement("path",{d:"M100 100H0V0h100v100zM10 90h80V10H10v80z",fill:"currentColor"}),React76.createElement("path",{d:"M50.008 39.806L80 54v-9.806L50.008 30 20 44.194V54l30.008-14.194zM80 20H20v10h60V20z",fill:"currentColor"}))}var D2=null;function V2(e){return React77.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React77.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 0h100v100H0V0zm32.854 35.063L10.163 10h79.674L67.146 35.063h22.691L63.96 53.295h25.877L61.804 66.97h28.033l-25.895 9.357h25.895l-23.902 6.477h23.902L50 90l-39.837-7.197h23.902l-23.902-6.477h25.895l-25.895-9.357h28.033L10.163 53.295H36.04L10.163 35.063h22.691z",fill:"currentColor"}))}var W2=null;function A2(e){return React78.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React78.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M100 0H0v100h100V0zM10 17.071V90h72.929L64.594 71.665v8.412h-10V54.594h25.434v10h-8.363L90 82.929V10H17.071l18.43 18.43.07-8.546 9.999.08-.204 25.443H19.973v-10h8.363L10 17.07zm19.745 37.701h-10v25.483H45.18v-10h-8.365l33.44-33.452v8.425h10V19.745H54.822v10h8.35L29.745 63.18v-8.409z",fill:"currentColor"}))}var P2=null;function T2(e){return React79.createElement("svg",i({viewBox:"0 0 110 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React79.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M50.028 9.658C27.178 12.136 9.39 31.491 9.39 55c0 8.832 2.51 17.078 6.857 24.063-2.302-8.325-2.151-17.035.801-24.035l-.015-.03.245-.498a25.44 25.44 0 01.81-1.65c6.717-13.595 20.721-22.947 36.91-22.948 12.318-.013 23.354 5.414 30.887 13.98.329-5.954-1.19-12.893-4.87-19.106-5.552-9.378-15.74-16.548-30.987-15.116v-.002zm42.655 45.894l.272-.551-.017-.034c2.956-7.012 3.1-15.739.787-24.075A45.397 45.397 0 01100.61 55c0 23.515-17.795 42.873-40.654 45.344v-.004c-15.246 1.431-25.435-5.739-30.987-15.117-3.678-6.212-5.198-13.148-4.87-19.102 7.534 8.562 18.582 13.976 30.902 13.976 16.2 0 30.185-9.394 36.896-22.95.28-.52.542-1.052.786-1.595zM55 0C24.624 0 0 24.624 0 55s24.624 55 55 55 55-24.624 55-55S85.376 0 55 0zm27.39 54.998c-3.929-6.688-10.221-11.812-17.719-14.21 4.53 3.092 7.504 8.297 7.504 14.195 0 5.93-3.012 11.157-7.582 14.243 7.533-2.393 13.855-7.527 17.798-14.228zM27.592 55c3.927-6.69 10.223-11.806 17.728-14.205-4.525 3.093-7.494 8.294-7.494 14.188 0 5.934 3.01 11.165 7.585 14.25C37.858 66.845 31.527 61.71 27.591 55zM55 47.198a7.785 7.785 0 000 15.57c4.287 0 7.784-3.49 7.784-7.785A7.785 7.785 0 0055 47.198z",fill:"currentColor"}))}var F2=null;function Z2(e){return React80.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React80.createElement("g",{clipPath:"url(#Share_with_Your_Team_(Team_Library)_svg__clip0)",fill:"currentColor"},React80.createElement("path",{d:"M33.33 24.946V8.384L24.946 0v24.946H0l8.384 8.384H33.33v-8.384zM58.286 33.33h8.385V8.384L58.286 0v24.946H33.331l8.394 8.384h16.561z"}),React80.createElement("path",{d:"M100 8.384L91.614 0v24.946H66.67l8.385 8.384H100V8.384zM33.33 58.286V41.724l-8.384-8.394v24.956H0l8.384 8.384H33.33v-8.384zM33.33 58.286l8.395 8.384H66.67V41.724l-8.385-8.394v24.956H33.331zM66.67 58.286l8.384 8.384H100V41.724l-8.385-8.394v24.956H66.67zM24.946 66.67v24.946H0L8.384 100H33.33V75.054l-8.384-8.384zM58.286 66.67v24.946H33.331L41.725 100H66.67V75.054l-8.385-8.384zM66.67 91.616L75.053 100h24.945V75.054l-8.384-8.384v24.946H66.67z"})),React80.createElement("defs",null,React80.createElement("clipPath",{id:"Share_with_Your_Team_(Team_Library)_svg__clip0"},React80.createElement("path",{fill:"#fff",d:"M0 0h100v100H0z"}))))}var j2=null;function N2(e){return React81.createElement("svg",i({viewBox:"0 0 101 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React81.createElement("path",{fill:"currentColor",d:"M.001 52.667h47.333V100H.001zM52.667 52.667H100V100H52.667zM52.667 26H74v21.333H52.667zM52.667 0H74v21.333H52.667zM78.667 26H100v21.333H78.667zM78.667 12.667h8.667v8.667h-8.667zM78.667 0h8.667v8.667h-8.667zM91.335 12.667h8.667v8.667h-8.667zM91.335 0h8.667v8.667h-8.667zM0 0h47.333v47.333H0z"}))}var U2=null;function K2(e){return React82.createElement("svg",i({viewBox:"0 0 100 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React82.createElement("path",{d:"M34.27 50.002v15.73H50c-8.69 0-15.73-7.04-15.73-15.73zM65.73 50.002v-15.73H50c8.69 0 15.73 7.04 15.73 15.73zM50 34.272H34.27v15.73c0-8.69 7.04-15.73 15.73-15.73z",fill:"currentColor"}),React82.createElement("path",{d:"M50 65.732h15.73v-15.73c0 8.69-7.04 15.73-15.73 15.73z",fill:"currentColor"}),React82.createElement("path",{d:"M0 .002v100h100v-100H0zm81.46 10c3.48 1.79 6.2 4.84 7.57 8.54h-7.57v-8.54zm-15.73 0c6.1 0 11.38 3.47 13.99 8.54H65.73v-8.54zm-15.73 0c6.1 0 11.38 3.47 13.99 8.54H36.01c2.61-5.07 7.89-8.54 13.99-8.54zm-15.73 0v8.54H20.28c2.61-5.07 7.89-8.54 13.99-8.54zm-15.73 80c-3.48-1.79-6.2-4.84-7.57-8.54h7.57v8.54zm0-10.28c-5.07-2.61-8.54-7.89-8.54-13.99h8.54v13.99zm0-15.73c-5.07-2.61-8.54-7.89-8.54-13.99 0-6.1 3.47-11.38 8.54-13.99v27.98zm0-29.72H10c0-6.1 3.47-11.38 8.54-13.99v13.99zm0-15.73h-7.57c1.37-3.7 4.09-6.75 7.57-8.54v8.54zm62.92 71.46v-8.54h7.57c-1.37 3.7-4.09 6.75-7.57 8.54zm0-10.28v-13.99H90c0 6.1-3.47 11.38-8.54 13.99zm0-29.72v-13.99c5.07 2.61 8.54 7.89 8.54 13.99 0 6.1-3.47 11.38-8.54 13.99v-13.99c0 8.69-7.04 15.73-15.73 15.73h15.73c0 8.69-7.04 15.73-15.73 15.73h13.99c-2.61 5.07-7.89 8.54-13.99 8.54v-8.54-15.73c0 8.69-7.04 15.73-15.73 15.73h13.99c-2.61 5.07-7.89 8.54-13.99 8.54-6.1 0-11.38-3.47-13.99-8.54H50c-8.69 0-15.73-7.04-15.73-15.73v24.27c-6.1 0-11.38-3.47-13.99-8.54h13.99c-8.69 0-15.73-7.04-15.73-15.73h15.73c-8.69 0-15.73-7.04-15.73-15.73 0-8.69 7.04-15.73 15.73-15.73H18.54c0-8.69 7.04-15.73 15.73-15.73v15.73c0-8.69 7.04-15.73 15.73-15.73 8.69 0 15.73 7.04 15.73 15.73v-15.73c8.69 0 15.73 7.04 15.73 15.73v-13.99c5.07 2.61 8.54 7.89 8.54 13.99H65.73c8.69 0 15.73 7.04 15.73 15.73z",fill:"currentColor"}))}var G2=null;function Y2(e){return React83.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React83.createElement("path",{d:"M50 70c11.046 0 20-8.954 20-20s-8.954-20-20-20-20 8.954-20 20 8.954 20 20 20z",fill:"currentColor"}),React83.createElement("path",{d:"M31 50V0H0v100h99.999V69H31V50z",fill:"currentColor"}),React83.createElement("path",{d:"M100 66V0H34v31h35v35h31z",fill:"currentColor"}))}var X2=null;function J2(e){return React84.createElement("svg",i({viewBox:"0 0 101 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React84.createElement("path",{d:"M38.963 0C17.45 0 0 18.136 0 40.495v8.507h9.444C30.967 49.002 48 30.41 48 8.05V.002L38.963 0zM100.002 38.965c0-21.513-18.136-38.963-40.495-38.963H51v9.444c0 21.523 18.592 38.556 40.951 38.556H100l.002-9.037zM61.039 100.004c21.513 0 38.963-18.136 38.963-40.495v-8.507h-9.444c-21.523 0-38.556 18.592-38.556 40.951v8.049l9.037.002zM0 61.039c0 21.513 18.136 38.963 40.495 38.963h8.507v-9.444c0-21.523-18.592-38.556-40.952-38.556H.002L0 61.039z",fill:"currentColor"}))}var Q2=null;function q2(e){return React85.createElement("svg",i({viewBox:"0 0 110 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React85.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M55 10c-24.853 0-45 20.147-45 45s20.147 45 45 45 45-20.147 45-45-20.147-45-45-45zM0 55C0 24.624 24.624 0 55 0s55 24.624 55 55-24.624 55-55 55S0 85.376 0 55zm33.8-35.64H76v10H43.8v20.19h11.75v-9.87c14.131 0 25.59 11.459 25.59 25.59S69.681 90.86 55.55 90.86 29.96 79.401 29.96 65.27h10c0 8.609 6.981 15.59 15.59 15.59s15.59-6.981 15.59-15.59c0-8.535-6.863-15.47-15.37-15.588v9.868H33.8V19.36z",fill:"currentColor"}))}var e5=null;function t5(e){return React86.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React86.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M55.666 3h15.333v15.333H55.666V3zm-3 18.333V0h21.333v21.333H52.666zM70.999 29H55.666v15.333h15.333V29zm-18.333-3v21.333h21.333V26H52.666zm-5.333 26.667H0V100h47.333V52.667zm52.666 0H52.666V100h47.333V52.667zM97 29H81.668v15.333H97V29zm-18.332-3v21.333H100V26H78.666zm3-10.333h2.666v2.666h-2.666v-2.666zm-3 5.666v-8.666h8.666v8.666h-8.666zM84.332 3h-2.666v2.667h2.666V3zm-5.666-3v8.667h8.666V0h-8.666zm15.667 15.667h2.667v2.666h-2.667v-2.666zm-3 5.666v-8.666h8.667v8.666h-8.667zM97.001 3h-2.667v2.667h2.667V3zm-5.667-3v8.667h8.667V0h-8.667zm-44 0H0v47.333h47.333V0z",fill:"currentColor"}))}var r5=null;function a5(e){return React87.createElement("svg",i({viewBox:"0 0 106 106",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React87.createElement("path",{d:"M53 101c26.51 0 48-21.49 48-48S79.51 5 53 5 5 26.49 5 53s21.49 48 48 48z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React87.createElement("path",{d:"M53 100.986c26.51 0 48-14.563 48-32.527 0-17.965-21.49-32.528-48-32.528S5 50.494 5 68.46c0 17.964 21.49 32.527 48 32.527z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React87.createElement("path",{d:"M53 100.998c26.51 0 48-8.682 48-19.39 0-10.71-21.49-19.391-48-19.391S5 70.898 5 81.607c0 10.71 21.49 19.391 48 19.391z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React87.createElement("path",{d:"M53 100.984c26.51 0 48-3.908 48-8.728S79.51 83.53 53 83.53 5 87.436 5 92.256s21.49 8.728 48 8.728z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}))}var n5=null;function l5(e){return React88.createElement("svg",i({viewBox:"0 0 111 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React88.createElement("path",{d:"M.223 57.064l-.208-.356a55.069 55.069 0 002.244 13.991l44.404-40.904-46.44 27.27zM3.27 73.804C10.953 94.924 31.208 110 55 110c23.926 0 44.285-15.269 51.865-36.582l-51.582-47.53L3.27 73.804zm88.867-9.358v24.36L64.838 63.584v39.003a1.49 1.49 0 01-1.486 1.486H47.287a1.49 1.49 0 01-1.486-1.486V63.585l-27.388 25.22V64.446l36.914-33.983 36.81 33.983zM107.861 70.299a54.916 54.916 0 002.125-13.442L63.873 29.78 107.861 70.3zM63.115 25.873l46.886 27.537c-.148-5.228-1.01-10.293-2.526-15.06l-44.36-12.477zM2.482 38.543C.966 43.356.119 48.465 0 53.753l47.436-27.864L2.482 38.543z",fill:"currentColor"}),React88.createElement("path",{d:"M106.241 34.934C98.216 14.482 78.302 0 55.001 0 31.625 0 11.68 14.57 3.7 35.112l51.582-14.511 50.958 14.333z",fill:"currentColor"}))}var o5=null;function i5(e){return React89.createElement("svg",i({viewBox:"0 0 104 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React89.createElement("path",{d:"M98.75 100.001c0-25.889-20.986-46.876-46.874-46.876C25.987 53.125 5 74.112 5 100.001",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React89.createElement("path",{d:"M16.704 100.001c0-19.416 15.74-35.171 35.172-35.171 19.43 0 35.171 15.74 35.171 35.171",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React89.createElement("path",{d:"M28.213 100.001c0-13.07 10.593-23.648 23.648-23.648 13.054 0 23.662 10.579 23.662 23.648",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React89.createElement("path",{d:"M39.736 100c0-6.692 5.432-12.124 12.124-12.124 6.693 0 12.124 5.432 12.124 12.124M5 0c0 25.889 20.987 46.875 46.875 46.875C77.764 46.875 98.751 25.89 98.751 0",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React89.createElement("path",{d:"M87.047 0c0 19.416-15.74 35.171-35.172 35.171-19.43 0-35.171-15.74-35.171-35.171",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React89.createElement("path",{d:"M75.538 0c0 13.07-10.593 23.648-23.648 23.648-13.054 0-23.662-10.579-23.662-23.648",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React89.createElement("path",{d:"M64.015 0c0 6.693-5.432 12.124-12.124 12.124S39.767 6.693 39.767.002",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}))}var s5=null;function d5(e){return React90.createElement("svg",i({viewBox:"0 0 110 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React90.createElement("path",{d:"M5 55h99.984c0 27.61-22.375 50-50 50S5 82.61 5 55z",fill:"currentColor",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React90.createElement("path",{d:"M55 105c27.614 0 50-22.386 50-50S82.614 5 55 5 5 27.386 5 55s22.386 50 50 50z",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React90.createElement("path",{d:"M23.534 55C23.534 37.62 37.62 23.534 55 23.534c17.382 0 31.466 14.085 31.466 31.466",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}),React90.createElement("path",{d:"M42.053 55c0-7.138 5.794-12.932 12.932-12.932 7.138 0 12.932 5.794 12.932 12.932",stroke:"currentColor",strokeWidth:10,strokeMiterlimit:10}))}var c5=null;function u5(e){return React91.createElement("svg",i({viewBox:"0 0 100 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React91.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M100 .929H0v100h100v-100zm-54.528 18.32v4.298l9.051-4.299h-9.05zm0 14.937v-5.883h9.051l-9.05 5.883zm0 3.166v7.467l9.051-7.467h-9.05zm0 18.1V46.4h9.051l-9.05 9.05zm0 1.586v7.467l9.051-7.467h-9.05zm0 16.517v-5.883h9.051l-9.05 5.883zm0 4.75v4.3l9.051-4.3h-9.05zM88.01 91.66v-2.715h2.715l-2.715 2.715zm0-13.354v4.3l2.715-4.3H88.01zm0-4.75v-5.883h2.715l-2.715 5.883zm0-16.517v7.467l2.715-7.467H88.01zm0-1.586V46.4h2.715l-2.715 9.05zm0-18.1v7.467l2.715-7.467H88.01zm0-3.166v-5.883h2.715l-2.715 5.883zm0-14.938v4.3l2.715-4.3H88.01zm0-6.334V10.2h2.715l-2.715 2.716zm-10.633 76.03v2.715l4.3-2.715h-4.3zm0-6.34v-4.299h4.3l-4.3 4.3zm0-14.932v5.883l4.3-5.883h-4.3zm0-3.167v-7.467h4.3l-4.3 7.467zm0-18.104v9.05l4.3-9.05h-4.3zm0-1.582v-7.467h4.3l-4.3 7.467zm0-16.516v5.883l4.3-5.883h-4.3zm0-4.756v-4.299h4.3l-4.3 4.3zm0-13.348v2.716l4.3-2.716h-4.3zM66.741 91.66v-2.715h5.883l-5.883 2.715zm0-13.354v4.3l5.883-4.3h-5.883zm0-4.75v-5.883h5.883l-5.883 5.883zm0-16.517v7.467l5.883-7.467h-5.883zm0-1.586V46.4h5.883l-5.883 9.05zm0-18.1v7.467l5.883-7.467h-5.883zm0-3.166v-5.883h5.883l-5.883 5.883zm0-14.938v4.3l5.883-4.3h-5.883zm0-6.334V10.2h5.883l-5.883 2.716zm-10.634 76.03v2.715l7.467-2.715h-7.467zm0-6.339v-4.3h7.467l-7.467 4.3zm0-14.932v5.883l7.467-5.883h-7.467zm0-3.168v-7.467h7.467l-7.467 7.467zm0-18.104v9.051l7.467-9.05h-7.467zm0-1.582v-7.467h7.467l-7.467 7.467zm0-16.516v5.883l7.467-5.883h-7.467zm0-4.755v-4.3h7.467l-7.467 4.3zm.001-13.348v2.715l7.467-2.715h-7.467zm-10.636 2.715v-2.716h9.051l-9.05 2.716zm-9.051 76.029v2.715l7.467-2.715H36.42zm0-6.34v-4.299h7.467l-7.467 4.3zm0-14.932v5.883l7.467-5.883H36.42zm0-3.167v-7.467h7.467l-7.467 7.467zm0-18.104v9.05l7.467-9.05H36.42zm0-1.582v-7.467h7.467l-7.467 7.467zm0-16.516v5.883l7.467-5.883H36.42zm0-4.756v-4.299h7.467l-7.467 4.3zm0-13.348v2.716l7.467-2.716H36.42zm-9.05 81.46v-2.715h5.883l-5.883 2.715zm0-13.354v4.3l5.883-4.3h-5.883zm0-4.75v-5.883h5.883l-5.883 5.883zm0-16.517v7.467l5.883-7.467h-5.883zm0-1.586V46.4h5.883l-5.883 9.05zm0-18.1v7.467l5.883-7.467h-5.883zm0-3.166v-5.883h5.883l-5.883 5.883zm0-14.938v4.3l5.883-4.3h-5.883zm0-6.334V10.2h5.883l-5.883 2.716zm-9.05 76.03v2.715l4.299-2.715h-4.3zm0-6.34v-4.299h4.299l-4.3 4.3zm0-14.932v5.883l4.299-5.883h-4.3zm0-3.167v-7.467h4.299l-4.3 7.467zm0-18.104v9.05l4.299-9.05h-4.3zm0-1.582v-7.467h4.299l-4.3 7.467zm0-16.516v5.883l4.299-5.883h-4.3zm0-4.756v-4.299h4.299l-4.3 4.3zm0-13.348v2.716l4.299-2.716h-4.3zm27.151 81.46v-2.715h9.051l-9.05 2.715zM9.27 88.944v2.715l2.715-2.715H9.27zm0-6.34v-4.299h2.715l-2.715 4.3zm0-14.932v5.883l2.715-5.883H9.27zm0-3.167v-7.467h2.715L9.27 64.505zm0-18.104v9.05l2.715-9.05H9.27zm0-1.582v-7.467h2.715L9.27 44.819zm0-16.516v5.883l2.715-5.883H9.27zm0-4.756v-4.299h2.715l-2.715 4.3zm0-13.348v2.715l2.716-2.715H9.268z",fill:"currentColor"}))}var h5=null;function m5(e){return React92.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React92.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M100 100H0V0h100v100zM67.146 64.937L89.837 90H10.163l22.691-25.063H10.163L36.04 46.705H10.163L38.196 33.03H10.163l25.895-9.357H10.163l23.902-6.477H10.163L50 10l39.837 7.197H65.935l23.902 6.477H63.942l25.895 9.357H61.804l28.033 13.674H63.96l25.877 18.232H67.146z",fill:"currentColor"}))}var v5=null;function g5(e){return React93.createElement("svg",i({viewBox:"0 0 110 110",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React93.createElement("path",{d:"M61.125 97.536H48.768v12.373h12.357V97.536zM81.608 88.743l-10.701 6.179 6.186 10.714 10.701-6.178-6.186-10.715zM94.92 70.897l-6.178 10.7 10.715 6.187 6.178-10.701-10.714-6.186zM89.445 61.127V48.77H78.014l9.91-5.724-6.178-10.71-9.895 5.724 5.724-9.895-10.71-6.179-5.724 9.895V20.45H48.769V31.88l-5.724-9.895-10.71 6.179 5.723 9.91-9.91-5.723-6.179 10.71 9.91 5.724H20.45v12.356h11.43l-9.91 5.724 6.179 10.71 9.91-5.723-5.723 9.91 10.71 6.178 5.724-9.91v11.431h12.356V78.032l5.724 9.91 10.71-6.178-5.724-9.895 9.895 5.724 6.179-10.71-9.91-5.724h11.447v-.031zM54.947 71.413c-9.095 0-16.465-7.37-16.465-16.465 0-9.095 7.37-16.465 16.465-16.465 9.095 0 16.465 7.37 16.465 16.465 0 9.095-7.37 16.465-16.465 16.465zM109.91 48.77H97.538v12.356h12.372V48.77zM99.46 22.114l-10.714 6.187L94.925 39l10.714-6.186-6.178-10.7zM77.082 4.276L70.896 14.99l10.701 6.179 6.186-10.715-10.7-6.178zM61.125 0H48.768v12.373h12.357V0zM32.825 4.281L22.124 10.46l6.186 10.714 10.701-6.178-6.186-10.715zM10.449 22.127L4.27 32.828l10.714 6.186 6.178-10.7-10.714-6.187zM12.373 48.77H0v12.356h12.373V48.77zM14.99 70.881L4.274 77.067l6.178 10.701 10.715-6.186-6.179-10.7zM28.311 88.746L22.125 99.46l10.701 6.179 6.186-10.715-10.7-6.178z",fill:"currentColor"}))}var p5=null;function f5(e){return React94.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React94.createElement("path",{d:"M100 38.086V0H61.914v9.93h21.132L54.963 38.013V16.88h-9.93v21.132L16.951 9.93h21.135V0H0v38.086h9.93V16.951l28.083 28.082H16.88v9.93h21.132L9.93 83.046V61.914H0V100h38.086v-9.93H16.951l28.082-28.086v21.135h9.93V61.984L83.046 90.07H61.914V100H100V61.914h-9.93v21.132L61.987 54.963H83.12v-9.93H61.987L90.07 16.951v21.135H100z",fill:"currentColor"}))}var b5=null;function C5(e){return React95.createElement("svg",i({viewBox:"0 0 100 100",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React95.createElement("path",{d:"M0 0v100h100V0H0zm90 90H61.91l20.87-12.52L90 89.52V90zm0-71.25H29.01L90 26.56v8.82l-42.3-5.42L90 42.3v9.12l-27.61-8.05L90 56.78v9.73l-15.29-7.42L90 71.34v11.22L76.02 71.35 61.06 90H49.84l24.82-30.94-8.62-4.19L48.98 90h-9.73l22.71-46.76-9.21-2.68L38.34 90h-9.12l17.53-60.15-10.48-1.35L28.4 90h-8.82l9.12-71.25h-9.94V90H10V10h80v8.75z",fill:"currentColor"}))}var w5=null;function E5(e){return React96.createElement("svg",i({viewBox:"0 0 134 134",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React96.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M67.59 60.288V0h-1.175v60.292L55.941.914l-1.157.204 10.474 59.374L44.636 3.841l-1.104.401 20.622 56.651L34.01 8.681l-1.017.588 30.144 52.213-38.752-46.184-.9.755 38.753 46.185-46.185-38.752-.755.9 46.184 38.752L9.27 32.993 8.68 34.01l52.212 30.144-56.65-20.622-.403 1.104 56.652 20.622L1.118 54.785l-.204 1.157 59.377 10.473H0v1.175h60.288L.914 78.058l.204 1.157 59.374-10.468L3.84 89.364l.402 1.104 56.651-20.617L8.681 99.99l.588 1.017 52.213-30.14-46.184 38.747.755.9 46.186-38.747-38.753 46.18.9.755 38.751-46.178-30.144 52.207 1.017.588 30.144-52.207-20.622 56.645 1.104.402 20.622-56.646-10.473 59.369 1.156.204 10.474-59.373V134h1.175V73.717l10.468 59.369 1.157-.204-10.468-59.37 20.617 56.647 1.104-.401-20.617-56.646 30.139 52.206 1.017-.587-30.14-52.208 38.747 46.179.9-.755-38.747-46.18 46.18 38.747.755-.9-46.179-38.746 52.208 30.139.588-1.017L73.112 69.85l56.646 20.617.401-1.104-56.646-20.617 59.369 10.468.204-1.157-59.37-10.468H134v-1.175H73.714l59.372-10.474-.204-1.156-59.369 10.473 56.646-20.622-.401-1.104-56.646 20.622 52.207-30.144-.588-1.017-52.208 30.144 46.179-38.752-.755-.9-46.18 38.753 38.747-46.185-.9-.755-38.746 46.184L101.007 9.27 99.99 8.68 69.85 60.893l20.617-56.65-1.104-.402-20.617 56.651L79.215 1.118 78.058.914 67.59 60.288z",fill:"currentColor"}))}var y5=null;function z5(e){return React97.createElement("svg",i({viewBox:"0 0 100 101",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React97.createElement("path",{d:"M66.667.929a33.333 33.333 0 010 66.666V.93zM0 34.263a33.333 33.333 0 0166.667 0H0zM33.333 100.929a33.338 33.338 0 01-23.57-9.763 33.333 33.333 0 0123.57-56.903v66.666z",fill:"currentColor"}),React97.createElement("path",{d:"M99.999 67.596a33.332 33.332 0 01-64.13 12.756 33.332 33.332 0 01-2.537-12.756h66.667zM33.334.93H.001v33.333h33.333z",fill:"currentColor"}),React97.createElement("path",{fill:"currentColor",d:"M100 67.595H66.667v33.333H100z"}))}var x5=null;function $5(e){return React98.createElement("svg",i({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React98.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M96 0H0v96h96V0zM84 12H12v72h72V12z",fill:"currentColor"}),React98.createElement("path",{fill:"currentColor",d:"M19.2 19.2h57.6v12H19.2zM19.2 38.4h57.6v12H19.2zM19.2 57.6h31.2v12H19.2z"}))}var M5=null;function k5(e){return React99.createElement("svg",i({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React99.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 67.2V96h96V0H67.2v67.2H0z",fill:"currentColor"}),React99.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 28.8V60h28.8V28.8H60V0H0v28.8z",fill:"currentColor"}))}var L5=null;function R5(e){return React100.createElement("svg",i({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React100.createElement("path",{d:"M22.8 12c5.965 0 10.8 4.835 10.8 10.8 0 .254-.008.505-.026.754C38.542 16.58 46.912 12 56.4 12 71.643 12 84 23.82 84 38.4c0 14.58-12.357 26.4-27.6 26.4-5.744 0-11.078-1.678-15.496-4.55A15.527 15.527 0 0143.2 68.4c0 8.616-6.984 15.6-15.6 15.6C18.985 84 12 77.016 12 68.4s6.985-15.6 15.6-15.6c2.444 0 4.757.562 6.816 1.564C30.892 49.93 28.8 44.399 28.8 38.4c0-2.6.393-5.11 1.125-7.483A10.76 10.76 0 0122.8 33.6c-5.964 0-10.8-4.835-10.8-10.8C12 16.835 16.836 12 22.8 12z",fill:"currentColor"}),React100.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 0h96v96H0V0zm12 12v72h72V12H12z",fill:"currentColor"}))}var _5=null;function H5(e){return React101.createElement("svg",i({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React101.createElement("path",{d:"M96 0H0v96h96V0zM84 12v72H12V12h72z",fill:"currentColor"}),React101.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M85.023 48.341L48.341 11.66 11.66 48.341 48.34 85.023l36.682-36.682zm-56.69 0L48.34 28.333 28.333 48.34zm20.842 19.175L68.35 48.34 49.175 29.167v38.349z",fill:"currentColor"}))}var S5=null;function I5(e){return React102.createElement("svg",i({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React102.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 0h96v28.704H47.844V12L12 48l35.844 36V67.305H96V96H0V0z",fill:"currentColor"}))}var B5=null;function O5(e){return React103.createElement("svg",i({viewBox:"0 0 96 96",fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),React103.createElement("circle",{cx:15.84,cy:15.84,r:11.04,stroke:"currentColor",strokeWidth:9.6}),React103.createElement("path",{d:"M59.52 15.84c0 5.963-5.022 11.04-11.52 11.04-6.498 0-11.52-5.077-11.52-11.04C36.48 9.877 41.502 4.8 48 4.8c6.498 0 11.52 5.077 11.52 11.04z",stroke:"currentColor",strokeWidth:9.6}),React103.createElement("circle",{cx:80.16,cy:15.84,r:15.84,fill:"currentColor"}),React103.createElement("path",{d:"M26.88 48c0 6.498-5.077 11.52-11.04 11.52C9.877 59.52 4.8 54.498 4.8 48c0-6.498 5.077-11.52 11.04-11.52 5.963 0 11.04 5.022 11.04 11.52z",stroke:"currentColor",strokeWidth:9.6}),React103.createElement("circle",{cx:48,cy:48,r:11.52,stroke:"currentColor",strokeWidth:9.6}),React103.createElement("path",{d:"M91.2 48c0 6.498-5.077 11.52-11.04 11.52-5.963 0-11.04-5.022-11.04-11.52 0-6.498 5.077-11.52 11.04-11.52 5.963 0 11.04 5.022 11.04 11.52z",stroke:"currentColor",strokeWidth:9.6}),React103.createElement("circle",{cx:15.84,cy:80.16,r:11.04,stroke:"currentColor",strokeWidth:9.6}),React103.createElement("path",{d:"M59.52 80.16c0 5.963-5.022 11.04-11.52 11.04-6.498 0-11.52-5.077-11.52-11.04 0-5.963 5.022-11.04 11.52-11.04 6.498 0 11.52 5.077 11.52 11.04z",stroke:"currentColor",strokeWidth:9.6}),React103.createElement("circle",{cx:80.16,cy:80.16,r:11.04,stroke:"currentColor",strokeWidth:9.6}))}var D5=null},355936:(me,A,g)=>{g.d(A,{zt:()=>z.Z,I0:()=>n.I,v9:()=>h.v9});var z=g(326890),R=g(345966),K=g(873530),n=g(248679),h=g(971137),de=g(490303),D=g(987045),fe=g(464332)},248679:(me,A,g)=>{g.d(A,{I:()=>n});var z=g(873530),R=g(490303);function K(h=z.E){const de=h===z.E?R.o:(0,R.f)(h);return function(){return de().dispatch}}const n=K()},490303:(me,A,g)=>{g.d(A,{f:()=>K,o:()=>n});var z=g(873530),R=g(359784);function K(h=z.E){const de=h===z.E?R.x:(0,R.o)(h);return function(){const{store:fe}=de();return fe}}const n=K()},443934:(me,A,g)=>{g.d(A,{zt:()=>D.zt,I0:()=>D.I0,v9:()=>D.v9});var z=g(659207),R=g(760425),K=g(116629),n=g(587664),h=g(971137),de=g(345966),D=g(355936);(0,h.Fu)(R.useSyncExternalStoreWithSelector),(0,de.v)(z.useSyncExternalStore),(0,n.F)(K.m)},323055:(me,A,g)=>{g.d(A,{P1:()=>He});var z="NOT_FOUND";function R(W){var M;return{get:function(F){return M&&W(M.key,F)?M.value:z},put:function(F,ge){M={key:F,value:ge}},getEntries:function(){return M?[M]:[]},clear:function(){M=void 0}}}function K(W,M){var S=[];function F(T){var k=S.findIndex(function(H){return M(T,H.key)});if(k>-1){var _=S[k];return k>0&&(S.splice(k,1),S.unshift(_)),_.value}return z}function ge(T,k){F(T)===z&&(S.unshift({key:T,value:k}),S.length>W&&S.pop())}function oe(){return S}function be(){S=[]}return{get:F,put:ge,getEntries:oe,clear:be}}var n=function(M,S){return M===S};function h(W){return function(S,F){if(S===null||F===null||S.length!==F.length)return!1;for(var ge=S.length,oe=0;oe<ge;oe++)if(!W(S[oe],F[oe]))return!1;return!0}}function de(W,M){var S=typeof M=="object"?M:{equalityCheck:M},F=S.equalityCheck,ge=F===void 0?n:F,oe=S.maxSize,be=oe===void 0?1:oe,T=S.resultEqualityCheck,k=h(ge),_=be===1?R(k):K(be,k);function H(){var V=_.get(arguments);if(V===z){if(V=W.apply(null,arguments),T){var j=_.getEntries(),J=j.find(function(Ce){return T(Ce.value,V)});J&&(V=J.value)}_.put(arguments,V)}return V}return H.clearCache=function(){return _.clear()},H}function D(W){var M=Array.isArray(W[0])?W[0]:W;if(!M.every(function(F){return typeof F=="function"})){var S=M.map(function(F){return typeof F=="function"?"function "+(F.name||"unnamed")+"()":typeof F}).join(", ");throw new Error("createSelector expects all input-selectors to be functions, but received the following types: ["+S+"]")}return M}function fe(W){for(var M=arguments.length,S=new Array(M>1?M-1:0),F=1;F<M;F++)S[F-1]=arguments[F];var ge=function(){for(var be=arguments.length,T=new Array(be),k=0;k<be;k++)T[k]=arguments[k];var _=0,H,V={memoizeOptions:void 0},j=T.pop();if(typeof j=="object"&&(V=j,j=T.pop()),typeof j!="function")throw new Error("createSelector expects an output function after the inputs, but received: ["+typeof j+"]");var J=V,Ce=J.memoizeOptions,Te=Ce===void 0?S:Ce,Je=Array.isArray(Te)?Te:[Te],i=D(T),L=W.apply(void 0,[function(){return _++,j.apply(null,arguments)}].concat(Je)),E=W(function(){for(var ot=[],Qt=i.length,vt=0;vt<Qt;vt++)ot.push(i[vt].apply(null,arguments));return H=L.apply(null,ot),H});return Object.assign(E,{resultFunc:j,memoizedResultFunc:L,dependencies:i,lastResult:function(){return H},recomputations:function(){return _},resetRecomputations:function(){return _=0}}),E};return ge}var He=fe(de),ve=function(M,S){if(S===void 0&&(S=He),typeof M!="object")throw new Error("createStructuredSelector expects first argument to be an object "+("where each property is a selector, instead received a "+typeof M));var F=Object.keys(M),ge=S(F.map(function(oe){return M[oe]}),function(){for(var oe=arguments.length,be=new Array(oe),T=0;T<oe;T++)be[T]=arguments[T];return be.reduce(function(k,_,H){return k[F[H]]=_,k},{})});return ge}}}]);

//# sourceMappingURL=6733.js.map