import {useState} from 'react'

function ThemeInput({onSubmit}) {
    const [theme, setTheme] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (theme.trim() === '') {
            setError('Theme cannot be empty');
            return;
        }
        setError('');
        onSubmit(theme);
    }

    return <div className="theme-input-container">
        <h1>Generate your adventure</h1>
        <p>Enter a theme for your adventure:</p>

        <form onSubmit={handleSubmit}>
            <div className="input-group">
                <input
                    type="text"
                    value={theme}
                    onChange={(e) => setTheme(e.target.value)}
                    placeholder="Enter a theme..."
                    className={error ? 'error': ''}
                />
            {error && <p className="error-text">{error}</p>}
            </div>
            <button className='generate-btn' type="submit">Generate story</button>

        </form>
    </div>
}

export default ThemeInput;