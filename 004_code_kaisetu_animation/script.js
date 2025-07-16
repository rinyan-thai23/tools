
    const codeInput = document.getElementById('codeInput');
    const explanationInput = document.getElementById('explanationInput');
    const startButton = document.getElementById('startButton');
    const inputContainer = document.getElementById('inputContainer');
    const outputContainer = document.getElementById('outputContainer');
    const codeOutput = document.getElementById('codeOutput');
    const rightPanel = document.getElementById('rightPanel');
    const typingSpeedInput = document.getElementById('typingSpeed');
    const pauseResumeButton = document.getElementById('pauseResumeButton');
    const languageSelect = document.getElementById('languageSelect');

    let typingSpeed = 10;
    let currentCharIndex = 0;
    let currentExplanationIndex = 0;
    let isTyping = false;
    let isPaused = false;
    let typeCharTimeout;
    let codeLines = [];
    let explanations = [];

    function updateSettings() {
        typingSpeed = parseInt(typingSpeedInput.value);
    }

    function updateControlButtons() {
        pauseResumeButton.textContent = isPaused ? "再開" : "一時停止";
        pauseResumeButton.disabled = !isTyping;
    }

    function resetToInputScreen() {
        outputContainer.style.display = 'none';
        inputContainer.style.display = 'block';
        isTyping = false;
        isPaused = false;
        currentCharIndex = 0;
        currentExplanationIndex = 0;
        clearTimeout(typeCharTimeout);
        updateControlButtons();
    }

    function pauseResumeTyping() {
        isPaused = !isPaused;
        updateControlButtons();
        if (!isPaused) {
            typeText();
        }
    }

    function highlightCodeLines(start, end) {
        const codeLines = codeOutput.querySelectorAll('.token-line');
        codeLines.forEach((line, index) => {
            if (index >= start - 1 && index <= end - 1) {
                line.innerHTML = line.innerHTML.replace(/<span class="highlight-line">(.*?)<\/span>/g, "$1");
                line.innerHTML = `<span class="highlight-line">${line.innerHTML}</span>`;
            } else {
                line.innerHTML = line.innerHTML.replace(/<span class="highlight-line">(.*?)<\/span>/g, "$1");
            }
        });
    }

    function parseExplanations(text) {
        const lines = text.split('\n');
        let explanations = [];
        let currentExplanation = null;

        lines.forEach(line => {
            const match = line.match(/^##(\d+(?:\.\d+)?)\s(.+)/);
            if (match) {
                if (currentExplanation) {
                    explanations.push(currentExplanation);
                }
                const [startLine, endLine] = match[1].split('.').map(Number);
                currentExplanation = {
                    lines: [startLine, endLine || startLine],
                    text: match[2] + '\n'
                };
            } else if (currentExplanation) {
                currentExplanation.text += line + '\n';
            }
        });

        if (currentExplanation) {
            explanations.push(currentExplanation);
        }

        return explanations;
    }

    startButton.addEventListener('click', () => {
        updateSettings();
        const code = codeInput.value;
        const explanation = explanationInput.value;
        if (code.trim() === '' || explanation.trim() === '') return;

        inputContainer.style.display = 'none';
        outputContainer.style.display = 'flex';
        
        // Apply syntax highlighting
        codeOutput.className = `language-${languageSelect.value}`;
        codeOutput.textContent = code;
        Prism.highlightElement(codeOutput);

        // Wrap each line in a span for individual highlighting
        codeOutput.innerHTML = codeOutput.innerHTML.split('\n').map(line => 
            `<span class="token-line">${line}</span>`
        ).join('\n');

        rightPanel.textContent = '';

        codeLines = code.split('\n');
        explanations = parseExplanations(explanation);

        currentCharIndex = 0;
        currentExplanationIndex = 0;
        isTyping = true;
        isPaused = false;
        updateControlButtons();

        typeText();
    });

    function typeText() {
        if (isPaused) return;

        if (currentExplanationIndex < explanations.length) {
            const currentExplanation = explanations[currentExplanationIndex];
            
            // ハイライトを最初に表示
            highlightCodeLines(currentExplanation.lines[0], currentExplanation.lines[1]);
            
            // 新しいセクションを開始する前に右パネルをクリア
            rightPanel.textContent = '';
            
            function typeChar() {
                if (isPaused) return;

                if (currentCharIndex < currentExplanation.text.length) {
                    rightPanel.textContent += currentExplanation.text[currentCharIndex];
                    currentCharIndex++;
                    rightPanel.scrollTop = rightPanel.scrollHeight;
                    typeCharTimeout = setTimeout(typeChar, typingSpeed + Math.random() * 50);
                } else {
                    // このセクションのタイピングが終了したら、少し待ってから次のセクションへ
                    setTimeout(() => {
                        currentExplanationIndex++;
                        currentCharIndex = 0;
                        typeText();
                    }, typingSpeed * 20); // より長い待機時間を設定
                }
            }
            typeChar();
        } else {
            isTyping = false;
            updateControlButtons();
        }
    }

    pauseResumeButton.addEventListener('click', pauseResumeTyping);

    outputContainer.addEventListener('click', (e) => {
        if (e.target === outputContainer || e.target === rightPanel) {
            resetToInputScreen();
        }
    });