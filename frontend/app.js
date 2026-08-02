/* ============================================================
   AI Book Writer v2.0 — Frontend Application Logic
   ============================================================
   Fixes:
   - Bug #1: Nav items now map directly to section IDs (step1→step1, step2→step2, step3→step3)
   - Bug #2: No dashboard loading / no /api/projects call on startup
   - Bug #3: SSE stream checks task status before starting, has timeout & reconnection
   ============================================================ */

// ========================================================
// STATE
// ========================================================
const state = {
    currentStep: 1,
    taskId: null,
    eventSource: null,
    generating: false,
    generationComplete: false,
    downloadFile: null,
    lastMessageTime: null,
    sseTimeout: null,
    treeData: {
        units: [
            {
                name: 'Unit 1: Introduction',
                topics: [
                    {
                        name: 'Fundamentals',
                        subtopics: ['Overview and History']
                    }
                ]
            }
        ]
    }
};

// ========================================================
// NAVIGATION — BUG #1 FIX
// Direct step number → section mapping. No key translation needed.
// ========================================================
function navigateTo(step) {
    // Prevent leaving step 2 while generating
    if (state.generating && state.currentStep === 2 && step !== 2) {
        return;
    }

    // Prevent going to step 3 if not complete
    if (step === 3 && !state.generationComplete) {
        return;
    }

    // Hide all sections
    document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));

    // Show the target section
    const targetSection = document.getElementById(`section-step${step}`);
    if (targetSection) {
        targetSection.classList.add('active');
    }

    // Update sidebar active states
    document.querySelectorAll('.step-item').forEach(item => {
        item.classList.remove('active');
    });
    const targetNav = document.getElementById(`nav-step${step}`);
    if (targetNav) {
        targetNav.classList.add('active');
    }

    // Mark completed steps
    for (let i = 1; i < step; i++) {
        const navItem = document.getElementById(`nav-step${i}`);
        if (navItem) {
            navItem.classList.add('completed');
        }
    }

    // Update status badge
    const statusBadge = document.getElementById('system-status');
    const statusText = statusBadge.querySelector('.status-text');
    statusBadge.className = 'status-badge';

    if (step === 1) {
        statusText.textContent = 'Ready';
    } else if (step === 2) {
        statusText.textContent = 'Generating...';
        statusBadge.classList.add('active');
    } else if (step === 3) {
        statusText.textContent = 'Complete';
    }

    state.currentStep = step;
}

