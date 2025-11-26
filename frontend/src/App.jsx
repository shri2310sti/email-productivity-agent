import React, { useState, useEffect } from 'react';
import { Mail, Send, Settings, MessageSquare, Inbox, Edit, Save, Trash2, RefreshCw, Download, Database, AlertCircle, CheckCircle, Info } from 'lucide-react';
import * as api from './services/api';

function App() {
  const [emails, setEmails] = useState([]);
  const [selectedEmail, setSelectedEmail] = useState(null);
  const [prompts, setPrompts] = useState({});
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [drafts, setDrafts] = useState([]);
  const [activeTab, setActiveTab] = useState('inbox');
  const [loading, setLoading] = useState(false);
  const [editingPrompt, setEditingPrompt] = useState(null);
  const [status, setStatus] = useState({ message: '', type: '' });

  useEffect(() => {
    loadPrompts();
    loadEmails();
    loadDrafts();
  }, []);

  const showStatus = (message, type = 'info') => {
    setStatus({ message, type });
    setTimeout(() => setStatus({ message: '', type: '' }), 5000);
  };

  const loadEmails = async () => {
    try {
      const response = await api.getEmails();
      setEmails(response.data.emails);
    } catch (error) {
      console.error('Error loading emails:', error);
    }
  };

  const loadPrompts = async () => {
    try {
      const response = await api.getPrompts();
      setPrompts(response.data.prompts);
    } catch (error) {
      console.error('Error loading prompts:', error);
    }
  };

  const loadDrafts = async () => {
    try {
      const response = await api.getDrafts();
      setDrafts(response.data.drafts);
    } catch (error) {
      console.error('Error loading drafts:', error);
    }
  };

  const loadMockInbox = async () => {
    setLoading(true);
    showStatus('Loading mock inbox with 20 sample emails...', 'loading');
    try {
      const response = await api.loadMockEmails();
      await loadEmails();
      showStatus(`✅ ${response.data.message || 'Mock inbox loaded successfully!'}`, 'success');
    } catch (error) {
      showStatus('❌ Error loading mock inbox: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const fetchNewEmails = async () => {
    setLoading(true);
    showStatus('Fetching emails from Gmail...', 'loading');
    try {
      await api.fetchEmails(20);
      await loadEmails();
      showStatus('✅ Emails fetched successfully from Gmail!', 'success');
    } catch (error) {
      console.error(error);
      showStatus('Gmail not configured. Please use "Load Mock Inbox" or set up Gmail credentials.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const processAllEmails = async () => {
    setLoading(true);
    showStatus('Processing emails with AI... This may take a minute.', 'loading');
    try {
      const response = await api.processEmails();
      await loadEmails();
      showStatus(`✅ Processed ${response.data.processed}/${response.data.total} emails successfully!`, 'success');
    } catch (error) {
      showStatus('❌ Error: ' + (error.response?.data?.error || error.message), 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleChatSubmit = async () => {
    if (!chatInput.trim() || !selectedEmail) return;

    const userMessage = { role: 'user', content: chatInput };
    setChatMessages([...chatMessages, userMessage]);
    setChatInput('');
    setLoading(true);

    try {
      const history = chatMessages.map(m => `${m.role}: ${m.content}`).join('\n');
      const response = await api.chatWithAgent(selectedEmail, chatInput, history);
      const assistantMessage = { role: 'assistant', content: response.data.response };
      setChatMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = { role: 'assistant', content: 'Sorry, I encountered an error processing your request.' };
      setChatMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const generateDraft = async (email) => {
    setLoading(true);
    showStatus('Generating draft reply with AI...', 'loading');
    try {
      await api.generateDraft(email);
      await loadDrafts();
      setActiveTab('drafts');
      showStatus('✅ Draft generated successfully! Check Drafts tab.', 'success');
    } catch (error) {
      showStatus('❌ Error generating draft: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const savePrompts = async () => {
    setLoading(true);
    try {
      await api.updatePrompts(prompts);
      setEditingPrompt(null);
      showStatus('✅ Prompts saved! Process emails again to see changes.', 'success');
    } catch (error) {
      showStatus('❌ Error saving prompts: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const StatusAlert = () => {
    if (!status.message) return null;

    const icons = {
      success: <CheckCircle className="w-5 h-5" />,
      error: <AlertCircle className="w-5 h-5" />,
      loading: <RefreshCw className="w-5 h-5 animate-spin" />,
      info: <Info className="w-5 h-5" />
    };

    const colors = {
      success: 'bg-green-50 text-green-800 border-green-200',
      error: 'bg-red-50 text-red-800 border-red-200',
      loading: 'bg-blue-50 text-blue-800 border-blue-200',
      info: 'bg-blue-50 text-blue-800 border-blue-200'
    };

    return (
      <div className={`mt-4 px-4 py-3 rounded-lg border flex items-start gap-3 ${colors[status.type]}`}>
        {icons[status.type]}
        <span className="flex-1">{status.message}</span>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div className="flex items-center space-x-3">
              <Mail className="w-8 h-8 text-indigo-600" />
              <div>
                <h1 className="text-3xl font-bold text-gray-800">Email Productivity Agent</h1>
                <p className="text-sm text-gray-500">Prompt-Driven AI Email Assistant</p>
              </div>
            </div>
            <div className="flex items-center space-x-2 flex-wrap gap-2">
              <button
                onClick={loadMockInbox}
                disabled={loading}
                className="flex items-center space-x-2 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 disabled:opacity-50 transition"
              >
                <Database className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                <span>Load Mock Inbox</span>
              </button>
              <button
                onClick={fetchNewEmails}
                disabled={loading}
                className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 transition"
              >
                <Download className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                <span>Fetch Real Gmail</span>
              </button>
              <button
                onClick={processAllEmails}
                disabled={loading || emails.length === 0}
                className="flex items-center space-x-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition"
              >
                <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                <span>Process All</span>
              </button>
            </div>
          </div>

          <StatusAlert />

          {emails.length === 0 && !loading && !status.message && (
            <div className="mt-4 px-4 py-3 bg-yellow-50 text-yellow-800 rounded-lg border border-yellow-200">
              👋 <strong>Welcome!</strong> Click <strong>"Load Mock Inbox"</strong> to start with 20 sample emails, or <strong>"Fetch Real Gmail"</strong> if you've configured Gmail.
            </div>
          )}
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow-lg mb-6">
          <div className="flex border-b overflow-x-auto">
            {[
              { key: 'inbox', label: 'Inbox', icon: Inbox, count: emails.length },
              { key: 'chat', label: 'Chat', icon: MessageSquare },
              { key: 'drafts', label: 'Drafts', icon: Edit, count: drafts.length },
              { key: 'prompts', label: 'Prompts', icon: Settings }
            ].map(tab => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`flex-1 px-6 py-4 text-center font-medium whitespace-nowrap flex items-center justify-center gap-2 ${activeTab === tab.key
                  ? 'border-b-2 border-indigo-600 text-indigo-600'
                  : 'text-gray-600 hover:text-indigo-600'
                  }`}
              >
                <tab.icon className="w-5 h-5" />
                <span className="capitalize">{tab.label}</span>
                {tab.count !== undefined && (
                  <span className="ml-1 px-2 py-0.5 bg-gray-200 text-gray-700 text-xs rounded-full">
                    {tab.count}
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Content Area - Inbox */}
        {activeTab === 'inbox' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1 bg-white rounded-lg shadow-lg p-4 max-h-[600px] overflow-y-auto">
              <h2 className="text-xl font-bold mb-4 text-black">Inbox ({emails.length})</h2>
              {emails.length === 0 ? (
                <div className="text-center py-12">
                  <Inbox className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500 mb-2">No emails loaded</p>
                  <p className="text-sm text-gray-400">Click "Load Mock Inbox" to get started</p>
                </div>
              ) : (
                emails.map(email => (
                  <div
                    key={email.id}
                    onClick={() => {
                      setSelectedEmail(email);
                      setChatMessages([]);
                    }}
                    className={`p-4 mb-2 rounded-lg cursor-pointer border-2 transition ${selectedEmail?.id === email.id
                      ? 'border-indigo-600 bg-indigo-50'
                      : 'border-black-200 hover:border-indigo-300 hover:shadow-md'
                      }`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <span className="font-semibold text-sm truncate flex-1 text-black">{email.from}</span>
                      {email.category && (
                        <span
                          className={`px-2 py-1 rounded text-xs whitespace-nowrap ml-2 ${email.category.toLowerCase().includes('important')
                            ? 'bg-red-100 text-red-800'
                            : email.category.toLowerCase().includes('to-do') || email.category.toLowerCase().includes('todo')
                              ? 'bg-yellow-100 text-yellow-800'
                              : email.category.toLowerCase().includes('newsletter')
                                ? 'bg-blue-100 text-blue-800'
                                : email.category.toLowerCase().includes('spam')
                                  ? 'bg-gray-100 text-gray-800'
                                  : 'bg-purple-100 text-purple-800'
                            }`}
                        >
                          {email.category}
                        </span>
                      )}
                    </div>
                    <div className="text-sm font-medium text-gray-800 mb-1 truncate">{email.subject}</div>
                    <div className="text-xs text-gray-500">{new Date(email.timestamp).toLocaleString()}</div>
                  </div>
                ))
              )}
            </div>

            <div className="lg:col-span-2 bg-white rounded-lg shadow-lg p-6">
              {selectedEmail ? (
                <>
                  <div className="mb-6">
                    <h3 className="text-2xl font-bold mb-2">{selectedEmail.subject}</h3>
                    <div className="text-sm text-gray-600 mb-4 flex items-center justify-between">
                      <span>
                        From: <strong>{selectedEmail.from}</strong>
                      </span>
                      <span className="text-xs">{new Date(selectedEmail.timestamp).toLocaleString()}</span>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg mb-4 max-h-96 overflow-y-auto">
                      <p className="text-black whitespace-pre-wrap">{selectedEmail.body}</p>
                    </div>
                    {selectedEmail.actionItems && selectedEmail.actionItems.length > 0 && (
                      <div className="bg-pink-500 p-4 rounded-lg mb-4 border border-yellow-200">
                        <h4 className="font-semibold mb-2 flex items-center">📋 Action Items Extracted:</h4>
                        <ul className="list-disc list-inside space-y-1">
                          {selectedEmail.actionItems.map((item, idx) => (
                            <li key={idx} className="text-sm">
                              <strong>{item.task}</strong>{' '}
                              {item.deadline && <span className="text-black-600">(Due: {item.deadline})</span>}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                  <button
                    onClick={() => generateDraft(selectedEmail)}
                    disabled={loading}
                    className="flex items-center space-x-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition"
                  >
                    <Send className="w-4 h-4" />
                    <span>Generate Draft Reply</span>
                  </button>
                </>
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-gray-400">
                  <MessageSquare className="w-16 h-16 mb-4" />
                  <p>Select an email to view details</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Chat Tab */}
        {activeTab === 'chat' && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold mb-4">📧 Email Agent Chat</h2>
            {selectedEmail ? (
              <>
                <div className="bg-indigo-50 p-4 rounded-lg mb-4 border border-indigo-200">
                  <p className="text-sm text-indigo-800">
                    Chatting about: <strong>{selectedEmail.subject}</strong>
                  </p>
                  <p className="text-xs text-indigo-600 mt-1">From: {selectedEmail.from}</p>
                </div>
                <div className="h-96 overflow-y-auto mb-4 space-y-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
                  {chatMessages.length === 0 ? (
                    <div className="text-center text-gray-400 py-12">
                      <MessageSquare className="w-12 h-12 mx-auto mb-2 opacity-50" />
                      <p>Start a conversation about this email...</p>
                      <p className="text-xs mt-2">Try: "Summarize this email" or "What actions do I need to take?"</p>
                    </div>
                  ) : (
                    chatMessages.map((msg, idx) => (
                      <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div
                          className={`max-w-2xl p-4 rounded-lg ${msg.role === 'user'
                            ? 'bg-indigo-600 text-white'
                            : 'bg-white text-gray-800 border border-gray-200 shadow-sm'
                            }`}
                        >
                          {msg.content}
                        </div>
                      </div>
                    ))
                  )}
                </div>
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={chatInput}
                    onChange={e => setChatInput(e.target.value)}
                    onKeyPress={e => e.key === 'Enter' && !e.shiftKey && handleChatSubmit()}
                    placeholder="Ask about this email... (e.g., 'What should I do about this?')"
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
                  />
                  <button
                    onClick={handleChatSubmit}
                    disabled={loading || !chatInput.trim()}
                    className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition"
                  >
                    Send
                  </button>
                </div>
              </>
            ) : (
              <div className="flex flex-col items-center justify-center h-96 text-gray-400">
                <MessageSquare className="w-16 h-16 mb-4" />
                <p>Select an email from the inbox to start chatting</p>
              </div>
            )}
          </div>
        )}

        {/* Drafts Tab */}
        {activeTab === 'drafts' && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold mb-4">✉️ Draft Emails ({drafts.length})</h2>
            {drafts.length > 0 ? (
              <div className="space-y-4">
                {drafts.map(draft => (
                  <div key={draft.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <div className="text-sm text-gray-600">
                          To: <strong>{draft.to}</strong>
                        </div>
                        <div className="font-semibold text-lg">{draft.subject}</div>
                      </div>
                      <button
                        onClick={() => {
                          api.deleteDraft(draft.id);
                          loadDrafts();
                        }}
                        className="text-red-600 hover:text-red-800 p-2 hover:bg-red-50 rounded transition"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                    <div className="bg-gray-50 p-3 rounded max-h-48 overflow-y-auto border border-gray-200">
                      <p className="text-sm whitespace-pre-wrap">{draft.body}</p>
                    </div>
                    <div className="text-xs text-gray-500 mt-2 flex justify-between items-center">
                      <span>Created: {new Date(draft.createdAt).toLocaleString()}</span>
                      <span className="text-green-600">✓ Saved as draft (not sent)</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-64 text-gray-400">
                <Edit className="w-16 h-16 mb-4" />
                <p>No drafts yet</p>
                <p className="text-sm mt-2">Generate a draft from an email in your inbox</p>
              </div>
            )}
          </div>
        )}

        {/* Prompts Tab */}
        {activeTab === 'prompts' && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">⚙️ Prompt Configuration (Agent Brain)</h2>
              <span className="text-sm text-gray-500">Edit prompts to change AI behavior</span>
            </div>
            <div className="mb-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-sm text-blue-800">
                💡 <strong>Tip:</strong> These prompts control how the AI categorizes emails, extracts tasks, and
                generates replies. Edit them to customize the agent's behavior, then click "Process All" to see
                changes.
              </p>
            </div>
            <div className="space-y-6">
              {Object.entries(prompts).map(([key, value]) => (
                <div key={key} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="font-semibold capitalize text-lg">
                      {key.replace(/([A-Z])/g, ' $1').trim()} Prompt
                    </h3>
                    {editingPrompt === key ? (
                      <button
                        onClick={savePrompts}
                        className="flex items-center space-x-1 text-green-600 hover:text-green-800 px-3 py-1 hover:bg-green-50 rounded transition"
                      >
                        <Save className="w-4 h-4" />
                        <span>Save</span>
                      </button>
                    ) : (
                      <button
                        onClick={() => setEditingPrompt(key)}
                        className="flex items-center space-x-1 text-indigo-600 hover:text-indigo-800 px-3 py-1 hover:bg-indigo-50 rounded transition"
                      >
                        <Edit className="w-4 h-4" />
                        <span>Edit</span>
                      </button>
                    )}
                  </div>
                  {editingPrompt === key ? (
                    <textarea
                      value={value}
                      onChange={e => setPrompts({ ...prompts, [key]: e.target.value })}
                      className="w-full h-32 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 font-mono text-sm"
                    />
                  ) : (
                    <div className="bg-gray-50 p-3 rounded border border-gray-200">
                      <p className="text-sm text-gray-700 whitespace-pre-wrap">{value}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;