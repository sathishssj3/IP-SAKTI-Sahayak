import React, { useState, useEffect, useRef } from 'react';
import {
  MessageSquare,
  Bot,
  Scale,
  Send,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  X,
  Minimize2,
  Maximize2,
  RotateCcw,
  Shield,
  FileText,
  ExternalLink,
  ChevronRight,
  Info,
  CheckCircle2,
  HelpCircle,
} from 'lucide-react';

const SUGGESTIONS = [
  { label: 'What is Section 3(p)?', query: 'What is Section 3(p) of the Patents Act and how does TKDL protect traditional knowledge?' },
  { label: 'Section 3(e) & Chou-Talalay Synergy', query: 'Explain Section 3(e) mere admixture bar and how Chou-Talalay Combination Index (CI < 1.0) overcomes it.' },
  { label: 'NBA Form III Approval', query: 'When is National Biodiversity Authority (NBA) Form III clearance required before applying for a patent?' },
  { label: 'Ayurveda Aahara (FSSAI 2022)', query: 'What are the regulatory guidelines for marketing Ayurveda Aahara under FSSAI 2022?' },
  { label: 'Can Haridra + Maricha be patented?', query: 'Can I patent a formulation of Haridra (Turmeric) and Maricha (Black Pepper) if bioavailability is enhanced?' },
  { label: 'General Patenting Criteria', query: 'What are the fundamental requirements for patentability: novelty, inventive step, and industrial applicability?' },
  { label: 'WIPO GRATK Treaty 2024', query: 'What does the WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (2024) mandate?' },
  { label: 'About this Project & SIH', query: 'What is the IP-SAKTI Sahayak platform, what problem does it solve for Ministry of Ayush, and who built it?' },
];