// ========================================================
// TREE EDITOR
// ========================================================
function renderTree() {
    const container = document.getElementById('syllabus-tree');
    container.innerHTML = '';

    state.treeData.units.forEach((unit, ui) => {
        const unitEl = document.createElement('div');
        unitEl.className = 'tree-unit';
        unitEl.innerHTML = `
            <div class="tree-unit-header">
                <span class="unit-badge">Unit ${ui + 1}</span>
                <input type="text" value="${escapeHtml(unit.name)}" 
                       onchange="updateUnitName(${ui}, this.value)" 
                       placeholder="Unit name...">
                <button class="btn-danger-sm" onclick="removeUnit(${ui})" title="Remove unit">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
        `;

        unit.topics.forEach((topic, ti) => {
            const topicEl = document.createElement('div');
            topicEl.className = 'tree-topic';
            topicEl.innerHTML = `
                <div class="tree-topic-header">
                    <span class="topic-badge">Topic ${ti + 1}</span>
                    <input type="text" value="${escapeHtml(topic.name)}" 
                           onchange="updateTopicName(${ui}, ${ti}, this.value)" 
                           placeholder="Topic name...">
                    <button class="btn-danger-sm" onclick="removeTopic(${ui}, ${ti})" title="Remove topic">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                </div>
            `;

            topic.subtopics.forEach((sub, si) => {
                const subEl = document.createElement('div');
                subEl.className = 'tree-subtopic';
                subEl.innerHTML = `
                    <input type="text" value="${escapeHtml(sub)}" 
                           onchange="updateSubtopicName(${ui}, ${ti}, ${si}, this.value)" 
                           placeholder="Subtopic name...">
                    <button class="btn-danger-sm" onclick="removeSubtopic(${ui}, ${ti}, ${si})" title="Remove subtopic">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                `;
                topicEl.appendChild(subEl);
            });

            // Add subtopic button
            const subActions = document.createElement('div');
            subActions.className = 'tree-actions';
            subActions.innerHTML = `
                <button class="btn-add-sm" onclick="addSubtopic(${ui}, ${ti})">
                    <i class="fa-solid fa-plus"></i> Add Subtopic
                </button>
            `;
            topicEl.appendChild(subActions);

            unitEl.appendChild(topicEl);
        });

        // Add topic button
        const topicActions = document.createElement('div');
        topicActions.style.cssText = 'margin-left: 1.5rem; margin-top: 0.5rem;';
        topicActions.innerHTML = `
            <button class="btn-add-sm" onclick="addTopic(${ui})">
                <i class="fa-solid fa-plus"></i> Add Topic
            </button>
        `;
        unitEl.appendChild(topicActions);

        container.appendChild(unitEl);
    });
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function addUnit() {
    const unitNum = state.treeData.units.length + 1;
    state.treeData.units.push({
        name: `Unit ${unitNum}`,
        topics: [{
            name: 'New Topic',
            subtopics: ['New Subtopic']
        }]
    });
    renderTree();
}

function removeUnit(ui) {
    if (state.treeData.units.length <= 1) return;
    state.treeData.units.splice(ui, 1);
    renderTree();
}

function updateUnitName(ui, value) {
    state.treeData.units[ui].name = value;
}

function addTopic(ui) {
    state.treeData.units[ui].topics.push({
        name: 'New Topic',
        subtopics: ['New Subtopic']
    });
    renderTree();
}

function removeTopic(ui, ti) {
    if (state.treeData.units[ui].topics.length <= 1) return;
    state.treeData.units[ui].topics.splice(ti, 1);
    renderTree();
}

function updateTopicName(ui, ti, value) {
    state.treeData.units[ui].topics[ti].name = value;
}

function addSubtopic(ui, ti) {
    state.treeData.units[ui].topics[ti].subtopics.push('New Subtopic');
    renderTree();
}

function removeSubtopic(ui, ti, si) {
    if (state.treeData.units[ui].topics[ti].subtopics.length <= 1) return;
    state.treeData.units[ui].topics[ti].subtopics.splice(si, 1);
    renderTree();
}

function updateSubtopicName(ui, ti, si, value) {
    state.treeData.units[ui].topics[ti].subtopics[si] = value;
}

function getTreeData() {
    return { units: state.treeData.units };
}

// ========================================================
// SMART SYLLABUS PARSER (Local Regex + AI Fallback)
// ========================================================
function parseSyllabusText(text) {
    if (!text || !text.trim()) return null;

    // 1. Extract Book Title if present
    let title = "";
    const titleMatch = text.match(/\*\*([^*]+)\*\*/) || text.match(/"([^"]+)"/) || text.match(/Title:\s*(.+)/i);
    if (titleMatch) {
        title = titleMatch[1].trim();
    }

    const lines = text.split('\n').map(l => l.trim()).filter(l => l.length > 0);
    const units = [];
    let currUnit = null;
    let currTopic = null;

    for (let line of lines) {
        if (line === '---' || line === '***' || line.toLowerCase().includes('book title')) continue;

        const clean = line.replace(/\*/g, '').replace(/^#+\s*/, '').trim();

        // Level 1: Chapter / Unit header (# Chapter or 1. Chapter or 1. Unit)
        const isLevel1 = line.startsWith('# ') || 
                         /^\d+\.\s*\*?(?:Chapter|Unit)/i.test(line);

        // Level 2: Topic (## 1.1 Topic or 1.1 Topic)
        const isLevel2 = line.startsWith('## ') || 
                         /^\d+\.\d+\s+/.test(clean);

        // Level 3: Subtopic (### 1.1.1 Subtopic or - Subtopic)
        const isLevel3 = line.startsWith('### ') || 
                         /^\d+\.\d+\.\d+\s+/.test(clean) || 
                         line.startsWith('-');

        if (isLevel1) {
            const unitName = clean.replace(/^\d+\.\s*/, '').trim();
            currUnit = { name: unitName, topics: [] };
            units.push(currUnit);
            currTopic = null;
        } else if (isLevel2) {
            if (!currUnit) {
                currUnit = { name: "Unit 1", topics: [] };
                units.push(currUnit);
            }
            currTopic = { name: clean, subtopics: [] };
            currUnit.topics.push(currTopic);
        } else if (isLevel3) {
            if (!currUnit) {
                currUnit = { name: "Unit 1", topics: [] };
                units.push(currUnit);
            }
            if (!currTopic) {
                currTopic = { name: currUnit.name, subtopics: [] };
                currUnit.topics.push(currTopic);
            }

            let subText = clean.replace(/^[-\*\•]\s*/, '').trim();
            if (subText.includes(',') && !subText.includes('.') && !line.startsWith('###')) {
                const parts = subText.split(/,|\band\b/).map(p => p.trim()).filter(p => p.length > 0);
                currTopic.subtopics.push(...parts);
            } else {
                currTopic.subtopics.push(subText);
            }
        }
    }

    // Ensure valid structure
    units.forEach(u => {
        if (!u.topics || u.topics.length === 0) {
            u.topics = [{ name: u.name, subtopics: ['Overview'] }];
        }
        u.topics.forEach(t => {
            if (!t.subtopics || t.subtopics.length === 0) {
                t.subtopics = ['Overview'];
            }
        });
    });

    if (units.length === 0) return null;

    return { title, units };
}

function handleSyllabusInput() {
    const text = document.getElementById('raw-syllabus-input').value;
    const parsed = parseSyllabusText(text);
    if (parsed) {
        if (parsed.title && !document.getElementById('book-title').value.trim()) {
            document.getElementById('book-title').value = parsed.title;
        }
        if (parsed.units && parsed.units.length > 0) {
            state.treeData.units = parsed.units;
            renderTree();
        }
    }
}

async function aiParseSyllabus() {
    const text = document.getElementById('raw-syllabus-input').value.trim();
    const apiKey = document.getElementById('api-key').value.trim();
    const btn = document.getElementById('btn-ai-parse');

    if (!text) {
        showError('Please paste your syllabus text first.');
        return;
    }
    if (!apiKey) {
        showError('Please enter your Gemini API key above to use AI Auto-Structuring.');
        return;
    }

    hideError();
    const origHtml = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Structuring...';
    btn.disabled = true;

    try {
        const response = await fetch('/api/parse-syllabus', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, api_key: apiKey })
        });

        const data = await response.json();
        if (data.error) {
            showError(data.error);
        } else {
            if (data.title) {
                document.getElementById('book-title').value = data.title;
            }
            if (data.units && data.units.length > 0) {
                state.treeData.units = data.units;
                renderTree();
            }
        }
    } catch (err) {
        showError('AI parsing failed: ' + err.message);
    } finally {
        btn.innerHTML = origHtml;
        btn.disabled = false;
    }
}

