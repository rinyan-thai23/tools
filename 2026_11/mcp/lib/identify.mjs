// 店の特定：「店名（＋地名）」から候補を出し、確信度を付ける。同名・チェーンで別の店を診断する事故を防ぐ。
// 使い方（コード）：const r = await identifyShop(mcp, {query:'ミント歯科', address_hint:'江古田', phone_hint:'03-...'});
// 確信度：high＝1店に絞れた／medium＝絞れたが確認推奨／low＝複数候補で絞れない（人が選ぶ）
const norm = s => (s || '').normalize('NFKC').toLowerCase().replace(/[\s　・･\-－ー_【】\[\]()（）「」『』,、.。]/g, '');
const digits = s => (s || '').replace(/[^0-9]/g, '');
export async function identifyShop(mcp, {query, address_hint, phone_hint, depth = 8}) {
  const d = await mcp.api('/v3/serp/google/maps/live/advanced', [{keyword: query, location_code: 2392, language_code: 'ja', depth}]);
  const items = (d.tasks?.[0]?.result?.[0]?.items || []).filter(i => i.cid);
  const q = norm(query); // 住所のヒントは検索語から取り除かない（取り除くと、チェーンの支店が同点になる）
  const cands = items.map(i => {
    const t = norm(i.original_title || i.title);
    let score = 0; const why = [];
    if (t && q && (t === q || t === q + '店')) { score += 3; why.push('店名が一致'); }
    else if (t.includes(q) || q.includes(t)) { score += 2; why.push('店名が部分一致'); }
    if (address_hint && (i.address || '').normalize('NFKC').includes(address_hint.normalize('NFKC'))) { score += 3; why.push('住所のヒントが一致'); }
    if (phone_hint && digits(i.phone).endsWith(digits(phone_hint).slice(-8)) && digits(phone_hint).length >= 8) { score += 5; why.push('電話番号が一致'); }
    return {cid: i.cid, 店名: i.original_title || i.title, 住所: i.address, 電話: i.phone, 評価: i.rating?.value ?? null, 口コミ数: i.rating?.votes_count ?? null, カテゴリ: i.category, 緯度: i.latitude, 経度: i.longitude, 点: score, 理由: why, 元: i};
  }).sort((a, b) => b.点 - a.点);
  const top = cands[0], second = cands[1];
  let confidence = 'low', reason = '';
  if (!top) reason = '候補が見つかりません';
  else if (top.点 >= 5 && (!second || top.点 - second.点 >= 2)) { confidence = 'high'; reason = top.理由.join('・'); }
  else if (top.点 >= 2 && (!second || top.点 - second.点 >= 1)) { confidence = 'medium'; reason = top.理由.join('・') + '（他に似た候補が少ない。確認推奨）'; }
  else { reason = second && top.点 === second.点 ? '同じ点の候補が複数（同名・チェーンの可能性）。住所か電話のヒントが要る' : '店名の一致が弱い。確認が要る'; }
  const sameName = top ? cands.filter(c => norm(c.店名) === norm(top.店名)).length : 0;
  if (sameName > 1 && confidence !== 'high') { confidence = 'low'; reason = `同名の店が${sameName}件あります。住所か電話のヒントが要る`; }
  return {shop: top?.元 || null, confidence, reason, candidates: cands.slice(0, 5).map(({元, ...r}) => r), cost: mcp.cost};
}