const LOCALIZED_LABELS = {
  en: {
    title: 'Sahayak Legal Guidance Desk',
    subtitle: 'Statutory IP & Ayush Regulatory Intelligence',
    status: 'Statutory Database Online',
    placeholder: 'Ask about § 3(p), synergy, botanicals, export...',
    ask_suggestions: 'Suggested Queries',
    clear: 'Clear conversation',
    close: 'Close assistant',
    minimize: 'Minimize',
    maximize: 'Expand',
    stop_tts: 'Stop reading',
    listen: 'Listen response',
    offline_notice: 'Offline mode active. Statutory fallback loaded.',
  },
  hi: {
    title: 'सहायक एआई विधिक सलाहकार',
    subtitle: 'सांविधिक बौद्धिक संपदा एवं आयुष प्रज्ञान',
    status: 'आरएजी एवं भाषिणी सक्रिय',
    placeholder: 'धारा 3(p), सिनर्जी, औषधियां, पेटेंट पर पूछें...',
    ask_suggestions: 'सुझाए गए प्रश्न',
    clear: 'संवाद साफ़ करें',
    close: 'सहायक बंद करें',
    minimize: 'छोटा करें',
    maximize: 'बड़ा करें',
    stop_tts: 'आवाज रोकें',
    listen: 'उत्तर सुनें',
    offline_notice: 'ऑफलाइन मोड सक्रिय। सांविधिक संग्रह लोड है।',
  },
  sa: {
    title: 'सहायक एआई विधि-परामर्शकः',
    subtitle: 'सांविधिक बौद्धिक सम्पदा एवं आयुर्वेद प्रज्ञानम्',
    status: 'सक्रियम्',
    placeholder: 'धारा ३(p), सम्मिश्रण-नियम, पेटेंट विषये पृच्छन्तु...',
    ask_suggestions: 'प्रश्नावलिः',
    clear: 'पुनः आरम्भः',
    close: 'पिदधातु',
    minimize: 'लघु करोतु',
    maximize: 'विस्तारयतु',
    stop_tts: 'वाणीं स्थगयतु',
    listen: 'उत्तरं शृणोतु',
    offline_notice: 'स्थानीय कोशः सक्रियः।',
  },
  ta: {
    title: 'சஹாயக் AI சட்ட ஆலோசகர்',
    subtitle: 'சட்டரீதியான ஐபி & ஆயுஷ் நுண்ணறிவு',
    status: 'நேரலையில் உள்ளது',
    placeholder: 'பிரிவு 3(p), காப்புரிமை, ஆயுர்வேத மூலிகைகள் பற்றி கேட்கவும்...',
    ask_suggestions: 'பரிந்துரைக்கப்பட்ட கேள்விகள்',
    clear: 'அரட்டையை அழிக்கவும்',
    close: 'மூடு',
    minimize: 'சுருக்கு',
    maximize: 'விரிவாக்கு',
    stop_tts: 'குரலை நிறுத்து',
    listen: 'பதிலைக் கேளுங்கள்',
    offline_notice: 'ஆஃப்லைன் முறை செயலில் உள்ளது.',
  },
  te: {
    title: 'సహాయక్ AI చట్టపరమైన అసిస్టెంట్',
    subtitle: 'చట్టబద్ధమైన IP & ఆయుష్ నిఘా',
    status: 'యాక్టివ్',
    placeholder: 'సెక్షన్ 3(p), పేటెంట్లు, మూలికల గురించి అడగండి...',
    ask_suggestions: 'సూచించిన ప్రశ్నలు',
    clear: 'చాట్ తొలగించు',
    close: 'మూసివేయి',
    minimize: 'కుదించు',
    maximize: 'విస్తరించు',
    stop_tts: 'వాయిస్ ఆపు',
    listen: 'సమాధానం వినండి',
    offline_notice: 'ఆఫ్‌లైన్ మోడ్ యాక్టివ్‌గా ఉంది.',
  },
  mr: {
    title: 'सहायक एआय कायदेशीर सल्लागार',
    subtitle: 'वैधानिक आयपी आणि आयुष बुद्धिमत्ता',
    status: 'सक्रिय',
    placeholder: 'कलम 3(p), सिनर्जी, औषधी वनस्पती, पेटंट बद्दल विचारा...',
    ask_suggestions: 'सुचवलेले प्रश्न',
    clear: 'संवाद साफ करा',
    close: 'बंद करा',
    minimize: 'लहान करा',
    maximize: 'मोठे करा',
    stop_tts: 'आवाज थांबवा',
    listen: 'उत्तर ऐका',
    offline_notice: 'ऑफलाइन मोड सक्रिय.',
  },
  bn: {
    title: 'সহায়ক এআই আইনি সহকারী',
    subtitle: 'বিধিবদ্ধ আইপি এবং আয়ুষ বুদ্ধিমত্তা',
    status: 'সক্রিয়',
    placeholder: 'ধারা ৩(p), পেটেন্ট, ভেষজ সম্পর্কে জিজ্ঞাসা করুন...',
    ask_suggestions: 'পরামর্শমূলক প্রশ্নাবলী',
    clear: 'চ্যাট সাফ করুন',
    close: 'বন্ধ করুন',
    minimize: 'ছোট করুন',
    maximize: 'বড় করুন',
    stop_tts: 'ভয়েস বন্ধ করুন',
    listen: 'উত্তর শুনুন',
    offline_notice: 'অফলাইন মোড সক্রিয়।',
  },
  gu: {
    title: 'સહાયક AI કાનૂની સહાયક',
    subtitle: 'વૈધાનિક આઈપી અને આયુષ ઇન્ટેલિજન્સ',
    status: 'સક્રિય',
    placeholder: 'કલમ 3(p), સિનર્જી, આયુર્વેદિક પેટન્ટ વિશે પૂછો...',
    ask_suggestions: 'સૂચવેલા પ્રશ્નો',
    clear: 'ચેટ સાફ કરો',
    close: 'બંધ કરો',
    minimize: 'નાનું કરો',
    maximize: 'મોટું કરો',
    stop_tts: 'અવાજ રોકો',
    listen: 'જવાબ સાંભળો',
    offline_notice: 'ઑફલાઇન મોડ સક્રિય.',
  },
};

const INITIAL_MESSAGE = {
  id: 'welcome-1',
  sender: 'assistant',
  text: `### IP-SAKTI Sahayak Statutory Advisory Desk

This advisory service provides statutory cross-referencing across:
- **Patents Act, 1970**: Section 3(p) Traditional Knowledge exclusion, Section 3(e) Mere Admixture bar, and Section 40 Foreign Filing Licenses.
- **Scientific Synergy**: Chou-Talalay Combination Index (CI < 1.0) and in-vitro isobolograms.
- **Biodiversity & Regulations**: Biological Diversity Act Form I–IV, DCA Rule 158B, FSSAI Ayurveda Aahara, Phytopharmaceutical Drugs G.S.R. 918(E), and WIPO GRATK Treaty 2024.
- **Patenting & Ayush Prior Art**: Novelty assessments, prior-art searches, botanical formulations, and export guidelines (US FDA and EU THMPD).

Enter your statutory question or formulation details below to review applicable legal provisions.`,
  citations: ['Patents Act 1970', 'CSIR-TKDL', 'Biological Diversity Act', 'WIPO GRATK 2024'],
  timestamp: Date.now(),
};

