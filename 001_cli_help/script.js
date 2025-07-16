document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const promptInput = document.getElementById('prompt-input');
    const copyPromptButton = document.getElementById('copy-prompt-button');
    const savePromptButton = document.getElementById('save-prompt-button');
    const savedPromptsSelect = document.getElementById('saved-prompts-select');
    const deletePromptButton = document.getElementById('delete-prompt-button');
    const commandButtonsContainer = document.getElementById('command-buttons-container');
    const templateButtonsContainer = document.getElementById('template-buttons-container');
    const tooltipArea = document.getElementById('tooltip-area');
    const placeholderInputsContainer = document.getElementById('placeholder-inputs-container');
    const addCustomCommandButton = document.getElementById('add-custom-command-button');
    const customCommandButtonsContainer = document.getElementById('custom-command-buttons-container');

    const originalTooltipText = tooltipArea.textContent;

    // --- Storage Keys ---
    const SAVED_PROMPTS_KEY = 'geminiHelper_savedPrompts';
    const CUSTOM_COMMANDS_KEY = 'geminiHelper_customCommands';

    // --- Utility Functions ---
    const getFromStorage = (key) => JSON.parse(localStorage.getItem(key)) || {};
    const saveToStorage = (key, data) => localStorage.setItem(key, JSON.stringify(data));

    // --- Feature 1: Prompt Actions (Copy, Save, Load, Delete) ---

    // 1a. Copy Prompt
    copyPromptButton.addEventListener('click', () => {
        if (!promptInput.value) return;
        navigator.clipboard.writeText(promptInput.value)
            .then(() => {
                const originalText = copyPromptButton.textContent;
                copyPromptButton.textContent = 'コピーしました！';
                setTimeout(() => {
                    copyPromptButton.textContent = originalText;
                }, 2000);
            })
            .catch(err => {
                console.error('コピーに失敗しました: ', err);
                alert('コピーに失敗しました。');
            });
    });

    // 1b. Save Prompt
    savePromptButton.addEventListener('click', () => {
        const promptText = promptInput.value;
        if (!promptText) {
            alert('保存するプロンプトが入力されていません。');
            return;
        }
        const promptName = prompt('プロンプトの保存名を入力してください:', `名称未設定プロンプト ${Object.keys(getFromStorage(SAVED_PROMPTS_KEY)).length + 1}`);
        if (promptName) {
            const savedPrompts = getFromStorage(SAVED_PROMPTS_KEY);
            savedPrompts[promptName] = promptText;
            saveToStorage(SAVED_PROMPTS_KEY, savedPrompts);
            loadSavedPrompts();
            alert(`「${promptName}」という名前でプロンプトを保存しました。`);
        }
    });

    // 1c. Load Saved Prompts into Select
    const loadSavedPrompts = () => {
        const savedPrompts = getFromStorage(SAVED_PROMPTS_KEY);
        savedPromptsSelect.innerHTML = '<option value="">保存済みプロンプトを選択...</option>';
        for (const name in savedPrompts) {
            const option = document.createElement('option');
            option.value = name;
            option.textContent = name;
            savedPromptsSelect.appendChild(option);
        }
    };

    // 1d. Handle Prompt Selection
    savedPromptsSelect.addEventListener('change', () => {
        const selectedName = savedPromptsSelect.value;
        if (selectedName) {
            const savedPrompts = getFromStorage(SAVED_PROMPTS_KEY);
            promptInput.value = savedPrompts[selectedName];
            promptInput.dispatchEvent(new Event('input')); // プレースホルダー更新をトリガー
        }
    });

    // 1e. Delete Prompt
    deletePromptButton.addEventListener('click', () => {
        const selectedName = savedPromptsSelect.value;
        if (!selectedName) {
            alert('削除するプロンプトを選択してください。');
            return;
        }
        if (confirm(`本当に「${selectedName}」を削除しますか？`)) {
            const savedPrompts = getFromStorage(SAVED_PROMPTS_KEY);
            delete savedPrompts[selectedName];
            saveToStorage(SAVED_PROMPTS_KEY, savedPrompts);
            loadSavedPrompts();
            promptInput.value = '';
             promptInput.dispatchEvent(new Event('input'));
        }
    });


    // --- Feature 2: Command Buttons (Default & Custom) ---

    const createButton = (text, description, container, className, isCustom = false) => {
        const button = document.createElement('button');
        button.textContent = text;
        button.classList.add(className);
        container.appendChild(button);

        button.addEventListener('click', () => {
            promptInput.value += text + ' ';
            promptInput.focus();
        });

        button.addEventListener('mouseover', () => {
            tooltipArea.textContent = description;
            tooltipArea.style.opacity = '1';
        });

        button.addEventListener('mouseout', () => {
            tooltipArea.textContent = originalTooltipText;
            tooltipArea.style.opacity = '1';
        });
        
        if (isCustom) {
            button.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                if(confirm(`カスタムコマンド「${text}」を削除しますか？`)){
                    const customCommands = getFromStorage(CUSTOM_COMMANDS_KEY);
                    delete customCommands[text];
                    saveToStorage(CUSTOM_COMMANDS_KEY, customCommands);
                    loadCustomCommands();
                }
            });
        }
    };

    // 2a. Default Commands
    const commandCategories = {
        "スラッシュコマンド (メタ指示)": {
            "/help": "利用可能なコマンドやキーボードショートカットの一覧を表示します。",
            "/tools": "現在AIが利用できるツール（機能）の一覧を表示します。",
            "/path": "プロジェクトのルートディレクトリを手動で指定し直します。",
            "/quit": "Gemini CLIのセッションを安全に終了します。"
        },
        "シェルコマンド (PCへの直接命令)": {
            "!dir": "[Win] 現在のフォルダ内のファイルやフォルダを一覧表示します。",
            "!ls -l": "[Mac/Linux] 詳細なファイル一覧を表示します。",
            "!cls": "[Win] ターミナルの画面をクリアします。",
            "!clear": "[Mac/Linux] ターミナルの画面をクリアします。",
            "!npm install": "Node.jsのパッケージをインストールします。"
        }
    };

    for (const categoryTitle in commandCategories) {
        const categoryH3 = document.createElement('h3');
        categoryH3.textContent = categoryTitle;
        commandButtonsContainer.appendChild(categoryH3);
        const commands = commandCategories[categoryTitle];
        for (const text in commands) {
            createButton(text, commands[text], commandButtonsContainer, 'command-btn');
        }
    }

    // 2b. Custom Commands
    const loadCustomCommands = () => {
        customCommandButtonsContainer.innerHTML = '';
        const customCommands = getFromStorage(CUSTOM_COMMANDS_KEY);
        for (const name in customCommands) {
            createButton(name, customCommands[name], customCommandButtonsContainer, 'custom-command-btn', true);
        }
    };

    addCustomCommandButton.addEventListener('click', () => {
        const name = prompt('追加するカスタムコマンドのボタン名を入力してください:');
        if (!name) return;
        const command = prompt(`「${name}」ボタンがクリックされた時に挿入されるテキストを入力してください:`);
        if (!command) return;

        const customCommands = getFromStorage(CUSTOM_COMMANDS_KEY);
        customCommands[name] = command;
        saveToStorage(CUSTOM_COMMANDS_KEY, customCommands);
        loadCustomCommands();
    });


    // --- Feature 3: Prompt Templates & Placeholder Support ---

    // 3a. Prompt Templates
    const promptTemplates = {
        "ファイルの要約": "# 指示: ファイルの要約\n\n以下のファイルの内容を読み込み、その目的と主要な機能を箇条書きで3点にまとめてください。\n\n@ファイル名を入力",
        "新規Webページ作成": "# 指示: 新規Webページ作成\n\n以下の仕様で、HTML, CSS, JSファイルを作成してください。\n\n## 目的\n@アプリの目的を記述\n\n## 機能\n- @機能1\n- @機能2\n- @機能3",
        "コードのリファクタリング": "# 指示: コードのリファクタリング\n\n@元のファイル名 を読み込み、より効率的で読みやすいコードに書き換えた新しいファイル @新しいファイル名 を作成してください。\n\n## 改善方針\n- 変数名を分かりやすくする\n- 重複コードを関数化する",
        "バグの原因調査": "# 指示: バグの原因調査\n\n以下のエラーメッセージと関連するコードを分析し、バグの根本的な原因と修正案を提案してください。\n\n## エラーメッセージ\n```\n@エラーメッセージを貼り付け\n```\n\n## 関連ファイル\n@関連ファイル名を入力",
        "テストコード生成": "# 指示: テストコード生成\n\n`@対象のソースファイル` のためのテストコードを、`@テストファイル名` として作成してください。\nフレームワークは `jest` を使用してください。",
        "アイデア出し": "# 指示: アイデア出し\n\nテーマ「@テーマを記述」について、革新的なアイデアを5つ提案してください。それぞれのアイデアには、簡単な説明と想定されるメリットを添えてください。",
        "翻訳": "# 指示: 翻訳\n\n以下のテキストを @翻訳先の言語 に翻訳してください。\n\n```\n@翻訳するテキストを入力\n```",
        "メール作成": "# 指示: メールの下書き作成\n\n件名：@件名\n\n宛先：@宛名 様\n\n内容：\n- 挨拶\n- @要件を記述\n- 結び",
        "ブログ記事作成": "# 指示: ブログ記事作成\n\nタイトル：@タイトル\n\nキーワード：\n- @キーワード1\n- @キーワード2\n\n構成案：\n- 導入\n- @主題\n- メリット・デメリット\n- まとめ"
    };

    for (const key in promptTemplates) {
        const templateText = promptTemplates[key];
        const button = document.createElement('button');
        button.textContent = key;
        button.classList.add('template-btn');
        templateButtonsContainer.appendChild(button);

        button.addEventListener('click', () => {
            promptInput.value = templateText;
            promptInput.dispatchEvent(new Event('input')); // プレースホルダー更新をトリガー
        });
        
        button.addEventListener('mouseover', () => {
            tooltipArea.textContent = templateText;
            tooltipArea.style.opacity = '1';
        });

        button.addEventListener('mouseout', () => {
            tooltipArea.textContent = originalTooltipText;
            tooltipArea.style.opacity = '1';
        });
    }

    // 3b. Placeholder Input Support
    const updatePlaceholders = () => {
        placeholderInputsContainer.innerHTML = '';
        const text = promptInput.value;
        const placeholderRegex = /@([^\s`\n@]+)/g;
        const placeholders = [...new Set(Array.from(text.matchAll(placeholderRegex), m => m[0]))]; // 重複を削除

        if (placeholders.length > 0) {
            placeholders.forEach(placeholder => {
                const inputGroup = document.createElement('div');
                inputGroup.className = 'placeholder-input-group';

                const label = document.createElement('label');
                label.textContent = placeholder;
                inputGroup.appendChild(label);

                const input = document.createElement('input');
                input.type = 'text';
                input.dataset.placeholder = placeholder;
                inputGroup.appendChild(input);

                input.addEventListener('input', () => {
                    let currentValue = promptInput.value;
                    const regex = new RegExp(input.dataset.placeholder, 'g');
                    // 入力値が空の場合はプレースホルダーをそのままに、そうでなければ置き換える
                    const replacement = input.value ? input.value : input.dataset.placeholder;
                    // このロジックだと入力するたびに元のプロンプトに戻ってしまうので修正が必要
                    // -> テンプレートを保持し、そこから毎回生成する方式に変更
                    
                    // 簡単な実装：毎回全置換する（カーソル位置が失われる欠点あり）
                    // この方法はユーザー体験が悪いので、より良い方法を検討
                });

                placeholderInputsContainer.appendChild(inputGroup);
            });
        }
    };
    
    // プレースホルダー機能の改善版
    let originalTemplate = '';

    const updatePromptFromPlaceholders = () => {
        let newPrompt = originalTemplate;
        const inputs = placeholderInputsContainer.querySelectorAll('input');
        inputs.forEach(input => {
            const placeholder = input.dataset.placeholder;
            const value = input.value;
            if (value) {
                newPrompt = newPrompt.replace(new RegExp(placeholder, 'g'), value);
            }
        });
        promptInput.value = newPrompt;
    };
    
    const setupPlaceholderInputs = (template) => {
        originalTemplate = template;
        placeholderInputsContainer.innerHTML = '';
        const placeholderRegex = /@([^\s`\n@]+)/g;
        const placeholders = [...new Set(Array.from(template.matchAll(placeholderRegex), m => m[0]))];

        if (placeholders.length > 0) {
            placeholders.forEach(placeholder => {
                const inputGroup = document.createElement('div');
                inputGroup.className = 'placeholder-input-group';

                const label = document.createElement('label');
                label.textContent = placeholder.substring(1); // Remove '@'
                inputGroup.appendChild(label);

                const input = document.createElement('input');
                input.type = 'text';
                input.dataset.placeholder = placeholder;
                input.placeholder = `値を入力...`;
                inputGroup.appendChild(input);

                input.addEventListener('input', updatePromptFromPlaceholders);
                placeholderInputsContainer.appendChild(inputGroup);
            });
        }
        updatePromptFromPlaceholders();
    };

    // テンプレートボタンのクリックイベントを修正
    templateButtonsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('template-btn')) {
            const templateKey = e.target.textContent;
            const templateText = promptTemplates[templateKey];
            promptInput.value = templateText;
            setupPlaceholderInputs(templateText);
        }
    });

    promptInput.addEventListener('input', () => {
        // ユーザーが手動で編集した場合は、プレースホルダー機能を一旦リセット
        if (promptInput.value !== originalTemplate) {
             placeholderInputsContainer.innerHTML = '';
             originalTemplate = '';
        }
    });


    // --- Initial Load ---
    loadSavedPrompts();
    loadCustomCommands();
});