// 安全な簡易Markdown表示。HTMLは全部無効化し、リンク・太字・見出し・箇条書き・表だけを通す。
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const inline = (s) => esc(s)
  .replace(/\[ハイライトの開始\]([\s\S]*?)\[ハイライトの終了\]/g, '<mark>$1</mark>')
  .replace(/\[\[(\d+)\]\]\((https?:\/\/[^\s)]+)\)/g, '<a class="cite" href="$2" target="_blank" rel="noopener nofollow">[$1]</a>')
  .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener nofollow">$1</a>')
  .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
  .replace(/\*([^*]+)\*/g, '<em>$1</em>');

export function markdownToHtml(src) {
  const lines = String(src).split('\n');
  let out = '', i = 0;
  const isList = (l) => /^\s*([-*]|\d+\.)\s+/.test(l);
  while (i < lines.length) {
    const L = lines[i];
    if (!L.trim()) { i++; continue; }
    if (L.trim().startsWith('|')) {
      const rows = [];
      while (i < lines.length && lines[i].trim().startsWith('|')) rows.push(lines[i++]);
      const cells = (x) => x.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
      const [head, , ...body] = rows;
      out += `<div class="scroll"><table><thead><tr>${cells(head).map((c) => `<th>${inline(c)}</th>`).join('')}</tr></thead><tbody>${body.map((x) => `<tr>${cells(x).map((c) => `<td>${inline(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
      continue;
    }
    const hm = L.match(/^(#{1,6})\s+(.*)/);
    if (hm) { out += `<h4>${inline(hm[2])}</h4>`; i++; continue; }
    if (isList(L)) {
      const ordered = /^\s*\d+\./.test(L);
      let items = '';
      while (i < lines.length && isList(lines[i])) {
        const depth = Math.min(2, (lines[i].match(/^(\t| {2,4})*/)[0].replace(/ {2,4}/g, '\t').length));
        items += `<li class="d${depth}">${inline(lines[i].replace(/^\s*([-*]|\d+\.)\s+/, ''))}</li>`;
        i++;
      }
      out += ordered ? `<ol>${items}</ol>` : `<ul>${items}</ul>`;
      continue;
    }
    out += `<p>${inline(L.trim())}</p>`;
    i++;
  }
  return out;
}
