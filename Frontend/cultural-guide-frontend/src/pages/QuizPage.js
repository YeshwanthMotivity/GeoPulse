import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Award, RefreshCcw, Home, ChevronLeft } from 'lucide-react';
import '../App.css';

const QuizPage = () => {
    const { countryName } = useParams();
    const navigate = useNavigate();

    const [quizData, setQuizData] = useState([]);
    const [loading, setLoading] = useState(true);

    const [currentIndex, setCurrentIndex] = useState(0);
    const [score, setScore] = useState(0);
    const [showResult, setShowResult] = useState(false);
    const [selectedOption, setSelectedOption] = useState(null);
    const [isCorrect, setIsCorrect] = useState(null);

    useEffect(() => {
        fetchQuiz();
    }, [countryName]);

    const fetchQuiz = async () => {
        try {
            const res = await fetch(`http://127.0.0.1:8000/api/quiz/${countryName}`);
            if (res.ok) {
                const data = await res.json();
                setQuizData(data);
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleOptionClick = (option) => {
        if (selectedOption) return;
        setSelectedOption(option);

        // Check answer
        const currentQ = quizData[currentIndex];
        const correct = option === currentQ.answer;

        setIsCorrect(correct);
        if (correct) setScore(score + 1);

        setTimeout(() => {
            if (currentIndex + 1 < quizData.length) {
                setCurrentIndex(currentIndex + 1);
                setSelectedOption(null);
                setIsCorrect(null);
            } else {
                setShowResult(true);
            }
        }, 1000); // Faster transition
    };

    if (loading) return <div className="quiz-container">Loading...</div>;

    if (!quizData || quizData.length === 0) return (
        <div className="quiz-container" style={{ textAlign: 'center' }}>
            <h2>No quiz data found for {countryName}</h2>
            <button className="btn-back" onClick={() => navigate("/")}>Go Home</button>
        </div>
    );

    // Result View
    if (showResult) {
        return (
            <div className="container fade-in">
                <div className="bg-blob-container">
                    <div className="blob blob-1"></div>
                </div>
                <div className="result-box">
                    <div className="award-icon-box">
                        <Award size={64} />
                    </div>
                    <h2 className="result-title">Quiz Complete!</h2>
                    <p className="result-score">
                        You scored <span className="score-highlight">{score}</span> out of {quizData.length}
                    </p>
                    <div className="result-actions">
                        <button className="btn-large btn-dark" onClick={() => navigate("/")}>
                            <Home size={20} /> Back to Home
                        </button>
                        <button className="btn-large btn-blue" onClick={() => {
                            setScore(0); setCurrentIndex(0); setShowResult(false); setSelectedOption(null);
                        }}>
                            <RefreshCcw size={20} /> Try Again
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    // Question View
    const progressPercent = ((currentIndex + 1) / quizData.length) * 100;
    const currentQ = quizData[currentIndex];

    return (
        <div className="quiz-container fade-in">
            <button className="btn-back" onClick={() => navigate("/")}>
                <ChevronLeft size={16} /> Exit Quiz
            </button>

            <div className="quiz-header-row">
                <div>
                    <span className="q-count">Question {currentIndex + 1} of {quizData.length}</span>
                    <h2 className="q-heading">{countryName} Knowledge</h2>
                </div>
            </div>

            <div className="progress-bar-bg">
                <div className="progress-bar-fill" style={{ width: `${progressPercent}%` }}></div>
            </div>

            <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '2rem', lineHeight: '1.4' }}>
                {currentQ.question}
            </h3>

            <div className="options-list">
                {currentQ.options.map((opt, i) => {
                    let statusClass = "";
                    if (selectedOption) {
                        if (opt === currentQ.answer) statusClass = "correct";
                        else if (opt === selectedOption) statusClass = "wrong";
                        else statusClass = "dimmed";
                    }

                    return (
                        <button
                            key={i}
                            className={`option-button ${statusClass}`}
                            onClick={() => handleOptionClick(opt)}
                            disabled={selectedOption !== null}
                        >
                            {opt}
                        </button>
                    );
                })}
            </div>
        </div>
    );
};

export default QuizPage;
