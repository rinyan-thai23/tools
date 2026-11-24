document.addEventListener('DOMContentLoaded', function() {
    // --- 設定 ---
    // プリセットキーワードをカテゴリ別に定義
    const presetCategories = [
        {
            name: "1. 学習・講座系",
            keywords: [
                { keyword: 'playlist', description: '最も基本。単独検索＋Filter で OK' },
                { keyword: 'playlists', description: '最も基本。単独検索＋Filter で OK' },
                { keyword: 'course', description: '「基礎から全部入り」のリストが多い' },
                { keyword: 'full course', description: '「基礎から全部入り」のリストが多い' },
                { keyword: 'complete course', description: '「基礎から全部入り」のリストが多い' },
                { keyword: 'tutorial', description: 'ハウツー系を一度に見たいとき' },
                { keyword: 'tutorial playlist', description: 'ハウツー系を一度に見たいとき' },
                { keyword: 'tutorial series', description: 'ハウツー系を一度に見たいとき' },
                { keyword: 'crash course', description: '短期集中講座の定番ワード' },
                { keyword: 'bootcamp', description: '“ゼロ→プロ”系の長尺講義' },
                { keyword: 'lecture series', description: '大学や研究機関の公開講義' },
                { keyword: 'lectures', description: '大学や研究機関の公開講義' },
                { keyword: 'masterclass', description: '1テーマを深掘りする上級者向け' },
                { keyword: 'training', description: '実務寄りの“研修”風リスト' },
                { keyword: 'training playlist', description: '実務寄りの“研修”風リスト' },
                { keyword: 'roadmap', description: '体系的コース' },
                { keyword: 'from scratch', description: '初心者～上級まで一気に学ぶ系' },
                { keyword: 'zero to hero', description: '初心者～上級まで一気に学ぶ系' },
                { keyword: 'beginner to advanced', description: '初心者～上級まで一気に学ぶ系' }
            ]
        },
        {
            name: "2. まとめ・一気見系",
            keywords: [
                { keyword: 'compilation', description: '音楽・アニメ・バラエティのまとめ' },
                { keyword: 'full compilation', description: '音楽・アニメ・バラエティのまとめ' },
                { keyword: 'collection', description: '公式 MV やアート作品などの“全集”' },
                { keyword: 'mix', description: '音楽系 BGM に強い' },
                { keyword: 'mega mix', description: '音楽系 BGM に強い' },
                { keyword: 'greatest hits', description: '有名アーティストや番組の「ベスト版」' },
                { keyword: 'best of', description: '有名アーティストや番組の「ベスト版」' },
                { keyword: 'full album', description: '“公式フル”が並ぶことも' },
                { keyword: 'full movie', description: '“公式フル”が並ぶことも' },
                { keyword: 'marathon', description: 'シリーズ動画を一気見したいとき' },
                { keyword: 'full episodes', description: 'ドラマ・アニメの公式一括公開' },
                { keyword: 'all episodes', description: 'ドラマ・アニメの公式一括公開' }
            ]
        },
        {
            name: "3. シリーズ物・連番系",
            keywords: [
                { keyword: 'series', description: '「part 1～」など連番構成が多い' },
                { keyword: 'season 1', description: '海外ドラマやポッドキャスト系 (Season 2... も同様)' },
                // { keyword: 'season 2', description: '海外ドラマやポッドキャスト系' }, // 例
                { keyword: 'episode 1', description: '第1話から追うときに便利 (ep 1 も同様)' },
                { keyword: 'ep 1', description: '第1話から追うときに便利' },
                { keyword: 'part 1', description: '分割アップロード物をまとめて拾える (part 2... も同様)' },
                // { keyword: 'part 2', description: '分割アップロード物' }, // 例
                { keyword: 'walkthrough', description: 'ゲーム実況の完走リストを探す' },
                { keyword: 'playthrough', description: 'ゲーム実況の完走リストを探す' }
            ]
        },
        {
            name: "4. テスト・勉強＆復習系",
            keywords: [
                { keyword: 'study guide', description: '試験直前まとめ系' },
                { keyword: 'revision', description: '試験直前まとめ系' },
                { keyword: 'practice questions', description: '問題演習リスト' },
                { keyword: 'exam prep', description: '問題演習リスト' },
                { keyword: 'flashcards', description: '単語帳スタイル動画' },
                { keyword: 'mock test', description: '模擬試験を一気に視聴' }
            ]
        },
        // --- 以下は多言語キーワードの例（必要なら追加・修正） ---
        {
            name: "5. 多言語キーワード (学習系)",
            keywords: [
                { keyword: 'curso completo', description: 'スペイン語: 完全コース' },
                { keyword: 'curso intensivo', description: 'スペイン語: 短期集中コース' },
                { keyword: 'cours complet', description: 'フランス語: 完全コース' },
                { keyword: 'formation complète', description: 'フランス語: 完全トレーニング' },
                { keyword: 'Komplettkurs', description: 'ドイツ語: 完全コース' },
                { keyword: 'Gesamtvorlesung', description: 'ドイツ語: 全講義' },
                { keyword: 'полный курс', description: 'ロシア語: 完全コース' },
                { keyword: 'интенсив', description: 'ロシア語: 短期集中' }
            ]
        }
    ];

    const youtubeSearchBaseUrl = 'https://www.youtube.com/results?search_query=';
    const playlistFilterParam = '&sp=EgIQAw%3D%3D';

    // --- 要素取得 ---
    const customKeywordInput = document.getElementById('customKeywordInput');
    const customSearchButton = document.getElementById('customSearchButton');
    const prefixKeywordInput = document.getElementById('prefixKeywordInput');
    const presetButtonsContainer = document.getElementById('presetButtons'); // ボタン全体を入れるコンテナ

    // --- 関数定義 ---
    function openYouTubePlaylistSearch(keyword) {
        if (!keyword || keyword.trim() === '') {
            alert('検索キーワードが空です。');
            return;
        }
        const encodedKeyword = encodeURIComponent(keyword.trim());
        const searchUrl = `${youtubeSearchBaseUrl}${encodedKeyword}${playlistFilterParam}`;
        window.open(searchUrl, '_blank');
    }

    // --- 初期化処理 (プリセットボタン生成) ---
    presetCategories.forEach(category => {
        // カテゴリ見出しを作成
        const categoryHeader = document.createElement('h3');
        categoryHeader.textContent = category.name;
        presetButtonsContainer.appendChild(categoryHeader);

        // このカテゴリのボタンを入れるdivを作成
        const categoryDiv = document.createElement('div');

        // カテゴリ内の各キーワードについて処理
        category.keywords.forEach(item => {
            // ボタンと説明文をまとめるコンテナを作成
            const itemWrapper = document.createElement('span'); // spanに変更しインライン表示しやすくする
            itemWrapper.className = 'preset-item'; // CSSクラスを適用

            // ボタンを作成
            const button = document.createElement('button');
            button.textContent = item.keyword;

            // 説明文を作成
            const descriptionSpan = document.createElement('span');
            descriptionSpan.className = 'description'; // CSSクラスを適用
            descriptionSpan.textContent = `(${item.description})`; // 説明文をカッコで囲む

            // ボタンクリック時のイベントリスナー
            button.addEventListener('click', function() {
                const prefix = prefixKeywordInput.value.trim();
                let finalKeyword = prefix ? `${prefix} ${item.keyword}` : item.keyword;
                openYouTubePlaylistSearch(finalKeyword);
            });

            // 要素を組み立てる
            itemWrapper.appendChild(button);
            itemWrapper.appendChild(descriptionSpan);
            categoryDiv.appendChild(itemWrapper); // カテゴリdivにアイテムを追加
        });

        presetButtonsContainer.appendChild(categoryDiv); // 全体コンテナにカテゴリdivを追加
    });

    // --- イベントリスナー設定 (自由検索) ---
    customSearchButton.addEventListener('click', function() {
        openYouTubePlaylistSearch(customKeywordInput.value);
    });
    customKeywordInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' || event.keyCode === 13) {
            event.preventDefault();
            openYouTubePlaylistSearch(customKeywordInput.value);
        }
    });
});