import { useState } from "react";
import axios from "axios";
import "./App.css"; // This connects the files!

function App() {
  const [text, setText] = useState("");
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/wanikani/", {
        input: text,
      });
      setResults(response.data);
    } catch (error) {
      alert("Check if FastAPI is running!");
    }
    setLoading(false);
  };

  const loadExample = () => {
    // From NHK NEws Easy (https://news.web.nhk/news/easy/ne2026022012083/ne2026022012083.html)
    const example = `
千葉県の動物園ぬいぐるみで遊ぶ子どもの猿が人気

千葉県市川市の動物園で、ぬいぐるみで遊ぶ子どもの猿が人気になっています。

この猿は「パンチ」という名前で、去年7月に生まれました。母親が世話をしなかったので、動物園の人がミルクをあげて育てました。

動物園の人がオランウータンのぬいぐるみを「パンチ」にあげると、いつも持って歩くようになりました。ぬいぐるみを母親の代わりのようにして抱きついて遊んでいます。

動物園には、「パンチ」を見に、たくさんの人が来ています。動物園の人は「思ったより多くの人が来て驚いています」と話していました。

(From NHK News Easy (https://news.web.nhk/news/easy/ne2026022012083/ne2026022012083.html))
`;
    setText(example);
  };

  const getLevelClass = (level: number) => {
    if (level <= 10) return "lvl-beginner";
    if (level <= 20) return "lvl-pleasant";
    if (level <= 30) return "lvl-painful";
    if (level <= 40) return "lvl-death";
    return "lvl-hell";
  };

  return (
    <div className="app-container">
      <div className="content-wrapper">
        <h1>Japanese Text Analyzer</h1>
        <h5>日本語を大好き!</h5>

        <textarea
          className="text-input"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste Japanese text here..."
        />

        <br />
        <button onClick={loadExample} className="example-btn">
          Try an Example
        </button>

        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Level"}
        </button>

        {results && (
          <div className="results-grid">
            <section>
              <h3 className="section-title-kanji">Kanji Levels</h3>
              <div className="badge-list">
                {Object.entries(results.kanji).map(([char, level]) => (
                  <div
                    key={char}
                    className={`level-badge ${getLevelClass(level as number)}`}
                  >
                    <div className="level-number">Lvl {level as number}</div>
                    <div className="level-char">{char}</div>
                  </div>
                ))}
              </div>
            </section>

            <section>
              <h3 className="section-title-vocab">Vocabulary Levels </h3>
              <div className="badge-list">
                {Object.entries(results.vocab).map(([char, level]) => (
                  <div
                    key={char}
                    className={`level-badge ${getLevelClass(level as number)}`}
                  >
                    <div className="level-number">Lvl {level as number}</div>
                    <div className="level-char">{char}</div>
                  </div>
                ))}
              </div>
            </section>
            <div className="legend">
              <span className="legend-item">
                <span className="dot dot-beginner">●</span> 1-10
              </span>
              <span className="legend-item">
                <span className="dot dot-pleasant">●</span> 11-20
              </span>
              <span className="legend-item">
                <span className="dot dot-painful">●</span> 21-30
              </span>
              <span className="legend-item">
                <span className="dot dot-death">●</span> 31-40
              </span>
              <span className="legend-item">
                <span className="dot dot-hell">●</span> 41+
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
