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
}

document.addEventListener('DOMContentLoaded', () => {
    new TechnicalTranslator();
    
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            if (!data.azure_configured) {
                const translator = new TechnicalTranslator();
                translator.showAlert('Azure Translator não configurado. Verifique as variáveis de ambiente.', 'warning');
            }
        })
        .catch(error => {
            console.error('Erro ao verificar status:', error);
        });
});
