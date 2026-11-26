// 公式MCP(dataforseo-mcp-server 3.1.3)を stdio で起動し、api_request を呼ぶ共通部品。
// 使う前に：このフォルダの親(2026_11/mcp)で `npm i`、実行時に NODE_USE_ENV_PROXY=1（クラウド環境のプロキシ用）。
// 認証：ID・パスワードはダミー。クラウド環境ではプロキシが本物に差し替える。自分のPCで動かす時は環境変数 DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD に本物を入れる。
import {Client} from '@modelcontextprotocol/sdk/client/index.js';
import {StdioClientTransport} from '@modelcontextprotocol/sdk/client/stdio.js';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export async function connect() {
  const t = new StdioClientTransport({
    command: 'node',
    args: [path.join(root, 'node_modules/dataforseo-mcp-server/dist/index.js')],
    env: {...process.env, DATAFORSEO_LOGIN: process.env.DATAFORSEO_LOGIN || 'dummy', DATAFORSEO_PASSWORD: process.env.DATAFORSEO_PASSWORD || 'dummy'},
    stderr: 'ignore',
  });
  const c = new Client({name: 'mcp-lab', version: '0.1'});
  await c.connect(t);
  const self = {cost: 0, calls: 0, tokens_chars: 0};
  // noAi=true で通常パス（cost が返る）。false で .ai パス（軽いが cost は返らない）
  self.api = async (path_, data, {noAi = true, method = 'POST'} = {}) => {
    const r = await c.callTool({name: 'api_request', arguments: {method, path: path_, data, noAiMode: noAi}});
    const text = r.content[0].text;
    self.calls++; self.tokens_chars += text.length;
    const d = JSON.parse(text);
    self.cost += d.cost || 0;
    return d;
  };
  self.close = () => c.close();
  return self;
}
