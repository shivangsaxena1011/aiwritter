document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const navItems = {
        dashboard: document.getElementById("nav-dashboard"),
        step1: document.getElementById("nav-step1"),
        step2: document.getElementById("nav-step2"),
        step3: document.getElementById("nav-step3"),
        step4: document.getElementById("nav-step4")
    };

    const sections = {
        dashboard: document.getElementById("section-dashboard"),
        credentials: document.getElementById("section-credentials"),
        tocReview: document.getElementById("section-toc-review"),
        orchestrator: document.getElementById("section-orchestrator"),
        export: document.getElementById("section-export")
    };

    const inputs = {
        syllabus: document.getElementById("syllabus-input"),
        openaiKey: document.getElementById("openai-key"),
        geminiKey: document.getElementById("gemini-key"),
        chapterCount: document.getElementById("chapter-count"),
        bookTitle: document.getElementById("book-title-input")
    };

    const buttons = {
        createNewProject: document.getElementById("btn-create-new-project"),
        generateToc: document.getElementById("btn-generate-toc"),
        backToStep1: document.getElementById("btn-back-to-step1"),
        startWriting: document.getElementById("btn-start-writing"),
        restart: document.getElementById("btn-restart"),
        downloadDocx: document.getElementById("link-download-docx"),
        downloadPdf: document.getElementById("link-download-pdf"),
        closeVersionModal: document.getElementById("btn-close-version-modal"),
        closeVersionModalBtn: document.getElementById("btn-close-version-modal-btn")
    };

    const containers = {
        projectsGrid: document.getElementById("projects-grid"),
        tocTree: document.getElementById("toc-tree"),
        consoleLogs: document.getElementById("console-logs"),
        livePreview: document.getElementById("live-preview"),
        progressBar: document.getElementById("progress-bar"),
        progressText: document.getElementById("progress-text"),
        systemStatus: document.getElementById("system-status"),
        versionListContainer: document.getElementById("version-list-container")
    };

    const modals = {
        loading: document.getElementById("loading-modal"),
        loadingTitle: document.getElementById("loading-title"),
        loadingMsg: document.getElementById("loading-msg"),
        versionHistory: document.getElementById("version-history-modal"),
        versionModalTitle: document.getElementById("version-modal-title")
    };

    // State Variables
    let activeSlug = null;
    let plannedTocData = null;
    let eventSource = null;

    // Navigation Switcher
    function navigateTo(sectionName) {
        Object.values(sections).forEach(sec => sec.classList.remove("active"));
        Object.values(navItems).forEach(item => item.classList.remove("active"));

        if (sections[sectionName]) sections[sectionName].classList.add("active");
        if (navItems[sectionName]) navItems[sectionName].classList.add("active");

        if (sectionName === "dashboard") {
            loadProjectsDashboard();
        }
    }

    Object.keys(navItems).forEach(key => {
        navItems[key].addEventListener("click", () => navigateTo(key));
    });

    if (buttons.createNewProject) {
        buttons.createNewProject.addEventListener("click", () => {
            activeSlug = null;
            plannedTocData = null;
            inputs.syllabus.value = "";
            navigateTo("step1");
        });
    }

    // Projects Dashboard Loading
    async function loadProjectsDashboard() {
        if (!containers.projectsGrid) return;
        containers.projectsGrid.innerHTML = '<div class="console-line">[System] Loading projects dashboard...</div>';

        try {
            const res = await fetch("/api/projects");
            if (!res.ok) throw new Error("Failed to load projects");
            const projects = await res.json();

            if (projects.length === 0) {
                containers.projectsGrid.innerHTML = `
                    <div class="glass-card full-width text-center" style="grid-column: 1 / -1; padding: 3rem;">
                        <i class="fa-solid fa-book-open-reader" style="font-size: 2.5rem; color: var(--accent-blue); margin-bottom: 1rem;"></i>
                        <h4>No Textbook Projects Found</h4>
                        <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">Start by creating your first university-grade textbook project.</p>
                        <button class="btn btn-primary" id="btn-empty-create"><i class="fa-solid fa-plus"></i> Create First Project</button>
                    </div>
                `;
                document.getElementById("btn-empty-create")?.addEventListener("click", () => {
                    activeSlug = null;
                    navigateTo("step1");
                });
                return;
            }

            containers.projectsGrid.innerHTML = projects.map(p => `
                <div class="project-card">
                    <div>
                        <div class="project-card-header">
                            <span class="project-card-title">${escapeHtml(p.book_name || "Untitled Textbook")}</span>
                            <span class="project-state-badge ${p.state || 'draft'}">${p.state || 'draft'}</span>
                        </div>
                        <div class="project-card-body">
                            <div class="project-meta-row">
                                <span>Version: v${p.version || '1.0.0'}</span>
                                <span>Progress: ${p.progress || 0}%</span>
                            </div>
                            <div class="project-progress-bar">
                                <div class="project-progress-fill" style="width: ${p.progress || 0}%;"></div>
                            </div>
                        </div>
                    </div>
                    <div class="project-card-actions">
                        <button class="btn btn-secondary btn-block btn-resume-project" data-slug="${p.slug}">
                            <i class="fa-solid fa-play"></i> Open / Resume
                        </button>
                        <button class="btn btn-outline btn-history-project" data-slug="${p.slug}" title="View Exports">
                            <i class="fa-solid fa-history"></i>
                        </button>
                    </div>
                </div>
            `).join("");

            document.querySelectorAll(".btn-resume-project").forEach(btn => {
                btn.addEventListener("click", (e) => {
                    const slug = e.currentTarget.getAttribute("data-slug");
                    resumeProject(slug);
                });
            });

            document.querySelectorAll(".btn-history-project").forEach(btn => {
                btn.addEventListener("click", (e) => {
                    const slug = e.currentTarget.getAttribute("data-slug");
                    showVersionHistory(slug);
                });
            });

        } catch (err) {
            containers.projectsGrid.innerHTML = `<div class="console-line style="color: var(--danger)">Failed to load projects: ${err.message}</div>`;
        }
    }

    async function resumeProject(slug) {
        showLoading("Loading Project", "Fetching project metadata and workspace state...");
        try {
            const res = await fetch(`/api/projects/${slug}`);
            if (!res.ok) throw new Error("Could not fetch project details");
            const project = await res.json();
            hideLoading();

            activeSlug = slug;
            plannedTocData = project.toc_data || null;

            if (project.state === "exported" || project.progress >= 100) {
                const docxUrl = `/api/projects/${slug}/export/docx`;
                buttons.downloadDocx.href = docxUrl;
                navigateTo("export");
            } else if (project.progress > 0) {
                navigateTo("step3");
                startEventStream(slug);
            } else if (plannedTocData) {
                inputs.bookTitle.value = plannedTocData.title || "";
                renderTocTree(plannedTocData);
                navigateTo("step2");
            } else {
                inputs.syllabus.value = project.syllabus || "";
                navigateTo("step1");
            }
        } catch (err) {
            hideLoading();
            alert(`Error: ${err.message}`);
        }
    }

    async function showVersionHistory(slug) {
        try {
            const res = await fetch(`/api/projects/${slug}`);
            if (!res.ok) throw new Error("Could not fetch project history");
            const project = await res.json();

            modals.versionModalTitle.textContent = `${project.book_name} - Export History`;
            const history = project.export_history || [];

            if (history.length === 0) {
                containers.versionListContainer.innerHTML = '<p style="color: var(--text-secondary);">No exports compiled yet for this project.</p>';
            } else {
                containers.versionListContainer.innerHTML = history.map(h => `
                    <div style="background: rgba(255,255,255,0.04); border: 1px solid var(--border-color); border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: var(--accent-blue);">Edition v${h.version}</strong>
                            <div style="font-size: 0.75rem; color: var(--text-secondary);">${new Date(h.exported_at).toLocaleString()}</div>
                        </div>
                        <a href="${h.docx_url}" class="btn btn-primary" style="padding: 0.4rem 0.8rem; font-size: 0.8rem;" download>
                            <i class="fa-solid fa-download"></i> Download Word
                        </a>
                    </div>
                `).join("");
            }

            modals.versionHistory.classList.add("active");
        } catch (err) {
            alert(`Error: ${err.message}`);
        }
    }

    if (buttons.closeVersionModal) buttons.closeVersionModal.addEventListener("click", () => modals.versionHistory.classList.remove("active"));
    if (buttons.closeVersionModalBtn) buttons.closeVersionModalBtn.addEventListener("click", () => modals.versionHistory.classList.remove("active"));

    // Step 1: Generate TOC
    if (buttons.generateToc) {
        buttons.generateToc.addEventListener("click", async () => {
            const syllabus = inputs.syllabus.value.trim();
            if (!syllabus) {
                alert("Please enter a syllabus or topic guidelines first.");
                return;
            }

            showLoading("Planning Table of Contents", "Structuring curriculum chapters using AI agents...");

            try {
                const res = await fetch("/api/plan-toc", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        syllabus: syllabus,
                        target_chapters: parseInt(inputs.chapterCount.value) || 5,
                        openai_key: inputs.openaiKey.value.trim(),
                        gemini_key: inputs.geminiKey.value.trim()
                    })
                });

                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.detail || "Failed to plan TOC");
                }

                plannedTocData = await res.json();
                hideLoading();

                inputs.bookTitle.value = plannedTocData.title || "Academic Textbook";
                renderTocTree(plannedTocData);
                navigateTo("step2");
            } catch (err) {
                hideLoading();
                alert(`Error: ${err.message}`);
            }
        });
    }

    function renderTocTree(toc) {
        if (!containers.tocTree) return;
        const chapters = toc.chapters || [];
        containers.tocTree.innerHTML = chapters.map(ch => `
            <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                <h4 style="color: var(--accent-blue); margin-bottom: 0.5rem;">Chapter ${ch.chapter_number}: ${escapeHtml(ch.title)}</h4>
                <ul style="padding-left: 1.2rem; color: var(--text-secondary); font-size: 0.9rem;">
                    ${(ch.subtopics || []).map(s => `<li>${escapeHtml(s.title)} ${s.needs_diagram ? '<span class="badge" style="background: rgba(139,92,246,0.2); color: var(--accent-purple); font-size: 0.7rem;">+ Diagram</span>' : ''}</li>`).join("")}
                </ul>
            </div>
        `).join("");
    }

    if (buttons.backToStep1) {
        buttons.backToStep1.addEventListener("click", () => navigateTo("step1"));
    }

    // Step 2 -> Step 3: Start Generation Pipeline
    if (buttons.startWriting) {
        buttons.startWriting.addEventListener("click", async () => {
            if (!plannedTocData) return;

            plannedTocData.title = inputs.bookTitle.value.trim() || plannedTocData.title;

            showLoading("Initializing Workspace", "Setting up multi-book project structure...");

            try {
                const res = await fetch("/api/generate-textbook", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        toc_data: plannedTocData,
                        openai_key: inputs.openaiKey.value.trim(),
                        gemini_key: inputs.geminiKey.value.trim(),
                        slug: activeSlug,
                        syllabus: inputs.syllabus.value.trim()
                    })
                });

                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.detail || "Failed to start textbook generation");
                }

                const data = await res.json();
                activeSlug = data.task_id;
                hideLoading();

                navigateTo("step3");
                startEventStream(activeSlug);
            } catch (err) {
                hideLoading();
                alert(`Error starting pipeline: ${err.message}`);
            }
        });
    }

    // EventSource Progress Stream
    function startEventStream(taskId) {
        if (eventSource) eventSource.close();

        containers.consoleLogs.innerHTML = "";
        containers.livePreview.innerHTML = '<div class="preview-placeholder"><i class="fa-solid fa-scroll"></i><p>Connecting to content writer stream...</p></div>';

        eventSource = new EventSource(`/api/stream-progress/${taskId}`);

        eventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);

                if (data.type === "log") {
                    appendConsoleLog(data.message);
                    updateLivePreviewFromLogs(data.message);
                } else if (data.type === "progress") {
                    updateProgress(data.percent, data.status);
                } else if (data.type === "completion") {
                    eventSource.close();
                    if (data.status === "COMPLETED") {
                        buttons.downloadDocx.href = data.docx_url || `/api/projects/${taskId}/export/docx`;
                        navigateTo("export");
                    } else {
                        alert("Textbook generation encountered an issue.");
                    }
                }
            } catch (e) {
                console.error("SSE parse error", e);
            }
        };

        eventSource.onerror = (err) => {
            console.error("EventSource failed:", err);
            eventSource.close();
        };
    }

    function appendConsoleLog(msg) {
        if (!containers.consoleLogs) return;
        const line = document.createElement("div");
        line.className = "console-line";
        line.textContent = msg;
        containers.consoleLogs.appendChild(line);
        containers.consoleLogs.scrollTop = containers.consoleLogs.scrollHeight;
    }

    function updateLivePreviewFromLogs(msg) {
        if (msg.includes("Writing Chapter") || msg.includes("Writing Subtopic:")) {
            const paper = containers.livePreview.querySelector(".preview-paper") || document.createElement("div");
            if (!paper.classList.contains("preview-paper")) {
                paper.className = "preview-paper";
                containers.livePreview.innerHTML = "";
                containers.livePreview.appendChild(paper);
            }
            const paragraph = document.createElement("p");
            paragraph.textContent = msg;
            paper.appendChild(paragraph);
            containers.livePreview.scrollTop = containers.livePreview.scrollHeight;
        }
    }

    function updateProgress(percent, status) {
        if (containers.progressBar) containers.progressBar.style.width = `${percent}%`;
        if (containers.progressText) containers.progressText.textContent = `${percent}%`;

        if (containers.systemStatus) {
            const text = containers.systemStatus.querySelector(".status-text");
            if (text) text.textContent = status || "Processing";
            containers.systemStatus.classList.add("active");
        }
    }

    function showLoading(title, msg) {
        if (modals.loadingTitle) modals.loadingTitle.textContent = title;
        if (modals.loadingMsg) modals.loadingMsg.textContent = msg;
        if (modals.loading) modals.loading.classList.add("active");
    }

    function hideLoading() {
        if (modals.loading) modals.loading.classList.remove("active");
    }

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }

    if (buttons.restart) {
        buttons.restart.addEventListener("click", () => {
            activeSlug = null;
            navigateTo("dashboard");
        });
    }

    // Initial Load
    loadProjectsDashboard();
});