// Simple Markdown Formatter for Assistant Responses
function renderFormattedMarkdown(rawText) {
  if (!rawText) return null;
  const lines = rawText.split('\n');

  return (
    <div className="chat-markdown">
      {lines.map((line, idx) => {
        const trimmed = line.trim();
        if (!trimmed) {
          return <div key={idx} style={{ height: '0.45rem' }} />;
        }

        // Headings
        if (trimmed.startsWith('### ')) {
          return (
            <h4 key={idx} className="chat-h3">
              {trimmed.substring(4)}
            </h4>
          );
        }
        if (trimmed.startsWith('## ')) {
          return (
            <h3 key={idx} className="chat-h2">
              {trimmed.substring(3)}
            </h3>
          );
        }

        // Blockquotes
        if (trimmed.startsWith('> ')) {
          return (
            <blockquote key={idx} className="chat-quote">
              {formatInlineText(trimmed.substring(2))}
            </blockquote>
          );
        }

        // Bullet lists
        if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
          return (
            <div key={idx} className="chat-bullet">
              <span className="chat-bullet-dot">•</span>
              <span className="chat-bullet-text">{formatInlineText(trimmed.substring(2))}</span>
            </div>
          );
        }

        // Standard paragraph
        return (
          <p key={idx} className="chat-p">
            {formatInlineText(trimmed)}
          </p>
        );
      })}
    </div>
  );
}

function formatInlineText(text) {
  // Regex to split on bold **text**, code `text`, and statutory sections like § 3(p)
  const parts = text.split(/(\*\*.*?\*\*|`.*?`|§\s*\d+[a-zA-Z]*(?:\([0-9a-zA-Z]+\))*)/g);
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i} className="chat-strong">{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return <code key={i} className="chat-code">{part.slice(1, -1)}</code>;
    }
    if (/^§\s*\d+/.test(part)) {
      return <span key={i} className="chat-statute-tag">{part}</span>;
    }
    return part;
  });
}

