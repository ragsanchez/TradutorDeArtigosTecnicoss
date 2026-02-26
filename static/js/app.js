class TechnicalTranslator {
    constructor() {
        this.initializeEventListeners();
        this.updateWordCount();
    }

    initializeEventListeners() {
        document.getElementById('translateBtn').addEventListener('click', () => {
            this.translateText();
        });

        document.getElementById('clearBtn').addEventListener('click', () => {
            this.clearTexts();
        });

        document.getElementById('pasteBtn').addEventListener('click', () => {
            this.pasteFromClipboard();
        });

        document.getElementById('uploadBtn').addEventListener('click', () => {
            this.showUploadModal();
        });

        document.getElementById('copyBtn').addEventListener('click', () => {
            this.copyToClipboard();
        });

        document.getElementById('downloadBtn').addEventListener('click', () => {
            this.downloadTranslation();
        });

        document.getElementById('processFileBtn').addEventListener('click', () => {
            this.processUploadedFile();
        });

        document.getElementById('historyBtn').addEventListener('click', () => {
            this.showHistory();
        });

        document.getElementById('clearHistoryBtn').addEventListener('click', () => {
            this.clearHistory();
            this.showHistory();
        });

        document.getElementById('sourceText').addEventListener('input', () => {
            this.updateWordCount();
        });

        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case 'Enter':
                        e.preventDefault();
                        this.translateText();
                        break;
                    case 'k':
                        e.preventDefault();
                        this.clearTexts();
                        break;
                }
            }
        });
    }

    async translateText() {
        const sourceText = document.getElementById('sourceText').value.trim();
        const sourceLanguage = document.getElementById('sourceLanguage').value;
        const targetLanguage = document.getElementById('targetLanguage').value;
        const preserveFormatting = document.getElementById('preserveFormatting').checked;

        if (!sourceText) {
            this.showAlert('Por favor, insira um texto para traduzir.', 'warning');
            return;
        }

        this.showProgressBar(true);
        this.setTranslateButtonState(true);

        try {
            const response = await fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: sourceText,
                    source_language: sourceLanguage,
                    target_language: targetLanguage,
                    preserve_formatting: preserveFormatting
                })
            });

            const data = await response.json();

            if (response.ok) {
                document.getElementById('translatedText').textContent = data.translated_text;
                document.getElementById('translationTime').textContent = `${data.translation_time}s`;
                
                // Salva no histórico
                this.saveToHistory({
                    original: sourceText,
                    translated: data.translated_text,
                    sourceLang: sourceLanguage,
                    targetLang: targetLanguage,
                    timestamp: new Date().toISOString(),
                    time: data.translation_time
                });
                
                this.showAlert('Tradução concluída com sucesso!', 'success');
            } else {
                throw new Error(data.error || 'Erro na tradução');
            }
        } catch (error) {
            console.error('Erro na tradução:', error);
            this.showAlert(`Erro na tradução: ${error.message}`, 'danger');
        } finally {
            this.showProgressBar(false);
            this.setTranslateButtonState(false);
        }
    }

    clearTexts() {
        if (confirm('Tem certeza que deseja limpar todos os textos?')) {
            document.getElementById('sourceText').value = '';
            document.getElementById('translatedText').textContent = '';
            document.getElementById('translationTime').textContent = '-';
            this.updateWordCount();
            this.showAlert('Textos limpos com sucesso!', 'info');
        }
    }

    async pasteFromClipboard() {
        try {
            const text = await navigator.clipboard.readText();
            document.getElementById('sourceText').value = text;
            this.updateWordCount();
            this.showAlert('Texto colado com sucesso!', 'success');
        } catch (error) {
            console.error('Erro ao colar texto:', error);
            this.showAlert('Erro ao colar texto. Tente usar Ctrl+V.', 'warning');
        }
    }

    async copyToClipboard() {
        const translatedText = document.getElementById('translatedText').textContent;
        if (!translatedText.trim()) {
            this.showAlert('Nenhum texto traduzido para copiar.', 'warning');
            return;
        }

        try {
            await navigator.clipboard.writeText(translatedText);
            this.showAlert('Texto copiado para a área de transferência!', 'success');
        } catch (error) {
            console.error('Erro ao copiar texto:', error);
            this.showAlert('Erro ao copiar texto.', 'danger');
        }
    }

    downloadTranslation() {
        const translatedText = document.getElementById('translatedText').textContent;
        if (!translatedText.trim()) {
            this.showAlert('Nenhum texto traduzido para download.', 'warning');
            return;
        }

        const blob = new Blob([translatedText], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `traducao_${new Date().toISOString().slice(0, 10)}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        this.showAlert('Download iniciado!', 'success');
    }

    showUploadModal() {
        const modal = new bootstrap.Modal(document.getElementById('uploadModal'));
        modal.show();
    }

    async processUploadedFile() {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];

        if (!file) {
            this.showAlert('Por favor, selecione um arquivo.', 'warning');
            return;
        }

        try {
            const text = await this.readFileContent(file);
            document.getElementById('sourceText').value = text;
            this.updateWordCount();
            
            const modal = bootstrap.Modal.getInstance(document.getElementById('uploadModal'));
            modal.hide();
            
            this.showAlert('Arquivo carregado com sucesso!', 'success');
        } catch (error) {
            console.error('Erro ao processar arquivo:', error);
            this.showAlert('Erro ao processar arquivo.', 'danger');
        }
    }

    readFileContent(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            
            if (file.type === 'text/plain' || file.name.endsWith('.txt') || file.name.endsWith('.md')) {
                reader.readAsText(file, 'UTF-8');
            } else {
                reject(new Error('Formato de arquivo não suportado'));
            }
        });
    }

    updateWordCount() {
        const text = document.getElementById('sourceText').value;
        const charCount = text.length;
        const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
        
        document.getElementById('charCount').textContent = charCount.toLocaleString('pt-BR');
        document.getElementById('wordCount').textContent = wordCount.toLocaleString('pt-BR');
    }

    showProgressBar(show) {
        const progressBar = document.getElementById('progressBar');
        progressBar.style.display = show ? 'block' : 'none';
    }

    setTranslateButtonState(loading) {
        const btn = document.getElementById('translateBtn');
        if (loading) {
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Traduzindo...';
            btn.classList.add('loading');
        } else {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-exchange-alt me-2"></i>Traduzir';
            btn.classList.remove('loading');
        }
    }

    showAlert(message, type = 'info') {
        const alertContainer = document.getElementById('alertContainer');
        const alertId = 'alert-' + Date.now();
        
        const alertHtml = `
            <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas fa-${this.getAlertIcon(type)} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        alertContainer.insertAdjacentHTML('beforeend', alertHtml);
        
        setTimeout(() => {
            const alert = document.getElementById(alertId);
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    }

    getAlertIcon(type) {
        const icons = {
            'success': 'check-circle',
            'danger': 'exclamation-triangle',
            'warning': 'exclamation-circle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    saveToHistory(translation) {
        try {
            let history = JSON.parse(localStorage.getItem('translationHistory') || '[]');
            
            // Adiciona no início
            history.unshift(translation);
            
            // Mantém apenas os últimos 50 itens
            if (history.length > 50) {
                history = history.slice(0, 50);
            }
            
            localStorage.setItem('translationHistory', JSON.stringify(history));
        } catch (error) {
            console.error('Erro ao salvar histórico:', error);
        }
    }

    getHistory() {
        try {
            return JSON.parse(localStorage.getItem('translationHistory') || '[]');
        } catch (error) {
            console.error('Erro ao carregar histórico:', error);
            return [];
        }
    }

    clearHistory() {
        if (confirm('Tem certeza que deseja limpar todo o histórico de traduções?')) {
            localStorage.removeItem('translationHistory');
            this.showAlert('Histórico limpo com sucesso!', 'success');
        }
    }

    loadFromHistory(item) {
        document.getElementById('sourceText').value = item.original;
        document.getElementById('translatedText').textContent = item.translated;
        document.getElementById('sourceLanguage').value = item.sourceLang;
        document.getElementById('targetLanguage').value = item.targetLang;
        document.getElementById('translationTime').textContent = `${item.time}s`;
        this.updateWordCount();
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('historyModal'));
        modal.hide();
        
        this.showAlert('Tradução carregada do histórico!', 'info');
    }

    showHistory() {
        const history = this.getHistory();
        const historyList = document.getElementById('historyList');
        
        if (history.length === 0) {
            historyList.innerHTML = '<p class="text-center text-muted">Nenhuma tradução no histórico</p>';
            return;
        }
        
        const languages = {
            'pt': 'Português',
            'en': 'Inglês',
            'es': 'Espanhol',
            'fr': 'Francês',
            'de': 'Alemão',
            'it': 'Italiano',
            'ru': 'Russo',
            'ja': 'Japonês',
            'ko': 'Coreano',
            'zh': 'Chinês',
            'ar': 'Árabe',
            'auto': 'Auto'
        };
        
        historyList.innerHTML = history.map((item, index) => {
            const date = new Date(item.timestamp);
            const dateStr = date.toLocaleString('pt-BR');
            const sourceLang = languages[item.sourceLang] || item.sourceLang;
            const targetLang = languages[item.targetLang] || item.targetLang;
            const preview = item.original.substring(0, 100) + (item.original.length > 100 ? '...' : '');
            
            return `
                <div class="card mb-2 border-start border-4 border-primary">
                    <div class="card-body p-3">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <div>
                                <small class="text-muted">
                                    <i class="fas fa-exchange-alt me-1"></i>
                                    ${sourceLang} → ${targetLang}
                                </small>
                                <br>
                                <small class="text-muted">
                                    <i class="fas fa-clock me-1"></i>
                                    ${dateStr} • ${item.time}s
                                </small>
                            </div>
                            <button class="btn btn-sm btn-outline-primary load-history-btn" data-index="${index}">
                                <i class="fas fa-arrow-left me-1"></i>Carregar
                            </button>
                        </div>
                        <p class="mb-0 small text-muted" style="max-height: 60px; overflow: hidden;">
                            ${preview}
                        </p>
                    </div>
                </div>
            `;
        }).join('');
        
        // Adiciona event listeners para os botões
        historyList.querySelectorAll('.load-history-btn').forEach((btn, index) => {
            btn.addEventListener('click', () => {
                this.loadFromHistory(history[index]);
            });
        });
    }
}

let translator;

document.addEventListener('DOMContentLoaded', () => {
    translator = new TechnicalTranslator();
    
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            if (!data.azure_configured) {
                translator.showAlert('Azure Translator não configurado. Verifique as variáveis de ambiente.', 'warning');
            }
        })
        .catch(error => {
            console.error('Erro ao verificar status:', error);
        });
});
