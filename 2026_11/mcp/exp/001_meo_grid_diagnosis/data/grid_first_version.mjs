import {Client} from '@modelcontextprotocol/sdk/client/index.js';
import {StdioClientTransport} from '@modelcontextprotocol/sdk/client/stdio.js';
import fs from 'fs';
const [lat0,lng0,kw]=[35.7057,139.6497,'ラーメン'];
const t=new StdioClientTransport({command:'node',args:['node_modules/dataforseo-mcp-server/dist/index.js'],env:{...process.env,DATAFORSEO_LOGIN:'dummy',DATAFORSEO_PASSWORD:'dummy'}});
const c=new Client({name:'grid',version:'0.1'});await c.connect(t);
const cells=[];for(let r=-2;r<=2;r++)for(let q=-2;q<=2;q++)cells.push({r,q,lat:+(lat0-r*0.005).toFixed(5),lng:+(lng0+q*0.0062).toFixed(5)});
const out=[];let cost=0,i=0;
async function w(){while(i<cells.length){const cell=cells[i++];
 const res=await c.callTool({name:'api_request',arguments:{method:'POST',path:'/v3/serp/google/maps/live/advanced',noAiMode:true,data:[{keyword:kw,location_coordinate:`${cell.lat},${cell.lng},15z`,language_code:'ja',depth:20}]}});
 const d=JSON.parse(res.content[0].text);cost+=d.cost||0;const tk=d.tasks?.[0];
 const items=(tk?.result?.[0]?.items||[]).map(x=>({rank:x.rank_group,title:x.title,cid:x.cid,rating:x.rating?.value,votes:x.rating?.votes_count,lat:x.latitude,lng:x.longitude,cat:x.category,claimed:x.is_claimed,photos:x.total_photos}));
 out.push({...cell,status:tk?.status_code,items});}}
await Promise.all([w(),w(),w(),w(),w()]);
fs.writeFileSync('out/grid.json',JSON.stringify({keyword:kw,center:[lat0,lng0],cost,cells:out}));
console.log('cells',out.length,'cost',cost,'errors',out.filter(o=>o.status!==20000).length);await c.close();