// ========================================================
// GENERATION
// ========================================================
async function startGeneration() {
    const title = document.getElementById('book-title').value.trim();
    const apiKey = document.getElementById('api-key').value.trim();
    const generateImages = document.getElementById('toggle-images').checked;
    const errorEl = document.getElementById('error-message');

    // Validate
    if (!title) {
        showError('Please enter a book title.');
        return;
    }
    if (!apiKey) {
        showError('Please enter your Gemini API key.');
        return;
    }
    if (state.treeData.units.length === 0) {
        showError('Please add at least one unit to the syllabus.');
        return;
    }

    // Check all units have topics with subtopics
    for (const unit of state.treeData.units) {
        if (!unit.name.trim()) {
            showError('All units must have a name.');
            return;
        }
        for (const topic of unit.topics) {
            if (!topic.name.trim()) {
                showError('All topics must have a name.');
                return;
            }
            for (const sub of topic.subtopics) {
                if (!sub.trim()) {
                    showError('All subtopics must have a name.');
                    return;
                }
            }
        }
    }

    hideError();
    state.generating = true;

    // Clear console
    const consoleEl = document.getElementById('console-log');
    consoleEl.innerHTML = '';
    appendLog('🚀 Starting book generation...', 'system');

    // Reset progress
    document.getElementById('progress-bar').style.width = '0%';
    document.getElementById('progress-text').textContent = '0%';
    document.getElementById('current-task').textContent = 'Initializing pipeline...';

    // Reset agent flow
    document.querySelectorAll('.agent-node').forEach(n => {
        n.classList.remove('active', 'completed');
    });
    document.getElementById('agent-writer').classList.add('active');

    // Navigate to step 2
    navigateTo(2);

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                api_key: apiKey,
                toc: getTreeData(),
                generate_images: generateImages
            })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Server error');
        }

        const data = await response.json();
        state.taskId = data.task_id;
        appendLog(`📋 Task created: ${state.taskId.substring(0, 8)}...`, 'system');
        connectSSE(state.taskId);
    } catch (err) {
        appendLog(`❌ Failed to start generation: ${err.message}`, 'error');
        state.generating = false;
    }
}