export default function Chatbot({ lang = 'en', t }) {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState([INITIAL_MESSAGE]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [speakingId, setSpeakingId] = useState(null);

  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);

  const labels = LOCALIZED_LABELS[lang] || LOCALIZED_LABELS.en;

  // Auto-scroll on message updates
  useEffect(() => {
    if (isOpen && !isMinimized && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen, isMinimized, isLoading]);

  // Clean up TTS when unmounting or closing
  useEffect(() => {
    return () => {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const handleSendMessage = async (textToSend) => {
    const query = (textToSend || inputText).trim();
    if (!query || isLoading) return;

    const userMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: query,
      timestamp: Date.now(),
    };

    const newHistory = [...messages, userMessage];
    setMessages(newHistory);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: query,
          language: lang,
          history: newHistory.slice(-6).map((m) => ({
            sender: m.sender,
            text: m.text,
          })),
        }),
      });

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }

      const data = await response.json();
      const assistantMessage = {
        id: `assistant-${Date.now()}`,
        sender: 'assistant',
        text: data.reply || 'No statutory answer returned.',
        citations: data.citations || [],
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.warn('Backend chat API failed, engaging client fallback:', err);
      // Client-side fallback handler
      const fallbackReply = generateClientFallback(query, lang);
      const fallbackMessage = {
        id: `assistant-${Date.now()}`,
        sender: 'assistant',
        text: fallbackReply.text,
        citations: fallbackReply.citations,
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, fallbackMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSpeechRecognition = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Speech Recognition is not supported in this browser. Please use Chrome or Edge.');
      return;
    }

    if (isListening) {
      if (recognitionRef.current) recognitionRef.current.stop();
      setIsListening(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.lang = lang === 'hi' ? 'hi-IN' : lang === 'ta' ? 'ta-IN' : lang === 'te' ? 'te-IN' : 'en-IN';
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onstart = () => setIsListening(true);
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputText(transcript);
        setIsListening(false);
      };
      recognition.onerror = (event) => {
        console.warn('Speech recognition error:', event.error);
        setIsListening(false);
      };
      recognition.onend = () => setIsListening(false);

      recognitionRef.current = recognition;
      recognition.start();
    } catch (e) {
      console.error('Speech recognition failed to start:', e);
      setIsListening(false);
    }
  };

  const handleSpeakText = (msgId, text) => {
    if (!('speechSynthesis' in window)) {
      alert('Speech Synthesis TTS is not supported in this browser.');
      return;
    }

    if (speakingId === msgId) {
      window.speechSynthesis.cancel();
      setSpeakingId(null);
      return;
    }

    window.speechSynthesis.cancel();
    // Clean text of markdown characters before speaking
    const cleanSpeech = text
      .replace(/#{1,6}\s+/g, '')
      .replace(/\*\*/g, '')
      .replace(/`+/g, '')
      .replace(/>\s+/g, '')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');

    const utterance = new SpeechSynthesisUtterance(cleanSpeech);
    utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-IN';
    utterance.rate = 0.95;

    utterance.onend = () => setSpeakingId(null);
    utterance.onerror = () => setSpeakingId(null);

    setSpeakingId(msgId);
    window.speechSynthesis.speak(utterance);
  };

  const handleClearChat = () => {
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    setSpeakingId(null);
    setMessages([INITIAL_MESSAGE]);
  };

  return (
    <>
      {/* Floating Launcher Button */}
      <div className="chat-float-container">
        {!isOpen && (
          <div className="chat-launcher-tooltip" onClick={() => setIsOpen(true)}>
            <span className="tooltip-pulse" />
            <span className="tooltip-text">{labels.title}</span>
          </div>
        )}
        <button
          type="button"
          className={`chat-float-btn ${isOpen ? 'active' : ''}`}
          onClick={() => {
            setIsOpen(!isOpen);
            setIsMinimized(false);
          }}
          aria-label={isOpen ? labels.close : labels.title}
          title={labels.title}
          id="chat-toggle-button"
        >
          <div className="chat-btn-inner">
            {isOpen ? <X size={24} /> : <MessageSquare size={24} />}
          </div>
          <span className="chat-online-dot" />
        </button>
      </div>

      {/* Expandable Chat Drawer Window */}
      {isOpen && (
        <div className={`chat-window ${isMinimized ? 'minimized' : ''}`} id="sahayak-chat-drawer">
          {/* Window Header */}
          <div className="chat-header">
            <div className="chat-header-info">
              <div className="chat-avatar">
                <Scale size={18} className="avatar-icon" />
              </div>
              <div className="chat-header-text">
                <div className="chat-title-row">
                  <span className="chat-title">{labels.title}</span>
                  <span className="chat-badge">IPR</span>
                </div>
                <div className="chat-sub">
                  <span className="status-indicator-dot" />
                  {labels.status}
                </div>
              </div>
            </div>

            <div className="chat-header-actions">
              <button
                type="button"
                className="chat-action-btn"
                onClick={handleClearChat}
                title={labels.clear}
                aria-label={labels.clear}
              >
                <RotateCcw size={15} />
              </button>
              <button
                type="button"
                className="chat-action-btn"
                onClick={() => setIsMinimized(!isMinimized)}
                title={isMinimized ? labels.maximize : labels.minimize}
                aria-label={isMinimized ? labels.maximize : labels.minimize}
              >
                {isMinimized ? <Maximize2 size={15} /> : <Minimize2 size={15} />}
              </button>
              <button
                type="button"
                className="chat-action-btn close"
                onClick={() => setIsOpen(false)}
                title={labels.close}
                aria-label={labels.close}
              >
                <X size={16} />
              </button>
            </div>
          </div>

          {!isMinimized && (
            <>
              {/* Message Feed */}
              <div className="chat-messages-container">
                {messages.map((msg) => {
                  const isUser = msg.sender === 'user';
                  const isSpeaking = speakingId === msg.id;

                  return (
                    <div
                      key={msg.id}
                      className={`chat-message-row ${isUser ? 'user-row' : 'assistant-row'}`}
                    >
                      {!isUser && (
                        <div className="assistant-avatar-small">
                          <Bot size={15} />
                        </div>
                      )}

                      <div className={`chat-bubble ${isUser ? 'user-bubble' : 'assistant-bubble'}`}>
                        {isUser ? (
                          <div className="chat-user-text">{msg.text}</div>
                        ) : (
                          <>
                            {renderFormattedMarkdown(msg.text)}

                            {msg.citations && msg.citations.length > 0 && (
                              <div className="chat-citations">
                                <div className="citations-label">
                                  <Shield size={12} style={{ marginRight: '4px' }} />
                                  Statutory Citations:
                                </div>
                                <div className="citations-chips">
                                  {msg.citations.map((c, i) => (
                                    <span key={i} className="citation-chip">
                                      {c}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )}

                            <div className="chat-bubble-footer">
                              <button
                                type="button"
                                className={`chat-tts-btn ${isSpeaking ? 'active' : ''}`}
                                onClick={() => handleSpeakText(msg.id, msg.text)}
                                title={isSpeaking ? labels.stop_tts : labels.listen}
                              >
                                {isSpeaking ? <VolumeX size={13} /> : <Volume2 size={13} />}
                                <span>{isSpeaking ? labels.stop_tts : labels.listen}</span>
                              </button>
                              <span className="chat-time">
                                {new Date(msg.timestamp).toLocaleTimeString([], {
                                  hour: '2-digit',
                                  minute: '2-digit',
                                })}
                              </span>
                            </div>
                          </>
                        )}
                      </div>
                    </div>
                  );
                })}

                {isLoading && (
                  <div className="chat-message-row assistant-row">
                    <div className="assistant-avatar-small">
                      <Bot size={15} />
                    </div>
                    <div className="chat-bubble assistant-bubble thinking">
                      <div className="chat-typing-dots">
                        <span className="dot" />
                        <span className="dot" />
                        <span className="dot" />
                      </div>
                      <span className="typing-label">Consulting statutory corpus & RAG...</span>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>

              {/* Quick Suggestion Chips */}
              <div className="chat-suggestions-section">
                <div className="suggestions-header">
                  <HelpCircle size={13} />
                  <span>{labels.ask_suggestions}</span>
                </div>
                <div className="chat-suggestions-scroller">
                  {SUGGESTIONS.map((s, idx) => (
                    <button
                      key={idx}
                      type="button"
                      className="chat-suggestion-chip"
                      onClick={() => handleSendMessage(s.query)}
                      disabled={isLoading}
                    >
                      {s.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Chat Input Bar */}
              <form
                className="chat-input-bar"
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSendMessage();
                }}
              >
                <button
                  type="button"
                  className={`chat-mic-btn ${isListening ? 'listening' : ''}`}
                  onClick={handleSpeechRecognition}
                  title={isListening ? 'Listening...' : 'Voice Input'}
                  aria-label="Voice input"
                >
                  {isListening ? <MicOff size={16} /> : <Mic size={16} />}
                </button>

                <input
                  type="text"
                  className="chat-text-input"
                  placeholder={labels.placeholder}
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  disabled={isLoading}
                  id="chat-user-input"
                />

                <button
                  type="submit"
                  className="chat-send-btn"
                  disabled={!inputText.trim() || isLoading}
                  title="Send message"
                  aria-label="Send message"
                  id="chat-send-btn"
                >
                  <Send size={16} />
                </button>
              </form>
            </>
          )}
        </div>
      )}
    </>
  );
}

// Client-side fallback generator for offline scenarios
function generateClientFallback(query, lang) {
  const q = query.toLowerCase();

  if (q.includes('3(p)') || q.includes('traditional knowledge') || q.includes('tkdl')) {
    return {
      text: `### Section 3(p) & Traditional Knowledge (TKDL)
**Section 3(p)** of The Patents Act, 1970 strictly excludes from patentability:
> *"An invention which, in effect, is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components."*

**Key Defensive Actions:**
1. **CSIR-TKDL Cross-Check:** Verify against 500,000+ formulations in classical Samhitas.
2. **Overcoming Section 3(p):** You cannot patent a raw herb or direct classical combination. Novelty requires a specialized synergistic mechanism or a purified bioactive fraction supported by quantitative clinical validation.`,
      citations: ['Patents Act 1970, Section 3(p)', 'CSIR-TKDL', 'Novartis AG v. Union of India'],
    };
  }

  if (q.includes('3(e)') || q.includes('synergy') || q.includes('admixture') || q.includes('chou-talalay') || q.includes('ci')) {
    return {
      text: `### Section 3(e) & Chou-Talalay Synergy Bar
Under **Section 3(e)** of The Patents Act, 1970:
> *"A substance obtained by a mere admixture resulting only in the aggregation of the properties of the components thereof"* is non-patentable.

**Mathematical Synergy Standard:**
- To defeat Section 3(e), the Indian Patent Office requires **Chou-Talalay Combination Index (CI) < 1.0**.
- CI = 1.0 indicates pure additive effect (barred under § 3(e)).
- CI < 1.0 proves supra-additive synergism (e.g., Curcumin + Piperine showing CI = 0.78).`,
      citations: ['Patents Act 1970, Section 3(e)', 'Chou-Talalay Algorithm', 'DCA Rule 158B'],
    };
  }

  if (q.includes('nba') || q.includes('biodiversity') || q.includes('form iii') || q.includes('form 3') || q.includes('abs')) {
    return {
      text: `### National Biodiversity Authority (NBA) & BDA 2002/2023
Section 6 of the Biological Diversity Act, 2002 mandates that **no person shall apply for any patent inside or outside India for any invention based on Indian biological resources without prior approval of the National Biodiversity Authority (NBA)**.

**Statutory Forms:**
- **Form III:** Mandatory prior clearance BEFORE patent grant.
- **Form I:** Commercial utilization by foreign-controlled entities (Section 3 entities).
- **Form II:** Transfer of research results to non-citizens.
- **ABS Fee:** Benefit sharing ranging from 0.1% to 0.5% ex-factory sales slab.`,
      citations: ['Biological Diversity Act 2002, Section 6', 'NBA Form III', 'ABS Guidelines 2024'],
    };
  }

  if (q.includes('aahara') || q.includes('fssai') || q.includes('food')) {
    return {
      text: `### FSSAI Ayurveda Aahara Regulations (2022)
Food Safety and Standards (Ayurveda Aahara) Regulations, 2022 govern food prepared in accordance with classical Ayurvedic treatises:
- Must use Schedule A classical texts only.
- Prohibited from containing synthetic vitamins, minerals, or isolated amino acids.
- Labeling must display the dedicated **Ayurveda Aahara Logo**.
- **Crucial Rule:** Cannot make medicinal therapeutic or preventive cure claims.`,
      citations: ['FSSAI Ayurveda Aahara 2022', 'Drugs & Cosmetics Act 1940', 'Food Safety Act 2006'],
    };
  }

  if (q.includes('sih') || q.includes('project') || q.includes('lethal christ') || q.includes('aiia')) {
    return {
      text: `### IP-SAKTI Sahayak — Statutory Intelligence Overview
**Problem Statement ID:** SIH26045
**Client Ministry:** Ministry of Ayush & All India Institute of Ayurveda (AIIA)
**Platform Purpose:** Statutory IP, bio-resource compliance, and export clearance engine designed to safeguard India's traditional knowledge while accelerating legitimate Ayurvedic biotechnology innovations.
**Engine Features:**
- 35+ Indexed statutory chunks with hybrid vector/BM25 retrieval.
- Tamper-evident DPDP 2023 SHA-256 Audit Ledger.
- Multilingual Project Bhashini NLI translation.
- Automated NBA Form 1–4 pre-filing dossiers.`,
      citations: ['SIH26045', 'Ministry of Ayush', 'AIIA', 'Team Lethal Christ'],
    };
  }

  return {
    text: `### Sahayak Statutory Guidance
Regarding your inquiry: *"**${query}**"*

In Ayurvedic intellectual property and regulatory compliance, every innovation must satisfy three critical statutory hurdles:
1. **Patents Act 1970 § 3(p):** Traditional knowledge prior art clearance via CSIR-TKDL.
2. **Patents Act 1970 § 3(e):** Proving non-obvious synergy (Chou-Talalay CI < 1.0) rather than a mere admixture.
3. **Biological Diversity Act 2002 § 6:** Securing NBA Form III approval before patent grant.

Enter specific provisions, botanical species, or export jurisdictions for statutory references.`,
    citations: ['Patents Act 1970', 'Biological Diversity Act 2002', 'DCA 1940'],
  };
}
