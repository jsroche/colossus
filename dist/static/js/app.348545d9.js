(function(e){function t(t){for(var i,o,l=t[0],s=t[1],c=t[2],u=0,d=[];u<l.length;u++)o=l[u],r[o]&&d.push(r[o][0]),r[o]=0;for(i in s)Object.prototype.hasOwnProperty.call(s,i)&&(e[i]=s[i]);p&&p(t);while(d.length)d.shift()();return a.push.apply(a,c||[]),n()}function n(){for(var e,t=0;t<a.length;t++){for(var n=a[t],i=!0,o=1;o<n.length;o++){var l=n[o];0!==r[l]&&(i=!1)}i&&(a.splice(t--,1),e=s(s.s=n[0]))}return e}var i={},o={app:0},r={app:0},a=[];function l(e){return s.p+"static/js/"+({}[e]||e)+"."+{"chunk-169ccd73":"005bf56e","chunk-2d0a2d59":"65c8a722","chunk-2d0bff12":"40bbffcd","chunk-2d0e6293":"8783b42d"}[e]+".js"}function s(t){if(i[t])return i[t].exports;var n=i[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,s),n.l=!0,n.exports}s.e=function(e){var t=[],n={"chunk-169ccd73":1};o[e]?t.push(o[e]):0!==o[e]&&n[e]&&t.push(o[e]=new Promise(function(t,n){for(var i="static/css/"+({}[e]||e)+"."+{"chunk-169ccd73":"e3b7e20a","chunk-2d0a2d59":"31d6cfe0","chunk-2d0bff12":"31d6cfe0","chunk-2d0e6293":"31d6cfe0"}[e]+".css",r=s.p+i,a=document.getElementsByTagName("link"),l=0;l<a.length;l++){var c=a[l],u=c.getAttribute("data-href")||c.getAttribute("href");if("stylesheet"===c.rel&&(u===i||u===r))return t()}var d=document.getElementsByTagName("style");for(l=0;l<d.length;l++){c=d[l],u=c.getAttribute("data-href");if(u===i||u===r)return t()}var p=document.createElement("link");p.rel="stylesheet",p.type="text/css",p.onload=t,p.onerror=function(t){var i=t&&t.target&&t.target.src||r,a=new Error("Loading CSS chunk "+e+" failed.\n("+i+")");a.code="CSS_CHUNK_LOAD_FAILED",a.request=i,delete o[e],p.parentNode.removeChild(p),n(a)},p.href=r;var _=document.getElementsByTagName("head")[0];_.appendChild(p)}).then(function(){o[e]=0}));var i=r[e];if(0!==i)if(i)t.push(i[2]);else{var a=new Promise(function(t,n){i=r[e]=[t,n]});t.push(i[2]=a);var c,u=document.createElement("script");u.charset="utf-8",u.timeout=120,s.nc&&u.setAttribute("nonce",s.nc),u.src=l(e),c=function(t){u.onerror=u.onload=null,clearTimeout(d);var n=r[e];if(0!==n){if(n){var i=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src,a=new Error("Loading chunk "+e+" failed.\n("+i+": "+o+")");a.type=i,a.request=o,n[1](a)}r[e]=void 0}};var d=setTimeout(function(){c({type:"timeout",target:u})},12e4);u.onerror=u.onload=c,document.head.appendChild(u)}return Promise.all(t)},s.m=e,s.c=i,s.d=function(e,t,n){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(s.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var i in e)s.d(n,i,function(t){return e[t]}.bind(null,i));return n},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/",s.oe=function(e){throw console.error(e),e};var c=window["webpackJsonp"]=window["webpackJsonp"]||[],u=c.push.bind(c);c.push=t,c=c.slice();for(var d=0;d<c.length;d++)t(c[d]);var p=u;a.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("56d7")},"1f7a":function(e,t,n){},"2a68":function(e,t,n){"use strict";n.d(t,"a",function(){return i}),n.d(t,"f",function(){return o}),n.d(t,"e",function(){return r}),n.d(t,"c",function(){return a}),n.d(t,"d",function(){return l}),n.d(t,"b",function(){return s});n("a481"),n("c5f6"),n("7cdf"),n("6762"),n("2fdb"),n("456d"),n("ac6a"),n("28a5");var i="http://colossus-test.canadacentral.cloudapp.azure.com:8000/api/";function o(e){var t=e.split("_");return t.forEach(function(e,n){t[n]=e.charAt(0).toUpperCase()+e.slice(1)}),t.join(" ")}function r(e){return e||"None"}function a(e,t){return this.$store.getters.getModelTitle(e,t)}function l(e){console.log("1"),Object.keys(e.fields).forEach(function(t){e.fields[t].default?e.fields[t].value=e.fields[t].default:e.fields[t].value=""}),console.log("2"),"children"in e&&(console.log("2-1"),Object.keys(e.children).forEach(function(t){console.log("2-2"),e.children[t].default?e.children[t].value=e.children[t].default:e.children[t].value=""})),console.log("3"),"relations"in e&&Object.keys(e.relations).forEach(function(t){Object.keys(e.relations).forEach(function(t){e.relations[t].default?e.relations[t].value=[e.relations[t].default]:e.relations[t].value=[]})})}function s(e,t){console.log("DETAIL FORM"),console.log(t),console.log(e),console.log("1"),t.fields=Object.assign({id:{type:"Id",value:e.id}},t.fields),console.log("2"),Object.keys(t.fields).forEach(function(n){e[n]?("Date"===t.fields[n].type&&(t.fields[n].value=c(e[n])),"Select"===t.fields[n].type?t.fields[n].value=t.fields[n].choices[e[n]]:t.fields[n].value=e[n]):t.fields[n].value=""}),console.log("3"),"children"in t&&Object.keys(t.children).forEach(function(n){console.log("3-1"),t.children[n].fields=Object.assign({id:{type:"Id",value:null}},t.children[n].fields),Object.keys(e[n]).forEach(function(i){console.log("3-2"),Object.keys(t.children[n].fields).includes(i)&&("Date"===t.children[n].fields[i].type?t.children[n].fields[i].value=c(e[n][i]):"Select"===t.children[n].fields[i].type?t.children[n].fields[i].value=t.children[n].fields[i].choices[e[n][i]]:t.children[n].fields[i].value=e[n][i])})}),console.log("4"),console.log("RELATION"),"relations"in t&&(Object.keys(t.relations).forEach(function(n){console.log(n),t.relations[n].selected=[],Object.keys(e).includes(n)&&(t.relations[n].many?Number.isInteger(e[n][0])?t.relations[n].selected=e[n]:e[n].forEach(function(e){t.relations[n].selected=[e.id]}):t.relations[n].selected.push(e[n].id))}),console.log("5"),console.log("SCHOOLINGS"),"schoolings"in t&&(console.log("SHCOLLSIN"),Object.keys(t.schoolings).forEach(function(n){console.log(n),console.log(t.schoolings[n]),console.log(e[n]),null!=e[n]||void 0!=e[n]?(console.log("FEFE"),t.schoolings[n].value=e[n]):t.schoolings[n].value=t.schoolings.many?[]:"",console.log(t.schoolings[n])}))),console.log("FORM READY"),console.log(t)}function c(e){return/^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$/.test(e)?new Date(e.replace("-"," ")).toISOString().substr(0,10):e}},"56d7":function(e,t,n){"use strict";n.r(t);n("cadf"),n("551c"),n("f751"),n("097d");var i=n("2b0e"),o=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-app",[n("v-app-bar",{attrs:{app:"","clipped-left":"",color:e.colour,dense:""}},[e.authorized?n("v-app-bar-nav-icon",{on:{click:function(t){t.stopPropagation(),e.drawer=!e.drawer}}}):e._e(),n("v-toolbar-title",{staticClass:"mr-12 align-center"},[n("span",{staticClass:"title"},[e._v("Kudu - Colossus BETA"+e._s(e.colour))])]),n("v-spacer"),n("v-layout",{staticStyle:{"max-width":"650px"},attrs:{"align-center":""}},[e.authorized?n("v-text-field",{attrs:{"append-icon-cb":function(){},placeholder:"Search feature is not there yet...","single-line":"","append-icon":"search",color:"white","hide-details":""},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.searchQuery(t)}},model:{value:e.query,callback:function(t){e.query=t},expression:"query"}}):e._e()],1)],1),n("v-navigation-drawer",{attrs:{app:"",clipped:""},model:{value:e.drawer,callback:function(t){e.drawer=t},expression:"drawer"}},[n("SideMenu")],1),n("v-content",[n("v-container",{attrs:{fluid:"","fill-height":""}},[n("v-layout",{attrs:{"child-flex":""}},[n("v-flex",[n("router-view",{key:e.$route.fullPath,staticClass:"router-component"})],1)],1)],1)],1)],1)},r=[],a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("v-list",{attrs:{dense:""}},[n("v-list-item",[n("v-list-item-content",[n("v-list-item-title",{staticClass:"title"},[e._v("\n           Kudu-Colossus\n         ")]),n("v-list-item-subtitle",[e._v("\n           Welcome, Simong\n         ")])],1)],1),n("v-divider"),n("v-list-item",{on:{click:function(t){return e.$router.push("/")}}},[n("v-list-item-action",[n("v-icon",[e._v("mdi-pine-tree")])],1),n("v-list-item-title",[e._v("Home")])],1),n("v-list-item",{on:{click:function(t){t.stopPropagation(),e.picker=!0}}},[n("v-list-item-action",[n("v-icon",[e._v("mdi-palette")])],1),n("v-list-item-title",[e._v("Colour")]),n("ColourPicker",{attrs:{picker:e.picker,pickerClose:e.pickerClose}})],1),n("v-list-item",{attrs:{disabled:""},on:{click:function(e){}}},[n("v-list-item-action",[n("v-icon",[e._v("mdi-account")])],1),n("v-list-item-title",[e._v("Account(NOTHIGN ATM)")])],1),n("v-list-item",{on:{click:e.toAPI}},[n("v-list-item-action",[n("v-icon",[e._v("mdi-format-list-bulleted")])],1),n("v-list-item-title",[e._v("API")])],1),n("v-list-item",{attrs:{disabled:""},on:{click:function(e){}}},[n("v-list-item-action",[n("v-icon",[e._v("mdi-account-key")])],1),n("v-list-item-title",[e._v("Admin(NOTHIGN ATM)")])],1),n("v-subheader",{staticClass:"mt-4 grey--text text--darken-1"},[e._v("FOLDERS")]),e._l(e.getStructure,function(t,i){return n("v-list-group",{key:i,attrs:{"prepend-icon":"mdi-folder","no-action":""},scopedSlots:e._u([{key:"activator",fn:function(){return[n("v-list-item-content",[n("v-list-item-title",{domProps:{textContent:e._s(i)}})],1)]},proxy:!0}],null,!0),model:{value:t.active,callback:function(n){e.$set(t,"active",n)},expression:"value.active"}},e._l(t,function(t,i){return n("v-list-item",{key:i,on:{click:function(n){return e.$router.push(t.link)}}},[n("v-list-item-action",[n("v-icon",[e._v(e._s(t.icon))])],1),n("v-list-item-content",[n("v-list-item-title",{domProps:{textContent:e._s(t.text)}})],1)],1)}),1)}),n("v-subheader",{staticClass:"mt-4 grey--text text--darken-1"},[e._v("KUDU")]),n("v-list-item",{staticClass:"mt-4",attrs:{disabled:""},on:{click:function(e){}}},[n("v-list-item-action",[n("v-icon",{attrs:{color:"grey darken-1"}},[e._v("mdi-help-box")])],1),n("v-list-item-title",{staticClass:"grey--text text--darken-1"},[e._v("About(NOTHING ATM)")])],1),n("v-list-item",{attrs:{disabled:""},on:{click:function(e){}}},[n("v-list-item-action",[n("v-icon",{attrs:{color:"grey darken-1"}},[e._v("settings")])],1),n("v-list-item-title",{staticClass:"grey--text text--darken-1"},[e._v("Settings(NOTHING ATM)")])],1),n("v-list-item",{on:{click:function(t){return e.$store.commit("LOGOUT")}}},[n("v-list-item-action",[n("v-icon",{attrs:{color:"grey darken-1"}},[e._v("mdi-logout")])],1),n("v-list-item-title",{staticClass:"grey--text text--darken-1"},[e._v("Logout(I ACTUALLY WORK)")])],1)],2)],1)},l=[],s=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-dialog",{attrs:{persistent:"",width:"345"},model:{value:e.picker,callback:function(t){e.picker=t},expression:"picker"}},[n("v-card",[n("v-card-title",[n("span",{staticClass:"headline"},[e._v("Go crazy!"+e._s(e.colour))])]),n("v-card-text",[n("v-color-picker",{attrs:{showSwatches:"",flat:""},model:{value:e.colour,callback:function(t){e.colour=t},expression:"colour"}})],1),n("v-card-actions",[n("v-spacer"),n("v-btn",{attrs:{color:"green darken-1",text:""},on:{click:e.pickerClose}},[e._v("cancel")]),n("v-btn",{attrs:{color:"green darken-1",text:""},on:{click:e.pickColour}},[e._v("Agree")])],1)],1)],1)},c=[],u={name:"colourPicker",props:["picker","pickerClose"],beforeDestroy:function(){this.picker=!1},data:function(){return{colour:"#FF0000"}},methods:{pickColour:function(){this.$store.commit("UPDATE_COLOUR",this.colour),console.log(this.$store.getters.colourGetter),this.pickerClose()}}},d=u,p=n("2877"),_=n("6544"),m=n.n(_),y=n("8336"),f=n("b0af"),g=n("99d9"),S=n("03a4"),h=n("169a"),A=n("2fa4"),v=Object(p["a"])(d,s,c,!1,null,null,null),I=v.exports;m()(v,{VBtn:y["a"],VCard:f["a"],VCardActions:g["a"],VCardText:g["b"],VCardTitle:g["c"],VColorPicker:S["a"],VDialog:h["a"],VSpacer:A["a"]});var b=n("2a68"),G={components:{ColourPicker:I},methods:{getRouterPath:function(e){return"/list/"+e},toAPI:function(){window.location.href=b["a"]},pickerClose:function(){this.picker=!1}},data:function(){return{picker:!1}},computed:{getStructure:function(){return this.$store.getters.getStructurekeys}}},k=G,x=n("ce7e"),C=n("132d"),E=n("8860"),T=n("56b0"),w=n("da13"),D=n("1800"),O=n("5d23"),L=n("e0c7"),q=Object(p["a"])(k,a,l,!1,null,null,null),P=q.exports;m()(q,{VDivider:x["a"],VIcon:C["a"],VList:E["a"],VListGroup:T["a"],VListItem:w["a"],VListItemAction:D["a"],VListItemContent:O["a"],VListItemSubtitle:O["b"],VListItemTitle:O["c"],VSubheader:L["a"]});var V={props:{source:String},components:{SideMenu:P},data:function(){return{drawer:!1,query:""}},created:function(){this.$vuetify.theme.dark=!0;var e=!!localStorage.getItem("user-token");e?this.$store.commit("UPDATE_AUTH_STATUS",!0):this.$store.commit("UPDATE_AUTH_STATUS",!1)},computed:{authorized:function(){var e=this.$store.state.account.authenticated;return this.drawer=!1,e},colour:function(){return this.$store.getters.colourGetter}},methods:{searchQuery:function(){this.query&&this.$router.push({name:"search",params:{query:this.query}})}},mounted:function(){this.authorized=!!localStorage.getItem("user-token"),console.log("authorized: ".concat(this.authorized))}},N=V,R=n("7496"),H=n("40dc"),j=n("5bc1"),B=n("a523"),F=n("a75b"),U=n("0e8f"),M=n("a722"),$=n("f774"),z=n("8654"),J=n("2a7f"),W=Object(p["a"])(N,o,r,!1,null,null,null),X=W.exports;m()(W,{VApp:R["a"],VAppBar:H["a"],VAppBarNavIcon:j["a"],VContainer:B["a"],VContent:F["a"],VFlex:U["a"],VLayout:M["a"],VNavigationDrawer:$["a"],VSpacer:A["a"],VTextField:z["a"],VToolbarTitle:J["a"]});var K=n("2f62"),Q=n("bc3a"),Y=n.n(Q),Z=n("a7fe"),ee=n.n(Z),te={sample_type:{P:"Patient",X:"Xenograft",Or:"Organid",C:"Cell Line",O:"Other"},tissue_state:{NONE:"None",FROZ:"Frozen",FRES:"Fresh","DIG-FRES":"Digested-Fresh"},tissue_type:{N:"Normal",B:"Benign",PM:"Pre-malignant",M:"Malignant",NNP:"Non-neoplastic Disease",U:"Undetermined",HP:"Hyperplasia",MP:"Metaplasia",DP:"Dysplasia"},input_type:{DLP:"DLP",PBAL:"PBAL",TENX:"TenX"},aligner:{A:"bwa-aln",M:"bwa-mem"},smoothing:{M:"modal",L:"loess"},montage_status:{Success:"Success",Error:"Error",Ignore:"Ignore",Pending:"Pending"},priority_level:{L:"Low",M:"Medium",H:"High"},verified:{T:"True",F:"False"},run_status:{IDLE:"Idle",ERROR:"Error",RUNNING:"Running",ARCHIVING:"Archiving",COMPLETE:"Complete",ALIGN_COMPLETE:"Align Complete",HMMCOPY_COMPLETE:"Hmmcopy Complete"},pathology_occurrence:{PR:"Primary",RC:"Recurrent or Relapse",ME:"Metastatic",RM:"Remission",UN:"Undetermined",US:"Unspecified"},treatment_status:{PR:"Pre-treatment",IN:"In-treatment",PO:"Post-treatment",NA:"N/A",UN:"unkown"},chip_format:{W:"Wafergen",M:"Microfluidic",B:"Bulk",O:"Other"},spotting_location:{AD:"Aparicio Lab - Deckard",AR:"Aparicio Lab - Rachael",H:"Hansen Lab",G:"GSC"},cell_state:{C:"Cells",N:"Nuclei",M:"Mixed",U:"Unknown"},qc_check:{P:"Will sequence",N:"Will not sequence"},rev_comp_override:{"i7,i5":"No Reverse Complement","i7,rev(i5)":"Reverse Complement i5","rev(i7),i5":"Reverse Complement i7","rev(i7),rev(i5)":"Reverse Complement i7 and i5"},read_type:{P:"PET",S:"SET"},sequencing_instrument:{"i7,i5":"No Reverse Complement","i7,rev(i5)":"Reverse Complement i5","rev(i7),i5":"Reverse Complement i7","rev(i7),rev(i5)":"Reverse Complement i7 and i5"},sequencing_output_mode:{L:"Low",M:"Medium",H:"High"},sequencing_center:{BCCAGSC:"BCCAGSC",UBCBRC:"UBCBRC"},lab_name:{SA:"Sam Aparicio",DH:"David Huntsman"},library_type:{"5'":"5'","3'":"3'","V(D)J":"V(D)J",CNV:"CNV"},chemistry_version:{VERSION_2:"v2",VERSION_3:"v3"},index_used:{SI_GA_A1:"SI-GA_A1",SI_GA_A2:"SI-GA-A2",SI_GA_A3:"SI-GA-A3",SI_GA_A4:"SI-GA-A4",SI_GA_A5:"SI-GA-A5",SI_GA_A6:"SI-GA-A6",SI_GA_A7:"SI-GA-A7",SI_GA_A8:"SI-GA-A8",SI_GA_A9:"S:I-GA-A9",SI_GA_A10:"SI-GA-A10",SI_GA_A11:"SI-GA-A11",SI_GA_A12:"SI-GA-A12",SI_GA_B1:"SI-GA-B1",SI_GA_B2:"SI-GA-B2",SI_GA_B3:"SI-GA-B3",SI_GA_B4:"SI-GA-B4",SI_GA_B5:"SI-GA-B5",SI_GA_B6:"SI-GA-B6",SI_GA_B7:"SI-GA-B7",SI_GA_B8:"SI-GA-B8",SI_GA_B9:"SI-GA-B9",SI_GA_B10:"SI-GA-B10",SI_GA_B11:"SI-GA-B11",SI_GA_B12:"SI-GA-B12",SI_GA_C1:"SI-GA-C1",SI_GA_C2:"SI-GA-C2",SI_GA_C3:"SI-GA-C3",SI_GA_C4:"SI-GA-C4",SI_GA_C5:"SI-GA-C5",SI_GA_C6:"SI-GA-C6",SI_GA_C7:"SI-GA-C7",SI_GA_C8:"SI-GA-C8",SI_GA_C9:"SI-GA-C9",SI_GA_C10:"SI-GA-C10",SI_GA_C11:"SI-GA-C11",SI_GA_C12:"SI-GA-C12",SI_GA_D1:"SI-GA-D1",SI_GA_D2:"SI-GA-D2",SI_GA_D3:"SI-GA-D3",SI_GA_D4:"SI-GA-D4",SI_GA_D5:"SI-GA-D5",SI_GA_D6:"SI-GA-D6",SI_GA_D7:"SI-GA-D7",SI_GA_D8:"SI-GA-D8",SI_GA_D9:"SI-GA-D9",SI_GA_D10:"SI-GA-D10",SI_GA_D11:"SI-GA-D11",SI_GA_D12:"SI-GA-D12",SI_GA_E1:"SI-GA-E1",SI_GA_E2:"SI-GA-E2",SI_GA_E3:"SI-GA-E3",SI_GA_E4:"SI-GA-E4",SI_GA_E5:"SI-GA-E5",SI_GA_E6:"SI-GA-E6",SI_GA_E7:"SI-GA-E7",SI_GA_E8:"SI-GA-E8",SI_GA_E9:"SI-GA-E9",SI_GA_E10:"SI-GA-E10",SI_GA_E11:"SI-GA-E11",SI_GA_E12:"SI-GA-E12",SI_GA_F1:"SI-GA-F1",SI_GA_F2:"SI-GA-F2",SI_GA_F3:"SI-GA-F3",SI_GA_F4:"SI-GA-F4",SI_GA_F5:"SI-GA-F5",SI_GA_F6:"SI-GA-F6",SI_GA_F7:"SI-GA-F7",SI_GA_F8:"SI-GA-F8",SI_GA_F9:"SI-GA-F9",SI_GA_F10:"SI-GA-F10",SI_GA_F11:"SI-GA-F11",SI_GA_F12:"SI-GA-F12",SI_GA_G1:"SI-GA-G1",SI_GA_G2:":SI-GA-G2",SI_GA_G3:"SI-GA-G3",SI_GA_G4:"SI-GA-G4",SI_GA_G5:":SI-GA-G5",SI_GA_G6:"SI-GA-G6",SI_GA_G7:"SI-GA-G7",SI_GA_G8:"SI-GA-G8",SI_GA_G9:"SI-GA-G9",SI_GA_G10:"SI-GA-G10",SI_GA_G11:"SI-GA-G11",SI_GA_G12:"SI-GA-G12",SI_GA_H1:"SI-GA-H1",SI_GA_H2:"SI-GA-H2",SI_GA_H3:"SI-GA-H3",SI_GA_H4:"SI-GA-H4",SI_GA_H5:"SI-GA:-H5",SI_GA_H6:"SI-GA-H6",SI_GA_H7:"SI-GA-H7",SI_GA_H8:"SI-GA-H8",SI_GA_H9:"SI-GA-H9",SI_GA_H10:"SI-GA-H10",SI_GA_H11:"SI-GA-H11",SI_GA_H12:"SI-GA-H12"}},ne={project:{fields:{name:{type:"String"},description:{type:"String"}},relations:{dlplibrary_set:{model:["dlp","library"],name:"pool_id",many:!0},tenxlibrary_set:{model:["tenx","library"],name:"name",many:!0}}},sample:{fields:{sample_id:{type:"String",must:!0},taxonomy_id:{type:"Integer"},sample_type:{type:"Select",choices:te.sample_type},anonymous_patient_id:{type:"String"},cell_line_id:{type:"String"},xenograft_id:{type:"String"}},relations:{tenxlibrary_set:{model:["tenx","library"],name:"name",many:!0},dlplibrary_set:{model:["dlp","library"],name:"pool_id",many:!0}},children:{additionalsampleinformation:{title:"Additional Sample Information",fields:{tissue_state:{type:"Select",choices:te.tissue_state},cancer_type:{type:"String"},cancer_subtype:{type:"String"},disease_condition:{type:"String"},sex:{type:"String"},patient_biopsy_date:{type:"Date"},anatomic_site:{type:"String"},anatomic_sub_site:{type:"String"},developmental_stage:{type:"String"},tissue_type:{type:"Select",choices:te.tissue_type},cell_type:{type:"String"},pathology_disease_name:{type:"String"},additional_pathology_information:{type:"String"},grade:{type:"String"},stage:{type:"String"},tumor_content:{type:"String"},pathology_occurrence:{type:"Select",choices:te.pathology_occurrence},treatment_status:{type:"Select",choices:te.treatment_status},family_information:{type:"String"}}}}},dlpanalysis:{fields:{version:{type:"String"},analysis_jira_ticket:{type:"String"},aligner:{type:"Select",choices:te.aligner},smoothing:{type:"Select",choices:te.smoothing},montage_status:{type:"Select",choices:te.montage_status},priority_level:{type:"Select",choices:te.priority_level},verified:{type:"Select",choices:te.verified}},relations:{library:{model:["dlp","library"],name:"pool_id",many:!1},sequnecings:{model:["dlp","sequencing"],name:"id",many:!0}},children:{analysis_run:{title:"Analysis Run",fields:{run_status:{type:"Select",choices:te.run_status},last_updated:{type:"Date"}}},reference_genome:{title:"Reference Genome",fields:{reference_genome:{type:"String"}}}}},dlplibrary:{fields:{pool_id:{type:"String"},jira_ticket:{type:"String"},description:{type:"String"},result:{type:"String"},title:{type:"String"},quality:{type:"Integer"},exclude_from_analysis:{type:"Bool"},failed:{type:"Bool"}},relations:{projects:{model:["core","project"],name:"name",many:!0},sample:{model:["core","sample"],name:"sample_id",many:!1},dlpsequencing_set:{model:["dlp","sequencing"],name:"id",many:!0}},schoolings:{doubletinformation:{title:"Doublet Information",pivot:!0},metadata:{title:"Metadata",many:!1},sublibraryinformation_set:{title:"Sublibrary",many:!0,api:"kududlpsublibrary_list/"}},children:{dlplibraryconstructioninformation:{title:"DLP Library Construction Information",fields:{chip_format:{type:"Select",choices:te.chip_format},library_construction_method:{type:"String"},library_type:{type:"String"},library_notes:{type:"String"},library_prep_date:{type:"Date"},number_of_pcr_cycles:{type:"Integer"},protocol:{type:"String"},spotting_location:{type:"Select",choices:te.spotting_location}}},dlplibrarysampledetail:{title:"DLP Library Sample Detail",fields:{sample_spot_date:{type:"Date"},spotting_location:{type:"Select",choices:te.spotting_location},cell_state:{type:"Select",choices:te.cell_state},estimated_percent_viability:{type:"Integer"},label_of_original_sample_vial:{type:"String"},lims_vial_barcode:{type:"String"},original_storage_temperature:{type:"Integer"},passage_of_cell_line:{type:"Integer"},sample_notes:{type:"String"},sample_preparation_method:{type:"String"},sample_preservation_method:{type:"String"}}},dlplibraryquantificationandstorage:{title:"DLP Quantification and Storage",fields:{average_size:{type:"Integer"},dna_concentration_nm:{type:"Integer"},dna_concentration_ngul:{type:"Integer"},dna_volume:{type:"String"},freezer:{type:"String"},rack:{type:"Integer"},shelf:{type:"Integer"},box:{type:"Integer"},position_in_box:{type:"Integer"},library_tube_label:{type:"String"},quantification_method:{type:"String"},size_range:{type:"String"},size_selection_method:{type:"String"},storage_medium:{type:"String"},agilent_bioanalyzer_xad:{type:"String"},agilent_bioanalyzer_image:{type:"String"},qc_check:{type:"Select",choices:te.qc_check},qc_notes:{type:"String"}}}}},dlpsequencing:{fields:{rev_comp_override:{type:"Select",choices:te.rev_comp_override},adapter:{type:"String"},format_for_data_submission:{type:"String"},index_read_type:{type:"String"},index_read1_length:{type:"Integer"},index_read2_length:{type:"Integer"},read_type:{type:"Select",choices:te.read_type},read1_length:{type:"Integer"},read2_length:{type:"Integer"},sequencing_instrument:{type:"Select",choices:te.sequencing_instrument},sequencing_output_mode:{type:"Select",choices:te.sequencing_output_mode},short_description_of_submission:{type:"String"},submission_date:{type:"Date"},number_of_lanes_requested:{type:"Integer"},gsc_library_id:{type:"String"},sequencer_id:{type:"String"},sequencing_center:{type:"Select",choices:te.sequencing_center},sequencer_notes:{type:"String"}},schoolings:{dlplane_set:{title:"DLP Lane",many:!0,api:"kududlplane_list/"}},relations:{dlplibrary:{model:["dlp","library"],name:"pool_id",many:!1},relates_to:{model:["dlp","sequencing"],name:"id",many:!0}}},tenxchip:{fields:{name:{type:"String"},lab_name:{type:"Select",choices:te.lab_name}},relations:{tenxlibrary:{model:["tenx","library"],name:"name",many:!0}}},tenxpool:{fields:{pool_name:{type:"String"},gsc_pool_name:{type:"String"},construction_location:{type:"Select",choices:te.sequencing_center},constructed_date:{type:"Date"}},relations:{tenxlibrary_set:{model:["tenx","library"],name:"name",many:!0},tenxsequencing:{model:["tenx","sequencing"],name:"id",many:!0}}},tenxanalysis:{fields:{input_type:{type:"Select",choices:te.input_type},version:{type:"String"},jira_ticket:{type:"String"},run_status:{type:"Select",choices:te.run_status},submission_date:{type:"Date"},description:{type:"String"}},relations:{tenxsequencing_set:{model:["tenx","sequencing"],name:"id",many:!0},tenx_library:{model:["tenx","library"],name:"name",many:!1}}},tenxsequencing:{fields:{sequencing_instrument:{type:"Select",choices:te.sequencing_instrument},sequencing_center:{type:"Select",choices:te.sequencing_center},submission_date:{type:"Date"},sequencer_id:{type:"String"},number_of_lanes_requested:{type:"Integer"}},schoolings:{tenxlane_set:{title:"TenX Lane",many:!0,api:"kudutenxlane_list/"}},relations:{tenxlibrary:{model:["tenx","library"],name:"name",many:!1},tenxpool:{model:["tenx","pool"],name:"pool_name",many:!1}}},tenxlibrary:{fields:{name:{type:"String"},jira_ticket:{type:"String"},description:{type:"String"},result:{type:"String"},num_sublibraries:{type:"String"},experimental_condition:{type:"String"},chip_well:{type:"Integer"},condition:{type:"String"},google_sheet:{type:"String"},failed:{type:"Bool"}},relations:{projects:{model:["core","project"],name:"name",many:!0},tenxchip:{model:["tenx","chip"],name:"name",many:!1},sample:{model:["core","sample"],name:"sample_id",many:!1},tenxpool:{model:["tenx","pool"],name:"pool_name",many:!1},tenxsequencing:{model:["tenx","sequencing"],name:"id",many:!0}},children:{tenxlibraryconstructioninformation:{title:"TenX Library Construction Information",fields:{library_construction_method:{type:"String"},submission_date:{type:"Date"},library_prep_location:{type:"String"},chip_lot_number:{type:"Integer"},reagent_lot_number:{type:"Integer"},library_type:{type:"Select",choices:te.library_type},index_used:{type:"Select",choices:te.index_used},pool:{type:"String"},concentration:{type:"Integer"},chemistry_version:{type:"Select",choices:te.chemistry_version}}},tenxlibrarysampledetail:{title:"TenX Library Sample Detail",fields:{sample_spot_date:{type:"Date"},spotting_location:{type:"Select",choices:te.spotting_location},cell_state:{type:"Select",choices:te.cell_state},estimated_percent_viability:{type:"Integer"},label_of_original_sample_vial:{type:"String"},lims_vial_barcode:{type:"String"},original_storage_temperature:{type:"Integer"},passage_of_cell_line:{type:"Integer"},sample_notes:{type:"String"},sample_preparation_method:{type:"String"},sample_preservation_method:{type:"String"}}},tenxlibraryquantificationandstorage:{title:"TenX Quantification And Storage",fields:{agilent_bioanalyzer_xad:{type:"String"},agilent_bioanalyzer_image:{type:"String"},qc_check:{type:"Select",choices:te.qc_check},qc_notes:{type:"String"}}}}}},ie={core:{sample:{title:"Core Samples",url:"/list/core/sample",list_api:"kudusample_list/",detail_api:"sample/",form_fields:ne.sample},project:{title:"Core Projects",url:"/list/core/project",list_api:"kuduproject_list/",detail_api:"project/",form_fields:ne.project},summary:!1},dlp:{library:{title:"DLP Libraries",url:"/list/dlp/library",list_api:"kududlplibrary_list/",detail_api:"library/",form_fields:ne.dlplibrary},sequencing:{title:"DLP Sequencings",url:"/list/dlp/sequencing",list_api:"kududlpsequencing_list/",detail_api:"sequencing/",form_fields:ne.dlpsequencing},analysis:{title:"DLP Analyses",url:"/list/dlp/analysis",list_api:"kududlpanalysis_list/",detail_api:"analysis_information/",form_fields:ne.dlpanalysis,noteditable:!0},summary:!0},tenx:{chip:{title:"Tenx Chips",url:"/list/tenx/chip",list_api:"kudutenxchip_list/",detail_api:"tenxchip/",form_fields:ne.tenxchip},pool:{title:"Tenx Pools",url:"/list/tenx/pool",list_api:"kudutenxpool_list/",detail_api:"tenxpool/",form_fields:ne.tenxpool},library:{title:"Tenx Libraries",url:"/list/tenx/library",list_api:"kudutenxlibrary_list/",detail_api:"tenxlibrary/",form_fields:ne.tenxlibrary},sequencing:{title:"Tenx Sequencings",url:"/list/tenx/sequencing",list_api:"kudutenxsequencing_list/",detail_api:"tenxsequencing/",form_fields:ne.tenxsequencing},analysis:{title:"Tenx Analyses",url:"/list/tenx/analysis",list_api:"kudutenxanalysis_list/",detail_api:"tenxanalysis/",form_fields:ne.tenxanalysis,noteditable:!0},summary:!0}},oe={account:{username:"Simong",authenticated:!1,colour:null},loading:!1,view:"list",model:{form_fields:{}},structure:ie,form:{},history:[]},re={SET_STRUCTURE:function(e,t){e.model=t.model,Object(b["d"])(e.model.form_fields)},SET_DETAIL:function(e,t){e.model=t.model,console.log("DETAIL"),console.log(e.model.form_fields),console.log(t.data),Object(b["b"])(t.data,e.model.form_fields),console.log("DETAIL"),console.log(e.model.form_fields)},AUTHENTICATE:function(e,t){e.account.authenticated=!0,e.account.username=t.username},LOADING:function(e){e.loading=!e.loading},KILLLOADING:function(e){console.log(e.loading),console.log("LOADING KILLED"),e.loading=!1,console.log(e.loading)},LOGOUT:function(e){console.log(this._vm.$session),e.account.authenticated=!1,localStorage.removeItem("user-token"),e.account.username=null,xe.push("/login")},UPDATE_AUTH_STATUS:function(e,t){e.account.authenticated=t},UPDATE_COLOUR:function(e,t){e.account.colour=t}},ae={searchQuery:function(e,t){e.commit;return new Promise(function(e,n){t.query||n("empty"),Y.a.get(b["a"]+"kudusearch/"+t.query,{headers:{Authorization:"JWT "+t.token}}).then(function(t){console.log("FFEE"),e(t.data)}).catch(function(e){console.log(e.response),n(e.response)})})},loadData:function(e,t){var n=e.commit,i=(e.dispatch,e.state);console.log("LOAD DATA"),console.log(t.type);var o=i.structure[t.app][t.model],r="list"===t.type||"relation"===t.type?o.list_api:o.detail_api+t.pk+"/";return new Promise(function(e,i){Y.a.get(b["a"]+r,{headers:{Authorization:"JWT "+t.token}}).then(function(i){"list"===t.type?(n("SET_STRUCTURE",{model:o}),e(i.data)):"relation"===t.type?e(i.data):"detail"===t.type&&n("SET_DETAIL",{data:i.data,model:o}),e("success")}).catch(function(e){console.log(e),i("fefe")})})},loadRelationList:function(e,t){e.commit,e.state;console.log("LOADRELATIONINFO"),console.log(t);var n=t.list.join(",");return new Promise(function(e,i){0==t.list.length&&i("empty"),Y.a.get(b["a"]+t.url,{params:{id__in:n},headers:{Authorization:"JWT "+t.token}}).then(function(t){e(t.data)}).catch(function(e){console.log(e),i(e.response)})})},login:function(e,t){var n=e.commit;return new Promise(function(e,i){Y.a.post(b["a"]+"auth/",{username:t.username,password:t.password}).then(function(i){localStorage.setItem("user-token",i.data.token),e("authenticated"),n("AUTHENTICATE",{username:t.username})}).catch(function(e){console.log("ERROR"),n("LOGOUT"),console.log(e),i("wrong username or password")})})},refresh:function(e,t){var n=e.commit;return new Promise(function(e,i){Y.a.post(b["a"]+"auth/refresh/",{token:t.token}).then(function(t){e("refreshed")}).catch(function(e){n("LOGOUT")})})}},le=(n("456d"),n("ac6a"),{getModel:function(e){return e.model},colourGetter:function(e){return console.log("waht do you mean"),console.log(e.account.colour),null===e.account.colour?"pink":e.account.colour},getModelTitle:function(e){return function(t,n){return e.structure[t][n].title}},getStructurekeys:function(e){var t={};return Object.keys(e.structure).forEach(function(n){var i=Object.keys(e.structure[n]);t[n.toUpperCase()]=[],e.structure[n].summary||(i=i.filter(function(e){return"summary"!==e})),i.forEach(function(i){var o=i.charAt(0).toUpperCase()+i.slice(1),r=e.structure[n][i].url;"summary"==i?t[n.toUpperCase()].push({icon:"mdi-chart-bar",text:o,link:r}):t[n.toUpperCase()].push({icon:"mdi-folder-open",text:o,link:r})})}),t},isEditable:function(e){return e.model.noteditable}});i["a"].use(K["a"]),i["a"].use(ee.a,Y.a);var se=new K["a"].Store({state:oe,mutations:re,actions:ae,getters:le}),ce=n("8c4f"),ue=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("v-card",{attrs:{flat:""}},[n("v-card-title",[n("h2",{class:"display-1 font-weight-light mb-4",style:{color:e.colour}},[e._v("Welcome to your new website!")])]),n("v-card-text",[n("v-icon",[e._v("mdi-human-greeting")]),e._v("\n    I am so happy to see you."),n("br"),n("h2",{class:"headline font-weight-light mb-4"},[e._v("Hopefully, this can replace our old boring website! \n    Just remember that there is still a lot of work to be done here. Only the visual part of the website is being completed right now.\n    I wanted to get some light feedback from you guys and see what I need to focus on from here."),n("br"),n("br"),e._v("\n    I still need to work on many features to ensure that this website provides every features that old colossus does. \n    But I want this to do much more than colossus, I am thinking of integrating other third party APIs like JIRA and Tantalus so everything you do can be done within this website."),n("br"),n("br"),n("v-icon",[e._v("mdi-bug")]),n("v-icon",[e._v("mdi-bug")]),e._v("Just be careful, since there are alot of bugs."),n("v-icon",[e._v("mdi-bug")]),n("v-icon",[e._v("mdi-bug")]),n("br"),n("br"),e._v("\n    \n    Or if you don't like this and wanna stick to our old website I will be hugely disappointed but that's fine too."),n("br"),n("br"),e._v("\n    If you have any problem, suggestion or feedback please contact Simong Song on our slack.")],1),n("div",{staticClass:"my-2"},[n("v-btn",{attrs:{text:""},on:{click:e.goToColossus}},[n("v-icon",[e._v("mdi-run-fast")]),e._v("\n      This upsets me take me back to old website.")],1)],1)],1)],1)],1)},de=[],pe={components:{},computed:{colour:function(){return this.$store.getters.colourGetter}},methods:{goToColossus:function(){window.location.href="https://colossus.canadacentral.cloudapp.azure.com"}}},_e=pe,me=Object(p["a"])(_e,ue,de,!1,null,null,null),ye=me.exports;m()(me,{VBtn:y["a"],VCard:f["a"],VCardText:g["b"],VCardTitle:g["c"],VIcon:C["a"]});var fe=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-content",[n("v-container",{attrs:{fluid:"","fill-height":""}},[n("v-layout",{attrs:{"align-center":"","justify-center":""}},[n("v-flex",{attrs:{xs12:"",sm8:"",md4:""}},[e.credentialsValid?e._e():n("v-alert",{attrs:{dense:"",outlined:"",type:"error"}},[e._v("\n        Invalid username or password\n      ")]),n("v-card",{staticClass:"elevation-12",staticStyle:{align:"center"}},[n("v-toolbar",{attrs:{color:"#E91E63",flat:""}},[n("v-toolbar-title",[e._v("Login")]),n("v-spacer")],1),n("v-card-text",[n("v-form",[n("v-text-field",{attrs:{"prepend-icon":"person",label:"Account"},on:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.login(t)}},model:{value:e.account.username,callback:function(t){e.$set(e.account,"username",t)},expression:"account.username"}}),n("v-text-field",{attrs:{id:"password",label:"Password",name:"password","prepend-icon":"lock","append-icon":e.show?"visibility":"visibility_off",type:e.show?"text":"password",rules:[e.rules.required,e.rules.min],hint:"At least 5 characters",counter:""},on:{"click:append":function(t){e.show=!e.show},keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.login(t)}},model:{value:e.account.password,callback:function(t){e.$set(e.account,"password",t)},expression:"account.password"}})],1)],1),n("v-card-actions",[n("v-spacer"),n("v-btn",{attrs:{color:"info"},on:{click:e.login}},[e._v("Login")])],1)],1)],1)],1)],1)],1)},ge=[],Se={name:"login",computed:{},methods:{login:function(){var e=this;this.$store.dispatch("login",this.account).then(function(t){console.log(t),e.$router.push("/")},function(t){e.credentialsValid=!1})}},data:function(){return{show:!1,rules:{required:function(e){return!!e||"Required"},min:function(e){return e.length>=5||"Min 8 characters"},emailMatch:function(){return"The email and password you entered don't match"}},account:{username:"",password:""},credentialsValid:!0}}},he=Se,Ae=(n("f1e4"),n("0798")),ve=n("4bd4"),Ie=n("71d9"),be=Object(p["a"])(he,fe,ge,!1,null,"670449d2",null),Ge=be.exports;m()(be,{VAlert:Ae["a"],VBtn:y["a"],VCard:f["a"],VCardActions:g["a"],VCardText:g["b"],VContainer:B["a"],VContent:F["a"],VFlex:U["a"],VForm:ve["a"],VLayout:M["a"],VSpacer:A["a"],VTextField:z["a"],VToolbar:Ie["a"],VToolbarTitle:J["a"]}),i["a"].use(ce["a"]);var ke=new ce["a"]({mode:"history",base:"/",routes:[{path:"/login",name:"login",component:Ge},{path:"/",name:"home",component:ye,meta:{auth:!0}},{path:"/detail/:app/:type/:pk",name:"detail",meta:{auth:!0},component:function(){return Promise.all([n.e("chunk-169ccd73"),n.e("chunk-2d0a2d59")]).then(n.bind(null,"0036"))}},{path:"/list/:app/:type/",name:"list",meta:{auth:!0},component:function(){return Promise.all([n.e("chunk-169ccd73"),n.e("chunk-2d0bff12")]).then(n.bind(null,"4055"))}},{path:"/search/:query",name:"search",meta:{auth:!0},component:function(){return n.e("chunk-2d0e6293").then(n.bind(null,"9820"))}}]});ke.beforeEach(function(e,t,n){var i=e.matched.some(function(e){return e.meta.auth}),o=!!localStorage.getItem("user-token")||"";i&&!o?n("/login"):n()});var xe=ke,Ce=(n("1f7a"),n("0628")),Ee=n.n(Ce),Te=(n("d1e7"),n("f309"));n("bf40");i["a"].use(Te["a"]);var we=new Te["a"]({icons:{iconfont:"mdi"}});i["a"].use(Te["a"]),i["a"].use(Ee.a),i["a"].config.productionTip=!1;t["default"]=new Te["a"]({icons:{iconfont:"md"},theme:{dark:{primary:"#3f51b5",secondary:"#b0bec5",accent:"#8c9eff",error:"#b71c1c",backgroundColor:"#fffff"}}});new i["a"]({router:xe,store:se,vuetify:we,render:function(e){return e(X)}}).$mount("#app")},e79e:function(e,t,n){},f1e4:function(e,t,n){"use strict";var i=n("e79e"),o=n.n(i);o.a}});
//# sourceMappingURL=app.348545d9.js.map