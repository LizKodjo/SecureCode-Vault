export default function SnippetSection({
  snippets,
  newSnippet,
  setNewSnippet,
  onCreateSnippet,
  onShareSnippet,
  loading,
}) {
  console.log("SnippetSection rendered with newSnippet:", newSnippet); // Debug

  const handleInputChange = (field, value) => {
    console.log(`Updating ${field}:`, value); // Debug
    setNewSnippet((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  return (
    <div className="snippet-section">
      {/* Create New Snippet */}
      <div className="card">
        <h2>Create New Snippet</h2>
        <div className="snippet-form">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              console.log("Form submitted with:", newSnippet); // Debug
              onCreateSnippet();
            }}
          >
            <div className="form-group">
              <label>Title</label>
              <input
                type="text"
                value={newSnippet.title}
                onChange={(e) => handleInputChange("title", e.target.value)}
                placeholder="Snippet title"
                required
              />
            </div>

            <div className="form-group">
              <label>Language</label>
              <select
                value={newSnippet.language}
                onChange={(e) => handleInputChange("language", e.target.value)}
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="typescript">TypeScript</option>
                <option value="java">Java</option>
                <option value="cpp">C++</option>
                <option value="html">HTML</option>
                <option value="css">CSS</option>
                <option value="sql">SQL</option>
              </select>
            </div>

            <div className="form-group">
              <label>Code</label>
              <textarea
                value={newSnippet.code}
                onChange={(e) => handleInputChange("code", e.target.value)}
                placeholder="Paste your code here..."
                rows="6"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary"
            >
              {loading ? "Creating..." : "Create Snippet"}
            </button>
          </form>
        </div>
      </div>

      {/* Snippets List */}
      <div className="card">
        <h2>My Snippets ({snippets.length})</h2>
        {snippets.length === 0 ? (
          <p className="no-snippets">
            No snippets yet. Create your first one above!
          </p>
        ) : (
          <div className="snippets-list">
            {snippets.map((snippet) => (
              <div key={snippet.id} className="snippet-item">
                <div className="snippet-header">
                  <h3>{snippet.title}</h3>
                  <span className="language-tag">{snippet.language}</span>
                </div>
                <pre className="snippet-code">{snippet.code}</pre>
                <div className="snippet-actions">
                  <button
                    onClick={() => onShareSnippet(snippet.id)}
                    className="btn btn-secondary"
                  >
                    🔗 Share
                  </button>
                  <span className="snippet-date">
                    Created: {new Date(snippet.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
