(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0a2d59"],{"0036":function(t,e,l){"use strict";l.r(e);var i=function(){var t=this,e=t.$createElement,l=t._self._c||e;return t.modelComputed?l("v-card",{staticStyle:{"border-radius":"0px"},attrs:{height:"calc(100vh - 70px)"}},[l("v-tabs",{attrs:{color:"white",right:""}},[l("v-tab",[t._v("Information")]),t.schoolingsExist?l("v-tab",[t._v("Additional")]):t._e(),l("v-tab",[t._v("Relations")]),l("v-tab",[t._v("Edit")]),l("v-tab",[t._v("Delete")]),l("v-tab-item",[l("v-container",[l("v-layout",[l("blockquote",{staticClass:"blockquote",staticStyle:{height:"calc(100vh - 150px)",width:"100%","overflow-y":"scroll"}},[l("span",{staticClass:"display-2"},[t._v(t._s(t.modelTitle)+" "+t._s(t.modelFields.id.value))]),l("br"),l("br"),l("ul",{staticStyle:{"list-style-type":"none","padding-left":"0px"}},t._l(t.modelFields,function(e,i){return l("li",{staticClass:"body-1",staticStyle:{clear:"both"}},[l("div",{staticStyle:{float:"left",width:"30%"}},[l("b",[t._v(t._s(t.titleEdit(i))+": ")])]),l("div",{staticStyle:{float:"left",width:"50%"}},[t._v(t._s(t.printNone(e.value)))]),l("v-divider")],1)}),0),l("br"),l("v-divider"),l("br"),t._l(t.modelChildren,function(e,i){return l("div",{staticStyle:{"margin-top":"20px"}},[l("span",{staticClass:"display-1"},[t._v(t._s(e.title))]),l("br"),l("ul",{staticStyle:{"list-style-type":"none","padding-left":"0px"}},t._l(e.fields,function(e,i){return l("li",{staticClass:"body-1",staticStyle:{clear:"both"}},[l("div",{staticStyle:{float:"left",width:"30%"}},[l("b",[t._v(t._s(t.titleEdit(i))+": ")])]),l("div",{staticStyle:{float:"left",width:"50%"}},[t._v(t._s(t.printNone(e.value)))]),l("v-divider")],1)}),0),l("br"),l("v-divider")],1)})],2)])],1)],1),t.schoolingsExist?l("v-tab-item",[l("v-container",{staticStyle:{height:"calc(90vh - 70px)","overflow-y":"scroll"}},[l("SchoolingComponent",{attrs:{schoolings:t.modelSchoolings}})],1)],1):t._e(),l("v-tab-item",[l("v-container",{staticStyle:{height:"calc(90vh - 70px)","overflow-y":"scroll"}},[l("ListComponent",{attrs:{relations:t.modelRelations}})],1)],1),l("v-tab-item",{staticStyle:{height:"calc(90vh - 70px)"}},[l("EditComponent",{attrs:{title:t.modelTitle,fields:t.modelFields,children:t.modelChildren,relations:t.modelRelations}})],1),l("v-tab-item",[l("v-card",{attrs:{flat:""}},[l("v-card-text",[l("div",{staticClass:"headline font-weight-light",style:{color:t.colour}},[t._v(" Are you sure? ")]),l("div",{staticClass:"display-1 font-weight-light"},[t._v("Other related entries can be affected by this deletion.")])])],1)],1)],1)],1):t._e()},o=[],s=(l("ac6a"),l("456d"),l("2a68")),r=function(){var t=this,e=t.$createElement,l=t._self._c||e;return l("div",[l("v-timeline",{attrs:{dense:""}},t._l(t.relations,function(e){return l("v-timeline-item",{attrs:{small:"","fill-dot":"",color:t.colour}},[l("SmallList",{attrs:{list:e.selected,url:t.getUrl(e),title:t.getTitle(e.model[0],e.model[1])}}),l("v-divider"),l("br")],1)}),1)],1)},a=[],n=function(){var t=this,e=t.$createElement,l=t._self._c||e;return l("v-data-table",{attrs:{dense:"",loading:t.loading,headers:t.headers,items:t.items,search:t.search},scopedSlots:t._u([{key:"top",fn:function(){return[l("v-toolbar",{attrs:{flat:""}},[l("h2",{class:"headline font-weight-light mb-4",style:{color:t.colour}},[t._v(t._s(t.title)+" LIST")]),l("v-spacer"),l("v-flex",{attrs:{xs6:"",md2:""}},[l("v-text-field",{attrs:{label:"search"},model:{value:t.search,callback:function(e){t.search=e},expression:"search"}})],1)],1)]},proxy:!0},{key:"item",fn:function(e){var i=e.item;return[l("tr",{on:{click:function(e){return t.$router.replace({name:"detail",params:{app:t.$route.params.app,type:t.$route.params.type,pk:i.id}})}}},t._l(t.headers,function(e){return l("td",[t._v("\n        "+t._s(i[e.value])+"\n      ")])}),0)]}}])})},c=[],d={name:"SmallList",props:["model","title","url","list"],created:function(){var t=this;this.$store.dispatch("loadRelationList",{url:this.url,list:this.list,token:localStorage.getItem("user-token")}).then(function(e){t.items=e,t.computeHeaders()},function(e){t.loading=!1})},data:function(){return{loading:!0,headers:[],items:[],search:""}},methods:{computeHeaders:function(){var t=this;Object.keys(this.items[0]).forEach(function(e){t.headers.push({align:"left",text:e.charAt(0).toUpperCase()+e.slice(1),value:e})}),this.loading=!1}},computed:{colour:function(){return this.$store.getters.colourGetter}}},u=d,h=l("2877"),m=l("6544"),f=l.n(m),v=l("8fea"),p=l("0e8f"),b=l("2fa4"),_=l("8654"),y=l("71d9"),g=Object(h["a"])(u,n,c,!1,null,null,null),S=g.exports;f()(g,{VDataTable:v["a"],VFlex:p["a"],VSpacer:b["a"],VTextField:_["a"],VToolbar:y["a"]});var x={name:"ListComponent",components:{SmallList:S},created:function(){},props:["relations"],methods:{getTitle:s["c"],getUrl:function(t){return this.$store.state.structure[t.model[0]][t.model[1]].list_api}},computed:{colour:function(){return this.$store.getters.colourGetter}}},$=x,C=l("ce7e"),k=l("8414"),w=l("1e06"),T=Object(h["a"])($,r,a,!1,null,null,null),V=T.exports;f()(T,{VDivider:C["a"],VTimeline:k["a"],VTimelineItem:w["a"]});var E=l("0f9f"),O=function(){var t=this,e=t.$createElement,l=t._self._c||e;return l("div",[l("v-timeline",{attrs:{dense:""}},t._l(t.schoolings,function(e){return l("v-timeline-item",{attrs:{small:"","fill-dot":"",color:t.colour}},[e.many?l("div",[l("SmallList",{attrs:{list:e.value,url:e.api,title:e.title}})],1):e.pivot?l("div",[l("h2",{class:"headline font-weight-light mb-4",style:{color:t.colour}},[t._v(t._s(e.title))]),l("PivotTable",{attrs:{structure:e.value}})],1):l("div",[l("h2",{class:"headline font-weight-light mb-4",style:{color:t.colour}},[t._v(t._s(e.title))]),l("ul",{staticStyle:{"list-style-type":"none","padding-left":"0px"}},[t._l(e.value,function(e,i){return l("li",{staticClass:"body-1",staticStyle:{clear:"both"}},[l("v-divider"),l("div",{staticStyle:{float:"left",width:"30%"}},[l("b",[t._v(t._s(t.titleEdit(i))+": ")])]),l("div",{staticStyle:{float:"left",width:"50%"}},[t._v(t._s(t.printNone(e)))]),l("br")],1)}),l("v-divider")],2),l("br")]),l("br")])}),1)],1)},j=[],L=function(){var t=this,e=t.$createElement,l=t._self._c||e;return 0!==Object.keys(t.structure).length?l("v-simple-table",[l("thead",[l("tr",[l("th"),t._l(t.colnames,function(e){return l("th",{staticClass:"text-left"},[l("b",[t._v(t._s(e))])])})],2)]),l("tbody",t._l(t.rownames,function(e){return l("tr",[l("td",[l("b",[t._v(t._s(e))])]),t._l(t.structure,function(i){return l("td",[t._v(t._s(i[e])+" ")])})],2)}),0)]):t._e()},I=[],D={name:"",props:["structure"],computed:{colnames:function(){return Object.keys(this.structure)},rownames:function(){return Object.keys(this.structure[this.colnames[0]])}}},F=D,N=l("1f4f"),R=Object(h["a"])(F,L,I,!1,null,null,null),G=R.exports;f()(R,{VSimpleTable:N["a"]});var A={name:"ListComponent",components:{SmallList:S,PivotTable:G},props:["schoolings"],computed:{colour:function(){return this.$store.getters.colourGetter}},methods:{titleEdit:s["f"],printNone:s["e"]}},U=A,q=Object(h["a"])(U,O,j,!1,null,null,null),H=q.exports;f()(q,{VDivider:C["a"],VTimeline:k["a"],VTimelineItem:w["a"]});var J={name:"detail",components:{ListComponent:V,EditComponent:E["a"],SchoolingComponent:H},data:function(){return{detailData:{}}},methods:{titleEdit:s["f"],printNone:s["e"],ifObjectNotEmpty:function(){Object.keys(yourObject).length}},created:function(){var t=this;this.$store.dispatch("refresh",{token:localStorage.getItem("user-token")}).then(this.$store.dispatch("loadData",{app:this.$route.params.app,type:"detail",pk:this.$route.params.pk,model:this.$route.params.type,token:localStorage.getItem("user-token")})).catch(function(e){t.$router.push("/login")})},computed:{colour:function(){return this.$store.getters.colourGetter},modelComputed:function(){return void 0!==this.$store.state.model.form_fields&&0!==Object.keys(this.$store.state.model.form_fields).length},modelTitle:function(){return this.$store.state.model.title},modelFields:function(){return this.$store.state.model.form_fields.fields},modelChildren:function(){return this.$store.state.model.form_fields.children},modelRelations:function(){return this.$store.state.model.form_fields.relations},schoolingsExist:function(){return"schoolings"in this.$store.state.model.form_fields},modelSchoolings:function(){return this.$store.state.model.form_fields.schoolings},isEditable:function(){return this.$store.state.model.noteditable}}},P=J,z=l("b0af"),B=l("99d9"),K=l("a523"),M=l("a722"),Q=l("71a3"),W=l("c671"),X=l("fe57"),Y=Object(h["a"])(P,i,o,!1,null,null,null);e["default"]=Y.exports;f()(Y,{VCard:z["a"],VCardText:B["b"],VContainer:K["a"],VDivider:C["a"],VLayout:M["a"],VTab:Q["a"],VTabItem:W["a"],VTabs:X["a"]})}}]);
//# sourceMappingURL=chunk-2d0a2d59.65c8a722.js.map