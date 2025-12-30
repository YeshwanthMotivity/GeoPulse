import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, MapPin, ChevronRight, BookOpen } from 'lucide-react';
import '../App.css';

const HomePage = ({ setGlobalCountry }) => {
    const [countries, setCountries] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [guide, setGuide] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const navigate = useNavigate();

    useEffect(() => {
        fetchCountries();
    }, []);

    const fetchCountries = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/countries");
            const data = await response.json();
            setCountries(data);
        } catch (error) {
            console.error("Error fetching countries:", error);
        }
    };

    const loadCountryData = async (countryName) => {
        setLoading(true);
        setGlobalCountry(countryName);

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/guide/${countryName}`);
            if (!response.ok) throw new Error("Country data not found");
            const data = await response.json();
            setGuide(data);
        } catch (err) {
            setError("Country not found.");
            setGuide(null);
        } finally {
            setLoading(false);
        }
    };

    const getFlag = (name) => {
        const map = {
            "Japan": "🇯🇵", "France": "🇫🇷", "Italy": "🇮🇹", "India": "🇮🇳", "China": "🇨🇳",
            "United States": "🇺🇸", "Brazil": "🇧🇷", "Germany": "🇩🇪", "United Kingdom": "🇬🇧",
            "Spain": "🇪🇸", "Australia": "🇦🇺", "Canada": "🇨🇦", "Mexico": "🇲🇽", "Russia": "🇷🇺",
            "South Africa": "🇿🇦", "Egypt": "🇪🇬", "Argentina": "🇦🇷", "Turkey": "🇹🇷"
        };
        return map[name] || "🌍";
    };

    const getIcon = (category) => {
        const map = {
            "GREETING": "🤝", "ETIQUETTE": "🙏", "DINING": "🍽️",
            "DOs & DONTs": "✅", "COMMON MISTAKES": "⚠️", "SITUATIONAL TIPS": "💡"
        };
        return map[category] || "📘";
    };

    const filteredCountries = countries.filter(c =>
        c.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="container fade-in">
            <div className="bg-blob-container">
                <div className="blob blob-1"></div>
                <div className="blob blob-2"></div>
                <div className="blob blob-3"></div>
            </div>

            {/* HERO SECTION - Show conditionally if no guide selected */}
            {!guide && (
                <div className="hero-section">
                    <h1 className="hero-title">
                        Explore the <span className="text-highlight">World</span>
                    </h1>
                    <p className="hero-desc">
                        Master cultural norms, etiquette, and traditions through interactive guides.
                    </p>

                    <div className="search-wrapper">
                        <Search className="search-icon-inside" size={20} />
                        <input
                            type="text"
                            className="search-input-field"
                            placeholder="Search countries (e.g., Japan)..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                </div>
            )}

            {/* COUNTRY GRID - Show if no guide selected */}
            {!guide ? (
                <div className="country-grid">
                    {filteredCountries.map((c) => (
                        <div
                            key={c.id}
                            className="country-card"
                            onClick={() => loadCountryData(c.name)}
                        >
                            <div className="card-flag-area">
                                {getFlag(c.name)}
                            </div>
                            <div className="card-content">
                                <div className="card-region">
                                    <MapPin size={12} /> {c.region || "World"}
                                </div>
                                <h3 className="card-title">{c.name}</h3>
                                <p className="card-desc">Click to read the guide and test your knowledge.</p>

                                <button className="btn-card-action">
                                    Read Guide <ChevronRight size={16} />
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                // GUIDE DETAIL VIEW
                <div className="guide-view slide-up">
                    {/* Guide Header */}
                    <div className="hero-section" style={{ marginBottom: '2rem' }}>
                        <div className="card-flag-area" style={{ background: 'transparent', height: 'auto', fontSize: '4rem', marginBottom: '1rem' }}>
                            {getFlag(guide.country)}
                        </div>
                        <h1 className="hero-title" style={{ fontSize: '3rem' }}>{guide.country}</h1>
                        <p className="hero-desc">Language: {guide.language}</p>

                        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '2rem' }}>
                            <button className="btn-large btn-dark" onClick={() => setGuide(null)}>
                                Back to Search
                            </button>
                            <button className="btn-large btn-blue" onClick={() => navigate(`/quiz/${guide.country}`)}>
                                Take Quiz <ChevronRight size={18} />
                            </button>
                        </div>
                    </div>

                    {/* Guide Cards Grid */}
                    <div className="country-grid">
                        {guide.details.map((item, index) => (
                            <div key={index} className="country-card" style={{ cursor: 'default', transform: 'none' }}>
                                <div className="card-content">
                                    <div className="card-region" style={{ fontSize: '0.9rem' }}>
                                        {getIcon(item.category)} {item.category}
                                    </div>
                                    <h3 className="card-title">{item.topic} {item.is_strict && <span style={{ color: 'red', fontSize: '0.7em' }}>(STRICT)</span>}</h3>
                                    <p className="card-desc" style={{ WebkitLineClamp: 'unset', color: '#374151' }}>
                                        {item.description}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default HomePage;
