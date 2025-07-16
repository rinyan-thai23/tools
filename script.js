document.addEventListener('DOMContentLoaded', () => {
    const toolListContainer = document.getElementById('tool-list');

    const tools = [
        {
            title: 'Gemini Prompt Helper',
            description: 'Google Gemini (CLI版) への指示（プロンプト）作成を強力にサポートするためのウェブアプリケーションです。よく使うコマンドや定型文（テンプレート）をボタン化し、プロンプト作成の手間を大幅に削減します。また、作成したプロンプトの保存・再利用も可能です。',
            link: '001_cli_help/index.html'
        },
        {
            title: 'LINE風ストーリー動画クリエイター Pro',
            description: 'LINEのトーク画面のような会話形式のストーリー動画をブラウザ上で簡単に作成できる高機能なウェブアプリケーションです。特別な動画編集ソフトを使わずに、テキストベースのスクリプトからアニメーション付きの動画を生成し、プレビューすることができます。',
            link: '002_line_story/index.html'
        },
        {
            title: 'YouTubeプレイリスト検索ツール',
            description: 'YouTubeのプレイリストを効率的に検索するためのウェブアプリケーションです。特定のキーワードで検索したり、あらかじめ定義された検索ワードの組み合わせを利用したりすることで、目的の動画リストを素早く見つけることができます。',
            link: '003_youtube_search_playlist/index.html'
        },
        {
            title: 'プログラミングコード解説アニメーションツール',
            description: 'プログラミングコードとその解説テキストを入力するだけで、コードの特定の部分をハイライトしながら、対応する解説をタイピング風に表示するアニメーションを生成するウェブアプリケーションです。教育的なコンテンツや、コードレビューのプレゼンテーションなどを視覚的に分かりやすく作成するのに役立ちます。',
            link: '004_code_kaisetu_animation/index.html'
        },
        {
            title: 'マルチタスクメモツール',
            description: '複数のテキストフィールドを使用してメモを効率的に管理できるシンプルなウェブアプリケーションです。各フィールドの文字数カウント、全体の合計文字数表示、ローカルストレージへの自動保存、そしてテキストファイルとしてのダウンロード機能を提供します。',
            link: '005_multi_task_memo/index.html'
        },
        {
            title: 'YouTube動画リサーチツール',
            description: 'YouTube Data API v3 を利用してYouTube動画を検索し、その結果を一覧表示するウェブアプリケーションです。キーワードやチャンネルID、最大表示件数を指定して動画を検索し、動画のタイトル、サムネイル、再生時間、そして動画URLを簡単に取得できます。',
            link: '006_youtube_video_researchtool/index.html'
        }
    ];

    tools.forEach(tool => {
        const toolCard = document.createElement('div');
        toolCard.classList.add('tool-card');

        const title = document.createElement('h2');
        title.textContent = tool.title;

        const description = document.createElement('p');
        description.textContent = tool.description;

        const link = document.createElement('a');
        link.href = tool.link;
        link.textContent = 'ツールを開く';
        link.target = '_blank'; // 新しいタブで開く

        toolCard.appendChild(title);
        toolCard.appendChild(description);
        toolCard.appendChild(link);
        toolListContainer.appendChild(toolCard);
    });
});