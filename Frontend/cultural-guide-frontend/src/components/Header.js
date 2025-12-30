import React from 'react';
import { Link } from 'react-router-dom';
import { Globe } from 'lucide-react';
import '../App.css';

const Header = () => {
    return (
        <header className="app-header">
            <div className="header-inner">
                <Link to="/" className="brand-link">
                    <div className="logo-box">
                        <Globe size={24} />
                    </div>
                    <span className="brand-name">GeoPulse</span>
                </Link>

                <nav className="nav-links">
                    <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>Home</Link>
                </nav>

                <div className="user-avatar"></div>
            </div>
        </header>
    );
};

export default Header;