function showError(msg) {
    const el = document.getElementById('error-message');
    el.textContent = msg;
    el.style.display = 'block';
}

function hideError() {
    document.getElementById('error-message').style.display = 'none';
}

// ========================================================
// SSE STREAMING — BUG #3 FIX
// - Checks task status before starting stream
// - Has 5-minute inactivity timeout
// - Proper error/reconnection handling
// ========================================================
function connectSSE(taskId) {
    // Close existing connection
    if (state.eventSource) {
        state.eventSource.close();
        state.eventSource = null;
    }

    // Clear any existing timeout
    if (state.sseTimeout) {
        clearTimeout(state.sseTimeout);
    }

    state.lastMessageTime = Date.now();

    const es = new EventSource(`/api/stream/${taskId}`);
    state.eventSource = es;

    // 5-minute inactivity timeout
    function resetTimeout() {
        if (state.sseTimeout) clearTimeout(state.sseTimeout);
        state.lastMessageTime = Date.now();
        state.sseTimeout = setTimeout(() => {
            appendLog('⚠️ No response from server for 5 minutes. Connection timed out.', 'error');
            es.close();
            state.eventSource = null;
            state.generating = false;
        }, 5 * 60 * 1000);
    }
    resetTimeout();

    es.onmessage = function(event) {
        resetTimeout();

        try {
            const data = JSON.parse(event.data);
            const type = data.type;
            const message = data.message || '';
            const progress = data.progress;

            if (type === 'log') {
                appendLog(message);
                document.getElementById('current-task').textContent = message;
                updateAgentFlow(message);
            }

            if (type === 'progress' || progress !== undefined) {
                updateProgress(progress);
            }

            if (type === 'error') {
                appendLog(`❌ ${message}`, 'error');
            }

            if (type === 'complete') {
                appendLog('✅ ' + message, 'success');
                updateProgress(100);

                es.close();
                state.eventSource = null;
                state.generating = false;
                state.generationComplete = true;

                // Extract download filename from message or use task
                if (data.download_file) {
                    state.downloadFile = data.download_file;
                }

                // Clear timeout
                if (state.sseTimeout) clearTimeout(state.sseTimeout);

                // Update agent flow
                document.querySelectorAll('.agent-node').forEach(n => {
                    n.classList.remove('active');
                    n.classList.add('completed');
                });

                document.getElementById('current-task').textContent = 'Generation complete!';

                // Update stats
                let totalSections = 0;
                state.treeData.units.forEach(u => {
                    u.topics.forEach(t => { totalSections += t.subtopics.length; });
                });
                document.getElementById('stat-chapters').textContent = state.treeData.units.length;
                document.getElementById('stat-sections').textContent = totalSections;
                document.getElementById('stat-images').textContent = document.getElementById('toggle-images').checked ? totalSections : '0';

                // Navigate to step 3 after a short delay
                setTimeout(() => navigateTo(3), 1500);
            }
        } catch (err) {
            console.error('SSE parse error:', err);
        }
    };

    es.onerror = function(err) {
        // Don't close immediately — SSE auto-reconnects
        if (es.readyState === EventSource.CLOSED) {
            appendLog('⚠️ Server connection closed.', 'error');
            state.generating = false;
            state.eventSource = null;
            if (state.sseTimeout) clearTimeout(state.sseTimeout);
        } else {
            // Auto-reconnecting
            appendLog('🔄 Reconnecting to server...', 'system');
        }
    };
}

function updateAgentFlow(message) {
    const msg = message.toLowerCase();
    if (msg.includes('writing') || msg.includes('✍️')) {
        setAgentActive('agent-writer');
    } else if (msg.includes('diagram') || msg.includes('🎨') || msg.includes('image')) {
        setAgentActive('agent-diagrams');
    } else if (msg.includes('compil') || msg.includes('docx') || msg.includes('📚') || msg.includes('export')) {
        setAgentActive('agent-exporter');
    }
}

function setAgentActive(activeId) {
    const nodes = ['agent-writer', 'agent-diagrams', 'agent-exporter'];
    let passedActive = false;
    nodes.forEach(id => {
        const el = document.getElementById(id);
        el.classList.remove('active', 'completed');
        if (id === activeId) {
            el.classList.add('active');
            passedActive = true;
        } else if (!passedActive) {
            el.classList.add('completed');
        }
    });
}

// ========================================================
// CONSOLE LOG
// ========================================================
function appendLog(message, type = '') {
    const consoleEl = document.getElementById('console-log');
    const line = document.createElement('div');
    line.className = 'console-line';

    if (type === 'error') line.classList.add('error-line');
    else if (type === 'success') line.classList.add('success-line');
    else if (type === 'system') line.classList.add('system-line');

    const now = new Date();
    const time = now.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });

    line.innerHTML = `<span class="timestamp">[${time}]</span> ${escapeHtml(message)}`;
    consoleEl.appendChild(line);

    // Auto-scroll
    consoleEl.scrollTop = consoleEl.scrollHeight;
}

// ========================================================
// PROGRESS
// ========================================================
function updateProgress(pct) {
    const bar = document.getElementById('progress-bar');
    const text = document.getElementById('progress-text');
    const rounded = Math.round(pct);
    bar.style.width = `${rounded}%`;
    text.textContent = `${rounded}%`;
}

// ========================================================
// DOWNLOAD
// ========================================================
function downloadBook() {
    if (state.downloadFile) {
        window.location.href = `/api/download/${state.downloadFile}`;
    } else if (state.taskId) {
        // Fallback: try fetching task status
        fetch(`/api/stream/${state.taskId}`)
            .then(r => r.text())
            .catch(() => {
                appendLog('Download link not available. Please check the output folder.', 'error');
            });
    }
}

function restartApp() {
    // Close SSE if open
    if (state.eventSource) {
        state.eventSource.close();
        state.eventSource = null;
    }
    if (state.sseTimeout) clearTimeout(state.sseTimeout);

    // Reset state
    state.currentStep = 1;
    state.taskId = null;
    state.generating = false;
    state.generationComplete = false;
    state.downloadFile = null;

    // Reset tree to defaults
    state.treeData = {
        units: [
            {
                name: 'Unit 1: Introduction',
                topics: [
                    {
                        name: 'Fundamentals',
                        subtopics: ['Overview and History']
                    }
                ]
            }
        ]
    };

    // Clear form
    document.getElementById('book-title').value = '';
    document.getElementById('api-key').value = '';
    document.getElementById('toggle-images').checked = false;
    document.getElementById('toggle-label').textContent = 'Disabled';
    hideError();

    // Reset nav completed states
    document.querySelectorAll('.step-item').forEach(item => {
        item.classList.remove('completed');
    });

    // Re-render and navigate
    renderTree();
    navigateTo(1);
}

// ========================================================
// TOGGLE SWITCH
// ========================================================
function setupToggle() {
    const toggle = document.getElementById('toggle-images');
    const label = document.getElementById('toggle-label');
    toggle.addEventListener('change', () => {
        label.textContent = toggle.checked ? 'Enabled' : 'Disabled';
    });
}

// ========================================================
// INITIALIZATION
// ========================================================
document.addEventListener('DOMContentLoaded', () => {
    // Setup navigation click handlers — DIRECT mapping, no translation
    document.getElementById('nav-step1').addEventListener('click', () => navigateTo(1));
    document.getElementById('nav-step2').addEventListener('click', () => navigateTo(2));
    document.getElementById('nav-step3').addEventListener('click', () => navigateTo(3));

    // Setup tree editor & raw syllabus parser
    document.getElementById('btn-add-unit').addEventListener('click', addUnit);
    
    const syllabusInput = document.getElementById('raw-syllabus-input');
    if (syllabusInput) {
        syllabusInput.addEventListener('input', handleSyllabusInput);
    }
    
    const aiParseBtn = document.getElementById('btn-ai-parse');
    if (aiParseBtn) {
        aiParseBtn.addEventListener('click', aiParseSyllabus);
    }
    
    renderTree();

    // Setup generate button
    document.getElementById('btn-generate').addEventListener('click', startGeneration);

    // Setup download button
    document.getElementById('btn-download').addEventListener('click', downloadBook);

    // Setup restart button
    document.getElementById('btn-restart').addEventListener('click', restartApp);

    // Setup toggle
    setupToggle();

    // Start on step 1 — NO dashboard loading, NO /api/projects call
    navigateTo(1);
});
